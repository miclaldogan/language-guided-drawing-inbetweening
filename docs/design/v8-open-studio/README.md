# Cue — Open Studio (V8)

An art-led website direction for the drawing inbetweening project. It takes cues from Hacktoberfest's confident event composition—dark color ground, paper light, condensed headlines, energetic accent blocks, and a distinctive illustrated hero—without reusing Hacktoberfest's logo or artwork.

## Preview

Open `index.html` in a current browser. No package install or build step is needed. For clipboard access to the GLSL study, serve this folder locally:

```bash
python -m http.server 8000 --directory docs/design/v8-open-studio
```

Then visit `http://localhost:8000`.

## Color balance

- **60% forest-charcoal:** deep green background and surrounding frame.
- **25% paper:** warm light drawing surfaces and content sections.
- **15% accents:** orange for action, sky blue for motion/interpretation, with ochre and coral supporting the artwork.

## Includes

- Expressive public landing page with a custom illustrated hero, method story, and direct studio entry.
- Pointer-responsive Wave-Line treatment over the hero illustration, with the original vector art as its static fallback.
- Six connected product screens for sign-in, library, keyframes, motion-plan review, generation, and result.
- A separate interactive Wave-Line lab with pitch, tone, wave, speed, and pointer controls.
- Responsive composition and reduced-motion support.

This remains a front-end mockup. Authentication, uploads, model inference, generated media, and real downloads are illustrative only.
