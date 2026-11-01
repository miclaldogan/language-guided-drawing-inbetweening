# Cue — Chromatic Atelier (V7)

A color-forward visual direction that fuses the precision of a contemporary animation tool with the framing, ornament, and material warmth of traditional printmaking.

## Preview

Open `index.html` in a current browser. The prototype has no package install or build step. For clipboard access to the GLSL study, serve this folder locally:

```bash
python -m http.server 8000 --directory docs/design/v7-chromatic-atelier
```

Then visit `http://localhost:8000`.

## Color proportion

- **60% mineral ground:** parchment and light stone keep drawings and instructions readable.
- **25% plum:** navigation, stage headers, and major visual panels provide the signature atmosphere.
- **15% saffron:** primary actions, selected frames, key shader accents, and fine ornamental rules.

The proportion describes the overall visual balance rather than a rigid count of pixels. Text contrast and state meaning take priority over applying the palette everywhere.

## Included

- Six connected product screens: sign in, library, keyframe upload, motion-plan review, generation status, and result.
- Independent Wave-Line laboratory with live GLSL controls for line spacing, tonal depth, wave amplitude, speed, and pointer response.
- Traditional engraving and geometric framing layered with technical index marks and fine grid rules.
- Responsive layout and `prefers-reduced-motion` support.

Everything remains a review mockup: authentication, upload, inference, generated MP4, and downloads are illustrative only. Source drawings and results are not passed through the decorative shader.
