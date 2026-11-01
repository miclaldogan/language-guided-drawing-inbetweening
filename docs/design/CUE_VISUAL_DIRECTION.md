# Cue — Visual Direction: Bordo Herbaryum

**Status:** Current full-site mockup for review. Source of truth: `docs/design/v10-bordo-herbaryum/`. Product requirements and workflow are sourced from the proposal traceability, screen plan, database proposal, and reviewed activity/sequence diagrams.

## Identity

Cue is an open drawing atelier for short in-between animations. Its visual world joins botanical field notes and printmaking with a precise digital worktable. The interface feels authored and artistic; the work stays easy to understand.

## Art direction

- **Palette:** burgundy `#4B2834`, warm paper `#F4EBDD`, sage `#91AA8A`, copper `#D39A62`, charcoal `#2B2727`.
- **Public landing:** asymmetrical editorial composition, oversized serif statement, botanical motion plate, field-note labels, and a distinct studio entry point.
- **Product shell:** slim top navigation and four-step progress line. There is no sidebar or dashboard-stat grid.
- **Drawings:** original engraved botanical marks on paper mats with registration ticks and calm, fine rules.
- **Typography:** system serif display, neutral sans-serif controls, monospace annotations. No external font loading.
- **Depth:** paper and ink planes, hairline rules, offset print plates. No glass, rounded utility cards, generic gradients, or soft toy-like illustration.
- **Motion:** only when it explains a state or response. Reduced-motion preference is respected; the user's drawings do not animate decoratively while being edited.

## Product screens

1. **Authentication:** log in / create account.
2. **Library:** owned animation gallery with done, running, and failed examples.
3. **Keyframes:** start and end drawings, each fitted to an 8:5 mat.
4. **Motion plan:** optional English instruction, ordered cue preview, approval, and drawings-only path.
5. **Generation status:** queued, running, done, failed, or cancelled. No invented progress percentage or ETA.
6. **Result:** discrete 16-frame player, source endpoints, and reproducibility details.

The Wave-Line lab is a separate visual study, outside the six-screen product flow.

## Guardrails from requirements and diagrams

- Job states use the five values in the database proposal: `queued`, `running`, `done`, `failed`, `cancelled`.
- Empty instruction skips plan parsing; a non-empty instruction needs a current approved plan.
- Plan preview is not persisted before job submission.
- The first and last of at most 16 frames are the submitted drawings; timing in the cue sheet shows order only.
- Media stays represented as authorized assets; the UI never exposes storage keys.
- Authentication, upload, model inference, job processing, and export are illustrative only in this mockup.
