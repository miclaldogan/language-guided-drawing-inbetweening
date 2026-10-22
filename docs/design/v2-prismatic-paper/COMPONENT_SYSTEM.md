# Component System (V2)

Tokens: `tokens.json`. Same component list and states as V1 (`CUE_COMPONENT_LIBRARY_SPEC.md`); this table gives the V2 visual spec. Common: focus = 2 px ink ring + 2 px cream gap; hover = 6% ink overlay; pressed = 12% overlay; disabled = cream-300 fill, hair border, ink-600 text; targets ≥ 40 px; radius 8 controls, 12 panels, pill chips.

| Component | Spec | Notes |
|---|---|---|
| Button primary | 50 high (generate, download), 44 default; fill `action-primary`, cream text, 1.5 px ink border, 3 px hard shadow; hover `action-primary-hover`; pressed `-active`, shadow shrinks to 1 px; loading spinner, width fixed | one per screen |
| Button secondary | cream-100 fill, ink outline, ink text | Back, Replace, Preview plan |
| Button danger | cream-100 fill, brick outline and text | Cancel generation, Delete (after confirm dialog) |
| Navigation | wordmark, text links; current page ink 800 weight with 3 px purple underline; account chip with email | on gold, ink text 8.8:1 |
| Stepper | 28 px circles: done = ink with check; current = purple with number; upcoming = ink-700 outline; connecting ink lines | not clickable forward |
| Input / text area | 46 high; cream-100 fill; 1.5 px `border-input` (ink-600, 5.7:1); focus 2.5 px ink ring; error: brick border, triangle icon, message below; label always above | no texture |
| Upload zone | 8:5, dashed `upload-border`, cream-100; drag-over: purple border and purple-tint fill; filled: drawing on paper-white with ink outline | native file input reachable |
| Gallery card | cream-100, 1.5 px ink border, hard shadow, 8 px inner padding; thumbnail 8:5 on the user's own paper; title 15/800; metadata; chip bottom right; focus ring around whole card | whole card is one link |
| Video thumbnail | poster only, play glyph in a cream disc; in-progress variant dimmed with frame strip; failed variant red-tint | no autoplay |
| Status chip | 28 high pill, icon + word: Done (green), Running (blue, dashed ring), Queued (cream-300, clock), Failed (brick, triangle), Cancelled (cream-300, triangle) | five FR-07 states |
| Frame strip | 16 ticks; ends orange-600 and taller; others ink at 85% | decorative on S2/S5, slider on S6 |
| Film strip (S5) | viewer-900 strip, gold-300 sprockets, 96×62 cells, hatched pending cells, orange outline on frames 1 and 16, numerals 11 px cream | activity is not progress |
| Cue block / CueSheet | see SIX_SCREEN_DESIGN_SPEC | ordered list in the DOM |
| Dialog | cream-100, ink border, elevation 3, 24 px padding; destructive confirm is brick, never purple | focus trap, Esc |
| Tooltip | ink-900 fill, cream-100 text 13 px, 8 px radius | icon buttons only |
| Toast | cream-100, ink border, icon + text, left bar in state colour | never sole error carrier |
| Alert | state-tint fill, 1.5 px state border, 6 px left bar, icon, bold title, secondary line | `role=alert` for async |
| Player controls | purple play disc, cream icon buttons, strip scrubber with purple current-frame outline | Space, ←/→ |
| Panel | cream-200, ink 1.5 px border, 3 px hard shadow, grain 9% | no nesting of panels |

Not built: tertiary buttons, glass, gradients, glow, sidebar.

## React/Tailwind reuse
Export `tokens.json` to CSS variables (`--bg-shell`, `--action-primary`, …) and map them in `tailwind.config` under `theme.extend.colors` using names such as `shell`, `surface`, `ink`, `action`. Components read only semantic tokens; no hex in JSX. Primitive tokens are not exposed to Tailwind classes.
