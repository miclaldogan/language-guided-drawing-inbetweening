# Cue — Open Studio

## Design intent

The site should read as an artist's drawing and motion studio, not a neutral utility dashboard. The opening is a visual statement: two endpoint drawings create a third thing—the movement between them. The application's workflow then carries that artistic identity into clear, practical screens.

## Reference translation

Hacktoberfest's current public site uses a dark forest ground, a warmer-than-white paper color, condensed high-impact display type, concise mono labels, and accent colors placed in small decisive areas. Its own brand guide describes forest as the ground and the accents as limited emphasis; its homepage uses a large event scale, direct hierarchy, and strong illustrated blocks. Cue adapts these ideas to drawings and motion, without using Hacktoberfest logos or assets.

| Share | Role | Color |
|---:|---|---|
| 60% | Forest-charcoal ground | `#2E4742` / `#3D5F58` |
| 25% | Warm paper and drawing surfaces | `#F2F2EB` |
| 15% | Action and image accents | Orange `#E53927`, sky `#8BB2DE`, ochre `#F5B726`, coral `#E97B77` |

The orange/blue pairing reinforces action versus motion cues. Ochre and coral live mostly in illustration, small marks, and selected controls. Text uses charcoal-green rather than pure black.

## Art direction

- **Illustration:** a hand-rendered profile study moves through three positions, with engraved contours, registration marks, a geometric orange disc, and a blue color plate.
- **Traditional register:** plate borders, print texture, curved contour drawing, small figure numbers, and a paper surface.
- **Future register:** shader movement, frame indexing, waveform line fields, precise mono metadata, and cursor response in the lab.
- **Typography:** condensed display face for the public landing statement, Inter for product controls, Martian Mono for technical labels. System fallbacks remain defined.
- **Depth:** simple paper/ink planes and offset color plates; no generic glass cards, soft toy shapes, or decorative gradients.
- **Motion:** isolated and slow in the lab; application transitions stay subordinate to the drawings and user's task.

## Site structure

1. **Public landing page:** oversized visual hero, process story, visual-study section, studio CTA.
2. **Sign-in:** branded cover panel and concise account form.
3. **Library:** recent animation archive and real job states.
4. **Keyframes:** clear start/end drawing plates and A→B order.
5. **Motion plan:** English instruction beside ordered cues and explicit approval.
6. **Generation status:** activity-only sixteen-frame strip, with no invented percent or ETA.
7. **Result:** large video stage, frame stepping, reproducibility details, and export affordances.
8. **Wave-Line lab:** independent, interactive GLSL study.

## Boundaries

- The custom illustrated hero is original SVG artwork, not a copied Hacktoberfest asset.
- The Wave-Line canvas samples its supplied study image; it does not stylize user inputs or outputs.
- HTML owns screen meaning and controls; WebGL remains decorative and replaceable.
- The active prompt remains English according to the existing project requirement; surrounding interface copy is Turkish.
- The website is a review mockup, not a connected product.
