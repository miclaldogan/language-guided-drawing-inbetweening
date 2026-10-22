# V1 → V2 Changelog

V1 (Midnight Motion) is preserved: files stay in `docs/design/` unchanged, and `docs/design/v1-midnight-motion-snapshot.tar.gz` holds a copy. Nothing in V1 was overwritten.

## Kept
Six screens and their states; FR/NFR traceability (`CUE_REQUIREMENTS_UI_TRACEABILITY.md`) and its recommendations R1–R9; user flows; component list; frame strip and CueSheet signatures; top-bar navigation (no sidebar); no progress percentages or ETAs; one primary action per screen; texture and colour never applied to user artwork.

## Changed
| Area | V1 | V2 |
|---|---|---|
| Mode | dark only | light paper world; dark only for the video viewer and film strip |
| Page background | `#0E0B14` | gold `#F8AA09` shell (cream in Direction B) |
| Surfaces | purple-tinted darks | cream-200 `#F6E8D1`, raised cream-100, sunken cream-300, paper-white behind art |
| Primary action | orange `#FF9A45` | ink purple `#4F0964` with cream text |
| Orange | generate and download | motion accent only (endpoint ticks, speed chevrons, End badge) |
| Purple | selection and plan | selection, plan, primary action, links |
| Blue | processing | processing and info (unchanged role, new value `#23437C`) |
| Yellow | rare highlight | the brand surface |
| Warning | yellow | amber-tint with brown text and a triangle (yellow is now the shell) |
| Focus ring | lilac | ink ring with cream gap |
| Fonts | Sora + Manrope | Fraunces + Manrope |
| Depth | lighter surfaces | 1.5 px ink outlines and a hard 3 px print shadow |
| Texture | none | static grain and fibre on shell and panels |
| UI language | English (recommended) | English, final |
| S5 strip | single row of ticks | two-row printed film strip with the same 16 frames |
| S4 CueSheet | dark lanes, lilac blocks | ruled paper lanes, ink-outline blocks, printed numerals |

## Token migration
See `migration-from-v1` in `tokens.json`. Summary: `bg-app`→`bg-shell`; `bg-elevated`→`bg-surface-raised`; `border-subtle`→`border-hair`; `accent-plan`→`plan-cue-number-bg`; `action-primary` keeps its name and changes value; `selected-*`, `info`, `warning`, `error`, `success` keep names, values re-tuned. New: `bg-viewer`, `motion-accent`, `text-accent-orange`, `focus-gap`, `texture.*`. Removed: `bg-overlay` (dialogs use `bg-surface-raised` with elevation 3). Rename in one pass at the CSS-variable layer, since components were never built against V1.

## Scope check
No screen added or removed; no feature changed; requirements untouched. The cancel action, retry, upload limits and plan vocabulary remain open (R1–R9, D1–D7 from V1).
