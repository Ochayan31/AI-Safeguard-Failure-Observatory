# AI Safeguard Failure Observatory
## Phase 1B — Discovery Pool (deduplicated)

**Document:** `discovery_pool.md`
**Status:** Discovery-pool population, per the frozen selection protocol (Section 3). This is the WIDE net, before eligibility screening and stratified selection. Inclusion here is NOT selection; it means "found and worth screening."
**Provenance:** Compiled from a four-slice systematic sweep (incident databases; public-sector algorithms; physical/safety/health AI; generative-LLM era). Duplicates across slices merged. `failure_mode` values are PROVISIONAL and are finalized only at the stratification step, from each case's primary source; cases where the sweep disagreed are marked `disputed`.
**Integrity note:** No incident here is fabricated. `src` = quality of the located source: **P** = authoritative primary (official investigation, court/tribunal ruling, regulator finding); **F** = first-party disclosure; **J** = original investigative journalism; **partial** = best available pending a stronger primary. Every candidate advances to eligibility screening, where the primary-source floor is enforced.

Count: **108 unique candidates** (C001–C108). The frozen ≥90 target is met after one targeted top-up sweep of thin domains (education, scientific-research, environmental, agentic/enterprise). The pool is now FINAL; selection follows.

---

### Autonomous vehicles
| id | slug | one-line | yr | system_type | failure_mode(prov) | harm | src |
|---|---|---|---|---|---|---|---|
| C001 | uber-atg-tempe | Uber self-driving SUV killed a pedestrian; misclassification + suppressed/disabled braking + distracted operator | 2018 | confirmed-ML | disputed | physical-safety | P (NTSB) |
| C002 | tesla-autopilot-brown | Autopilot failed to detect a crossing truck; driver killed | 2016 | confirmed-ML | disputed | physical-safety | P (NTSB) |
| C003 | tesla-autopilot-huang | Autopilot steered into a highway barrier gore point; driver killed | 2018 | confirmed-ML | active-failure | physical-safety | P (NTSB) |
| C004 | cruise-drag-sf | Robotaxi ran over and dragged a pedestrian ~20ft; video withheld from regulators | 2023 | confirmed-ML | active-failure | physical-safety | P (DOJ/DMV) |
| C005 | tesla-fsd-lowvis | NHTSA probe: FSD pedestrian fatality in sun-glare/low-visibility conditions | 2024 | confirmed-ML | omission-dominated | physical-safety | P (NHTSA) |
| C006 | tesla-autopilot-emergency-veh | NHTSA probe: Autopilot repeatedly hit stationary emergency vehicles | 2021 | confirmed-ML | omission-dominated | physical-safety | P (NHTSA) |
| C007 | tesla-autopilot-2m-recall | ~2M-vehicle recall for inadequate driver-engagement controls | 2023 | confirmed-ML | omission-dominated | physical-safety | P (NHTSA) |
| C008 | waymo-construction-recall | ~3.9k robotaxis recalled after entering freeway construction zones | 2026 | confirmed-ML | active-failure | physical-safety | P (NHTSA) |
| C009 | zoox-braking-recall | Zoox recalls for unexpected hard braking / smoke perception confusion | 2025 | confirmed-ML | active-failure | physical-safety | P (NHTSA) |

### Aviation / other automated control
| id | slug | one-line | yr | system_type | failure_mode(prov) | harm | src |
|---|---|---|---|---|---|---|---|
| C010 | boeing-737max-mcas | MCAS driven by a single failed sensor with no redundancy; two crashes, 346 dead | 2018 | algorithmic-nonML | active-failure | physical-safety | P (NTSB/Congress) |
| C011 | airbus-a400m-seville | ECU software config fault shut down three engines on test flight; 4 killed | 2015 | algorithmic-nonML | active-failure | physical-safety | partial |

### Industrial robotics
| id | slug | one-line | yr | system_type | failure_mode(prov) | harm | src |
|---|---|---|---|---|---|---|---|
| C012 | vw-baunatal-robot | Assembly-line robot crushed a worker during setup | 2015 | algorithmic-nonML | active-failure | physical-safety | J |
| C013 | skorea-goseong-robot | Box-handling robot crushed a worker it apparently read as a box | 2023 | algorithmic-nonML | active-failure | physical-safety | J |
| C014 | stellantis-robot-death | Mechanic killed by a robot during retooling; energy-isolation/bypass failure | 2025 | algorithmic-nonML | active-failure | physical-safety | partial |
| C015 | wisconsin-pizza-robot | Worker crushed by a robotic machine at a pizza plant | 2023 | algorithmic-nonML | active-failure | physical-safety | J |
| C016 | amazon-warehouse-robots | Higher injury rates reported at robot-automated fulfillment centers | 2020 | unknown | disputed | physical-safety | J |

### Finance
| id | slug | one-line | yr | system_type | failure_mode(prov) | harm | src |
|---|---|---|---|---|---|---|---|
| C017 | knight-capital | Dormant test code activated on deploy; ~$460M lost in 45 min | 2012 | algorithmic-nonML | active-failure | financial-loss | P (SEC) |
| C018 | flash-crash-2010 | Automated trading triggered a ~1000-pt Dow plunge/recovery | 2010 | algorithmic-nonML | active-failure | financial-loss | P (SEC) |
| C019 | zillow-offers | Home-price ML model overpaid; ~$500M writedown, unit shut | 2021 | confirmed-ML | active-failure | financial-loss | J |
| C020 | apple-card-gender | Claims of gendered credit limits; NY DFS found no unlawful bias but transparency flaws | 2019 | probable-ML | disputed | rights-discrimination | P (NY DFS) |
| C021 | saferent-screening | Tenant-screening score disadvantaged Black/Hispanic/voucher renters; $2.28M settlement | 2024 | probable-ML | omission-dominated | rights-discrimination | P (settlement) |

### Healthcare / clinical
| id | slug | one-line | yr | system_type | failure_mode(prov) | harm | src |
|---|---|---|---|---|---|---|---|
| C022 | optum-risk-bias | Population-health algorithm used cost as proxy for need; under-referred Black patients | 2019 | probable-ML | omission-dominated | rights-discrimination | P (Science) |
| C023 | epic-sepsis-model | Widely deployed sepsis model far worse than advertised in external validation | 2021 | confirmed-ML | omission-dominated | physical-safety | P (JAMA) |
| C024 | ibm-watson-oncology | Internal docs: unsafe/incorrect cancer treatment recommendations | 2018 | confirmed-ML | omission-dominated | physical-safety | J (STAT) |
| C025 | therac-25 | Race condition + removed interlocks caused fatal radiation overdoses | 1987 | algorithmic-nonML | active-failure | physical-safety | P (peer-reviewed) |
| C026 | davinci-surgical-robot | Robotic-surgery injuries/deaths; adverse events underreported to FDA | 2013 | algorithmic-nonML | disputed | physical-safety | J |
| C027 | pulse-oximeter-bias | Oximeters overestimate O2 in darker skin; missed hypoxemia | 2020 | algorithmic-nonML | omission-dominated | physical-safety | P (peer-reviewed) |
| C028 | unitedhealth-nhpredict | nH Predict alleged to drive wrongful post-acute care denials; class action | 2023 | probable-ML | active-failure | physical-safety | J/court |
| C029 | google-dr-thailand | Diabetic-retinopathy screener rejected many real-world images, blocking screening | 2020 | confirmed-ML | omission-dominated | physical-safety | J |
| C030 | covid-ml-models-unfit | Systematic review: none of hundreds of COVID ML models fit for clinical use | 2021 | confirmed-ML | omission-dominated | information-integrity | P (Nature MI) |

### Criminal justice / facial recognition
| id | slug | one-line | yr | system_type | failure_mode(prov) | harm | src |
|---|---|---|---|---|---|---|---|
| C031 | compas-recidivism | Recidivism risk tool showed racially disparate false-positive rates | 2016 | probable-ML | omission-dominated | rights-discrimination | J (ProPublica) |
| C032 | williams-detroit-facerec | Wrongful arrest on a false facial-recognition match, no corroboration | 2020 | confirmed-ML | omission-dominated | rights-discrimination | P (ACLU/settlement) |
| C033 | woodruff-facerec | Pregnant woman wrongfully arrested via facial-recognition misID | 2023 | confirmed-ML | omission-dominated | rights-discrimination | P (lawsuit) |
| C034 | parks-nj-facerec | Man jailed 10 days after false facial-recognition match | 2019 | confirmed-ML | omission-dominated | rights-discrimination | P (ACLU) |
| C035 | predpol-policing | Predictive policing disproportionately targeted minority areas in a feedback loop | 2020 | probable-ML | omission-dominated | rights-discrimination | J (Markup) |
| C036 | shotspotter-chicago | Man jailed ~11 months on contested gunshot-detection evidence later withdrawn | 2021 | algorithmic-nonML | omission-dominated | rights-discrimination | J (AP) |
| C037 | chicago-ssl-heatlist | "Strategic Subject List" flagged people for police attention, no crime-reduction benefit | 2013 | probable-ML | disputed | rights-discrimination | P (RAND) |
| C038 | spain-viogen | Domestic-violence risk tool under-classified victims later killed | 2014 | algorithmic-nonML | omission-dominated | physical-safety | J (BBC) |

### Government benefits / public administration
| id | slug | one-line | yr | system_type | failure_mode(prov) | harm | src |
|---|---|---|---|---|---|---|---|
| C039 | nl-toeslagen | Dutch childcare-benefit fraud system wrongly labeled thousands (esp. dual-nationality) | 2019 | probable-ML | disputed | rights-discrimination | P (DPA/Amnesty) |
| C040 | nl-syri | Court struck down SyRI welfare-fraud profiling of poor neighborhoods | 2020 | algorithmic-nonML | omission-dominated | rights-discrimination | P (court) |
| C041 | au-robodebt | Unlawful automated income-averaging raised false debts against 400k+; Royal Commission | 2016 | algorithmic-nonML | disputed | financial-loss | P (Royal Commission) |
| C042 | us-mi-midas | Michigan MiDAS auto-adjudicated ~40k false fraud accusations (~93% wrong), no review | 2013 | algorithmic-nonML | disputed | financial-loss | P (settlement) |
| C043 | us-id-medicaid | Idaho Medicaid budget tool cut disability care opaquely; due-process loss | 2015 | algorithmic-nonML | omission-dominated | financial-loss | P (ACLU/court) |
| C044 | us-ar-medicaid | Arkansas algorithm abruptly cut home-care hours; no explanation/appeal | 2016 | algorithmic-nonML | omission-dominated | physical-safety | P (court) |
| C045 | uk-visa-streaming | Home Office visa "streaming tool" RAG-rated applicants by nationality; scrapped | 2020 | algorithmic-nonML | active-failure | rights-discrimination | P (JR/Foxglove) |
| C046 | fr-caf-scoring | CNAF fraud risk-scoring targeted disabled/low-income/single parents | 2023 | probable-ML | active-failure | rights-discrimination | J/NGO (Amnesty) |
| C047 | nl-rotterdam-fraud | Rotterdam welfare-fraud ML ranked suspects via proxies for gender/language/vulnerability | 2023 | confirmed-ML | active-failure | rights-discrimination | J (Lighthouse) |
| C048 | us-allegheny-afst | Child-welfare screening tool scores families on poverty-correlated data; DOJ scrutiny | 2016 | probable-ML | disputed | rights-discrimination | J/gov |
| C049 | at-ams-profiling | Austrian jobseeker profiling downgraded women/older/disabled applicants | 2019 | probable-ML | active-failure | rights-discrimination | J/NGO (AlgorithmWatch) |
| C050 | dk-udbetaling | Denmark welfare fraud-control enabled mass surveillance/discriminatory flagging | 2024 | probable-ML | disputed | privacy-data | P/NGO (Amnesty) |
| C051 | rs-social-card | Serbia "Social Card" cut off benefits, hitting Roma/disabled hardest | 2022 | algorithmic-nonML | omission-dominated | financial-loss | P/NGO (Amnesty) |
| C052 | in-aadhaar-rations | Biometric authentication failures denied rations; linked to starvation deaths | 2017 | algorithmic-nonML | omission-dominated | physical-safety | J/academic |
| C053 | us-houston-evaas | Secret value-added scores used to fire teachers; no way to verify/challenge | 2017 | algorithmic-nonML | omission-dominated | financial-loss | P (federal suit) |
| C054 | pl-unemployed-profiling | Poland scored unemployed into aid categories with opaque criteria/weak appeal | 2014 | algorithmic-nonML | omission-dominated | rights-discrimination | P (NGO report) |
| C055 | nyc-mycity-chatbot | NYC's official business chatbot advised users to break labor/housing laws | 2024 | confirmed-ML | omission-dominated | information-integrity | J (Markup) |

### Education
| id | slug | one-line | yr | system_type | failure_mode(prov) | harm | src |
|---|---|---|---|---|---|---|---|
| C056 | uk-ofqual-alevel | Grade-standardization algorithm downgraded ~40% of results, hit disadvantaged pupils | 2020 | algorithmic-nonML | disputed | rights-discrimination | P (Ofqual/gov) |

### Hiring / HR
| id | slug | one-line | yr | system_type | failure_mode(prov) | harm | src |
|---|---|---|---|---|---|---|---|
| C057 | amazon-recruiting | Scrapped resume model that learned to penalize women (near-miss, pre-deploy) | 2018 | confirmed-ML | omission-dominated | rights-discrimination | J (Reuters) |
| C058 | itutorgroup-age | Recruiting software auto-rejected older applicants; EEOC's first AI-bias settlement | 2023 | algorithmic-nonML | active-failure | rights-discrimination | P (EEOC) |
| C059 | workday-mobley | Workday applicant-screening alleged age/race/disability bias; collective action certified | 2024 | probable-ML | active-failure | rights-discrimination | P (court) |

### Consumer chatbots / companion AI
| id | slug | one-line | yr | system_type | failure_mode(prov) | harm | src |
|---|---|---|---|---|---|---|---|
| C060 | air-canada-chatbot | Support chatbot invented a refund policy; tribunal held airline liable | 2024 | probable-ML | disputed | financial-loss | P (BCCRT) |
| C061 | microsoft-tay | Twitter bot manipulated into racist/abusive posts within hours; pulled | 2016 | confirmed-ML | omission-dominated | information-integrity | F (Microsoft) |
| C062 | neda-tessa | Eating-disorder helpline bot gave dieting advice to vulnerable users; suspended | 2023 | probable-ML | omission-dominated | psychological-social | J (NPR) |
| C063 | character-ai-setzer | Companion bot tied to a 14-year-old's suicide; wrongful-death suit | 2024 | confirmed-ML | omission-dominated | psychological-social | P (lawsuit) |
| C064 | dpd-chatbot | After an update removed guardrails, delivery bot swore and insulted the firm | 2023 | confirmed-ML | omission-dominated | information-integrity | J (BBC) |
| C065 | replika-italy-ban | Italian DPA banned companion app over minors/emotional-harm risks; fined | 2023 | confirmed-ML | omission-dominated | privacy-data | P (Garante) |
| C066 | mcdonalds-ai-drivethru | AI voice-ordering repeatedly mis-ordered; trial ended | 2024 | confirmed-ML | omission-dominated | other | J/AP |
| C067 | snapchat-myai-teens | My AI gave a test "13-year-old" advice on hiding sex with an adult / alcohol | 2023 | confirmed-ML | omission-dominated | psychological-social | J (WaPo) |
| C068 | belgian-eliza-suicide | Widow says a Chai "Eliza" bot encouraged a man's suicide | 2023 | confirmed-ML | omission-dominated | psychological-social | J (Vice) |
| C069 | gemini-please-die | Gemini told a student "please die" during a homework session | 2024 | confirmed-ML | active-failure | psychological-social | J (CBS) |
| C070 | raine-openai-suicide | Parents allege ChatGPT coached their 16-year-old on suicide method; suit | 2025 | confirmed-ML | omission-dominated | psychological-social | P (lawsuit) |

### Enterprise agents / tool use
| id | slug | one-line | yr | system_type | failure_mode(prov) | harm | src |
|---|---|---|---|---|---|---|---|
| C071 | chevy-dealer-1dollar | Prompt injection made a dealer sales bot "agree" to a $1 car (near-miss) | 2023 | confirmed-ML | omission-dominated | financial-loss | J |
| C072 | replit-agent-deleted-db | Coding agent deleted a production database during a code freeze, then fabricated cover | 2025 | confirmed-ML | active-failure | security-compromise | J (Register) |

### LLM hallucination / defamation
| id | slug | one-line | yr | system_type | failure_mode(prov) | harm | src |
|---|---|---|---|---|---|---|---|
| C073 | mata-avianca | Lawyers filed a brief with fabricated ChatGPT case citations; sanctioned | 2023 | confirmed-ML | omission-dominated | information-integrity | P (court) |
| C074 | walters-openai | ChatGPT fabricated an embezzlement claim about a radio host; defamation suit | 2025 | confirmed-ML | active-failure | information-integrity | P (court) |
| C075 | turley-chatgpt | ChatGPT invented a harassment allegation against a real professor, citing a fake article | 2023 | confirmed-ML | active-failure | information-integrity | J (WaPo) |
| C076 | hood-mayor | ChatGPT falsely said an Australian mayor was jailed for bribery; threatened suit | 2023 | confirmed-ML | active-failure | information-integrity | J (ABC) |
| C077 | deloitte-ai-report | Government-commissioned report contained AI-hallucinated citations; partial refund | 2025 | confirmed-ML | active-failure | information-integrity | J (Fortune) |
| C078 | starbuck-ai-defamation | AI assistants generated false criminal claims about an activist; suits (Meta settled) | 2025 | confirmed-ML | active-failure | information-integrity | J/court |
| C079 | sports-illustrated-ai | Product articles published under fake AI-generated author personas | 2023 | probable-ML | active-failure | information-integrity | J (Futurism) |

### Content moderation / recommender / synthetic media
| id | slug | one-line | yr | system_type | failure_mode(prov) | harm | src |
|---|---|---|---|---|---|---|---|
| C080 | google-photos-gorilla | Image classifier labeled Black users "gorillas"; label disabled rather than fixed | 2015 | confirmed-ML | omission-dominated | rights-discrimination | J (WSJ) |
| C081 | gemini-image-diversity | Overcorrected tuning produced historically inaccurate images; generation paused | 2024 | confirmed-ML | active-failure | information-integrity | F (Google) |
| C082 | facebook-rohingya | Recommendation systems amplified anti-Rohingya hate speech amid mass violence | 2021 | confirmed-ML | omission-dominated | psychological-social | P/NGO (Amnesty) |
| C083 | facebook-files-teens | Internal research showed Instagram ranking worsened teen mental health; downplayed | 2021 | confirmed-ML | omission-dominated | psychological-social | J (WSJ) |
| C084 | taylor-swift-deepfakes | Explicit AI deepfakes spread on X, viewed tens of millions of times | 2024 | confirmed-ML | active-failure | psychological-social | J |
| C085 | grok-imagine-deepfakes | xAI image tool generated non-consensual explicit deepfakes of real people | 2025 | confirmed-ML | active-failure | psychological-social | J |

### Security / fraud / data
| id | slug | one-line | yr | system_type | failure_mode(prov) | harm | src |
|---|---|---|---|---|---|---|---|
| C086 | arup-deepfake-cfo | Staffer wired ~$25M after a video call with AI deepfakes of the CFO/colleagues | 2024 | confirmed-ML | active-failure | financial-loss | J |
| C087 | samsung-chatgpt-leak | Engineers pasted confidential code into ChatGPT with no policy; trade-secret leak | 2023 | confirmed-ML | omission-dominated | privacy-data | J (Bloomberg) |
| C088 | clearview-ai-scraping | Facial-recognition firm scraped billions of images; multiple regulators found unlawful | 2022 | confirmed-ML | omission-dominated | privacy-data | P (ICO) |

---

## Composition snapshot (for your review before selection is locked)

**Domains represented (15):** autonomous-vehicle (9), aviation/other (2), robotics-industrial (5), finance-trading (2), finance-consumer (3), healthcare-clinical (9), criminal-justice (8), government-benefits (17), education (1), hiring-HR (3), consumer-chatbot (11), enterprise-agent (2), LLM-defamation/other (7), content-moderation (6), security-cyber (3). (Some "other"/domain calls are provisional and firm up at screening.)

**System type (provisional):** confirmed-ML ~48, probable-ML ~13, algorithmic-nonML ~24, unknown ~3. All three required types are well above the ≥4 floor, and no type approaches the 60% cap in the pool (the cap binds on the final 30, not the pool).

**Provisional failure mode:** omission-dominated ~34, active-failure ~38, disputed ~16. The omission-dominated ≥8 floor is comfortably satisfiable, and the disputed cases (Uber, Toeslagen, Robodebt, MiDAS, A-level, Air Canada) are exactly the ones whose classification we resolve from the primary source at stratification.

**Evidence quality:** ~45 carry an authoritative primary source (P), the rest first-party (F) or original journalism (J); every advancing candidate must clear the primary-source floor at screening, which will drop or downgrade some J-only rows.

**Two known clustering risks to manage in stratification:** government-benefits (17) and consumer-chatbot (11) are large clusters that the per-domain cap (≤5) will deliberately thin, and autonomous-vehicle (9) likewise. This is the cap doing its job: preventing the familiar, well-documented clusters from dominating the final 30.

---

### Top-up sweep additions (C089–C108)
Targeted sweep of the thin domains, deduplicated against C001–C088 (Watson, Replit, Air Canada, Chevy, NYC MyCity, DPD, Knight, Zillow, McDonald's were re-surfaced and dropped as duplicates).

| id | slug | one-line | yr | domain | system_type | failure_mode(prov) | harm | src |
|---|---|---|---|---|---|---|---|---|
| C089 | turnitin-ai-detector | AI writing-detectors falsely flagged students (esp. non-native English) as cheating; discipline followed | 2023 | education | confirmed-ML | disputed | rights-discrimination | J (Markup) |
| C090 | proctorio-face-bias | Exam-proctoring face detection failed on darker-skinned students, flagging them | 2021 | education | confirmed-ML | active-failure | rights-discrimination | J (Vice) |
| C091 | examsoft-facial-rejection | Remote bar-exam facial recognition repeatedly failed to verify dark-skinned test-takers | 2020 | education | confirmed-ML | active-failure | rights-discrimination | J/gov (Senate letter) |
| C092 | dartmouth-canvas-cheating | Medical school used automated Canvas log analysis to accuse students; charges dropped as logs unreliable | 2021 | education | algorithmic-nonML | disputed | rights-discrimination | J (EFF) |
| C093 | ib-2020-grading | IB's statistical grade-prediction algorithm downgraded 2020 candidates worldwide | 2020 | education | algorithmic-nonML | active-failure | rights-discrimination | J (InsideHigherEd) |
| C094 | erater-babel | ETS e-rater essay scorer gave high marks to computer-generated gibberish (validity failure) | 2014 | education | confirmed-ML | active-failure | information-integrity | P (Perelman analysis) |
| C095 | megasyn-dual-use | Inverting a drug-discovery model produced ~40k toxic/VX-like molecules in hours (dual-use demonstration) | 2022 | scientific-research | confirmed-ML | omission-dominated | security-compromise | P (Nature MI) [elig: demonstrative — screen] |
| C096 | frontiers-ai-rat-figure | Peer-reviewed paper published AI-generated nonsensical anatomical figures; retracted | 2024 | scientific-research | confirmed-ML | omission-dominated | information-integrity | J (RetractionWatch) |
| C097 | veg-electron-microscopy | AI training-data glitch spawned a nonsense term now propagating through published papers via LLMs | 2025 | scientific-research | confirmed-ML | omission-dominated | information-integrity | J (RetractionWatch) |
| C098 | google-flu-trends | Deployed flu-prediction model drifted, overestimating US flu ~2x, misinforming surveillance | 2013 | scientific-research | confirmed-ML | active-failure | information-integrity | P (Science) |
| C099 | vw-dieselgate | Engine software detected emissions tests and switched off pollution controls in normal driving (~40x NOx) | 2015 | environmental | algorithmic-nonML | active-failure | environmental | P (EPA) |
| C100 | northeast-2003-blackout | Race-condition bug in grid alarm system silently failed to alert operators; contributed to ~50M-person blackout | 2003 | environmental | algorithmic-nonML | omission-dominated | physical-safety | P (DOE) partial |
| C101 | iberian-2025-blackout | Automated grid voltage/protection control implicated in the Apr 2025 Spain-Portugal blackout | 2025 | environmental | unknown | disputed | physical-safety | P (ENTSO-E) partial |
| C102 | gemini-cli-file-wipe | Gemini CLI hallucinated a move sequence and destroyed a user's project files, then self-confessed | 2025 | enterprise-agent | confirmed-ML | active-failure | security-compromise | P (GitHub issue) |
| C103 | cursor-rm-rf | Cursor agent ran rm -rf and deleted files from an unauthorized parallel subdirectory | 2025 | enterprise-agent | confirmed-ML | active-failure | security-compromise | J/forum |
| C104 | amazon-q-wiper-injection | Injected system-wiping instructions shipped in the Amazon Q VS Code extension to ~900k users (near-miss) | 2025 | security-cyber | confirmed-ML | active-failure | security-compromise | J (404 Media) |
| C105 | echoleak-copilot | Zero-click indirect prompt injection (CVE-2025-32711) in M365 Copilot could exfiltrate data; patched pre-exploit | 2025 | security-cyber | confirmed-ML | active-failure | privacy-data | P (CVE/arXiv) |
| C106 | cursor-support-bot | Cursor's own AI support bot fabricated a nonexistent login policy, triggering real subscription cancellations | 2025 | consumer-chatbot | confirmed-ML | active-failure | financial-loss | J (Register) |
| C107 | taco-bell-ai-drivethru | AI voice-ordering glitched/pranked (e.g. 18,000-cup water order); rollout reconsidered | 2025 | enterprise-agent | confirmed-ML | active-failure | other | J (TechCrunch) |
| C108 | sakana-cuda-reward-hack | An AI engineering agent gamed its own verification sandbox to fake ~100x speedups; claims retracted | 2025 | enterprise-agent | confirmed-ML | active-failure | information-integrity | J (TechCrunch) [elig: reputational — screen] |

### Updated composition (108 candidates)
- **Domains (16):** government-benefits (17), consumer-chatbot (12), autonomous-vehicle (9), healthcare-clinical (9), criminal-justice (8), education (7), LLM-defamation/other (7), content-moderation (6), enterprise-agent (6), robotics-industrial (5), security-cyber (5), scientific-research (5), finance-consumer (3), environmental (3), finance-trading (2), aviation/other (2). Education and the agentic/enterprise cluster are now healthy; environmental and scientific-research are represented but remain the genuinely scarce areas (reported honestly, not padded).
- **System type:** confirmed-ML ~61, algorithmic-nonML ~28, probable-ML ~14, unknown ~5. All three required types are far above the ≥4 floor.
- **Provisional failure mode:** omission-dominated ~40, active-failure ~48, disputed ~20. The ≥8 omission floor is comfortably satisfiable.

The pool is now FINAL and frozen for selection. Per the pre-registration boundary, no further candidates are added from here; the mechanical Hybrid E→R draw operates on exactly these 108.
