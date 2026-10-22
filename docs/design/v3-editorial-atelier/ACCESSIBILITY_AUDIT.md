# Accessibility Audit (V3)

Target WCAG 2.2 AA. Ratios computed with the WCAG relative-luminance formula from `tokens.json` values. Text needs 4.5:1; UI boundaries, focus indicators and graphics need 3:1. Rows marked FAIL are combinations the system forbids or that carry a second cue; none is used as the sole carrier of information.

## Calculated contrast
| Kind | Pair | Ratio | Needs | Result | Note |
|---|---|---|---|---|---|
| Text | ink on gold ground (`#241629` / `#FFB509`) | 9.71 | 4.5 | pass |  |
| Text | ink-700 on gold (S1 body) (`#4D3D55` / `#FFB509`) | 5.61 | 4.5 | pass |  |
| Text | ink-600 on gold (`#6E5F76` / `#FFB509`) | 3.33 | 4.5 | FAIL | not used on gold |
| Text | paper-white on purple (nav text, primary button) (`#FFFAF0` / `#431452`) | 13.82 | 4.5 | pass |  |
| Text | gold on purple (nav indicator, avatar) (`#FFB509` / `#431452`) | 8.12 | 3 | pass | graphic |
| Text | ink on paper (`#241629` / `#F5EBD8`) | 14.53 | 4.5 | pass |  |
| Text | ink-700 on paper (`#4D3D55` / `#F5EBD8`) | 8.40 | 4.5 | pass |  |
| Text | ink-600 muted on paper (`#6E5F76` / `#F5EBD8`) | 4.99 | 4.5 | pass | metadata |
| Text | ink-600 muted on elevated paper (`#6E5F76` / `#FFFAF0`) | 5.67 | 4.5 | pass |  |
| Text | ink-700 on sunken paper (Queued chip) (`#4D3D55` / `#EBDFC8`) | 7.53 | 4.5 | pass |  |
| Text | ink-600 on sunken paper (`#6E5F76` / `#EBDFC8`) | 4.47 | 4.5 | FAIL | avoid for small text |
| Text | purple on paper (links, active) (`#431452` / `#F5EBD8`) | 12.16 | 4.5 | pass |  |
| Text | purple on purple-tint (Ready chip) (`#431452` / `#EFE4F3`) | 11.68 | 4.5 | pass |  |
| Text | blue on blue-tint (Processing chip) (`#23437C` / `#E1E9F4`) | 7.93 | 4.5 | pass |  |
| Text | green on green-tint (Done chip) (`#2F6B3B` / `#DFEBD9`) | 5.18 | 4.5 | pass |  |
| Text | red on red-tint (Failed, error) (`#A1413C` / `#F8E0DC`) | 5.00 | 4.5 | pass |  |
| Text | ink on red-tint (error detail) (`#4D3D55` / `#F8E0DC`) | 7.89 | 4.5 | pass |  |
| Text | paper-white on dark duration chip (`#FFFAF0` / `#3A2C41`) | 12.49 | 4.5 | pass | ink at 86% over art; approximated |
| Text | orange text-safe #B4440F on paper (`#B4440F` / `#F5EBD8`) | 4.70 | 4.5 | pass | orange text token |
| Text | orange #ED782A on paper (`#ED782A` / `#F5EBD8`) | 2.43 | 4.5 | FAIL | forbidden as text |
| Text | orange #ED782A on gold (`#ED782A` / `#FFB509`) | 1.62 | 4.5 | FAIL | forbidden |
| Text | ink-600 disabled label on sunken paper (Continue) (`#6E5F76` / `#EBDFC8`) | 4.47 | 3 | pass | inactive control, exempt; passes 3:1 |
| UI | input border on elevated paper (`#85748A` / `#FFFAF0`) | 4.15 | 3 | pass | inputs |
| UI | input border on paper (`#85748A` / `#F5EBD8`) | 3.65 | 3 | pass |  |
| UI | upload dashed border on upload fill (`#85748A` / `#F9F1E0`) | 3.84 | 3 | pass |  |
| UI | purple focus ring on paper (`#431452` / `#F5EBD8`) | 12.16 | 3 | pass | 2px ring + 2px paper gap |
| UI | purple focus ring on gold (`#431452` / `#FFB509`) | 8.12 | 3 | pass |  |
| UI | purple focus ring on elevated paper (`#431452` / `#FFFAF0`) | 13.82 | 3 | pass |  |
| UI | selected check box purple on paper (`#431452` / `#F5EBD8`) | 12.16 | 3 | pass |  |
| UI | orange-600 graphic #C4531A (speed bars) on paper (`#C4531A` / `#FFFAF0`) | 4.39 | 3 | pass |  |
| UI | gold End tag on elevated paper (fill alone) (`#FFB509` / `#FFFAF0`) | 1.70 | 3 | FAIL | fails alone; ink outline 1.3px (15.5:1) and word "End" carry it |
| UI | ink outline of End tag on elevated paper (`#241629` / `#FFFAF0`) | 16.52 | 3 | pass |  |
| UI | secondary button border on paper (`#85748A` / `#F5EBD8`) | 3.65 | 3 | pass |  |
| UI | film-strip dashed frame on viewer (`#3A2C41` / `#17101C`) | 1.43 | 1 | pass | decorative; state also stated in words |
| UI | hairline #85748A at 14% on paper (`#EBDFC8` / `#F5EBD8`) | 1.12 | 3 | FAIL | decorative divider; never the only boundary (fails by design) |

## Findings
| Concern | Result | Handling |
|---|---|---|
| Orange against yellow | `#ED782A` on gold is 1.3:1 | Orange never sits on gold; speed bars are on paper, as `#C4531A` (4.4:1 on paper-100, 3.9:1 on paper), and each is paired with the word Fast or Slow |
| White against yellow | gold on paper-100 is 1.7:1, and white-ish on gold is under 2:1 | not used; text on gold is ink (9.7:1) |
| Purple against yellow | 8.1:1 | allowed for text and graphics |
| Text over texture | grain 5–7%, pattern 14–20% at 1 px marks | text blocks sit on opaque sheets; the S1 hero has the pattern masked behind it; checked in a 200% render |
| Muted metadata on paper | ink-600 4.99:1 on paper, 5.67 on paper-100 | passes; never on sunken paper below 14 px |
| Form boundaries | `#85748A` 3.65–4.15:1 | pass |
| Hover/selected | selected adds 2 px purple outline (12:1) and tint; hover is an overlay plus cursor | not colour only |
| End identity | gold fill alone 1.7:1 on paper-100 | ink 1.3 px outline (15.5:1), numeral "2", and the word "End drawing" |
| Status | each chip has icon and word; S5 track has icon, shape and word | no colour-only status |
| Focus | purple ring with paper gap passes on paper, paper-100 and gold | never removed |

## Behaviour
Keyboard order follows the visual order; stepper is not clickable forward; Esc closes dialogs; Space and ←/→ in the player; a native file input backs the dropzone (dragging alternative); target size ≥ 40 px for primary controls (small text links are inline links with 24 px minimum target); no motion except small state transitions (see V1 motion doc); reduced-motion removes translations and the optional sweep; no video autoplay. The pattern and grain are removed under `prefers-contrast: more` and forced-colors. 200% zoom and 320 px reflow: sheet padding drops to 16 px, columns stack, film strip becomes four rows of four, rail list stays vertical.

## Checked and not checked
Checked: calculated contrast; visual inspection of every render, including S1 at 200%. Not checked: screen readers, real keyboard test, forced-colors, rendered anti-aliasing of 12.5 px Manrope on real displays, user eye-comfort testing. These need a built UI.
