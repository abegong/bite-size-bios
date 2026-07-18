# Vincent van Gogh — Image Notes

No reliable photographs of the adult Van Gogh exist (a disputed 1873 photo shows him at 19), so his self-portraits — of which he painted more than 35 — are the standard visual reference. Both references below are museum-held works with clear provenance, fetched from Wikimedia Commons.

## Reference Images

- **Self-Portrait (September 1889), Musée d'Orsay, Paris**  
  https://commons.wikimedia.org/wiki/File:Vincent_van_Gogh_-_Self-Portrait_-_Google_Art_Project.jpg  
  Use for: face structure, red-blond hair and beard, intense gaze, late-period appearance (age 36).  
  Notes: Google Art Project scan of the Orsay canvas; public domain. Accessed 2026-07-18.

- **Self-Portrait with Grey Felt Hat (winter 1887–88), Van Gogh Museum, Amsterdam**  
  https://commons.wikimedia.org/wiki/File:Vincent_van_Gogh_-_Self-portrait_with_grey_felt_hat_-_Google_Art_Project.jpg  
  Use for: fuller beard, alternate angle, Paris-period appearance.  
  Notes: Google Art Project scan of the Van Gogh Museum canvas; public domain. Accessed 2026-07-18.

## Selected Output

- File: `site/static/img/biographies/van-gogh-vincent.png`
- Rationale: first generation accepted. Recognizable likeness (angular face, swept-back hair, red-blond beard, intense gaze, echoing the 1889 Orsay self-portrait), clean ink-cut style consistent with the existing portrait set, readable at thumbnail size, plain light background, square 1024x1024 crop with good margin, no text or artifacts.
- Caveats: likeness derives from self-portraits rather than photographs, so it reflects how Van Gogh painted himself.

        ## Generation Run — 2026-07-18 17:20 UTC

        - Model: `gpt-image-2`
        - Size: `1024x1024`
        - Quality: `medium`
        - Output format: `png`
        - Output file: `site/static/img/biographies/van-gogh-vincent.png`

        ### Reference Files

        - `/tmp/claude-0/-home-user-bite-size-bios/ed1371ff-5c3f-5ff3-8449-3b2e71bcca95/scratchpad/vangogh-ref-orsay-1889.jpg`
- `/tmp/claude-0/-home-user-bite-size-bios/ed1371ff-5c3f-5ff3-8449-3b2e71bcca95/scratchpad/vangogh-ref-greyhat-1887.jpg`

        ### Style Reference Files

        - `site/static/img/biographies/nash-john.png`
- `site/static/img/biographies/washington-george.png`
- `site/static/img/biographies/winfrey-oprah.png`

        ### Generation Prompt

        ```text
        Create a square, high-contrast black-and-white ink-cut portrait of Vincent van Gogh, Dutch painter, 1880s, mid-thirties, gaunt angular face, prominent cheekbones, intense deep-set eyes, short cropped red-blond hair, full trimmed beard and moustache, wearing a simple 19th-century jacket over a buttoned shirt.

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
