# Colour and Surface System

Starting palette kept with no hex changed; four derived values were added only for contrast reasons. Tokens: `tokens.json`.

## Palette
| Name | Hex | Role |
|---|---|---|
| Golden yellow | `#FFB509` | brand ground (S1–S4), nav indicator, End identity |
| Deep purple | `#431452` | nav, primary action, selection, plan index |
| Warm paper | `#F5EBD8` | sheet and paper ground |
| Elevated paper | `#FFFAF0` | inputs, artwork matte, raised items |
| Sunken paper | `#EBDFC8` | queued chip, disabled controls (derived) |
| Dark ink | `#241629` | text |
| Painted blue | `#23437C` | processing, info |
| Pigment orange | `#ED782A` | motion accent as a fill; never text |
| Orange text-safe `#B4440F`, graphic `#C4531A` | derived: `#ED782A` fails on paper (2.43:1) |
| Ink-700 / ink-600 | `#4D3D55` / `#6E5F76` | secondary and muted text; ink-600 is not used on gold (see audit) |
| Input line | `#85748A` | 3.65–4.15:1 on paper |

## Distribution (visual guide, measured on the final renders)
| Screen | Gold | Paper surfaces | Purple | Other (art, accents) |
|---|---|---|---|---|
| S1 Auth | 29% | 41% | 17% | 12% |
| S2 Dashboard | 20% | 55% | 8% | 17% |
| S3 Upload | 17% | 70% | 7% | 6% |
| S4 Motion plan | 10% | 75% | 8% | 7% |
| S5 Status | 0% | 78% | 7% | 15% |
| S6 Result | 3% | 79% | 8% | 11% |
Target was 55–60% paper, 25–30% gold, 10–15% purple and pigment. Result: paper is on target or above (41–79%); gold averages about 13%, below the target; purple averages 9% and other colour (artwork, chips, pigment) about 11%. This follows the brief ("do not force every screen into the same distribution"), but gold is under-represented on S4–S6. Levers if more gold is wanted: wider ground margins (56 px) on S3–S4, a gold ground on S5, or the experiment-3 band. Decision V3-D1.

## Roles
| Need | Token |
|---|---|
| Navigation | `bg-nav` purple, `text-on-nav` paper-white, `nav-indicator` gold |
| Ground | `bg-ground-gold` / `bg-ground-paper` |
| Work surface | `bg-sheet`; raised `bg-surface-raised`; sunken `bg-surface-sunken` |
| Work canvas | `bg-canvas` (artwork matte), `bg-viewer` (video) |
| Primary / secondary action | purple fill / paper-100 with line border |
| Active selection | `selected-bg` tint plus `selected-outline` 2 px purple |
| Upload zone | `bg-upload`, dashed `border-input` |
| Motion plan | `plan-index` and `plan-rail` purple, `motion-accent` for speed |
| Processing / warning / error / success | blue / amber / brick / green, each with a tint |
| Focus | 2 px purple ring plus 2 px paper gap |

## Surfaces and borders
| Level | Use | Treatment |
|---|---|---|
| Ground | page background | gold or paper, pattern layer, grain 7% / 5% |
| Sheet | one per screen | paper-200, radius 14, soft shadow (elevation 2), 1 px ink 10% edge, grain 5% |
| Raised | inputs, artwork matte, secondary buttons | paper-100 |
| Sunken | queued chip, disabled | paper-300 |
Borders: none where tone and spacing group (sheet sections, gallery items); hairline (ink 12%) for dividers and secondary edges; control border (`#85748A`, ≥3:1) for inputs and upload; strong 2 px purple for selected and focus.

## Paper warmth
Paper is `#F5EBD8`/`#FFFAF0`: yellow-warm, low saturation, with 5% grain. The risk of looking dirty comes from grey-brown tones, so the sunken tone is used only for small inactive elements.
