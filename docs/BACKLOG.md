# Initial project backlog

These are planned tasks, not completed implementations. All 15 tasks have corresponding [GitHub issues](https://github.com/miclaldogan/language-guided-drawing-inbetweening/issues); this list also records their initial acceptance criteria.

## 1. Finalize system architecture

[GitHub issue #1](https://github.com/miclaldogan/language-guided-drawing-inbetweening/issues/1)

Labels: research, documentation

Review component boundaries and choose an initial local architecture.

Acceptance criteria: Document responsibilities and request lifecycle; identify unresolved stack decisions; review compute and privacy constraints.

Reference: [docs/architecture/SYSTEM_ARCHITECTURE.md](../docs/architecture/SYSTEM_ARCHITECTURE.md)

## 2. Define dataset capture protocol

[GitHub issue #2](https://github.com/miclaldogan/language-guided-drawing-inbetweening/issues/2)

Labels: data, documentation

Review the draft protocol before any recording.

Acceptance criteria: Approve consent and usage policy; agree pilot size and camera settings; define motion prompts and quality/rejection criteria.

Reference: [docs/dataset/CAPTURE_PROTOCOL.md](../docs/dataset/CAPTURE_PROTOCOL.md)

## 3. Record pilot dataset

[GitHub issue #3](https://github.com/miclaldogan/language-guided-drawing-inbetweening/issues/3)

Labels: data

Capture a small consent-cleared pilot after protocol approval.

Acceptance criteria: Record approved motions and pseudonymous provenance; review face/hand/body visibility; report actual sequence counts and exclusions without committing recordings.

Reference: [docs/dataset/DATASET_CARD.md](../docs/dataset/DATASET_CARD.md)

## 4. Build frame extraction pipeline

[GitHub issue #4](https://github.com/miclaldogan/language-guided-drawing-inbetweening/issues/4)

Labels: data

Implement reproducible timestamp-aware extraction after the pilot format is known.

Acceptance criteria: Preserve source IDs/timestamps; handle variable frame rates and missing frames; validate output sampling and avoid tracking generated frames.

Reference: [docs/architecture/AI_PIPELINE.md](../docs/architecture/AI_PIPELINE.md)

## 5. Select temporally consistent drawing stylization method

[GitHub issue #5](https://github.com/miclaldogan/language-guided-drawing-inbetweening/issues/5)

Labels: data, research

Compare feasible sequence stylization approaches.

Acceptance criteria: Review licenses and compute; assess flicker, appearance, face/hand preservation, and paired alignment; document selection and rejected alternatives.

Reference: [docs/architecture/AI_PIPELINE.md](../docs/architecture/AI_PIPELINE.md)

## 6. Create dataset metadata schema

[GitHub issue #6](https://github.com/miclaldogan/language-guided-drawing-inbetweening/issues/6)

Labels: data

Define a versioned schema for paired sequences and motion instructions.

Acceptance criteria: Include clip/person/session IDs, timestamps, paired paths, action order, quality flags, transform version, provenance, allowed use, and split; exclude identity mappings.

Reference: [data/README.md](../data/README.md)

## 7. Define train/val/test split

[GitHub issue #7](https://github.com/miclaldogan/language-guided-drawing-inbetweening/issues/7)

Labels: data, evaluation

Freeze source-group-aware splits before training and tuning.

Acceptance criteria: Keep each source video and derivatives together; prefer person-disjoint splits; audit repeated takes and duplicates; document ratios, seed, and feasibility.

Reference: [docs/dataset/DATASET_CARD.md](../docs/dataset/DATASET_CARD.md)

## 8. Implement first inbetweening baseline

[GitHub issue #8](https://github.com/miclaldogan/language-guided-drawing-inbetweening/issues/8)

Labels: model, research

Implement endpoint-only Baseline A after candidate and pilot selection.

Acceptance criteria: Provide reproducible inference with reviewed weights; document conditioning and compute; evaluate under the agreed protocol; do not invent results.

Reference: [docs/experiments/EXPERIMENT_PLAN.md](../docs/experiments/EXPERIMENT_PLAN.md)

## 9. Define evaluation metrics

[GitHub issue #9](https://github.com/miclaldogan/language-guided-drawing-inbetweening/issues/9)

Labels: evaluation, research

Calibrate metrics and human review on the first baseline.

Acceptance criteria: Select implementations and aggregation; run sanity checks; address temporal order, face/hand failures, and multiple valid motions; freeze the protocol.

Reference: [docs/experiments/METRICS.md](../docs/experiments/METRICS.md)

## 10. Compare candidate video generation models

[GitHub issue #10](https://github.com/miclaldogan/language-guided-drawing-inbetweening/issues/10)

Labels: model, research

Evaluate pretrained candidates before selecting architecture or framework versions.

Acceptance criteria: Compare endpoint/text support, drawing behavior, licensing, adaptation effort, hardware, and latency; record evidence and open questions.

Reference: [docs/architecture/AI_PIPELINE.md](../docs/architecture/AI_PIPELINE.md)

## 11. Design backend API

[GitHub issue #11](https://github.com/miclaldogan/language-guided-drawing-inbetweening/issues/11)

Labels: backend

Specify generation request and job contracts.

Acceptance criteria: Define inputs/outputs, validation, status/error responses, artifact access, retention, cancellation, and model-service boundary; choose framework after review.

Reference: [docs/architecture/SYSTEM_ARCHITECTURE.md](../docs/architecture/SYSTEM_ARCHITECTURE.md)

## 12. Create frontend mockup

[GitHub issue #12](https://github.com/miclaldogan/language-guided-drawing-inbetweening/issues/12)

Labels: frontend

Design a usable keyframe and instruction submission flow.

Acceptance criteria: Show drawing inputs, motion text, progress, errors, and output playback; review accessibility and avoid exposing internal implementation details.

Reference: [docs/architecture/SYSTEM_ARCHITECTURE.md](../docs/architecture/SYSTEM_ARCHITECTURE.md)

## 13. Build end-to-end MVP

[GitHub issue #13](https://github.com/miclaldogan/language-guided-drawing-inbetweening/issues/13)

Labels: backend, frontend, model

Connect the reviewed frontend, API, and inference path locally.

Acceptance criteria: Demonstrate real start/end/text to intermediate-frame output; validate failure handling and provenance; document limits and hardware.

Reference: [docs/ROADMAP.md](../docs/ROADMAP.md)

## 14. Prepare deployment

[GitHub issue #14](https://github.com/miclaldogan/language-guided-drawing-inbetweening/issues/14)

Labels: deployment, backend

Package the validated MVP for the course demonstration.

Acceptance criteria: Document environment and serving resource needs; define logging and artifact retention; check secrets/access controls; choose hosting only after feasibility review.

Reference: [docs/ROADMAP.md](../docs/ROADMAP.md)

## 15. Final evaluation and documentation

[GitHub issue #15](https://github.com/miclaldogan/language-guided-drawing-inbetweening/issues/15)

Labels: evaluation, documentation

Run the frozen held-out evaluation and prepare course deliverables.

Acceptance criteria: Report measured comparisons and failures; finish reproducibility notes, demo video, presentation, and v1.0 release checklist; review data permissions before sharing.

Reference: [docs/ROADMAP.md](../docs/ROADMAP.md)
