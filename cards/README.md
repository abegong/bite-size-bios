# Employee Card Art Pipeline

This directory is a self-contained pipeline for generating consistent
character art for employee cards. It pairs each employee's reference photos
with a shared set of style-reference images and calls the OpenAI Images API
(`images/edits`) to produce card art that preserves the employee's likeness
while matching the style of the reference set.

It follows the same approach as the biography portrait tool at
`research/scripts/create_bio_image.py`, generalized to batch generation over
a roster.

## Layout

```text
cards/
├── README.md               # this file
├── generate_card_art.py    # the pipeline script
├── roster.toml             # who to generate, plus shared defaults
├── employees/<slug>/       # 1-3 reference photos per employee (likeness)
├── style-references/       # 2-4 exemplar images that define the art style
└── art/                    # generated output + manifest.json (created on first run)
```

## How style transfer works

Each API request attaches two groups of images, in order:

1. **Subject references** — the employee's photos from `employees/<slug>/`.
   The prompt instructs the model to use these only for likeness.
2. **Style references** — every image in `style-references/`. The prompt
   instructs the model to copy their artistic style, palette, and background
   treatment exactly, and never their faces or identity.

The written `style` description in `roster.toml` reinforces the style
references. Keep both pointing at the same look: once you have a few cards
you like, move them into `style-references/` so later batches converge on a
consistent set.

## Setup

1. Python 3.11+ (uses only the standard library).
2. `export OPENAI_API_KEY=...`
3. Add style exemplars to `style-references/`.
4. For each employee: add a `[[employees]]` entry to `roster.toml` and put
   1-3 reference photos in `employees/<slug>/`.

## Usage

Always inspect the planned requests first — this prints every prompt and
attachment without calling the API:

```sh
python3 cards/generate_card_art.py --dry-run
```

Generate art for everyone who does not have an output file yet:

```sh
python3 cards/generate_card_art.py
```

Common variations:

```sh
# One employee only
python3 cards/generate_card_art.py --only doe-jane

# Regenerate even though output exists
python3 cards/generate_card_art.py --only doe-jane --force

# Three variants to choose between (writes <slug>-v1.png, -v2, -v3)
python3 cards/generate_card_art.py --only doe-jane --variants 3
```

Existing outputs are skipped by default, so re-running the script after
adding new employees generates only the new cards.

## Roster reference

`[defaults]` keys (all optional):

| Key | Default | Purpose |
| --- | --- | --- |
| `model` | `gpt-image-2` | OpenAI image model |
| `size` | `1024x1024` | Output dimensions |
| `quality` | `high` | `low` / `medium` / `high` |
| `output_format` | `png` | `png` / `jpeg` / `webp` |
| `style` | built-in | Written description of the target style |
| `style_reference_dir` | `style-references` | Where style exemplars live |
| `output_dir` | `art` | Where generated art is written |

`[[employees]]` keys:

| Key | Required | Purpose |
| --- | --- | --- |
| `slug` | yes | Names `employees/<slug>/` and the output file |
| `name` | yes | Used in the prompt |
| `role` | no | Adds context to the prompt |
| `notes` | no | Likeness details to emphasize (glasses, beard, ...) |
| `references` | no | Explicit photo paths; overrides auto-discovery |
| `prompt` | no | Replaces the built-in prompt template entirely |

## Iteration checklist

Inspect each card before accepting it:

- The employee is recognizable from their reference photos.
- The style matches `style-references/` closely enough to feel like a set.
- The portrait reads clearly at thumbnail size.
- Square crop, centered, generous margin around the head.
- No text, name tags, logos, watermarks, extra people, or distorted anatomy.

If a card fails, adjust `notes` (for likeness problems) or the `style`
description and style references (for style drift), then regenerate with
`--force` or generate `--variants 3` and pick the best. Every run is
recorded in `art/manifest.json` — prompt, references, model settings, and
timestamp — so good results are reproducible.

## Privacy note

Employee reference photos are personal data. Get consent before adding
them, and if this repository is shared or public, keep the photos out of
version control (add `cards/employees/*/` image files to `.gitignore`) and
distribute them through a private channel instead.
