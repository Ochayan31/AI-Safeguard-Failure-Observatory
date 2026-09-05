# AI Safeguard Failure Observatory

**A relational dataset of how AI and algorithmic safeguards fail, coded across 30 real-world
incidents (2010-2025).**

Dataset v1.0 · Frozen 2026-09-05 · Exploratory descriptive study (n = 30) · Not statistically
representative.

## What this is

Most AI-risk discussion asks whether a system failed. This project asks what happened to the
*safeguards* that were supposed to prevent the harm. For 30 incidents spanning autonomous vehicles,
welfare automation, healthcare, criminal justice, chatbots, agentic LLM tools, finance, hiring, and
more, every identifiable safeguard is coded as a structured interaction (its system layer, control
function, observed state at incident time, the evidence behind that coding, and its causal role),
along with the typed relationships between safeguards. The dataset is the artifact; the paper is
generated from it.

## Headline findings (each with its denominator)

- **75.7%** of the 181 incident-time safeguards were non-functional; only **20.4%** were Working.
- Of the Working safeguards, **70.3%** sat in the **external-ecosystem** layer (press, regulators,
  courts, researchers), not inside the operator's own controls.
- **Prevention** was the most-**Absent** function; **governance**, when present, was most often
  **Inadequate** rather than missing.
- In **11 of 30** incidents a **detective control was Working at incident time yet harm still
  occurred**: within this sample, detection was frequently insufficient to prevent harm where
  downstream escalation, intervention, and authority-to-act were weak.
- Failures were **multi-safeguard** (mean 2.8 typed relationships/incident, all ≥2); the dominant
  relationship was **enabling** (58.3%), the data-level signature of Swiss-cheese hole alignment.
- Primary responsibility was attributed to **organizational** causes in **18/30** incidents, to the
  AI system itself in only **2**.
- The newest generative/agentic systems (8/30) fail mostly along **old fault lines**, with **indirect
  prompt injection** as the clearest new attack surface (and LLM confabulation a second candidate).

## Contents

| Path | What |
|---|---|
| `data/` | The machine-readable dataset: 5 CSVs + `observatory_dataset.json` (deliverable A) |
| `docs/B_data_dictionary.md` | Every field, its values, purpose, and denominator rules |
| `docs/C_coding_manual.md` | The teachable coding procedure (framework: `cir_framework_v0.3.md`) |
| `docs/D_selection_methodology.md` | How the 30 were chosen (protocol: `incident_selection_protocol.md`) |
| `docs/E_qa_report.md` | Integrity validation + resolution of the 12 flagged calls |
| `docs/I_technical_grounding.md` | Findings mapped to safety-science and AI-safety literature |
| `docs/K_references.md` | 24 verified references |
| `docs/L_reproducibility.md` | Runbook to rebuild and verify everything |
| `docs/N_final_integrity_audit.md` | Independent clean-room audit of every number and inference (deliverable N) |
| `analysis/analysis_results.json` | All computed statistics (deliverable F) |
| `tables/` | 6 publication tables, md + csv (deliverable G) |
| `figures/` | 6 publication figures, png (deliverable H) |
| `paper/J_research_paper.md` | The full research paper (deliverable J) |
| `scripts/` | `build_dataset.py`, `validate.py`, `analyze.py`, `make_tables.py`, `make_figures.py`, `audit_independent.py`, `select_sample_v2.py` |

## Reproduce it

```
cd observatory
python3 scripts/build_dataset.py && python3 scripts/validate.py && \
python3 scripts/analyze.py && python3 scripts/make_tables.py && python3 scripts/make_figures.py
```

`validate.py` must print `RESULT: PASS`. See `docs/L_reproducibility.md`.

## How to read the numbers honestly

n = 30, selected on the occurrence of realized harm or credible near-miss. Nothing here is
representative of AI systems in general, and some distributions (for example zero Working preventive
controls) are partly a property of selecting on harm. Every claim carries its denominator and unit of
analysis. Contested and unresolved cases are coded Disputed or at low confidence, not adjudicated. The
artifact is released for scrutiny, correction, and extension.

## Integrity

No incident fact, statistic, source, DOI, or safeguard is invented anywhere in this project. The only
synthetic content is one clearly labeled worked example in the framework document. No inter-rater
reliability figure is reported because none was computed; per-row `evidence_status` and `confidence`
are the transparency substitute.
