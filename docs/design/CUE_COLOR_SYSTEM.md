# Cue — Color System: Bordo Herbaryum

Source of truth: [`v10-bordo-herbaryum/tokens.json`](v10-bordo-herbaryum/tokens.json). The five chosen palette colors are retained; semantic roles keep their use consistent across the public site and studio screens.

## Palette and roles

| Color | Hex | Role |
|---|---|---|
| Burgundy | `#4B2834` | Brand field, public hero, navigation, selected steps |
| Warm paper | `#F4EBDD` | Main reading surface and drawing mat |
| Sage | `#91AA8A` | Selected/approved states and secondary emphasis |
| Copper | `#D39A62` | Primary actions, frame endpoints, registration marks |
| Charcoal ink | `#2B2727` | Text on paper and controls |

Supporting surface neutrals (`paper-light`, `muted`, `rule`) are low-chroma tints for text hierarchy and hairline structure; they do not introduce another brand hue.

## Distribution

The public landing page places burgundy across the hero field, paper in the editorial process section, and sage/copper in concentrated accents. The product workspace moves more area to paper for sustained reading, while the burgundy shell and selected/primary controls keep the same identity.

## Contrast checks

Relative luminance ratios calculated from the selected tokens:

| Pair | Ratio | Use |
|---|---:|---|
| Ink on paper | 12.50:1 | Body text and controls |
| Paper on burgundy | 10.76:1 | Hero and navigation text |
| Ink on sage | 5.85:1 | Text on sage-filled controls |
| Ink on copper | 6.02:1 | Text on primary copper buttons |
| Sage on burgundy | 5.04:1 | Large hero emphasis and decorative marks |

For small text on paper, use charcoal or the muted neutral, not copper or sage. Every job state includes a word and shape in addition to its color. The current palette and WCAG 2.2 contrast thresholds are documented at [W3C Contrast Minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum).

## Color behavior

- **Burgundy:** identity and spatial framing.
- **Paper:** readable workspace and drawing surfaces.
- **Sage:** selected, approved, and completed cues.
- **Copper:** the next action and small printmaking marks.
- **Charcoal:** primary text on light surfaces.

Colors are not the only way to communicate status. No extra blue/purple meaning system is carried forward from the earlier concept.
