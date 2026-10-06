# Evaluation metrics — provisional

All metrics below are candidates, not implemented or validated measures. Freeze exact implementations, versions, preprocessing, aggregation, and reporting conventions after the first baseline. No scores or success thresholds are established.

| Dimension | Candidate measurement | Caveat / decision to resolve |
| --- | --- | --- |
| Endpoint consistency | SSIM, LPIPS, PSNR where useful against supplied endpoints | Report raw generated endpoints separately if endpoints are inserted by construction |
| Perceptual image similarity | LPIPS and SSIM on aligned reference drawing frames | Multiple valid motions and timing differences can penalize plausible outputs |
| Temporal consistency | Appropriate temporal perceptual or flow-based consistency measure | Flicker reduction alone may reward static outputs; select and validate the implementation |
| Motion continuity | Pose/flow trajectory continuity and human review | Detector reliability on stylized drawings is unverified |
| Text-motion alignment | Text-video/text-motion similarity plus stage order/timing rubric | Generic embedding scores may miss order, gaze, and subtle expression timing |
| Character/style preservation | Perceptual features and qualitative identity/style rubric | Human-face identity tools may not transfer to drawings |
| Face consistency | Landmark/expression stability plus human review | Report missing detections and failure rate, not only successful detections |
| Hand consistency | Landmark/gesture checks and human review | Occlusions and drawing-domain detector errors can distort scores |
| Video-level quality | FVD or an appropriate alternative | Sample size, feature encoder domain, and preprocessing strongly affect interpretation |
| Inference time | End-to-end and model-only latency, memory, hardware, output size | Separate cold/warm runs; report loading, preprocessing, generation, postprocessing |
| Qualitative user evaluation | Consent-compatible, randomized blinded comparison and rubric | Participant count, procedure, and uncertainty are TODO |

## Reporting plan

Use the same held-out sequences, resolution, sampling, and comparable seed sets across variants. Report sequence-level aggregates, motion-category breakdowns, failure rates, and uncertainty when sample size permits; adjacent frames are not independent motion samples. Evaluate endpoints and intermediate frames separately. Define whether each metric expects higher or lower values only after selecting its exact implementation.

Check metric behavior with simple sanity cases before trusting model comparisons (identical reference, temporal shuffling, frozen motion, corrupted frames). Do not convert undefined or failed measurements into zeros. Keep raw run artifacts outside Git; commit reviewed small summary reports without private recordings or identifiable metadata.
