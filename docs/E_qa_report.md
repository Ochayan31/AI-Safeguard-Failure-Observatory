# Deliverable E - Coding QA Report

**AI Safeguard Failure Observatory**
Dataset version: v1.0 · Frozen: 2026-09-05 · Unit of analysis: incident (n=30)

This report documents the quality-assurance pass performed on the 30 coded incidents
before the dataset was frozen. It covers (1) automated integrity validation, (2) resolution
of the twelve coding calls flagged for scrutiny, (3) the Batch-1 calibration decisions applied
consistently across the sample, and (4) residual limitations carried forward honestly into the
paper. No incident facts, statistics, sources, or scores were invented at any point; where
evidence was insufficient, the coding records uncertainty rather than resolving it.

## 1. Automated integrity validation (`scripts/validate.py`)

The frozen dataset passes all structural and denominator-discipline checks with **0 errors,
0 warnings**:

- **Referential integrity** - every safeguard, relationship, contributing-factor and source
  row resolves to a real incident_id; every relationship endpoint resolves to a real safeguard
  within the same incident.
- **ID uniqueness** - no duplicate interaction_id, relationship_id, factor_id, source_id, or
  incident_id.
- **Controlled vocabulary** - every categorical field value is drawn from its CIR v0.3 vocabulary
  (observed_state, primary_function, system_layer, system_type, timeliness, inadequacy_type,
  existence_timing, evidence_status, confidence, causal_role, relationship_type, and the
  incident-level fields).
- **Denominator-contamination guards** - `suspected_absent=1` occurs only where
  `observed_state=Unknown` (5 rows, never counted as Absent); `inadequacy_type` is present only
  where `observed_state=Inadequate`; `existence_timing=added-after` rows (21) are flagged for
  exclusion from all incident-time distributions.
- **control_group integrity** - no control_group spans more than one incident.
- **Cardinality** - CSV counts match the combined JSON.

Totals: **30 incidents, 202 safeguard-interaction rows (181 incident-time + 21 added-after),
84 relationships, 25 contributing factors, 52 sources.**

## 2. Resolution of the twelve flagged coding calls

Each call from the pre-freeze review index was re-examined against its primary source and the
frozen framework. Dispositions:

1. **COMPAS system_type.** Confirmed **algorithmic-nonML** (the Northpointe/equivant model is a
   statistical instrument, not learned ML in the modern sense) and **observed_state = Disputed**
   on the fairness constraint, with `ai_causal_contribution = disputed`. This is the dataset's
   single showcase Disputed and is retained deliberately, grounded in the genuine ProPublica /
   Dressel-Farid / Flores-et-al dispute over what "fair" means. *Kept.*
2. **IBM Watson for Oncology.** `outcome_class` retained at the **incident level as realized-harm**
   (organizational and reputational harm plus unsafe recommendations surfaced internally), while
   the **patient-level** exposure is coded as a near-miss because physician oversight remained
   Working. The two levels are recorded distinctly. *Kept.*
3. **Facebook Files (Instagram).** `ai_causal_contribution = contributory-non-necessary` retained;
   the evidence is largely internal self-report and correlational, which does not support the
   stronger major-contributor claim. *Kept (conservative).*
4. **Raine v. OpenAI and Mobley v. Workday.** Both coded conservatively: everything ALLEGED,
   `confidence = low`, `evidence_status = disputed`, `ai_causal_contribution = disputed`. These are
   active/unresolved matters; the coding does not adjudicate them. *Kept (conservative).*
5. **Gemini image generation.** The diversity-tuning intervention is coded as a **safeguard that
   Failed** (a preventive/assurance control that over-corrected), not as a contributing factor.
   This is a deliberate, documented modelling choice: an over-firing safeguard is still a safeguard
   interacting with the incident. *Kept.*
6. **Rotterdam vs. Toeslagen human review.** Rotterdam S3 = **Inadequate (operation) + disputed
   evidence**; Toeslagen review = **Bypassed**. The contrast is deliberate and evidence-driven
   (Toeslagen reviewers were more clearly denied the information needed to review; Rotterdam
   reviewers were nominally present but ineffective). *Kept.*
7. **C101 excluded, C104 backfilled.** The 2025 Iberian blackout was excluded at coding as
   ineligible (conventional grid-engineering/voltage failure with only classical protective-relay
   automation and no AI/ML or algorithmic *decision* system; E1 fail). Per the frozen rule,
   `select_sample_v2.py` was re-run with C101 marked ineligible and C104 (Amazon Q) deterministically
   backfilled; all other 29 held. *Confirmed - one clean, logged swap.*
8. **Recurrence pairs kept separate.** Two Tesla Autopilot fatalities and two Dutch welfare
   programs are coded as distinct incidents rather than merged, because recurrence is itself a
   finding about safeguard persistence. *Kept.*
9. **assurance-governance boundary.** The fifth control function carries ~30 incident-time rows
   (disclosure, validation, certification, testing standards, impact assessment, expert review). Its
   boundary with the organizational-process *layer* holds: function describes what the control is
   for; layer describes where it sits. *Kept, boundary verified.*
10. **Disabled.** Applied only where deliberate suppression/deactivation is evidenced (Boeing AoA
    alert and MCAS disclosure; Robodebt ×2; MiDAS ×1). Not conflated with Absent (never existed) or
    Bypassed (present but circumvented). *Kept, rule reads consistently.*
11. **e-rater control_group split.** Human oversight coded twice under one shared control_group
    (Working in high-stakes essay scoring / Absent where the machine is sole scorer) to represent
    genuine state divergence of the *same* control across contexts. *Kept.*
12. **Near-miss outcomes.** EchoLeak and Amazon Q coded `outcome_class = near-miss`; the
    Watson patient-level near-miss is recorded within an incident whose overall class is realized-harm.
    Near-misses are reported separately from realized harms in the analysis. *Kept.*

## 3. Batch-1 calibration decisions (applied sample-wide)

- **Robodebt S2 = Disabled** (not Bypassed) where suppression/deactivation of the safeguard is
  evidenced.
- **Robodebt S4 merged into S3** where they represent one underlying control rather than two.

Both were locked as Batch-1 conventions and applied consistently to all later incidents. They were
not reopened, per instruction, because no later evidence showed the rules themselves to be defective.

## 4. Residual limitations carried into the paper

- **Selection on realized harm** makes some distributions partly tautological (e.g., no preventive
  control is coded Working at incident time - in a sample of incidents where harm occurred,
  prevention by definition did not fully hold). The paper states this explicitly and does not treat
  it as a discovered effect.
- **Documentation skew** toward institutionally investigated harms remains, partly offset by the
  recency/generative-era floor.
- **Two failure-mode operationalizations** exist and are kept distinct: the selection-time
  "dominant failure mode" label (descriptive composition) and the analysis-time "omission-dominated"
  measure (Absent is the top non-Working state in the incident). They are reported separately and
  never conflated.
- **Sub-judice cases** (Raine, Workday) are coded at low confidence and disputed status; their
  values should be read as provisional.

**QA result: PASS.** The dataset is internally consistent, denominator-clean, conservatively coded,
and frozen at v1.0.
