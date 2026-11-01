# Cue — Figma Structure

> Historical handoff from the earlier visual concept. The current mockup and palette source of truth are [v10 Bordo Herbaryum](v10-bordo-herbaryum/index.html).

## Connection status (verified this session)
- Installed plugin `figma@claude-plugins-official` and an `mcp__claude_ai_Figma` server are registered.
- In this session the Figma server exposed **only** `authenticate` / `complete_authentication`. No design-creation, variable or file tools were available, and OAuth was not completed (it needs the user in a browser).
- Consequence: **no Figma file was created or modified.** Everything here is a build specification. After the user authenticates, re-check which tools appear before promising any creation.

## File: "Cue — Design System & Screens"
| Page | Contents |
|---|---|
| 00 Foundations | Cover, principles, grid and spacing, elevation, iconography rules, motion tokens as reference |
| 01 Colors & Typography | Variable collections: `primitive` (palette), `semantic` (light-less, one Dark mode), `type` (text styles Sora/Manrope per scale), `space`, `radius`. Mirrors `CUE_DESIGN_TOKENS.json` names |
| 02 Components | Button (type × size × state), Input, TextArea, NavItem, TopBar, Tabs, Stepper, JobCard, StatusChip, ProgressBar, FrameStrip, UploadZone, Dialog, Alert, Toast, Tooltip, CueBlock, CueSheet, PlayerControls, EmptyState |
| 03 Desktop Screens | 1440×900 frames S1–S6, each with its state variants beside it |
| 04 Responsive Adaptations | 1280, 768 and 390 versions of S2, S3, S4, S6 (S1 and S5 follow the same patterns) |
| 05 Prototype Flows | Main flow and alternate paths, from `CUE_USER_FLOWS.md` |
| 06 Design Handoff | Token table, spacing redlines for S4, component-to-React map, accessibility notes |

## Conventions
- Variables for every color, space, radius; no raw hex in components. Variable names equal token names (`bg-surface`, `action-primary`).
- Text styles named `product-heading`, `screen-title`, … as in typography doc.
- Components: Auto Layout everywhere; variant properties `State`, `Size`, `Type`; boolean `Loading`, `Disabled`. Variants created only where a state exists in the spec.
- Layer names: `S4/Instruction/Textarea`, never "Frame 123".
- Constraints: left+right for stretching panels; media frames lock 8:5 aspect.
- Frames per screen: Default + each state in the UX plan.

## Prototype
Login → Dashboard → Upload → Motion Plan → Generation Status → Result → Dashboard (Back to Library). Interactions: On click, Navigate to. Use Smart animate with the page-transition timing (200 ms, standard easing). Do not simulate uploads, parsing, or progress beyond swapping state variants.

## Order of work
1. Foundations, variables, text styles. 2. Components with states. 3. Review gate: direction and traceability approved. 4. Desktop screens. 5. Responsive. 6. Prototype and handoff. The six high-fidelity screens are deliberately not drawn until step 3 passes.
