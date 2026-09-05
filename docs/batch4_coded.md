# AI Safeguard Failure Observatory
## Phase 1B — Batch 4, coded against CIR v0.3

**Incidents:** C042 Michigan MiDAS, C070 Raine v. OpenAI, C083 Facebook Files (Instagram teens), C099 VW Dieselgate, C027 pulse-oximeter racial bias.
**Conventions:** the five Batch-1 locked decisions apply.
**Care notes:** C070 (a teen suicide in active litigation, transcripts under seal) is coded soberly with low confidence and explicit ALLEGED/CONFIRMED markers; nothing method-specific is recorded. C099 is the archetypal **safeguard-defeated-by-design** case (the emissions test, Bypassed). C042 gives a second flagship **Disabled** (human review designed out), parallel to Robodebt. C083 is the clearest **detection-worked-but-was-ignored** case.

---

## INCIDENT 16 — C042 Michigan MiDAS unemployment-fraud false accusations

**Incident row.** `incident_id` 2013-2015-us-mi-midas · domain government-benefits · date_start 2013-10 / date_end 2015-08 · scope **systemic-program** · **observation_boundary:** MiDAS auto-adjudication of unemployment fraud with no human review (Oct 2013–Aug 2015) and the ~40,000 false accusations (~93% error); excludes broader UIA operations · harm_primary financial-loss · harm_secondary psychological-social · outcome realized-harm · system_type **algorithmic-nonML** (deterministic rules: mismatch-as-fraud, income-spreading) · ai_causal_contribution **major-contributor** · attributed_primary_cause **organizational** · incident_confidence high.

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Human review before fraud determination / penalty | human-operator | preventive | **Disabled** | direct-artifact, post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S2 | Evidentiary-basis requirement (real evidence, not inference) | organizational-process | preventive | Absent | regulation-policy, post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S3 | Adequate notice / due process | application | preventive | Failed | direct-artifact | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S4 | Pre-deployment testing / validation | organizational-process | assurance-governance | Inadequate (design) | post-incident-finding | multiply-reported | latent-condition | not-applicable | incident-time | medium |
| S5 | Internal governance / response to the error signal | organizational-process | detective | Failed | post-incident-finding | confirmed-authoritative | contributing | too-late | incident-time | high |
| S6 | External oversight: Auditor General | external-ecosystem | detective | Working | direct-artifact | confirmed-authoritative | mitigating | too-late | incident-time | high |
| S7 | External oversight: courts (Bauserman/Cahoo) | external-ecosystem | recovery | Working | direct-artifact | confirmed-authoritative | mitigating | too-late | incident-time | high |
| S8 | Post-incident: human review mandated + refunds + settlement + penalty caps | organizational-process | preventive | Working | direct-artifact | confirmed-authoritative | not-causally-relevant | in-time | **added-after** | high |

Relationships: **S1 → S3** enabling (medium): removing human review is why auto-generated notices reached dormant accounts with no sanity check. **S1 → S2** common-cause (high): both reflect the single decision to auto-adjudicate fraud. **S5 → S6** **masking** (medium): the agency's defensiveness and refusal of transparency delayed the Auditor General's detection.

Contributing factors: **CF1** the fraud-recovery incentive (penalties up to 400%, highest in the US) rewarding aggressive determinations (factor_type incentive-structure, effect harm-enabling, role aggravating, basis post-incident-finding, conf medium).

**Coding notes.** S1 is the batch's flagship **Disabled**, mirroring Robodebt S3: a human-verification checkpoint that exists in normal adjudication was deliberately designed out of the automated pathway (Cahoo: "no human being took part in this process") and later restored — deliberate deactivation of a safeguard's protective effect. This is now the second public-administration case with the same Disabled signature.

---

## INCIDENT 17 — C070 Raine v. OpenAI [sensitive; litigation, mostly alleged]

**Care note.** This concerns a 16-year-old's suicide and is in active litigation with the core transcripts under court seal. Everything below is coded at low confidence with ALLEGED/CONFIRMED markers; OpenAI denies liability and attributes causation to other factors. No method-specific content is recorded.

**Incident row.** `incident_id` 2024-2025-raine-openai-chatgpt · domain consumer-chatbot · date_start 2024-09 / date_end 2025-04-11 · scope **discrete-event** · harm_primary psychological-social · outcome realized-harm · system_type **confirmed-ML** (GPT-4o) · ai_causal_contribution **disputed** (contested; causation not adjudicated) · attributed_primary_cause **disputed** · incident_confidence **low** (sealed transcripts; allegations).

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Self-harm refusal / crisis-resource guardrails | model | preventive | Bypassed | operator-claim, direct-artifact | disputed | primary | not-applicable | incident-time | low |
| S2 | Long-conversation safety-degradation control | model | preventive | Failed | operator-claim | confirmed-authoritative | primary | not-applicable | incident-time | medium |
| S3 | Age verification / minor protections | application | preventive | Absent | established-practice | inferred-indirect | contributing | not-applicable | incident-time | medium |
| S4 | Crisis escalation / human handoff | human-operator | recovery | Absent | comparable-system | inferred-indirect | contributing | not-applicable | incident-time | medium |
| S5 | Self-harm detection with intervention | application | detective | Failed | operator-claim | disputed | primary | too-late | incident-time | low |
| S6 | Post-incident: sensitive-chat routing, parental controls, age prediction, emergency contacts | application | recovery | Working | operator-claim | multiply-reported | not-causally-relevant | in-time | **added-after** | medium |

Relationships: **S2 → S1** enabling (low): OpenAI's confirmed admission that safety training can degrade over long conversations is the alleged mechanism by which the guardrails became bypassable; low confidence because the case-specific chain is sealed. **S5 → S4** enabling (low): detection allegedly flagged the content but no escalation path existed to act on it.

Contributing factors: none coded as established; the litigation dispute over causation (OpenAI alleges pre-existing factors and circumvention; plaintiffs allege guardrail removal) is recorded at the incident level as `ai_causal_contribution = disputed` rather than as a one-sided factor.

**Coding notes.** The one **CONFIRMED** safeguard finding is S2: OpenAI publicly admitted safety training "can sometimes become less reliable in long interactions where parts of the model's safety training may degrade." S1 is coded **Bypassed** (guardrails present but defeated by fiction/"world-building" framing, per the complaint); the plaintiffs' further allegation that a categorical-refusal protocol was deliberately removed (which would be Disabled) is contested and recorded in notes, not as the coded state. S3 and S4 are **Absent** and corroborated by OpenAI announcing them as new post-incident measures. Low incident_confidence and disputed evidence_status throughout keep the honesty visible; this row should not be used for any confident cross-incident claim.

---

## INCIDENT 18 — C083 Facebook Files (Instagram engagement ranking & teen harm)

**Incident row.** `incident_id` 2019-2021-facebook-files-instagram-teens · domain content-moderation · date_start 2019 / date_end 2021-10 (revealed) · scope **systemic-program** · **observation_boundary:** Instagram's engagement-based recommendation/ranking and its documented teen-mental-health harms as evidenced by Meta's internal 2019–2021 research and the 2021 disclosures; excludes the later Teen Accounts era · harm_primary psychological-social · outcome realized-harm · system_type **confirmed-ML** (engagement-optimizing ranking models) · ai_causal_contribution **contributory-non-necessary** (amplification contributed; teen mental-health harm is multifactorial and the internal evidence is self-report/correlational) · attributed_primary_cause **organizational** · incident_confidence medium (self-report research; Meta disputes the framing).

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Internal harm-detection research | organizational-process | detective | Working | direct-artifact | confirmed-authoritative | not-causally-relevant | in-time | incident-time | high |
| S2 | Product-safety response to internal findings | organizational-process | recovery | Failed | direct-artifact, post-incident-finding | multiply-reported | primary | not-applicable | incident-time | medium |
| S3 | Vulnerable-user recommendation guardrails | application | preventive | Inadequate (operation) | post-incident-finding | multiply-reported | primary | not-applicable | incident-time | medium |
| S4 | Transparency / honest disclosure (public & Congress) | organizational-process | assurance-governance | Failed | direct-artifact | confirmed-authoritative | aggravating | too-late | incident-time | high |
| S5 | External oversight (SEC complaints, Senate hearings) | external-ecosystem | detective | Working | direct-artifact | confirmed-authoritative | mitigating | too-late | incident-time | medium |
| S6 | Post-incident: Instagram Kids paused, Take a Break, later Teen Accounts | application | preventive | Working | direct-artifact | multiply-reported | not-causally-relevant | in-time | **added-after** | medium |

Relationships: **S1 → S2** temporal-precedence (high): the internal research detected and quantified the harm; the product-safety response then failed to act on it — the broken escalation-to-action loop is the signature, but we do not assert a stronger mechanism than sequence. **S4 → S5** **masking** (medium): public downplaying (Meta's "not conclusive" / "not toxic") masked the harm from regulators and the public until the leak forced oversight. **S2 → S3** enabling (medium): the failure to act on internal findings is why the vulnerable-user guardrails stayed inadequate.

Contributing factors: **CF1** the engagement-maximizing business incentive that set the ranking objective (factor_type incentive-structure, effect harm-enabling, role primary-upstream, basis post-incident-finding, conf medium).

**Coding notes.** S1 is the dataset's cleanest **detection Working but ignored**: the internal research safeguard functioned exactly as a detection control should (harm measured and documented), so its state is Working even though the incident is a failure — because the *response* control (S2) Failed. Separating these two is what lets the data say "they knew" without conflating knowing with acting. S4 (public contradiction of internal findings) is an **assurance-governance** Failed, the same accountability-control failure seen at Cruise and Air Canada.

---

## INCIDENT 19 — C099 Volkswagen "Dieselgate" defeat device

**Incident row.** `incident_id` 2015-vw-dieselgate · domain environmental · date_start ~2009 / date_end 2015-09 (revealed) · scope **systemic-program** · **observation_boundary:** the 2.0L TDI defeat-device software (MY2009–2015, ~475–500k US vehicles) and its defeat of emissions testing; the separate 3.0L matter and non-US markets are context only · harm_primary environmental · outcome realized-harm · system_type **algorithmic-nonML** (deterministic test-detection logic; deliberate deception) · ai_causal_contribution **major-contributor** · attributed_primary_cause **organizational** · incident_confidence high.

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Regulatory emissions certification test | external-ecosystem | detective | **Bypassed** | direct-artifact, post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S2 | On-road / in-use emissions testing | external-ecosystem | detective | Absent | comparable-system, post-incident-finding | confirmed-authoritative | contributing | not-applicable | incident-time | high |
| S3 | Internal governance / engineering-ethics controls | organizational-process | preventive | Failed | direct-artifact | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S4 | Certification / type-approval oversight (self-certification) | external-ecosystem | assurance-governance | Inadequate (enforcement) | direct-artifact | confirmed-authoritative | contributing | not-applicable | incident-time | high |
| S5 | Detection (ICCT/WVU on-road study) | external-ecosystem | detective | Working | direct-artifact | confirmed-authoritative | mitigating | too-late | incident-time | high |
| S6 | Accountability / recovery (EPA NOV, $14.7bn + $4.3bn, criminal plea, SEC) | external-ecosystem | recovery | Working | direct-artifact | confirmed-authoritative | mitigating | too-late | incident-time | high |
| S7 | Post-incident: recalls + EU Real-Driving-Emissions (PEMS) on-road testing | external-ecosystem | detective | Working | direct-artifact | confirmed-authoritative | not-causally-relevant | in-time | **added-after** | high |

Relationships: **S3 → S1** enabling (high): the internal-governance failure is what allowed a defeat device to be designed and installed to beat the test. **S2 → S5** enabling (high): the absence of routine on-road testing is why detection depended on a fortuitous external study rather than the regulatory process. **S4 → S1** enabling (medium): the self-certification trust model is the specific oversight weakness the defeat exploited.

Contributing factors: **CF1** the commercial mandate to market "clean diesel" at scale while simultaneously meeting emissions, performance, and cost targets (factor_type incentive-structure, effect harm-causing, role primary-upstream, basis post-incident-finding, conf medium-high).

**Coding notes.** S1 is the archetypal **Bypassed**: a real external regulatory safeguard (the emissions test) that VW did not switch off but *defeated by design* — software detected the test and behaved compliantly only during it. This is circumvention of another control, the textbook Bypassed under the locked rule (as opposed to Disabled, which would be deactivating one's own control). The whole incident is unusual in that the harm was *intended*, which is why `attributed_primary_cause` is cleanly organizational and every internal control is Failed rather than merely inadequate.

---

## INCIDENT 20 — C027 Pulse-oximeter racial bias

**Incident row.** `incident_id` 2020-pulse-oximeter-racial-bias · domain healthcare-clinical · date surfaced 2020 (Sjoding et al.; bias long-standing) · scope **systemic-program** · **observation_boundary:** racial bias in pulse-oximeter SpO2 estimation from unrepresentative calibration (surfaced 2020) and the resulting occult hypoxemia / treatment delays; focuses on the calibration and regulatory-testing failure · harm_primary physical-safety · harm_secondary rights-discrimination · outcome realized-harm · system_type **algorithmic-nonML** (data-derived, non-learned calibration curve) · ai_causal_contribution **major-contributor** · attributed_primary_cause **organizational** (device design + FDA testing standard) · incident_confidence high.

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Representative calibration data (diverse skin tones) | model | preventive | Absent | post-incident-finding, comparable-system | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S2 | FDA premarket clearance testing standard (skin-tone diversity) | external-ecosystem | assurance-governance | Inadequate (enforcement) | post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S3 | Clinical-awareness / labeling of the bias | application | detective | Inadequate (design) | direct-artifact | confirmed-authoritative | contributing | too-late | incident-time | high |
| S4 | Post-market surveillance / detection | organizational-process | detective | Failed | post-incident-finding | confirmed-authoritative | latent-condition | too-late | incident-time | high |
| S5 | Post-incident: FDA panel (2022), meeting (2024), draft guidance (2025, Monk scale) | external-ecosystem | assurance-governance | Working | direct-artifact | confirmed-authoritative | not-causally-relevant | in-time | **added-after** | medium |

Relationships: **S2 → S1** enabling (high): the inadequate FDA testing bar (as few as ~2 dark-skinned subjects) is what permitted unrepresentative calibration to reach market. **S4 → S3** temporal-precedence (high): the bias was known in small studies from ~2005 but post-market surveillance did not surface it; the late labeling followed only after external research. 

Contributing factors: **CF1** the historical structural under-representation of dark-skinned individuals in clinical/calibration research (factor_type cultural, effect harm-enabling, role primary-upstream, basis research-evidence, conf high).

**Coding notes.** Cleanly **omission-dominated**: the two root controls (representative calibration S1, adequate regulatory testing S2) are Absent/Inadequate. S5 (remediation) is marked Working but is genuinely still in progress (2025 draft guidance is non-binding) — coded added-after and not counted in incident-time distributions, with the "not yet binding" caveat in notes. The agent's point that this is a data-representativeness failure in a *non-ML* system is worth flagging for the eventual analysis: the same failure mode as ML training-data bias, without any ML.

---

## Batch-4 quick stats (interaction-level, NOT analysis)
38 safeguard interactions coded (33 incident-time, 5 added-after). Incident-time state spread: Failed 10, Absent 8, Working 6, Inadequate 6, Bypassed 2, Disabled 1, Unknown 0. Contributing factors: 5. Cumulative Batches 1–4: **20 of 30 incidents coded.**

## Running cross-incident observations (not yet analysis)
- **Failed** rose sharply this batch, driven by the intentional-deception cases (VW: every internal control Failed) and the "detected-but-not-acted-on" governance failures (Facebook, MiDAS).
- The **detection-worked-but-ignored** pattern (Facebook S1, MiDAS S6, and the Dutch/Boeing warnings from earlier) is now firmly a recurring signature distinct from pure omission — a strong candidate finding.
- **assurance-governance** now spans disclosure, validation, certification, testing-standards, and impact-assessment controls across all four batches; it is carrying a large and coherent share of the governance-layer failures.
- Only 10 incidents remain (C003, C007, C018, C019, C024, C047, C059, C081, C094, C101).
