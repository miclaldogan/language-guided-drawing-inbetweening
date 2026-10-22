# Background Pattern Spec

Pattern and paper texture are separate layers. Texture (grain, 5–7%) gives material warmth everywhere on paper and gold. Pattern gives rhythm and composition and appears only on the ground and the S1 brand panel.

## Candidates (`patterns/pattern-samples.png`)
| | Motif | Verdict |
|---|---|---|
| A | Animation registration marks | **Selected.** Drawn from animation paper and print. Sparse and precise, it adds structure without noise. |
| B | Drafting grid | Rejected: collides with the ruled elements and thumbnails, reads as graph paper. |
| C | Halftone dots | Rejected: busy at 200% zoom, reads as generic texture. |
| D | Frame-sequence rhythm | Rejected: duplicates the 16-frame strip, which should stay a component. |

## Selected: registration marks
| Property | Value |
|---|---|
| Tile | 96 × 96 px, seamless (marks at centre, corner dots shared) |
| Mark | circle r 5 px plus a 22 px cross, 1 px stroke |
| Corner dots | r 1.1 px at tile corners |
| Colour and opacity | on gold: ink `#241629`, marks 20%, dots 18%; on paper: purple `#431452`, marks 16%, dots 14% |
| Placement | page ground margins and the S1 gold panel only |
| Never under | sheets' content, inputs, uploaded drawings, video, motion-plan area (sheets are opaque, so the pattern shows only around them) |
| Responsive | same tile at all widths; hidden below 640 px when the ground is under 24 px wide; removed for `prefers-contrast: more` and forced-colors |
| Zoom | at 200% the tile scales with the page; marks stay 1 px (`vector-effect` not required because it is a background image) |
| Performance | one 400-byte SVG as a CSS background image; no filters, no animation, no canvas |
| Seams | none visible: all elements sit inside or on the tile edge symmetrically |

## Assets
`assets/pattern-registration-on-gold.svg`, `assets/pattern-registration-on-paper.svg`, and `assets/background-patterns.css` (data-URI variables and `.ground-gold` / `.ground-paper` classes). Original, not derived from the reference images.

## Contrast and readability
Text never sits on the pattern. The tightest case is the S1 hero and body on gold; the S1 pattern marks are 20% ink 1 px lines at 96 px spacing and were checked visually in the render: they stay out of the text lines (title at x 64–510, marks every 96 px; a few cross the paragraph margin region). If any mark crosses body text in implementation, mask the pattern in that block with a radial or rectangular fade.

Known limit: in the S1 render a few marks fall between hero text lines, which is tolerable but not ideal.
