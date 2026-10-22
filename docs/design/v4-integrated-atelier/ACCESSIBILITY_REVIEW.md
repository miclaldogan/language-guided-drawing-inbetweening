# Accessibility Review (V4)

Target WCAG 2.2 AA. The palette is unchanged from V3, so the V3 contrast table applies in full (`../v3-editorial-atelier/ACCESSIBILITY_AUDIT.md`). New or changed pairs, calculated with the same formula:

| Pair | Ratio | Needs | Result |
|---|---|---|---|
| Eyebrow `#6E5F76` on page `#F5EBD8` | 4.99 | 4.5 | pass |
| Kebab dots `#6E5F76` on card `#FFFAF0` | 5.67 | 3 | pass |
| Muted caption `#6E5F76` on worktable `#F0E4CC` | 4.68 | 4.5 | pass |
| Secondary text `#4D3D55` on worktable | 7.89 | 4.5 | pass |
| Ink on worktable | 13.65 | 4.5 | pass |
| Dialog text `#4D3D55` on `#FFFAF0` | 9.55 | 4.5 | pass |
| Input border `#85748A` on worktable | 3.43 | 3 | pass |
| Upload dashed border `#85748A` on `#FAF3E3` | 3.91 | 3 | pass |
| Gold stripe, corners, margin marks | decorative | n/a | no information carried |
| Gold on purple (nav indicator, avatar) | 8.12 | 3 | pass |

## Notes
- Registration marks and brush carry no information, are `aria-hidden`, and are removed under `prefers-contrast: more` and forced-colors.
- No text sits on the gold corners or marks except the S1 hero, where the marks are masked behind the text block.
- The dialog traps focus, closes with Esc and returns focus to the kebab button; Delete is brick-coloured and never the default focus target.
- Kebab menu: `aria-haspopup="menu"`, 40 px hit area, visible focus.
- Status chips keep icon plus word.
- 200% zoom: single-column reflow, no horizontal scroll (see LAYOUT_SYSTEM.md). Not tested in a browser.
- Not done: screen-reader pass, real keyboard walkthrough, forced-colors test, user eye-comfort test.
