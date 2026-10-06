# Dataset capture protocol — initial draft

This protocol must be reviewed before recording and will evolve after pilot experiments. No recording or participant consent is claimed to exist.

## Suggested settings

- Clip length: **7–10 seconds** per controlled motion sequence.
- Source recording: **1080p / 30 FPS**.
- Potential training sampling: **12–15 FPS**, preserving source timestamp correspondence.
- Stable camera; use a tripod or fixed mount.
- Consistent lighting and simple initial backgrounds.
- Full body visible when necessary, including sit/stand transitions.
- Hands visible throughout relevant gestures; face sufficiently visible for expression/gaze tasks.
- Minimal motion blur; check focus, exposure, framing, and occlusion before each take.

Record actual dimensions, frame rate/timebase (including variable-frame-rate behavior), duration, device, and session details. Do not assume timestamps can always be recovered from nominal FPS alone.

## Before capture

Approve consent and usage/retention terms; obtain participant agreement; assign pseudonymous person/session/clip IDs. Keep names, contact information, and consent records outside Git in controlled storage. Avoid bystanders and unintended background identifiers. Confirm participant comfort and allow stopping any action.

## Motion groups

- Neutral → smile.
- Neutral → surprised.
- Look left → look right.
- Head forward → head left.
- Hand down → hand raised.
- Idle → wave.
- Sit → stand.
- Turn → smile.
- Look → turn → gesture.
- Expression + hand + body combinations.

Use paired prompts with similar endpoints but different stage order or timing where feasible. Include clear brief start/end holds within the clip duration. Repeat takes with recorded variations; do not treat repeats as independent split candidates. Describe observer-relative versus subject-relative left/right consistently in annotations.

## Per-take record and quality review

Record clip ID, person/session ID, motion category, planned instruction, observed action sequence, timing notes, camera settings, quality flags, consent-policy reference, and approved access scope. Check framing, hand/face visibility, focus, endpoint clarity, blur, background privacy, and whether the performance matches the instruction. Mark exclusions and reasons rather than silently changing labels.

## Pilot exit review

TODO: Agree pilot size and participant count. Test extraction and one-to-one real/drawing pairing; inspect stylization flicker and identity/hand/face drift; review annotation agreement and stage timing. Confirm enough independent people/videos for meaningful grouped splits. Resolve quality failures and revise this protocol before scaling.

## Storage and splitting

Preserve restricted originals under local `data/raw/`; derivatives inherit source IDs and split membership. Freeze a person/video-level held-out set, audit repeated takes and near-duplicates, and avoid fitting learned processing on validation/test data. Use [data storage guidance](../../data/README.md) and the [dataset card](DATASET_CARD.md).
