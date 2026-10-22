# Cue — Requirements ↔ UI Traceability

Source: requirements list in the submitted proposal PDF (FR-01…FR-12, NFR-01…NFR-07, screens S1–S6 as named there). No requirement was changed.

## Matrix
| Screen | Req | User goal | UI component | Interaction | State | Acceptance check |
|---|---|---|---|---|---|---|
| S1 | FR-01 | Create account, log in | Tabs, input ×2, password toggle, primary button | submit | loading, field error, auth error | valid login lands on S2; invalid shows generic error |
| S1/top bar | FR-01 | Log out | account menu item | click | — | session ends, S1 shown |
| S2 | FR-02 | See only my animations | job gallery | open | empty, loading, fetch error | other users' jobs never listed; direct URL gives "Not found" (NFR-01) |
| S2 | FR-09 | List, see status, delete | job card, status chip, overflow menu, confirm dialog | open / delete | queued, running, done, failed, cancelled, deleting | list shows all five statuses; delete requires confirmation |
| S3 | FR-03 | Upload start and end drawing | two upload zones, preview, replace/remove | drop/browse | empty, uploading, filled, error | wrong type/size/dimension rejected with reason; Continue disabled until both valid |
| S4 | FR-04 | Describe motion in English | text area, example chips | type | empty (optional), filled, over limit | empty allowed; text kept after errors |
| S4 | FR-05 | See, approve, or be refused a plan; run without command | cue sheet, approval checkbox, alert, Generate | preview, approve | skeleton, ready, out-of-date, rejected | plan shown before generation; unsupported command refused with reason; empty command generates |
| S4→S5 | FR-06 | Start generation | primary button | click | loading | job created, user lands on S5 |
| S5 | FR-06 | Know it is working | frame strip, elapsed time | wait | queued, running | no invented percentage or ETA |
| S5 | FR-07 | Understand status and errors | status chip, alert, cancel button | cancel | queued, running, done, error, cancelled | five states each have a distinct word, icon and message |
| S5/S6 | FR-10 | See what was used | metadata panel | read | loading, not found | model version, seed, duration, plan, input shown |
| S6 | FR-08 | Watch and download | player, Download MP4 | play, step, download | loading, error, ready | MP4 downloads; playback works with keyboard |
| S6 | FR-06 | Trust first/last frame | scrubber end-tick labels | — | — | ticks 1 and 16 labelled "Your drawing" |
| — | FR-11, FR-12 | scripts | **no UI** by design | | | |
| — | NFR-01 | 404 on unauthorized | "Not found" error state (variant, not a screen) | | | |
| — | NFR-02/03 | time, consistent state | S5 states reflect server state on reload | | | |
| — | NFR-05 | privacy, deletion | delete in S2 | | | |

## Gap review
**Requirements without a dedicated interface:** FR-11, FR-12 (scripts), NFR-04, 06, 07 (engineering). Intentional.

**Screens without a requirement:** none. S1 → FR-01; S2 → FR-02, FR-09; S3 → FR-03; S4 → FR-04, FR-05; S5 → FR-07; S6 → FR-08.

**Duplicated actions:** "New animation" appears in the top bar and S2 empty state and S6; one component, three placements, acceptable. Delete appears only in S2.

**Unnecessary navigation avoided:** no sidebar, no settings, no profile page.

**Inconsistent-control check:** one primary orange control per screen; Back always bottom-left; Continue on S3 deliberately not orange.

## Recommendations requiring review (not added silently)
| ID | Observation | Proposed handling |
|---|---|---|
| R1 | Upload limits (format, size, dimensions) are not specified in FR-03 | Backend to define; UI copy placeholder TBD |
| R2 | FR-07 lists "cancelled" but no FR names a cancel action | Confirm cancel is in scope; UI includes a confirmed cancel button |
| R3 | No retry behaviour committed | Do not build; propose "Reuse inputs" as optional later |
| R4 | Queue position / progress not specified | UI shows state and elapsed time only; add fields only if API provides them |
| R5 | Delete from S6 not specified | Kept in S2 only |
| R6 | Result comparison (original vs generated) not committed | Not designed |
| R7 | Plan schema vocabulary (regions, speed levels, simultaneity) not in the PDF | Confirm with plan schema before final S4 copy |
| R8 | Account/email rules, session expiry UX | Backend decision |
| R9 | UI language (English vs Turkish) not stated | Decision D1 |
