# Colour Palette and 60/30/10

Values in `tokens.json`. Ratios are in `ACCESSIBILITY_REPORT.md`.

## Hierarchy
| Share (visual balance) | Role | Colours |
|---|---|---|
| ~60 | Golden shell (frame, header zone, margins, gaps) | gold-500 `#F8AA09`; highlight `#FBC750` for hover/featured only |
| ~30 | Cream work surfaces | cream-200 `#F6E8D1` panels; cream-100 `#FBF3E4` inputs and raised; cream-300 `#EDE0CA` sunken; paper-white `#FFFDF7` behind drawings |
| ~10 | Ink and pigment | ink `#241629`, purple `#4F0964`, blue `#23437C`, orange `#F88526`/`#D2620F`, state colours |

Measured on the previews (pixel classification): gold 33–43% in A, cream/paper 40–49%, other 10–20%. Gold leads outright only on S5; on the other screens cream/paper is 1–13 points larger. The gold share is below the requested 60%; see VISUAL_DIRECTION.md and decision V2-D1.

## Semantic roles (re-evaluated from scratch)
| Role | Token | Value |
|---|---|---|
| Main app background | bg-shell | `#F8AA09` |
| Content surface | bg-surface | `#F6E8D1` |
| Elevated paper (inputs, cards) | bg-surface-raised | `#FBF3E4` |
| Sunken (ruled lanes, disabled) | bg-surface-sunken | `#EDE0CA` |
| Work canvas (behind artwork) | bg-canvas | `#FFFDF7` |
| Video viewer | bg-viewer | `#1B1220` |
| Primary / secondary / muted text | text-primary / -secondary / -muted | `#241629` / `#4B3B52` / `#6B5A72` |
| Primary action | action-primary | `#4F0964` (hover `#65198A`, pressed `#3B0650`), cream text |
| Secondary action | action-secondary | cream-100 fill, ink outline, ink text |
| Danger action | action-danger | `#A1413C` outline and text |
| Active selection | selected-bg / -border | `#E8D7F0` / `#4F0964` |
| Upload zone | upload-border / -bg | dashed `#6B5A72` on `#FBF3E4` |
| Motion plan | plan-cue-bg, plan-cue-number-bg | `#E8D7F0`, `#4F0964` |
| Motion accent | motion-accent / -fill | `#D2620F` graphics on cream; `#F88526` fill with ink content |
| Processing / info | info / info-bg | `#23437C` / `#DCE5F3` |
| Warning | warning / warning-bg | `#8A5A00` / `#FBE6A6` |
| Error | error / error-bg | `#A1413C` / `#F6D9D4` |
| Success | success / success-bg | `#2F6B3B` / `#D9EAD3` |
| Focus | focus-ring + focus-gap | ink 2 px + cream 2 px gap |
| Borders | border-strong / -input / -hair | `#241629` / `#6B5A72` / `#CDB99A` (hair is decorative only) |

## Consistent purposes
- **Purple = Cue's ink:** primary action, selection, plan numbers, links.
- **Orange = motion:** the first/last frame ticks, speed chevrons, the End badge, "Start/End" labels. Never a button colour, never body text.
- **Blue = work in progress:** Running chip, info.
- **Gold = the brand surface.** Not a status colour; warnings use amber-tint on cream with a triangle icon, so they are not confused with the shell.
- Status always has a word and an icon.

## Rules learned from the contrast results
1. Orange `#F88526` fails as text or graphic on both gold (1.28) and cream (2.08). Use it only as a fill with ink content (6.85), or use the darker `#B03E06` (4.9 on cream) for text and `#D2620F` (3.2 on cream) for graphics.
2. White on gold is 1.95; use ink or cream-on-purple instead.
3. Muted ink-600 on gold is 3.23; on gold use ink-700 only.
4. Purple on gold is 6.9, so purple text on the shell is allowed.
