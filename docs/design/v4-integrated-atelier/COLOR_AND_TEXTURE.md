# Colour and Texture

Palette unchanged from V3: purple `#431452`, gold `#FFB509`, paper `#F5EBD8`, light paper `#FFFAF0`, ink `#241629`, blue `#23437C`, orange `#ED782A` (fill only), plus text-safe orange `#B4440F` and graphic orange `#C4531A`, input line `#85748A`, worktable `#F0E4CC`.

## Distribution (measured on the renders)
| Screen | Gold | Paper | Purple | Other |
|---|---|---|---|---|
| S1 Auth | 31% | 41% | 16% | 13% |
| S2 | 2% | 75% | 8% | 15% |
| S3 | 3% | 84% | 7% | 6% |
| S4 | 2% | 83% | 7% | 7% |
| S5 | 2% | 76% | 7% | 15% |
| S6 | 4% | 78% | 8% | 11% |
Paper dominates, purple anchors, and S1 carries the large gold brand area. Gold on operational screens is 2–4% and sits at the edges. Decision V4-D1 covers whether to add more.

## Materials
- **Paper:** 5% fractal grain plus 4% horizontal fibre over the page; flat fills inside inputs, cards and artwork so texture never sits under text or drawings.
- **Canvas weave:** not adopted. It was not rendered in this round, so no claim is made about it; paper grain and fibre are the only material layers.
- **Registration marks:** sparse, in the 72 px margins only: three per side at y 116, 470, 836, circle r 6 and cross, 1 px, 30% purple, joined by 12% guide lines. Hidden under the brush corners. Tile versions in `assets/` are used on the S1 gold panel.
- **Brush:** one filter (turbulence 0.016, 2 octaves, displacement 8) on gold shapes, with faint bristle streaks and a paper grain over the paint. Allowed: S1 brand panel and its purple block, page corners, nav stripe, empty states. Forbidden: cards, buttons, inputs, player controls, plan data, error messages.
- **Elevation:** only cards (small) and overlays (large). No page-level shadow.

Assets: `assets/brush-corner-top-left.svg`, `brush-corner-bottom-right.svg`, `pattern-registration-on-gold.svg`, `pattern-registration-on-paper.svg`, `background-patterns.css`.
