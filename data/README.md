# Local data storage

No dataset has been collected or distributed by this repository. These folders are local storage boundaries, not published data.

| Directory | Intended contents |
| --- | --- |
| `raw/` | Restricted original recordings; preserve original files |
| `interim/` | Extracted frames and intermediate processing outputs |
| `processed/` | Validated aligned real-drawing sequences and annotations |
| `external/` | Individually reviewed external datasets, stored separately by source/terms |
| `splits/` | Local versioned split manifests; no identifying metadata in Git |

Only this README and empty directory markers are tracked. Keep consent records and identifying subject information in separately controlled storage, outside this repository. Never use names in clip IDs. Drawing conversion is not an anonymization guarantee.

Record source video ID, pseudonymous person ID, session ID, source timestamp, frame index, transform/version, paired paths, instruction and action order, quality flags, provenance, usage constraints, and split assignment. This is a proposed field list; the metadata schema is pending review.

Keep all derivatives of a source clip in its assigned split. Prefer person-disjoint splits and group repeated takes/session duplicates; check duplicates across sources. Do not randomly split frames. Fit learned preprocessing/stylization only on permitted training data. Preserve pairing when resampling or dropping frames.

Store runs and checkpoints outside the tracked tree (e.g. ignored `artifacts/` and `checkpoints/`). Exclusions also cover raster images by default. A future small consent-cleared documentation illustration requires an explicit, narrow ignore-rule exception and review; do not force-add recordings or generated frame collections.

See the [dataset card](../docs/dataset/DATASET_CARD.md), [capture protocol](../docs/dataset/CAPTURE_PROTOCOL.md), and [source register](../docs/dataset/DATA_SOURCES.md).
