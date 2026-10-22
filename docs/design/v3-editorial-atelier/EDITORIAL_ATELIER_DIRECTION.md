# Cue — Editorial Atelier

"A modern creative workstation shaped by the visual language of traditional animation, paper, ink and editorial design."

## How it works
- **Frame:** a deep purple navigation bar. Under it, a golden ground carrying registration marks on S1–S4, with one warm-paper sheet laid on it (like a sheet on a lightbox desk). On S5 and S6 the ground is warm paper with a 4 px gold rule under the nav, so status and playback stay calm.
- **Content inside the sheet:** grouped by space, hairlines and tone, not by boxes. Raised paper (`#FFFAF0`) is for inputs and drawings; the sheet is `#F5EBD8`.
- **Colour roles:** purple = structure and the primary action; gold = the brand ground and the End identity; blue = processing; orange = motion (speed meters, never text); ink = text.
- **Type:** Fraunces for the S1 hero, the wordmark and printed plan numerals. Manrope everywhere else, including page titles.
- **Art:** mock keyframes are ink-line studies with one flat pigment shape slightly off-register, so the content looks like printed animation studies instead of a drawing tutorial. They are mockup content only; no art generation is implied.
- **Signatures kept:** the 16-frame strip (start tick purple, end tick gold with ink outline) and the CueSheet, now a sequence notation with a rail.

## Experiments (rendered at 1440×900, S2 with real content)
| | Image | Gold | Verdict |
|---|---|---|---|
| 1 Purple nav, paper sheet on patterned gold | `experiments/experiment-1.png` | 19% | **Selected.** Strongest identity; the purple bar separates chrome, the gold frames the work, the sheet is clean. |
| 2 Cream nav, yellow editorial accents | `experiment-2.png` | 1% | Most refined, but gold nearly vanishes and the nav barely differs from the page. Loses the brand. Its pattern also leaked under the gallery (lesson: pattern only on the ground). |
| 3 Purple nav, restrained gold band | `experiment-3.png` | 12% | Good, but the pattern in the band ran under the subtitle, and the paper area below looked empty. Kept as the fallback if experiment 1's gold ground feels strong. |

## Principles
1. Artwork and video are the saturated content; the UI is quiet around them.
2. Borders only where an element needs to be identified or is selected.
3. Pattern and texture are different layers; neither sits under text, inputs, artwork or video.
4. One primary action per screen, always purple.
5. English only; copy is plain and states what happens.

## Avoid list (checked against renders)
Not a chatbot, not dark SaaS, not childish (no mascot, no cartoon face), not museum-like (no ornament, no script), not a gradient-card template. The honest risk: cream paper with a serif is a popular look; here the serif is confined to the hero and numerals, and the purple bar, gold ground and registration marks are what carry the difference.

## Acceptance test (answers backed by renders)
1. Professional creative software? Closer than V2: a purple nav, one sheet, quiet type, believable art. Still a static mock; real data will vary.
2. Navbar identity? Yes; the purple bar with gold end ticks and indicator is recognisable.
3. Gold recognisable? Yes on S1–S3 (17–29%); weaker on S4 (10%) and nearly absent on S5–S6 by design. Flagged V3-D1.
4. Eye strain reduced? Plausibly: gold appears as a frame, long reading is on paper with ink at 14:1. Not tested with users.
5. Pattern sophisticated and subtle? Yes at 100% and at 200% (checked in the S1 render), masked behind the hero text.
6. Paper warm, not dirty? Yes in renders; sunken paper is used sparingly.
7. Thick outlines only when necessary? Yes; none remain on panels, cards or buttons.
8. Typography appropriate? Yes; Manrope on all operational screens, Fraunces limited.
9. Less childish? Yes; the biggest change is the artwork and the removal of outlines.
10. Drawings and video primary? Yes: thumbnails, upload slots and the viewer are the largest and most saturated elements.
11. Six screens consistent? Yes: same nav, sheet, header, footer.
12. Practical for one developer? Yes: one sheet component, flat buttons, an SVG background; the CueRow rail and film strip are the only custom parts.
13. Requirements preserved? Yes; traceability unchanged.
14. English only? Yes; every string in the renders is English.
Weak spots after revision: the mock studies are simple vector shapes, not real drawings; S4–S6 carry little gold; the registration-mark pattern is nearly invisible at normal viewing, which is intended but means it adds little.
