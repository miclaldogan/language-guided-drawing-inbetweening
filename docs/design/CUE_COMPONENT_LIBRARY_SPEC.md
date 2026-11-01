# Cue — Component Library Spec

The active component treatment is implemented in [`v10-bordo-herbaryum/`](v10-bordo-herbaryum/). Components use the semantic palette in `CUE_DESIGN_TOKENS.json`.

| Component | Current treatment | Behavior |
|---|---|---|
| Primary button | Copper fill, charcoal label, squared edge | One main action per screen; disabled state remains visible |
| Secondary button | Transparent paper fill, burgundy outline | Back, change drawings, preview plan |
| Top navigation | Burgundy bar, wordmark left, two main destinations, account | Active destination marked with a fine copper rule |
| Workflow stepper | Four numbered steps and thin rules | Current step is burgundy; finished steps show a check |
| Job card | 8:5 illustrated plate, status word, short title, date | Click opens the matching status or result; delete asks for confirmation |
| Upload slot | 8:5 paper surface, start/end label, visible file input | Empty, selected, replaced, removed, or file-type error |
| Motion cue sheet | Ordered cue rows and event blocks | Caption says order only; approval clears when instruction changes |
| Status chip | Word plus shape | Supports queued, running, done, failed, and cancelled |
| Frame strip | Sixteen discrete ticks, copper endpoints | Activity-only during generation; functional stepping in result view |
| Alert / toast | Text plus icon or border marker | Carries the reason and next action; color is never the only signal |

## Interaction rules

- Minimum interactive target: 40 px where layout permits.
- All inputs retain visible labels and keyboard focus.
- No hover lift or automatic video playback on gallery cards.
- Delete and cancel require confirmation.
- Focus uses a visible 2 px outline.
- Reduced-motion preference turns off repeated decorative movement.
