# Deliverable B - Data Dictionary

**AI Safeguard Failure Observatory** · Dataset v1.0 · Frozen 2026-09-05

The dataset is a relational set of five CSV tables (also bundled as one JSON,
`data/observatory_dataset.json`). The keys join as: `incidents.incident_id` is the
parent; `safeguards`, `relationships`, `contributing_factors`, and `sources` each carry
`incident_id` as a foreign key. Relationship rows additionally reference safeguard rows
by their `interaction_id` (`from_interaction` / `to_interaction`).

Every quantitative field notes its **analytical purpose** and, where relevant, the
**denominator discipline** that governs its use, so that no field is silently double-counted.

---

## Table 1 - `incidents.csv` (n=30; unit = incident)

| field | type | allowed values / format | purpose |
|---|---|---|---|
| incident_id | string (PK) | slug, e.g. `2023-cruise-drag-sf` | unique incident key |
| title | string | free text | human-readable incident name |
| domain | enum | autonomous-vehicle, government-benefits, healthcare, consumer-chatbot, enterprise-agent, criminal-justice, content-moderation, education, environmental, finance-trading, security-cyber, hiring-HR, other | sector; supports per-domain caps and stratification |
| domain_detail | string | free text (optional) | sub-sector detail |
| date_start / date_end | date | YYYY or YYYY-MM-DD | incident temporal extent |
| incident_scope | enum | discrete-event, bounded-episode, systemic-program | bounds the unit; a systemic program is one incident, not many |
| observation_boundary | string | free text (required for systemic-program) | states exactly what is and is not inside the coded incident |
| harm_primary / harm_secondary | enum | physical-safety, financial-loss, psychological-social, rights-liberty, health-clinical, environmental, security-breach, discrimination, other | harm typing |
| outcome_class | enum | realized-harm, near-miss, averted | realized vs. potential harm; **near-miss reported separately** from realized harm |
| system_type | enum | confirmed-ML, probable-ML, algorithmic-nonML, unknown | epistemic honesty about whether ML was actually involved |
| era | enum | legacy, genai | generative/LLM/agentic-paradigm system (predominantly 2022+), assigned by system paradigm not calendar date alone; e.g. two 2023 autonomous-vehicle incidents are `legacy` because they are not generative/agentic systems |
| agentic | bool | 0/1 | autonomous tool-use system |
| ai_causal_contribution | enum | major-contributor, contributory-non-necessary, minor, disputed, none, unknown | the AI/algorithmic system's causal weight, **coded separately from blame** |
| attributed_primary_cause | enum | AI-system, human-operator, organizational, external, multiple, disputed, unknown | where primary responsibility was attributed by authoritative sources |
| incident_confidence | enum | high, medium, low | overall evidentiary confidence in the incident coding |
| n_safeguards | int | derived | count of safeguard rows for the incident |
| dataset_version | string | v1.0 | provenance stamp |

---

## Table 2 - `safeguards.csv` (202 rows; unit = safeguard-interaction)

| field | type | allowed values | purpose / denominator note |
|---|---|---|---|
| interaction_id | string (PK) | `<incident_id>::S<n>` | unique safeguard-interaction key |
| incident_id | string (FK) | → incidents | parent incident |
| local_sid | string | `S1`, `S2`, … | within-incident id (relationship endpoints) |
| name | string | free text | the safeguard/control described |
| system_layer | enum | model, application, infrastructure-environment, human-operator, organizational-process, external-ecosystem | *where* the control sits |
| primary_function | enum | preventive, detective, containment, recovery, assurance-governance | *what job* the control does. **One control = one row** unless its state diverges by context |
| secondary_functions | string | (rarely used) | secondary role, not counted in the primary-function distribution |
| observed_state | enum | Working, Absent, Inadequate, Bypassed, Disabled, Failed, Disputed, Unknown | the core outcome variable (see §Vocabulary below) |
| inadequacy_type | enum | design, operation, enforcement, unknown, (blank) | present **only** when observed_state=Inadequate |
| suspected_absent | bool | 0/1 | may be 1 **only** when observed_state=Unknown; **never counted as Absent** |
| timeliness | enum | in-time, delayed, too-late, not-applicable | assessed against the control's own objective |
| evidentiary_basis | string | semicolon-joined tokens: direct-artifact, post-incident-finding, comparable-system, established-practice, operator-claim, regulation-policy, inferred-indirect, research-evidence | *how we know* what the state was |
| evidence_status | enum | confirmed-authoritative, multiply-reported, single-source-reported, inferred-indirect, disputed | strength/quality of the evidence |
| causal_role | enum | primary, contributing, aggravating, mitigating, latent-condition, not-causally-relevant, unknown | the control's role in the causal story |
| existence_timing | enum | incident-time, added-after | **incident-time is the denominator** for state/function/layer distributions; added-after excluded |
| confidence | enum | high, medium, low | confidence in this row's coding |
| control_group | string | free text (optional) | groups rows that are the same control coded across diverging contexts |

---

## Table 3 - `relationships.csv` (84 rows; unit = directed relationship)

| field | type | allowed values | purpose |
|---|---|---|---|
| relationship_id | string (PK) | `<incident_id>::R<n>` | unique key |
| incident_id | string (FK) | → incidents | parent incident |
| from_interaction / to_interaction | string (FK) | → safeguards.interaction_id | directed endpoints (same incident) |
| relationship_type | enum | enabling, masking, temporal-precedence, common-cause, cascading, compensating | the typed relationship. **temporal-precedence encodes sequence only, never causation** |
| relationship_confidence | enum | high, medium, low | confidence in the relationship claim |

---

## Table 4 - `contributing_factors.csv` (25 rows; unit = contributing factor)

Contributing factors are conditions that shaped the incident but are **not safeguards**. They are
kept in a separate table and **never enter safeguard distributions.**

| field | type | allowed values | purpose |
|---|---|---|---|
| factor_id | string (PK) | `<incident_id>::F<n>` | unique key |
| incident_id | string (FK) | → incidents | parent incident |
| name | string | free text | the factor |
| factor_type | enum | incentive-structure, cultural, economic, political, organizational, technical, other | typing |
| effect_direction | enum | increased-harm, increased-risk, reduced-harm, mixed, unclear | how the factor bore on the outcome |
| causal_role | enum | (as safeguards) | role in the causal story |
| confidence | enum | high, medium, low | confidence |

---

## Table 5 - `sources.csv` (52 rows; unit = source)

| field | type | purpose |
|---|---|---|
| source_id | string (PK) | unique key |
| incident_id | string (FK) | parent incident |
| url | string | locator (primary/authoritative material) |
| title | string | source title |
| source_tier | string | e.g. official-investigation, regulator, court, peer-reviewed, investigative-journalism |

---

## Controlled vocabulary - `observed_state` (the core variable)

- **Working** - the safeguard performed its intended decision/detection/mitigation function.
- **Inadequate** - present and engaged but insufficient (qualify with inadequacy_type:
  design / operation / enforcement).
- **Failed** - present and engaged but did not perform (malfunction or wrong output).
- **Bypassed** - present but circumvented, including *hollow/rubber-stamp* human review where
  meaningful engagement was structurally prevented. Ineffective review is not automatically Bypassed.
- **Disabled** - deliberately suppressed, deactivated, or switched off.
- **Absent** - did not exist, **and there is positive evidence it should have** (the evidentiary
  fence). Where absence cannot be evidenced, code Unknown (optionally suspected_absent=1).
- **Disputed** - authoritative sources genuinely disagree about the state.
- **Unknown** - insufficient evidence to code a state.

**"Meaningful engagement"** refers to the safeguard performing its intended decision, detection, or
mitigation function, not merely to a human or system nominally processing the case.
