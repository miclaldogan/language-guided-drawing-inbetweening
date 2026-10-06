# Project scope

## Objective

Explore generating intermediate drawing frames from start/end drawings and a natural-language instruction that describes motion order and timing. The course deliverable is an evaluated local prototype on a feasible pilot dataset; approximately 1,000 sequences and up to 150,000 aligned frame pairs are longer-term targets.

## In scope

- Controlled video acquisition.
- Paired real/drawing dataset creation.
- Drawing inbetweening.
- Language-guided motion control.
- Quantitative and qualitative evaluation.
- An end-to-end prototype connecting a UI, API, and model inference path.

## Out of scope for the initial course version

- Training a foundation video model from scratch.
- Production-scale cloud infrastructure.
- Unrestricted long-form video generation.
- Full commercial animation-suite replacement.
- Quantum ML integration.

Quantum ML may be explored in future research, but is not part of the current core architecture, dependencies, or experiment plan.

## Current foundation deliverable

Documentation, package structure, development checks, data-handling exclusions, and a task backlog. No trained model, recording collection, drawing converter, database, API, or frontend is implemented here.

## Proposed course acceptance criteria

A consent-cleared pilot; leakage-aware frozen test split; documented baseline; controlled comparison of endpoint-only and language-conditioned variants; reproducible run metadata; error analysis; and an end-to-end demonstration. Numerical thresholds and pilot size are TODOs to agree after feasibility testing. Report negative results and infeasible experiments honestly.

## Decisions pending

Capture/consent approval; team responsibilities; literature bibliography; pilot size and split feasibility; hardware and compute budget; baseline/checkpoint and license; stylization method; metric definitions; app/database/tracking stack; code license and data usage policy. No research publication or commercial suitability is assumed.
