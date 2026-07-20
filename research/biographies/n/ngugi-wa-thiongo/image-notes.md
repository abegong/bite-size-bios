---
kind: image-notes
---

# Ngũgĩ wa Thiong'o - Image Notes

## Reference Images

- **Library of Congress / Shawn Miller - Ngũgĩ wa Thiong'o reading at the Coolidge Auditorium, May 9, 2019 (via Wikimedia Commons)**  
  https://commons.wikimedia.org/wiki/File:Ng%C5%A9g%C4%A9_wa_Thiong%27o_2019_(48139052733).jpg  
  Use for: facial structure in later life, smile, sparse white chin beard, era context.  
  Notes: Photo by Shawn Miller, Library of Congress; released under Creative Commons Zero (CC0) public domain dedication. Caption identifies him reading from his work in Gikuyu and English. Downloaded 2026-07-20. Face partly angled downward and wearing a flat cap, so used mainly for facial features and beard.

- **Festivaletteratura 2012 portrait (via Wikimedia Commons)**  
  https://commons.wikimedia.org/wiki/File:Ngugi_wa_Thiong%27o_-_Festivaletteratura_2012.JPG  
  Use for: primary likeness — receding hairline with short white-flecked hair, facial structure, sparse goatee, embroidered African tunic (clothing in the final portrait).  
  Notes: Wikimedia Commons file from Festivaletteratura, Mantua, September 2012; clear frontal-ish view of the face. Downloaded 2026-07-20.

- **Attempted: Literaturhaus München 2012 photo** — the Special:FilePath download returned an HTML page instead of the image; discarded. Two good references were sufficient.

## Generation Prompt

```text
Create a square, high-contrast black-and-white ink-cut portrait of Ngugi wa Thiong'o.

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
```

(Script default prompt via `--person "Ngugi wa Thiong'o"`; the script appended its standard instruction that the three attached Bite-Size Bios portraits — winfrey-oprah, churchill-winston, john-brown — were style references only, not likeness sources.)

## Selected Output

- File: `site/static/img/biographies/ngugi-wa-thiongo.png`
- Rationale: First generation passed the full iteration checklist — 1024x1024 square, centered head-and-shoulders bust, plain light background, pure black-and-white ink-cut style consistent with the existing set, readable at thumbnail size, and recognizably based on the references: receding hairline with white-flecked short hair, warm smile, sparse chin beard, and an embroidered collarless tunic echoing the 2012 Festivaletteratura photo.
- Caveats: An editorial illustration, not a documentary likeness. The portrait blends his 2010s appearance from both references; the tunic is a stylized simplification of the embroidered garment in the 2012 photo.
