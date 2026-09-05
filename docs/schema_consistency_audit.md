# AI Safeguard Failure Observatory
## Schema Consistency Audit (pre-v0.2 gate)

**Document:** `schema_consistency_audit.md`
**Purpose:** Before writing v0.2, audit every field across all four tables. For each field: (1) analytical purpose, (2) how it is distinct from fields it could be confused with, (3) allowable values, (4) whether and how it can affect quantitative analysis. Then resolve the overlap clusters that the added fields create.
**Result headline:** The schema is consistent and ready for a v0.2 write-up, with four overlap risks that this audit resolves by rule (Section 5) and three fields whose quantitative use must be constrained (flagged **[Q-guard]**). No field was found redundant; two fields were found to need explicit "do not double-count" rules.

A note on the fourth column. "Affects quantitative analysis?" is answered in one of four ways, because not every column is a variable:
- **Metric** — a coded categorical/boolean variable that distributions, counts, or cross-tabs are computed over. These are the fields Phase 3 actually analyzes.
- **Filter** — used to include/exclude or stratify rows before computing a metric, but not itself the headline variable.
- **Qualifier** — modifies how another field is counted (e.g., caps, or "primary only"). Can distort metrics if misused, hence the [Q-guard] flags.
- **Non-metric** — identifier, free text, or provenance. Never counted directly.

---

## 1. Table INCIDENTS — field audit

| Field | Analytical purpose | Distinct from | Allowable values | Quant. role |
|---|---|---|---|---|
| `incident_id` | Primary key; join target for the other three tables. | Not a variable. | Stable slug, unique, never reused. | Non-metric |
| `title` | Human label. | — | Free text. | Non-metric |
| `domain` | Sector context; enables cross-domain pattern analysis. | Not `harm_type` (domain = where it happened; harm_type = what kind of harm). | Controlled vocab 1.4.1 (single-valued). | **Metric** (cross-domain distributions) |
| `date_start` / `date_end` | Temporal placement; enables trend-over-time analysis. | Not `existence_timing` (that is per-safeguard). | ISO date or year. | Filter (era stratification) |
| `incident_scope` | Records whether the row is a discrete event, a bounded episode, or a systemic program, so coarse-grained rows are flagged. | Not `outcome_class`. Scope = granularity of the unit; outcome = whether harm realized. | {discrete-event, bounded-episode, systemic-program}. | **Filter [Q-guard]** — see G-5: program-level rows must be separable in any per-incident count, because one systemic row is not comparable to one discrete event. |
| `observation_boundary` | For bounded-episode and systemic-program rows, states explicitly what is inside and outside the coded scope (time window, population, subsystems). Prevents silent scope drift. | Not `summary` (summary describes; boundary delimits). | Free text; **required** when scope ∈ {bounded-episode, systemic-program}, else null. | Non-metric (but governs metric validity) |
| `summary` | Neutral factual description. | — | Prose ≤150 words. | Non-metric |
| `chronology` | Ordered, source-tagged events; the substrate for relationship coding. | Not `relationships` table (chronology = raw events; relationships = coded links between safeguards). | Ordered list, each event source-tagged. | Non-metric |
| `harm_type_primary` | The principal kind of harm. | Not `domain`. | Controlled vocab 1.4.2 (single). | **Metric** |
| `harm_type_secondary` | Additional co-occurring harms (multi-harm sociotechnical cases). | Same vocab as primary but multi. | Vocab 1.4.2 (multi, optional). | **Metric [Q-guard]** — G-3: headline harm distribution counts `harm_type_primary` only; secondary reported as a separate enrichment, never added into the primary tally. |
| `outcome_class` | Which arm of the eligibility gate (realized / attempted / near-miss). | Not `ai_causal_contribution`. | {realized-harm, attempted-harm, near-miss}. | **Metric** |
| `ai_system_role` | What the AI actually did. | Prose context for the two causal fields below. | Free text. | Non-metric |
| `system_type` | Records ML-ness as a coded variable rather than an eligibility gate (your F-5 decision). Enables the robustness check "do findings hold for confirmed-ML only?" | Not `domain`. | {confirmed-ML, probable-ML, algorithmic-nonML, unknown}. | **Metric / Filter** |
| `ai_causal_contribution` | The analyst's apportionment of how much the AI system contributed to the harm. | See G-2. Distinct from `attributed_primary_cause` (official blame) and from safeguard-level `causal_role`. | {sole-cause, major-contributor, minor-contributor, contributory-non-necessary, disputed, unknown}. | **Metric** |
| `ai_causal_contribution_basis` | Justification + sources for the above. | Provenance, not a variable. | Free text + refs. | Non-metric |
| `attributed_primary_cause` | What the authoritative/official finding blamed as primary cause (may differ from our reading). Enables the "attribution divergence" analysis. | See G-2. This is *reported external attribution*, not our judgment. | Short category or text (e.g., "human operator", "organizational", "AI system", "external actor", "none/unresolved"). | **Metric** (divergence analysis) |
| `attributed_primary_cause_source` | Which authority made that attribution. | Provenance. | Ref. | Non-metric |
| `primary_sources` / `supporting_sources` | Evidentiary backing. | Provenance. | Citations. | Non-metric |
| `incident_confidence` | Overall certainty in the incident-level facts. | Distinct from per-cell `confidence` in safeguard rows (this one is incident-wide). | {high, medium, low}. | Filter (sensitivity analysis) |
| `notes` | Coder notes, open questions. | — | Free text. | Non-metric |
| `coder_id` / `coding_date` / `dataset_version` | Provenance and versioning; enables inter-rater work. | — | String / date / version tag. | Filter (inter-rater subsets) |

---

## 2. Table SAFEGUARD_INTERACTIONS — field audit

| Field | Analytical purpose | Distinct from | Allowable values | Quant. role |
|---|---|---|---|---|
| `interaction_id` | Primary key; endpoint for relationships. | — | Unique. | Non-metric |
| `incident_id` | FK to incidents. | — | FK. | Non-metric (join) |
| `control_group` | Links rows that are the SAME physical control split because their state diverged across functions (amendment A1). Lets you count at the control level, not just the interaction level. | Not `incident_id`. control_group ⊂ incident. | Nullable group id. | **Qualifier [Q-guard]** — G-6: control-level counts must dedupe by `control_group`; interaction-level counts do not. State which you are reporting. |
| `safeguard_name` | The control, named specifically; normalized against the glossary. | — | Short string. | Filter (grouping like controls) |
| `safeguard_description` | Intended function of this control. | — | Prose. | Non-metric |
| `system_layer_primary` | Where the control sits; enables layer distributions. | Not `control_function` (layer = where; function = what defensive role). | Vocab 1.4.4 (single). | **Metric** |
| `system_layer_secondary` | Additional layer(s) when a control genuinely spans (Uber Volvo AEB). | Same vocab, multi. | Vocab 1.4.4 (multi, optional). | **Metric [Q-guard]** — G-3: headline layer distribution counts primary only. |
| `primary_function` | The control's principal defensive role. | Not `causal_role` (function = designed intent; role = what actually happened causally). | {preventive, detective, containment, recovery}. | **Metric** |
| `secondary_functions` | Additional functions the same control serves (amendment A1). | Same set, multi. | {preventive, detective, containment, recovery} (multi, optional). | **Metric [Q-guard]** — G-3. |
| `observed_state` | The condition of the control in this incident. The core dependent variable of the whole project. | See G-1 (state vs role vs timeliness) and G-4 (Disabled/Bypassed/Inadequate/Absent boundaries). | {Working, Absent, Inadequate, Bypassed, Disabled, Failed, Disputed, Unknown}. | **Metric** (the headline distribution) |
| `inadequacy_type` | When state = Inadequate, which kind: bad design, not operated, or unenforced. | Sub-qualifier of `observed_state`; only meaningful when Inadequate. | {design, operation, enforcement, unknown}; null otherwise. | **Metric** (conditional on Inadequate) |
| `suspected_absent` | Boolean flag allowing the coder to record "I suspect this was missing but cannot meet the Absent evidentiary bar." Only meaningful when state = Unknown. | Not `observed_state = Absent`. See G-7. | boolean; only true when state = Unknown. | **Qualifier [Q-guard]** — G-7: **prohibited** from being counted as Absent in any prevalence/distribution. May be reported only as its own separately-labeled "suspected-absent" count. |
| `timeliness` | When the control acted relative to its own objective; rescues "worked but far too late." | Not `observed_state` (state = did it function; timeliness = did it function in time). Not `existence_timing` (that = when the control came into existence). See G-1. | {in-time, delayed, too-late, not-applicable}. Assessed relative to the safeguard's objective. | **Metric** |
| `evidentiary_basis` | The TYPE of grounds for the coded state; gates the Absent rule. | See G-8 (evidence trio). | Multi-select vocab 1.4.5. | Filter / **Metric** (basis-mix reporting) |
| `evidence_status` | The CORROBORATION level of those grounds. | See G-8. | Vocab 1.4.6. | Filter / **Metric** |
| `causal_role` | The role this control's state played in THIS incident's harm. | See G-1 and G-2. | Vocab 1.4.7. | **Metric** |
| `existence_timing` | Whether the control existed at incident time or was added afterward. Excludes remediation from incident-time distributions. | Renamed from `temporal_state`. Not `timeliness`. See G-9. | {incident-time, added-after}. Legitimate post-harm recovery that existed at incident time is `incident-time`, NOT `added-after`. | **Filter [Q-guard]** — G-9: incident-time distributions exclude `added-after` rows. |
| `confidence` | Coder's certainty in THIS cell's coding. | See G-8. Subject to caps (v0.1 §1.3.9). | {high, medium, low}. | Filter / Qualifier (confidence-weighted or -filtered analyses) |
| `source_refs` | Sources for this specific row. | Provenance. | Citations. | Non-metric |
| `coder_notes` | Reasoning, alternatives considered. | — | Free text. | Non-metric |

---

## 3. Table RELATIONSHIPS — field audit

| Field | Analytical purpose | Distinct from | Allowable values | Quant. role |
|---|---|---|---|---|
| `relationship_id` | Primary key. | — | Unique. | Non-metric |
| `incident_id` | FK; both endpoints must share it. | — | FK. | Non-metric |
| `from_interaction_id` / `to_interaction_id` | The directed pair of safeguard interactions linked. | — | FKs to safeguard_interactions. | Non-metric (structure) |
| `relationship_type` | The nature of the link; the carrier of CIR's relational claim. Ordered weakest→strongest. | — | {temporal-precedence, enabling, masking, compensating, common-cause, causal, unknown}. | **Metric** (pathway analysis) |
| `relationship_confidence` | Certainty in the link itself, independent of endpoint confidence. Enforces amendment A2. | Distinct from endpoints' `confidence`. | {high, medium, low}. | Filter / Qualifier |
| `basis` | Why this link and this type (A2 requires mechanism evidence for anything above temporal-precedence). | Provenance + rule-enforcement. | Free text + refs. | Non-metric |

---

## 4. Table CONTRIBUTING_FACTORS (new) — field audit

Purpose of the table: hold non-safeguard factors that actively drove or amplified harm (counterproductive incentives, cultural/economic/political conditions), so they are recorded without contaminating safeguard distributions. **Rows here are never counted in any safeguard-state distribution (G-10).**

| Field | Analytical purpose | Distinct from | Allowable values | Quant. role |
|---|---|---|---|---|
| `factor_id` | Primary key. | — | Unique. | Non-metric |
| `incident_id` | FK. | — | FK. | Non-metric |
| `factor_name` | The factor, named. | Not a `safeguard_name`; this is not a control. | Short string. | Filter |
| `factor_description` | What it was and how it drove harm. | — | Prose. | Non-metric |
| `factor_type` | Category of factor. | Distinct from safeguard `observed_state`; a factor has no "state," it has a type and a direction. | {incentive-structure, cultural, economic, political, counterproductive-control, other}. | **Metric** (factor-type distribution, reported separately) |
| `effect_direction` | How it bore on harm. | Not `causal_role` alone; this says harm-ward direction. | {harm-causing, harm-amplifying, harm-enabling}. | **Metric** (separate) |
| `system_layer_primary` (+ secondary optional) | Where the factor sits. | Same vocab as safeguards for cross-referencing. | Vocab 1.4.4. | **Metric** (separate) |
| `causal_role` | Role in the harm. | Reuses the safeguard vocab for consistency, but computed in a separate table. | Vocab 1.4.7. | **Metric** (separate) |
| `evidentiary_basis` / `evidence_status` / `confidence` | Same three-layer evidence model as safeguards. | See G-8. | As per safeguards. | Filter |
| `source_refs` / `notes` | Provenance. | — | Citations / text. | Non-metric |

---

## 5. Overlap resolution rules (the reason for the audit)

These are the collisions the new fields create, each resolved by an explicit rule that goes into the v0.2 coding manual.

**G-1 — The three independent axes of a safeguard: STATE, ROLE, TIMELINESS.** These are orthogonal and must never be conflated.
- `observed_state` = *what condition was the control in?* (Working, Absent, Disabled, …)
- `causal_role` = *what did that condition contribute to the harm?* (primary, mitigating, latent-condition, …)
- `timeliness` = *did it act in time relative to its objective?* (in-time, too-late, …)
A control can be Working + mitigating + too-late (the Dutch DPA), or Absent + latent-condition + not-applicable (a missing pre-deployment check). Coders fill all three independently. **Rule:** never infer one from another.

**G-2 — The three causal fields, at two different scopes.** Confusion here would corrupt every causal metric.
- `ai_causal_contribution` (incident scope, our judgment): how much the AI system contributed.
- `attributed_primary_cause` (incident scope, external report): what the authority blamed.
- `causal_role` (safeguard scope): what one specific control's state contributed.
**Rule:** the two incident-level fields are answered once per incident; `causal_role` is answered once per safeguard row. The "attribution divergence" metric is defined as cases where `ai_causal_contribution ∈ {sole, major}` but `attributed_primary_cause ≠ AI system`, and vice versa.

**G-3 — Primary/secondary multi-valued fields must not double-count.** Applies to `harm_type`, `system_layer`, and `secondary_functions`. **Rule:** every headline distribution counts the PRIMARY value only, so each row contributes exactly once. Secondary values are reported as a separate, clearly-labeled "also-present" enrichment and are never summed into the primary tally. This preserves "one row, one vote" in the core metrics.

**G-4 — The Absent / Disabled / Bypassed / Inadequate / Failed boundary.** The most error-prone decision. Decision order (also encoded in the v0.2 decision tree):
1. Did the control exist at incident time? If **no** → Absent (if the evidentiary-basis rule is met) or Unknown (if not).
2. If it existed: was it deliberately turned off / suppressed by the operator or system design? → **Disabled**.
3. If it was on: was it engaged/exercised in the incident at all?
   - If it was **not meaningfully engaged** because it was circumvented, routed around, overridden, or structurally prevented from functioning (no information, no authority, no time) → **Bypassed**.
   - If it **was genuinely engaged** but its design or standard was too weak to help → **Inadequate** (set `inadequacy_type`).
   - If it was supposed to act and simply did not fire / errored → **Failed**.
4. If quality sources actively disagree among the above → **Disputed**. If evidence is merely thin → **Unknown**.
**Your F-11 modification, encoded:** ineffective human review is NOT automatically Bypassed. The test is engagement. A reviewer who could not interrogate a black-box score was structurally prevented from functioning → Bypassed. A reviewer who had the information and authority but applied a weak standard → Inadequate. The decision tree asks "was the control put in a position where it could function?" before choosing.

**G-5 — Systemic rows are not unit-comparable to discrete rows.** A `systemic-program` incident aggregates what might be thousands of episodes. **Rule:** any per-incident count must be reported with scope held constant or explicitly stratified by `incident_scope`; never mix a systemic-program row and a discrete-event row in the same "one incident = one data point" claim without saying so. Every bounded-episode and systemic-program row carries an `observation_boundary`.

**G-6 — Control-level vs interaction-level counts.** Because A1 can split one control into multiple rows on state divergence, there are two legitimate denominators. **Rule:** state which you are using. "Distribution of safeguard states" is an *interaction-level* count (each row votes). "How many distinct controls were absent" is a *control-level* count (dedupe by `control_group`). Both are valid; labeling is mandatory.

**G-7 — `suspected_absent` is quarantined from Absent.** **Rule:** in any prevalence or distribution of Absent, `suspected_absent = true` rows (whose `observed_state` is Unknown) are NOT counted as Absent. They may appear only in a separately-labeled "suspected-absent" figure. This preserves the integrity of the Absent evidentiary-basis rule while capturing the analyst's signal.

**G-8 — The evidence trio stays three fields (re-affirmed).** `evidentiary_basis` = kind of grounds; `evidence_status` = corroboration level; `confidence` = resulting certainty. The pilot (P3) confirmed they carry independent information. **Rule:** do not collapse; confidence caps (v0.1 §1.3.9) still apply.

**G-9 — `existence_timing` ≠ `timeliness`.** Existence timing asks whether the control came into being before or after the incident (remediation filter). Timeliness asks, for a control that existed, whether it acted in time. A recovery control that existed at incident time but acted years later is `existence_timing = incident-time` + `timeliness = too-late`, and is INCLUDED in incident-time distributions. Only `added-after` (genuinely new post-incident controls) are excluded. **Rule (your #8 modification):** legitimate post-harm recovery is never coded `added-after`.

**G-10 — Contributing factors never enter safeguard metrics.** **Rule:** the `contributing_factors` table is analyzed on its own. No factor row is ever counted in an `observed_state`, `control_function`, or `system_layer` distribution over safeguards. Cross-references between a factor and a safeguard (e.g., the Dutch cost-recovery incentive → absent proportionality control) are expressed as prose or, if needed later, a typed cross-table link (deferred).

---

## 6. Audit conclusions

1. **No redundant fields.** Every field has a distinct analytical purpose. The closest pairs (`existence_timing`/`timeliness`, the three causal fields, the evidence trio) are genuinely orthogonal and now have explicit separation rules (G-1, G-2, G-8, G-9).
2. **Three fields need quantitative guards** so they cannot silently distort metrics: `suspected_absent` (G-7), the primary/secondary multi-values (G-3), and `incident_scope` (G-5). All are flagged [Q-guard] above and carry a rule.
3. **Two denominators now exist** (interaction-level and control-level); every reported count must name which (G-6).
4. **The new `contributing_factors` table is quarantined** from safeguard metrics (G-10), which is the whole reason it is a separate table rather than a new state.
5. **`observed_state` remains the single headline dependent variable**, now with eight values; `Disabled` and the engagement-based Bypassed/Inadequate split (G-4) are the substantive changes and are the ones most in need of a worked manual example, which v0.2 will provide.

Ready to write v0.2.
