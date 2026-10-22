# V2 → V3 Changelog

V1 and V2 are untouched in `docs/design/` and `docs/design/v2-prismatic-paper/`. V3 is a new directory.

## Kept
Six screens and their states, requirement mapping, flows, the two Cue signatures (frame strip, CueSheet), the colour family, English-only UI, honest status (no percentages, ETAs, per-frame progress), no artwork on or from the product.

## Changed
| Area | V2 | V3 |
|---|---|---|
| Frame | gold everywhere, ink-on-gold header | purple nav, gold ground on S1–S4, paper ground on S5–S6 |
| Gold share | 33–43% | 0–29%, average about 13% |
| Grouping | 1.5 px black outline on every box | one sheet; hairlines, spacing, tone; strong outline only for selection and focus |
| Titles | Fraunces 46 | Manrope 28; Fraunces only for the S1 hero, wordmark, plan numerals |
| Background | flat gold with grain and fibre | registration-mark pattern on the ground, grain only |
| Artwork | one cartoon face repeated | six ink studies with off-register pigment shapes |
| Primary action | purple with hard shadow | flat purple, no outline |
| Chips | outlined | tinted, borderless |
| CueSheet | boxed lanes, chevrons, elbow arrow | rail, numbered nodes, "then", speed meter |
| S5 | gold, two-row film strip | paper, one-row film strip, status track |
| S6 | gold | paper, dark viewer |
| Palette | `#F8AA09`, `#4F0964`, `#F6E8D1` … | `#FFB509`, `#431452`, `#F5EBD8`, `#FFFAF0` … (brief's starting palette) |

## Token migration
See `migration-from-v2` in `tokens.json`. In short: `bg-shell` → `bg-ground-gold`/`bg-ground-paper`; `bg-surface` → `bg-sheet`; hard shadows → soft elevations; `border-strong` split into hairline, control and strong; focus ring ink → purple.

## Scope check
No screen or feature was added or removed. Open items from V1 (R1–R9, D2–D5) still stand; V2-D1 is superseded by V3-D1.

## Open decisions
| ID | Question |
|---|---|
| V3-D1 | Gold averages about 13%, below the 25–30% guide. Accept, or widen the ground, add a gold ground on S5, or use experiment 3's band? |
| V3-D2 | Purple nav is recommended; confirm against the cream nav. |
| V3-D3 | Mock artwork is a procedural stand-in. Use real example drawings in the final mockups if their rights are cleared. |
| V3-D4 | The paper sheet lifts with a soft shadow; confirm it feels light enough or use flat tone only. |
