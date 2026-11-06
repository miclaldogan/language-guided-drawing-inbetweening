# Cue v11 — design direction

Built in three passes, each led by one skill set.

## 1. Direction (taste-skill)

**Public page: "The product performs"** (seed 536979242, sector ai-product). The page shows working pieces of the product instead of describing features. The hero is a live cue sheet, and every further capability is a cropped, true-size piece of the interface.

> **Idea:** On this page, the animator's cue sheet (where the name *Cue* comes from) becomes a working fragment that turns a sentence into ordered cues and redraws sixteen frames.

**Live thing:** type a sentence and see the plan and the frames change. It works on a phone and needs no network.

**Studio: "Framed sheet"** (seed 1329022550, kind builder), with the page's palette and typeface kept.
- **Face:** the frame is tinted from the brand plum, and the brand pink is the one data hue.
- **Signature element:** the cue sheet lanes.

| Role | Page | Studio |
|---|---|---|
| Ground | `#0d060b` plum-black | `#f8f5f7` plum-tinted frame, white sheet |
| Field | `#470c35` plum, `#ffffff` white | — |
| Accent | `#ff488b` pink (primary action) | `#d8296c` pink on data only (4.8:1 on white) |
| Type | Switzer 400/500/600, one face | Switzer; system mono only for job IDs |

House rules held throughout: no eyebrows, no index numbers, no gradients, no glass, no shadows at rest (only menus, dialogs and toasts float), and no monospace outside IDs.

## 2. Motion (Emil Kowalski skills)

- **Signature:** while untouched, the hero stage crossfades slowly between the two drawings (1.6 s, holding about 5 s), like flipping a sheet on a light table. It pauses when the tab is hidden.
- **Cue blocks** arrive left to right in reading order (60 ms stagger, 260 ms ease-out), once per new plan. The animation teaches the order.
- **Frame strip swap:** a 120 ms blur bridges the old strip and the new one.
- **Press feedback:** `scale(0.97)` on every pressable. Hover effects are gated to `(hover: hover) and (pointer: fine)`.
- **Frame stepping** with the keyboard or buttons is instant. A keyboard action never animates.
- **Playback** runs at 12 fps on twos, with a short hold on the last drawing.
- **Easing:** strong custom curves (`0.23,1,0.32,1` and `0.77,0,0.175,1`). Nothing uses ease-in, and UI transitions stay under 300 ms.
- **Generation activity** is a 2.4 s shimmer across ticks 2–15. It shows activity, not progress, and there is no percentage or ETA.
- **Reduced motion:** no travel and no shimmer, the film doesn't play, and fades only.

## 3. Final touches (impeccable polish)

- Cue blocks lost their 3 px coloured left edge. They now carry a pale pink fill, and the numbered disc keeps the hue.
- Hero content is visible from the first paint (no hidden-then-revealed headline).
- Section entrances vary: text rises, and archival pictures open from the bottom edge with `clip-path`.
- The zoetrope strip moves with the reader's scroll instead of running as a marquee.
- Loading skeletons pulse in place instead of sweeping.
- Browser surfaces are themed: selection, caret, scrollbars, underline offset and focus rings.
- The display tracking floor is held at -0.04em, and a favicon was added.

## Checks run

- taste-skill `inspect.mjs` (page): **0 FAIL**. Five warnings remain, each a deliberate choice:
  - The showcase carousel scrolls sideways by design.
  - The four dataset figures are equal peer tiles.
  - The font-size count includes the product's true-size interface fragments.
- `inspect.mjs --app` (library): the two failures (a heavy shadow on the mockup bar, text near the edge on the phone) were fixed.
- impeccable `detect`: no anti-patterns. The only findings are "cramped padding" on deliberately edge-to-edge pictures and drawing stages.
- No console errors on the page or on any studio screen.
