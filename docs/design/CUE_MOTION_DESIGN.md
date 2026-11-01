# Cue — Motion Design

> Historical motion specification from the earlier concept. Color references such as “purple” are superseded by the semantic roles in [the current color system](CUE_COLOR_SYSTEM.md).

Principle: motion answers an action or shows a state change. Nothing loops near the user's drawing while they are working. Tokens: `duration.instant 80 / fast 120 / base 200 / slow 320 ms`; `easing.standard (0.2,0,0,1)`, `enter (0,0,0,1)`, `exit (0.4,0,1,1)`.

| Where | Motion | Duration / easing | Purpose |
|---|---|---|---|
| Buttons | background changes to hover/active tone | 120 ms standard | feedback |
| Primary button loading | spinner swaps with icon; width fixed | 120 ms | no layout shift |
| Page transitions | content cross-fades; stage shifts 8 px | 200 ms enter | keeps orientation between steps |
| S1 brand panel | frame strip ticks settle in once on load (stagger 20 ms, total ≈ 500 ms), then still | 320 ms enter | the only decorative moment, plays once |
| Upload slot | drag-over border to purple; on success the preview fades in and the slot border settles | 120 / 200 ms | confirm it worked |
| Upload error | message appears, no shake | 120 ms | clarity |
| Plan appears | cue blocks reveal left to right in order, 60 ms stagger (max ≈ 400 ms) | 200 ms enter | teaches reading order; plays once per parse |
| Plan out of date | blocks fade to muted | 200 ms | state change |
| Generation running | inner ticks (2–15) carry a slow left-to-right shimmer, 2.4 s cycle, low contrast | linear, loop | shows activity, not progress |
| Generation done | ticks fill once; chip changes | 320 ms | completion |
| Gallery | card border brightens; poster stays still | 120 ms | no autoplay of videos |
| Dialog / toast | fade + 8 px rise / fall on exit | 200 enter / 120 exit | spatial origin |
| Player | scrubber tick moves with the frame; frame step is instant | none | precision |

## Reduced motion
`prefers-reduced-motion: reduce` → remove translations and stagger; transitions become 0–80 ms opacity; S1 strip appears static; shimmer replaced with a static running label and a blinking-free "Running, 2 min 10 s" text; clip autoplay is already off.

## Do not
No parallax, scroll-triggered effects, hover lift on cards, looping decoration, animated gradients, or page-load fades on every section.
