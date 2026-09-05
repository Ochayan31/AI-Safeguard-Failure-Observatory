# AI Safeguard Failure Observatory
## Phase 1B Coding — Review Index (for your sign-off before Phase 1C)

All 30 incidents, where to find them, and the coding calls most worth your scrutiny. Nothing here is locked; flag anything and I will revise before building the machine-readable dataset.

## The 30 incidents at a glance

| # | id | incident | batch file | domain | system_type | dominant failure mode |
|---|---|---|---|---|---|---|
| 1 | C004 | Cruise pedestrian dragging | batch1 | autonomous-vehicle | confirmed-ML | active-failure |
| 2 | C041 | Robodebt | batch1 | government-benefits | algorithmic-nonML | omission (+overridden) |
| 3 | C022 | Optum health algorithm | batch1 | healthcare | probable-ML | omission |
| 4 | C060 | Air Canada chatbot | batch1 | consumer-chatbot | probable-ML | omission |
| 5 | C102 | Gemini CLI file wipe | batch1 | enterprise-agent | confirmed-ML | active-failure |
| 6 | C010 | Boeing 737 MAX MCAS | batch2 | other (aviation) | algorithmic-nonML | active + overridden |
| 7 | C039 | Dutch Toeslagen | batch2 | government-benefits | probable-ML | omission |
| 8 | C032 | Williams facial-recognition arrest | batch2 | criminal-justice | confirmed-ML | omission |
| 9 | C073 | Mata v. Avianca (ChatGPT) | batch2 | other (legal) | confirmed-ML | omission |
| 10 | C105 | EchoLeak (M365 Copilot) | batch2 | security-cyber | confirmed-ML | active-failure (near-miss) |
| 11 | C002 | Tesla Autopilot (Brown) | batch3 | autonomous-vehicle | confirmed-ML | active-failure |
| 12 | C031 | COMPAS | batch3 | criminal-justice | algorithmic-nonML | **disputed** |
| 13 | C061 | Microsoft Tay | batch3 | consumer-chatbot | confirmed-ML | omission |
| 14 | C088 | Clearview AI | batch3 | security-cyber | confirmed-ML | omission |
| 15 | C056 | UK Ofqual A-level | batch3 | education | algorithmic-nonML | omission (+overridden) |
| 16 | C042 | Michigan MiDAS | batch4 | government-benefits | algorithmic-nonML | omission (+Disabled) |
| 17 | C070 | Raine v. OpenAI | batch4 | consumer-chatbot | confirmed-ML | **alleged** |
| 18 | C083 | Facebook Files (Instagram) | batch4 | content-moderation | confirmed-ML | detected-but-ignored |
| 19 | C099 | VW Dieselgate | batch4 | environmental | algorithmic-nonML | defeated-by-design |
| 20 | C027 | Pulse-oximeter bias | batch4 | healthcare | algorithmic-nonML | omission |
| 21 | C018 | 2010 Flash Crash | batch5 | finance-trading | algorithmic-nonML | active-failure |
| 22 | C019 | Zillow Offers | batch5 | finance-trading | probable-ML | active-failure |
| 23 | C024 | IBM Watson for Oncology | batch5 | healthcare | confirmed-ML | omission (patient near-miss) |
| 24 | C059 | Mobley v. Workday | batch5 | hiring-HR | probable-ML | **alleged** |
| 25 | C081 | Gemini image generation | batch5 | content-moderation | confirmed-ML | counterproductive-safeguard |
| 26 | C003 | Tesla Autopilot (Huang) | batch6 | autonomous-vehicle | confirmed-ML | active-failure |
| 27 | C007 | Tesla 2M-vehicle recall | batch6 | autonomous-vehicle | confirmed-ML | active-failure |
| 28 | C047 | Rotterdam welfare scoring | batch6 | government-benefits | confirmed-ML | omission |
| 29 | C094 | ETS e-rater / BABEL | batch6 | education | confirmed-ML | omission |
| 30 | C104 | Amazon Q injection | batch6 | security-cyber | confirmed-ML | active-failure (near-miss) |

## The 12 calls I'd most want you to check

1. **COMPAS (12)** recoded `system_type = algorithmic-nonML` (vendor: logistic regression, not ML) and `observed_state = Disputed` on the fairness constraint, with `ai_causal_contribution = disputed`. This is the dataset's showcase Disputed — confirm you want it there and coded this way.
2. **Watson (23)** `outcome_class = realized-harm` with patient-level harm framed as a **near-miss** (physician oversight Working). Defensible either way; you could argue the whole incident is a near-miss.
3. **Facebook Files (18)** `ai_causal_contribution = contributory-non-necessary` (evidence is self-report/correlational). Confirm you don't want the stronger major-contributor.
4. **Raine (17) and Workday (24):** everything ALLEGED, low confidence, disputed evidence_status, `ai_causal_contribution = disputed`. Confirm the conservative handling is what you want for sub-judice cases.
5. **Gemini image (25):** the diversity tuning is coded as a **safeguard that Failed** (counterproductive over-correction), NOT a contributing factor. This is a deliberate call about what counts as a safeguard.
6. **Rotterdam (28) S3** human review = **Inadequate(operation) + disputed evidence** (city claims review; critics say hollow), deliberately *different* from Toeslagen's **Bypassed** because the reviewers were not as clearly denied information. Check the contrast reads right.
7. **C101 excluded, C104 backfilled** (30): the Iberian blackout dropped as ineligible (no algorithmic decision system) and deterministically replaced. Confirm you're comfortable with the exclusion and the swap.
8. **Recurrence pairs kept separate:** two Tesla Autopilot crashes (11, 26) coded near-identically, and two Dutch welfare cases (7, 28). I treated recurrence as data rather than merging — confirm you agree (it matters for the distributions).
9. **`assurance-governance`** (the v0.3 fifth function) now carries ~12 controls (disclosure, validation, certification, testing standards, impact assessment, expert review). Confirm it isn't over-applied and the boundary with `organizational-process` layer is holding.
10. **`Disabled`** appears in Boeing (×3: AoA alert, MCAS disclosure — and the sensor cross-check is Absent not Disabled), Robodebt (×2), MiDAS (×1). Confirm the "deliberate suppression/deactivation = Disabled" rule reads consistently across them.
11. **e-rater (29) `control_group` split:** human oversight coded twice (Working high-stakes / Absent sole-scorer) sharing one control_group. Confirm this is the right use of the state-divergence split.
12. **Near-miss outcomes** (EchoLeak 10, Amazon Q 30, Watson-patient-level 23): confirm the `outcome_class = near-miss` calls, since they'll be reported separately from realized harms in Phase 3.

## Cross-cutting integrity check (all maintained)
No fabricated facts or statistics; every incident sourced to primary/authoritative material with uncertainty flagged; contested cases coded Disputed or low-confidence rather than resolved; one incident excluded for ineligibility and logged; the sample is 57% omission-dominated (CIR-unfavorable direction). The only synthetic content in the whole project remains the labeled example in the framework's §1.10.

Tell me which of the 12 (or anything else in the batch files) you want revised, and I'll apply it before building the Phase 1C machine-readable dataset.
