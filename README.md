# Language-Guided Drawing Animation Inbetweening

A university AI engineering design project exploring language-controlled motion between drawing keyframes. **Status: research and repository foundation; no dataset, model, or experimental results are delivered yet.**

## Overview

Traditional 2D animation requires intermediate frames between keyframes. Current interpolation and video-generation systems can infer motion between images, but user control over **how** movement unfolds is still limited. This project explores drawing-domain animation generation conditioned on visual endpoints and a natural-language motion description.

```text
Start Drawing
+
End Drawing
+
Natural-Language Motion Description
↓
Intermediate Drawing Frames
```

For example, a character starts looking forward and ends turned left and smiling. The instruction “First move the eyes to the left, then slowly turn the head, and begin smiling near the end of the motion” specifies the order and timing of the movement. The project is under active research; feasibility and architectural choices remain experimental.

## Motivation

Identical start/end frames can correspond to different valid motions. A character might:

- Turn the head immediately.
- Move the eyes first and then turn the head.
- Raise a hand while turning, then lower it before the endpoint.
- Gradually transition from a neutral expression to a smile.

Endpoint information alone may not fully specify the intended animation. Language could provide additional control over the sequence, timing, and combination of actions.

## Main Research Question

> Can sparse drawing keyframes and natural-language motion descriptions be jointly used to generate temporally coherent intermediate animation frames while preserving character appearance, motion structure, facial expressions, and hand gestures?

## Proposed Pipeline

```text
Controlled Human Motion Videos
        ↓
Frame Extraction
        ↓
Temporally Consistent Drawing Conversion
        ↓
Real ↔ Drawing Paired Sequences
        ↓
Train / Validation / Test Split
        ↓
Start Drawing + End Drawing + Text Instruction
        ↓
Conditional Video Generation Model
        ↓
Intermediate Drawing Frames
        ↓
Evaluation
        ↓
Web Prototype
```

This is a conceptual pipeline. Source-video/person split assignments should be established before fitting preprocessing or stylization components; every derivative inherits its source split.

## Dataset Plan

The planned custom dataset consists of controlled short human-motion recordings and temporally consistent drawing-style conversions. Each real frame will correspond to a drawing frame at the same source timestamp.

**Long-term targets, not completed statistics:**

- Approximately 1,000 controlled motion clips.
- Around 10 seconds per clip.
- Around 15 sampled frames per second.
- Approximately 1,000 motion sequences and up to 150,000 temporally aligned real-drawing frame pairs.

The frame-pair target does not represent 150,000 independent motion samples. Adjacent frames are highly correlated. Train/validation/test splitting should happen at the video/person level, keeping each video, its derived frames, and preferably all recordings of a person in one split. A small pilot comes first; the full dataset target may extend beyond the course schedule. External datasets may supplement recordings only after individual license and usage review.

See the [dataset card](docs/dataset/DATASET_CARD.md), [capture protocol](docs/dataset/CAPTURE_PROTOCOL.md), and [source register](docs/dataset/DATA_SOURCES.md).

## Motion Coverage

- Head orientation.
- Gaze direction.
- Facial expression changes.
- Hand gestures.
- Upper-body motion.
- Full-body motion.
- Combined multi-stage actions.

## Model Direction

The project is investigating pretrained video-generation / video-diffusion architectures, including image-to-video and keyframe-conditioned generation. Adaptation and fine-tuning are preferred over training a large video foundation model from scratch.

Potential research directions include:

- First/last-frame conditioning.
- Sparse keyframe conditioning.
- Natural-language temporal control.
- Pose conditioning.
- Facial landmark conditioning.
- Hand landmark conditioning.
- Parameter-efficient fine-tuning.
- Temporally consistent stylization.

No architecture, checkpoint, training framework, or CUDA version has been selected. Candidate selection will consider drawing-domain behavior, conditioning support, compute requirements, and model/data licensing.

## Evaluation

Planned evaluation dimensions are endpoint consistency, perceptual image similarity, temporal consistency, motion continuity, text-motion alignment, character/style preservation, face consistency, hand consistency, inference time, and qualitative user evaluation.

Possible metrics under investigation include SSIM, LPIPS, PSNR where useful, FVD or appropriate video-level metrics, and text-video / text-motion alignment metrics. **Metrics are provisional until baselines are established.** Pixel agreement alone cannot establish that one of several valid motions is correct. See the [metric plan](docs/experiments/METRICS.md) and [experiment plan](docs/experiments/EXPERIMENT_PLAN.md). No scores have been measured.

## Cue: the web studio

**Cue** is the product built on top of this research: a web animation studio where a signed-in user uploads two keyframe drawings, optionally describes the motion in one English sentence, approves a structured motion plan, and receives a short generated animation (up to 16 frames, MP4 plus frames). Generation is asynchronous: a GPU worker claims jobs from a PostgreSQL-backed queue, so a request is answered immediately and progress is followed from the user's personal library.

Committed capabilities: account creation and login, a personal library (list, status, delete), keyframe upload with validation, an optional English instruction with a reviewed plan, asynchronous generation with status and clear errors, cancellation, MP4 playback and download, and a per-generation record (inputs, plan, model version, seed, duration). Out of scope: training a video model from scratch, long video, video input, password reset, sharing, admin panel, negative prompts.

| Area | Where |
| --- | --- |
| Six-screen UI design (specification, tokens, previews, Figma hand-off) | [`docs/design/`](docs/design/) |
| Database schema, migrations, data dictionary, indexes | [`docs/architecture/database-and-diagrams-v2/database/`](docs/architecture/database-and-diagrams-v2/database/) |
| UML, ER, sequence, state, deployment and AI-pipeline diagrams (English and Turkish) | [`docs/architecture/database-and-diagrams-v2/diagrams/`](docs/architecture/database-and-diagrams-v2/diagrams/) |
| Week 2 delivery (technology stack table, checklist) | [`docs/architecture/database-and-diagrams-v2/week-02/`](docs/architecture/database-and-diagrams-v2/week-02/) |

## Mockups and diagrams

Quick access to every page of the UI mockup and every engineering diagram.

**Report (Turkish, 18 pages):** database design, the 17 diagrams explained, and the UI mockups in one document: [Word](docs/reports/Cue_Veritabani_Diyagramlar_Mockuplar_Raporu.docx) · [PDF](docs/reports/Cue_Veritabani_Diyagramlar_Mockuplar_Raporu.pdf)

### UI mockup pages (Bordo Herbaryum, 1440 px screenshots)

Interactive source: [`docs/design/v10-bordo-herbaryum/index.html`](docs/design/v10-bordo-herbaryum/index.html) (open in a browser, no build step). Mockup only: no API, database or model is connected.

[Landing](docs/design/v10-bordo-herbaryum/screenshots/01-landing.png) · [Sign in](docs/design/v10-bordo-herbaryum/screenshots/02-signin.png) · [Library](docs/design/v10-bordo-herbaryum/screenshots/03-library.png) · [Keyframes (empty)](docs/design/v10-bordo-herbaryum/screenshots/04a-keyframes-empty.png) · [Keyframes (ready)](docs/design/v10-bordo-herbaryum/screenshots/04b-keyframes-ready.png) · [Motion plan (empty)](docs/design/v10-bordo-herbaryum/screenshots/05a-plan-empty.png) · [Motion plan (preview)](docs/design/v10-bordo-herbaryum/screenshots/05b-plan-preview.png) · [Motion plan (approved)](docs/design/v10-bordo-herbaryum/screenshots/05c-plan-approved.png) · [Status: queued](docs/design/v10-bordo-herbaryum/screenshots/06-status-queued.png) · [Status: running](docs/design/v10-bordo-herbaryum/screenshots/06-status-running.png) · [Status: done](docs/design/v10-bordo-herbaryum/screenshots/06-status-done.png) · [Status: failed](docs/design/v10-bordo-herbaryum/screenshots/06-status-failed.png) · [Status: cancelled](docs/design/v10-bordo-herbaryum/screenshots/06-status-cancelled.png) · [Result](docs/design/v10-bordo-herbaryum/screenshots/07-result.png) · [Wave-Line study](docs/design/v10-bordo-herbaryum/screenshots/08-wave-line-lab.png) · [Library (mobile)](docs/design/v10-bordo-herbaryum/screenshots/09-library-mobile.png) · [Landing (mobile)](docs/design/v10-bordo-herbaryum/screenshots/10-landing-mobile.png)

### Engineering diagrams

English PNGs; each has a Turkish version under `diagrams/tr/`, plus `.puml` source, `.svg` and `.pdf` beside it. Index: [`INDEX.md`](docs/architecture/database-and-diagrams-v2/diagrams/INDEX.md). All diagrams are proposals pending approval.

| Diagram | English | Türkçe |
| --- | --- | --- |
| Use case | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/use-case/uc-01-use-case.png) | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/tr/use-case/uc-01-use-case.png) |
| System architecture (containers) | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/architecture/arch-01-container.png) | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/tr/architecture/arch-01-container.png) |
| Activity: authentication | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/activity/act-01-authentication.png) | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/tr/activity/act-01-authentication.png) |
| Activity: animation creation | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/activity/act-02-animation-creation.png) | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/tr/activity/act-02-animation-creation.png) |
| Activity: job execution | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/activity/act-03-job-execution.png) | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/tr/activity/act-03-job-execution.png) |
| AI pipeline | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/ai-pipeline/ai-01-pipeline.png) | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/tr/ai-pipeline/ai-01-pipeline.png) |
| Job state machine | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/state-machine/sm-01-job-state-machine.png) | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/tr/state-machine/sm-01-job-state-machine.png) |
| ER: conceptual | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/database/conceptual-erd.png) | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/tr/database/conceptual-erd.png) |
| ER: physical schema | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/database/physical-erd.png) | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/tr/database/physical-erd.png) |
| Sequence: authentication | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/sequence/sd-01-authentication.png) | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/tr/sequence/sd-01-authentication.png) |
| Sequence: keyframe upload | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/sequence/sd-02-keyframe-upload.png) | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/tr/sequence/sd-02-keyframe-upload.png) |
| Sequence: plan preview | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/sequence/sd-03-plan-preview.png) | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/tr/sequence/sd-03-plan-preview.png) |
| Sequence: job submission | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/sequence/sd-04a-job-submission.png) | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/tr/sequence/sd-04a-job-submission.png) |
| Sequence: job execution | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/sequence/sd-04b-job-execution.png) | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/tr/sequence/sd-04b-job-execution.png) |
| Sequence: status and result | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/sequence/sd-05-status-and-result.png) | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/tr/sequence/sd-05-status-and-result.png) |
| Sequence: cancel, failure, delete | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/sequence/sd-06-cancel-failure-delete.png) | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/tr/sequence/sd-06-cancel-failure-delete.png) |
| Deployment | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/deployment/dep-01-deployment.png) | [PNG](docs/architecture/database-and-diagrams-v2/diagrams/tr/deployment/dep-01-deployment.png) |

### Chosen stack (proposal) and what is verified

React frontend, FastAPI backend, **PostgreSQL 18** (users, sessions, job queue, motion plan as JSONB, model versions, media metadata), a file store for drawings, frames archive and MP4 behind a `MediaStore` interface, a separate GPU worker, Docker Compose. The AI components (ToonCrafter backbone, LoRA, plan module, English plan interpreter) are research hypotheses and are **not implemented or verified yet**.

The database design is verified against a disposable PostgreSQL 18 container: constraints and ownership foreign keys, column-level permissions, job state consistency, concurrent workers claiming jobs (`FOR UPDATE SKIP LOCKED`), worker crash and cancellation races, idempotent submission, migrations (up/down/up), a row-level-security proposal, and backup/restore with media reconciliation. 110 tests, run with Docker and `uv` (no system packages needed):

```bash
docs/architecture/database-and-diagrams-v2/database/validation/run.sh
```

Diagrams are PlantUML sources (`.puml`) with rendered `.svg`/`.png`/`.pdf`; Turkish versions are generated from the English sources (`tools/build_tr.py`). SVG files reference the DejaVu Sans font by name; use the PNG or PDF files for sharing. See the [database and diagrams README](docs/architecture/database-and-diagrams-v2/README.md) for regeneration commands.

## System Architecture

The eventual system is expected to contain a frontend, backend/API, model service, dataset pipeline, training pipeline, evaluation pipeline, database, and experiment tracking. Boundaries and technology choices are provisional; the initial prototype may run locally without separately deployed services.

See [system architecture](docs/architecture/SYSTEM_ARCHITECTURE.md) and the [AI pipeline](docs/architecture/AI_PIPELINE.md).

## Project Status

Research and data:

- [x] Project definition
- [x] Initial literature review (project-provided status; bibliography to be recorded)
- [x] Dataset strategy
- [ ] Dataset capture protocol
- [ ] Pilot dataset
- [ ] Stylization pipeline
- [ ] Baseline model
- [ ] Language conditioning experiments
- [ ] Full model integration

Product (Cue web studio):

- [x] Requirements baseline (12 functional, 7 non-functional) and six-screen flow
- [x] UI design specification (six screens, tokens, component spec; design studies v1-v10)
- [x] Database design: PostgreSQL schema, migrations, data dictionary, indexes (verified, 110 tests)
- [x] Engineering diagrams: use case, architecture, three activity flows, AI pipeline, job state machine, ER, seven sequence diagrams, deployment
- [x] Week 2 technology stack table
- [ ] Clickable Figma prototype (six screens)
- [ ] Backend skeleton (database, authentication, endpoints, Swagger)
- [ ] Frontend, GPU worker, plan interpreter, end-to-end MVP
- [ ] Web prototype
- [ ] Deployment (Docker Compose, HTTPS, logging)
- [ ] Final evaluation

The capture protocol included here is a draft awaiting pilot validation. The literature-review status follows the supplied project brief and is not a claim that this repository contains a verified literature review.

## Repository Structure

```text
.
├── README.md
├── .gitignore
├── .env.example
├── .pre-commit-config.yaml
├── pyproject.toml
├── requirements/                 # Base, training, and app dependency boundaries
├── configs/                      # data/, model/, training/, inference/
├── data/                         # Local-only raw/interim/processed/external/splits
├── src/
│   └── language_guided_drawing_inbetweening/
│       ├── data/
│       ├── preprocessing/
│       ├── stylization/
│       ├── models/
│       ├── training/
│       ├── inference/
│       ├── evaluation/
│       └── utils/
├── app/                          # backend/, frontend/
├── scripts/                      # data/, training/, evaluation/, inference/
├── notebooks/                    # 01-data-exploration/, 02-baselines/, 03-experiments/
├── tests/
├── docs/                         # Scope, roadmap, architecture, dataset, experiments
├── assets/                       # diagrams/, examples/ — reviewed small public-safe assets
├── third_party/                  # Dependency and license review guidance
└── .github/                      # CI and issue templates
```

The requested source responsibilities live under a project-specific Python namespace inside `src/`, avoiding generic top-level imports such as `data` or `models`. Empty future implementation directories have placeholders, not fabricated implementations.

See the [initial task backlog](docs/BACKLOG.md) for research and implementation acceptance criteria.

## Development Setup

Use **Python 3.11**. No large ML packages are required or installed by this foundation.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
pre-commit install
cp .env.example .env
ruff check .
ruff format --check .
pytest
pre-commit run --all-files
```

The initial test checks package installation only; there are no model tests or training commands yet. `requirements/base.txt`, `training.txt`, and `app.txt` reserve dependency boundaries. Add reviewed dependencies when a component is selected; do not assume these files define runnable services. Development-tool ranges are intentionally not an ML environment lock.

## Data and Licensing

- Custom recorded data will have its own consent and usage policy, established before recording.
- Third-party datasets must be reviewed individually in the [source register](docs/dataset/DATA_SOURCES.md).
- Dataset licenses and source-code licenses must be treated separately; model weights may carry separate terms too.
- External data must not automatically be redistributed.
- Non-commercial datasets must not silently be mixed into a dataset intended for commercial use.

No blanket dataset license is assigned. The source-code license is also undecided; no open-source permission is implied. Raw recordings, extracted/generated frames, model weights, checkpoints, secrets, and experiment artifacts must not be committed. See [data storage guidance](data/README.md) and [third-party guidance](third_party/README.md).

## Academic Context

This repository belongs to a university Artificial Intelligence / Engineering Design course project and may later evolve into a research project. It makes no publication claims. The [scope](docs/PROJECT_SCOPE.md) and [10-week roadmap](docs/ROADMAP.md) distinguish the initial course deliverable from longer-term research targets.

## Status

The repository contains the research foundation (scope, dataset and experiment plans, tooling, CI), the Cue product design (UI specification and engineering diagrams) and a tested database design. No trained model, dataset, backend, frontend or worker implementation exists yet. Progress is tracked in the [backlog](docs/BACKLOG.md) and the [roadmap](docs/ROADMAP.md).
