# Deliverable N - Final Independent Integrity Audit (v1.0)

Independent clean-room recomputation of every number in the abstract, Results, Discussion,
Conclusion, tables, and figure captions, computed directly from the frozen `data/*.csv` files by
`scripts/audit_independent.py` **without** reading `analysis/analysis_results.json`. Followed by an
overclaiming audit of the substantive inferences, a denominator/unit audit, and a figure/table
reconciliation.

## Part 1 - Numerical verification (all recomputed from raw rows)

Every number below was recomputed independently. Except where the Discrepancy column says otherwise,
the paper's value is **confirmed correct**.

| # | Location | Current claim | Recomputed | Discrepancy | Severity | Correction |
|---|---|---|---|---|---|---|
| 1 | Abstract / §6.1 / Table 2 / Fig 1 | 137/181 non-functional = 75.7% | 44+32+41+15+5 = 137; 137/181 = 75.6906% -> 75.7% | none | - | none |
| 2 | Abstract / §6.1 | 20.4% Working | 37/181 = 20.4420% -> 20.4% | none | - | none |
| 3 | Abstract / §6.1 / Table 6 | 70.3% of Working are external-ecosystem | 26/37 = 70.2703% -> 70.3% | none | - | none |
| 4 | §6.1 / Table 6 | 25/30 (83.3%) incidents have >=1 Absent | 25/30 = 83.33% | none | - | none |
| 5 | Abstract / §6.3 / Table 6 | 11/30 (36.7%) detective-Working yet realized harm | 12 incidents had detective Working; 11 of them realized-harm (the 12th, EchoLeak, is a near-miss) -> 11/30 = 36.7% | none | - | none |
| 6 | Abstract / §6.4 / Table 5 / Fig 4 | enabling 49/84 = 58.3% | 49/84 = 58.3333% -> 58.3% | none | - | none |
| 7 | §6.4 / Table 6 | mean 2.8 relationships/incident, all >=2, range 2-5 | 84/30 = 2.8000; min 2, max 5; 30/30 covered | none | - | none |
| 8 | Abstract / §6.5 | AI major-contributor in 26/30 | 26 major-contributor, 3 disputed, 1 contributory-non-necessary | none | - | none |
| 9 | Abstract / §6.5 | organizational attribution 18/30; AI-system 2/30 | organizational 18, multiple 6, AI-system 2, human-operator 1, disputed 3 | none | - | none |
| 10 | §6.2 / Fig 2 / Fig 6 | preventive Working = 0/51 | 0/51 | none | - | none |
| 11 | §6.2 / §6.5 / Table 6 | assurance-governance Inadequate = 13 (43.3%) | 13/30 = 43.3% | none | - | none |
| 12 | Abstract / §4 / Fig 5 | generative era = 8/30 | era=genai = 8 | none (see D-3 for doc reconciliation) | - | none to paper |
| 13 | Abstract / §6.6 | 3 agentic | agentic flag = 3 | none | - | none |
| 14 | §4 | system_type 17 / 8 / 5 | confirmed-ML 17, algorithmic-nonML 8, probable-ML 5 | none | - | none |
| 15 | §4 | 14 discrete / 14 systemic / 2 bounded | 14 / 14 / 2 | none | - | none |
| 16 | §5 / Cardinality | 202 = 181 incident-time + 21 added-after | 181 + 21 = 202; 0 rows with other timing | none | - | none |
| 17 | §5 / E report | 146 confirmed-authoritative, 8 disputed; 134 high, 13 low confidence (of 202) | 146 / 8; 134 / 13 | none | - | none |
| 18 | §7 / Table 6 | omission-dominated 8/30 (26.7%) | 8/30 = 26.7% | none | - | none |
| 19 | §8 | 2 near-miss incidents (EchoLeak, Amazon Q) | outcome near-miss = exactly those 2 | none | - | none |
| 20 | Function totals (Fig 2 / Table 3) | preventive 51, detective 46, containment 29, recovery 25, assurance 30 | identical; sum 181 | none | - | none |
| 21 | Layer totals (Fig 3 / Table 4) | model 14, application 43, infra 8, human-operator 26, org-process 50, external 40 | identical; sum 181 | none | - | none |
| **22** | **§4** | **"span 13 domains (... 5 named ...) and nine domains with 1-2 each"** | **13 domains total; 5 have >=3; the remaining are eight domains, not nine (5 + 9 = 14 != 13)** | **OFF-BY-ONE** | **Low (real numeric error)** | **change "nine" to "eight"** |

The user's specific concern (that "non-functional" must not silently absorb Unknown and Disputed) is
**confirmed handled correctly**: the paper's 137 non-functional is the sum of Absent, Failed,
Inadequate, Bypassed, and Disabled only. Unknown (6) and Disputed (1) are excluded; they are 7 rows,
3.9% of 181, and the paper never counts them as failures. "Not Working" (144/181, 79.6%) and
"non-functional" (137/181, 75.7%) are distinct and the paper uses the latter throughout.

## Part 2 - Overclaiming audit of substantive inferences

| # | Inference (location) | Supported by data? | Severity | Recommended wording change |
|---|---|---|---|---|
| O-1 | "the most reliable safeguard was the outside world noticing" (§6.1) | Partly. External-ecosystem has the highest Working rate by layer (26/40 = 65%) and holds 70% of all Working rows, so it is defensible as stated - BUT incidents partly enter the sample *because* external actors surfaced them, which inflates external Working. Already hedged with "in this sample." | Low | Keep, but add a half-sentence noting the selection effect (external actors surfacing harm is part of why incidents are known), so the reader does not read it as an unconditional reliability ranking. |
| O-2 | "Detection is usually not the binding constraint" (§6.3 heading + "This locates the binding constraint downstream of detection") | Overclaims. Only 37% of incidents had Working detection with harm; in the majority, detection itself was Absent/Failed/Inadequate/Bypassed (33 of 46 detective rows non-functional). "Usually" is not supported. The abstract already says "frequently," which is fine. | Medium | Change heading "usually" -> "frequently"; soften the body from "This locates the binding constraint downstream of detection" to "In these cases the binding constraint lay downstream of detection." |
| O-3 | "models were rarely the layer that failed" (raised by reviewer; paper §6.5 wording) | The paper does not use this exact phrase; it says the model layer is least-coded (14/181) and blame is rarely attributed to the AI system (2/30), which is supported. But the audit shows all 14 model-layer safeguards were non-functional (0 Working), so "models rarely fail" would be a misreading. | Low-Medium | Add a clause to §6.5: model-layer controls were few but, where present, uniformly non-functional (0/14 Working); the point is that few safeguards sit at the model layer and blame lands organizationally, not that models are reliable. |
| O-4 | "The one genuinely new surface is indirect prompt injection" (§6.6) | Overclaims by singularizing. Indirect prompt injection is clearly novel, but LLM confabulation presented as authoritative (Mata fake citations, Air Canada fabricated policy) is arguably also a new surface. The abstract's plural "new attack surfaces ... (indirect prompt injection)" is fine. | Medium | Change §6.6 to "The clearest new attack surface is indirect prompt injection," and acknowledge LLM confabulation as a second candidate. |
| O-5 | Any prevalence/generalization beyond n=30 | The paper is consistently careful: "exploratory," "not representative," per-denominator claims, "in this sample." The only rhetorical stretches are O-1 and O-2 above. Conclusion's "mostly not working" is denominated to "these 30 incidents." | Low | No global change beyond O-1/O-2. |

## Part 3 - Denominator and unit-of-analysis audit

Confirmed that units are never mixed:

- **Incident-level** (n=30): system_type, era, outcome_class, incident_scope, ai_causal_contribution,
  attributed_primary_cause, "incidents with >=1 Absent," detective-Working incidents, omission-dominated.
- **Safeguard-level, incident-time (denominator 181):** observed-state, function, and layer
  distributions. The 21 added-after rows are excluded from all of these and reported separately.
- **Safeguard-level, all rows (202):** evidence_status and confidence quality counts only (explicitly
  scoped in §5 / E report).
- **Function-level and layer-level:** row n stated per category; totals reconcile to 181 exactly.
- **Relationship-level (denominator 84):** relationship-type shares and per-incident relationship
  counts.

No statistic crosses these boundaries. Percentages always carry the denominator that matches their
unit.

## Part 4 - Cardinality reconciliation

181 incident-time + 21 added-after = 202 total safeguards (0 rows with any other existence_timing).
Observed-state counts sum to 181 (37+41+32+15+5+44+6+1). Function counts sum to 181. Layer counts sum
to 181. Relationship endpoints: 0 unresolved (all resolve within their own incident). All confirmed.

## Part 5 - System-type conceptual consistency

confirmed-ML 17, probable-ML 5, algorithmic-nonML 8, and zero architecture-unknown. This is consistent
with the frozen scope: every incident could be classified, so no "unknown/architecture-unknown" slot
was needed; "probable-ML" is the frozen sample's realization of the scope's hybrid-uncertain category.
COMPAS sits in algorithmic-nonML per the QA correction (a statistical instrument, not learned ML),
which is the intended, documented placement. No inconsistency.

## Part 6 - Era definition (definitional finding)

`era` is a **paradigm** flag (generative/LLM/agentic system), not a pure calendar cutoff. Two
autonomous-vehicle incidents dated 2023 (Cruise drag, Tesla recall) are correctly coded `legacy`
because they are not generative/agentic-paradigm systems. The data dictionary's gloss "(2022+)" is
therefore slightly misleading. Severity: Low. Recommended correction: reword the data-dictionary
definition to "generative/LLM/agentic-paradigm system (predominantly 2022+), assigned by system
paradigm, not calendar date alone."

## Part 7 - Figure / table reconciliation

Every figure and table was regenerated deterministically from the frozen data and each reconciles
with the independent recomputation: Fig 1 / Table 2 (state counts), Fig 2 / Table 3 (state x
function), Fig 3 / Table 4 (state x layer), Fig 4 / Table 5 (relationship types 49/18/10/7), Fig 5
(system_type 17/8/5; era 22/8; outcome 28/2; ai_causal 26/3/1), Fig 6 (Working share: preventive 0%,
detective 28%, containment 24%, recovery 60%, assurance 7%). Figure-caption denominators (181 for
Figs 1-3/6, 84 for Fig 4, n=30 for Fig 5) are correct. No figure or table disagrees with the dataset.

## Summary of required corrections

Only the following changes are warranted; everything else is sound and is left unchanged.

1. **§4 numeric fix (Low but real):** "nine domains with 1-2 each" -> "eight domains with 1-2 each."
2. **§6.3 overclaim (Medium) - applied:** the section was rewritten to lead with the explicit 11/30
   observation ("In this sample, detection was frequently insufficient to prevent harm: 11 of 30
   incidents involved at least one detective safeguard that was Working at incident time despite harm
   subsequently occurring"), interpreted cautiously and only of these 30 incidents. The terms "usually"
   and "binding constraint" were removed from §6.3, the abstract, and the conclusion.
3. **§6.6 overclaim (Medium):** "the one genuinely new surface" -> "the clearest new attack surface,"
   acknowledging LLM confabulation as a second candidate.
4. **§6.1 hedge (Low):** add a selection-effect caveat to the "outside world noticing" sentence.
5. **§6.5 clarity (Low-Medium):** add a clause that model-layer controls were few but uniformly
   non-functional.
6. **Data dictionary (Low):** reword the `era` definition to paradigm-based.
7. **Selection doc reconciliation (Low, doc-only):** note that the frozen dataset's generative-era
   count is 8 (the paper is correct); the pre-freeze selection note said 7 because Workday's era tag
   was assigned at coding.

No fabricated numbers were found; no denominator or unit errors were found; no figure/table
disagreements were found. The dataset itself requires no change and remains frozen at v1.0.
