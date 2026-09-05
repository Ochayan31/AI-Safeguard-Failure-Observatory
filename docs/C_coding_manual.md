# Deliverable C - Coding Manual

**AI Safeguard Failure Observatory** · CIR framework v0.3 · Operational guide for coders.

This manual is the teachable procedure for coding an incident into the CIR framework. The full
framework specification is `docs/cir_framework_v0.3.md`; this document is the how-to. A second coder
should be able to reproduce the coding style from this manual plus the framework.

## Step 0 - Eligibility

Admit an incident only if an AI or algorithmic decision system **materially contributed** to a harm,
attempted harm, or credible near-miss. Materially contributed is weaker than "was the primary cause";
the causal weight is coded separately (`ai_causal_contribution`). Exclude incidents with no
algorithmic decision system in the causal chain, even if technology was involved (the exclusion
principle that removes Therac-25 and the 2025 Iberian blackout: classical automation with static
thresholds and no learned or algorithmic *decision* is out of scope).

## Step 1 - Bound the incident

Set `incident_scope` to discrete-event, bounded-episode, or systemic-program. For a systemic program
(for example Robodebt), write an explicit `observation_boundary` stating what is and is not inside the
coded incident, so the program is one incident rather than an unbounded set. Legitimate post-harm
recovery is part of the incident; it is not "added-after."

## Step 2 - Enumerate safeguards

List every control that did, could, or should have borne on the harm. For each, create one
safeguard-interaction row. Code:

- **system_layer** (where it sits): model, application, infrastructure-environment, human-operator,
  organizational-process, external-ecosystem.
- **primary_function** (what job it does): preventive, detective, containment, recovery,
  assurance-governance. One control gets **one row** unless its observed state genuinely diverges by
  context, in which case use a shared `control_group` and one row per divergent state (see e-rater).

## Step 3 - Code the observed state (the core judgment)

Choose exactly one state, assessed by whether the control performed its **intended function**, not
whether a human or system was nominally present ("meaningful engagement").

- **Working** - performed its function.
- **Inadequate** - engaged but insufficient; add `inadequacy_type` (design / operation / enforcement).
- **Failed** - engaged but malfunctioned or produced the wrong output.
- **Bypassed** - present but circumvented, including hollow rubber-stamp review where meaningful
  engagement was structurally prevented (for example a four-second-per-case appeal quota). Merely
  ineffective review is not automatically Bypassed; there must be evidence the review could not
  function.
- **Disabled** - deliberately suppressed, deactivated, or switched off.
- **Absent** - did not exist **and** there is positive evidence it should have (the evidentiary
  fence). If you cannot evidence the absence, code Unknown.
- **Disputed** - authoritative sources genuinely disagree about the state.
- **Unknown** - insufficient evidence. Optionally set `suspected_absent=1`; this is **never** counted
  as Absent.

## Step 4 - Code evidence and causal role

- **evidentiary_basis** (how you know): one or more of direct-artifact, post-incident-finding,
  comparable-system, established-practice, operator-claim, regulation-policy, inferred-indirect,
  research-evidence.
- **evidence_status** (strength): confirmed-authoritative, multiply-reported, single-source-reported,
  inferred-indirect, disputed.
- **causal_role**: primary, contributing, aggravating, mitigating, latent-condition,
  not-causally-relevant, unknown.
- **timeliness**: in-time, delayed, too-late, not-applicable (against the control's own objective).
- **existence_timing**: incident-time or added-after. Added-after rows are excluded from incident-time
  distributions.
- **confidence**: high / medium / low for this row.

## Step 5 - Code relationships

For each meaningful pair of safeguards, add a typed, directed relationship: enabling (one's failure
opens the path for another), masking (one hides another's failure), common-cause (a shared root),
temporal-precedence (sequence only), cascading, or compensating. **Temporal precedence alone never
justifies a causal type.** Set `relationship_confidence`.

## Step 6 - Code contributing factors separately

Conditions that shaped the incident but are not controls (incentive-structure, cultural, economic,
political, organizational, technical, other) go in the contributing-factors table. They are **never**
counted as safeguards.

## Step 7 - Incident-level fields

Code `system_type` (confirmed-ML / probable-ML / algorithmic-nonML / unknown; be honest about whether
ML was actually involved), `era`, `agentic`, `ai_causal_contribution` (causal weight),
`attributed_primary_cause` (where blame landed), `outcome_class` (realized-harm / near-miss / averted),
harms, and `incident_confidence`. Attach at least one primary/authoritative source per incident.

## Non-negotiables

Never invent an incident fact, statistic, source, DOI, or safeguard. Never resolve a genuine dispute;
code it Disputed or low-confidence. Never count suspected_absent as Absent, added-after as
incident-time, or a contributing factor as a safeguard. When in doubt, prefer the more conservative
(less certain) coding and record the uncertainty.
