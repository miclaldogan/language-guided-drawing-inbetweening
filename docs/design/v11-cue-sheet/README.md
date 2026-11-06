# Cue — v11 Cue Sheet

A full redesign of the public page and the six product screens. It replaces v10 Bordo Herbaryum as the current mockup. The previous studies are kept as history.

Open `index.html` (the public page) or `app.html` (studio screens S1–S6) directly in a browser. There is no build step, and fonts and pictures are local. The screens are interactive mockups: they never connect to the API, database, authentication or generation worker.

## What is new

- **The page performs the product.** The hero holds a working cue sheet. Type an English sentence, or pick an example, and the plan is laid out in lanes (gaze, head, expression, hand) in reading order. The sixteen frames are redrawn from the plan, and you can play them, step through them and use onion skin. A sentence that can't reach the end drawing is refused with a reason, as FR-05 requires.
- **The character is drawn in code** (`cue.js`). One line-drawing figure is controlled by four parameters, so every frame on the page and in the app comes from the same plan. These are illustrations, not model output.
- **Inbetweening, since 1833.** Six real archival pictures and one film set Cue in the history of the craft: a phenakistiscope disc, a zoetrope strip, Muybridge, *The Horse in Motion*, Cohl's *Fantasmagorie* (a muted loop) and McCay's Gertie. Credits are in the footer and in `assets/credits.json`.
- **The studio uses a framed sheet.** A plum-tinted L-frame holds a white sheet. Pink appears only on data (cue blocks, frame strips, the selected frame), and the primary action is near-black.

## Screens and states

The bar at the bottom of `app.html` switches screens and states. They follow `../CUE_SCREEN_BY_SCREEN_UX_PLAN.md`.

| Screen | States |
|---|---|
| S1 Log in | log in, create account, wrong password, logging in |
| S2 Library | animations, empty, loading, fetch error, plus the delete menu with its confirm dialog and toast |
| S3 Drawings | both ready, empty, uploading, wrong file |
| S4 Motion plan | approved, not approved, reading, out of date, refused, no instruction |
| S5 Generation | running, queued, done, failed, cancelled, plus the cancel confirmation |
| S6 Result | ready (play, frame step, loop, scrubber, Space and arrow keys), video failed |

## Proposed changes to review

- **Library poster frame.** The cards show frame 9 instead of frame 1. People often reuse the same start drawing, so first frames would make every card look the same. The UX plan says first frame; this needs a decision.
- **Primary action colour.** In the app the primary action is near-black, not orange, and the brand pink is kept for data. "One primary per screen" still holds.

## Sample data to replace

Everything in `app.js` → `JOBS`: job IDs, titles, dates, seeds, durations, file sizes, the failure reason and the model name `cue-ib 0.1-dev`. The account "İclal Doğan / iclal@example.edu" is sample data too. Upload limits stay "to be set" (R1).

## Files

- `index.html`, `page.css`, `page.js`: the public page
- `app.html`, `app.css`, `app.js`: the studio screens
- `cue.js`: the shared figure, plan parser and frame planner
- `fonts/`: Switzer 400/500/600 (Fontshare, self-hosted)
- `assets/`: archival pictures and the film excerpt, with `credits.json`
- `screenshots/`: renders at 1440 × 900 and 390 × 844
- `DESIGN_DIRECTION.md`: the direction, the palette and the motion decisions
- `.taste-skill/`: the dealt direction sheets (page and app), kept for reference
