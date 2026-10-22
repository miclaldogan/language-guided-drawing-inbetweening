# Typography (V3)

Fonts unchanged from V2's evaluation (`../v2-prismatic-paper/TYPOGRAPHY_SYSTEM.md`): Fraunces (OFL, Turkish and English glyphs verified) and Manrope (OFL). The change is where each is used.

| Token | Family | Size / line | Weight | Spacing | Use |
|---|---|---|---|---|---|
| wordmark | Fraunces (opsz 72, SOFT 50, WONK 0) | 27 / 1 | 800 | -0.01em | nav and S1 |
| auth-hero | Fraunces | 54 / 62 | 600 | -0.02em | S1 headline only |
| page-title | Manrope | 28 / 34 | 800 | -0.015em | S2–S6 titles |
| section-title | Manrope | 20 / 26 | 800 | -0.01em | "Instruction", "Motion plan" |
| group-label | Manrope | 16 / 22 | 800 | 0 | "Your plan", "Run details", "Details" |
| card-title | Manrope | 14.5 / 20 | 700 | 0 | gallery titles, plan event titles use 17 / 800 |
| body | Manrope | 15 / 24 | 500 | 0 | sentences, instruction input at 16 |
| body-secondary | Manrope | 14 / 22 | 500 | 0 | subtitles, helper text |
| form-label | Manrope | 13.5 / 20 | 800 | 0 | labels |
| metadata | Manrope tnum | 12.5 / 18 | 500 | 0.005em | dates, seed, size, counters |
| button-label | Manrope | 14.5 / 20 | 700 | 0 | buttons |
| status-text | Manrope | 12.5 / 18 | 700 | 0.01em | chips |
| plan-index | Fraunces | 18 / 1 | 600 | 0 | numerals on the plan rail, lining figures |
| numeral | Manrope tnum | 22 / 28 | 700 | 0 | elapsed time |

## Rules
- Fraunces appears in three places: wordmark, S1 hero, plan numerals. The empty state heading ("No animations yet.") may use Fraunces 24 as the one optional editorial moment.
- Section titles never compete with page titles: 20 vs 28, same family, same colour.
- Bold is used for titles, labels and button text; body is 500.
- Numbers in metadata and elapsed time use tabular figures so columns align.
- Minimum text size 12.5 px; metadata is never lighter than ink-600 (5.0:1 on paper).
- Sentence case everywhere; no all-caps.

## Realistic examples (from the renders)
| Element | Rendered as |
|---|---|
| Wordmark | "Cue" Fraunces 800 on purple with 7 ticks, ends gold |
| Dashboard heading | "Your animations" Manrope 28/800 |
| Project title | "Turn the head, then move the eyes" 14.5/700, truncated at 35 characters |
| Motion-plan heading | "Motion plan" 20/800; rail numerals in Fraunces |
| Primary button | "Generate animation" 14.5/700 paper-white on purple |
| Video metadata | "Generated in 3 min 52 s", label 13.5/500 ink-600 and value 13.5/700 ink |
| Empty state | "No animations yet." Fraunces 24/600 + "Upload two drawings to make your first one." body-secondary |
| Error message | "That file is 14.3 MB. Choose an image under 10 MB." 14/800 in brick + 12.5 ink-700 detail |
