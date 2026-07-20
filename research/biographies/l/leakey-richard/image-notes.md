---
kind: image-notes
---

# Richard Leakey - Image Notes

## Reference Images

- **Wikimedia Commons - "Richard Leakey cropped" (Ed Schipul, Progressive Forum, Houston)**  
  https://commons.wikimedia.org/wiki/File:Richard_Leakey_cropped.jpg  
  Direct file: https://upload.wikimedia.org/wikipedia/commons/1/13/Richard_Leakey_cropped.jpg  
  Use for: facial structure, older-age features, brow, mouth, head shape, suit-and-collar appearance.  
  Notes: CC BY-SA 2.0, author Ed Schipul, dated October 28, 2010, taken at the Progressive Forum in Houston. Clear provenance; identity confirmed by Commons file page. Accessed 2026-07-20.

- **Wikimedia Commons - "Richard Leakey 2015 (cropped)" (World Travel & Tourism Council, WTTC Global Summit 2015)**  
  https://commons.wikimedia.org/wiki/File:Richard_Leakey_2015_(cropped).jpg  
  Direct file: https://upload.wikimedia.org/wikipedia/commons/a/a8/Richard_Leakey_2015_%28cropped%29.jpg  
  Use for: late-life appearance, hairline, jaw, expression, cross-check of likeness against the 2010 reference.  
  Notes: CC BY 2.0, author World Travel & Tourism Council, dated April 15, 2015. Clear provenance. Accessed 2026-07-20.

## Generation Prompt

```text
Create a square, high-contrast black-and-white ink-cut portrait of Richard Leakey.

Use the attached reference images only to understand facial structure, hair, clothing, and historical appearance. Make the final image an original editorial biography illustration, not a photorealistic copy.

Style: bold black ink shapes on a light warm-gray background, clean vector-like edges, minimal shading, strong silhouette, similar to a linocut or stencil portrait.

Composition: centered head-and-shoulders bust portrait, square crop, face clearly readable at thumbnail size, generous margin around the head, simple clothing appropriate to a modern scientist and public figure.

Avoid: text, captions, signatures, watermarks, frames, props, dramatic scenery, color, painterly brushwork, soft photorealism, busy background.

Additional style guidance: the final attached image(s) are style references from existing Bite-Size Bios portraits. Use them only for black-and-white ink-cut visual style, crop, plain light background, margin, contrast, and graphic treatment. Do not borrow their faces, clothing, era, or identity.
```

(Generated via `research/scripts/create_bio_image.py` with the two Wikimedia references above and style references `winfrey-oprah.png`, `churchill-winston.png`, `john-brown.png`.)

## Selected Output

- File: `site/static/img/biographies/leakey-richard.png`
- Rationale: Square 1024x1024 PNG, high-contrast black-and-white ink-cut portrait, centered head-and-shoulders bust on a plain light background, readable at thumbnail size, and recognizably the older Richard Leakey (balding, lined face, suit and tie) without copying either source photograph. Style matches the existing biography set. Accepted on the first generation attempt; the iteration checklist passed on all points (likeness, thumbnail readability, square/centered crop, plain light background, near-monochrome, no text/watermark/frame/extra person/distorted anatomy, consistent style).
- Caveats: An editorial illustration, not a documentary likeness. Based on later-life (2010/2015) references, so it depicts Leakey as an older man rather than the young field scientist of the 1970s Koobi Fora era.
