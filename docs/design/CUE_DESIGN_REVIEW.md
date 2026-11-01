# Cue — Strict Design Review

> Historical review of the superseded Midnight Motion concept. Its palette, style tiles, and findings do not describe the current design. See [Bordo Herbaryum](v10-bordo-herbaryum/index.html) and its [design direction](v10-bordo-herbaryum/DESIGN_DIRECTION.md).

Reviewer stance: creative director, no credit for effort. Review is of the specifications and two style tiles, not of built screens; nothing has been tested with users.

## 16 questions
| # | Question | Verdict |
|---|---|---|
| 1 | Recognisable identity? | Partly. The frame strip and cue sheet are ownable, but only if they are drawn well. A dark purple UI with an orange button is common; the strip is what separates Cue. Risk: if the strip is only on S1 it becomes decoration. Kept it functional on S2, S5, S6. |
| 2 | Palette cohesive? | Yes on the tiles. Blue and yellow are both light and bright; keeping them rare is what prevents chaos. |
| 3 | 60/30/10 appropriate? | Yes as a guide. In practice the 10% is mostly empty; most screens show orange once and one other accent. |
| 4 | Orange reserved? | Yes: Generate, Download, New animation. Weakness: "New animation" in the top bar and an orange primary on the same screen (S2 empty state) would double up. Rule added: on S2 the top bar button is the only orange one; the empty state uses a secondary button. |
| 5 | Purple meaningful? | Selection, active nav, plan. Risk of creep into headings; forbidden in the color rules. |
| 6 | Blue/yellow consistent? | Blue = in progress, yellow = attention. Both pass contrast as text on dark. |
| 7 | Comfortable for long sessions? | Plausible, but unverified. Sessions in Cue are short (upload, prompt, wait), so "long session" matters less than reading the plan clearly. Pure white drawing paper on a dark frame is the biggest glare risk; consider dimming the paper to `#F4F1FA` (already) and offering no toggles. |
| 8 | Accessible? | All text pairs pass AA by calculation. Not yet tested with real assistive tech. |
| 9 | Fonts right for an animation tool? | Sora has personality; Manrope is a neutral UI face. Fine. Neither is distinctive by itself. |
| 10 | Generic AI dashboard? | Avoided structurally (no sidebar, no stat cards, no chat). The dashboard card gallery is conventional; its distinction is the 8:5 media thumbnails and chips. |
| 11 | Understandable without instructions? | S3 and S6 yes. S4 needs the "Order shown, not exact timing" caption and one example, which the plan includes. |
| 12 | One product? | Yes by shared shell, stepper, action row and one-orange rule. |
| 13 | Empty / processing / error covered? | Covered per screen in the UX plan. |
| 14 | S4 distinctive? | The cue sheet is. Honest caveat: lanes with bar widths suggest timing the model does not expose; we mitigate by labelling order-only and fixed block widths. If the plan schema is just an ordered list, the lane view still works but is lighter on information. |
| 15 | Implementable on schedule? | UI is 5–7 weeks in the proposal. The component set is about 20 components, no canvas, no charts. The risk items are CueSheet and PlayerControls; all else is standard. Ship a plain ordered list first, lanes second. |
| 16 | Every screen justified? | Yes, see traceability. S5 is the weakest case: it is justified by FR-07 but a thin screen; it earns its place because it is where users spend waiting time. |

## Changes made because of this review
1. Fixed one orange per screen conflict on S2.
2. Changed S3 Continue to non-orange so orange keeps its meaning.
3. Made the cue sheet explicitly order-only (fixed block widths, caption).
4. Dropped Space Grotesk to keep two families.
5. Kept the focus ring neutral to avoid colour-meaning collisions.
6. Mobile support kept because no canvas is required.

## Weaknesses not resolved
- A and B tiles are close at thumbnail size; the choice is partly a judgement call.
- No real drawings were used in tiles; line art on dark may look different.
- The logo is a concept only, not a designed mark.
- Turkish vs English UI, upload limits, plan vocabulary and cancel are open (see below).

## Decisions requiring review
| ID | Decision |
|---|---|
| D1 | UI language: English recommended (commands are English), Turkish would add translation work |
| D2 | Confirm cancel action (R2) |
| D3 | Confirm region and speed vocabulary and whether events can be simultaneous (R7) |
| D4 | Whether to build a preset-plan picker (proposal fallback) |
| D5 | Upload limits (R1) |
| D6 | Whether the instructor's Figma review expects Turkish labels |
| D7 | Top bar instead of sidebar (the brief listed a sidebar component) |
