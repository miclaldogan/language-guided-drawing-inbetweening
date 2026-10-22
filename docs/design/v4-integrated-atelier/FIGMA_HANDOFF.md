# Figma Handoff (V4)

**Status:** the Figma connector is still not authenticated (only `authenticate` tools are exposed; no tools to create files, frames or variables). Nothing was created in Figma. After sign-in, re-check available tools first.

## Build steps
1. Variables from `tokens.json`: `Cue/primitive`, `Cue/semantic` (alias), `Cue/space`, `Cue/radius`, `Cue/border`, `Cue/surface` (level 1–3). Names equal token names.
2. Text styles: wordmark, auth-hero, page-title (Fraunces 34), eyebrow, section-title, group-label, card-title, body, body-secondary, form-label, metadata, button-label, status-text, plan-index, numeral.
3. Effects: `elevation/card`, `elevation/overlay`; blur filter for the brush is not native: import `assets/brush-corner-*.svg` as vector layers.
4. Assets: brush corners, nav stripe (rectangle with the same displacement baked into an SVG), registration marks as a single component `Mark` placed in margin columns.
5. Components: Nav, PageHeader (eyebrow, title, subtitle, stepper slot), Button, Input, TextArea, UploadZone, IdentityTag, GalleryCard (+ kebab), StatusChip, FrameStrip, FilmStrip, Worktable, CueRow, PlayerControls, Dialog, Alert, Toast, Tooltip. Auto Layout throughout; variant properties `State`, `Size`, `Type`.
6. Page templates: `Template/Auth`, `Template/Library`, `Template/Flow` (nav; page margin 72; header; content; footer). Screens S1–S6 are instances.
7. Responsive frames at 1280, 768 and 390 (see LAYOUT_SYSTEM.md). Hide marks and brush corners below 640.
8. Prototype: Login → Dashboard → Upload → Motion Plan → Generation Status → Result → Dashboard; Navigate-to on primary buttons; Smart animate 200 ms; S5 states swap by variant, no simulated progress.

## CSS variables and React mapping
`tokens.json` → `tokens.css` (`--bg-page`, `--bg-card`, `--bg-worktable`, `--bg-dialog`, `--bg-scrim`, `--action-primary`, `--border-card`, `--elevation-card`, `--elevation-overlay`, …). Tailwind `theme.extend.colors` maps `page`, `card`, `ink`, `action`, `gold`, `purple` to variables only.
| Design | React |
|---|---|
| Template/Flow | `layouts/FlowLayout` (Nav, PageHeader, `<main>`, FooterBar) |
| Template/Library | `layouts/LibraryLayout` |
| Nav | `components/Nav` |
| PageHeader | `components/PageHeader` with `stepper` prop |
| GalleryCard | `components/GalleryCard` (`status` prop; menu button with `aria-haspopup`) |
| Worktable | `components/Worktable` |
| CueRow | `components/cue/CueRow`, `CuePlan` (`<ol>`) |
| FilmStrip | `components/FilmStrip` |
| Dialog | headless dialog with focus trap |
| MarginMarks, BrushCorner | decorative `aria-hidden` components rendered once in the layout |
No production code was written.
