---
kind: image-notes
---

# George Washington - Image Notes

## Reference Images

- **Gilbert Stuart, *George Washington* (Williamstown/Athenaeum-type portrait, 1796–1803), Sterling and Francine Clark Art Institute — via Wikimedia Commons**  
  https://commons.wikimedia.org/wiki/File:Gilbert_Stuart_Williamstown_Portrait_of_George_Washington.jpg  
  Use for: face, wig, cravat, coat, pose — the source painting for the entire portrait.  
  Notes: Public domain (painter died 1828). This is the Athenaeum-type likeness — the same Stuart likeness used on the one-dollar bill, so it is the most recognizable image of Washington that exists. Fetched via Special:FilePath at 1920x2331. Accessed 2026-07-12.

## Generation Method

`OPENAI_API_KEY` was not available in the environment, so
`research/scripts/create_bio_image.py` could not be used. The portrait was
instead derived directly from the public-domain Stuart painting with a
deterministic image-processing pipeline (Pillow + NumPy):

1. Square head-and-shoulders crop (1560 px side, centered on the head, inset
   from the canvas edges), resized to 1400 px working resolution.
2. Backdrop removal by color: the olive-brown backdrop is dark *and* warm
   (red − blue > 14), while the coat is dark and neutral, which cleanly
   separates the two.
3. Ink mask = coat pixels plus mid-tone facial/wig shadows
   (luminance < 114, excluding backdrop).
4. Median filter + Gaussian blur + re-threshold to merge the mask into bold,
   blobby linocut-style shapes.
5. Composite: ink `#1A1B1B` on paper `#F0EEEC` (sampled from the existing
   Bite-Size Bios portraits), downsampled to 1024x1024 PNG.

A luminance threshold of 114 was chosen from a 100/108/114 comparison sheet:
lower values hollowed out the eyes and nose; higher values turned the shadowed
right side of the face into a solid black band.

## Selected Output

- File: `site/static/img/biographies/washington-george.png`
- Rationale: Based on the single most recognizable likeness of Washington;
  reads clearly at thumbnail size; black-and-white palette, plain light
  background, and centered bust composition match the existing portrait set.
- Caveats: Because the image is a direct stylization of one painting rather
  than a synthesis of several references, it inherits the pose and lighting of
  the Stuart portrait exactly. If an OpenAI key becomes available, the standard
  `create_bio_image.py` workflow can regenerate a more interpretive ink-cut
  portrait using this same painting as a reference.
