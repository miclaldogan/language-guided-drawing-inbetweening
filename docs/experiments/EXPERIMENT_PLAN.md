# Experiment plan — conceptual

No experiments have run and no results are reported. Model, dataset, compute budget, and metric implementations remain unselected.

## Research comparison

| Family | Visual input | Language input | Purpose |
| --- | --- | --- | --- |
| Baseline A | Start + end drawing | None | Measure what endpoints alone can specify |
| Baseline B | Start + end drawing | Generic text encoder conditioning | Test whether language improves instruction adherence |
| Proposed / advanced | Start + end drawing | Richer temporal language conditioning | Test staged action order and timing control |
| Optional later | Start + end drawing | Selected language variant | Ablate pose, face landmarks, and hand landmarks separately |

Richer conditioning might encode ordered stages or temporal spans; its representation and model integration are open questions. A generic encoder also requires a model-compatible conditioning pathway. Do not assume any candidate natively supports all variants.

## Protocol

1. Approve source/model terms, pilot quality, and a frozen group-aware held-out split.
2. Compare feasible pretrained candidates on conditioning support, drawing preservation, memory, latency, and adaptation effort; record rejected options and reasons.
3. Establish Baseline A and metric sanity checks before fine-tuning or advanced variants.
4. Match dataset/splits, output resolution, clip length, sampling, and seed sets where feasible. Identify unavoidable architectural differences as confounders.
5. Evaluate endpoint-matched instructions with different temporal order/timing, plus a no-text or shuffled-text ablation when feasible. Check whether the output actually changes with the instruction.
6. Tune on validation data only. Keep test data out of checkpoint selection and learned preprocessing. Use sequence/person-level summaries rather than treating adjacent frames as independent trials.
7. Log configuration, code/model/data revisions, hardware, seeds, timing, failure cases, and controlled artifact references. Distinguish development observations from final test results.
8. Run the agreed final benchmark once the protocol is frozen; report all variants, exclusions, negative results, and limitations.

Optional conditions must be available at inference. Results using ground-truth intermediate poses/landmarks must be labeled as oracle studies and separated from deployable variants.

## Results table template

An em dash means **not measured**, never zero. Create a row per completed, traceable run; attach split/config/model identifiers and metric definitions in Notes or a linked report.

| Experiment | Visual Conditions | Text Conditioning | Additional Conditions | SSIM | LPIPS | Temporal Metric | Text-Motion Metric | Inference Time | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TODO — no run yet | TODO | TODO | TODO | — | — | — | — | — | No results collected |

See [METRICS.md](METRICS.md). Metric names, aggregation, and thresholds remain provisional until baseline calibration.
