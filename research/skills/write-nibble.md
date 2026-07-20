# Write Nibble

Use this skill to derive a nibble — the shortest Bite-Size Bios format — from an already-published bite-size biography. A nibble is three to four paragraphs (roughly 250–400 words) that capture the arc of a life in a single glance.

Nibbles are derivative works. Write them from two inputs, in this order of authority:

1. The published bite at `site/content/biographies/<slug>/index.md`.
2. The research dossier at `research/biographies/<initial>/<slug>/research-links.md`.

Do not introduce facts, dates, or claims that appear in neither input.

---

## Where It Lives

Publish the nibble at `site/content/nibbles/<slug>/index.md`, using the **same slug** as the bite. The site cross-links the two versions automatically by slug, in both directions — no front matter linking is needed, but the slugs must match exactly.

Front matter fields (validated by `.katalyst/schemas/published_nibble.yaml`):

```toml
+++
title = "Thomas Edison"
lifespan = "1847-1931"
date = "2026-07-20"
draft = false
summary = "Before him, invention was a lone tinkerer's game; after his laboratories, it was an industry."
image = "/img/biographies/thomas-edison.png"
+++
```

- `title`, `lifespan`, and `image` should match the bite exactly.
- `summary` is 40–180 characters, shown in full on the opening page. Follow the Card Summary rules in `research/skills/write-bio.md`: no stock openers ("A nibble-size portrait of...", "The story of..."), don't re-introduce the name, and take a different angle from the bite's summary — not a rewording of it.
- No `tags`, `categories`, or `archives` — the bite is the canonical taxonomy entry for the person.

---

## Structure

No headings, no sources section. The nibble body is just paragraphs; the layout supplies the link to the bite, which carries the full sources list.

### Paragraph 1 — The hook
Reuse (compressed) the bite's opening scene or defining moment, and state why this person matters. If the bite corrects a myth, keep the correction.

### Paragraph 2 — Formation
Birth, formative world, and the one or two experiences that explain everything that follows.

### Paragraph 3 — The work
The central project or struggle, its defining turn, and its immediate consequence. One or two concrete dates at most.

### Paragraph 4 — The reckoning
Death, legacy, and the honest one-sentence verdict. End on the idea the reader should carry away, not on a list of accomplishments.

Three paragraphs are fine when formation and work compress naturally into one.

---

## Notes

- Compression is the craft: prefer cutting whole episodes over summarizing all of them thinly.
- Keep the bite's caution flags — anything the bite hedges ("sources disagree..."), the nibble must not state as certain. It is always acceptable to omit a disputed detail entirely.
- Keep one vivid, concrete image; a nibble with no scene reads like an encyclopedia entry.
- Match the bite's framing and tone. A reader who finishes the nibble and clicks through should feel they are getting more of the same story, not a different one.
