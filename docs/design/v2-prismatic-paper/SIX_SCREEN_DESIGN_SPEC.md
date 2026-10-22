# Six-Screen Design Spec (V2)

Functionality, states, requirement links and flows are unchanged from V1 (`CUE_SCREEN_BY_SCREEN_UX_PLAN.md`, `CUE_REQUIREMENTS_UI_TRACEABILITY.md`). This file says only how Prismatic Paper changes presentation. Reference frame 1440×900; previews in `previews/`. All copy is English. Values such as the 10 MB limit are placeholders until the backend fixes them (R1).

Shared: gold shell with a 1.2 px ink rule under the top bar; wordmark left, "Library" nav, account menu right; on S3–S6 a four-step stepper (Keyframes, Motion, Generate, Result) with the current step in purple; screen title in Fraunces; content in cream panels with 1.5 px ink border and a hard 3 px print shadow; one purple primary action per screen at the bottom right, Back at the bottom left.

| Screen | Preview | Change from V1 |
|---|---|---|
| S1 Authentication | `s1-authentication_A` | Split: left gold brand field, right cream form. Headline "Two drawings in. One animation out." in Fraunces 72. Under it, a rough-edged purple swash holds five frames turning; first and last have orange outlines labelled "Your start" and "Your end". Form: Log in / Create account tabs, labelled Email and Password fields (46 px), "Show" text toggle, purple "Log in". Focus visible as ink ring. The artistic part is the left; the form stays plain. |
| S2 Dashboard | `s2-dashboard_A`, `_B` | Title "Your animations" and purple "New animation" on gold. Cards sit directly on gold (A) so the gallery is the colour; each card is cream with ink outline and a thumbnail on the user's own paper. Status chips (Done, Running, Queued, Failed) have icon and word. Running and Queued thumbnails are dimmed with a small frame strip; Failed has a red-tint placeholder with a triangle and reason. No metrics. |
| S3 Keyframe Upload | `s3-keyframes_A` | Cream panel with two equal slots on a flat white canvas. Start is a purple numbered circle, End an orange square badge, both with words. Filled slot shows the drawing unmodified with file name, size, Replace, Remove. Empty slot is dashed with Browse files; the error shows a red-tint bar with triangle and a plain instruction. Continue is disabled (cream-300) with a helper line, not orange or purple. |
| S4 Motion Prompt and Plan | `s4-motion-plan_A`, `_B` | Left panel: instruction text area (English, optional), counter, two example chips, "Preview plan", and small start/end keyframes with "Change drawings". Right panel: CueSheet with a 16-tick ruler (ends orange, labelled Start drawing / End drawing), ruled lanes (Gaze, Head), numbered cue blocks, ink elbow arrow, speed chevrons, "Order is shown, not exact timing" caption, then a one-line plain-language summary and the approval checkbox. Purple "Generate animation" bottom right. |
| S5 Generation Status | `s5-status_A` | Running chip, elapsed time as a Fraunces numeral, then the 16-frame printed film strip in two rows of eight. Frames 1 and 16 show the user's drawings with orange outlines; frames 2–15 are hatched paper (pending). No percentage, no ETA; a sentence says so. Right panel: plan, job, submitted time, model version, seed, and a red-outline Cancel generation. "Back to Library" bottom left. |
| S6 Result Preview | `s6-result_A` | The clip is the largest element, on a dark neutral viewer inside the cream panel; the page stays gold. Controls: play, previous/next frame, loop, and the frame strip as scrubber with a purple current-frame outline. Right panel: purple "Download MP4", details (plan, format, length, created, generation time, model version, seed), Back to Library, New animation. |

## S4: the CueSheet in detail
- Ruler: sixteen ticks across the lane width; first and last are taller and orange. They mean "your drawings", not specific events.
- Lanes: region name at left (vocabulary pending, R7); one ruled strip per lane used by the plan.
- Cue block: purple-tint fill, ink 1.5 px outline, purple disc with printed number, action title, region and speed, then three chevrons with the speed count filled in orange-700 (not colour alone: the words "fast"/"slow" are also shown).
- Order: cues step down and to the right; an ink elbow arrow joins each cue to the next. Block widths are fixed; positions imply order only.
- Plain-words line mirrors the plan for quick reading and for screen readers (the DOM is an ordered list).
- States: skeleton ("Reading your instruction…"), ready, out of date (muted, approval cleared), rejected (amber-tint alert with the reason and an example). No drag, resize or timing editing.

## Empty, processing, error coverage
Empty: S2 "No animations yet. Upload two drawings to make your first one." with a secondary "New animation". Processing: S2 chips, S5 film strip. Errors: S1 form alert, S2 failed card, S3 slot error, S4 rejected plan, S5 failed state with message and links, S6 video load error. All keep the V1 behaviours.

## Responsive
Unchanged from V1. At ≤1023 px the side panels stack below the stage; S5 film strip becomes four rows of four; S4 lanes become an ordered vertical list; S1 stacks the form above a shortened brand field.
