# Layout System

Reference 1440×900. Figma Auto Layout compatible.

| Item | Value |
|---|---|
| Nav | 64 px purple, then a 6 px brushed gold stripe |
| Page margin | 72 px left and right (the margin columns carry the registration marks) |
| Content width | 1296 px (12 columns, 24 px gutter) |
| Eyebrow row | baseline y 114: label, hairline, stepper (S3–S6) at the right |
| Page title | Fraunces 34, baseline y 166; subtitle Manrope 14.5 at y 194 |
| Divider | 1 px 16% ink at y 220 |
| Content start | y 244 |
| Footer | hairline at y 784, buttons at y 806 (S3, S4); Back left, primary right |
| Gallery | 4 columns, 24 px gap; card 306 wide: 8 px padding, 8:5 thumbnail, 72 px text area |
| Two-column workspace (S4) | left 520, 1 px divider at x 640, right 684 |
| Worktable (S3) | full-bleed band y 240–756 with two 600×375 slots |
| Viewer (S6) | 864×540 at x 72, details column at x 984 with a 1 px divider at x 960 |
| Corners | gold brush top-left (nav to y 276 at the margin) and bottom-right; neither enters the 72 px content margin |

## Responsive
| Width | Behaviour |
|---|---|
| ≥1280 | as above |
| 1024–1279 | margin 48; gallery 3 columns; S4 columns 45/55 |
| 768–1023 | margin 32; gallery 2 columns; S4 stacks (instruction, then plan); S6 details move below the viewer; film strip 8×2 |
| 640–767 | gallery 2 columns; stepper becomes "Step 2 of 4" under the title |
| <640 | single column, margin 16; footer actions stack and stick to the bottom; film strip 4×4; brush corners and margin marks hidden |
At 200% zoom the layout equals the 720 px case: one column, no horizontal scroll.

## Page templates (Figma frames)
`Template/Auth` (split), `Template/Library` (header, gallery), `Template/Flow` (header with stepper, content area, footer; used by S3–S6). All share nav, eyebrow row, title block and divider.
