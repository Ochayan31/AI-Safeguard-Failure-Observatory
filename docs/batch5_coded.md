# AI Safeguard Failure Observatory
## Phase 1B — Batch 5, coded against CIR v0.3

**Incidents:** C018 2010 Flash Crash, C019 Zillow Offers, C024 IBM Watson for Oncology, C059 Mobley v. Workday, C081 Google Gemini image generation.
**Conventions:** the five Batch-1 locked decisions apply.
**Notable this batch:** the Flash Crash contributes a rare **Working containment** (the CME stop-logic pause) beside multiple absent controls; Watson is coded as a **patient-level near-miss** (unsafe recommendations produced and deployed, but human oversight prevented documented patient injury); Gemini is the dataset's **counterproductive-safeguard** case (a fairness intervention that itself produced integrity harm — coded as a safeguard that Failed by over-application, not a contributing factor); Workday is **ALLEGED** throughout (active litigation, low confidence).

---

## INCIDENT 21 — C018 2010 Flash Crash

**Incident row.** `incident_id` 2010-flash-crash · domain finance-trading · date 2010-05-06 · scope **discrete-event** · harm_primary financial-loss · outcome realized-harm · system_type **algorithmic-nonML** (volume-keyed execution algorithm + HFT + a layering/spoofing algorithm) · ai_causal_contribution **major-contributor** · attributed_primary_cause **multiple** (CFTC-SEC report's single-trigger narrative is itself debated; later Sarao spoofing added) · incident_confidence high (report authoritative; causal attribution debated).

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Execution-algorithm price/time limits | application | preventive | Absent | direct-artifact | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S2 | Market-wide circuit breakers | external-ecosystem | containment | Inadequate (design) | direct-artifact | confirmed-authoritative | contributing | not-applicable | incident-time | high |
| S3 | Single-stock circuit breakers | external-ecosystem | containment | Absent | direct-artifact | confirmed-authoritative | contributing | not-applicable | incident-time | high |
| S4 | Guard against nonsensical (stub-quote) executions | infrastructure-environment | containment | Absent | direct-artifact | confirmed-authoritative | contributing | not-applicable | incident-time | high |
| S5 | Spoofing / manipulation surveillance | external-ecosystem | detective | Failed | direct-artifact | confirmed-authoritative | contributing | too-late | incident-time | medium |
| S6 | CME Globex stop-logic pause | infrastructure-environment | containment | Working | direct-artifact | confirmed-authoritative | mitigating | in-time | incident-time | high |
| S7 | Broken-trade cancellation ("clearly erroneous") | external-ecosystem | recovery | Working | direct-artifact | confirmed-authoritative | mitigating | too-late | incident-time | medium |
| S8 | Post-incident: single-stock CBs, Limit-Up-Limit-Down, stub-quote ban, tighter CBs, CAT | external-ecosystem | containment | Working | direct-artifact | confirmed-authoritative | not-causally-relevant | in-time | **added-after** | high |

Relationships: **S1 → S4** enabling (medium): the price-blind sell algorithm drove prices into the stub-quote region where the absent nonsensical-execution guard let pennies-to-$100,000 trades print. **S2 → S3** common-cause (low): both circuit-breaker gaps reflect a containment regime calibrated only to daily thresholds. **S5 → S1** temporal-precedence (low): the undetected spoofing preceded/accompanied the algorithmic sell cascade, but the report's causal weighting is debated, so no stronger type.

Contributing factors: **CF1** the day's pre-existing macro stress (European debt-crisis fears; buy-side liquidity already down ~55% before the sell program) (factor_type economic, effect harm-amplifying, role contributing, basis direct-artifact, conf high).

**Coding notes.** S6 is a valuable **Working + in-time containment** — the CME's 5-second stop-logic pause halted the cascade and is the rare designed safeguard that fired correctly during the event, a useful counterweight to the many "worked-too-late" recoveries elsewhere. Nearly all structural fixes (S8) postdate the event and are `added-after`. `attributed_primary_cause = multiple` reflects that the report's single-trigger story is genuinely contested.

---

## INCIDENT 22 — C019 Zillow Offers iBuying collapse

**Incident row.** `incident_id` 2021-zillow-offers · domain finance-trading · date 2021-11-02 · scope **discrete-event** · harm_primary financial-loss · outcome realized-harm · system_type **probable-ML** (neural Zestimate seeded the live cash offers; exact production buy-model undisclosed) · ai_causal_contribution **major-contributor** · attributed_primary_cause **organizational** · incident_confidence high (Zillow filings) with reporting-only elements flagged.

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Price-forecast model accuracy / validation | model | preventive | Failed | operator-claim | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S2 | Human oversight of algorithmic buy decisions | human-operator | detective | Bypassed | multiply-reported | multiply-reported | primary | not-applicable | incident-time | medium |
| S3 | Risk limits on purchase volume / price | organizational-process | containment | Inadequate (design) | post-incident-finding | multiply-reported | contributing | not-applicable | incident-time | medium |
| S4 | Backtesting / stress-testing for volatile markets | organizational-process | assurance-governance | Inadequate (design) | post-incident-finding | inferred-indirect | latent-condition | not-applicable | incident-time | medium |
| S5 | Loss detection | organizational-process | detective | Working | operator-claim | confirmed-authoritative | mitigating | too-late | incident-time | high |
| S6 | Containment: wind-down + inventory sell-off | organizational-process | recovery | Working | direct-artifact | confirmed-authoritative | mitigating | too-late | incident-time | high |

Relationships: **S1 → S3** enabling (medium): the forecasting failure would have been survivable had volume/price risk limits bound; they did not, so mispriced buys scaled. **S2 → S1** enabling (medium): reporting that Zillow tuned the algorithm to "bid more aggressively" to chase growth loosened the human check that might have caught the drift. **S4 → S1** enabling (low): inadequate stress-testing is why the model's behavior in a turning market surprised the company.

Contributing factors: **CF1** competitive pressure in iBuying (vs Opendoor) driving aggressive buying (factor_type incentive-structure, effect harm-enabling, role contributing, basis multiply-reported, conf medium).

**Coding notes.** S1 Failed is directly supported by the CEO's own admission ("the unpredictability in forecasting home prices far exceeds what we anticipated"). S2 is coded **Bypassed** (the human oversight was loosened/routed around by tuning toward aggressive automated bidding) at medium confidence, since that narrative is well-reported but not company-confirmed — the evidence_status (multiply-reported) carries that caveat. S3/S4 are Inadequate-by-inference from the inventory blow-up and the CEO's surprise, not from a disclosed controls document — held at medium confidence. Unusually for the dataset, the recovery (S6) was decisive and the harm fell on the operator itself.

---

## INCIDENT 23 — C024 IBM Watson for Oncology

**Incident row.** `incident_id` 2018-ibm-watson-oncology · domain healthcare-clinical · date 2018-07 (STAT investigation; internal docs 2017) · scope **systemic-program** · **observation_boundary:** the MSK-trained commercial Watson for Oncology product, its synthetic-case training and unsafe recommendations as revealed by internal 2017 documents; excludes the separate MD Anderson project (context only) · harm_primary information-integrity (unsafe/incorrect clinical recommendations) · harm_secondary physical-safety · outcome **realized-harm** at the product/organizational level; **patient-level harm was a near-miss** (no documented patient injury) · system_type **confirmed-ML** · ai_causal_contribution **major-contributor** · attributed_primary_cause **organizational** · incident_confidence medium (STAT via internal docs; IBM disputes framing).

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Training-data validity (real-world evidence grounding) | model | preventive | Absent | direct-artifact | multiply-reported | primary | not-applicable | incident-time | high |
| S2 | Clinical / outcome validation before deployment | organizational-process | assurance-governance | Inadequate (design) | direct-artifact | multiply-reported | primary | not-applicable | incident-time | high |
| S3 | Marketing / deployment honesty (claims match reality) | organizational-process | assurance-governance | Failed | direct-artifact | multiply-reported | aggravating | not-applicable | incident-time | high |
| S4 | Physician oversight / override (human in the loop) | human-operator | containment | Working | operator-claim | multiply-reported | mitigating | in-time | incident-time | medium |
| S5 | Detection (internal decks + client complaints) | organizational-process | detective | Working | direct-artifact | confirmed-authoritative | mitigating | too-late | incident-time | high |
| S6 | Incident-time remediation (patching, continued sale) | organizational-process | recovery | Inadequate (operation) | direct-artifact | multiply-reported | not-causally-relevant | too-late | incident-time | medium |
| S7 | Later: wind-down + divestiture (→ Merative 2022) | organizational-process | recovery | Working | direct-artifact | confirmed-authoritative | not-causally-relevant | in-time | **added-after** | high |

Relationships: **S1 → S2** enabling (high): training on a few doctors' synthetic cases is why validation could only ever be circular concordance-to-those-doctors rather than outcome validation. **S3 → S4** masking (medium): marketing that the advice rested on real patient data eroded the appropriate skepticism the physician-override safeguard depends on, weakening (but not defeating) it. **S5 → S6** temporal-precedence (high): internal and client detection preceded the inadequate patch-and-continue response.

**Coding notes.** The careful harm distinction is coded explicitly: S4 (physician oversight) is **Working + mitigating + in-time** and is the most plausible reason no patient injury is documented — which is why patient-level harm is recorded as a near-miss while the product-/trust-level harm is realized. S1 Absent applies specifically to *real-world-evidence grounding* (IBM/MSK would defend synthetic expert curation as a design choice — noted). S3 is another **assurance-governance Failed** (marketing claims contradicted internal knowledge), the same accountability pattern as Facebook and Cruise.

---

## INCIDENT 24 — C059 Mobley v. Workday [ALLEGED; active litigation]

**Care note.** Active, contested litigation; the 2024–2025 rulings decide procedural questions (motion-to-dismiss survival; conditional ADEA collective certification), NOT whether discrimination occurred. All safeguard states are ALLEGED and coded at low-to-medium confidence with disputed evidence_status.

**Incident row.** `incident_id` 2023-2025-mobley-workday · domain hiring-HR · date_start 2023 (filed) / ongoing · scope **systemic-program** · **observation_boundary:** the allegations and rulings in Mobley v. Workday regarding AI applicant-screening and discrimination; excludes adjudicated liability (none yet) · harm_primary rights-discrimination · outcome realized-harm (alleged) · system_type **probable-ML** · ai_causal_contribution **disputed** (unadjudicated) · attributed_primary_cause **disputed** · incident_confidence low.

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Bias audit / disparate-impact testing | organizational-process | assurance-governance | Absent | post-incident-finding | disputed | primary | not-applicable | incident-time | low |
| S2 | Transparency to applicants (explainability of screening) | application | assurance-governance | Absent | post-incident-finding | disputed | contributing | not-applicable | incident-time | low |
| S3 | Human oversight of automated screening | human-operator | detective | Bypassed | post-incident-finding | disputed | primary | not-applicable | incident-time | low |
| S4 | Vendor accountability ("agent" liability under anti-discrimination law) | external-ecosystem | assurance-governance | Working | direct-artifact | confirmed-authoritative | mitigating | too-late | incident-time | medium |
| S5 | Regulatory oversight (EEOC amicus; ADEA collective certification) | external-ecosystem | detective | Working | direct-artifact | confirmed-authoritative | mitigating | too-late | incident-time | medium |
| S6 | External bias-audit regime (NYC Local Law 144, separate jurisdiction) | external-ecosystem | assurance-governance | Inadequate (enforcement) | research-evidence | multiply-reported | not-causally-relevant | in-time | **added-after** | medium |

Relationships: **S1 → S3** enabling (low): if adequate disparate-impact testing was absent, the near-instant automated rejections (pled as evidence of no human review) could proceed unchecked; both states are alleged. **S3 → S2** common-cause (low): opaque, automated screening bundles the transparency and human-oversight gaps.

**Coding notes.** The one clearly **CONFIRMED** element is S4/S5: the court's "agent" ruling (a software vendor can face direct anti-discrimination liability) and the EEOC amicus + conditional ADEA certification are real events, coded Working, even though the underlying discrimination is unproven. This makes Workday a useful case for the *accountability-safeguard* axis (the legal system supplying a vendor-accountability control that did not exist ex ante) while keeping every product-side state at low confidence and disputed evidence_status. S6 (NYC LL144) is `added-after` and Inadequate-enforcement per compliance research, and is a separate jurisdiction — included as an emerging external safeguard, not a control on this incident.

---

## INCIDENT 25 — C081 Google Gemini image generation [counterproductive-safeguard case]

**Incident row.** `incident_id` 2024-google-gemini-image-generation · domain content-moderation · date 2024-02 · scope **discrete-event** · harm_primary information-integrity · outcome realized-harm (low severity: historically false images, reputational) · system_type **confirmed-ML** · ai_causal_contribution **major-contributor** · attributed_primary_cause **organizational** (Google's tuning/launch choices) · incident_confidence high (Google's own admissions).

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Demographic-bias fairness tuning | model | preventive | Failed | operator-claim | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S2 | Context / historical-accuracy gate | application | preventive | Absent | operator-claim | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S3 | Over-refusal safety layer (prompt sensitivity) | model | preventive | Failed | operator-claim | confirmed-authoritative | contributing | not-applicable | incident-time | high |
| S4 | Pre-launch testing / red-teaming | organizational-process | assurance-governance | Inadequate (design) | operator-claim | inferred-indirect | latent-condition | not-applicable | incident-time | medium |
| S5 | Internal detection (pre-public) | organizational-process | detective | Failed | direct-artifact | confirmed-authoritative | contributing | too-late | incident-time | high |
| S6 | Feature pause / kill-switch | application | containment | Working | direct-artifact | confirmed-authoritative | mitigating | in-time | incident-time | high |
| S7 | Later: re-release on Imagen 3 with new evals/red-teaming/principles | model | preventive | Working | direct-artifact | confirmed-authoritative | not-causally-relevant | in-time | **added-after** | high |

Relationships: **S1 → S2** enabling (high): the global "show a range of people" tuning produced the harm precisely because the context/accuracy gate that should have suppressed it for historically-constrained prompts was absent. **S3 → harm** (contributing): the over-refusal layer compounded it by rejecting anodyne prompts. **S5 → S6** enabling (high): internal detection failing (caught externally by users) is why containment was reactive rather than proactive.

Contributing factors: none coded — the diversity tuning is coded as a *safeguard that failed* (S1), not a contributing factor, because it is a genuine fairness control that misfired rather than a non-safeguard driver.

**Coding notes.** This is the dataset's clearest **counterproductive-safeguard** case: S1, a fairness intervention intended to counter demographic bias, is the proximate cause of an integrity harm because it was applied without a context gate (S2 Absent). Coding it as `observed_state = Failed` on a preventive control (rather than shunting it to contributing_factors) is deliberate — it *is* a safeguard, and "a safeguard whose failure mode is over-correction" is a finding worth surfacing. S6 (fast feature pause) is a clean **Working + in-time** containment, the inverse counterpart to S1.

---

## Batch-5 quick stats (interaction-level, NOT analysis)
41 safeguard interactions coded (37 incident-time, 4 added-after). Incident-time state spread: Absent 9, Working 11, Inadequate 8, Failed 7, Bypassed 2, Disabled 0, Unknown 0, Disputed 0. Contributing factors: 3. Cumulative Batches 1–5: **25 of 30 incidents coded.**

## Running cross-incident observations (not yet analysis)
- **Working** jumped this batch, driven by cases with genuine functioning controls: the Flash Crash CME pause and post-hoc reforms, Zillow's decisive exit, Watson's physician override, Gemini's feature pause, and the Workday accountability rulings. A useful corrective to any impression that the dataset is all failure.
- **in-time** timeliness appeared several times this batch (Flash Crash S6, Watson S4, Gemini S6) — all *containment/oversight at the point of action*, contrasting with the *external recoveries* that are almost always too-late.
- The **counterproductive-safeguard** pattern (Gemini) and the **near-miss-averted-by-human-oversight** pattern (Watson) are both new this batch and worth their own mention in the eventual analysis.
- 5 incidents remain (C003 Tesla Mountain View, C007 Tesla 2M-recall, C047 Rotterdam welfare fraud, C094 e-rater essay scoring, C101 Iberian blackout).
