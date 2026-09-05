# AI Safeguard Failure Observatory
## The CIR Coding Framework, Version 0.3

**Document:** `cir_framework_v0.2.md`
**Supersedes:** `cir_framework_v0.2.md`
**Companions:** `pilot_coding_report.md` (the stress-test that motivated these changes), `schema_consistency_audit.md` (the pre-write field audit whose rules G-1..G-10 are embedded here).
**Status:** Framework accepted for the pilot-plus-amendments stage. This is the living source of truth. The 20-to-30 incident collection may begin against this version once you have reviewed it. Deferred items (Appendix D) remain open.

CIR = **Control-Incident-Relationship**: the safeguard interactions (controls), the incident that contains them, and the typed relationships between them, now with a fourth table for non-safeguard contributing factors.

---

## CHANGELOG (v0.1 → v0.2)

| # | Change | Origin |
|---|---|---|
| A1 | Multi-function controls: one control = one row, with `primary_function` + `secondary_functions`; split only on state divergence, linked by `control_group`. | Your instruction |
| A2 | Temporal precedence alone cannot justify a stronger relationship type; `causal` requires a source asserting mechanism. | Your instruction |
| C1 | Eligibility no longer gates on ML. Added `system_type` {confirmed-ML, probable-ML, algorithmic-nonML, unknown}. Scope = ML plus algorithmic decision systems. | Pilot F-5 |
| C2 | Added `observed_state = Disabled` (existed and functional but deliberately turned off/suppressed). | Pilot F-2 |
| C3 | Added `timeliness` {in-time, delayed, too-late, not-applicable}, assessed against the safeguard's objective. | Pilot F-14 |
| C4 | Added optional `inadequacy_type` {design, operation, enforcement, unknown}, only when state = Inadequate. | Pilot F-3/F-4 |
| C5 | New `contributing_factors` table for counterproductive/anti-safeguard factors; excluded from all safeguard distributions. | Pilot F-12 |
| C6 | Split `ai_causal_contribution` from `attributed_primary_cause`. | Pilot F-1 |
| C7 | Added `incident_scope` {discrete-event, bounded-episode, systemic-program} and required `observation_boundary` for bounded/systemic rows. | Pilot F-7 |
| C8 | Renamed `temporal_state` → `existence_timing` {incident-time, added-after}; legitimate post-harm recovery stays incident-time. | Pilot F-16 |
| C9 | Added `suspected_absent` boolean (only with state = Unknown), prohibited from being counted as Absent. | Pilot F-17/F-18 |
| C10 | `harm_type` and `system_layer` become primary + secondary (multi), counted primary-only in headline metrics. | Pilot F-6/F-8 |
| C11 | Redefined `Bypassed` to include structurally-prevented (not-meaningfully-engaged) controls, with an engagement test separating it from `Inadequate`. | Pilot F-11 |
| C12 (v0.3) | **Promoted `assurance-governance` to a fifth `control_function` value.** Re-coded the 3 affected controls (Cruise disclosure, Air Canada accountability defense, Dutch pilot accountability). | Recurred in 3 of the first 8 coded incidents (pilot + batch 1); within the "revisit after 5–10 incidents" window. |
| — | Deferred (unchanged): `joint-omission` relationship type, `asserted-rejected` accountability state. Revisit after more incidents. | Pilot F-15/F-19 |

Re-coding impact: the three pilot incidents (P1–P3) were coded against interim states and must be re-coded against v0.2 before any of them enters a released dataset. No released data exists yet, so impact is limited to the pilot.

Editorial clarification (post-review, no version bump): the engagement test now carries the sentence "Meaningful engagement refers to the safeguard performing its intended decision, detection, or mitigation function, not merely to a human or system nominally processing the case" in both §1.3.3 and §1.9.

---

# PART 0 — PROJECT DEFINITION

## 0.1 Research question
Unchanged from v0.1. Primary: when AI or algorithmic decision systems are involved in real-world harms, attempted harms, or credible near-misses, how do the safeguards intended to prevent, detect, contain, or recover from those harms behave, and what does explicitly representing the interaction between safeguards and the incident reveal that flat incident taxonomies do not? Secondary questions on state distributions, recurring pathways, and the loss of relational information under flat taxonomies are unchanged.

## 0.2 What counts as a safeguard failure
Unchanged in substance. A safeguard is any mechanism, technical or organizational, intended to prevent, detect, contain, or recover from a class of harm involving an AI or algorithmic system. A safeguard is in a failure state when its `observed_state` is one of Absent, Inadequate, Bypassed, Disabled, or Failed. Working controls are still coded, because "the control that held" is evidence.

## 0.3 Inclusion and exclusion criteria
**Eligibility gate (v0.2):**
- **(E1) Material contribution.** An AI or **algorithmic decision** system materially contributed to the harm, attempted harm, or credible near-miss. (Scope broadened per C1; ML-ness is now recorded in `system_type`, not gated.)
- **(E2) At least one codeable safeguard interaction**, with a defensible basis (including a defensible Absent under the evidentiary-basis rule, or an honest Unknown).

Inclusion also requires a public primary source, a bounded-or-explicitly-delimited episode (see `incident_scope` and `observation_boundary`), and datability to at least a year. Exclusions (hypotheticals, non-algorithmic "AI in name only," uncorroborated single-claim episodes that cannot exceed Unknown, pure benchmark underperformance, duplicates) are logged in `excluded_log` with the failed criterion.

**Scope decision (C1), recorded:** the Observatory covers ML systems **and** algorithmic decision systems. `system_type` carries the distinction so that any finding can be re-run on confirmed-ML rows only. This mirrors the project's house pattern: let a contested boundary into the dataset as a recorded variable rather than a doorman.

## 0.4 Unit of analysis: four tables
- **INCIDENTS** — one row per incident.
- **SAFEGUARD_INTERACTIONS** — one row per (incident, safeguard).
- **RELATIONSHIPS** — one row per directed link between two safeguard interactions in the same incident.
- **CONTRIBUTING_FACTORS** — one row per non-safeguard factor that actively drove or amplified harm. Analyzed separately; never mixed into safeguard metrics (rule G-10).

## 0.5 Target size
20 to 30 incidents. Intermediate counts are not completion.

## 0.6 Scope lock (v0.2)
Fixed until amended via 0.7: the eligibility gate; the four-table architecture; the `observed_state` vocabulary (eight values); the Absent evidentiary-basis rule; the A2 relationship rule; the primary-only headline counting rule (G-3); the quarantine of `contributing_factors` and `suspected_absent` from safeguard/Absent metrics (G-10, G-7); target size.

## 0.7 Amendment rule
Any change to a scope-locked item is recorded in the CHANGELOG with date, change, reason, and re-coding impact.

---

# PART 1 — THE FRAMEWORK

## 1.1 Architecture

```
INCIDENTS (1 per incident)
   incident_id ─┬───────────────┬──────────────────┐
                │ 1─to─many     │ 1─to─many        │ 1─to─many
   SAFEGUARD_INTERACTIONS   CONTRIBUTING_FACTORS   (chronology is in-row)
   interaction_id ─┐
                   │ pairs within an incident
   RELATIONSHIPS (from_interaction_id → to_interaction_id)
```

## 1.2 INCIDENTS — schema

`incident_id` [req, key]; `title` [req]; `domain` [req, vocab 1.4.1, single]; `date_start`/`date_end` [req]; `incident_scope` [req, {discrete-event, bounded-episode, systemic-program}]; `observation_boundary` [req when scope ∈ {bounded-episode, systemic-program}, else optional]; `summary` [req, ≤150w]; `chronology` [req, source-tagged events]; `harm_type_primary` [req, vocab 1.4.2]; `harm_type_secondary` [opt, vocab 1.4.2, multi]; `outcome_class` [req, {realized-harm, attempted-harm, near-miss}]; `ai_system_role` [req]; `system_type` [req, {confirmed-ML, probable-ML, algorithmic-nonML, unknown}]; `ai_causal_contribution` [req, vocab 1.4.3]; `ai_causal_contribution_basis` [req]; `attributed_primary_cause` [req, {AI-system, human-operator, organizational, external-actor, multiple, none-unresolved, unknown}]; `attributed_primary_cause_source` [req if a cause is named]; `primary_sources` [req]; `supporting_sources` [opt]; `incident_confidence` [req, {high, medium, low}]; `notes` [opt]; `coder_id` [req]; `coding_date` [req]; `dataset_version` [req].

**`observation_boundary` (C7).** For any bounded-episode or systemic-program incident, state explicitly what is inside and outside the coded scope: the time window, the population/subsystem, and what was deliberately excluded. This prevents silent scope drift and makes systemic rows honestly comparable only to each other (rule G-5).

## 1.3 SAFEGUARD_INTERACTIONS — schema and field rules

`interaction_id` [req, key]; `incident_id` [req, FK]; `control_group` [opt, links state-divergent rows of one control]; `safeguard_name` [req]; `safeguard_description` [req]; `system_layer_primary` [req, vocab 1.4.4]; `system_layer_secondary` [opt, vocab 1.4.4, multi]; `primary_function` [req, {preventive, detective, containment, recovery, assurance-governance}]; `secondary_functions` [opt, same set, multi]; `observed_state` [req, vocab 1.4.5]; `inadequacy_type` [req iff state = Inadequate, {design, operation, enforcement, unknown}]; `suspected_absent` [opt boolean, true only when state = Unknown]; `timeliness` [req, {in-time, delayed, too-late, not-applicable}]; `evidentiary_basis` [req, vocab 1.4.6, multi]; `evidence_status` [req, vocab 1.4.7]; `causal_role` [req, vocab 1.4.8]; `existence_timing` [req, {incident-time, added-after}]; `confidence` [req, {high, medium, low}]; `source_refs` [req]; `coder_notes` [opt].

### 1.3.1 The three orthogonal axes (rule G-1)
`observed_state` (what condition the control was in), `causal_role` (what that condition contributed to the harm), and `timeliness` (whether it acted in time) are independent. Never infer one from another. A control can be Working + mitigating + too-late; or Absent + latent-condition + not-applicable.

### 1.3.2 `observed_state` — the eight values
- **Working** — existed and functioned as intended (may have limited harm).
- **Absent** — a control that could reasonably be expected did not exist. **Gated** by the evidentiary-basis rule (1.3.4).
- **Inadequate** — existed, was genuinely engaged, but its design or standard was too weak. Set `inadequacy_type`.
- **Bypassed** — existed and was on, but was **not meaningfully engaged**: circumvented, routed around, overridden, or **structurally prevented from functioning** (denied information, authority, or time). (C11)
- **Disabled** — existed and was functional but was **deliberately turned off or suppressed** by the operator or system design. (C2)
- **Failed** — existed, was supposed to act, and did not fire or errored.
- **Disputed** — quality sources actively disagree among the above.
- **Unknown** — state cannot be determined. The honest default when nothing better is supported. May carry `suspected_absent = true`.

### 1.3.3 The Absent / Disabled / Bypassed / Inadequate / Failed decision order (rule G-4)
1. Did the control exist at incident time? If no → **Absent** (if evidentiary basis met) or **Unknown** (if not; may set `suspected_absent`).
2. If it existed: deliberately turned off/suppressed by operator or design? → **Disabled**.
3. If it was on: **was it put in a position where it could function, and was it genuinely engaged?**
   - Not meaningfully engaged (circumvented, overridden, or structurally prevented: no info/authority/time) → **Bypassed**.
   - Genuinely engaged but too weak by design/standard → **Inadequate** (+ `inadequacy_type`).
   - Supposed to act but did not fire / errored → **Failed**.
4. Sources actively disagree → **Disputed**. Evidence merely thin → **Unknown**.

**The engagement test (your F-11 modification).** Ineffective human review is NOT automatically Bypassed. Ask first: *could the control function, and was it engaged?* A reviewer denied the information to interrogate a black-box score was structurally prevented → Bypassed. A reviewer with full information and authority who applied a weak standard → Inadequate. This single question is the fork. **Meaningful engagement refers to the safeguard performing its intended decision, detection, or mitigation function, not merely to a human or system nominally processing the case.**

### 1.3.4 The Absent evidentiary-basis rule (unchanged, load-bearing)
Code Absent only if at least one defensible basis supports the expectation it should have existed: regulation/policy, explicit operator/developer claim, established practice at the time, presence in a comparable system, authoritative post-incident finding, or strong research evidence. Otherwise code **Unknown** (optionally `suspected_absent = true`). `suspected_absent` is never counted as Absent in any distribution (rule G-7).

### 1.3.5 `timeliness` (C3)
Assessed relative to the safeguard's own objective. `in-time` = acted early enough to prevent/contain/recover as intended; `delayed` = acted but late enough to reduce its value; `too-late` = acted after the harm was substantially done; `not-applicable` = timing is meaningless for this state (e.g., Absent controls). Distinct from `existence_timing` (rule G-9).

### 1.3.6 `existence_timing` (C8)
`incident-time` = the control existed (or was expected) at incident time, **including recovery controls that legitimately act after the harm**. `added-after` = a genuinely new control introduced in response to the incident. Only `added-after` rows are excluded from incident-time distributions (rule G-9). Legitimate post-harm recovery is never `added-after`.

### 1.3.7 Multi-function and multi-layer (A1, C10, rule G-3)
One control = one row. `primary_function`/`secondary_functions` and `system_layer_primary`/`system_layer_secondary` capture multiplicity. Headline distributions count the **primary** value only (one row, one vote); secondaries are a separate enrichment. Split a control into multiple rows **only** when its `observed_state` genuinely differs across functions; link those rows by `control_group` and dedupe by it for control-level counts (rule G-6).

### 1.3.8 The evidence trio (rule G-8, unchanged)
`evidentiary_basis` = kind of grounds (multi); `evidence_status` = corroboration level; `confidence` = resulting certainty (with caps from v0.1 §1.3.9: single non-authoritative source caps at medium; Absent resting only on "established practice" caps at medium).

## 1.4 Controlled vocabularies

- **1.4.1 `domain`:** healthcare-clinical, finance-trading, finance-consumer, autonomous-vehicle, robotics-industrial, consumer-chatbot, enterprise-agent, content-moderation, hiring-HR, criminal-justice, government-benefits, security-cyber, scientific-research, education, other.
- **1.4.2 `harm_type`:** physical-safety, financial-loss, information-integrity, privacy-data, rights-discrimination, security-compromise, environmental, psychological-social, other.
- **1.4.3 `ai_causal_contribution`:** sole-cause, major-contributor, minor-contributor, contributory-non-necessary, disputed, unknown.
- **1.4.4 `system_layer`:** model, application, infrastructure-environment, human-operator, organizational-process, external-ecosystem. (Definitions unchanged from v0.1.)
- **1.4.4b `control_function`:** preventive (stop the harm occurring), detective (notice it going wrong), containment (limit blast radius once wrong), recovery (restore a safe state after harm), **assurance-governance** (assure/govern the sociotechnical system rather than act on the harm directly: disclosure and transparency to oversight, accountability and responsibility mechanisms, audits, evaluations, red-teaming, governance sign-off). Assurance-governance controls typically fail by omission (no audit), evasion (denied accountability), or deception (withheld disclosure). Added v0.3 (C12).
- **1.4.5 `observed_state`:** Working, Absent, Inadequate, Bypassed, Disabled, Failed, Disputed, Unknown.
- **1.4.6 `evidentiary_basis`** (multi): regulation-policy, operator-claim, established-practice, comparable-system, post-incident-finding, research-evidence, direct-artifact.
- **1.4.7 `evidence_status`:** confirmed-authoritative, multiply-reported, single-source-reported, inferred-indirect, disputed, unknown.
- **1.4.8 `causal_role`:** primary, contributing, latent-condition, aggravating, mitigating, not-causally-relevant, unknown.
- **1.4.9 `relationship_type`:** temporal-precedence, enabling, masking, compensating, common-cause, causal, unknown.
- **1.4.10 `system_type`:** confirmed-ML, probable-ML, algorithmic-nonML, unknown.
- **1.4.11 `inadequacy_type`:** design, operation, enforcement, unknown.
- **1.4.12 `incident_scope`:** discrete-event, bounded-episode, systemic-program.
- **1.4.13 `attributed_primary_cause`:** AI-system, human-operator, organizational, external-actor, multiple, none-unresolved, unknown.
- **1.4.14 `factor_type`:** incentive-structure, cultural, economic, political, counterproductive-control, other.
- **1.4.15 `effect_direction`:** harm-causing, harm-amplifying, harm-enabling.

Every categorical field permits `other`/`unknown`; repeated `other` values signal a needed vocabulary revision (log it).

## 1.5 RELATIONSHIPS — schema and the A2 rule

`relationship_id` [req, key]; `incident_id` [req, FK]; `from_interaction_id` [req, FK]; `to_interaction_id` [req, FK]; `relationship_type` [req, vocab 1.4.9]; `relationship_confidence` [req, {high, medium, low}]; `basis` [req].

**Types, weakest to strongest:** temporal-precedence (order only, no causal claim; the humble default), enabling (A's state created the precondition for B), masking (A hid/suppressed B), compensating (B was the designed backstop for A), common-cause (shared upstream cause), causal (A's state directly caused B's), unknown.

**A2 rule (enforced).** Observed ordering justifies at most `temporal-precedence`. Any stronger type requires affirmative mechanism evidence beyond the ordering. `causal` additionally requires a source that asserts the mechanism, not merely the sequence. `relationship_confidence` is independent of the endpoints' confidence.

## 1.6 CONTRIBUTING_FACTORS — schema (C5, new)

Purpose: record non-safeguard factors that actively drove or amplified harm, without contaminating safeguard metrics.

`factor_id` [req, key]; `incident_id` [req, FK]; `factor_name` [req]; `factor_description` [req]; `factor_type` [req, vocab 1.4.14]; `effect_direction` [req, vocab 1.4.15]; `system_layer_primary` [req, vocab 1.4.4]; `system_layer_secondary` [opt, multi]; `causal_role` [req, vocab 1.4.8]; `evidentiary_basis` [req, multi]; `evidence_status` [req]; `confidence` [req]; `source_refs` [req]; `notes` [opt].

**Rule G-10.** No factor row is ever counted in a safeguard `observed_state`, `control_function`, or `system_layer` distribution. Factor-type and effect-direction distributions are reported separately. A factor→safeguard connection (e.g., a cost-recovery incentive driving an absent proportionality control) is expressed in prose for now; a typed cross-table link is deferred.

## 1.7 Dataset hygiene (Phase 1C)
Standardize `safeguard_name` against the glossary; no blanks (Unknown, never empty); duplicate incidents merged and logged; contradiction checks, now including: `observed_state = Absent` with `existence_timing = added-after` (contradiction); `suspected_absent = true` with `observed_state ≠ Unknown` (contradiction); `inadequacy_type` set with `observed_state ≠ Inadequate` (contradiction); `timeliness ≠ not-applicable` on an Absent row (review); a `contributing_factors` row that is actually a safeguard (re-file). Every row carries `dataset_version`.

## 1.8 Coding decision tree (v0.2)

**Stage A — Eligibility.** (1) AI/algorithmic system materially contributed to a harm/attempt/near-miss? (2) At least one codeable safeguard (defensible Absent or honest Unknown)? (3) Primary source exists? (4) Duplicate? Merge:log. Otherwise create the incident row and set `incident_scope`; if bounded/systemic, write `observation_boundary`.

**Stage B — Incident-level.** Fill identity, chronology, harm types (primary + any secondary), outcome, `ai_system_role`, `system_type`, `ai_causal_contribution` (+ basis), and `attributed_primary_cause` (+ source). Note where the two causal fields diverge. Set `incident_confidence`.

**Stage C — Enumerate safeguards** across all six layers, including working controls.

**Stage D — Per safeguard.** (1) Name + describe. (2) `system_layer_primary` (+secondary), `primary_function` (+secondary). (3) `observed_state` via the G-4 decision order (existence → Disabled? → engagement test: Bypassed vs Inadequate vs Failed → Disputed/Unknown). If Inadequate, set `inadequacy_type`. If Unknown, consider `suspected_absent`. (4) `timeliness` relative to the objective. (5) `evidentiary_basis`, then `evidence_status`. (6) `causal_role`. (7) `existence_timing` (recovery acting post-harm is still incident-time). (8) `confidence` with caps. (9) `source_refs`. If `observed_state` genuinely differs across this control's functions, split into rows sharing a `control_group`.

**Stage E — Contributing factors.** Record any non-safeguard factor that drove/amplified harm in the CONTRIBUTING_FACTORS table. Do not put these in the safeguard table.

**Stage F — Relationships.** For each warranted directed pair, create a relationship row; default `temporal-precedence`; upgrade only with mechanism evidence (A2). Set `relationship_confidence` independently.

**Stage G — Integrity.** Remove unsourced claims; run hygiene/contradiction checks; confirm every required field is filled (Unknown where honest); confirm no factor leaked into the safeguard table and no `suspected_absent` is being read as Absent.

## 1.9 Manual: the decisions most likely to split coders

1. **Bypassed vs Inadequate (the engagement test, G-4/C11).** *Could the control function and was it engaged?* Structurally prevented → Bypassed. Engaged but weak → Inadequate. Worked example: a black-box risk score handed to a caseworker with no ability to interrogate it → the human-review control is **Bypassed** (structurally prevented), not Inadequate. Meaningful engagement refers to the safeguard performing its intended decision, detection, or mitigation function, not merely to a human or system nominally processing the case.
2. **Disabled vs Bypassed (C2; Batch-1 calibration decision, 2026-08-24).** Disabled = the operator/own-design turned it off **or suppressed/deactivated its protective effect, even where the control nominally produced an output**. Bypassed = a control that was NOT itself deliberately suppressed was circumvented, overridden, or structurally prevented from functioning (e.g., denied information). Worked examples: a factory automatic-braking system automatically deactivated under experimental computer control → **Disabled**; internal legal/safety advice that was produced and then suppressed or omitted so it could not protect → **Disabled** (its protective effect was deactivated by the operator); an external oversight body defeated by being fed false information → **Bypassed** (structurally prevented, not self-suppressed). The line: Disabled = you neutralize your *own* safeguard's effect; Bypassed = *another* control is circumvented or denied the ability to function.
3. **Absent vs Unknown + suspected_absent (1.3.4/G-7).** No defensible basis that it should have existed → Unknown, optionally `suspected_absent`. Worked example: an output-grounding check on a chatbot whose architecture is undocumented → **Unknown** with `suspected_absent = true`; never counted as Absent.
4. **existence_timing vs timeliness (G-9).** A regulator that existed all along but acted years late → `existence_timing = incident-time`, `timeliness = too-late`, included in incident-time metrics. A spend cap added the week after → `existence_timing = added-after`, excluded.
5. **Safeguard vs contributing factor (G-10).** If the item's purpose was to reduce harm, it is a safeguard (code its state). If it had no protective purpose and instead drove harm (a cost-recovery quota), it is a contributing factor (separate table).

## 1.10 Worked example (illustrative, synthetic, NOT a dataset entry)
The same refund-agent sketch as v0.1 §1.8, updated for v0.2 states. Key deltas: the missing per-transaction cap → **Absent** (basis: comparable-system) with `timeliness = not-applicable`; a filter the operator switched off for latency → **Disabled**; a fraud-review queue the agent's speed outran so no human ever saw the transactions → **Bypassed** (structurally prevented, engagement test), not Inadequate; the post-incident spend cap → `existence_timing = added-after`, excluded from incident-time metrics; a cost-per-refund incentive that discouraged holds → a CONTRIBUTING_FACTORS row (`factor_type = incentive-structure`, `effect_direction = harm-enabling`), never in the safeguard distribution. This synthetic example is the only invented content in the project.

---

## Appendix A — CSV headers (four tables)

**incidents:** `incident_id, title, domain, date_start, date_end, incident_scope, observation_boundary, summary, chronology, harm_type_primary, harm_type_secondary, outcome_class, ai_system_role, system_type, ai_causal_contribution, ai_causal_contribution_basis, attributed_primary_cause, attributed_primary_cause_source, primary_sources, supporting_sources, incident_confidence, notes, coder_id, coding_date, dataset_version`

**safeguard_interactions:** `interaction_id, incident_id, control_group, safeguard_name, safeguard_description, system_layer_primary, system_layer_secondary, primary_function, secondary_functions, observed_state, inadequacy_type, suspected_absent, timeliness, evidentiary_basis, evidence_status, causal_role, existence_timing, confidence, source_refs, coder_notes`

**relationships:** `relationship_id, incident_id, from_interaction_id, to_interaction_id, relationship_type, relationship_confidence, basis`

**contributing_factors:** `factor_id, incident_id, factor_name, factor_description, factor_type, effect_direction, system_layer_primary, system_layer_secondary, causal_role, evidentiary_basis, evidence_status, confidence, source_refs, notes`

## Appendix B — Quantitative guards (from the audit)
- **G-3:** headline harm/layer/function distributions count PRIMARY values only.
- **G-5:** never mix `systemic-program` and `discrete-event` rows in one "per incident" claim without stratifying by `incident_scope`.
- **G-6:** label every count as interaction-level or control-level (dedupe by `control_group` for the latter).
- **G-7:** `suspected_absent` is never counted as Absent.
- **G-9:** incident-time distributions exclude `added-after` only.
- **G-10:** contributing factors never enter safeguard distributions.

## Appendix C — Integrity commitments
No invented statistics; no fabricated incidents or facts (the only synthetic content is §1.10); proposed validation labeled proposed until run; uncertainty represented explicitly (Unknown, Disputed, suspected_absent, confidence, evidence_status, relationship_confidence); every schema change logged with re-coding impact.

## Appendix D — Deferred open issues (revisit after 5–10 more incidents)
1. ~~Assurance/governance as a fifth `control_function` (F-13).~~ **PROMOTED in v0.3 (C12)** — now the fifth `control_function` value; no longer deferred.
2. `joint-omission` relationship type for linking co-absent controls (F-15), given the absence-dominated-graph finding.
3. `asserted-rejected` accountability state for adjudicated defenses (F-19).
4. `inadequacy_type` value `latent-condition` overlap with `causal_role = latent-condition` — watch for confusion in coding.
5. Typed factor→safeguard cross-table link (currently prose only).
6. Whether the absence-dominated-graph finding warrants an explicit selection policy for Phase 1B (open question you raised; affects collection, not schema).
