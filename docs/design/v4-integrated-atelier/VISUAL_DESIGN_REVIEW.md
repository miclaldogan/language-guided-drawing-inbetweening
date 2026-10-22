# Visual Design Review (V4)

Judged against the rejection criteria, using the rendered screens (`previews/`, `experiments/`, `before-after/`).

| Rejection criterion | Result |
|---|---|
| 1 A giant rounded panel still encloses the page | **Pass.** No enclosing container on any screen. The only large rounded shape is the level-3 dialog. S3's worktable is a full-bleed band with hairline edges. |
| 2 Looks like an ordinary SaaS template | **Partial.** Layout is cleaner than V3, but a card grid with kebab menus is a familiar pattern. The paper, brush corners, margin marks and artwork are what differ. |
| 3 Paper texture excessive | **Pass.** 5% grain, 4% fibre; no texture under inputs, cards or artwork. At 100% it reads as paper, not noise. |
| 4 Registration marks interfere | **Pass.** They live in the 72 px margins only. |
| 5 Yellow disappears | **Borderline.** Present on every screen (nav stripe, corners) and strong on S1 (31%), but only 2–4% on S2–S6. I tried a title highlight to raise it and removed it because it looked gimmicky. Decision V4-D1. |
| 6 Purple navigation loses consistency | **Pass.** Same 64 px bar on S2–S6 with the same stripe. |
| 7 Thumbnails stop being the focus | **Pass.** They are the most saturated and largest content; no competing fills. |
| 8 Childish or decorative | **Pass with a caveat.** No stickers or mascots; the brush is limited to edges. The artwork is simple vector stand-ins. |
| 9 Functional components made less usable | **Pass.** Controls keep the V3 sizes and borders (inputs 3.4–4.2:1); the kebab has a 40 px target; the delete flow is a dialog. |
| 10 Six screens no longer share a design language | **Pass.** One template, one header, one footer, one set of surfaces. S1 is the intentional exception and shares the brush, marks and palette. |

## Problems found during rendering and fixed
- Torn-looking brush edges (displacement too strong): reduced to scale 8 at lower frequency.
- Dialog copy ran past its box: split across two lines.
- Title highlight in gold looked like a marker pen: removed.
- S3 worktable band is drawn over the margin guide lines, which now show through at its edges; cosmetic.

## Remaining weaknesses
- Gold balance (V4-D1).
- The S1 purple block has ragged edges that may read as torn paper rather than painted.
- Mock art is procedural, not real drawings.
- Accessibility checks beyond contrast need a built UI.

## Verdict
The giant-container problem is solved in the renders. The result is closer to an animation studio's asset library than V3. It is not finished until the gold balance is decided and real artwork is tested in it.
