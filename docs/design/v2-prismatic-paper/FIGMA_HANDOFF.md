# Figma Handoff (V2)

## Connection status
The Figma connector is **not authenticated** in this session. The only Figma tools exposed (`mcp__claude_ai_Figma__authenticate`, `mcp__plugin_product-management_figma__authenticate`) start sign-in; no tools for creating files, frames or variables are available. OAuth needs the user in a browser and was not started. **No Figma file was created.** After the user authenticates, check what tools appear before promising a draft. No other connector or plugin was installed.

## What to build, in order
1. **Variables.** Collection `Cue/primitive` with every colour in `tokens.json` (single mode); `Cue/semantic` aliasing primitives (one mode: Prismatic Paper); `Cue/space`, `Cue/radius`. Names equal token names.
2. **Text styles.** `wordmark`, `display-hero`, `screen-title`, `section-heading`, `card-title`, `body`, `body-secondary`, `form-label`, `metadata`, `button-label`, `status-text`, `numeral`. Fraunces: set Soft 50, Wonk 0 and optical size in Figma's variable-font axes where available; otherwise use "Fraunces 72pt Soft" style names. Manrope from Google Fonts.
3. **Effects.** `shadow/print` = offset 0,3, no blur, ink 16%. `shadow/dialog` = 0,10,24 at 28%.
4. **Texture.** A 256×256 tile of grain as an image fill at 9–12% on shell and panels, in a layer named `texture/grain`; never on inputs, drawings or video.
5. **Components** (page `02 Components`): Button (Type: primary/secondary/danger × Size × State), Input, TextArea, TopBar, Stepper, Tabs, GalleryCard (Status), StatusChip (5), FrameStrip, FilmStrip, UploadZone (Empty/DragOver/Filled/Error), CueBlock, CueSheet, PlayerControls, Dialog, Alert, Toast, Tooltip, EmptyState. All Auto Layout; properties `State`, `Size`, `Type`, booleans `Loading`, `Disabled`.
6. **Screens** (page `03 Desktop Screens`): frames 1440×900 named `S1/Authentication`, `S2/Dashboard`, `S3/Keyframes`, `S4/MotionPlan`, `S5/Status`, `S6/Result`, with state variants beside each. Use the PNG/SVG previews as visual references, not as imported art.
7. **Responsive** (page `04`): 1280, 768, 390 for S2, S3, S4, S6.
8. **Prototype** (page `05`): Login → Dashboard → Upload → Motion Plan → Generation Status → Result → Dashboard. Triggers: On click, Navigate to; transition Smart animate 200 ms, ease out. S5 states (Queued, Running, Done) swap by On click variant, not by simulated timers or progress.

## File structure
`00 Foundations`, `01 Colors & Typography`, `02 Components`, `03 Desktop Screens`, `04 Responsive Adaptations`, `05 Prototype Flows`, `06 Design Handoff` (token table, spacing redlines for S4, component-to-React map from COMPONENT_SYSTEM.md).

## Layer hierarchy and constraints
`Frame S4/MotionPlan` → `TopBar`, `Stepper`, `Header` (title, subtitle), `Content` (Auto Layout horizontal, gap 24: `Panel/Instruction`, `Panel/MotionPlan`), `ActionRow` (space-between). Panels hug height and fill width; media frames fix aspect 8:5; top bar fixed height 76 and stretches left–right.

## Exportable references
`style-tiles/*.png|svg` and `previews/*.png|svg` are rendered with the fonts and tokens above; they can be placed in Figma as reference layers.
