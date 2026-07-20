#!/usr/bin/env python3
"""Generate employee-card character art with the OpenAI Images API.

Reads a roster of employees, pairs each employee's reference photos with a
shared set of style-reference images, and asks the OpenAI Images API to
produce card art that matches the style while preserving the employee's
likeness. Run with --dry-run to inspect every request before spending API
credits.
"""

from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import json
import mimetypes
import os
from pathlib import Path
import sys
import textwrap
import time
import tomllib
from urllib import error, request


API_URL = "https://api.openai.com/v1/images"
DEFAULT_MODEL = "gpt-image-2"
DEFAULT_SIZE = "1024x1024"
DEFAULT_QUALITY = "high"
DEFAULT_FORMAT = "png"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
RETRYABLE_STATUS = {429, 500, 502, 503, 504}
MAX_ATTEMPTS = 4

DEFAULT_STYLE = """\
Stylized character-portrait illustration with clean shapes, confident line
work, and a simple flat background. Friendly and professional, readable at
small card size."""

SUBJECT_REFERENCE_PARAGRAPH = """\
The {which} attached image(s) are reference photos of {name}. Use them only
to capture likeness: facial structure, hair, skin tone, glasses or facial
hair, and overall build. Make the final image an original illustration, not
a photographic copy of any single reference."""

STYLE_REFERENCE_PARAGRAPH = """\
The {which} attached image(s) are style references from the existing card
set. Match their artistic style, rendering technique, palette, background
treatment, and level of detail exactly, so the new card feels like part of
the same set. Do not borrow faces, identity, or clothing from the style
references."""

AVOID_PARAGRAPH = """\
Avoid: text, captions, name tags, logos, watermarks, frames, extra people,
distorted anatomy, busy background."""


def cards_root() -> Path:
    return Path(__file__).resolve().parent


def load_roster(path: Path) -> dict[str, object]:
    if not path.exists():
        raise SystemExit(f"Roster file not found: {path}")
    with path.open("rb") as handle:
        return tomllib.load(handle)


def discover_images(directory: Path) -> list[Path]:
    if not directory.is_dir():
        return []
    return sorted(
        path
        for path in directory.iterdir()
        if path.suffix.lower() in IMAGE_EXTENSIONS
    )


def employee_references(root: Path, employee: dict[str, object]) -> list[Path]:
    explicit = employee.get("references")
    if explicit:
        return [root / str(item) for item in explicit]
    return discover_images(root / "employees" / str(employee["slug"]))


def build_prompt(
    employee: dict[str, object],
    style: str,
    subject_count: int,
    style_count: int,
) -> str:
    if override := employee.get("prompt"):
        return str(override).strip()

    name = str(employee.get("name") or employee["slug"])
    role = employee.get("role")
    role_clause = f", {role}," if role else ""

    paragraphs = [
        f"Create a square character portrait of {name}{role_clause} for an "
        "employee trading card."
    ]

    if subject_count:
        which = f"first {subject_count}" if style_count else "attached"
        paragraphs.append(
            SUBJECT_REFERENCE_PARAGRAPH.format(which=which, name=name)
        )
    if style_count:
        which = f"remaining {style_count}" if subject_count else "attached"
        paragraphs.append(STYLE_REFERENCE_PARAGRAPH.format(which=which))

    paragraphs.append(f"Style: {style.strip()}")

    background = (
        "simple background consistent with the style references"
        if style_count
        else "simple flat background"
    )
    paragraphs.append(
        "Composition: centered head-and-shoulders bust portrait, square crop, "
        "face clearly readable at card-thumbnail size, generous margin around "
        f"the head, {background}."
    )

    if notes := employee.get("notes"):
        paragraphs.append(f"Subject details: {notes}")

    paragraphs.append(AVOID_PARAGRAPH)
    return "\n\n".join(paragraphs)


def encode_multipart(
    fields: dict[str, str],
    files: list[tuple[str, Path]],
    boundary: str,
) -> bytes:
    chunks: list[bytes] = []

    for name, value in fields.items():
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("utf-8"),
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode(
                    "utf-8"
                ),
                value.encode("utf-8"),
                b"\r\n",
            ]
        )

    for name, path in files:
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("utf-8"),
                (
                    f'Content-Disposition: form-data; name="{name}"; '
                    f'filename="{path.name}"\r\n'
                ).encode("utf-8"),
                f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"),
                path.read_bytes(),
                b"\r\n",
            ]
        )

    chunks.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(chunks)


def perform_request(req: request.Request) -> dict[str, object]:
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            with request.urlopen(req, timeout=300) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except error.HTTPError as exc:
            details = exc.read().decode("utf-8", errors="replace")
            if exc.code in RETRYABLE_STATUS and attempt < MAX_ATTEMPTS:
                delay = 2**attempt
                print(
                    f"  OpenAI returned {exc.code}; retrying in {delay}s "
                    f"(attempt {attempt}/{MAX_ATTEMPTS})",
                    file=sys.stderr,
                )
                time.sleep(delay)
                continue
            raise SystemExit(
                f"OpenAI API request failed: {exc.code} {exc.reason}\n{details}"
            )
        except error.URLError as exc:
            if attempt < MAX_ATTEMPTS:
                delay = 2**attempt
                print(
                    f"  Network error ({exc.reason}); retrying in {delay}s "
                    f"(attempt {attempt}/{MAX_ATTEMPTS})",
                    file=sys.stderr,
                )
                time.sleep(delay)
                continue
            raise SystemExit(f"OpenAI API request failed: {exc.reason}")
    raise SystemExit("OpenAI API request failed after retries.")


def call_images_api(
    api_key: str,
    prompt: str,
    images: list[Path],
    model: str,
    size: str,
    quality: str,
    output_format: str,
) -> bytes:
    fields = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "quality": quality,
        "output_format": output_format,
        "background": "opaque",
    }

    if images:
        boundary = "employee-card-art-boundary"
        body = encode_multipart(fields, [("image[]", path) for path in images], boundary)
        content_type = f"multipart/form-data; boundary={boundary}"
        url = f"{API_URL}/edits"
    else:
        body = json.dumps(fields).encode("utf-8")
        content_type = "application/json"
        url = f"{API_URL}/generations"

    req = request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": content_type,
        },
        method="POST",
    )
    response = perform_request(req)

    data = response.get("data")
    if not isinstance(data, list) or not data or not isinstance(data[0], dict):
        raise SystemExit("OpenAI response did not include data[0].")
    b64_json = data[0].get("b64_json")
    if not isinstance(b64_json, str):
        raise SystemExit("OpenAI response did not include data[0].b64_json.")
    return base64.b64decode(b64_json)


def output_paths(
    art_dir: Path, slug: str, output_format: str, variants: int
) -> list[Path]:
    ext = "jpg" if output_format == "jpeg" else output_format
    if variants == 1:
        return [art_dir / f"{slug}.{ext}"]
    return [art_dir / f"{slug}-v{index}.{ext}" for index in range(1, variants + 1)]


def update_manifest(
    manifest_path: Path,
    slug: str,
    entry: dict[str, object],
) -> None:
    manifest: dict[str, object] = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    runs = manifest.setdefault(slug, [])
    assert isinstance(runs, list)
    runs.append(entry)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate employee-card character art with the OpenAI Images API."
    )
    parser.add_argument(
        "--roster",
        default=None,
        help="Path to the roster TOML file (default: cards/roster.toml).",
    )
    parser.add_argument(
        "--only",
        action="append",
        default=[],
        metavar="SLUG",
        help="Generate art only for this employee slug. Repeat for several.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate art even when the output file already exists.",
    )
    parser.add_argument(
        "--variants",
        type=int,
        default=1,
        help="Number of variants to generate per employee (default: 1).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the planned requests without calling the OpenAI API.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = cards_root()
    roster_path = Path(args.roster) if args.roster else root / "roster.toml"
    roster = load_roster(roster_path)

    defaults = roster.get("defaults", {})
    assert isinstance(defaults, dict)
    model = str(defaults.get("model", DEFAULT_MODEL))
    size = str(defaults.get("size", DEFAULT_SIZE))
    quality = str(defaults.get("quality", DEFAULT_QUALITY))
    output_format = str(defaults.get("output_format", DEFAULT_FORMAT))
    style = str(defaults.get("style", DEFAULT_STYLE))
    style_dir = root / str(defaults.get("style_reference_dir", "style-references"))
    art_dir = root / str(defaults.get("output_dir", "art"))

    style_references = discover_images(style_dir)

    employees = roster.get("employees", [])
    assert isinstance(employees, list)
    if not employees:
        raise SystemExit(f"No [[employees]] entries found in {roster_path}.")

    if args.only:
        known = {str(employee["slug"]) for employee in employees}
        missing = [slug for slug in args.only if slug not in known]
        if missing:
            raise SystemExit(f"Unknown slug(s) in --only: {', '.join(missing)}")
        employees = [
            employee for employee in employees if str(employee["slug"]) in args.only
        ]

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key and not args.dry_run:
        raise SystemExit("Set OPENAI_API_KEY before running this script.")

    generated = 0
    skipped = 0
    for employee in employees:
        slug = str(employee["slug"])
        references = employee_references(root, employee)
        for path in references + style_references:
            if not path.exists():
                raise SystemExit(f"Reference image not found: {path}")

        if not references:
            print(
                f"warning: no reference photos found for {slug} in "
                f"{root / 'employees' / slug}; likeness will be invented",
                file=sys.stderr,
            )

        prompt = build_prompt(employee, style, len(references), len(style_references))
        images = references + style_references
        outputs = output_paths(art_dir, slug, output_format, args.variants)

        for output in outputs:
            if output.exists() and not args.force:
                print(f"skip {output.name} (exists; use --force to regenerate)")
                skipped += 1
                continue

            if args.dry_run:
                endpoint = "edits" if images else "generations"
                print(f"--- {slug} -> {output}")
                print(f"endpoint: {API_URL}/{endpoint}")
                print(f"model: {model}  size: {size}  quality: {quality}")
                print("subject references:")
                for path in references:
                    print(f"  - {path}")
                print("style references:")
                for path in style_references:
                    print(f"  - {path}")
                print("prompt:")
                print(textwrap.indent(prompt, "  "))
                continue

            print(f"generating {output.name} ...")
            image_bytes = call_images_api(
                api_key or "",
                prompt,
                images,
                model,
                size,
                quality,
                output_format,
            )
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(image_bytes)
            generated += 1
            print(f"wrote {output}")

            update_manifest(
                art_dir / "manifest.json",
                slug,
                {
                    "generated_at": datetime.now(timezone.utc).isoformat(
                        timespec="seconds"
                    ),
                    "output": str(
                        output.relative_to(root) if output.is_relative_to(root) else output
                    ),
                    "model": model,
                    "size": size,
                    "quality": quality,
                    "subject_references": [
                        str(path.relative_to(root)) if path.is_relative_to(root) else str(path)
                        for path in references
                    ],
                    "style_references": [
                        str(path.relative_to(root)) if path.is_relative_to(root) else str(path)
                        for path in style_references
                    ],
                    "prompt": prompt,
                },
            )

    if not args.dry_run:
        print(f"done: {generated} generated, {skipped} skipped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
