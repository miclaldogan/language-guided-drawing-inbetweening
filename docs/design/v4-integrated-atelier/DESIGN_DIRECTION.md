# Cue V4 — Integrated Atelier

V1–V3 are untouched. V4 removes the one structural habit that made V3 look like a template: a large rounded panel laid over the page background with all content inside. In V4 the page itself is the paper canvas.

## Structure (every authenticated screen)
Purple nav → paper page canvas → eyebrow row (+ stepper on S3–S6) → page title and subtitle → hairline divider → content directly on the page → hairline footer with Back and the one primary action. No enclosing panel, no outer drop shadow, no outer radius.

## What came from where
| Source | Kept |
|---|---|
| Experiment 2 (primary) | purple navigation, warm paper page, restrained decoration, thin dividers, clear hierarchy, unboxed gallery rhythm |
| Experiment 3 (selected details) | gold as a brand colour, registration marks, print-inspired details, gentle paper texture |
| The reference image you attached (`~/Downloads/Cue Animation Library Dashboard.png`) | brushed gold corners, a gold stripe under the nav, margin registration marks with guide lines, eyebrow-plus-rule above the title, kebab menu on cards. Not copied: the spark lines beside the button (read as a sticker), the oversized 56 px title (reduced to 34), the caps eyebrow (sentence case) |

## Dashboard experiments (rendered at 1440×900, `experiments/`)
| | A Integrated paper workspace | B Integrated paper + golden frame |
|---|---|---|
| Frame | paper only, margin marks | same plus brushed gold corners and a gold stripe under the nav |
| Gold on screen | ≈0% | ≈2% (S1 31%) |
| Verdict | Clean and professional, but the identity falls back to "purple bar on cream"; gold nearly vanishes, which breaks the rule that yellow must stay recognisable | **Selected.** Same layout; the gold corners and stripe tie the page to the brand without adding a container. |

Neither version has an enclosing panel. B is the one applied to all six screens.

## Material system
Level 1 page canvas: paper with 5% grain and 4% fibre. Level 2 functional surfaces: cards, inputs, upload zones, the worktable band, the viewer; tone and a 10% hairline, small shadow only on cards. Level 3 overlays: dialogs and menus, with scrim and larger shadow. See `SURFACE_HIERARCHY.md`.

## Principles
1. The page is the working surface; structure comes from alignment, rules and type.
2. Boxes only where a thing needs identifying (a video, an input, a drop zone).
3. Artwork and video stay the most saturated content.
4. Gold is a brand accent placed at the edges (corners, stripe, S1 panel), never behind content.
5. Brush is rare, and never touches functional components.
6. Purple: nav and the one primary action per screen.

## Honest risks
- Gold covers only 2–4% of operational screens (31% on S1). It is recognisable at the edges, but if you want more, the next lever is the title highlight I tried and removed: it looked like a highlighter pen.
- The mock thumbnails are procedural studies, not real drawings.
- Cards on paper with kebab menus, hairlines and small shadows are common; the differences are the paper, the brush corners, the registration marks and the artwork.
