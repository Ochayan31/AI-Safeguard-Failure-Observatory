# AI Safeguard Failure Observatory
## Phase 1B — Batch 2, coded against CIR v0.3

**Document:** `batch2_coded.md`
**Incidents:** C010 Boeing 737 MAX MCAS, C039 Dutch childcare benefits (recoded from pilot P2), C032 Williams facial-recognition wrongful arrest, C073 Mata v. Avianca (ChatGPT fabricated citations), C105 EchoLeak (M365 Copilot prompt injection).
**Conventions:** the five Batch-1 locked calibration decisions apply throughout (assurance-governance function; Disabled = deliberate suppression/deactivation; one row per control; merge same-underlying controls; engagement test for Bypassed vs Inadequate). Field abbreviations as in Batch 1.
**New patterns this batch worth noting:** Boeing carries three Disabled controls and two assurance-governance controls; Mata is the clean **ai_causal_contribution ≠ attributed_primary_cause** divergence (AI fabricated, but the court blamed the human); EchoLeak produces the batch's only **timeliness = in-time** control (caught pre-exploitation); Mata's "ask ChatGPT to confirm" is coded as a **contributing factor** (illusory verification), not a safeguard.

---

## INCIDENT 6 — C010 Boeing 737 MAX MCAS (Lion Air 610 + Ethiopian 302)

**Incident row.** `incident_id` 2018-2019-boeing-737max-mcas · domain other (aviation) · date_start 2018-10-29 / date_end 2019-03-10 · scope **bounded-episode** · **observation_boundary:** the MCAS design/certification failure and the two 737 MAX accidents plus the between-crash period; excludes broader 737 MAX program issues unrelated to MCAS · harm_primary physical-safety · outcome realized-harm · system_type **algorithmic-nonML** (deterministic control law, fixed AoA thresholds, no learning) · ai_causal_contribution **major-contributor** · attributed_primary_cause **multiple** (US House: Boeing faulty assumptions + management non-transparency + FAA insufficient oversight; ET302 crew-response contested by NTSB/BEA) · incident_confidence high.

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | MCAS control-law bounding (authority limit, single activation) | model | containment | Inadequate (design) | post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S2 | AoA sensor redundancy / cross-check | infrastructure-environment | preventive | Absent | comparable-system, post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S3 | AoA Disagree alert | application | detective | **Disabled** | post-incident-finding | confirmed-authoritative | contributing | not-applicable | incident-time | high |
| S4 | Pilot disclosure & training on MCAS | organizational-process | assurance-governance | **Disabled** | post-incident-finding, direct-artifact | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S5 | Runaway-trim / stab-cutout recovery procedure | human-operator | recovery | Inadequate (operation) | post-incident-finding | confirmed-authoritative | contributing | delayed | incident-time | high |
| S6 | System safety analysis / hazard classification | organizational-process | assurance-governance | Failed | post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S7 | FAA certification oversight (ODA delegation) | external-ecosystem | assurance-governance | Inadequate (enforcement) | post-incident-finding | confirmed-authoritative | latent-condition | not-applicable | incident-time | high |
| S8 | Between-crash intervention (Emergency AD, no grounding) | external-ecosystem | containment | Inadequate (design) | post-incident-finding, direct-artifact | confirmed-authoritative | contributing | delayed | incident-time | high |
| S9 | MCAS redesign (dual-sensor, single activation, capped authority) + grounding + training | model | containment | Working | direct-artifact | confirmed-authoritative | not-causally-relevant | in-time | **added-after** | high |

Relationships: **S6 → S2** enabling (high): rating MCAS below "catastrophic" is what permitted the single-sensor design. **S2 → S1** enabling (high): the absent cross-check let one faulty AoA drive the unbounded control law. **S4 → S5** enabling (high): pilots not knowing MCAS existed is why the recovery procedure was not promptly/effectively applied (NTSB). **S3 → S5** **masking** (medium): the inoperative AoA Disagree alert hid the sensor disagreement that would have cued recovery. **S8 → S1** enabling (medium): the inadequate post-Lion-Air intervention left the same MCAS mechanism live for Ethiopian 302.

Contributing factors: **CF1** schedule/competitive pressure vs the Airbus A320neo and cost-driven decisions (factor_type incentive-structure, effect harm-enabling, role aggravating, basis post-incident-finding, conf medium-high).

**Coding notes.** Three Disabled/near-Disabled controls make this the densest Disabled case yet: S3 (alert gated behind an unpurchased option and known-broken since 2015) and S4 (MCAS references deleted from manuals and scrubbed from the FSB report via concealment from the FAA — the basis of the DOJ fraud charge) are both deliberate deactivations of a safeguard's protective effect → Disabled. S2 is **Absent** rather than Disabled: the second AoA sensor physically existed, but a *cross-check control* was never architected into MCAS, so the safeguard never existed as a functioning control. S4, S6, S7 all use the new **assurance-governance** function (disclosure, internal safety analysis, external certification). The ET302 human-factors dispute (NTSB/BEA dissent from the EAIB report) is noted at incident level and does not change any safeguard state.

---

## INCIDENT 7 — C039 Dutch childcare benefits (Toeslagenaffaire) [recoded pilot P2 → v0.3]

**Incident row.** `incident_id` 2013-2021-nl-toeslagenaffaire · domain government-benefits · date_start 2013 / date_end 2021 · scope **systemic-program** · **observation_boundary:** the childcare-benefit fraud risk-classification system and its safeguards (~2013–2020) and the resulting harms to wrongly-accused families; excludes the separate FSV blacklist · harm_primary rights-discrimination · harm_secondary financial-loss, psychological-social · outcome realized-harm · system_type **probable-ML** (authorities call it "self-learning"; the described mechanism is a weighted risk-scorer — contested) · ai_causal_contribution **major-contributor** · attributed_primary_cause **organizational** · incident_confidence medium (technical nature contested; harm well-established).

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Human-rights / data-protection impact assessment (pre-deployment) | organizational-process | assurance-governance | Absent | regulation-policy, post-incident-finding | confirmed-authoritative | latent-condition | not-applicable | incident-time | high |
| S2 | Bias mitigation / removal of nationality feature | model | preventive | Absent | post-incident-finding, regulation-policy | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S3 | Model transparency / explainability | application | detective | Absent | post-incident-finding | confirmed-authoritative | latent-condition | not-applicable | incident-time | high |
| S4 | Meaningful individual human review of flagged cases | human-operator | detective | **Bypassed** | post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S5 | Proportionality safeguard on benefit reclamation | application | containment | Absent | post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S6 | Legal basis / GDPR compliance | organizational-process | preventive | Failed | regulation-policy, post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S7 | Internal accountability / honest disclosure to regulator | organizational-process | assurance-governance | Failed | post-incident-finding | confirmed-authoritative | aggravating | not-applicable | incident-time | high |
| S8 | External oversight: Data Protection Authority | external-ecosystem | detective | Working | direct-artifact | confirmed-authoritative | mitigating | too-late | incident-time | high |
| S9 | External oversight: courts / parliament | external-ecosystem | recovery | Working | direct-artifact | confirmed-authoritative | mitigating | too-late | incident-time | high |

Relationships: **S3 → S4** enabling (high): the black-box design is what structurally prevented meaningful human review. **S2 → S4** enabling (medium): the biased score handed to caseworkers who could not interrogate it enabled rubber-stamping. **S1 → S2** enabling (medium): the absent up-front assessment is why the discriminatory feature was never caught. **S7 → S8** **masking** (medium): the false denial of processing to the regulator delayed the DPA's finding.

Contributing factors: **CF1** cost-recovery/fraud-savings incentive requiring the operation to prove its own efficiency (factor_type incentive-structure, effect harm-enabling, role aggravating, basis post-incident-finding, conf medium).

**Coding notes.** S4 is the canonical **Bypassed** (caseworkers structurally denied the information to interrogate a black-box score — engagement test). Recoded from the pilot: S1 now uses **assurance-governance** (an impact assessment is a governance control) rather than the pilot's "preventive"; and the pilot's `existence_timing` becomes v0.3 `existence-time = incident-time` for the late-acting external controls (S8, S9) with `timeliness = too-late`. system_type is **probable-ML**, carrying the contested "self-learning vs weighted-scorer" question as a coded value rather than a gate.

---

## INCIDENT 8 — C032 Williams facial-recognition wrongful arrest

**Incident row.** `incident_id` 2020-williams-detroit-facerec · domain criminal-justice · date 2020-01-09 · scope **discrete-event** · harm_primary rights-discrimination · harm_secondary psychological-social · outcome realized-harm · system_type **confirmed-ML** (DataWorks Plus / NEC / Rank One deep-learning face matching) · ai_causal_contribution **major-contributor** (false match initiated the arrest; human failures compounded) · attributed_primary_cause **organizational** (police over-reliance and failed corroboration), source ACLU / NYT / settlement · incident_confidence high.

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | "Investigative lead only, not probable cause" policy | organizational-process | preventive | **Bypassed** | direct-artifact, post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S2 | Independent human corroboration before arrest | human-operator | preventive | Absent | established-practice, post-incident-finding | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S3 | Photo-lineup integrity (untainted witness) | human-operator | detective | Inadequate (operation) | post-incident-finding | confirmed-authoritative | contributing | not-applicable | incident-time | high |
| S4 | Image-quality / match-confidence threshold | application | preventive | Absent | comparable-system | inferred-indirect | contributing | not-applicable | incident-time | medium |
| S5 | FR analyst / examiner verification | human-operator | detective | Inadequate (operation) | post-incident-finding | multiply-reported | contributing | not-applicable | incident-time | medium |
| S6 | Warrant / judicial pre-arrest check | external-ecosystem | preventive | **Bypassed** | post-incident-finding | confirmed-authoritative | contributing | not-applicable | incident-time | medium |
| S7 | Prosecutorial review / charge dismissal | external-ecosystem | recovery | Working | direct-artifact | confirmed-authoritative | mitigating | too-late | incident-time | high |
| S8 | Detroit PD facial-recognition policy (no arrest on FR alone, corroboration, audit) | organizational-process | preventive | Working | direct-artifact | confirmed-authoritative | not-causally-relevant | in-time | **added-after** | high |

Relationships: **S1 → S2** enabling (high): treating the match as an identification is precisely why no independent corroboration was sought. **S4 → S1** enabling (medium): the absent image-quality gate let a weak, ninth-ranked match flow forward to be treated as an ID. **S3 → S6** enabling (medium): the tainted lineup is what misled the magistrate into issuing the warrant.

Contributing factors: **CF1** documented higher facial-recognition misidentification rates for people of color (factor_type other [demographic-bias condition], effect harm-amplifying, role contributing, basis research-evidence, conf medium).

**Coding notes.** Two Bypassed controls of different kinds: S1 is a written policy **ignored/overridden** by the officers (the "lead only, not probable cause" disclaimer on the report itself); S6 is a judicial check **defeated by being fed incomplete information** (the magistrate later said she was misled). Both are circumvention/structural-prevention of controls that were not self-suppressed → Bypassed, consistent with the locked rule. S7 (dismissal) is the only recovery control and it is `too-late` (after arrest and ~30 hours detention).

---

## INCIDENT 9 — C073 Mata v. Avianca (ChatGPT fabricated legal citations)

**Incident row.** `incident_id` 2023-mata-avianca-chatgpt · domain other (legal) · date 2023-03 (filing) / 2023-06-22 (sanctions) · scope **discrete-event** · harm_primary information-integrity (fabricated authorities filed in court) · outcome realized-harm · system_type **confirmed-ML** (ChatGPT, generative LLM) · ai_causal_contribution **major-contributor** · attributed_primary_cause **human-operator** (the court sanctioned the attorneys' failure to verify, finding bad faith) · incident_confidence high.

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Attorney verification of cited cases vs a real database (Rule 11) | human-operator | preventive | **Bypassed** | direct-artifact | confirmed-authoritative | primary | not-applicable | incident-time | high |
| S2 | Signing-attorney gatekeeping inquiry (Rule 11 signature) | human-operator | preventive | Bypassed | direct-artifact | confirmed-authoritative | contributing | not-applicable | incident-time | high |
| S3 | Firm AI-use / tool-appropriateness policy | organizational-process | preventive | **Unknown** (suspected_absent=true) | inferred-indirect | inferred-indirect | latent-condition | not-applicable | incident-time | low |
| S4 | Detection (opposing counsel + court) | external-ecosystem | detective | Working | direct-artifact | confirmed-authoritative | mitigating | too-late | incident-time | high |
| S5 | Accountability / Rule 11 sanctions + judge-notification | external-ecosystem | recovery | Working | direct-artifact | confirmed-authoritative | mitigating | too-late | incident-time | high |
| S6 | Court standing orders on AI disclosure (Starr, Fuentes) | external-ecosystem | preventive | Working | direct-artifact | confirmed-authoritative | not-causally-relevant | in-time | **added-after** | high |

Relationships: **S1 → S2** common-cause (medium): both verification failures reflect the same absent verification discipline at authoring and signing. **S1 → S4** temporal-precedence (high): the unverified brief preceded external detection; ordering only.

Contributing factors: **CF1** the "ask ChatGPT whether the cases are real" self-confirmation — an **illusory verification** in which the fabricating system certified its own output (factor_type other [illusory-verification], effect harm-enabling, role contributing, basis direct-artifact, conf high). Coded as a contributing factor, not a safeguard, because it did not reduce harm; it manufactured false confidence.

**Coding notes.** This is the clean **ai_causal_contribution (major-contributor) vs attributed_primary_cause (human-operator)** divergence the framework's F-1 split was built for: the LLM fabricated the content, but the authoritative finding blamed the attorney's failure to verify. S3 is coded **Unknown + suspected_absent** rather than Absent: a firm AI-use policy was not established practice in early 2023, so there is no defensible basis it should have existed, though I suspect it was missing. The illusory self-verification is exactly the kind of non-safeguard the contributing_factors table exists to hold.

---

## INCIDENT 10 — C105 EchoLeak (M365 Copilot zero-click prompt injection)

**Incident row.** `incident_id` 2025-echoleak-m365-copilot · domain security-cyber · date 2025 (reported Jan, patched May, disclosed Jun; CVE-2025-32711) · scope **discrete-event** · harm_primary privacy-data · outcome **near-miss** (researcher-discovered; Microsoft confirmed no customers affected) · system_type **confirmed-ML** (RAG LLM over M365 data) · ai_causal_contribution **major-contributor** · attributed_primary_cause **AI-system** (LLM scope violation) · incident_confidence medium (Aim-demonstrated chain; Microsoft confirmed existence/severity/fix).

| id | safeguard | layer | fn | state | basis | status | role | time | exist | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Prompt-injection classifiers (XPIA) | application | detective | **Bypassed** | operator-claim, direct-artifact | multiply-reported | primary | not-applicable | incident-time | medium |
| S2 | Data-scope / trust-boundary isolation (least privilege) | infrastructure-environment | containment | Inadequate (design) | direct-artifact | single-source-reported | primary | not-applicable | incident-time | medium |
| S3 | Markdown link/image redaction | application | containment | Inadequate (design) | direct-artifact | single-source-reported | contributing | not-applicable | incident-time | medium |
| S4 | CSP / URL egress allowlist | infrastructure-environment | containment | **Bypassed** | direct-artifact | single-source-reported | contributing | not-applicable | incident-time | medium |
| S5 | Human-in-the-loop confirmation at exfiltration | human-operator | preventive | Absent | comparable-system | inferred-indirect | contributing | not-applicable | incident-time | medium |
| S6 | Detection (Aim Labs responsible disclosure) | external-ecosystem | detective | Working | direct-artifact | confirmed-authoritative | mitigating | **in-time** | incident-time | high |
| S7 | Remediation (Microsoft server-side fix) | application | recovery | Working | operator-claim | multiply-reported | not-causally-relevant | in-time | **added-after** | high |

Relationships: **S1 → S2** enabling (medium): evading the injection classifier let the untrusted instruction reach privileged data (the LLM scope violation). **S3 → S4** enabling (medium): the un-redacted reference-style markdown carried the exfiltration URL that then abused the trusted-domain allowlist. **S2 → S5** enabling (low): the broken trust boundary meant the only remaining gate would have been a human confirmation, which was absent.

Contributing factors: **CF1** immature prompt-injection defense tooling / scarcity of quality injection-detection datasets, per the researchers (factor_type other [immature-defense-tooling], effect harm-enabling, role contributing, basis operator-claim, conf low).

**Coding notes.** EchoLeak is the batch's **defense-in-depth-with-gaps** case: three containment/detection layers existed (XPIA, redaction, CSP allowlist) and each had a gap (Bypassed or Inadequate), while the human-in-the-loop layer was Absent (the zero-click property). S6 is the batch's only **timeliness = in-time** control — researcher responsible disclosure caught it before any exploitation — the deliberate contrast with all the too-late external recoveries elsewhere, and the reason `outcome_class = near-miss`. Evidence_status is mostly single-source-reported (the technical chain rests on the Aim/Cato account), keeping confidence at medium.

---

## Batch-2 quick stats (interaction-level, NOT analysis)
39 safeguard interactions coded (35 incident-time, 4 added-after). Incident-time state spread: Absent 11, Inadequate 9, Bypassed 7, Working 4, Failed 3, Disabled 3, Unknown 1 (suspected_absent). Contributing factors: 5. `timeliness=in-time` appears once at incident time (EchoLeak S6); `too-late` dominates the recovery controls, as expected. Cumulative across Batches 1–2: 10 of 30 incidents coded.

## Notable cross-incident coding observations (for eventual analysis, not yet analysis)
- **Disabled** is concentrating in engineered-safety and public-administration cases where operators deactivated their own controls (Boeing ×3, Robodebt ×2), and is essentially absent from the LLM/agentic cases so far — a pattern to watch, not yet report.
- **assurance-governance** (new in v0.3) has already absorbed 6 controls across the two batches (Cruise, Air Canada, Boeing ×3, Toeslagen ×2), confirming the promotion was warranted.
- The **too-late recovery** pattern (external oversight working only years/weeks after harm) recurs in nearly every omission-dominated case; EchoLeak is the sole in-time exception so far.
