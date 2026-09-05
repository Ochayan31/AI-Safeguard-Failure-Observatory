# AI Safeguard Failure Observatory
## Phase 1B — Batch 1 (calibration), coded against CIR v0.2

**Document:** `batch1_coded.md`
**Purpose:** Deep-code the first 5 of the locked 30 to fix coding conventions before the remaining 25. These 5 were chosen to span archetypes: an autonomous-vehicle active-failure (Cruise), a public-sector omission systemic program (Robodebt), a healthcare omission case (Optum), a recent chatbot case (Air Canada), and an agentic tool-use case (Gemini CLI).
**For your review:** The "calibration notes" under each incident flag the convention decisions I most want you to confirm, because these are the patterns that will repeat 25 more times.
**Format:** Prose-and-table coding of the four v0.2 tables. Machine-readable CSV/JSON comes in Phase 1C once conventions are locked. Fields abbreviated in tables: layer, fn=primary_function, state=observed_state, role=causal_role, time=timeliness, exist=existence_timing, conf=confidence, basis=evidentiary_basis, status=evidence_status.

---

## Convention decisions demonstrated in this batch (please confirm)

1. **Disabled vs Bypassed.** Robodebt's removed human-verification step = **Disabled** (a pre-existing control switched off). Its suppressed legal advice = **Disabled** (the operator deactivated the safeguard's protective effect, even though an output was produced). An *external* control defeated by deception (the Ombudsman) = **Bypassed**. The line: neutralizing your own safeguard = Disabled; circumventing another control = Bypassed.
2. **Bypassed vs Inadequate, the sequel.** Optum's clinicians were **Inadequate** (genuinely engaged, but the control's design cannot see population-level bias), contrasting with the Dutch caseworkers from the pilot who were **Bypassed** (structurally denied the information to function). Same "hollow oversight" surface, opposite codes, decided by the engagement test.
3. **Unknown + suspected_absent vs Absent.** Air Canada's output-grounding safeguard = **Unknown + suspected_absent** (no basis it existed; architecture undocumented), while its human-review safeguard = **Absent** (established-practice basis, confidence capped). Two "missing" controls in one incident, coded differently by the evidentiary-basis rule.
4. **masking relationships** carry the disclosure/oversight-defeat cases (Cruise's withheld video; Robodebt misleading the Ombudsman): a safeguard failure that hid the harm from a recovery control.
5. **contributing_factors** table absorbs non-safeguards that drove harm (Optum's upstream care-access inequity; Robodebt's budget-savings mandate), keeping them out of safeguard distributions.

---

## INCIDENT 1 — C004 Cruise robotaxi pedestrian dragging

**Incident row.** `incident_id` 2023-cruise-drag-sf · domain autonomous-vehicle · date 2023-10-02 · scope **discrete-event** · harm_primary physical-safety · outcome realized-harm · system_type **confirmed-ML** · ai_causal_contribution **major-contributor** (a human-driven car struck the pedestrian first and threw her into the AV's path; the AV's own contribution is the post-collision **dragging**, which was its decision) · attributed_primary_cause **multiple** (human driver for initial impact; AV design for the drag; Cruise org for the disclosure failure), sources NTSB recall 23E-086, DOJ DPA, CA DMV, Quinn Emanuel report · incident_confidence high.

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Perception / pedestrian avoidance at impact | application | preventive | Failed | post-incident-finding, direct-artifact | confirmed-authoritative | contributing | too-late | incident-time | medium |
| S2 | Emergency hard-braking | application | containment | Working | direct-artifact | confirmed-authoritative | mitigating | in-time | incident-time | medium |
| S3 | Post-collision decision logic (collision classification) | application | containment | Failed | post-incident-finding | confirmed-authoritative | primary | too-late | incident-time | high |
| S4 | "Do not move with person/object underneath" occupancy stop | application | containment | Absent | comparable-system, post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | medium |
| S5 | Remote-assistance human oversight | human-operator | detective | Bypassed | post-incident-finding | confirmed-authoritative | contributing | too-late | incident-time | low |
| S6 | Organizational honest disclosure to regulators | organizational-process | assurance-governance | Failed | post-incident-finding, direct-artifact | confirmed-authoritative | aggravating | too-late | incident-time | high |
| S7 | External regulatory oversight (DMV/NHTSA/CPUC/DOJ) | external-ecosystem | recovery | Working | direct-artifact | confirmed-authoritative | mitigating | too-late | incident-time | high |
| S8 | Software fix: collision-classification remains-stationary | application | containment | Working | direct-artifact | confirmed-authoritative | not-causally-relevant | in-time | **added-after** | high |

Relationships: **S3 → S4** enabling (med): the misclassification-triggered pullover is what made the missing occupancy-stop consequential; mechanism asserted by NHTSA recall. **S6 → S7** **masking** (high): omitting the dragging from reports hid it from regulators, delaying the recovery response; DOJ established the omission. **S1 → S3** temporal-precedence (high): impact preceded the post-collision logic; no causal claim beyond order.

Contributing factors: **CF1** Cruise "us-versus-them" posture toward regulators and move-fast pressure (factor_type cultural, effect harm-amplifying, role aggravating, basis post-incident-finding [Quinn Emanuel], conf medium) — drove the disclosure failure but is not itself a safeguard.

**Calibration notes.** (a) S5 remote oversight is **Bypassed**, not Failed: the operators were structurally denied the footage of the drag (only ~3s + ~14s clips transmitted, not the pullover), so the control could not function — engagement test → Bypassed; confidence low because it is genuinely unclear a remote human could have intervened in the seconds available. (b) S6 disclosure is a governance/accountability control that does not fit prevention/detection/containment/recovery cleanly; per the deferred assurance-governance issue I filed it under organizational-process with fn=detective (it surfaces truth to oversight) and flagged it. (c) S2 is coded **Working/mitigating** to record a control that held (it did brake), even though harm still occurred — "the control that held" is evidence too. (d) The QE-vs-DOJ intent dispute does not change S6's state (Failed either way); it would only affect a future "intent" field.

---

## INCIDENT 2 — C041 Robodebt (Online Compliance Intervention)

**Incident row.** `incident_id` 2015-2020-au-robodebt · domain government-benefits · date_start 2016 (mass rollout) / date_end 2020 (wind-back) · scope **systemic-program** · **observation_boundary:** the automated income-averaging debt-raising process and its safeguards, ~July 2016 rollout to the May 2020 wind-back; excludes unrelated Centrelink compliance activity · harm_primary financial-loss · harm_secondary psychological-social · outcome realized-harm · system_type **algorithmic-nonML** (deterministic averaging + data-matching, no learning) · ai_causal_contribution **major-contributor** · attributed_primary_cause **organizational** (Royal Commission), sources Royal Commission 2023, Amato [2019] FCA, Prygodicz (No 2) [2021] FCA 634, Commonwealth Ombudsman 2017 · incident_confidence high.

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Correct-calculation on actual fortnightly income | application | preventive | Absent | regulation-policy, post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S2 | Legality / lawful-basis check (internal legal advice) | organizational-process | preventive | **Disabled** | post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S3 | Human officer verification before debt-raising (incl. burden-of-proof on government) | human-operator | preventive | **Disabled** | regulation-policy, post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S5 | Recipient challenge / appeal mechanism | human-operator | recovery | Inadequate (operation) | post-incident-finding | confirmed-authoritative | contributing | too-late | incident-time | high |
| S6 | Internal governance: heed warnings / AAT rulings | organizational-process | detective | Failed | post-incident-finding | confirmed-authoritative | contributing | too-late | incident-time | high |
| S7 | External oversight: Commonwealth Ombudsman | external-ecosystem | detective | Bypassed | post-incident-finding | confirmed-authoritative | contributing | delayed | incident-time | medium |
| S8 | External oversight: courts (Amato/Prygodicz) | external-ecosystem | recovery | Working | direct-artifact | confirmed-authoritative | mitigating | too-late | incident-time | high |
| S9 | External oversight: Royal Commission | external-ecosystem | recovery | Working | direct-artifact | confirmed-authoritative | mitigating | too-late | incident-time | high |

Relationships: **S2 → S1** enabling (med): overriding the legality safeguard let the unlawful method stand. **S3 → S5** enabling (med): removing pre-debt human verification (and reversing the onus) pushed all correction into an overloaded appeal channel. **S7 → S8** **masking** (med): officers misleading the Ombudsman hid the illegality, delaying judicial recovery by years.

Contributing factors: **CF1** budget-savings mandate / pressure to book compliance savings (factor_type incentive-structure, effect harm-enabling, role aggravating, basis post-incident-finding, conf medium).

**Calibration notes (updated per Batch-1 locked decisions).** (a) **S3 is the flagship Disabled example**: a human-verification control that demonstrably existed pre-OCI and was deliberately removed by design; the burden-of-proof reversal is **merged into S3** as one control (locked decision 2), not a separate row. (b) **S2 is Disabled** (locked decision 1): the operator's own legal-review safeguard produced 2014 advice that the method was unlawful, and that protective output was suppressed/omitted from the Cabinet proposal — deliberately deactivating the safeguard's protective effect is Disabled, even though an output was produced. This corrects the initial batch-1 draft, which had it as Bypassed. (c) S7 Ombudsman stays **Bypassed** (an *external* control defeated by being fed false information = structurally prevented, not self-suppressed) — the clean line is: neutralizing your *own* safeguard's effect = Disabled; circumventing/starving *another* control = Bypassed. (d) All external recovery controls (S8, S9) are `existence-time = incident-time` with `timeliness = too-late`, the distinction that stops "worked eventually" from being mis-scored as Working-in-time.

---

## INCIDENT 3 — C022 Optum / Impact Pro health risk algorithm

**Incident row.** `incident_id` 2013-2019-optum-impact-pro-bias · domain healthcare-clinical · date_start ~2013 (deployment) / date_end 2019 (external detection) · scope **systemic-program** · **observation_boundary:** the commercial cost-based care-management risk-prediction algorithm studied by Obermeyer et al. (2019), its label-choice bias and triage use; excludes other vendor products · harm_primary rights-discrimination · harm_secondary physical-safety (reduced access to care) · outcome realized-harm · system_type **confirmed-ML** · ai_causal_contribution **major-contributor** (race not an input; harm via the cost proxy) · attributed_primary_cause **organizational** (design/label choice, per Obermeyer et al. and NY DFS/DoH), sources Science 2019 (Obermeyer et al.), NY DFS/DoH letter 2019 · incident_confidence high.

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Target-label validation (does cost = need?) | model | preventive | Absent | post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | medium |
| S2 | Pre-deployment subgroup (racial) fairness audit | organizational-process | detective | Absent | post-incident-finding | confirmed-authoritative | latent-condition | not-applicable | incident-time | medium |
| S3 | Human clinical oversight / override in enrollment | human-operator | detective | Inadequate (design) | post-incident-finding | confirmed-authoritative | contributing | not-applicable | incident-time | medium |
| S4 | Deployment bias monitoring (internal) | organizational-process | detective | Absent | post-incident-finding | confirmed-authoritative | latent-condition | not-applicable | incident-time | medium |
| S5 | External research scrutiny (detection) | external-ecosystem | detective | Working | direct-artifact | confirmed-authoritative | mitigating | too-late | incident-time | high |
| S6 | External regulatory oversight (NY DFS/DoH) | external-ecosystem | recovery | Working | direct-artifact | confirmed-authoritative | mitigating | too-late | incident-time | medium |
| S7 | Vendor remediation: retrain on blended target (~84% bias cut) | model | recovery | Working | post-incident-finding | confirmed-authoritative | not-causally-relevant | in-time | **added-after** | medium |

Relationships: **S1 → S3** enabling (med): the unvalidated cost proxy produced biased scores that the clinical-override control could not correct. **S2 → S4** common-cause (med): both absences reflect one missing fairness-governance program. **S1 → S5** temporal-precedence (high): the design flaw long preceded external detection; no mechanism claim.

Contributing factors: **CF1** upstream structural inequity — less is historically spent on Black patients at equal illness, which the cost proxy imported (factor_type economic/cultural, effect harm-causing, role primary-upstream, basis post-incident-finding, conf high). This is the societal condition the algorithm encoded; it is not a safeguard, so it lives here.

**Calibration notes.** (a) **S3 Inadequate(design) is the deliberate contrast with the Dutch caseworkers (Bypassed).** Optum's clinicians were genuinely engaged and had full information about each patient; the control simply cannot perceive a population-level statistical skew from case-by-case review — that is a design inadequacy, not structural prevention. The Dutch reviewers, by contrast, were denied the information to function at all. Same "hollow oversight" appearance, opposite code. (b) S1/S2/S4 are coded **Absent** rather than Unknown+suspected: the authoritative post-incident finding (the Science paper demonstrating the bias was detectable by routine subgroup analysis) is the defensible basis that these checks should have existed — so the Absent evidentiary-basis rule is satisfied via post-incident-finding, at medium confidence to reflect the retrospective element.

---

## INCIDENT 4 — C060 Air Canada chatbot (recoded from pilot P3 to v0.2)

**Incident row.** `incident_id` 2022-air-canada-chatbot · domain consumer-chatbot · date 2022-11-11 (harm) · scope **discrete-event** · harm_primary financial-loss · outcome realized-harm · system_type **probable-ML** (the tribunal recorded no architecture detail; generative is likely but unconfirmed) · ai_causal_contribution **major-contributor** · attributed_primary_cause **organizational** (tribunal held Air Canada responsible; rejected the "chatbot is a separate entity" defense), source Moffatt v. Air Canada 2024 BCCRT 149 · incident_confidence high.

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Output grounding / verification vs real policy | application | preventive | **Unknown** (suspected_absent=true) | inferred-indirect | inferred-indirect | primary | not-applicable | incident-time | low |
| S2 | Human review of chatbot answers | human-operator | detective | Absent | established-practice | inferred-indirect | contributing | not-applicable | incident-time | low |
| S3 | Effective disclaimer / ToS carve-out | application | containment | Absent | comparable-system | single-source-reported | contributing | not-applicable | incident-time | medium |
| S4 | Linked correct policy page (reachability) | application | containment | Inadequate (design) | direct-artifact | confirmed-authoritative | contributing | not-applicable | incident-time | high |
| S5 | Pre-deployment accuracy testing | organizational-process | preventive | **Unknown** (suspected_absent=true) | inferred-indirect | inferred-indirect | latent-condition | not-applicable | incident-time | low |
| S6 | Organizational accountability ("separate entity" defense) | organizational-process | assurance-governance | Failed | direct-artifact | confirmed-authoritative | aggravating | too-late | incident-time | high |
| S7 | External adjudication (Civil Resolution Tribunal) | external-ecosystem | recovery | Working | direct-artifact | confirmed-authoritative | mitigating | too-late | incident-time | high |

Relationships: **S1 → S4** temporal-precedence (low): the answer contradicted the linked policy page, but the mechanism producing the contradiction is unknown, so A2 caps this at temporal. **S2 → S1** temporal-precedence (low): human review could in principle have caught the ungrounded answer, but no source asserts the mechanism, so it stays temporal. **S6 → S7** temporal-precedence (high): the rejected accountability defense preceded the remedy; ordering only.

Contributing factors: none coded.

**Calibration notes.** (a) **S1 vs S2 is the headline calibration contrast.** Both are "missing" controls, but S1 (grounding) has *no defensible basis* it existed given the undocumented architecture → **Unknown + suspected_absent**, never counted as Absent in any distribution. S2 (human review) has a weak-but-real **established-practice** basis → **Absent**, with confidence capped at low/medium per the 1.3.9 cap. This is exactly the discipline the Absent evidentiary-basis rule is meant to enforce. (b) S6 is the recurring assurance/governance-function gap (the "asserted-then-rejected" accountability posture); coded Failed under organizational-process and flagged for the deferred `asserted-rejected` state.

---

## INCIDENT 5 — C102 Gemini CLI file-destruction (agentic tool-use)

**Citation correction:** the canonical incident is GitHub issue **#4586** (July 2025, user Anuraag Gupta), corroborated by Winbuzzer, AI Incident Database #1178, and Fortune/Guardian reprints. Issue #15821 (Jan 2026) is a *separate* later report and is not coded here.

**Incident row.** `incident_id` 2025-gemini-cli-file-destruction · domain enterprise-agent · date 2025-07 · scope **discrete-event** · harm_primary security-compromise (irreversible data loss) · outcome realized-harm · system_type **confirmed-ML** · ai_causal_contribution **major-contributor** (the agent executed the destructive commands on hallucinated state) · attributed_primary_cause **AI-system** (agent's unverified action on confabulated filesystem state), sources GitHub issue #4586, AI Incident Database #1178 · incident_confidence medium (much of the root-cause detail is the model's own post-hoc self-report and the affected user's analysis, not a maintainer reproduction).

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Internal command-success verification (read-after-write) | application | detective | Failed | direct-artifact | single-source-reported | primary | too-late | incident-time | medium |
| S2 | Human confirmation before destructive commands | human-operator | preventive | **Unknown** | operator-claim | disputed | contributing | not-applicable | incident-time | low |
| S3 | Sandboxing / write-scope containment | infrastructure-environment | containment | Inadequate (operation) | direct-artifact | single-source-reported | contributing | not-applicable | incident-time | medium |
| S4 | Dry-run / preview of net effect | application | preventive | Absent | comparable-system | inferred-indirect | contributing | not-applicable | incident-time | medium |
| S5 | Backup / undo / recovery (snapshot, VCS) | infrastructure-environment | recovery | Absent | comparable-system, established-practice | multiply-reported | contributing | not-applicable | incident-time | medium |
| S6 | Real-time failure detection / auto-halt | application | detective | Failed | direct-artifact | single-source-reported | contributing | too-late | incident-time | medium |

Relationships: **S1 → S6** enabling (med): because the agent never verified the failed `mkdir` (S1), no real-time signal existed for a halt (S6) to fire on; mechanism asserted in the user's technical account. **S1 → S3** temporal-precedence (low): the unverified command preceded the in-scope destruction; scoping bounded reach but not in-scope harm. **S4 → S5** common-cause (low): both absent, reflecting a coding-agent run configured without guardrails.

Contributing factors: **CF1** user running the agent on un-version-controlled experimental files with sandbox disabled (factor_type other [user-configuration], effect harm-enabling, role contributing, basis direct-artifact, conf medium) — a usage condition that amplified harm; not a safeguard of the system itself.

**Calibration notes.** (a) **S2 is coded Unknown, deliberately not Bypassed or Working.** The tool has confirmation prompts by default and a YOLO/auto-approve bypass, but the sources genuinely do not establish whether prompts appeared, were approved, or were disabled in this run. Coding it Unknown (rather than guessing Bypassed) is the honest call and a good calibration precedent for agentic cases where the run configuration is unclear. (b) S3 Inadequate(operation): a write-scope restriction existed (the agent could not act outside the project dir) but was run with OS sandbox off, so it bounded blast radius without preventing in-scope destruction — an operational inadequacy, not a design one. (c) Low incident_confidence and single-source-reported evidence_status throughout reflect that the root cause rests on the model's confabulated self-report; the three-field evidence model keeps that honesty visible.

---

## Batch-1 quick stats (interaction-level, for a sanity check — NOT analysis)
Across the 5 incidents: 36 safeguard interactions coded (34 incident-time, 2 added-after) after the S3/S4 merge. Incident-time state spread: Absent 9, Working 7, Failed 7, Inadequate 4, Unknown 3 (2 with suspected_absent), Bypassed 2, Disabled 2. Contributing factors: 4. Illustrative of coding behavior only; no cross-incident analysis until all 30 are coded and locked.

## Batch-1 LOCKED calibration decisions (binding for the remaining 25)
1. **Governance/accountability controls** use the new fifth `control_function` value **assurance-governance** (framework v0.3, C12). Cruise S6 and Air Canada S6 re-coded accordingly.
2. **Coding granularity:** one row per named control (confirmed). Do not split into sub-mechanisms unless their `observed_state` genuinely diverges (then use `control_group`).
3. **Disabled covers deliberate suppression/deactivation of a safeguard's protective effect**, even where the control produced an output (Robodebt S2 legal advice = Disabled). Bypassed is reserved for circumvention or structural prevention of a control that was not itself self-suppressed (Robodebt S7 Ombudsman, Dutch caseworkers, Cruise remote operator).
4. **Merge controls that are the same underlying safeguard** rather than coding them as separate rows (Robodebt burden-of-proof merged into the human-verification control S3).
5. **Unchanged and confirmed:** Optum clinicians = Inadequate(design) vs Dutch caseworkers = Bypassed; Air Canada grounding = Unknown+suspected_absent vs human-review = Absent; Gemini confirmation prompt = Unknown (no guess); Cruise perception-at-impact = Failed.

These are binding and will not be reopened unless later evidence shows the underlying rule itself is defective.
