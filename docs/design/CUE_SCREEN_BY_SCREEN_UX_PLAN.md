# Cue — Screen-by-Screen UX Plan

Six screens, as committed. States are variants of a screen, not new screens. UI copy is English (commands are English; see review item D1). Values marked **TBD** are not fixed by the requirements.

Shared chrome (S2–S6): top bar (wordmark, Library, New animation, account menu with Log out), then stepper on S3–S6.

## S1 — Authentication (FR-01)
Layout: left 5/12 brand panel on bg-canvas with the frame strip slowly settling once on load (see motion doc) and one line: "Two drawings in, one clip out." Right: form.
- Tabs: Log in | Create account (one screen, two states).
- Fields: email, password (show/hide toggle, 44 px target). Create account has no extra fields unless the backend requires them.
- Password rules shown under the field before typing, not after failing. Exact rules **TBD** with backend.
- Validation on blur; error text under the field with icon; form-level error in an alert above the button ("Email or password is incorrect.", never revealing which).
- Loading: button shows spinner and "Logging in…", fields disabled.
- Success → S2. Orange button: "Log in" / "Create account".
- No password reset, no social login.

## S2 — Personal video dashboard (FR-02, FR-07, FR-09)
Title "Your animations". Primary action "New animation" (orange, top right). In the empty state the same action is a secondary button, so the screen keeps a single orange control.
- Gallery of job cards, newest first. Card = 8:5 thumbnail, title (first 40 chars of command, else "Untitled animation"), created date, status chip.
- Done: thumbnail is the result's first frame; hover shows play affordance (poster only, no autoplay). Click → S6.
- Queued/running: placeholder thumbnail with the start drawing dimmed and the frame strip; chip "Queued" or "Running". Click → S5.
- Error: placeholder with icon, chip "Failed", one-line reason. Click → S5 (shows detail). Cancelled: chip "Cancelled".
- Delete (FR-09): overflow menu on the card → confirmation dialog "Delete this animation? The video and its drawings are removed." Cancel / Delete (destructive, not orange).
- Empty: "No animations yet. Upload two drawings to make your first one." + New animation.
- Loading: 6 skeleton cards. Fetch error: inline alert with "Try again".
- No filters, search, sort or folders (not required). Revisit only if lists get long.

## S3 — Keyframe upload (FR-03)
Two equal 8:5 slots, labelled **Start drawing** and **End drawing**, with a connector between them (a dotted line with a small run of ticks) so order is spatial. Slot header carries the label, not only the placeholder.
- Empty slot: dashed input-border, icon, "Drop an image or browse", accepted formats and limits below (**format, max size and required dimensions TBD**; output is 512×320, so show how the image will be fitted: "Shown at 8:5").
- Uploading: file name, determinate bar (upload progress is measurable), cancel.
- Filled: preview on drawing-paper matte, file name, size, dimensions, Replace and Remove buttons.
- Error (in slot, role=alert): wrong type, too large, wrong dimensions; says what to do.
- Selected/drag-over: purple border.
- Action row: "Back to Library" (secondary) and "Continue to motion" (secondary style, not orange, because orange is reserved for starting generation). Continue stays disabled until both slots are valid, with a helper line stating why.
- Do not swap automatically; offer a "Swap" icon button between slots (low-cost, prevents re-upload).

## S4 — English motion prompt and plan (FR-04, FR-05, FR-06)
The signature screen. Layout: top, keyframe pair as small thumbnails (start→end, read-only, "Change" returns to S3). Below, two columns: left the instruction, right the plan. Cue sheet spans below both.
1. **Instruction field.** Label "Describe the motion (optional)". Text area, placeholder "First move the eyes to the left, then turn the head slowly." Helper: "Describe the order of movements in English. Leave empty to generate from the drawings only." Char limit **TBD**. Example chips (2–3 samples) insert text on click.
2. **"Preview plan"** (secondary button). Calls the plan parser. Loading: cue sheet shows skeleton lanes with "Reading your instruction…".
3. **Cue sheet.** Lanes per region (gaze, head, expression, hand — final vocabulary **TBD**, from the plan schema). Each event is a numbered cue block in lane, showing region action and speed (slow / normal / fast). Blocks are ordered left to right; label "Order shown, not exact timing". Simultaneous events (if the schema allows) share a column with a "together" bracket. Reading order is also available as a numbered list below for screen readers and narrow screens.
4. **Approval.** Checkbox "This plan is correct" (required when a plan exists). Changing the text invalidates the approval and greys the cue sheet to "Out of date" until previewed again.
5. **Primary action.** "Generate animation" (orange, 48 px). Enabled when: no instruction (drawings-only run, FR-05 "komutsuz üretim") or a current plan is approved. When disabled, a line explains which.
6. **Unsupported instruction (FR-05 reasoned rejection).** Yellow alert replaces cue sheet: "Cue couldn't turn this into a plan. [reason from validator]. Try: 'First move the eyes to the left, then turn the head.'" Negative commands, unsupported regions and more than two events (if limited) produce specific reasons. Text stays editable.
7. No manual drag/reorder, no timing handles, no region drawing (out of scope). Optional plan picker (preset plans) exists only as the proposal's fallback; do not build unless the language layer fails (decision D4).

## S5 — Generation status (FR-06, FR-07, FR-10)
Stage: start and end drawings on either side of a large frame strip (16 ticks). Header: job title and status chip.
- **Queued:** "Waiting for the GPU worker." Frame strip static. Elapsed time since submit. Queue position only if the API exposes it (**TBD**).
- **Running:** "Generating 16 frames." Strip ticks 2–15 show a slow sweeping shimmer (activity, not progress). Elapsed time ticking. No percentage and no ETA unless the backend measures them; if it ever reports "frames done", ticks fill.
- **Done:** strip full, chip "Done", primary button "View result" (orange) → S6. No auto-redirect.
- **Error:** red alert with the human-readable message (FR-07), job id, and what to do. Buttons: "Back to Library", "Start a new animation". "Retry with same inputs" is a recommendation requiring review (R3).
- **Cancelled:** neutral message and back links.
- **Cancel:** secondary text-danger button "Cancel generation" with a confirm dialog, shown while Queued/Running. The cancelled state exists in FR-07; a cancel action is implied but not worded in the FRs (R2).
- Side panel: submitted plan summary (read-only cue list), model version and seed once known (FR-10).
- Leaving the page does not stop the job; a line says so, and the Library card continues to update.

## S6 — Result preview and export (FR-08, FR-10)
Stage: the clip in an 8:5 frame on bg-canvas, up to 1280 px wide; it is the largest element on the page.
- Player: Play/Pause, loop toggle, frame-step back/forward (meaningful because there are ≤16 discrete frames), scrubber made of the frame strip with the first and last ticks marked "Your drawing". Keyboard: Space play, ←/→ step. Speed control only if cheap; not required.
- Primary: "Download MP4" (orange). Secondary: "Back to Library", "New animation".
- Side panel (FR-10): command used, plan summary, model version, seed, duration of generation, created date, file size.
- Error: video fails to load → alert "The video couldn't be loaded" with Reload and Download retry; download fails → toast + inline retry.
- No comparison or sharing (not committed). Delete is available through the Library; a duplicate action here is not added (see R5).
