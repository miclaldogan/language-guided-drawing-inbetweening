# Accessibility Report (V2)

Target WCAG 2.2 AA. Ratios were computed with the WCAG relative-luminance formula from the token values. Text needs 4.5:1 (large text and UI boundaries 3:1). The six "FAIL" rows are intentional: they document combinations the system forbids, and they are not used in the previews.

## Calculated contrast
| Kind | Pair | Ratio | Needs | Result | Note |
|---|---|---|---|---|---|
| Text | ink on gold (`#241629` / `#F8AA09`) | 8.79 | 4.5 | pass |  |
| Text | ink-700 on gold (secondary text on shell) (`#4B3B52` / `#F8AA09`) | 5.25 | 4.5 | pass |  |
| Text | ink-600 on gold (muted) (`#6B5A72` / `#F8AA09`) | 3.23 | 4.5 | FAIL | banned on gold; use ink-700 |
| Text | ink on cream-200 / cream-100 (`#241629` / `#F6E8D1`) | 14.23 | 4.5 | pass |  |
| Text | ink-700 on cream-200 (`#4B3B52` / `#F6E8D1`) | 8.49 | 4.5 | pass |  |
| Text | ink-600 (muted) on cream-200 (`#6B5A72` / `#F6E8D1`) | 5.22 | 4.5 | pass | metadata |
| Text | ink-600 on cream-300 (sunken) (`#6B5A72` / `#EDE0CA`) | 4.84 | 4.5 | pass |  |
| Text | ink-600 on cream-100 (`#6B5A72` / `#FBF3E4`) | 5.72 | 4.5 | pass |  |
| Text | purple on gold (`#4F0964` / `#F8AA09`) | 6.91 | 4.5 | pass |  |
| Text | purple on cream-200 (`#4F0964` / `#F6E8D1`) | 11.17 | 4.5 | pass | links, Change drawings |
| Text | cream-100 on purple (primary button) (`#FBF3E4` / `#4F0964`) | 12.24 | 4.5 | pass |  |
| Text | cream-100 on purple hover (`#FBF3E4` / `#65198A`) | 9.25 | 4.5 | pass |  |
| Text | cream-100 on purple pressed (`#FBF3E4` / `#3B0650`) | 14.34 | 4.5 | pass |  |
| Text | purple on purple-tint (selected) (`#4F0964` / `#E8D7F0`) | 9.91 | 4.5 | pass |  |
| Text | ink on purple-tint (`#241629` / `#E8D7F0`) | 12.61 | 4.5 | pass |  |
| Text | white on gold (`#FFFFFF` / `#F8AA09`) | 1.95 | 4.5 | FAIL | banned |
| Text | orange-500 on gold (`#F88526` / `#F8AA09`) | 1.28 | 4.5 | FAIL | banned as text/graphic |
| Text | orange-500 on cream-200 (`#F88526` / `#F6E8D1`) | 2.08 | 4.5 | FAIL | banned as text; fill only |
| Text | orange-700 on cream-200 (`#B03E06` / `#F6E8D1`) | 4.91 | 4.5 | pass | orange text token |
| Text | orange-700 on gold (`#B03E06` / `#F8AA09`) | 3.04 | 4.5 | FAIL | do not use on gold |
| Text | ink on orange-500 fill (`#241629` / `#F88526`) | 6.85 | 4.5 | pass | label on orange fill |
| Text | blue on cream-200 (`#23437C` / `#F6E8D1`) | 8.03 | 4.5 | pass |  |
| Text | blue on blue-tint (Running chip) (`#23437C` / `#DCE5F3`) | 7.64 | 4.5 | pass |  |
| Text | blue on gold (`#23437C` / `#F8AA09`) | 4.96 | 4.5 | pass | only large text |
| Text | cream-100 on blue (`#FBF3E4` / `#23437C`) | 8.79 | 4.5 | pass |  |
| Text | red on cream-200 (`#A1413C` / `#F6E8D1`) | 5.21 | 4.5 | pass |  |
| Text | red on red-tint (error) (`#A1413C` / `#F6D9D4`) | 4.73 | 4.5 | pass |  |
| Text | green on green-tint (Done chip) (`#2F6B3B` / `#D9EAD3`) | 5.07 | 4.5 | pass |  |
| Text | warning-brown on yellow-tint (`#8A5A00` / `#FBE6A6`) | 4.79 | 4.5 | pass |  |
| Text | ink on yellow-tint (`#241629` / `#FBE6A6`) | 13.89 | 4.5 | pass |  |
| Text | cream-200 on viewer (film strip numerals) (`#F6E8D1` / `#1B1220`) | 15.06 | 4.5 | pass |  |
| UI | input border ink-600 on cream-100 (`#6B5A72` / `#FBF3E4`) | 5.72 | 3 | pass | inputs, textarea, upload zone |
| UI | ink border on cream-200 (`#241629` / `#F6E8D1`) | 14.23 | 3 | pass | panels, buttons |
| UI | purple border/checkbox on cream-100 (`#4F0964` / `#FBF3E4`) | 12.24 | 3 | pass | selected, plan approval |
| UI | orange-600 on cream-200 (`#D2620F` / `#F6E8D1`) | 3.16 | 3 | pass | endpoint ticks on cream |
| UI | orange-500 on viewer (`#F88526` / `#1B1220`) | 7.26 | 3 | pass | film strip endpoints |
| UI | blue on cream-200 (activity) (`#23437C` / `#F6E8D1`) | 8.03 | 3 | pass |  |
| UI | ink focus ring on gold (`#241629` / `#F8AA09`) | 8.79 | 3 | pass | 2px ink + 2px cream gap |
| UI | ink focus ring on cream-200 (`#241629` / `#F6E8D1`) | 14.23 | 3 | pass |  |
| UI | cream gap on viewer (focus in video region) (`#FBF3E4` / `#1B1220`) | 16.50 | 3 | pass |  |
| UI | hairline on cream-200 (`#CDB99A` / `#F6E8D1`) | 1.58 | 3 | FAIL | decorative only; never sole boundary |

## Findings and how they were handled
| Concern | Result | Decision |
|---|---|---|
| Orange against yellow | 1.28:1, fails | Orange never on gold. On gold, endpoint accents are purple/ink; orange appears only on cream (as `#D2620F`, 3.2:1) or dark film |
| White against yellow | 1.95:1, fails | Never white on gold; ink is used (8.8:1) |
| Purple against yellow | 6.9:1, passes | Purple text and underlines allowed on gold |
| Orange text | 2.1:1 on cream | Orange is never text; `#B03E06` (4.9:1) exists for the rare orange label |
| Muted metadata | 5.2:1 on cream-200, 3.2:1 on gold | Metadata only on cream; ink-700 on gold |
| Form boundaries | 5.7:1 (ink-600 on cream-100) | 1.5 px border; focus 2.5 px ink ring |
| Hover / selected | selected purple border 12:1 on cream; selection also adds the checkmark and tint | not colour only |
| Text over texture | texture ≤12% opacity; inputs and long text are flat | contrast measured on the flat colour; recheck rendered at build |
| Status | each chip has icon, word and colour | no colour-only status |
| Focus | ink ring + cream gap passes on gold (8.8), cream (14.2), and the dark viewer via the gap (15.1) | always visible, never removed |

## Behaviour requirements
Keyboard reachability and order; Esc closes dialogs; arrows in tabs; Space and ←/→ in the player; native file input for uploads (dragging alternative, 2.5.7); target size ≥ 40 px (24 px AA minimum); sticky bar must not cover focused elements (scroll-padding). 200% zoom and 320 px reflow: panels stack, film strip drops to four rows, CueSheet becomes an ordered list. Reduced motion: see motion section below. Forced-colors and `prefers-contrast: more` remove the texture.

## Reduced motion
Removes translations and staggers; transitions become opacity-only at 0–80 ms; S1 strip is static; S5 shimmer (if used) is replaced by static pending frames and live text "Running, 2 min 14 s"; no autoplay of video. Plan reveal, page transition and button feedback timings are unchanged from V1's motion doc, as no motion rule depends on colour.

## Not done
No screen-reader, 200% zoom, forced-colors or keyboard test on a built UI exists yet; these are static SVG renders. User testing for eye comfort has not been done. Rendered anti-aliasing of 13 px Manrope on gold has not been checked on real displays.
