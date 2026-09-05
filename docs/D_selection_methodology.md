# Deliverable D - Selection Methodology

**AI Safeguard Failure Observatory**

This deliverable is the reproducible account of how the 30 coded incidents were chosen. The full,
dated protocol (with the frozen §11 parameters and amendment log) is
`docs/incident_selection_protocol.md`; the discovery pool is `docs/discovery_pool.md`; the locked
sample and its composition are `docs/selected_sample_final.md`; the selection is executed by
`scripts/select_sample_v2.py` (seed `AISFO-2026-08-24`). This document summarizes the design and its
guarantees.

## Purpose and threat model

The central threat to a study like this is selection favorable to the framework: choosing incidents
because they have rich relational structure, many safeguards, or a satisfying narrative would make the
framework look better than it is. The protocol is built to prevent that, and to be reproducible by an
independent researcher.

## Design

1. **Discovery pool separate from coded sample.** A fixed-source sweep produced 108 candidate
   incidents. This pool is documented and frozen before selection so the sampling frame is inspectable.

2. **Eligibility screen.** Candidates without an AI or algorithmic decision system in the causal chain
   are removed with a recorded reason. Eight were excluded at screen.

3. **Frozen "Hybrid E then R" selection rule.** Within predefined strata, eligible cases are ranked by
   a pre-specified evidence-quality rubric, and the highest-ranked are taken up to each stratum's
   quota. Where cases tie at the selection boundary, a seeded random draw (seed `AISFO-2026-08-24`)
   breaks the tie reproducibly. The evidence-quality rubric is explicitly barred from incorporating
   whether a case appears interesting, supports CIR, contains many safeguards, or supports any
   anticipated finding. Selection occurs before any outcome or relational analysis.

4. **Anti-cherry-picking floors and caps** (frozen in §11): at least 8 omission-dominated cases (so
   the sample cannot consist only of relationally rich cases), at least 5 generative-era cases, at
   least 2 agentic cases, per-domain cap of 5, and a documentation-tier cap. The locked sample
   satisfies all of them.

5. **Full exclusion accounting.** The 8 screen exclusions (with reasons) and 70 excluded-but-eligible
   cases are recorded in the script output, so what was left out, and why, is auditable.

## The one amendment and the one swap

A dated amendment added a mechanism/recency floor to ensure generative and agentic coverage; it moved
the omission-dominated composition from 19/30 to 17/30 by adding active-failure agentic cases, a small
and declared shift. Separately, during coding, one selected case (the 2025 Iberian blackout) was found
ineligible on close research and was deterministically replaced by re-running the selection script with
it marked ineligible; the backfill was Amazon Q and all other 29 selections held. This is an
eligibility correction, not a re-selection, and is the only change to the locked sample. Both events
are logged.

## Reconciliation note (post-freeze audit)

The pre-freeze selection notes recorded the generative/recency-era count as 7. In the frozen v1.0
dataset the `era=genai` count is **8**, because the Mobley v. Workday incident (2023-2025) was assigned
the generative-era paradigm tag at the coding stage, after selection. This is a coding-stage
classification, not a change to which cases were selected; the frozen dataset (era=genai = 8) is
authoritative, the research paper reports 8, and every recency floor (>=5) is satisfied under either
count. Recorded here for full traceability.

## Reproducibility

Re-running `scripts/select_sample_v2.py` with the same seed reproduces the locked 30 exactly. The
sampling frame, rubric, floors, caps, seed, exclusions, amendment, and swap are all documented, so the
selection is reproducible and its biases (documentation skew, uncovered domains) are declared rather
than hidden. Those biases are restated as limitations in the paper (Section 7).
