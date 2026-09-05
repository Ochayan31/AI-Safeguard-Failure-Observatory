# AI Safeguard Failure Observatory
## Incident Selection Protocol (Phase 1B gate)

**Document:** `incident_selection_protocol.md`
**Status:** FROZEN (approved by David, 2026-08-24). Parameters are locked in Section 11. Any later change is a dated amendment with a reason, per the framework CHANGELOG discipline. This document is now part of the published methodology.
**Companions:** `cir_framework_v0.2.md` (the coding framework), `pilot_coding_report.md` (source of the selection-tension problem this protocol addresses).

---

## 0. The problem this protocol exists to solve

The pilot established an uncomfortable fact: CIR's relational machinery reconstructs more structure for active-failure incidents (Uber) than for omission-dominated ones (the Dutch scandal). That creates a specific, insidious bias risk. If the researcher, even unconsciously, gravitates toward cases that "code nicely," the dataset fills with CIR-favorable incidents, the analysis then shows CIR performing well, and the demonstration is circular: the method looks good because the cases were chosen to make it look good. A reviewer who spots this discredits the entire contribution, and they would be right to.

The defense is not willpower. You cannot reliably out-discipline your own preferences by trying hard. The defense is a **procedure that removes the degrees of freedom through which preference operates**, and that makes every selection decision auditable by someone else. That is what this protocol is.

A single organizing principle runs through all of it: **selection must be blind to CIR-favorability.** No case is ever included or excluded because of how much relational structure it will yield, how cleanly it demonstrates CIR's advantage, or how it will look in the paper. Every rule below is a mechanism for enforcing that blindness.

---

## 1. Three distinct populations (requirement 6)

Keeping these separate is the backbone of the protocol. Conflating them is how cherry-picking hides.

- **Discovery pool** — every candidate incident found through the systematic source sweep (Section 3), recorded before any judgment about suitability. Target size: **at least 3× the final sample**, i.e. **60–90 candidates**. Discovery entries are cheap (a few fields); coding is expensive, so we discover abundantly and code selectively.
- **Eligible pool** — the subset of the discovery pool that passes the CIR-blind eligibility screen (Section 4). Binary, mechanical, no taste.
- **Final coded sample** — the 20–30 incidents drawn from the eligible pool by the pre-registered stratified procedure (Sections 5–6). These are the only incidents that get fully coded.

Every candidate has a `candidate_id` and lives in a log for its whole life, so the path from "found" to "coded or excluded, and why" is fully traceable.

---

## 2. Pre-registration (requirements 4, 5)

Before any collection begins, the following are frozen and dated in this document: the source list (Section 3), the eligibility screen (Section 4), the stratification dimensions and their caps and floors (Section 5), the within-stratum selection rule (Section 6), and the exclusion taxonomy (Section 7).

**Why this reduces bias:** pre-registration removes hindsight. You cannot retrofit a rule to admit a favorite case if the rules were fixed and dated before you saw the cases. Any deviation from the pre-registered rules during collection must be logged as a dated amendment with a reason, exactly like the framework CHANGELOG. This converts "I changed my mind about what counts" from an invisible act into a visible, criticizable one.

Optional strengthening: register the frozen protocol externally (e.g., an OSF timestamped page or a git tag/commit hash in the public repo) so the freeze date is independently verifiable. Recommended but not required; the git commit hash of this file at freeze time is the lightweight version.

---

## 3. Systematic discovery (requirements 3, 5)

Discovery is source-driven, not memory-driven. We enumerate a fixed set of sources and sweep each, rather than adding whatever incidents we happen to recall (which is itself a bias, toward famous cases). Proposed source set:

- **Established incident repositories:** the AI Incident Database (AIID), the AIAAIC repository, the OECD AI Incidents Monitor. (For cross-referencing taxonomies, the MIT AI Risk Repository.)
- **Official and legal records:** national safety boards (e.g., NTSB), data-protection authorities, court and tribunal decisions, parliamentary and regulatory inquiries.
- **Academic surveys** of AI incidents and harms (used to find cases and their primary sources, not as primary sources themselves).
- **Reputable journalism**, used only to locate candidates whose primary sources are then retrieved.

For every candidate a source sweep surfaces that plausibly meets the eligibility gate, we create a discovery-log row **before** forming any opinion about its CIR value:

`candidate_id, discovery_source, one_line_description, domain_guess, system_type_guess, provisional_dominant_failure_mode, primary_source_found (y/n), discovery_date`

**Why this reduces bias:** a fixed source list makes the discovery step reproducible (another researcher sweeping the same sources finds substantially the same pool) and stops the pool from skewing toward whatever the researcher already admires. Recording candidates before judging them means the pool is not pre-filtered by preference.

**Silent-cap honesty:** if any source is only partially swept (e.g., we take the first N results of a large repository), the log records exactly what was and was not covered, so the coverage boundary is explicit rather than passed off as exhaustive.

---

## 4. Eligibility screen (CIR-blind) (requirements 2, 7)

Each discovery-pool candidate is screened against the v0.2 eligibility gate, mechanically:

- E1: an AI or algorithmic decision system materially contributed to a harm, attempted harm, or credible near-miss.
- E2: at least one relevant safeguard is codeable (defensible Absent, or honest Unknown).
- A public primary source exists.
- The episode is bounded or explicitly delimitable (`incident_scope` + `observation_boundary` can be set).
- Datable to at least a year.

The screen is binary. Its result and reason are written to the log. **CIR-favorability is not a screening criterion and must not enter here.** A case with rich relational structure and a case that is a single flat omission both pass or fail on the gate alone.

**Why this reduces bias:** separating a mechanical eligibility gate from any suitability judgment means cases are admitted for meeting objective criteria, not for being interesting. It also produces the exclusion record (Section 7) as a byproduct.

---

## 5. Stratification: forcing in variation and the CIR-unfavorable cases (requirements 1, 3, 4)

This is the heart of the anti-bias design. We do not select 20–30 cases freely from the eligible pool; we fill **pre-declared strata with caps and floors**, so the sample's shape is set by policy before selection, not by preference during it.

Stratification dimensions and their rules (proposed; exact numbers are the main thing for you to approve):

- **Domain (spread + cap).** Aim for coverage across sectors; **cap any single domain at ~4–5** of the final sample, so no familiar domain (autonomous vehicles, chatbots) dominates.
- **System type (representation).** Ensure all of `confirmed-ML`, `probable-ML`, and `algorithmic-nonML` appear; **no more than ~60%** of the sample may be any single system_type, so the dataset is not secretly "just LLM chatbots."
- **Dominant safeguard-failure mode (the critical one).** Classify each eligible case, from its primary source, as **active-failure-dominated** (controls existed and were bypassed/failed/disabled) or **omission-dominated** (controls largely absent). Set a **floor of at least ~8 omission-dominated incidents** in the final 20–30. This is the mechanism that directly defeats the selection tension: the protocol *forces in* the cases that make CIR look worse, so their inclusion is not left to a researcher who is (consciously or not) rewarded for excluding them.
- **Evidence quality (range, with a floor).** Include both high-evidence cases (authoritative post-incident findings) and thinner but primary-sourced cases, so the dataset is not composed only of pristine NTSB-grade investigations (which would bias toward a particular kind of well-scrutinized incident). The primary-source requirement remains a hard floor; "thinner" never means "unsourced."
- **Temporal and geographic spread (soft).** Prefer a spread across years and jurisdictions where the other strata allow, to avoid an all-recent, all-US dataset.

**Why this reduces bias:** quotas convert selection from an additive act of preference ("which cases do I want in?") into a subtractive act under constraint ("this stratum needs three more omission-dominated, algorithmic-nonML cases; which eligible candidates fill it?"). The floor on omission-dominated cases is the single most important line in this document, because it removes the exact freedom the selection tension exploits.

---

## 6. Within-stratum selection: closing the last degree of freedom (requirements 2, 4)

When a stratum has more eligible candidates than its quota, preference could still creep in at the final pick. We remove it with a **neutral, reproducible selection rule** applied within each stratum. Two candidate rules (you choose one at approval):

- **Rule R (seeded random draw):** from the eligible candidates in a stratum, draw the quota at random using a pre-declared seed. Maximally bias-free; fully reproducible from the seed; but may discard a better-documented case in favor of a thinner one.
- **Rule E (evidence-quality ranking):** rank the stratum's eligible candidates by a **CIR-neutral** documentation-quality score (number and authority of primary sources, completeness of the public record) and take the top of the quota. Favors codability without favoring CIR structure; deterministic and reproducible; but "quality" scoring has mild subjectivity.

**FROZEN — Hybrid E→R (tie-breaker form).** Within each predefined stratum, rank the eligible cases using the pre-specified evidence-quality rubric (Section 6.1). Select the highest-ranked cases up to the stratum quota. Where cases are tied at the selection boundary (equal rubric score straddling the quota cutoff), break the tie with a reproducible seeded random draw. We record: the seed, the full eligible discovery pool, the selected cases, and the excluded-but-eligible cases. The evidence-quality score must NOT incorporate whether a case appears interesting, supports CIR, contains many safeguards, or supports any anticipated finding. Selection occurs before any outcome analysis.

### 6.1 The evidence-quality rubric (CIR-neutral, fixed in advance)
Each eligible case scores 0–3 on each of four axes; the sum (0–12) is its documentation-quality score. None of these axes references CIR structure, safeguard count, or expected findings.
- **Source authority (0–3):** highest available source tier. 3 = official investigation / court or tribunal decision / regulator finding; 2 = first-party postmortem or disclosure; 1 = investigative journalism with original evidence; 0 = only secondary coverage.
- **Corroboration (0–3):** number of independent primary or authoritative sources. 3 = three or more; 2 = two; 1 = one; 0 = none that qualify (would fail eligibility anyway).
- **Record completeness (0–3):** how fully the public record supports coding. 3 = chronology plus explicit safeguard/decision detail; 2 = chronology plus partial detail; 1 = outcome documented but mechanism thin; 0 = outcome only.
- **Verifiability (0–3):** how checkable the facts are by another researcher. 3 = primary documents publicly retrievable; 2 = retrievable with effort; 1 = paywalled/archival; 0 = referenced but not retrievable.

Ties at the boundary are decided by seeded random draw, not by re-scoring on any CIR-related quality.

**Why this reduces bias:** whichever rule, the final pick within a stratum is made by a mechanism, not by taste, and can be re-derived by another researcher (from the seed, or from the rubric). Taste has no remaining place to operate.

---

## 7. Exclusion recording (requirement 7)

Nothing is ever silently dropped. Every discovery-pool candidate that does not reach the final sample gets an exclusion-log row:

`candidate_id, stage_excluded (eligibility | stratum-full | within-stratum-not-drawn | duplicate-merged), reason, excluding_rule_ref, date`

The `stage_excluded` distinction matters: a case dropped at `eligibility` failed an objective gate; a case dropped at `stratum-full` or `within-stratum-not-drawn` was eligible and was set aside for balance or by the neutral rule, not because it was inconvenient. Duplicate merges point to the surviving `incident_id`.

**Why this reduces bias:** the exclusion log is what makes the selection auditable. An independent reviewer can scan it for a telltale pattern, e.g., omission-dominated cases being quietly excluded at a higher rate, which would reveal bias the quotas were supposed to prevent. Exclusions are data, not waste.

---

## 8. Post-selection bias audit (requirements 2, 4)

After the sample is locked but before conclusions are drawn:

1. **Balance check.** Report the realized distribution of dominant-failure-mode, system_type, domain, and evidence quality against the pre-declared quotas. If the omission-dominated floor was not met, the sample is not valid and discovery/selection continues until it is.
2. **Exclusion-pattern check.** An independent person (ideally the Phase 6 second coder) reviews the exclusion log for systematic bias in what got dropped.
3. **CIR-performance-by-stratum reporting rule.** In the eventual analysis, CIR's reconstructive value is reported **separately for active-failure and omission-dominated strata**. This turns the selection tension into an explicit finding ("CIR adds most here, least there") instead of a hidden thumb on the scale. This reporting commitment is made now, pre-registered, so it cannot be dropped later if the omission results are unflattering.

**Why this reduces bias:** the audit catches failures of the protocol itself, and the by-stratum reporting rule removes the incentive to skew the sample, because a skew toward active-failure cases would no longer inflate the headline result; it would just shrink the (separately reported) omission stratum.

---

## 9. Requirement-coverage map

| Your requirement | Where met |
|---|---|
| 1. Preserve 20–30 target | Section 1 (final sample), Section 5 (quotas sum to 20–30) |
| 2. Not selected because favorable to CIR | Section 0 principle, Section 4 (CIR-blind screen), Section 6 (neutral pick), Section 8 (audit + by-stratum reporting) |
| 3. Variation across domain, system type, failure mode, evidence | Section 5 (stratification dimensions) |
| 4. Prevents cherry-picking | Section 2 (pre-registration), Section 5 (quotas/floors), Section 6 (neutral rule), Section 7 (exclusion log), Section 8 (audit) |
| 5. Reproducible by another researcher | Section 2 (frozen + dated), Section 3 (fixed sources), Section 6 (seed/rubric) |
| 6. Discovery pool vs final sample distinguished | Section 1 (three populations) |
| 7. Exclusions recorded, not discarded | Section 4 and Section 7 (exclusion log) |

---

## 11. FROZEN PARAMETERS (approved 2026-08-24)

| Parameter | Frozen value |
|---|---|
| **Final sample size (N)** | **30** |
| **Within-stratum rule** | **Hybrid E→R**: deterministic evidence-quality rank (rubric 6.1), select top up to quota; seeded random draw ONLY for boundary ties. Record seed, full eligible pool, selected, and excluded-but-eligible. |
| **Omission-dominated floor** | **≥ 8** of the 30 must be omission-dominated (controls largely Absent). |
| **Per-domain cap** | ≤ 5 of the 30 in any single `domain` (⇒ ≥ 6 domains represented). |
| **System-type spread** | Each of `confirmed-ML`, `probable-ML`, `algorithmic-nonML` ≥ 4; no single type > 18 (60%). |
| **Evidence-quality range** | ≤ ~70% of the sample from the top documentation tier (rubric score ≥ 10); hard primary-source floor on every case. |
| **Discovery pool target** | ≥ 90 candidates (≥ 3× N), swept from the fixed source set (Section 3). |
| **Pre-registration** | Git commit hash of this frozen file at freeze time (lightweight). OSF timestamp optional later. |
| **Selection-before-analysis** | Selection is completed and locked before any outcome/CIR analysis begins. Non-negotiable. |

Deviation from any frozen value during Phase 1B requires a dated amendment here with a stated reason, exactly like the framework CHANGELOG.

### Amendment log
| Date | Amendment | Reason |
|---|---|---|
| 2026-08-24 | **Mechanism/recency floor added:** ≥5 of the 30 from the 2022+ generative/agentic era, of which ≥2 agentic tool-use. Applied in `select_sample_v2.py` before the omission and system-type floors. | The v1 mechanical draw covered zero agentic/recent-generative cases, because the evidence-quality rubric structurally favors older, institutionally-documented harms. This is a coverage gap, not a CIR-favorability bias (v1 was 63% omission-dominated). The floor is a structural constraint, not hand-picked cases. Declared cost: a small drop in average documentation quality, and a slight rise in CIR-favorability (agentic cases are active-failure), from 19/30 to 17/30 omission-dominated. Both noted in the methodology. |
