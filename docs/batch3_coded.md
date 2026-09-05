# AI Safeguard Failure Observatory
## Phase 1B — Batch 3, coded against CIR v0.3

**Incidents:** C002 Tesla Autopilot (Williston/Brown 2016), C031 COMPAS recidivism, C061 Microsoft Tay, C088 Clearview AI, C056 UK Ofqual A-level algorithm.
**Conventions:** the five Batch-1 locked calibration decisions apply. Field abbreviations as before.
**Notable this batch:** COMPAS is the dataset's **Disputed** showcase (a bias claim that is mathematically contested, not merely opinion) and its `system_type` is recoded **algorithmic-nonML** (vendor: logistic regression/survival analysis, not ML) — this does not break the locked selection (probable-ML → 5, algorithmic-nonML → 8, both still ≥ the floor of 4). Ofqual is the batch's **Bypassed-via-NDA** case (external statistical experts structurally excluded). Tesla is the "**no defect but inadequate**" case (NHTSA found no defect; NTSB found the design contributory) — coded Inadequate(design), preserving that distinction.

---

## INCIDENT 11 — C002 Tesla Autopilot fatal crash (Williston, FL)

**Incident row.** `incident_id` 2016-tesla-autopilot-williston · domain autonomous-vehicle · date 2016-05-07 · scope **discrete-event** · harm_primary physical-safety · outcome realized-harm · system_type **confirmed-ML** (Mobileye EyeQ3 vision classifier) · ai_causal_contribution **major-contributor** · attributed_primary_cause **multiple** (NTSB: truck driver's failure to yield + car driver's over-reliance + Tesla design permitting disengagement) · incident_confidence high.

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Perception / crossing-object detection | application | preventive | Inadequate (design) | post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S2 | Automatic emergency braking | application | containment | Inadequate (design) | post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S3 | Driver-attention monitoring | application | detective | Inadequate (design) | post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S4 | Operational-design-domain (ODD) enforcement / geofence | application | preventive | Absent | comparable-system, post-incident-finding | confirmed-authoritative | contributing | not-applicable | incident-time | high |
| S5 | Driver attention / intervention (human) | human-operator | recovery | Failed | post-incident-finding | confirmed-authoritative | primary | too-late | incident-time | high |
| S6 | Post-incident: hands-on escalation + Autosteer "strike-out" | application | detective | Working | direct-artifact | confirmed-authoritative | not-causally-relevant | in-time | **added-after** | high |

Relationships: **S1 → S2** enabling (high): the perception classifier not recognizing the crossing trailer is why AEB had no target to brake for. **S3 → S5** enabling (high): torque-only monitoring permitted the prolonged inattention that the human safeguard then failed on. **S4 → S1** enabling (medium): engaging Autopilot on a non-limited-access cross-traffic road is where the perception design limit bit.

Contributing factors: **CF1** the truck driver's failure to yield the right of way (factor_type other [external-actor], effect harm-causing, role primary, basis post-incident-finding, conf high); **CF2** the car driver operating at 74 in a 65 mph zone (factor_type other [operator-behavior], effect harm-amplifying, conf high).

**Coding notes.** S1/S2/S3 are **Inadequate(design)**, not Failed: NHTSA found no component defect, but the designs were too weak for the scenario. Preserving "non-defective yet inadequate" is exactly what the inadequacy_type field is for. S4 (ODD lockout) is **Absent** — it did not exist at incident time (NTSB recommended creating it). S5 is the human safeguard, **Failed** + causal_role primary per the probable cause.

---

## INCIDENT 12 — C031 COMPAS recidivism risk scoring [Disputed showcase]

**Incident row.** `incident_id` 2016-compas-recidivism · domain criminal-justice · date 2016 (ProPublica investigation; State v. Loomis) · scope **systemic-program** · **observation_boundary:** COMPAS pretrial/sentencing risk scoring as examined by ProPublica (Broward County) and State v. Loomis (Wisconsin); the bias controversy and due-process challenge; excludes other risk tools · harm_primary rights-discrimination · outcome realized-harm · system_type **algorithmic-nonML** (vendor: logistic regression + survival analysis; internal weights trade-secret and unverifiable) · ai_causal_contribution **disputed** · attributed_primary_cause **disputed** · incident_confidence medium (the bias harm is mathematically contested).

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Independent pre-deployment disparate-impact validation | organizational-process | assurance-governance | Absent | post-incident-finding | confirmed-authoritative | latent-condition | not-applicable | incident-time | high |
| S2 | Algorithmic transparency (non-proprietary scoring) | application | detective | Absent | direct-artifact, post-incident-finding | confirmed-authoritative | latent-condition | not-applicable | incident-time | high |
| S3 | Model fairness constraint (equalized error rates) | model | preventive | **Disputed** | research-evidence | disputed | disputed | not-applicable | incident-time | medium |
| S4 | Human oversight (judge in the loop) | human-operator | containment | Inadequate (design) | post-incident-finding | confirmed-authoritative | contributing | not-applicable | incident-time | medium |
| S5 | Due-process protections (State v. Loomis restrictions) | external-ecosystem | assurance-governance | Working | direct-artifact | confirmed-authoritative | mitigating | too-late | incident-time | high |
| S6 | Loomis-mandated warning advisement in presentence reports | external-ecosystem | assurance-governance | Working | direct-artifact | confirmed-authoritative | not-causally-relevant | in-time | **added-after** | high |

Relationships: **S2 → S4** enabling (high): the trade-secret black box is why judicial oversight cannot meaningfully weigh or interrogate the score. **S1 → S3** temporal-precedence (low): the absent disparate-impact audit preceded the disputed-bias finding; ordering only, and the fairness question itself is Disputed.

Contributing factors: **CF1** differing recidivism base rates across groups (~51% vs ~39% in the Broward sample), which make calibration and equalized error rates mathematically incompatible (Chouldechova/Kleinberg impossibility) — the structural reason the bias claim is Disputed rather than resolvable (factor_type other [statistical base-rate condition], effect harm-enabling, role primary-upstream, basis research-evidence, conf high).

**Coding notes.** S3 is the framework's first **Disputed** `observed_state`, and it is a *substantive* Disputed, not a fallback: ProPublica (equalized-odds framing) and Northpointe (calibration framing) are each mathematically correct, and no model can satisfy both under differing base rates. `ai_causal_contribution` and `attributed_primary_cause` are both **disputed** at the incident level for the same reason. S1 and S2 are cleanly Absent regardless of the fairness dispute — the *transparency* and *independent-audit* failures are not contested, only the bias characterization is. This incident is the clearest demonstration that CIR can hold genuine scientific disagreement as a coded value rather than forcing a verdict.

---

## INCIDENT 13 — C061 Microsoft Tay chatbot

**Incident row.** `incident_id` 2016-microsoft-tay · domain consumer-chatbot · date 2016-03-23 · scope **discrete-event** · harm_primary information-integrity · harm_secondary psychological-social · outcome realized-harm · system_type **confirmed-ML** (learns from interactions) · ai_causal_contribution **major-contributor** · attributed_primary_cause **multiple** (coordinated adversarial attack + Microsoft design oversight) · incident_confidence high (Microsoft first-party postmortem + reporting).

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Output content filter (learning/generation path) | application | preventive | Inadequate (design) | operator-claim, post-incident-finding | multiply-reported | primary | not-applicable | incident-time | medium |
| S2 | Online-learning poisoning safeguard | application | preventive | Absent | comparable-system, post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S3 | Adversarial testing / red-teaming pre-launch | organizational-process | assurance-governance | Inadequate (design) | operator-claim | single-source-reported | latent-condition | not-applicable | incident-time | medium |
| S4 | Guard on the "repeat after me" function | application | preventive | Absent | direct-artifact | multiply-reported | contributing | not-applicable | incident-time | medium |
| S5 | Real-time abuse monitoring / auto-halt | application | detective | **Unknown** (suspected_absent=true) | inferred-indirect | inferred-indirect | contributing | not-applicable | incident-time | low |
| S6 | Kill-switch / takedown (containment) | human-operator | containment | Working | operator-claim | multiply-reported | mitigating | too-late | incident-time | high |

Relationships: **S3 → S2** enabling (medium): the inadequate adversarial testing is why the poisoning gap shipped. **S2 → S6** temporal-precedence (high): the poisoning and offensive output preceded the takedown. **S5 → S6** enabling (medium): the absent real-time detection is why containment was a late manual decision rather than an automatic trip.

Contributing factors: **CF1** an off-platform coordinated adversarial campaign (4chan-organized) directing abusive inputs at Tay (factor_type other [coordinated-adversary], effect harm-causing, role primary, basis post-incident-finding, conf high).

**Coding notes.** S1 is **Inadequate(design)** not Absent: a partial topic blacklist existed (canned answers on some subjects) but did not cover the generative/learned output stream. S5 is **Unknown + suspected_absent** rather than Absent: reporting indicates the takedown was a manual human decision (implying no auto-trip), but no source confirms the presence/absence of a real-time monitor, so we do not guess. S6 (takedown) Working + too-late is the same recovery pattern as elsewhere.

---

## INCIDENT 14 — C088 Clearview AI mass facial-recognition scraping

**Incident row.** `incident_id` 2017-2022-clearview-ai-scraping · domain security-cyber · date_start ~2017 / date_end 2022 · scope **systemic-program** · **observation_boundary:** Clearview's non-consensual scraping of ~3–20bn facial images and the resulting biometric database (~2017 onward) and the 2021–2022 regulatory findings; excludes post-2022 appeals · harm_primary privacy-data · outcome realized-harm · system_type **confirmed-ML** (biometric face-matching) · ai_causal_contribution **major-contributor** · attributed_primary_cause **organizational** · incident_confidence high.

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Consent / lawful basis for biometric processing | organizational-process | preventive | Absent | regulation-policy, post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S2 | Data-protection-by-design / DPIA | organizational-process | assurance-governance | Absent | post-incident-finding | confirmed-authoritative | latent-condition | not-applicable | incident-time | medium |
| S3 | Transparency / notice / opt-out | organizational-process | preventive | Absent | regulation-policy, post-incident-finding | confirmed-authoritative | contributing | not-applicable | incident-time | high |
| S4 | Purpose-limitation & retention limits | organizational-process | containment | Absent | regulation-policy, post-incident-finding | confirmed-authoritative | contributing | not-applicable | incident-time | high |
| S5 | External oversight: data-protection authorities (ICO/CNIL/Garante/OAIC) | external-ecosystem | detective | Working | direct-artifact | confirmed-authoritative | mitigating | too-late | incident-time | high |
| S6 | Structural restraint: US BIPA / ACLU settlement | external-ecosystem | containment | Working | direct-artifact | confirmed-authoritative | mitigating | too-late | incident-time | high |
| S7 | Enforcement of deletion / cease orders | external-ecosystem | recovery | Failed | direct-artifact | multiply-reported | not-causally-relevant | too-late | incident-time | high |

Relationships: **S2 → S1** enabling (medium): the absent by-design governance is why no lawful basis was ever secured. **S1 → S3** common-cause (medium): the entire product model presumes neither consent nor notice. **S5 → S7** temporal-precedence (high): the DPAs issued findings and orders, then enforcement of deletion largely failed (fines unpaid, data retained, jurisdiction contested).

Contributing factors: **CF1** absence of an international enforcement convention, letting a US-based actor contest jurisdiction and evade EU/UK deletion orders (factor_type political, effect harm-enabling, role contributing, basis post-incident-finding, conf medium).

**Coding notes.** The purest **omission-dominated** case in the batch: every preventive safeguard (S1–S4) is Absent by design. S5/S6 are external controls that Worked but too-late; S7 is a rare **recovery control that Failed at execution** (orders issued but deletion not achieved, most fines unpaid) — distinct from a control that was never attempted. S2 coded Absent with medium confidence: the by-design failure is well-evidenced (OAIC), but a discrete "no DPIA conducted" finding is not directly quoted, so confidence is held down rather than the state changed.

---

## INCIDENT 15 — C056 UK Ofqual A-level grading algorithm

**Incident row.** `incident_id` 2020-uk-ofqual-alevel · domain education · date_start 2020-03-18 / date_end 2020-08-17 · scope **bounded-episode** · **observation_boundary:** the 2020 England A-level/GCSE algorithmic standardisation and its withdrawal (Mar–Aug 2020); England-focused; excludes the SQA/Wales/NI parallel episodes · harm_primary rights-discrimination (indirect, socio-economically correlated) · harm_secondary psychological-social · outcome realized-harm · system_type **algorithmic-nonML** (deterministic statistical standardisation; Ofqual later published the R code) · ai_causal_contribution **major-contributor** · attributed_primary_cause **organizational** · incident_confidence high.

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Equality / fairness impact assessment | organizational-process | assurance-governance | Inadequate (design) | direct-artifact, post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S2 | Individual-level validation / testing | organizational-process | assurance-governance | Inadequate (design) | post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S3 | Appeals / redress mechanism | organizational-process | recovery | Inadequate (operation) | direct-artifact | confirmed-authoritative | contributing | too-late | incident-time | high |
| S4 | External expert review & oversight (RSS, Education Committee) | organizational-process | assurance-governance | **Bypassed** | direct-artifact | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S5 | Transparency (model published for scrutiny pre-results) | application | assurance-governance | Inadequate (design) | direct-artifact, post-incident-finding | confirmed-authoritative | contributing | not-applicable | incident-time | high |
| S6 | Recovery / rollback to teacher-assessed grades | external-ecosystem | recovery | Working | direct-artifact | confirmed-authoritative | mitigating | too-late | incident-time | high |
| S7 | Post-incident: code publication + OSR review | organizational-process | assurance-governance | Working | direct-artifact | confirmed-authoritative | not-causally-relevant | in-time | **added-after** | high |

Relationships: **S4 → S1** enabling (high): structurally excluding the Royal Statistical Society (via an overbroad NDA) and ignoring the Education Committee's advance warning is why the equality-assessment gap was never fixed. **S4 → S5** enabling (medium): the same NDA-driven exclusion caused the pre-results transparency failure. **S2 → S3** enabling (medium): the individual-level "rogue results" the aggregate-optimized model produced overwhelmed the inadequate appeals route.

Contributing factors: **CF1** the political mandate to prevent "grade inflation" / preserve year-on-year aggregate comparability, which set the model's optimization target against individual fairness (factor_type political, effect harm-enabling, role primary-upstream, basis post-incident-finding, conf medium-high).

**Coding notes.** S4 is the batch's **Bypassed** case, and a distinctive one: the external statistical-expert safeguard was structurally excluded by an NDA so broad the RSS could not participate, and parliamentary warnings issued **before** deployment were overridden — a control starved/circumvented rather than self-suppressed, so Bypassed per the locked rule. This case's signature (like Robodebt and Boeing) is **existing safeguards overridden, not merely absent** — the advance warnings were on the record. S6 (the U-turn) Worked but too-late and, notably, was triggered by external legal pressure (Foxglove judicial-review threat) plus public protest rather than by any internal control firing.

---

## Batch-3 quick stats (interaction-level, NOT analysis)
39 safeguard interactions coded (36 incident-time, 3 added-after). Incident-time state spread: Absent 11, Inadequate 14, Working 5, Bypassed 2, Failed 2, Disputed 1, Unknown 1 (suspected_absent). Contributing factors: 6. Cumulative Batches 1–3: **15 of 30 incidents coded (halfway).**

## Running cross-incident observations (not yet analysis)
- **Inadequate** is now the largest single state this batch, concentrated in the "no defect but too weak" engineered cases (Tesla ×3) and the "existed in form, insufficient in substance" governance cases (Ofqual ×3, Tay ×2). Worth watching whether Inadequate or Absent dominates the full dataset.
- **assurance-governance** continues to earn its keep: 10 controls across three batches now use it (validation, transparency, disclosure, expert review, impact assessment).
- **Disputed** finally appears (COMPAS S3), used substantively for a genuine mathematical incompatibility, exactly the honest-uncertainty use it was designed for.
- The **"warnings existed and were overridden"** pattern (Robodebt, Boeing, Ofqual) is emerging as a distinct failure signature separate from pure omission — a candidate finding for the eventual analysis.
