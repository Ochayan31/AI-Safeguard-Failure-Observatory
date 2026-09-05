# AI Safeguard Failure Observatory
## Phase 1B — Batch 6 (final), coded against CIR v0.3

**Incidents:** C003 Tesla Autopilot (Mountain View/Huang), C007 Tesla 2M-vehicle Autopilot recall, C047 Rotterdam welfare-fraud scoring, C094 ETS e-rater / BABEL, C104 Amazon Q supply-chain injection.
**Selection note:** C101 (2025 Iberian blackout) was **excluded at the coding stage** as ineligible — close research established it as a conventional grid-engineering/voltage-control failure with only classical protective-relay automation (static thresholds) in the causal chain and no AI/ML or algorithmic *decision* system (E1 fail; the Spanish Senate explicitly found it was not an automated-system breakdown). Per the frozen selection rule (`select_sample_v2.py`, C101 marked ineligible), the deterministic backfill is **C104 (Amazon Q)**; all other 29 held. This is logged in the selection amendment note.
**Conventions:** the five Batch-1 locked decisions apply.
**Notable this batch:** e-rater demonstrates the **`control_group` state-divergence split** (one human-oversight control, Working in high-stakes vs Absent where the machine scores alone); Amazon Q is a **Bypassed access control + Unknown agent guardrails** near-miss; the two Tesla cases deliberately parallel C002 (recurrence is data, not redundancy).

---

## INCIDENT 26 — C003 Tesla Autopilot fatal crash (Mountain View / Walter Huang)

**Incident row.** `incident_id` 2018-tesla-autopilot-mountain-view · domain autonomous-vehicle · date 2018-03-23 · scope **discrete-event** · harm_primary physical-safety · outcome realized-harm · system_type **confirmed-ML** · ai_causal_contribution **major-contributor** · attributed_primary_cause **multiple** (NTSB: Autopilot steering into the gore + driver distraction/over-reliance + Tesla design permitting it + damaged crash attenuator + NHTSA's non-regulatory approach) · incident_confidence high.

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Perception / obstacle (barrier) detection + AEB | application | preventive | Inadequate (design) | post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S2 | Driver-attention monitoring | application | detective | Inadequate (design) | post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S3 | Operational-design-domain restriction | application | preventive | Absent | comparable-system, post-incident-finding | confirmed-authoritative | contributing | not-applicable | incident-time | high |
| S4 | Driver attention / intervention (human) | human-operator | recovery | Failed | post-incident-finding | confirmed-authoritative | primary | too-late | incident-time | medium |
| S5 | Highway crash attenuator (infrastructure) | external-ecosystem | containment | Failed | post-incident-finding | confirmed-authoritative | contributing | too-late | incident-time | high |
| S6 | Federal (NHTSA) oversight of partial automation | external-ecosystem | assurance-governance | Inadequate (enforcement) | post-incident-finding | confirmed-authoritative | latent-condition | not-applicable | incident-time | high |
| S7 | Post-incident: NTSB recommendations + attenuator repair | external-ecosystem | assurance-governance | Working | direct-artifact | confirmed-authoritative | not-causally-relevant | in-time | **added-after** | high |

Relationships: **S2 → S4** enabling (high): torque-only monitoring permitted the driver's distraction (NTSB: likely a phone game). **S3 → S1** enabling (medium): engaging Autopilot at a known-problematic gore point is where the perception design limit bit. **S5 → outcome** aggravating: the already-crushed, unrepaired attenuator increased crash severity.

Contributing factors: **CF1** Apple's lack of a distracted-driving policy for the employee-driver (factor_type organizational, effect harm-enabling, role contributing, basis post-incident-finding, conf medium).

**Coding notes.** Deliberately parallel to C002 (Tesla/Brown): S1 Inadequate(design), S2 Inadequate(design), S3 Absent, S4 Failed. Two independent NTSB-investigated Autopilot fatalities sharing the same four-safeguard signature is a *finding about recurrence*, not duplicate coding — the framework should show the pattern, and the two incidents remain distinct records. S5 (crash attenuator) is a Failed external containment (Caltrans/CHP), and S6 uses **assurance-governance** for the regulatory-oversight failure NTSB explicitly criticized.

---

## INCIDENT 27 — C007 Tesla ~2M-vehicle Autopilot recall (NHTSA EA22-002)

**Incident row.** `incident_id` 2023-tesla-autopilot-2m-recall · domain autonomous-vehicle · date 2023-12-12 · scope **systemic-program** · **observation_boundary:** NHTSA's finding that Autopilot driver-engagement controls were insufficient to prevent foreseeable misuse across ~2M vehicles, and the Dec 2023 recall, based on the crash set including stationary-emergency-vehicle collisions; excludes individual crash specifics · harm_primary physical-safety · outcome realized-harm · system_type **confirmed-ML** · ai_causal_contribution **major-contributor** · attributed_primary_cause **organizational** (Tesla's engagement-control design) with driver misuse · incident_confidence high.

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Driver-engagement monitoring controls | application | detective | Inadequate (design) | post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S2 | Operational-design-domain / misuse limiting | application | preventive | Inadequate (design) | post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S3 | Regulatory oversight (NHTSA EA22-002 investigation) | external-ecosystem | detective | Working | direct-artifact | confirmed-authoritative | mitigating | too-late | incident-time | high |
| S4 | Recall remedy (OTA: alerts, checks, Autosteer strike-out) | application | detective | Inadequate (operation) | direct-artifact | multiply-reported | not-causally-relevant | delayed | **added-after** | medium |

Relationships: **S1 → S3** temporal-precedence (high): the inadequate engagement controls are what NHTSA's investigation eventually caught and forced to recall; ordering, not a stronger claim. **S1 → S2** common-cause (medium): both reflect a design that permitted foreseeable misuse.

Contributing factors: **CF1** the "Autopilot"/"Full Self-Driving" naming and marketing that encourage over-reliance (factor_type other [marketing], effect harm-enabling, role contributing, basis multiply-reported, conf medium).

**Coding notes.** S4 (the recall remedy) is `added-after` and coded **Inadequate(operation)** rather than Working, because NHTSA opened recall-query RQ24009 into the remedy's effectiveness (post-remedy crashes; parts of the fix are driver-selectable/reversible) — a rare case where the dataset records a *remediation that is itself under investigation*. S3 (the NHTSA investigation) is the Working detective control here, the regulatory counterpart to the individual-crash cases.

---

## INCIDENT 28 — C047 Rotterdam welfare-fraud risk scoring

**Incident row.** `incident_id` 2017-2021-nl-rotterdam-fraud · domain government-benefits · date_start 2017 / date_end 2021 · scope **systemic-program** · **observation_boundary:** Rotterdam's gradient-boosting welfare-fraud risk-scoring model (~2017–2021; ~30,000 recipients scored, top ~1,000/yr investigated) and its discriminatory scoring, as audited by Lighthouse/WIRED and the Rotterdam Court of Audit; excludes other municipalities · harm_primary rights-discrimination · harm_secondary psychological-social · outcome realized-harm · system_type **confirmed-ML** (gradient-boosting / xgboost) · ai_causal_contribution **major-contributor** · attributed_primary_cause **organizational** · incident_confidence high (auditors obtained the actual model, code, and training data).

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Pre-deployment bias / fairness audit | organizational-process | assurance-governance | Absent | post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S2 | Feature / data governance (proxy & subjective-feature control) | model | preventive | Inadequate (design) | post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S3 | Meaningful individual human review of flagged cases | human-operator | detective | Inadequate (operation) | post-incident-finding | disputed | contributing | not-applicable | incident-time | medium |
| S4 | Transparency to affected people | application | assurance-governance | Absent | post-incident-finding | confirmed-authoritative | latent-condition | not-applicable | incident-time | high |
| S5 | Governance / Court-of-Audit oversight (incl. DPIA) | organizational-process | assurance-governance | Inadequate (design) | direct-artifact | confirmed-authoritative | latent-condition | not-applicable | incident-time | high |
| S6 | Internal detection during operation | organizational-process | detective | Failed | post-incident-finding | confirmed-authoritative | contributing | not-applicable | incident-time | high |
| S7 | External oversight & recovery (Rekenkamer 2021; audit 2023; suspension) | external-ecosystem | recovery | Working | direct-artifact | confirmed-authoritative | mitigating | too-late | incident-time | high |

Relationships: **S1 → S2** enabling (medium): the absent fairness audit is why the discriminatory proxy/subjective features were never caught. **S4 → S3** enabling (medium): opacity undercut the individual human review. **S6 → S7** temporal-precedence (high): the internal-detection failure is why correction depended on external audit and journalism.

Contributing factors: **CF1** fraud-detection efficiency/cost pressure prioritizing hit-rate over fairness (factor_type incentive-structure, effect harm-enabling, role contributing, basis post-incident-finding, conf medium).

**Coding notes.** Deliberately parallel to C039 (Dutch Toeslagen): both are Dutch welfare-fraud scoring, but distinct systems (municipal ML model vs national tax-authority system) and coded independently. Key difference from Toeslagen: S3 here is **Inadequate(operation)** with **evidence_status = disputed** — the city claims flagged cases always had human review while critics document rubber-stamping; the reviewers were not as clearly denied information as the Toeslagen caseworkers (who were Bypassed), so Inadequate-with-disputed-evidence is the honest call rather than Bypassed.

---

## INCIDENT 29 — C094 ETS e-rater / BABEL automated-essay-scoring validity failure

**Incident row.** `incident_id` erater-babel-aes-validity · domain education · date ~2014 (BABEL demonstration) onward · scope **systemic-program** · **observation_boundary:** the construct-validity and adversarial-robustness failure of ETS e-rater automated essay scoring as demonstrated by the BABEL generator (2014) and ETS's response; focuses on e-rater, with other AES engines as context · harm_primary information-integrity (invalid assessment) · outcome realized-harm (in sole-scorer deployments; high-stakes harm mitigated by human pairing) · system_type **confirmed-ML** (NLP/statistical, trained on human-scored essays) · ai_causal_contribution **major-contributor** · attributed_primary_cause **organizational** · incident_confidence high.

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf | control_group |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Construct validity (measures writing quality, not surface proxies) | model | preventive | Failed | research-evidence, direct-artifact | confirmed-authoritative | primary | not-applicable | incident-time | high | — |
| S2 | Adversarial / gaming robustness | model | preventive | Absent | research-evidence | confirmed-authoritative | primary | not-applicable | incident-time | high | — |
| S3 | Human-in-the-loop pairing — high-stakes (e.g. GRE) | human-operator | containment | Working | direct-artifact | confirmed-authoritative | mitigating | in-time | incident-time | high | **HO** |
| S4 | Human oversight — where e-rater scores alone (Criterion, practice, some K-12) | human-operator | containment | Absent | direct-artifact | confirmed-authoritative | primary | not-applicable | incident-time | high | **HO** |
| S5 | Vendor response: BABEL-advisory detector | application | detective | Inadequate (design) | direct-artifact | confirmed-authoritative | not-causally-relevant | too-late | **added-after** | high | — |

Relationships: **S1 → S2** common-cause (high): both stem from feature/proxy-based scoring that ignores meaning — construct-blindness is why the engine is gameable. **S2 → S5** temporal-precedence (high): the robustness gap (BABEL) preceded and prompted the narrow advisory detector.

Contributing factors: **CF1** the cost/scale incentive to automate high-volume essay scoring (factor_type incentive-structure, effect harm-enabling, role primary-upstream, basis research-evidence, conf medium).

**Coding notes.** S3 and S4 are the dataset's clean demonstration of the **`control_group` state-divergence split (amendment A1)**: the *same* control-type (human oversight of e-rater output) is **Working** in the high-stakes check-score model (human decisive; a BABEL essay's inflated machine score routes to more humans) but **Absent** where the engine scores alone — so it is coded as two rows sharing `control_group = HO`, with `observed_state` genuinely divergent across deployment contexts. Counting at the control level dedupes by HO; at the interaction level both rows vote. This is exactly the case A1 was written for.

---

## INCIDENT 30 — C104 Amazon Q Developer extension supply-chain injection [near-miss; backfill for C101]

**Incident row.** `incident_id` 2025-amazon-q-wiper-injection · domain security-cyber · date 2025-07 (CVE-2025-8217) · scope **discrete-event** · harm_primary security-compromise · outcome **near-miss** (malicious agent-prompt shipped in signed release v1.84 to ~900k installs, but payload was malformed/defanged and did not execute at scale; AWS reports no customer impact) · system_type **confirmed-ML** (LLM-based agentic coding assistant with filesystem/bash/AWS-CLI tool access) · ai_causal_contribution **major-contributor** (the AI agent was the intended destruction vector) · attributed_primary_cause **organizational** (AWS access-control / supply-chain failure) · incident_confidence medium (AWS-confirmed core; some attacker-claimed details disputed).

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | PR review / repo write-access control | organizational-process | preventive | **Bypassed** | operator-claim, direct-artifact | multiply-reported | primary | not-applicable | incident-time | high |
| S2 | Supply-chain / release-integrity vetting | organizational-process | preventive | Failed | operator-claim | multiply-reported | primary | not-applicable | incident-time | high |
| S3 | Agent execution guardrails (destructive-command confirmation/sandbox) | application | containment | **Unknown** (suspected_absent=true) | inferred-indirect | inferred-indirect | contributing | not-applicable | incident-time | low |
| S4 | Proactive detection (pre-release / at-merge) | organizational-process | detective | Failed | direct-artifact | multiply-reported | contributing | too-late | incident-time | medium |
| S5 | Containment of destructive payload | infrastructure-environment | containment | Absent | operator-claim | multiply-reported | latent-condition | not-applicable | incident-time | high |
| S6 | Response / remediation (revoke token, remove code, pull 1.84, ship 1.85) | organizational-process | recovery | Working | operator-claim | multiply-reported | mitigating | delayed | incident-time | high |

Relationships: **S1 → S2** enabling (high): the over-scoped GitHub token / merged malicious PR fed straight into an auto-built signed release, so the access-control bypass caused the release-integrity failure. **S4 → S6** temporal-precedence (high): late external detection preceded the reactive remediation.

Contributing factors: none coded. The reason this is a near-miss — the payload being malformed (AWS) or deliberately defanged (attacker) — is recorded at the incident level as `outcome_class = near-miss` and in these notes, **not** as a contributing factor, because it is harm-*reducing* luck/intent, not a harm-driving factor (and not a working safeguard).

**Coding notes.** S1 is **Bypassed** (an attacker circumvented write-access control via an over-scoped token — circumvention of a control, per the locked rule). S3 is **Unknown + suspected_absent**: no source documents an agent-side destructive-command guardrail, and because the payload never properly executed, any such guardrail was never tested — so we record suspicion without asserting Absent. S5 (containment) is **Absent** with the explicit note that non-execution was *accidental*, not a control — the honest coding of a near-miss that was luck, not defense. Medium incident_confidence reflects the AWS-vs-attacker disputes over access mechanism and whether the code ran at all.

---

## Batch-6 quick stats (interaction-level, NOT analysis)
33 safeguard interactions coded (30 incident-time, 3 added-after). Incident-time state spread: Inadequate 10, Absent 7, Failed 6, Working 4, Bypassed 2, Unknown 1 (suspected_absent), Disputed 0. Contributing factors: 4. **Cumulative Batches 1–6: 30 of 30 incidents coded — Phase 1B coding complete.**

## Phase 1B coding — closing note
All 30 selected incidents are now coded against CIR v0.3 across the four tables. One selected incident (C101 Iberian blackout) was excluded at the coding stage as ineligible and deterministically backfilled with C104 per the frozen selection rule; the exclusion and swap are logged. The full dataset now needs the Phase 1C hygiene pass (standardize terminology, machine-readable CSV/JSON export, contradiction checks, versioning) before Phase 3 analysis. No cross-incident analysis has been run yet — every "running observation" in these batch documents is a flagged candidate for Phase 3, not a result.
