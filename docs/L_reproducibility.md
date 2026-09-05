# Deliverable L - Reproducibility Documentation

**AI Safeguard Failure Observatory** · Dataset v1.0 · Frozen 2026-09-05

Anyone with Python 3 and the standard scientific stack can regenerate the entire artifact from source
and verify every number in the paper. This document is the runbook.

## Environment

- Python 3.11+ with `pandas`, `numpy`, `matplotlib` (3.10.x used), and the standard library
  (`csv`, `json`). No network access is required to build, validate, analyze, or plot.
- Install: `pip install pandas numpy matplotlib`

## Directory layout

```
observatory/
  scripts/
    build_dataset.py      # source of truth: encodes all 30 QA'd incidents -> CSV + JSON
    validate.py           # integrity + denominator-discipline checks (must PASS)
    analyze.py            # descriptive analysis -> analysis/analysis_results.json
    make_tables.py        # publication tables -> tables/*.md, *.csv
    make_figures.py       # publication figures -> figures/*.png
    select_sample_v2.py   # reproducible selection (seed AISFO-2026-08-24)
  data/                   # generated: 5 CSVs + observatory_dataset.json
  analysis/               # generated: analysis_results.json
  tables/                 # generated: 6 tables (md + csv)
  figures/                # generated: 6 figures (png)
  docs/                   # framework, protocol, manual, dictionary, QA, grounding, refs, this file
  paper/                  # the research paper
```

## Rebuild the whole artifact (deterministic)

```
cd observatory
python3 scripts/build_dataset.py     # -> data/*.csv, data/observatory_dataset.json
python3 scripts/validate.py          # -> must print RESULT: PASS (exit 0)
python3 scripts/analyze.py           # -> analysis/analysis_results.json
python3 scripts/make_tables.py       # -> tables/
python3 scripts/make_figures.py      # -> figures/
```

Expected top-line counts (also asserted by validate.py): **30 incidents, 202 safeguards
(181 incident-time + 21 added-after), 84 relationships, 25 contributing factors, 52 sources.**

## Reproduce the sample selection

```
python3 scripts/select_sample_v2.py   # seed AISFO-2026-08-24 reproduces the locked 30
```

## Provenance and integrity guarantees

- **Single source of truth.** All coded content lives in `build_dataset.py`; the CSV/JSON are
  generated artifacts. To correct a coding, edit `build_dataset.py` and rebuild; never hand-edit the
  generated files.
- **Determinism.** The build and the selection are deterministic; the selection's only stochastic step
  (boundary tie-break) is seeded. Re-running reproduces byte-stable data given the same source.
- **Validation gate.** `validate.py` must pass before the dataset is considered valid; it enforces
  referential integrity, ID uniqueness, controlled vocabularies, and the denominator-contamination
  guards (suspected_absent never Absent; added-after excluded from incident-time; inadequacy_type only
  where Inadequate; factors never safeguards).
- **Denominator discipline in analysis.** `analyze.py` computes state/function/layer distributions on
  incident-time safeguards only and labels every statistic with its denominator, so the paper's numbers
  cannot silently mix units.
- **No fabrication.** No statistic, source, DOI, or incident fact is invented; contested matters are
  coded Disputed or low-confidence. No inter-rater reliability figure is reported because none was
  computed; the per-row evidence_status and confidence fields are the transparency substitute.

## Versioning

The dataset is frozen at **v1.0 (2026-09-05)**. Any change after freeze must (a) bump the version in
`build_dataset.py`, (b) re-pass `validate.py`, and (c) be recorded with a rationale, so that published
numbers remain traceable to a specific dataset version.
