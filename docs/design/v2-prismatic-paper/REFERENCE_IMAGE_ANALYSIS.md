# Reference Image Analysis

All three files were found and opened: `~/Downloads/yellow-purple.jpg` (413×743), `~/Downloads/bakcgorun theme.png` (762×1024), `~/Downloads/orange-blue.jpg` (1000×667). Colours below come from median-cut quantisation of the real pixels (8 clusters each), not from the suggested values. Relative luminance (L) is WCAG.

## C — Yellow and purple (primary)
A hand painting a deep purple stroke over a flat golden panel; a caption bar overlays the image.
| Share | Hex | Note |
|---|---|---|
| 39% | `#F8AA09` | the yellow field, hue 40°, saturation 0.96, L 0.49 |
| 16% | `#4F0964` | the purple, hue 286°, L 0.03 |
| 11% | `#FBC750` | lighter yellow where light catches the panel |
| 11% | `#E68F1F` | darker amber, shaded areas |
| 10% | `#762042` | purple-red where wet paint thins over yellow |
| 8% | `#C06C31` | purple thinning over yellow reads brown-orange |

Findings: the yellow is more amber than the suggested `#FFB509` (hue 40° vs 43°), and the purple is darker than `#530871`. Adopted `#F8AA09` and `#4F0964`. Painted quality: bristle streaks at the stroke's edge, dry brush ends, slight tonal variation in the yellow. We reproduce this once, as a rough-edged swash on S1, and in the grain of the shell. Not reproduced: the hand, caption bar, or any of the photo.

## B — Historical colour wheel
Aged cream paper with fine engraved lines and a printed title.
| Share | Hex |
|---|---|
| ~58% in total | `#F6E8D1`, `#FAEAD3`, `#F5E5CE`, `#EDE0CA` (paper) |
| 14% | `#8F7857` (aged line and shadow brown) |
| 12% | `#A1413C` (brick red) |
| 9% | `#ABAD8B` (muted sage) |
Adopted: paper `#F6E8D1` as the work surface, `#EDE0CA` as the sunken tone, `#FBF3E4` one step lighter for inputs, and brick `#A1413C` as the error colour. Taken as principles: fine hairlines, wide margins, serif numerals. Not taken: script lettering, ornaments, the wheel itself.

## A — Orange and blue
Watercolour on paper: indigo over orange and amber, pigment bleeds, grainy paper tooth.
| Share | Hex |
|---|---|
| 32% | `#F88526`, `#FA8621`, `#FAA020` (orange and amber) |
| 43% | `#23437C`, `#2D476E`, `#1F3664` (blue) |
Adopted: orange `#F88526`, blue `#23437C` (and `#1F3664` for depth). Taken as principle: pigment colours are used flat and saturated, and paper tooth is the texture. Not taken: bleeds and gradients between colours (rejected for readability).

## Palette outcome
| Role | Value | Origin |
|---|---|---|
| Golden yellow | `#F8AA09` | pixel, ref C |
| Ink purple | `#4F0964` | pixel, ref C |
| Painted blue | `#23437C` | pixel, ref A |
| Pigment orange | `#F88526` | pixel, ref A |
| Paper cream | `#F6E8D1` | pixel, ref B |
| Dark ink | `#241629` | designed: purple-black for text, warmer than neutral black |
| Brick (error) | `#A1413C` | pixel, ref B |

The suggested values `#FFB509`, `#530871`, `#214079`, `#FF792B` were within a few units of these; the pixel versions replaced them because the reference yellow is the one the user prefers.

## Rights
The reference images were studied and not embedded in any asset or the UI. Texture and swash are procedural SVG.
