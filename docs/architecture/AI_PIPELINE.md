# AI pipeline — research plan

## Dataset preparation

1. Record controlled motion with approved consent and pseudonymous clip/person/session IDs.
2. Assign source-video/person groups to train, validation, or held-out test; freeze assignments before fitting learned transforms.
3. Extract frames with source timestamps at the selected sampling rate.
4. Convert sequences into drawings using a method evaluated for temporal stability. No converter has been selected.
5. Check one-to-one timestamp alignment, missing frames, style drift, face/hand visibility, and motion coverage. Both sides of a rejected pair must be handled together.
6. Annotate motion descriptions and ordered stages, with temporal spans when feasible; record review status and provenance.
7. Build local manifests, preserving split membership for every crop, conversion, augmentation, and repeated take.

## Baselines and adaptation

Investigate pretrained image-to-video or video-diffusion candidates that support endpoint/keyframe conditioning. Establish endpoint-only generation before comparing generic language and richer temporal language conditioning. If a candidate lacks a conditioning interface, record the required adaptation and feasibility cost; do not assume compatibility. Consider parameter-efficient fine-tuning only after a baseline and dataset quality checks exist.

Pose, face landmarks, and hand landmarks are optional later conditions. At inference, they must be obtainable from provided inputs or explicit user controls; using held-out ground-truth intermediate motion is an oracle experiment, not a deployable comparison.

## Generation and evaluation

Input: start drawing, end drawing, motion instruction, and eventually agreed duration/sampling controls. Output: intermediate drawing frames with ordering/timing metadata. Endpoint inclusion in returned sequences is a contract decision to settle before implementation.

Compare variants under matched splits, resolution, duration, seed sets, and compute reporting. Report endpoint consistency separately from intermediate-frame quality; include temporal order, style, face/hand failure analysis, and latency. Do not hide endpoint inconsistency by replacing generated endpoints without documenting it.

Track code commit, model/checkpoint revision and license, dataset/split version, stylization version, config, seeds, runtime environment, device, timing methodology, and artifact locations. No model, weights, training loop, or results are part of this initialization.
