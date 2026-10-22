# Typography System

## Decision
**Fraunces** (headings, wordmark, numerals) + **Manrope** (all interface text). Two families.

## Evaluation (files inspected)
| | Fraunces | Newsreader | Manrope |
|---|---|---|---|
| Latin and Turkish (ğ Ğ ş Ş ı İ ç Ç ö Ö ü Ü), digits, quotes, dashes | present | present | present |
| "→" arrow | missing | missing | present (so no arrows in headings; use words) |
| Variable axes | opsz 9–144, wght 100–900, SOFT 0–100, WONK 0–1 | opsz 6–72, wght 200–800 | wght 200–800 |
| Licence | SIL OFL 1.1 | SIL OFL 1.1 | SIL OFL 1.1 |
| Figma | in Google Fonts library | same | same |
| Small-size readability | not for UI; display use only | good for text | good |
Rendered side by side on gold: Newsreader is calmer and more conventional; Fraunces with SOFT 50 has rounded, inky terminals that suit "drawn" more than "printed". Chosen: Fraunces. Settings: `opsz` auto, `SOFT 50`, `WONK 0` (WONK 1 adds leaning forms that look quirky at headline size). Newsreader remains the fallback if Fraunces' character ever tires.
Not verified: rendering on Windows ClearType at 13 px (Manrope) and the WOFF2 sizes; do this after subsetting.

## Loading
Self-host both as WOFF2 variable files, subset to Latin plus Latin Extended. Preload Fraunces (opsz+wght) and Manrope; `font-display: swap`; fallback `Georgia` and `system-ui`. Because Fraunces is only used on short headings, consider instancing it to `wght 600/800` with SOFT baked in to cut size (the previews use exactly that static instance). Expected cost is roughly 60–100 KB for both; estimate, to confirm.

## Scale (full table in tokens.json)
| Token | Family | Size / line | Weight | Spacing | Use |
|---|---|---|---|---|---|
| wordmark | Fraunces | 34 / 1 | 800 | -0.01em | Cue wordmark only |
| display-hero | Fraunces | 72 / 80 | 600 | -0.02em | S1 headline only |
| screen-title | Fraunces | 46 / 52 | 600 | -0.015em | page titles S2–S6 |
| section-heading | Fraunces | 26 / 32 | 600 | -0.005em | panel headings ("Motion plan") |
| card-title | Manrope | 15 / 22 | 800 | 0 | gallery card title |
| body | Manrope | 16 / 26 | 500 | 0 | sentences, instruction text |
| body-secondary | Manrope | 14 / 22 | 500 | 0 | helper text |
| form-label | Manrope | 14 / 20 | 800 | 0 | always-visible labels |
| metadata | Manrope tnum | 13 / 20 | 500 | 0.005em | dates, seed, size |
| button-label | Manrope | 15 / 20 | 700 | 0.005em | buttons |
| status-text | Manrope | 13 / 20 | 700 | 0.01em | chips |
| numeral | Fraunces tnum | 22 / 28 | 600 | 0 | elapsed time, cue numbers |

## Usage rules
- Fraunces is for headings, the wordmark and printed numerals (cue numbers, elapsed time). Never for labels, buttons, errors or metadata.
- Minimum text size 13 px; sentence case throughout; no all-caps.
- Hierarchy comes from size, weight and the serif/sans change, not from colour alone.
- Line length under 72 characters.

## Realistic examples (as rendered in the previews)
| Element | Style |
|---|---|
| Wordmark | "Cue" Fraunces 800, preceded by seven ticks, endpoints purple |
| Dashboard heading | "Your animations" screen-title, ink |
| Project title | "Move the eyes left, then turn the head" card-title (truncate at 34 characters) |
| Motion-plan heading | "Motion plan" section-heading |
| Primary button | "Generate animation" button-label, cream on purple |
| Video metadata | "Generated in 3 min 52 s", metadata, ink-600 label with ink value |
| Empty state | "No animations yet." section-heading style + "Upload two drawings to make your first one." body |
| Error message | "That file is 14.3 MB. Choose an image under 10 MB." Manrope 800 in error colour plus body-secondary line below |
