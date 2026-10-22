# Cue — Responsive, Accessibility and Frontend Handoff

Layout breakpoints are in `CUE_SPACING_AND_LAYOUT.md`; colour contrast results are in `CUE_COLOR_SYSTEM.md`. This file adds behaviour rules and the mapping to code. Target: WCAG 2.2 AA.

## Accessibility rules
- **Keyboard:** every action reachable by Tab; logical order = visual order; Esc closes dialogs and tooltips; arrows in tabs; Space/←/→ in the player.
- **Focus:** 2 px `focus-ring` + 2 px offset, always visible, never removed; focus is not obscured by sticky bars (scroll-padding = top bar height + 8) (WCAG 2.4.11).
- **Targets:** ≥40 px (≥24 px is the AA minimum, 2.5.8).
- **Status without colour:** each chip has a word and an icon; errors have an icon and text; the cue sheet has an ordered text list.
- **Forms:** visible labels, errors tied with `aria-describedby`, `autocomplete` on email/password, errors announced via `role=alert`.
- **Upload zones:** native file input reachable, not only drag-and-drop (2.5.7 dragging alternative).
- **Progress:** upload bar uses `role=progressbar` with value; generation activity uses `role=status` text ("Running, 2 min 10 s"); the shimmer carries no value. Update the live region at most every 30 s to avoid noise.
- **Video:** custom controls expose labels and state; frame-step buttons; the video has no audio, so no captions are needed (declare "no audio" in the UI).
- **Reduced motion:** see motion doc.
- **Language:** `lang="en"`; if Turkish UI is chosen later, per-locale `lang`.
- **Contrast of user content:** drawings are the user's; the UI never overlays text on them except the "Start/End" corner labels, which sit on an opaque chip.

Manual checks to perform on the built UI (not yet done): screen-reader pass (NVDA/VoiceOver) of S4 and S5, 200% zoom and 320 px reflow, forced-colors mode, keyboard-only walkthrough of the main flow.

## Responsive decisions for the workspace
The creative surface is two images and a sentence, not a canvas, so nothing needs hover or precision pointing. Below 768 px: S3 slots stack; S4 order is keyframes thumbnails → instruction → plan list → approval → Generate (sticky bottom bar); S6 video is full width with controls under it; the side metadata becomes a collapsible section. Hover-only affordances are never the sole route (card menus are visible on touch).

## Frontend handoff
| Design | Code |
|---|---|
| Tokens JSON | `tokens.css` CSS variables (`--bg-surface`, `--action-primary`…) generated from JSON; Tailwind theme extends from the same variables; no hex in components |
| Text styles | utility classes or a `Text` component with `variant` prop |
| Components | `components/ui/`: Button, Input, Textarea, Tabs, StatusChip, ProgressBar, FrameStrip, UploadZone, Dialog (use a headless primitive such as Radix for focus trapping), Alert, Toast, Tooltip |
| Cue-specific | `components/cue/`: CueSheet, CueBlock, PlayerControls |
| Layouts | `layouts/AuthLayout`, `AppShell` (top bar + stepper slot), `StageWithPanel` |
| Pages | `pages/Auth`, `Library`, `Keyframes`, `MotionPlan`, `GenerationStatus`, `Result` |
| Semantic HTML | `<header>/<nav aria-label="Main">/<main>`, `<h1>` = screen title, job card = `<article>` with a single link, cue list = `<ol>`, stepper = `<ol>` with `aria-current="step"`, status = `<span role="status">` where live |
| Focus | one global `:focus-visible` rule using the ring tokens |
| Fonts | self-hosted WOFF2, `font-display: swap` |
| State | server state (jobs) polled or pushed; UI states map 1:1 to FR-07 statuses |

React and CSS-variables are the stack in the proposal (React client, FastAPI server). Nothing here assumes a specific component library beyond a headless dialog primitive, which is optional.
