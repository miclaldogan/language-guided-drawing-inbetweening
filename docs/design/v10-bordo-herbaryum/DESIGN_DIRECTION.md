# Cue — Bordo Herbaryum: design direction

## Intent

Make Cue feel like a contemporary drawing atelier informed by botanical field books and printmaking. The visual language combines sober editorial typography, specimen-paper details, and restrained tool controls. It should feel authored and artistic without turning the workflow into a decorative toy.

## Palette

| Share | Role | Color |
|---:|---|---|
| 60% | Burgundy field | `#4B2834` |
| 25% | Warm drawing paper | `#F4EBDD` |
| 15% | Sage and copper accents | `#91AA8A`, `#D39A62` |
| Text | Charcoal ink on paper | `#2B2727` |

Sage marks selection and approved interpretation. Copper marks primary actions and small registration notes. The accent colors are kept off small text unless contrast permits it.

## Composition and materials

- The public opening uses an asymmetric editorial spread: a large typographic statement against burgundy, paired with an original botanical motion plate.
- Product views use a narrow top navigation, a visible four-step sequence, and open paper surfaces. No sidebar, generic metric cards, glass panels, heavy rounded containers, or repeated stat tiles.
- Drawings sit on pale paper mats with fine plate rules, registration ticks, small specimen labels, and restrained engraved contours.
- Headings use Fraunces, the interface uses Manrope (both self-hosted in `fonts/`, no external requests). Monospace appears only on IDs, file names and counters. Text is never smaller than 12 px.
- The selected palette colors are retained; the component composition and illustration are redesigned.

## Product flow and boundaries

The six product screens follow `docs/design/CUE_SCREEN_BY_SCREEN_UX_PLAN.md`, `CUE_USER_FLOWS.md`, and the flow/state diagrams in `docs/architecture/database-and-diagrams-v2/diagrams/`. The interface uses the database's five job states and metadata vocabulary. Empty instruction means a drawings-only run; a non-empty instruction needs a current, approved plan. Plan preview is not stored until job submission.

The prototype uses illustrative sample data. It never claims an actual upload, authenticated account, model call, queued job, generated video, or download. The Wave-Line study is a separate visual experiment and does not change the workflow output.
