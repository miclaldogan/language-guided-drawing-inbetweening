# V3 → V4 Changelog

V1–V3 are preserved. V4 changes the page architecture, not the product.

| Area | V3 | V4 |
|---|---|---|
| Page structure | gold ground, one large rounded paper sheet with all content | paper canvas is the page; content sits directly on it |
| Outer shadow and radius | sheet shadow, radius 14 | none |
| Gold | ground around the sheet (10–20%) | brushed corners, stripe under the nav, S1 panel; 2–4% on S2–S6, 31% on S1 |
| Registration marks | tiled over the ground | sparse margin marks with guide lines |
| Brush | S1 swash only | S1, corners, nav stripe; limited by explicit rules |
| Page title | Manrope 28 | Fraunces 34 with a Manrope eyebrow row |
| Header | title + subtitle + stepper | eyebrow row (+stepper), title, subtitle, divider |
| Gallery | unboxed thumbnails | cards with 8 px padding, kebab menu and hairline |
| S3 | two slots inside the sheet | full-bleed worktable band |
| S4 | columns inside the sheet | two columns divided by a hairline on the page |
| S5 / S6 | paper ground with a sheet | page directly; film strip and viewer as functional surfaces |
| Overlays | not shown | dialog with scrim as level 3 |

## Token migration
See `migration-from-v3` in `tokens.json`: `bg-sheet` removed; `bg-ground-*` → `bg-page`; new `bg-card`, `bg-worktable`, `bg-dialog`, `bg-scrim`, `text-eyebrow`; elevation reduced to `card` and `overlay`.

## Scope check
No screen, state, field or action changed. The kebab menu is the placement for the existing delete action (FR-09).

## Open decisions
| ID | Question |
|---|---|
| V4-D1 | Gold is 2–4% on operational screens. Keep as brand edges, or add more (larger corners, gold section accents)? |
| V4-D2 | Fraunces 34 for page titles, or return to Manrope 28 (V3)? |
| V4-D3 | Confirm kebab-menu delete and the dialog copy |
| V4-D4 | Canvas weave was not explored; decide whether it is worth a test |
