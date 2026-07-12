---
kind: image-notes
---

# George Washington - Image Notes

## Reference Images

- **Gilbert Stuart, Portrait of George Washington (Athenaeum type), 1796-1803 — Sterling and Francine Clark Art Institute, via Wikimedia Commons**  
  https://commons.wikimedia.org/wiki/File:Gilbert_Stuart_Williamstown_Portrait_of_George_Washington.jpg  
  Use for: facial structure, jaw and mouth set, powdered hair, black coat and white cravat/jabot, presidential-era appearance.  
  Notes: The Athenaeum-type portrait is the canonical Washington likeness (the dollar-bill image), painted from life in 1796. Public domain. Accessed 2026-07-12.

- **Gilbert Stuart, George Washington (Lansdowne portrait), 1796 — National Portrait Gallery, Smithsonian Institution, via Wikimedia Commons**  
  https://commons.wikimedia.org/wiki/File:Gilbert_Stuart,_George_Washington_(Lansdowne_portrait,_1796).jpg  
  Use for: full-figure context, posture, black velvet suit, era-appropriate dress.  
  Notes: Full-length state portrait painted from life in 1796. Public domain. Accessed 2026-07-12.

## Generation Prompt

```text
Create a square, high-contrast black-and-white ink-cut portrait of George Washington.

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

## Generation Run - 2026-07-12 22:58 UTC

- Model: `gpt-image-2`
- Size: `1024x1024`
- Quality: `medium`
- Output format: `png`
- Output file: `site/static/img/biographies/washington-george.png`

## Selected Output

- File: `site/static/img/biographies/washington-george.png`
- Rationale: First generation passed the checklist — recognizably the Athenaeum-portrait Washington (powdered curled hair, black coat, white jabot), square and centered with generous margin, plain light background, pure black-and-white ink-cut style consistent with the existing set, readable at thumbnail size, no text or artifacts.
- Caveats: The portrait is an editorial illustration derived from Gilbert Stuart's paintings, not a documentary likeness; no photographs of Washington exist.
