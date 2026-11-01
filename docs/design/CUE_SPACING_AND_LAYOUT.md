# Cue — Spacing and Layout

Current values follow [`v10-bordo-herbaryum/styles.css`](v10-bordo-herbaryum/styles.css). The layout uses open editorial areas and compact controls rather than a generic rounded-card grid.

## Responsive frame

| Region | Desktop | Tablet / mobile |
|---|---|---|
| Public hero | Two-column statement and specimen plate | Stacked statement and plate |
| Product header | Full-width wordmark, two destinations, account | Compressed horizontal navigation |
| Main content | Maximum 1440 px, generous side margin | Single column with 17–22 px margins |
| Library | Three columns | Two columns, then one on narrow phones |
| Keyframes | Equal 8:5 start/end work surfaces | Stacked surfaces connected vertically |
| Motion plan | Instruction and cue sheet side by side | Instruction above cue sheet |
| Status/result | Main stage with metadata rail | Stage above metadata |

## Layout rules

- Four steps appear on keyframes, motion plan, generation, and result. Past steps are marked complete; future steps are not clickable.
- Product navigation remains at the top. No sidebar is added for two main destinations.
- A single main action appears per view; secondary navigation remains outlined or text-only.
- Drawing surfaces use an 8:5 aspect ratio and clear start/end labels.
- Cards and panels use square corners and hairline borders. Shadows appear only behind an illustration plate or transient overlay.
- On narrow screens, upload actions and page controls stack in reading order.
