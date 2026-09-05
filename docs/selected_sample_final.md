# AI Safeguard Failure Observatory
## Phase 1B — FINAL Selected Sample (locked)

**Document:** `selected_sample_final.md`
**Produced by:** `select_sample_v2.py`, seed `AISFO-2026-08-24`, fully reproducible.
**Status:** LOCKED. This is the sample the Observatory will code against v0.2. Selection is complete and precedes any outcome/CIR analysis, per the frozen protocol. From here, no case is added or dropped except by a dated protocol amendment.

## 1. Constraint check (all pass, incl. the 2026-08-24 amendment)

| Constraint | Target | Result |
|---|---|---|
| Sample size | 30 | 30 ✓ |
| Recency/generative-era floor | ≥5 | 6 ✓ |
| Agentic tool-use floor | ≥2 | 2 ✓ |
| Omission-dominated floor | ≥8 | 17 ✓ |
| system_type confirmed-ML / probable-ML / algorithmic-nonML | ≥4 each, ≤18 | 16 / 6 / 7 ✓ |
| Per-domain cap | ≤5 | max 4 ✓ |
| Top-documentation-tier | ≤21 | 21 ✓ |

## 2. The locked 30

| # | id | slug | domain | system_type | mode | era |
|---|---|---|---|---|---|---|
| 1 | C002 | tesla-autopilot-brown | autonomous-vehicle | confirmed-ML | active | |
| 2 | C003 | tesla-autopilot-huang | autonomous-vehicle | confirmed-ML | active | |
| 3 | C004 | cruise-drag-sf | autonomous-vehicle | confirmed-ML | active | |
| 4 | C007 | tesla-autopilot-2m-recall | autonomous-vehicle | confirmed-ML | omission | |
| 5 | C010 | boeing-737max-mcas | aviation-other | algorithmic-nonML | active | |
| 6 | C018 | flash-crash-2010 | finance-trading | algorithmic-nonML | active | |
| 7 | C019 | zillow-offers | finance-trading | probable-ML | active | |
| 8 | C022 | optum-risk-bias | healthcare-clinical | probable-ML | omission | |
| 9 | C024 | ibm-watson-oncology | healthcare-clinical | confirmed-ML | omission | |
| 10 | C027 | pulse-oximeter-bias | healthcare-clinical | algorithmic-nonML | omission | |
| 11 | C031 | compas-recidivism | criminal-justice | probable-ML | omission | |
| 12 | C032 | williams-detroit-facerec | criminal-justice | confirmed-ML | omission | |
| 13 | C039 | nl-toeslagen | government-benefits | probable-ML | omission | |
| 14 | C041 | au-robodebt | government-benefits | algorithmic-nonML | omission | |
| 15 | C042 | us-mi-midas | government-benefits | algorithmic-nonML | omission | |
| 16 | C047 | nl-rotterdam-fraud | government-benefits | confirmed-ML | omission | |
| 17 | C056 | uk-ofqual-alevel | education | algorithmic-nonML | omission | |
| 18 | C059 | workday-mobley | hiring-HR | probable-ML | active | |
| 19 | C060 | air-canada-chatbot | consumer-chatbot | probable-ML | omission | genai |
| 20 | C061 | microsoft-tay | consumer-chatbot | confirmed-ML | omission | |
| 21 | C070 | raine-openai-suicide | consumer-chatbot | confirmed-ML | omission | genai |
| 22 | C073 | mata-avianca | llm-other | confirmed-ML | omission | genai |
| 23 | C081 | gemini-image-diversity | content-moderation | confirmed-ML | active | genai |
| 24 | C083 | facebook-files-teens | content-moderation | confirmed-ML | omission | |
| 25 | C088 | clearview-ai-scraping | security-cyber | confirmed-ML | omission | |
| 26 | C094 | erater-babel | education | confirmed-ML | active | |
| 27 | C099 | vw-dieselgate | environmental | algorithmic-nonML | active | |
| 28 | C104 | amazon-q-wiper-injection | security-cyber | confirmed-ML | active | AGENTIC | *(coding-stage backfill for C101, see note)* |
| 29 | C102 | gemini-cli-file-wipe | enterprise-agent | confirmed-ML | active | AGENTIC |
| 30 | C105 | echoleak-copilot | security-cyber | confirmed-ML | active | AGENTIC |

## 3. Composition and honest limitations

**Domains (14):** autonomous-vehicle 4, government-benefits 4, healthcare-clinical 3, consumer-chatbot 3, content-moderation 2, criminal-justice 2, education 2, environmental 2, finance-trading 2, security-cyber 2, enterprise-agent 1, llm-other 1, hiring-HR 1, aviation-other 1.

**Era balance:** 6 of 30 from the 2022+ generative/agentic era (including 2 agentic tool-use); the rest span 2010–2021, giving the dataset historical depth as well as current relevance.

**CIR-favorability (declared):** 17 of 30 (57%) are omission-dominated, where CIR reconstructs *less* relational structure. The sample therefore leans, if anything, against CIR's strengths, which is the safe direction for an honest demonstration. The 2026-08-24 amendment moved this from 19/30 to 17/30 by adding active-failure agentic cases; that shift is small and declared.

**Limitations to state in the methodology (not hidden):**
- **Uncovered domains:** scientific-research, robotics-industrial, and finance-consumer received no slots. The recency amendment targeted generative/agentic coverage, not these; they remain in the excluded-but-eligible log and could seed a future expansion.
- **Documentation-quality skew:** the evidence-quality rubric favors institutionally-documented harms, so the sample is somewhat weighted toward cases with official investigations. This is a known, declared property, partially offset by the recency floor.
- **Provisional failure-mode calls** for the "disputed" cases (e.g., Toeslagen, Air Canada) were resolved from the primary source at this step and are revisited during full coding; a change there does not retroactively alter selection (selection is locked), but is noted if it occurs.

## 3b. Coding-stage exclusion + backfill (logged 2026-08-24)
During Phase 1B coding, **C101 (2025 Iberian blackout) was excluded as ineligible**: close research established it as a conventional grid-engineering/voltage-control failure with only classical protective-relay automation (static thresholds) in the causal chain and no AI/ML or algorithmic *decision* system (E1 fail; the Spanish Senate explicitly found it was not an automated-system breakdown — the same principle by which Therac-25 and the A400M were excluded at screening). Per the frozen rule, `select_sample_v2.py` was re-run with C101 marked ineligible; the deterministic backfill is **C104 (Amazon Q supply-chain injection)**, and all other 29 selections held unchanged. Effects on composition: environmental → 1, security-cyber → 3, agentic → 3, recency-era → 7; all frozen floors and caps remain satisfied. This is an eligibility correction, not a re-selection, and is the only change to the locked sample.

## 4. Provenance / reproducibility
- Discovery pool: `discovery_pool.md` (108 candidates, fixed-source sweep).
- Eligibility + selection: `select_sample_v2.py`, seed `AISFO-2026-08-24`. Re-running the script reproduces this exact sample.
- 8 excluded at screen (with reasons) and 70 excluded-but-eligible are recorded in the script output and will be committed to the public repo (Phase 5).
- Amendment logged in `incident_selection_protocol.md` §11.

## 5. Next step (Phase 1B coding)
The 30 are now coded against CIR v0.2, in batches of 5 (the framework's cadence), each incident populating the four tables (incidents, safeguard_interactions, relationships, contributing_factors). Recommended: code the first batch of 5 spanning different archetypes, deliver for a coding-consistency review, then proceed once the coding style is confirmed.
