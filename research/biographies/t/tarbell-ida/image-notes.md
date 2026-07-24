---
kind: image-notes
---

# Ida Tarbell - Image Notes

## Reference Images

- **J. E. Purdy & Co., Ida M. Tarbell, photograph, 1904 — Library of Congress Prints and Photographs Division, via Wikimedia Commons**  
  https://commons.wikimedia.org/wiki/File:Ida_M._Tarbell.jpg  
  Use for: facial structure, upswept Gibson-era hair, high-collared dark blouse with lace yoke, direct level gaze, appearance at the time of the Standard Oil series.  
  Notes: The canonical Tarbell likeness, taken the year the Standard Oil book appeared. Public domain. Accessed 2026-07-19.

- **Pen-and-ink portrait of Ida M. Tarbell (period illustration), via Wikimedia Commons**  
  https://commons.wikimedia.org/wiki/File:Portrait_of_Ida_M._Tarbell.png  
  Use for: secondary check on facial proportions and hair mass in a graphic black-and-white treatment.  
  Notes: Period line drawing; public domain. Accessed 2026-07-19.

## Generation Prompt

```text
Create a square, high-contrast black-and-white ink-cut portrait of Ida Tarbell, the American investigative journalist, as she appeared around 1904.

Use the attached reference images only to understand facial structure, hair, clothing, and historical appearance. Make the final image an original editorial biography illustration, not a photorealistic copy.

Style: bold black ink shapes on a light warm-gray background, clean vector-like edges, minimal shading, strong silhouette, similar to a linocut or stencil portrait.

Composition: centered head-and-shoulders bust portrait, square crop, face clearly readable at thumbnail size, generous margin around the head, upswept Edwardian hair and a high-collared dark blouse with a lace yoke appropriate to a professional woman of 1904.

Avoid: text, captions, signatures, watermarks, frames, props, dramatic scenery, color, painterly brushwork, soft photorealism, busy background.
```

        ## Generation Run — 2026-07-19 14:08 UTC

        - Model: `gpt-image-2`
        - Size: `1024x1024`
        - Quality: `medium`
        - Output format: `png`
        - Output file: `site/static/img/biographies/tarbell-ida.png`

        ### Reference Files

        - `/tmp/claude-0/-home-user-bite-size-bios/44224e48-3c90-5a94-86c5-b7978ee49597/scratchpad/tarbell-ref-1.jpg`
- `/tmp/claude-0/-home-user-bite-size-bios/44224e48-3c90-5a94-86c5-b7978ee49597/scratchpad/tarbell-ref-2.png`

        ### Style Reference Files

        - `site/static/img/biographies/washington-george.png`
- `site/static/img/biographies/nash-john.png`
- `site/static/img/biographies/john-brown.png`

        ### Generation Prompt

        ```text
        Create a square, high-contrast black-and-white ink-cut portrait of Ida Tarbell, the American investigative journalist, as she appeared around 1904.

Use the attached reference images only to understand facial structure, hair, clothing, and historical appearance. Make the final image an original editorial biography illustration, not a photorealistic copy.

Style: bold black ink shapes on a light warm-gray background, clean vector-like edges, minimal shading, strong silhouette, similar to a linocut or stencil portrait.

Composition: centered head-and-shoulders bust portrait, square crop, face clearly readable at thumbnail size, generous margin around the head, upswept Edwardian hair and a high-collared dark blouse with a lace yoke appropriate to a professional woman of 1904.

Avoid: text, captions, signatures, watermarks, frames, props, dramatic scenery, color, painterly brushwork, soft photorealism, busy background.

Additional style guidance: the final attached image(s) are style references from
existing Bite-Size Bios portraits. Use them only for black-and-white ink-cut
visual style, crop, plain light background, margin, contrast, and graphic
treatment. Do not borrow their faces, clothing, era, or identity.
        ```

## Selected Output

- File: `site/static/img/biographies/tarbell-ida.png`
- Rationale: First generation passed the checklist — recognizably the 1904 Purdy-photograph Tarbell (upswept Edwardian hair, high collar with lace yoke and brooch, direct level gaze), square and centered with generous margin, plain light background, pure black-and-white ink-cut style consistent with the existing portrait set, readable at thumbnail size, no text or artifacts.
- Caveats: An editorial illustration derived from the 1904 photograph, not a documentary likeness; depicts Tarbell at the time of the Standard Oil series rather than in later life.
