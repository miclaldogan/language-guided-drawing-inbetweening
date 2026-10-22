# Six-Screen Redesign (V3)

Functionality, states and requirement links are unchanged (`../CUE_REQUIREMENTS_UI_TRACEABILITY.md`, R1–R9 still open). Previews: `previews/`. All mock artwork is placeholder content for mockups.

Shared frame (S2–S6): 64 px purple nav; ground; one sheet at x 40 with 32 px padding; page title Manrope 28 with a one-line subtitle; hairline; content; hairline footer with Back left and the one primary action right. A four-step stepper (Keyframes, Motion, Generate, Result) sits at the right of the title row on S3–S6.

| Screen | Ground | What changed |
|---|---|---|
| S1 Authentication | gold, 29% gold | Asymmetric: left gold panel with registration marks, Fraunces hero "Two drawings in. One animation out.", a purple study block bleeding off the left and bottom edges with three different keyframe studies (Start drawing, Drawn by Cue, End drawing) and a 16-tick strip; right paper panel with a calm form (tabs, labelled fields with 1 px borders, 2 px purple focus, "Show", purple Log in). |
| S2 Dashboard | gold with pattern | Sheet with title, count, purple "New animation", hairline, then a 4-column unboxed gallery. Eight different studies; chips for Processing, Queued, Done, Failed; durations on done items. Gold shows around the sheet and below it. |
| S3 Keyframe Upload | gold | Two large equal slots, 8:5. Start (purple 1) shows an uploaded study; End (gold 2) is a dashed dropzone with the error beneath it. Replace and Remove for filled slots; Continue disabled with a reason. |
| S4 Motion Plan | gold | Left: instruction (field, counter, examples, Preview plan) and the keyframe pair with Start/End tags. Right: "Motion plan" with a rail of numbered events (Look left, Fast; Turn left, Slow), "then" between them, a plain-words sentence, the approval checkbox with the caption "Order and speed only. Exact frame timing is not part of the plan.", and the 16-tick output strip. Footer: Back and purple Generate animation. |
| S5 Generation Status | paper | Three-step status track (Queued, Processing, Completed) with Processing active; Elapsed in tabular numerals; a single-row dark film strip with frames 1 and 16 shown and 2–15 as dashed pending frames; your plan and run details; Cancel generation. Failed variant: `s5-generation-status-failed.png` (red marker, message, New animation). No percentage, no per-frame progress, no ETA. |
| S6 Result Preview | paper | Dark viewer with the clip at 8:5 as the largest element, refined controls (play, previous, next, loop, strip scrubber, "Frame 8 of 16"). Right: purple Download MP4, details as label/value rows with hairlines, Back to Library and New animation. |

## S4 CueSheet rationale
A sequence notation: rail + numbered nodes + the word "then" shows order with no arrows. Speed is a three-bar meter and a word (not colour only). Nothing aligns to frame positions, so nothing suggests exact timing. The 16-tick strip appears separately as the output (start drawing, 14 generated frames, end drawing).

## States not drawn as separate images
S2 empty and error, S3 drag-over and uploading, S4 rejected plan and out-of-date plan, S6 video error, dialogs. They follow the component rules and V1's UX plan.
