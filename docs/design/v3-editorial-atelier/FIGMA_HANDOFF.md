# Figma Handoff (V3)

## Connection status
Not authenticated. Only `authenticate` tools for Figma are exposed in this session (`mcp__claude_ai_Figma__authenticate` and the product-management Figma connector); there are no tools to create files, frames or variables. OAuth needs the user in a browser and was not started. **No Figma file was created.** After authentication, re-check which tools appear before promising a draft. No plugin was installed.

## Build order
1. **Variables.** `Cue/primitive` (colours from `tokens.json`), `Cue/semantic` (aliases, one mode "Editorial Atelier"), `Cue/space`, `Cue/radius`, `Cue/border`. Names equal token names; no raw hex in components.
2. **Text styles.** wordmark, auth-hero, page-title, section-title, group-label, card-title, body, body-secondary, form-label, metadata, button-label, status-text, plan-index, numeral. Fraunces with Soft 50, Wonk 0; Manrope.
3. **Effects.** `elevation/1` 0,2,6 at 14%; `elevation/2` 0,14,36 at 20%; `elevation/3`.
4. **Pattern assets.** Import `assets/pattern-registration-on-gold.svg` and `…-on-paper.svg` as 96×96 tiles; fill a rectangle with Tile (scale 1) on the ground layers only; layer name `pattern/registration`.
5. **Texture.** Grain tile at 5–7% on nav, ground and sheet; layer name `texture/grain`; never on inputs, artwork or the viewer.
6. **Components** (page `02 Components`): Nav (Auth/Library), Sheet, Button (primary/secondary/danger/ghost/disabled × size), Input, TextArea, UploadZone (Empty, DragOver, Filled, Error), IdentityTag (Start/End), GalleryItem (Done, Processing, Queued, Failed), StatusChip, FrameStrip, FilmStrip, CueRow, CuePlan (rail), PlayerControls, Stepper, Dialog, Alert, Toast, Tooltip. Auto Layout throughout; properties `State`, `Size`, `Type`; booleans `Loading`, `Disabled`.
7. **Screens** (page `03`): 1440×900 frames `S1/Authentication` … `S6/Result`. Use `previews/*.svg` as references. Layer structure: `Frame` → `Nav`, `Ground` (fill + pattern + texture), `Sheet` (Auto Layout vertical: `Header` row, `Content` row, `Footer` row).
8. **Responsive** (page `04`): 1280, 768, 390. Sheet fills width with 16–32 px margins; two-column content becomes one; film strip rows 16→8→4; gallery 4→3→2→1.
9. **Prototype** (page `05`): Login → Dashboard → Upload → Motion Plan → Generation Status → Result → Dashboard. Navigate-to on the primary buttons; Smart animate 200 ms ease-out; swap S5 state variants by click, no simulated progress.
10. **Handoff** (page `06`): token table, redlines for S4, component-to-React map (unchanged from V2, `Nav`, `Sheet`, `CueRow`, `FilmStrip` added).

## Constraints
Nav fixed 64 px, left+right. Sheet: width fill, height hug, min 40 px margin on desktop. Media frames lock 8:5. Gallery uses a wrapping Auto Layout with 24 px gaps.

## CSS variable spec
Generate `tokens.css` from `tokens.json`: `--bg-nav`, `--bg-ground-gold`, `--bg-sheet`, `--action-primary`, `--border-input`, … plus `--pattern-gold`/`--pattern-paper` from `assets/background-patterns.css`. Tailwind: `theme.extend.colors` maps `nav`, `ground`, `sheet`, `raised`, `ink`, `action` to the semantic variables only.
