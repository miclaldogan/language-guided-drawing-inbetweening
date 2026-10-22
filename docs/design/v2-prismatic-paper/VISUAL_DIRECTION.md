# Cue V2 — Prismatic Paper

V1 (Midnight Motion, dark) stays untouched in `docs/design/` and is also archived as `docs/design/v1-midnight-motion-snapshot.tar.gz`. V2 replaces its colour, type and surface decisions. It keeps V1's two signatures, the six screens, the requirements mapping and the flows. No feature or screen was added or removed. The whole UI is English.

## Idea
Warm traditional drawing materials, precise modern software. A golden painted field, cream paper where work happens, deep ink-purple as the one strong action colour. The painted quality is limited to the shell and one rough-edged purple swash on S1; the work surfaces stay clean.

## What was taken from the references
- **Yellow and purple (primary):** golden shell, deep purple painted over it. Purple on gold measures 6.9:1, so the reference pairing is readable as text, not only as decoration.
- **Orange and blue:** pigment orange as the motion accent, painted blue for information and processing.
- **Historical colour wheel:** aged cream paper, fine ink lines, a serif display face with printed numerals. Not copied: no ornament, no script lettering, no faux ageing stains.

## Layout rule: gold frames, cream works
Gold is the outer shell: top area, page title zone, margins and the gaps between cards. Cream panels hold anything that needs concentration (forms, plan, keyframes, details). Drawings and video sit on `paper-white` or the dark viewer, never on texture or gold. This is how the identity stays yellow-led without reading text on saturated yellow.

## Eye comfort (the user asked that it not tire the eyes)
- Gold is the dimmer field (relative luminance 0.49) and cream the brighter reading surface (0.82), so the large area is never the glaring one.
- Long reading happens on cream with ink text at 14:1.
- No gradients, no glow, no animated noise. Texture is static and low-contrast.
- Muted text is never placed on gold (it fails there). Secondary text on gold uses ink-700 (5.3:1).
- Result video sits on a dark neutral viewer, so a bright gold shell does not flood the clip.
- Honest limit: this is by calculation and by looking at renders. It has not been tested with users or over long sessions. If A still feels strong, Direction B (below) lowers gold share without changing any token.

## Two directions
| | A Prismatic Paper (recommended) | B Atelier Paper |
|---|---|---|
| Shell | Full gold page, cream panels sit on it | Cream page, gold header band and frame |
| Measured gold share in previews | 33–43% (S2 38%) | 23–24% |
| Measured cream/paper share | 40–49% | 57–63% |
| Feel | Energetic, unmistakable | Calmer, more editorial |
| Risk | Most saturated; needs discipline on contrast | Gold becomes a header colour; identity weaker |

Honest reading of the 60/30/10 brief: A does not reach 60% of pixels, because the panels need room. Measured gold vs cream/paper: S1 40/41, S2 38/44, S3 41/49, S4 40/48, S5 43/40, S6 36/49. So gold is the single most saturated and recognisable colour on every screen and leads outright only on S5; cream (panel, raised and paper-white counted together) is slightly larger on the other five. That is a real gap from "60% yellow". The levers to close it are narrower panels, larger gold margins, or putting small cards straight on gold (done on S2), each costing workspace. **Recommendation: A**, matching the stated preference, with this gap flagged as decision V2-D1. B stays as a fallback.

## Signatures (kept from V1, restyled)
- **Frame strip:** 16 ink ticks; first and last are orange and taller because they are the user's drawings. On S5 it becomes a printed film strip (dark film, sprocket holes) in two rows of eight; on S6 it is the scrubber.
- **CueSheet:** a printed exposure-sheet notation: ruled lanes, numbered cues in ink-outlined blocks, an ink elbow arrow from cue 1 to 2, chevrons for speed. "In plain words" sentence below for non-visual and quick reading. It is not JSON and not a handwritten notebook.

## Avoid list (checked)
Not a chatbot, not dark SaaS, not childish (no stickers, no mascot), not museum-like (no ornament), not gradient cards (cards are flat cream with ink outline and a hard 3 px print shadow).

## Previews
`previews/` holds S1–S6 (A) plus S2 and S4 in B. `style-tiles/` holds tiles A and B. All are SVG with PNG renders; faces in thumbnails are procedurally drawn stand-ins for user artwork.
