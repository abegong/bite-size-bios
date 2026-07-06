# Create Bio Image

Use this skill to create the square portrait image for a bite-size biography. Start from web reference images of the subject, generate a consistent stylized portrait with `research/scripts/create_bio_image.py`, and place the final asset at `site/static/img/biographies/<slug>.<ext>`.

---

## Output Goal

- Produce a square portrait that works as both the biography header and list thumbnail.
- Match the existing site style: high-contrast black ink-cut portrait, light neutral background, centered bust or head-and-shoulders composition.
- Make the person recognizable when reliable visual references exist.
- Avoid photorealism, painterly color, busy backgrounds, text, signatures, logos, frames, or dramatic props.

---

## Source Image Workflow

1. Read `research-links.md` first for names, dates, era, visual leads, and uncertainty warnings.
2. Find 1-3 credible visual references for the person.
3. Prefer museum, archive, library, encyclopedia, historical society, or Wikimedia-hosted images with clear provenance.
4. For living or modern public figures, use current, high-quality references from reputable sources.
5. For historical figures without reliable portraits, use period-appropriate visual references and state the uncertainty.
6. Save source URLs and provenance notes in `research/biographies/<initial>/<slug>/image-notes.md`.

Do not use a reference image as proof of identity unless the source identifies it clearly.

---

## Prompt Contract

Use the reference images with `research/scripts/create_bio_image.py`. The script calls the OpenAI Images API, using the edits endpoint when reference images are provided and the generations endpoint when they are not. It saves `1024x1024` square PNG assets by default.

The script reads `OPENAI_API_KEY` from the environment. Run `--dry-run` first to inspect the request without calling the API.

Pass existing Bite-Size Bios portraits with `--style-reference`; the script appends an instruction telling the API to use those final attached images only for visual style, not for likeness or identity.

Example:

```sh
python3 research/scripts/create_bio_image.py \
  --slug brown-john \
  --person "John Brown" \
  --reference /path/to/reference-1.png \
  --reference /path/to/reference-2.jpg \
  --style-reference site/static/img/biographies/john-brown.png \
  --style-reference site/static/img/biographies/elizabeth-bathory.png \
  --style-reference site/static/img/biographies/gandhi.jpg \
  --notes \
  --notes-path temp/brown-john/image-notes.md \
  --update-frontmatter
```

Use `--notes-path` when intermediate notes should stay in `temp/` instead of the permanent research folder.

Include a prompt with these components:

- Subject identity: name, era, age range if known, notable facial features, hair, clothing, and posture.
- Style: high-contrast black-and-white ink-cut portrait, bold silhouette, clean vector-like edges, editorial biography illustration.
- Composition: centered bust portrait, head and shoulders visible, square crop, generous margin around the head, light warm-gray or off-white background.
- Constraints: no text, no watermark, no frame, no decorative background, no photorealistic rendering, no color palette beyond black, white, and subtle gray.
- Fidelity: preserve the subject's recognizable facial structure from the reference images without copying any single source photo exactly.

Template:

```text
Create a square, high-contrast black-and-white ink-cut portrait of <person>.

Use the attached reference images only to understand facial structure, hair, clothing, and historical appearance. Make the final image an original editorial biography illustration, not a photorealistic copy.

Style: bold black ink shapes on a light warm-gray background, clean vector-like edges, minimal shading, strong silhouette, similar to a linocut or stencil portrait.

Composition: centered head-and-shoulders bust portrait, square crop, face clearly readable at thumbnail size, generous margin around the head, simple clothing appropriate to <era/context>.

Avoid: text, captions, signatures, watermarks, frames, props, dramatic scenery, color, painterly brushwork, soft photorealism, busy background.
```

---

## Iteration Checklist

After generation, inspect the image before adding it to the site:

- The subject reads correctly from the reference images.
- The portrait remains readable as a small thumbnail.
- The crop is square and centered, with no important facial features near the edge.
- The background is plain and light.
- The image is black-and-white or nearly black-and-white.
- There is no text, watermark, frame, extra person, distorted anatomy, or inappropriate symbol.
- The style matches the existing biography images closely enough to feel like a set.

If any item fails, revise the prompt and regenerate instead of fixing a poor image downstream.

---

## File Placement

The script writes this path by default:

```text
site/static/img/biographies/<slug>.<ext>
```

Then set the biography front matter:

```toml
image = "/img/biographies/<slug>.<ext>"
```

Prefer PNG for generated ink-cut portraits. Use JPG only when the final asset is photographic or already compressed as JPG.

---

## Image Notes Format

Write `research/biographies/<initial>/<slug>/image-notes.md`:

~~~markdown
# <Person Name> — Image Notes

## Reference Images

- **<Source title or institution>**  
  <URL>  
  Use for: <face / hair / clothing / pose / era context>  
  Notes: <provenance, uncertainty, license, access date if useful>

## Generation Prompt

```text
<final prompt used>
```

## Selected Output

- File: `site/static/img/biographies/<slug>.<ext>`
- Rationale: ...
- Caveats: ...
~~~

---

## Quality Bar

- Use at least one credible reference image when available.
- Record reference URLs and the final prompt.
- Keep the final asset square and at least 980 x 980 pixels.
- Make the image compatible with both the card thumbnail and biography header.
- If reliable visual references do not exist, say so in `image-notes.md` and create a historically plausible portrait rather than a false likeness.
