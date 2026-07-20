---
kind: image-notes
---

# Jomo Kenyatta - Image Notes

## Reference Images

- **Israel National Photo Collection / Government Press Office - Jomo Kenyatta with P.M. Levi Eshkol, State House, Nairobi, 15 June 1966**  
  https://upload.wikimedia.org/wikipedia/commons/9/90/Jomo_Kenyatta_1966-06-15.jpg (file page: https://commons.wikimedia.org/wiki/File:Jomo_Kenyatta_1966-06-15.jpg)  
  Use for: frontal facial structure, deep-set eyes, brow, nose, mouth, beard, hairline, suit-and-tie appearance as president.  
  Notes: Israel Government Press Office photograph, public domain in Israel under the 2007 statute (created before 24 May 2008). Caption identifies Kenyatta by name at State House, Nairobi. Accessed 2026-07-20.

- **Dutch National Archives (Nationaal Archief) / Anefo collection - Portrait of Jomo Kenyatta, President of Kenya, 22 August 1978**  
  https://upload.wikimedia.org/wikipedia/commons/f/f3/Jomo_Kenyatta_1978.jpg (file page: https://commons.wikimedia.org/wiki/File:Jomo_Kenyatta_1978.jpg)  
  Use for: profile view, goatee beard shape, ear and jawline, elder-statesman era appearance.  
  Notes: Fotocollectie Algemeen Nederlands Persbureau (Anefo), Bestanddeelnummer 929-8665; author unknown; CC BY-SA 3.0 NL. Press portrait published at his death. Accessed 2026-07-20.

## Generation Prompt

```text
Create a square, high-contrast black-and-white ink-cut portrait of Jomo Kenyatta, first president of Kenya, as an elder statesman in the 1960s-1970s: an older African man with a receding hairline of short gray-flecked hair, a full gray goatee beard, deep-set watchful eyes, strong brow and broad nose, wearing a simple dark suit, collared shirt, and tie.

Use the attached Jomo Kenyatta reference photographs only to understand his facial structure, beard, hairline, and period appearance. Make the final image an original editorial biography illustration, not a photorealistic copy of any photograph.

Style: bold black ink shapes on a light warm-gray background, clean vector-like edges, minimal shading, strong silhouette, similar to a linocut or stencil portrait.

Composition: centered head-and-shoulders bust portrait facing forward, square crop, face clearly readable at thumbnail size, generous margin around the head, simple dark suit and tie appropriate to a 1960s head of state.

Avoid: text, captions, signatures, watermarks, frames, flags, medals, chains of office, flywhisk, hats, props, dramatic scenery, color, painterly brushwork, soft photorealism, busy background, extra people.

Additional style guidance: the final attached images are existing Bite-Size Bios portraits provided only as style references for the black-and-white ink-cut visual style, crop, plain light background, margin, contrast, and graphic treatment - not for likeness or identity.
```

Style references passed with `--style-reference`: `site/static/img/biographies/winfrey-oprah.png`, `site/static/img/biographies/churchill-winston.png`, `site/static/img/biographies/john-brown.png`.

## Selected Output

- File: `site/static/img/biographies/kenyatta-jomo.png`
- Rationale: First generation accepted. The portrait is square (1024 x 1024), centered, high-contrast black ink on a light warm-gray background, readable at thumbnail size, and recognizably based on Kenyatta's elder-statesman appearance from the two archival references (deep-set eyes, heavy brow, broad nose, gray-flecked goatee, suit and tie) without copying either photograph. Style matches the existing site set.
- Caveats: The generated portrait is an editorial illustration, not a documentary likeness; the illustrated hairline is slightly fuller than in the 1966 photograph. No reliable photographs exist of Kenyatta before the 1920s, so the portrait deliberately depicts his presidential-era appearance, which is how he is publicly remembered.
