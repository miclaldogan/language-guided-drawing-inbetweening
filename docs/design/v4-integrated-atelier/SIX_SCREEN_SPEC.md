# Six-Screen Spec (V4)

Functionality, states and requirement links are unchanged (`../CUE_REQUIREMENTS_UI_TRACEABILITY.md`). Previews in `previews/`. Mock artwork is placeholder content.

| Screen | Composition |
|---|---|
| S1 Authentication | Brand split kept and made more painterly: the gold panel's right edge is brushed; a brushed purple block holds three keyframe studies and the 16-tick strip; hero in Fraunces 54; right side is a plain paper page with a calm form. Only screen allowed this much brush. |
| S2 Dashboard | Eyebrow "Library", Fraunces 34 title, purple New animation, divider, then an unboxed 4-column gallery on the page. Cards: 8 px padding, 8:5 thumbnail, title, kebab menu (where Delete lives, FR-09), date, status chip. Gold only in the corners and stripe. Overlay state: `overlay-delete-dialog.png`. |
| S3 Keyframe Upload | A continuous worktable: one full-bleed tonal band carrying both 600×375 artwork surfaces, Start (purple 1) and End (gold 2), a connector between them, file row, and the error under the End zone. Footer integrated with a hairline. |
| S4 Motion Plan | Two columns on the page, split by a 1 px line: Instruction (field, examples, Preview plan, keyframes) and Motion plan (rail with numbered events and "then", speed meter, plain-words line, approval, 16-tick output strip). Footer action row below a hairline. |
| S5 Generation Status | Status track, elapsed time, a single-row film strip (frames 1 and 16 shown, 2–15 dashed pending), then plan and run details separated by a 1 px divider, with Cancel generation. Failed variant rendered. No percentage, per-frame progress or ETA. |
| S6 Result | The 864×540 viewer is the centre; controls (play, frame step, loop, strip scrubber, "Frame 8 of 16") sit beneath it; a vertical divider separates Download MP4 and the detail rows. No enclosing panel. |

Shared across S2–S6: nav, stripe, eyebrow row, title block, divider, margin marks, brush corners, footer pattern. Stepper on S3–S6.
