# Component Refinement

Full V1 state tables still apply (`../CUE_COMPONENT_LIBRARY_SPEC.md`); this lists what changed. Focus on every control: 2 px purple ring, 2 px paper gap. Hover: 6% ink overlay. Pressed: 12%. Disabled: sunken paper, ink-600 text. Targets ≥ 40 px.

| Component | V3 spec | Change from V2 |
|---|---|---|
| Navigation | 64 px purple, wordmark, separator, Library with 3 px gold bar, account control | was ink on gold |
| Sheet | paper-200, radius 14, soft shadow, 1 px 10% edge, 32 px padding | replaces all panel boxes |
| Primary button | purple fill, paper-100 text, no outline, radius 8, 44–50 px | removed outline and hard shadow |
| Secondary button | paper-100 fill, 1 px `#85748A` | was 1.5 px black |
| Danger button | paper-100 fill, 1 px brick, brick text | |
| Ghost action | purple text, icon | new, for "New animation" on S6 |
| Input / text area | 46 px, paper-100 fill, 1 px control border, focus 2 px purple with gap | thinner border |
| Upload zone | `#F9F1E0`, dashed 1.5 px `#85748A`; drag-over: purple dashed border plus tint; filled: artwork on paper-100 with 1 px 14% edge | |
| Start / End identity | Start: purple numeral circle; End: gold circle with 1.3 px ink outline; each with a word | gold and purple, as asked |
| Gallery item | no card box; thumbnail radius 6 with a small soft shadow; title, date, chip below; duration chip on done items | was a boxed card |
| Video thumbnail | done: poster plus "3.2 s" chip; processing and queued: dimmed art plus mini frame strip; failed: hatched sunken paper with triangle | |
| Status chip | 26 px, tinted fill, no outline, icon + word | outline removed |
| Frame strip | 16 thin ticks (6 px); start purple, end gold with ink outline | thin ticks, not squares |
| Film strip (S5) | dark viewer strip, 16 frames, dashed pending frames, frames 1 and 16 outlined; numbers beneath | single row, no per-frame progress |
| Cue row / CueSheet | rail with 30 px numbered nodes (Fraunces numerals), title 17/800, region 13.5, speed meter (3 bars + word), "then" label between nodes | replaces lane boxes and arrows |
| Player | purple play disc, ghost icon buttons, strip scrubber with a purple current-frame outline, "Frame 8 of 16" | |
| Dialog | paper-100, radius 14, elevation 3, 24 px padding; destructive confirm in brick | |
| Alert / feedback | state-tint fill, 4 px left bar, icon, bold title, detail line; no outline | |
| Tooltip | ink fill, paper-100 text | |
| Toast | paper-100, elevation 2, left bar in state colour | |

## Border hierarchy
None (grouping by space and tone) → hairline 12% ink (dividers, sheet edge) → control border `#85748A` (inputs, secondary buttons, upload) → strong 2 px purple (selected, focus). No black 1.5 px outlines remain.
