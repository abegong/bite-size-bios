#!/usr/bin/env python3
"""Generate a Bite-Size Bios portrait image with the OpenAI Images API."""

from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import json
import mimetypes
import os
from pathlib import Path
import textwrap
from urllib import error, request


API_URL = "https://api.openai.com/v1/images"
DEFAULT_MODEL = "gpt-image-2"
DEFAULT_SIZE = "1024x1024"
DEFAULT_QUALITY = "medium"
DEFAULT_FORMAT = "png"
STYLE_REFERENCE_INSTRUCTION = """

Additional style guidance: the final attached image(s) are style references from
existing Bite-Size Bios portraits. Use them only for black-and-white ink-cut
visual style, crop, plain light background, margin, contrast, and graphic
treatment. Do not borrow their faces, clothing, era, or identity.
"""


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def biography_dir(root: Path, slug: str) -> Path:
    return root / "research" / "biographies" / slug[0].lower() / slug


def default_prompt(person: str) -> str:
    return textwrap.dedent(
        f"""\
        Create a square, high-contrast black-and-white ink-cut portrait of {person}.

        Use the attached reference images only to understand facial structure, hair,
        clothing, and historical appearance. Make the final image an original
        editorial biography illustration, not a photorealistic copy.

        Style: bold black ink shapes on a light warm-gray background, clean
        vector-like edges, minimal shading, strong silhouette, similar to a linocut
        or stencil portrait.

        Composition: centered head-and-shoulders bust portrait, square crop, face
        clearly readable at thumbnail size, generous margin around the head, simple
        clothing appropriate to the subject's era and context.

        Avoid: text, captions, signatures, watermarks, frames, props, dramatic
        scenery, color, painterly brushwork, soft photorealism, busy background.
        """
    ).strip()


def read_prompt(args: argparse.Namespace) -> str:
    if args.prompt_file:
        return Path(args.prompt_file).read_text(encoding="utf-8").strip()
    if args.prompt:
        return args.prompt.strip()
    if args.person:
        return default_prompt(args.person)
    raise SystemExit("Provide --prompt-file, --prompt, or --person.")


def prompt_with_style_guidance(prompt: str, style_references: list[Path]) -> str:
    if not style_references:
        return prompt
    return prompt.rstrip() + textwrap.dedent(STYLE_REFERENCE_INSTRUCTION).rstrip()


def output_path(root: Path, slug: str, output_format: str, explicit: str | None) -> Path:
    if explicit:
        return Path(explicit)
    ext = "jpg" if output_format == "jpeg" else output_format
    return root / "site" / "static" / "img" / "biographies" / f"{slug}.{ext}"


def api_headers(api_key: str, content_type: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": content_type,
    }


def request_json(url: str, api_key: str, payload: dict[str, object]) -> dict[str, object]:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=body,
        headers=api_headers(api_key, "application/json"),
        method="POST",
    )
    return perform_request(req)


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
        filename = path.name
        content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("utf-8"),
                (
                    f'Content-Disposition: form-data; name="{name}"; '
                    f'filename="{filename}"\r\n'
                ).encode("utf-8"),
                f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"),
                path.read_bytes(),
                b"\r\n",
            ]
        )

    chunks.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(chunks)


def request_multipart(
    url: str,
    api_key: str,
    fields: dict[str, str],
    files: list[tuple[str, Path]],
) -> dict[str, object]:
    boundary = "bite-size-bios-image-boundary"
    body = encode_multipart(fields, files, boundary)
    req = request.Request(
        url,
        data=body,
        headers=api_headers(api_key, f"multipart/form-data; boundary={boundary}"),
        method="POST",
    )
    return perform_request(req)


def perform_request(req: request.Request) -> dict[str, object]:
    try:
        with request.urlopen(req, timeout=300) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"OpenAI API request failed: {exc.code} {exc.reason}\n{details}")
    except error.URLError as exc:
        raise SystemExit(f"OpenAI API request failed: {exc.reason}")


def extract_image_bytes(response: dict[str, object]) -> bytes:
    data = response.get("data")
    if not isinstance(data, list) or not data:
        raise SystemExit("OpenAI response did not include data[0].")
    first = data[0]
    if not isinstance(first, dict):
        raise SystemExit("OpenAI response data[0] was not an object.")
    b64_json = first.get("b64_json")
    if not isinstance(b64_json, str):
        raise SystemExit("OpenAI response did not include data[0].b64_json.")
    return base64.b64decode(b64_json)


def update_frontmatter(markdown_path: Path, image_value: str) -> None:
    if not markdown_path.exists():
        raise SystemExit(f"Cannot update missing front matter file: {markdown_path}")

    text = markdown_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    replaced = False
    for index, line in enumerate(lines):
        if line.startswith("image = "):
            lines[index] = f'image = "{image_value}"'
            replaced = True
            break

    if not replaced:
        insert_at = 1 if lines and lines[0] == "+++" else 0
        lines.insert(insert_at, f'image = "{image_value}"')

    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_notes(
    root: Path,
    notes_path: Path,
    person: str | None,
    slug: str,
    prompt: str,
    references: list[Path],
    style_references: list[Path],
    output: Path,
    model: str,
    size: str,
    quality: str,
    output_format: str,
) -> None:
    notes_path.parent.mkdir(parents=True, exist_ok=True)
    if not notes_path.exists():
        title = person or slug.replace("-", " ").title()
        notes_path.write_text(
            textwrap.dedent(
                f"""\
                # {title} — Image Notes

                ## Reference Images

                - TODO: Add source URLs, provenance, license, and what each reference is useful for.

                """
            ),
            encoding="utf-8",
        )

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    ref_lines = "\n".join(f"- `{path}`" for path in references) or "- None"
    style_ref_lines = "\n".join(f"- `{path}`" for path in style_references) or "- None"
    try:
        relative_output = output.relative_to(root)
    except ValueError:
        relative_output = output

    entry = textwrap.dedent(
        f"""\

        ## Generation Run — {now}

        - Model: `{model}`
        - Size: `{size}`
        - Quality: `{quality}`
        - Output format: `{output_format}`
        - Output file: `{relative_output}`

        ### Reference Files

        {ref_lines}

        ### Style Reference Files

        {style_ref_lines}

        ### Generation Prompt

        ```text
        {prompt}
        ```
        """
    )
    with notes_path.open("a", encoding="utf-8") as handle:
        handle.write(entry)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a Bite-Size Bios portrait with the OpenAI Images API."
    )
    parser.add_argument("--slug", required=True, help="Biography slug, e.g. brown-john.")
    parser.add_argument("--person", help="Person name for the default prompt.")
    parser.add_argument("--prompt", help="Prompt text. Use --prompt-file for long prompts.")
    parser.add_argument("--prompt-file", help="Path to a prompt text file.")
    parser.add_argument(
        "--reference",
        action="append",
        default=[],
        help="Local subject/reference image path. Repeat for multiple references.",
    )
    parser.add_argument(
        "--style-reference",
        action="append",
        default=[],
        help="Existing site portrait used only as a visual style reference.",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--size", default=DEFAULT_SIZE)
    parser.add_argument("--quality", default=DEFAULT_QUALITY)
    parser.add_argument(
        "--output-format",
        default=DEFAULT_FORMAT,
        choices=["png", "jpeg", "webp"],
    )
    parser.add_argument("--output", help="Override output image path.")
    parser.add_argument(
        "--update-frontmatter",
        action="store_true",
        help="Set image front matter in site/content/biographies/<slug>/index.md.",
    )
    parser.add_argument(
        "--notes",
        action="store_true",
        help="Append generation details to research/biographies/<initial>/<slug>/image-notes.md.",
    )
    parser.add_argument(
        "--notes-path",
        help="Override where --notes writes generation details.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the planned request without calling the OpenAI API.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = repo_root()
    base_prompt = read_prompt(args)
    references = [Path(path) for path in args.reference]
    style_references = [Path(path) for path in args.style_reference]
    prompt = prompt_with_style_guidance(base_prompt, style_references)
    all_references = references + style_references
    for path in all_references:
        if not path.exists():
            raise SystemExit(f"Reference image not found: {path}")

    output = output_path(root, args.slug, args.output_format, args.output)
    endpoint = "edits" if all_references else "generations"
    image_value = f"/img/biographies/{output.name}"

    if args.dry_run:
        print(f"endpoint: {API_URL}/{endpoint}")
        print(f"model: {args.model}")
        print(f"size: {args.size}")
        print(f"quality: {args.quality}")
        print(f"output_format: {args.output_format}")
        print(f"output: {output}")
        print("references:")
        for path in references:
            print(f"  - {path}")
        print("style_references:")
        for path in style_references:
            print(f"  - {path}")
        print("\nprompt:\n" + prompt)
        return 0

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("Set OPENAI_API_KEY before running this script.")

    if all_references:
        fields = {
            "model": args.model,
            "prompt": prompt,
            "size": args.size,
            "quality": args.quality,
            "output_format": args.output_format,
            "background": "opaque",
        }
        files = [("image[]", path) for path in all_references]
        response = request_multipart(f"{API_URL}/edits", api_key, fields, files)
    else:
        payload = {
            "model": args.model,
            "prompt": prompt,
            "size": args.size,
            "quality": args.quality,
            "output_format": args.output_format,
            "background": "opaque",
        }
        response = request_json(f"{API_URL}/generations", api_key, payload)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(extract_image_bytes(response))
    print(f"Wrote {output}")

    if args.update_frontmatter:
        content_path = root / "site" / "content" / "biographies" / args.slug / "index.md"
        update_frontmatter(content_path, image_value)
        print(f"Updated {content_path} with {image_value}")

    if args.notes:
        notes_path = (
            Path(args.notes_path)
            if args.notes_path
            else biography_dir(root, args.slug) / "image-notes.md"
        )
        append_notes(
            root,
            notes_path,
            args.person,
            args.slug,
            prompt,
            references,
            style_references,
            output,
            args.model,
            args.size,
            args.quality,
            args.output_format,
        )
        print(f"Updated {notes_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
