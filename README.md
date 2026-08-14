# Sleep Temporal Entropy (STE)

[![Tests](https://github.com/JonChen916/SleepTemporalEntropy/actions/workflows/tests.yml/badge.svg)](https://github.com/JonChen916/SleepTemporalEntropy/actions/workflows/tests.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21926192.svg)](https://doi.org/10.5281/zenodo.21926192)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Sleep Temporal Entropy (STE) is an entropy-based metric derived from a
hypnogram. It quantifies how the total duration of a sleep stage is distributed
among its continuous episodes (bouts). This repository contains the reference
Python implementation accompanying the manuscript *Sleep Temporal Entropy as a
Digital Biomarker of Sleep Fragmentation for Cardiometabolic and Mortality
Risk*.

## Definition

For a sleep stage with episode durations \(d_1, \ldots, d_n\), define

\[
p_j = \frac{d_j}{\sum_{k=1}^{n} d_k}
\]

and

\[
\mathrm{STE} = -\sum_{j=1}^{n} p_j \log_2(p_j).
\]

The implementation reports stage-specific STE for Wake, N1, N2, N3, and REM.
NREM STE pools the N1, N2, and N3 episode durations. Overall STE pools all
recognized stage episodes, including Wake. A stage represented by one episode
has an entropy of 0; a stage with no episodes is reported as `null`/`None`.
See [`docs/algorithm.md`](docs/algorithm.md) for the complete operational
definition.

## Installation

Python 3.9 or newer is required.

```bash
git clone https://github.com/JonChen916/SleepTemporalEntropy.git
cd SleepTemporalEntropy
python -m pip install .
```

For development and testing:

```bash
python -m pip install ".[test]"
pytest
```

## Quick start

The repository contains only a fully synthetic XML annotation. It does not
contain participant-level SHHS or SSHSC data.

```bash
sleep-temporal-entropy examples/synthetic_sleep_stages.xml
```

Python API:

```python
from sleep_temporal_entropy import calculate_sleep_temporal_entropy

result = calculate_sleep_temporal_entropy(
    "examples/synthetic_sleep_stages.xml"
)
print(result)
```

The returned keys are:

```text
Wake_Time_Entropy
N1_Time_Entropy
N2_Time_Entropy
N3_Time_Entropy
REM_Time_Entropy
Overall_Time_Entropy
NREM_Time_Entropy
```

NSRR XML stage labels currently recognized are `Wake`, `Stage 1 sleep`,
`Stage 2 sleep`, `Stage 3 sleep`, `Stage 4 sleep` (combined with N3), and
`REM sleep`. Text following the first `|` in an `EventConcept` is ignored.

## Data availability and privacy

SHHS data are available through the National Sleep Research Resource (NSRR),
subject to an approved data-access request and the applicable Data Access and
Use Agreement: <https://sleepdata.org/datasets/shhs>. Restricted
participant-level files must not be uploaded to this repository. See
[`data/README.md`](data/README.md).

## Reproducibility

Run the complete public verification workflow with:

```bash
python -m pip install ".[test]"
pytest
sleep-temporal-entropy examples/synthetic_sleep_stages.xml
```

The synthetic example and hand-calculated unit tests verify XML parsing,
episode merging, stage-specific entropy, NREM entropy, and overall entropy.
Study-level statistical analyses require controlled-access cohort data and are
not included in this metric-only repository.

## Citation

Citation metadata are provided in [`CITATION.cff`](CITATION.cff). GitHub will
display them through **Cite this repository**. To reproduce or cite the
software used for the associated manuscript, cite the archived `v1.0.0`
release:

> Chen, J. *Sleep Temporal Entropy* (Version 1.0.0) [Computer software].
> Zenodo. <https://doi.org/10.5281/zenodo.21926192> (2026).

The version-specific DOI above identifies the exact archived release. The
[concept DOI](https://doi.org/10.5281/zenodo.21926191) resolves to the latest
software version. The software DOI and the future journal-article DOI are
different identifiers and should be cross-linked after article publication.

## License

Copyright © 2026 Jiong Chen. Released under the [MIT License](LICENSE).
