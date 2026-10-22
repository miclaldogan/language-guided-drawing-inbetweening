# Paper Texture System

Texture belongs to the interface only. It is never applied to uploaded drawings, generated frames, thumbnails of them, or the video.

## Three surface treatments
| Surface | Base | Texture | Used for |
|---|---|---|---|
| Golden paper | `bg-shell` `#F8AA09` | grain 12% + fibre 5% | page shell, S1 brand panel |
| Warm cream paper | `bg-surface` `#F6E8D1` | grain 9% + fibre 5% | panels, cards |
| Clean neutral canvas | `bg-canvas` `#FFFDF7` | none | behind drawings; `bg-viewer` `#1B1220` for video |
Inputs, text areas and any block of text longer than about 60 characters per line sit on flat `bg-surface-raised`, no texture.

## Technique (implemented in the previews)
An SVG filter run once, static:
1. `feTurbulence` fractal noise, baseFrequency 0.9, 2 octaves (grain).
2. `feTurbulence` with anisotropic frequency `0.012 0.30` (horizontal fibres).
3. `feColorMatrix` turns noise into a faint ink-tinted alpha layer; layer opacity is 5–12%.
Imperfect printing: 1.5 px ink borders plus a hard 3 px offset shadow at 16% (a print misregistration feel) instead of soft blur.
Painted accent: one purple swash on S1 only (rect through `feDisplacementMap`, scale 16, plus faint bristle lines clipped inside it).

## Implementation for the web
- Prefer one pre-rendered 256×256 tileable PNG or WebP (about 10–20 KB) as a `background-image` at `background-blend-mode: multiply`, or the same SVG filter in a CSS `url(data:image/svg+xml…)`. Do not run turbulence on a full-screen element at runtime; it is expensive.
- Apply the texture to the shell and panels as a single pseudo-element (`::before`, `pointer-events: none`), not per card.
- Never animate it. Respect `prefers-contrast: more` and forced-colors by removing the texture.
- Budget: one texture asset, under 25 KB; no external image of the reference.

## Rules
- Text contrast is measured on the flat colour; texture at ≤12% opacity changes it by under 3%, and the tightest text pair on a textured surface is ink-600 on cream-200 (5.2:1).
- No photographic paper, no stains, no torn edges except the single S1 swash.
- Drawings sit on flat `paper-white` inside a 1.5 px ink border; the border is UI, the drawing is unmodified.
