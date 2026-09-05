# AI Safeguard Failure Observatory
## Pilot Coding Report: Three Incidents (Framework Stress-Test)

**Document:** `pilot_coding_report.md`
**Companion to:** `cir_framework_v0.1.md`
**Status:** Pilot. The purpose is to stress-test the CIR framework, not to generate findings. The three coded incidents below are real and sourced, but they are a test harness for the schema, not a dataset release.
**Stop rule honored:** This report ends by recommending we do NOT proceed to the 20-to-30 collection until the friction items are reviewed and the framework is amended and versioned.

---

## 0. Method and how to read this

I coded three deliberately dissimilar incidents against the full v0.1 framework, applying the two amendments you approved for the pilot (Section 1). While coding, every time a field, category, or rule forced a judgment call, broke down, or produced ambiguity, I flagged it inline as **[F-n]** and collected all of them into the consolidated Friction Report (Section 5). Section 6 proposes a v0.2 amendment set for your review. Nothing in Section 6 is applied yet.

The three incidents were chosen to span the difficulty space on purpose:

| Pilot ID | Incident | Archetype | Why chosen |
|---|---|---|---|
| **P1** | Uber ATG test-vehicle fatality (Tempe, 2018) | High-evidence, physically bounded | Gold-standard NTSB investigation; clean facts; should code smoothly and expose the *fewest* framework problems (the control case). |
| **P2** | Dutch childcare benefits scandal (Toeslagenaffaire, ~2013–2021) | Messy sociotechnical | Diffuse, multi-year, organizational, contested even on whether it is "ML"; should expose the *most* problems. |
| **P3** | Moffatt v. Air Canada chatbot (2024) | Technically complex / generative-AI-adjacent | Clean legal record but the underlying mechanism is genuinely uncertain; tests the evidence and Absent machinery. |

A deliberate result preview: P1 and P3 coded relatively cleanly; P2 broke the framework in several places. That spread is the point. If all three had coded smoothly, the pilot would have taught us nothing.

---

## 1. Amendments applied in this pilot (approved by you)

**A1 — Multi-function controls.** One control = one interaction row. `control_function` becomes `primary_function` [required, single] plus `secondary_functions` [optional, multi]. Headline function distributions count each control once under `primary_function`. Split into multiple rows only when the same physical control shows *different observed states across functions*; linked rows then share a `control_group` id. We split on state divergence, never on function multiplicity.

**A2 — Temporal precedence cannot justify causation.** Observed ordering (A before B) justifies at most `relationship_type = temporal-precedence`. Any stronger type (`enabling`, `masking`, `causal`) requires affirmative mechanism evidence beyond the ordering; `causal` additionally requires a source asserting the mechanism.

Both worked as intended in the pilot and I recommend keeping them. A2 in particular did real work in P1 (see the relationships).

---

## 2. Incident P1 — Uber ATG test-vehicle fatality

### Incident row
| Field | Value |
|---|---|
| `incident_id` | `2018-uber-atg-tempe-fatality` |
| `title` | Uber ATG autonomous test vehicle strikes and kills pedestrian, Tempe AZ |
| `domain` | autonomous-vehicle |
| `date_start` / `date_end` | 2018-03-18 |
| `harm_type` | physical-safety |
| `outcome_class` | realized-harm |
| `ai_system_role` | Automated driving system (ADS) in full control of the vehicle; responsible for perception, prediction, and braking. |
| `ai_causal_contribution` | **major-contributor** (see [F-1]) |
| `ai_causal_contribution_basis` | NTSB assigned probable cause to the operator's inattention, but found the ADS design (suppressed braking, no jaywalking-pedestrian case, tracking reset on reclassification) contributing. The ADS was in control and its design precluded the avoidance action. |
| `incident_confidence` | high (authoritative NTSB report HAR-19/03) |

### Safeguard-interaction rows
| ID | Safeguard | Layer | Primary fn | State | Evid. basis | Evid. status | Causal role | Temporal | Conf. |
|---|---|---|---|---|---|---|---|---|---|
| P1-S1 | Sensor detection (radar/lidar) | infrastructure-environment | detective | **Working** | direct-artifact (ADS logs) | confirmed-authoritative | mitigating | incident-time | high |
| P1-S2 | Object classification + path prediction | application | preventive | **Failed** | post-incident-finding, direct-artifact | confirmed-authoritative | primary | incident-time | high |
| P1-S3 | ADS autonomous emergency braking | application | recovery | **Disabled-by-design** [F-2] | post-incident-finding | confirmed-authoritative | primary | incident-time | high |
| P1-S4 | Volvo factory AEB / forward-collision warning | model→infrastructure [F-6] | recovery | **Disabled-by-design** [F-2] | post-incident-finding | confirmed-authoritative | primary | incident-time | high |
| P1-S5 | Human safety operator (monitor + intervene) | human-operator | recovery | **Failed** | post-incident-finding | confirmed-authoritative | primary | incident-time | high |
| P1-S6 | Second operator (redundancy) | human-operator | recovery | **Absent** | comparable-system, established-practice | confirmed-authoritative | contributing | incident-time | high |
| P1-S7 | In-vehicle driver-monitoring system | human-operator | detective | **Absent** | comparable-system, established-practice | confirmed-authoritative | contributing | incident-time | medium |
| P1-S8 | Uber ATG safety management / risk assessment | organizational-process | preventive | **Inadequate** | post-incident-finding | confirmed-authoritative | latent-condition | incident-time | high |
| P1-S9 | Retroactive operator-behavior monitoring | organizational-process | detective | **Inadequate** [F-3] | post-incident-finding | confirmed-authoritative | latent-condition | incident-time | medium |
| P1-S10 | Federal (NHTSA) oversight of AV testing | external-ecosystem | preventive | **Inadequate** [F-4] | post-incident-finding | confirmed-authoritative | latent-condition | incident-time | medium |
| P1-S11 | State (AZ DOT) oversight | external-ecosystem | preventive | **Inadequate** | post-incident-finding | confirmed-authoritative | contributing | incident-time | medium |

Post-incident remediations (action suppression removed; Volvo AEB re-enabled; tracking retains history across reclassification; two operators restored; driver monitoring added) are coded as separate rows with `temporal = post-incident-remediation` and excluded from the incident-time picture. Not reproduced here for length.

### Relationship rows (within P1)
| From → To | Type | Rel. conf. | Basis |
|---|---|---|---|
| P1-S2 (classification Failed) → P1-S3/S4 (braking unavailable) | temporal-precedence [F-9] | high | The perception failure preceded and coincided with braking unavailability, but the braking was disabled independently of the classification outcome, so this is co-occurrence, not causation. A2 correctly blocks an `enabling` code here. |
| P1-S3 + P1-S4 (both braking disabled) → P1-S5 (operator is sole remaining control) | enabling | high | NTSB explicitly states the design "relied instead on the operator's intervention." The mechanism is asserted: disabling both braking systems is what made the operator the only safeguard. Meets A2's bar for a stronger-than-temporal type. |
| P1-S8 (safety management Inadequate) → P1-S5 (operator Failed) | enabling | medium | NTSB links inadequate management of automation complacency to the operator's inattention. Mechanism asserted but one step removed, hence medium. |
| P1-S8 → P1-S7 (driver monitoring Absent) | common-cause | medium | Both trace to the same inadequate safety culture. |

**P1 verdict:** coded cleanly. The framework represented the physical incident well, and A2 earned its keep on the first relationship. Friction items raised: [F-1], [F-2], [F-3], [F-4], [F-6], [F-9].

---

## 3. Incident P2 — Dutch childcare benefits scandal

### Incident row
| Field | Value |
|---|---|
| `incident_id` | `2013-2021-nl-toeslagenaffaire` |
| `title` | Dutch tax authority childcare-benefit risk-classification scandal |
| `domain` | government-benefits |
| `date_start` / `date_end` | 2013 / 2021 **[F-7: an 8-year span in a schema built for bounded episodes]** |
| `harm_type` | rights-discrimination (primary); financial-loss; psychological-social **[F-8: single harm_type inadequate]** |
| `outcome_class` | realized-harm |
| `ai_system_role` | Automated risk-classification/profiling system scored benefit applications; high-risk scores routed applicants to fraud review with severe automated consequences. |
| `ai_causal_contribution` | **major-contributor**, but see **[F-5: is this even an AI/ML system?]** |
| `ai_causal_contribution_basis` | The DPA and Amnesty characterize a self-learning algorithm using nationality as a risk factor. The concrete mechanism described is a weighted, points-based risk-scoring model, whose autonomous-learning nature is asserted by authoritative bodies but not technically verified in the public record. |
| `incident_confidence` | medium (authoritative bodies agree on harm and discrimination; technical nature of the system is contested) |

### Safeguard-interaction rows
| ID | Safeguard | Layer | Primary fn | State | Evid. basis | Evid. status | Causal role | Temporal | Conf. |
|---|---|---|---|---|---|---|---|---|---|
| P2-S1 | Human-rights / data-protection impact assessment before deployment | organizational-process | preventive | **Absent** | regulation-policy, post-incident-finding | confirmed-authoritative | latent-condition | incident-time | high |
| P2-S2 | Bias mitigation / removal of nationality feature | model | preventive | **Absent** | post-incident-finding, regulation-policy | confirmed-authoritative | primary | incident-time | high |
| P2-S3 | Model transparency / explainability (non-black-box) | application | detective | **Absent** [F-10] | post-incident-finding | confirmed-authoritative | latent-condition | incident-time | high |
| P2-S4 | Meaningful individual human review of flagged cases | human-operator | detective | **Inadequate / Bypassed** [F-11] | post-incident-finding | confirmed-authoritative | primary | incident-time | high |
| P2-S5 | Proportionality safeguard on benefit reclamation | application | containment | **Absent** | post-incident-finding | confirmed-authoritative | primary | incident-time | high |
| P2-S6 | Legal basis / GDPR compliance check | organizational-process | preventive | **Failed** | regulation-policy, post-incident-finding | confirmed-authoritative | primary | incident-time | high |
| P2-S7 | Cost-recovery incentive structure | organizational-process | (n/a) | **Counterproductive** [F-12] | post-incident-finding | multiply-reported | aggravating | incident-time | medium |
| P2-S8 | Internal accountability / honest disclosure to regulator | organizational-process | detective | **Failed / Bypassed** [F-13] | post-incident-finding | confirmed-authoritative | aggravating | incident-time | high |
| P2-S9 | External oversight: Data Protection Authority | external-ecosystem | detective | **Working-but-catastrophically-late** [F-14] | post-incident-finding | confirmed-authoritative | mitigating | incident-time | high |
| P2-S10 | External oversight: courts / parliament | external-ecosystem | recovery | **Working-but-late** [F-14] | direct-artifact (inquiry report) | confirmed-authoritative | mitigating | incident-time | high |

### Relationship rows (within P2)
| From → To | Type | Rel. conf. | Basis |
|---|---|---|---|
| P2-S2 (nationality feature, no bias mitigation) → P2-S4 (human review inadequate) | enabling | medium | The black-box score with nationality baked in was handed to caseworkers who could not interrogate it, so the design enabled the rubber-stamping. Mechanism asserted by Amnesty/DPA. |
| P2-S1 (no impact assessment) → P2-S2 (no bias mitigation) | enabling | medium | Absent up-front assessment is why the discriminatory feature was never caught pre-deployment. |
| P2-S7 (cost-recovery incentive) → P2-S5 (no proportionality) | enabling | medium | The incentive to recover funds pushed toward all-or-nothing clawbacks. |
| **Most relationships here are between ABSENT controls** | — | — | **[F-15: absence-dominated incidents produce degenerate relationship graphs]** |

**P2 verdict:** the framework partially broke. It captured the safeguard inventory, but the incident's diffuseness, its contested AI/ML status, its absence-heavy profile, and several genuinely novel control behaviors (counterproductive incentive, catastrophically-late oversight, nominal-but-hollow human review) all exceeded the v0.1 vocabulary. Friction items: [F-5], [F-7], [F-8], [F-10], [F-11], [F-12], [F-13], [F-14], [F-15].

---

## 4. Incident P3 — Moffatt v. Air Canada chatbot

### Incident row
| Field | Value |
|---|---|
| `incident_id` | `2022-air-canada-chatbot-bereavement` |
| `title` | Air Canada support chatbot asserts non-existent bereavement-refund policy |
| `domain` | consumer-chatbot |
| `date_start` / `date_end` | 2022-11-11 (harm) / 2024-02-14 (adjudication) **[F-16: incident date vs resolution date]** |
| `harm_type` | financial-loss |
| `outcome_class` | realized-harm |
| `ai_system_role` | Customer-facing website chatbot answered a policy question with a confident, specific falsehood contradicting the airline's own linked policy. |
| `ai_causal_contribution` | **major-contributor** (the false answer induced reliance; tribunal accepted causation) |
| `ai_causal_contribution_basis` | Moffatt v. Air Canada, 2024 BCCRT 149, paras. 15, 17, 30. |
| `incident_confidence` | high (written tribunal decision with findings of fact) |

### Safeguard-interaction rows
| ID | Safeguard | Layer | Primary fn | State | Evid. basis | Evid. status | Causal role | Temporal | Conf. |
|---|---|---|---|---|---|---|---|---|---|
| P3-S1 | Output grounding / verification against real policy | application | preventive | **Unknown** [F-17] | operator-claim (none given) | inferred-indirect | primary | incident-time | low |
| P3-S2 | Human review of chatbot answers before delivery | human-operator | detective | **Absent** | established-practice | inferred-indirect | contributing | incident-time | low |
| P3-S3 | Effective disclaimer / ToS carve-out | application | containment | **Absent** | comparable-system | single-source-reported | contributing | incident-time | medium |
| P3-S4 | Linked correct policy page (reachability) | application | containment | **Inadequate** | direct-artifact (decision) | confirmed-authoritative | contributing | incident-time | high |
| P3-S5 | Pre-deployment accuracy testing / evaluation | organizational-process | preventive | **Unknown** [F-18] | (none defensible) | inferred-indirect | latent-condition | incident-time | low |
| P3-S6 | Organizational accountability ("chatbot is separate entity" defense) | organizational-process | recovery | **Bypassed→Rejected** [F-19] | direct-artifact (decision) | confirmed-authoritative | aggravating | incident-time | high |
| P3-S7 | External adjudication (Civil Resolution Tribunal) | external-ecosystem | recovery | **Working** | direct-artifact (decision) | confirmed-authoritative | mitigating | post-incident [F-16] | high |

### Relationship rows (within P3)
| From → To | Type | Rel. conf. | Basis |
|---|---|---|---|
| P3-S1 (grounding Unknown) → P3-S4 (linked page Inadequate) | temporal-precedence | low | We know the answer contradicted the linked page; we do not know the mechanism that produced the contradiction, so A2 caps this at temporal-precedence. |
| P3-S2 (no human review) → P3-S1 (ungrounded answer reached user) | enabling | low | Had answers been reviewed, the falsehood could have been caught; mechanism plausible but not asserted by the source, so low confidence. |

**P3 verdict:** coded cleanly at the incident level, but exposed the Absent-vs-Unknown boundary hard. Our own Absent evidentiary-basis rule forced `Unknown` on the two most intuitively "missing" controls (grounding, testing), which is the rule working as designed but feels lossy. Friction items: [F-16], [F-17], [F-18], [F-19].

---

## 5. FRICTION REPORT (the deliverable)

Every field, category, or rule that failed, required a judgment call, or produced ambiguity. Grouped by theme. Severity: **High** = blocks or distorts the eventual analysis if unfixed; **Medium** = introduces coder inconsistency; **Low** = cosmetic or easily managed.

### Theme 1 — The control-state vocabulary is missing states

**[F-2] "Disabled by design / deliberately turned off" has no home. (High.)** In P1, both the ADS emergency braking (suppressed by a designed 1-second delay) and the Volvo factory AEB (automatically deactivated under ADS control) *existed and were functional* but were *deliberately switched off by the operator's own design choice*. None of `Inadequate` (worked-as-designed-but-weak), `Bypassed` (circumvented by an external actor/input), `Failed` (broke), or `Absent` (never existed) fits. I coded a provisional `Disabled-by-design`. This is arguably the single most important safeguard state in AV and agentic-AI incidents, where operators routinely disable a safety feature for performance or false-positive reasons. **It must be added.**

**[F-12] "Counterproductive / anti-safeguard" has no home. (Medium-High.)** In P2, the cost-recovery incentive was not a weak safeguard, it was a mechanism that *actively drove harm*. `observed_state` has no value for "this control made things worse," and `control_function` cannot even be assigned (I left it n/a). We either need a `Counterproductive` state or an explicit decision to exclude anti-safeguards from the safeguard table and record them elsewhere (e.g., a `contributing_factors` table). **Design decision required.**

**[F-14] "Worked, but far too late to prevent or contain the harm" is unrepresentable. (High.)** In P2, the DPA, courts, and parliament all eventually functioned, but years after the harm. Coding them `Working` overstates their protective value; coding them `Failed` is false. There is no field for control *latency* or *timeliness*. A recovery control that acts in 8 years and one that acts in 8 hours currently look identical. **Needs a timeliness dimension** (see proposed fix F-14 in Section 6).

### Theme 2 — The Absent / Inadequate / Bypassed / Unknown boundaries blur under automation bias

**[F-11] "The human review existed on paper but was hollow." (High.)** P2's caseworkers nominally reviewed flagged cases but were handed an uninterrogable score and effectively rubber-stamped it. Is that `Inadequate` (existed, too weak), `Bypassed` (present but not meaningfully engaged), or `Failed`? All three are defensible. This is the automation-bias signature and it will recur in most human-oversight failures across the dataset. If three coders split three ways on the most common failure mode, inter-rater agreement (Phase 6) collapses. **Needs an explicit disambiguation rule.**

**[F-17 / F-18] Absent-vs-Unknown is doing heavy lifting and it hurts. (Medium.)** In P3, the Absent evidentiary-basis rule correctly forced `Unknown` on "output grounding" and "pre-deployment testing," because we have no defensible basis they should have existed beyond weak established-practice. The rule worked exactly as designed. But it means the two most intuitively damning gaps in the case are recorded as "we don't know" rather than "missing," which understates the finding. This is a genuine tension between epistemic honesty and analytic usefulness, and it is worth confirming you still want the rule this strict. (I recommend keeping it and solving the felt loss with a `suspected_absent` flag, see Section 6.)

**[F-3][F-4] Inadequate absorbs too much. (Medium.)** P1's retroactive operator monitoring (a real capability that was rarely used) and NHTSA's voluntary-but-unenforced self-assessment both landed in `Inadequate`, but they are different failure modes: one is "control exists but is not operated," the other is "control exists but has no teeth." `Inadequate` is becoming a catch-all. Consider subtypes: `inadequate-design` vs `inadequate-operation`.

### Theme 3 — Scope and unit-of-analysis strain

**[F-5] The eligibility gate's "AI/ML system" term is undefined at the boundary. (High, and it is a Phase 0 decision.)** P2 may or may not be machine learning; authoritative bodies call it "self-learning" while describing a weighted rule-based scorer. P3's chatbot architecture is unestablished (LLM vs scripted). If the Observatory only admits confirmed-ML systems, both P2 and P3 wobble, and P2 is one of the most important algorithmic-harm cases in existence. **You must decide the scope boundary explicitly:** does the Observatory cover (a) only ML systems, (b) ML plus algorithmic decision systems, or (c) any automated decision system materially involving data-driven scoring? My recommendation is (b), with an `system_type` field recording {confirmed-ML, probable-ML, algorithmic-nonML, unknown} so the boundary is *coded* rather than *gated*, mirroring how we already handle causal contribution. This keeps the important cases in and lets you filter later.

**[F-7] The "incident" unit assumes a bounded episode; systemic harms break it. (High.)** P2 spans eight years, tens of thousands of victims, and two overlapping systems. Treating it as one row flattens enormous internal variation; splitting it into many incidents is arbitrary. The two-table architecture handles multiple safeguards per incident but not *one program that is really many episodes*. **Needs a rule** for decomposing or bounding systemic cases (e.g., an `incident_scope` field: {discrete-event, campaign, systemic-program} and a convention that systemic programs are coded at the program level with a note).

**[F-15] Absence-dominated incidents produce degenerate relationship graphs. (Medium.)** P2's safeguards are mostly `Absent`. You cannot easily sequence absences (there is no "when" to a control that never existed), so the relationships table, the mechanism that carries your whole thesis, is sparse and weak exactly where the incident is most about missing controls. This is important: it means CIR's relational advantage may be strongest for *active-failure* incidents and weakest for *omission* incidents. That is a finding about the method itself and belongs in the eventual paper's limitations. It may also motivate a distinct relationship type for absences (e.g., `joint-omission` linking controls that were all absent for a common reason).

### Theme 4 — Field-level and vocabulary gaps

**[F-1] `ai_causal_contribution` conflates "how much did the AI contribute" with "was the AI the blamed cause." (Medium.)** In P1, NTSB's *probable cause* is the human operator, yet the AI system materially contributed. Coding `major-contributor` is defensible but loses the distinction between the analyst's causal apportionment and the official/legal attribution. Consider splitting into `ai_causal_contribution` (our judgment) and `attributed_primary_cause` (what the authoritative finding blamed).

**[F-6] `system_layer` is not always single-valued. (Medium.)** P1's Volvo AEB is a hardware safety feature (infrastructure/environment) that is also a model-adjacent perception function, and disabling it was an application-layer decision. I had to pick one. Either allow a primary+secondary layer (mirroring the function fix A1) or write a tie-break rule.

**[F-8] `harm_type` should be multi-valued. (Medium.)** P2 caused discrimination, financial ruin, and psychological harm simultaneously. Forcing one primary harm loses the multi-harm signature that is characteristic of sociotechnical cases. Make it primary + secondary, like function and (proposed) layer.

**[F-13] Honesty/accountability controls do not fit the four functions. (Low-Medium.)** P2's director-general falsely denied processing data to the regulator. That is a governance/integrity control failing, but it is not cleanly preventive/detective/containment/recovery. This is the same gap flagged in the framework's own Appendix B (assurance/governance function). The pilot confirms the gap is real; per your instruction I did NOT add the fifth function, and I am logging it here as the promised explicit open issue.

**[F-16] Incident date vs resolution date, and recovery controls that act post-incident. (Low.)** P3's harm is 2022; adjudication is 2024. The external tribunal (P3-S7) is a `Working` recovery control but its `temporal_state` is post-incident by nature, which collides with the rule that post-incident-remediation rows are excluded from the incident-time picture. Recovery controls are *supposed* to act after the harm, so "post-incident" is not the same as "remediation added later." **Needs disambiguation** between `post-incident-by-function` (recovery doing its job) and `post-incident-remediation` (a new control added after).

**[F-19] "Asserted defense that was rejected" is a state we invented on the fly. (Low.)** P3's "chatbot is a separate entity" argument is an accountability posture the operator tried and the tribunal rejected. I coded `Bypassed→Rejected`, which is not in the vocabulary. This is niche but will recur in adjudicated cases.

### Theme 5 — What worked (recording the negatives is also a pilot result)

- The two-table-plus-relationships architecture held up structurally in all three cases.
- A2 (temporal-precedence rule) prevented at least three tempting-but-unsupported causal codes (P1-S2→braking, P3-S1→S4, P3-S2→S1). It is doing exactly what you designed it to do.
- The three-field evidence separation (basis / status / confidence) proved its worth in P3, where high-authority findings (the decision) sat next to low-confidence inferences (testing) in the same incident, and the fields kept them honestly distinct. Do not merge them.
- The Absent evidentiary-basis rule fired correctly in P1 (defensible Absent for the removed second operator) and P3 (forced Unknown for unprovable gaps). The rule is sound; the only open question is the felt loss in F-17/F-18.
- `confidence` caps behaved sensibly; nothing was coded `high` on thin sourcing.

---

## 6. Proposed v0.2 amendment set (for your review — NOT yet applied)

Ordered by severity. I recommend we discuss these before I touch the framework file, then I roll all approved changes into one clean v0.2 with a CHANGELOG entry.

1. **[from F-2] Add `observed_state = Disabled` (or `Deactivated`):** a control that existed and was functional but was deliberately turned off/suppressed by the operator or system design. High priority; pervasive in AV and agentic cases.
2. **[from F-5] Replace the AI/ML eligibility *gate* with a scope decision plus a coded `system_type` field** {confirmed-ML, probable-ML, algorithmic-nonML, unknown}. Recommend scope option (b): ML plus algorithmic decision systems. This is a Phase 0 amendment and needs your explicit call.
3. **[from F-14] Add a `timeliness` field to safeguard interactions** {in-time, delayed, too-late, n/a} so that "worked but catastrophically late" is representable without abusing `Working`/`Failed`.
4. **[from F-11] Add a disambiguation rule for hollow human oversight:** define `Bypassed` to include "present but not meaningfully engaged (rubber-stamping / automation bias)," and reserve `Inadequate` for genuine design weakness. Add a worked example to the manual.
5. **[from F-7] Add `incident_scope`** {discrete-event, campaign, systemic-program} and a convention for coding systemic programs at the program level.
6. **[from F-8, F-6] Make `harm_type` and `system_layer` primary+secondary**, mirroring the function fix A1.
7. **[from F-1] Split `ai_causal_contribution` from `attributed_primary_cause`** so analyst apportionment and official attribution are distinct.
8. **[from F-16] Split `temporal_state`** into `existence_timing` {incident-time, added-after} and note that recovery controls legitimately *act* post-incident; only *added-after* controls are excluded from incident-time distributions.
9. **[from F-17/F-18] Add a `suspected_absent` boolean** that can accompany an `Unknown` state, so the analyst's suspicion is captured without violating the Absent evidentiary-basis rule.
10. **[from F-12] Decide: `Counterproductive` state, or a separate `contributing_factors` table** for anti-safeguards. Recommend the separate table, to keep the safeguard table's state semantics clean.
11. **[from F-13] The assurance/governance function** remains an explicit open issue, not yet added, per your instruction. The pilot confirms it is a real gap; revisit after 5–10 more incidents as originally planned.
12. **[from F-15, F-19] Lower priority:** consider a `joint-omission` relationship type and an `asserted-rejected` accountability state. Defer unless they recur.

---

## 7. Recommendation and stop

Per your guardrail, I am stopping here and NOT proceeding to the 20-to-30 collection. The pilot did its job: three incidents surfaced nineteen distinct friction points, of which four are High-severity and would have silently distorted the eventual analysis had we coded twenty incidents first and discovered them at case fifteen. Two of the High items (F-2 Disabled state, F-5 AI/ML scope) are near-certain to appear in a large fraction of the full dataset.

Two of these need *your* decision specifically, because they change project scope rather than mechanics: the AI/ML scope boundary (F-5) and how systemic programs are bounded (F-7). The rest are mechanical and I can draft into v0.2 once you approve the direction.

---

## Sources

**P1 — Uber ATG:** NTSB report HAR-19/03 (adopted Nov 2019), [full report PDF](https://www.ntsb.gov/investigations/accidentreports/reports/har1903.pdf); [NTSB Vehicle Automation Report (docket)](https://data.ntsb.gov/Docket/Document/docBLOB?ID=40477717&FileExtension=.PDF&FileName=Vehicle+Automation+Report-Master.PDF); [investigation page](https://www.ntsb.gov/investigations/Pages/HWY18MH010.aspx); [ETSC summary](https://etsc.eu/inadequate-safety-culture-contributed-to-fatal-uber-automated-test-vehicle-crash/).

**P2 — Toeslagenaffaire:** Amnesty International, *Xenophobic Machines* (2021), [PDF](https://www.amnesty.nl/content/uploads/2021/10/20211014_FINAL_Xenophobic-Machines.pdf); Autoriteit Persoonsgegevens [childcare/nationality report](https://www.autoriteitpersoonsgegevens.nl/documenten/onderzoek-belastingdienst-kinderopvangtoeslag) and [FSV report](https://www.autoriteitpersoonsgegevens.nl/documenten/onderzoek-belastingdienst-fraude-signalering-voorziening-fsv); [DPO English decision summary](https://thedpo.eu/en/decisions/7bd0d509-ac6c-423d-a927-66dce2996b32); [Wikipedia overview](https://en.wikipedia.org/wiki/Dutch_childcare_benefits_scandal).

**P3 — Moffatt v. Air Canada:** [2024 BCCRT 149 full text PDF](https://s3.amazonaws.com/IGG/AI+Part+1+-+Materials/Moffatt+v.+Air+Canada.pdf); [CanLII record](https://www.canlii.org/en/bc/bccrt/doc/2024/2024bccrt149/2024bccrt149.html); [Forbes](https://www.forbes.com/sites/marisagarcia/2024/02/19/what-air-canada-lost-in-remarkable-lying-ai-chatbot-case/); [ABA Business Law Today](https://www.americanbar.org/groups/business_law/resources/business-law-today/2024-february/bc-tribunal-confirms-companies-remain-liable-information-provided-ai-chatbot/); [McCarthy Tétrault analysis](https://www.mccarthy.ca/en/insights/blogs/techlex/moffatt-v-air-canada-misrepresentation-ai-chatbot).
