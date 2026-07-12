---
kind: image-notes
---

# John Nash - Image Notes

## Reference Images

- **Peter Badge, "John Forbes Nash, Jr." — Nobel laureate portrait series, via Wikimedia Commons**  
  https://commons.wikimedia.org/wiki/File:John_Forbes_Nash,_Jr._by_Peter_Badge.jpg  
  Use for: facial structure, eyes, ears, thin white hair, tweed jacket over checked shirt, late-life appearance.  
  Notes: Portrait by Peter Badge from the Typos1/Nobel laureate photography project; clearly identified as Nash. CC BY-SA license. Accessed 2026-07-12.

- **John F. Nash at a 2006 event, via Wikimedia Commons**  
  https://commons.wikimedia.org/wiki/File:John_f_nash_20061102_3.jpg  
  Use for: face at a slight angle, jaw and brow structure, expression, elderly appearance in his late 70s.  
  Notes: Photo of Nash at a public appearance in November 2006; freely licensed on Wikimedia Commons. Accessed 2026-07-12.

## Generation Prompt

```text
Create a square, high-contrast black-and-white ink-cut portrait of John Forbes Nash Jr.

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

Additional style guidance: the final attached image(s) are style references from
existing Bite-Size Bios portraits. Use them only for black-and-white ink-cut
visual style, crop, plain light background, margin, contrast, and graphic
treatment. Do not borrow their faces, clothing, era, or identity.
```

Style references passed alongside the subject references: `site/static/img/biographies/john-brown.png`, `site/static/img/biographies/elizabeth-bathory.png`, `site/static/img/biographies/gandhi.jpg`.

## Generation Run - 2026-07-12 23:00 UTC

- Model: `gpt-image-2`
- Size: `1024x1024`
- Quality: `medium`
- Output format: `png`
- Output file: `site/static/img/biographies/nash-john.png`

## Selected Output

- File: `site/static/img/biographies/nash-john.png`
- Rationale: First generation passed the checklist — recognizably the late-life Nash of the reference photos (thin swept hair, prominent ears, deep-set eyes, tweed jacket over a checked shirt), square and centered with generous margin, plain light background, black-and-white ink-cut style consistent with the existing set, readable at thumbnail size, no text or artifacts.
- Caveats: The portrait depicts Nash in old age, matching the strongest available references, rather than during his 1950s Princeton years; it is an editorial illustration, not a documentary likeness.
