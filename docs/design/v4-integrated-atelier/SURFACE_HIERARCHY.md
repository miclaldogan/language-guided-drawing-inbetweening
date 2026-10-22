# Surface Hierarchy

| Level | Purpose | Surfaces | Treatment |
|---|---|---|---|
| 1 Page canvas | the working surface | page background | `bg-page` `#F5EBD8`, grain 5%, fibre 4%, margin marks, brush corners and nav stripe in the margins only |
| 2 Functional surfaces | where something must be identified or manipulated | gallery cards, inputs, upload zone, worktable band (S3), video viewer, film strip, status chips, plan rail | tone step (`bg-card` `#FFFAF0`, `bg-worktable` `#F0E4CC`, `bg-viewer` `#17101C`), 1 px 10% hairline, card shadow `0 2px 6px 10%` |
| 3 Temporary overlays | interrupts | delete confirmation dialog, menus, popovers | `bg-dialog` `#FFFAF0`, radius 14, shadow `0 22px 56px 30%`, scrim 38% ink |

## Rules
- Permanent page content never uses level 3 styling.
- Nothing wraps the whole page or a whole column. Section grouping uses hairlines (16%), vertical dividers (12%) and whitespace.
- No card inside a card. The S3 worktable is a full-bleed tonal band with hairline edges, not a rounded container.
- Radii: 4 (thumbnails), 8 (cards, inputs, buttons), 14 (dialogs only).
- Borders: none (grouping by space), hairline (cards, dividers), control `#85748A` (inputs, upload), 2 px purple (selected, focus).
- Render proof: `previews/overlay-delete-dialog.png` shows level 3 over the library.
