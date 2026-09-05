#!/usr/bin/env python3
"""
AI Safeguard Failure Observatory - dataset builder (single source of truth).
Encodes the 30 QA'd incidents coded in Phase 1B against CIR v0.3, and emits the
four+1 machine-readable tables (incidents, safeguards, relationships,
contributing_factors, sources) as CSV and a combined JSON.

Dataset version: v1.0 (frozen 2026-09-05).

Safeguard tuple positions:
 (sid, name, layer, primary_function, secondary_functions, observed_state,
  inadequacy_type, suspected_absent, timeliness, evidentiary_basis,
  evidence_status, causal_role, existence_timing, confidence, control_group)
Relationship tuple: (from_sid, to_sid, relationship_type, relationship_confidence)
Factor tuple: (name, factor_type, effect_direction, causal_role, confidence)
Source tuple: (url, source_type, label)
"""
import csv, json, os

DATASET_VERSION = "v1.0"
FROZEN = "2026-09-05"

# ---- helper to keep rows terse ----
def SG(sid,name,layer,pf,state,role,exist,conf,timeliness="not-applicable",
       basis="post-incident-finding",evstatus="confirmed-authoritative",
       inad="",suspected=0,secfn="",cg=""):
    return dict(sid=sid,name=name,system_layer=layer,primary_function=pf,
                secondary_functions=secfn,observed_state=state,inadequacy_type=inad,
                suspected_absent=suspected,timeliness=timeliness,evidentiary_basis=basis,
                evidence_status=evstatus,causal_role=role,existence_timing=exist,
                confidence=conf,control_group=cg)
def R(a,b,t,c): return dict(from_sid=a,to_sid=b,relationship_type=t,relationship_confidence=c)
def F(n,ft,ed,role,c): return dict(name=n,factor_type=ft,effect_direction=ed,causal_role=role,confidence=c)
def S(u,t,l): return dict(url=u,source_type=t,label=l)

INC = {}
def add(cid, **kw): INC[cid]=kw

# ============================ INCIDENTS ============================

add("2023-cruise-drag-sf",
 title="Cruise robotaxi drags pedestrian after collision (San Francisco)",
 domain="autonomous-vehicle", domain_detail="", date_start="2023-10-02", date_end="2023-10-02",
 incident_scope="discrete-event", observation_boundary="",
 harm_primary="physical-safety", harm_secondary="", outcome_class="realized-harm",
 system_type="confirmed-ML", era="legacy", agentic=0,
 ai_causal_contribution="major-contributor", attributed_primary_cause="multiple",
 incident_confidence="high",
 safeguards=[
  SG("S1","Perception / pedestrian avoidance at impact","application","preventive","Failed","contributing","incident-time","medium",timeliness="too-late",basis="post-incident-finding;direct-artifact"),
  SG("S2","Emergency hard-braking","application","containment","Working","mitigating","incident-time","medium",timeliness="in-time",basis="direct-artifact"),
  SG("S3","Post-collision decision logic (collision classification)","application","containment","Failed","primary","incident-time","high",timeliness="too-late"),
  SG("S4","Do-not-move-with-person-underneath occupancy stop","application","containment","Absent","primary","incident-time","medium",basis="comparable-system;post-incident-finding"),
  SG("S5","Remote-assistance human oversight","human-operator","detective","Bypassed","contributing","incident-time","low",timeliness="too-late"),
  SG("S6","Organizational honest disclosure to regulators","organizational-process","assurance-governance","Failed","aggravating","incident-time","high",timeliness="too-late",basis="post-incident-finding;direct-artifact"),
  SG("S7","External regulatory oversight (DMV/NHTSA/CPUC/DOJ)","external-ecosystem","recovery","Working","mitigating","incident-time","high",timeliness="too-late",basis="direct-artifact"),
  SG("S8","Software fix: collision-classification remains stationary","application","containment","Working","not-causally-relevant","added-after","high",timeliness="in-time",basis="direct-artifact"),
 ],
 relationships=[R("S3","S4","enabling","medium"),R("S6","S7","masking","high"),R("S1","S3","temporal-precedence","high")],
 factors=[F("Cruise us-versus-them posture / move-fast pressure","cultural","harm-amplifying","aggravating","medium")],
 sources=[S("https://www.justice.gov/usao-ndca/pr/cruise-admits-submitting-false-report-influence-federal-investigation-and-agrees-pay","primary","US DOJ deferred-prosecution announcement"),
          S("https://static.nhtsa.gov/odi/rcl/2023/RCLRPT-23E086-7725.PDF","primary","NHTSA recall 23E-086")])

add("2015-2020-au-robodebt",
 title="Robodebt automated welfare-debt scheme (Australia)",
 domain="government-benefits", domain_detail="", date_start="2016", date_end="2020",
 incident_scope="systemic-program",
 observation_boundary="Online Compliance Intervention income-averaging debt-raising, ~2016 rollout to 2020 wind-down; excludes unrelated Centrelink compliance.",
 harm_primary="financial-loss", harm_secondary="psychological-social", outcome_class="realized-harm",
 system_type="algorithmic-nonML", era="legacy", agentic=0,
 ai_causal_contribution="major-contributor", attributed_primary_cause="organizational",
 incident_confidence="high",
 safeguards=[
  SG("S1","Correct calculation on actual fortnightly income","application","preventive","Absent","primary","incident-time","high",basis="regulation-policy;post-incident-finding"),
  SG("S2","Legality / lawful-basis check (internal legal advice)","organizational-process","preventive","Disabled","primary","incident-time","high"),
  SG("S3","Human officer verification before debt-raising (incl. burden-of-proof on government)","human-operator","preventive","Disabled","primary","incident-time","high",basis="regulation-policy;post-incident-finding"),
  SG("S5","Recipient challenge / appeal mechanism","human-operator","recovery","Inadequate","contributing","incident-time","high",timeliness="too-late",inad="operation"),
  SG("S6","Internal governance: heed warnings / AAT rulings","organizational-process","detective","Failed","contributing","incident-time","high",timeliness="too-late"),
  SG("S7","External oversight: Commonwealth Ombudsman","external-ecosystem","detective","Bypassed","contributing","incident-time","medium",timeliness="delayed"),
  SG("S8","External oversight: courts (Amato / Prygodicz)","external-ecosystem","recovery","Working","mitigating","incident-time","high",timeliness="too-late",basis="direct-artifact"),
  SG("S9","External oversight: Royal Commission","external-ecosystem","recovery","Working","mitigating","incident-time","high",timeliness="too-late",basis="direct-artifact"),
 ],
 relationships=[R("S2","S1","enabling","medium"),R("S3","S5","enabling","medium"),R("S7","S8","masking","medium")],
 factors=[F("Budget-savings mandate / cost-recovery pressure","incentive-structure","harm-enabling","aggravating","medium")],
 sources=[S("https://robodebt.royalcommission.gov.au/publications/report","primary","Royal Commission into the Robodebt Scheme final report"),
          S("https://www.legalaid.vic.gov.au/explainer-deanna-amatos-robo-debt-case","primary","Amato v Commonwealth (unlawfulness concession)")])

add("2013-2019-optum-impact-pro",
 title="Cost-as-proxy racial bias in a health risk-prediction algorithm (Optum/Impact Pro)",
 domain="healthcare-clinical", domain_detail="", date_start="2013", date_end="2019",
 incident_scope="systemic-program",
 observation_boundary="The commercial cost-based care-management risk-prediction algorithm studied by Obermeyer et al. (2019); label-choice bias and triage use; excludes other vendor products.",
 harm_primary="rights-discrimination", harm_secondary="physical-safety", outcome_class="realized-harm",
 system_type="probable-ML", era="legacy", agentic=0,
 ai_causal_contribution="major-contributor", attributed_primary_cause="organizational",
 incident_confidence="high",
 safeguards=[
  SG("S1","Target-label validation (does cost equal need?)","model","preventive","Absent","primary","incident-time","medium"),
  SG("S2","Pre-deployment subgroup (racial) fairness audit","organizational-process","detective","Absent","latent-condition","incident-time","medium"),
  SG("S3","Human clinical oversight / override in enrollment","human-operator","detective","Inadequate","contributing","incident-time","medium",inad="design"),
  SG("S4","Deployment bias monitoring (internal)","organizational-process","detective","Absent","latent-condition","incident-time","medium"),
  SG("S5","External research scrutiny (detection)","external-ecosystem","detective","Working","mitigating","incident-time","high",timeliness="too-late",basis="direct-artifact"),
  SG("S6","External regulatory oversight (NY DFS/DoH)","external-ecosystem","recovery","Working","mitigating","incident-time","medium",timeliness="too-late",basis="direct-artifact"),
  SG("S7","Vendor remediation: retrain on blended target","model","recovery","Working","not-causally-relevant","added-after","medium",timeliness="in-time"),
 ],
 relationships=[R("S1","S3","enabling","medium"),R("S2","S4","common-cause","medium"),R("S1","S5","temporal-precedence","high")],
 factors=[F("Upstream structural inequity (less spent on Black patients at equal illness)","economic","harm-causing","primary","high")],
 sources=[S("https://www.science.org/doi/10.1126/science.aax2342","primary","Obermeyer et al., Science 2019"),
          S("https://www.dfs.ny.gov/reports-and-publications/comment-letters/dfs-doh-joint-letter-uhgi-20191025","primary","NY DFS/DoH inquiry letter")])

add("2022-air-canada-chatbot",
 title="Air Canada support chatbot asserts non-existent refund policy",
 domain="consumer-chatbot", domain_detail="", date_start="2022-11-11", date_end="2022-11-11",
 incident_scope="discrete-event", observation_boundary="",
 harm_primary="financial-loss", harm_secondary="", outcome_class="realized-harm",
 system_type="probable-ML", era="genai", agentic=0,
 ai_causal_contribution="major-contributor", attributed_primary_cause="organizational",
 incident_confidence="high",
 safeguards=[
  SG("S1","Output grounding / verification vs real policy","application","preventive","Unknown","primary","incident-time","low",suspected=1,basis="inferred-indirect",evstatus="inferred-indirect"),
  SG("S2","Human review of chatbot answers","human-operator","detective","Absent","contributing","incident-time","low",basis="established-practice",evstatus="inferred-indirect"),
  SG("S3","Effective disclaimer / ToS carve-out","application","containment","Absent","contributing","incident-time","medium",basis="comparable-system",evstatus="single-source-reported"),
  SG("S4","Linked correct policy page (reachability)","application","containment","Inadequate","contributing","incident-time","high",inad="design",basis="direct-artifact"),
  SG("S5","Pre-deployment accuracy testing","organizational-process","preventive","Unknown","latent-condition","incident-time","low",suspected=1,basis="inferred-indirect",evstatus="inferred-indirect"),
  SG("S6","Organizational accountability (separate-entity defense)","organizational-process","assurance-governance","Failed","aggravating","incident-time","high",timeliness="too-late",basis="direct-artifact"),
  SG("S7","External adjudication (Civil Resolution Tribunal)","external-ecosystem","recovery","Working","mitigating","incident-time","high",timeliness="too-late",basis="direct-artifact"),
 ],
 relationships=[R("S1","S4","temporal-precedence","low"),R("S2","S1","temporal-precedence","low"),R("S6","S7","temporal-precedence","high")],
 factors=[],
 sources=[S("https://www.canlii.org/en/bc/bccrt/doc/2024/2024bccrt149/2024bccrt149.html","primary","Moffatt v. Air Canada, 2024 BCCRT 149")])

add("2025-gemini-cli-file-destruction",
 title="Gemini CLI coding agent destroys user files on hallucinated state",
 domain="enterprise-agent", domain_detail="", date_start="2025-07", date_end="2025-07",
 incident_scope="discrete-event", observation_boundary="",
 harm_primary="security-compromise", harm_secondary="", outcome_class="realized-harm",
 system_type="confirmed-ML", era="genai", agentic=1,
 ai_causal_contribution="major-contributor", attributed_primary_cause="AI-system",
 incident_confidence="medium",
 safeguards=[
  SG("S1","Internal command-success verification (read-after-write)","application","detective","Failed","primary","incident-time","medium",timeliness="too-late",basis="direct-artifact",evstatus="single-source-reported"),
  SG("S2","Human confirmation before destructive commands","human-operator","preventive","Unknown","contributing","incident-time","low",basis="operator-claim",evstatus="disputed"),
  SG("S3","Sandboxing / write-scope containment","infrastructure-environment","containment","Inadequate","contributing","incident-time","medium",inad="operation",basis="direct-artifact",evstatus="single-source-reported"),
  SG("S4","Dry-run / preview of net effect","application","preventive","Absent","contributing","incident-time","medium",basis="comparable-system",evstatus="inferred-indirect"),
  SG("S5","Backup / undo / recovery","infrastructure-environment","recovery","Absent","contributing","incident-time","medium",basis="comparable-system;established-practice",evstatus="multiply-reported"),
  SG("S6","Real-time failure detection / auto-halt","application","detective","Failed","contributing","incident-time","medium",timeliness="too-late",basis="direct-artifact",evstatus="single-source-reported"),
 ],
 relationships=[R("S1","S6","enabling","medium"),R("S1","S3","temporal-precedence","low"),R("S4","S5","common-cause","low")],
 factors=[F("User ran agent on un-version-controlled files with sandbox disabled","other","harm-enabling","contributing","medium")],
 sources=[S("https://github.com/google-gemini/gemini-cli/issues/4586","primary","GitHub issue #4586 (user report)"),
          S("https://incidentdatabase.ai/cite/1178/","secondary","AI Incident Database #1178")])

add("2018-2019-boeing-737max-mcas",
 title="Boeing 737 MAX MCAS crashes (Lion Air 610, Ethiopian 302)",
 domain="other", domain_detail="aviation", date_start="2018-10-29", date_end="2019-03-10",
 incident_scope="bounded-episode",
 observation_boundary="The MCAS design/certification failure and the two 737 MAX accidents plus the between-crash period; excludes broader 737 MAX issues unrelated to MCAS.",
 harm_primary="physical-safety", harm_secondary="", outcome_class="realized-harm",
 system_type="algorithmic-nonML", era="legacy", agentic=0,
 ai_causal_contribution="major-contributor", attributed_primary_cause="multiple",
 incident_confidence="high",
 safeguards=[
  SG("S1","MCAS control-law bounding (authority limit, single activation)","model","containment","Inadequate","primary","incident-time","high",inad="design"),
  SG("S2","AoA sensor redundancy / cross-check","infrastructure-environment","preventive","Absent","primary","incident-time","high",basis="comparable-system;post-incident-finding"),
  SG("S3","AoA Disagree alert","application","detective","Disabled","contributing","incident-time","high"),
  SG("S4","Pilot disclosure & training on MCAS","organizational-process","assurance-governance","Disabled","primary","incident-time","high",basis="post-incident-finding;direct-artifact"),
  SG("S5","Runaway-trim / stab-cutout recovery procedure","human-operator","recovery","Inadequate","contributing","incident-time","high",timeliness="delayed",inad="operation"),
  SG("S6","System safety analysis / hazard classification","organizational-process","assurance-governance","Failed","primary","incident-time","high"),
  SG("S7","FAA certification oversight (ODA delegation)","external-ecosystem","assurance-governance","Inadequate","latent-condition","incident-time","high",inad="enforcement"),
  SG("S8","Between-crash intervention (Emergency AD, no grounding)","external-ecosystem","containment","Inadequate","contributing","incident-time","high",timeliness="delayed",inad="design",basis="post-incident-finding;direct-artifact"),
  SG("S9","MCAS redesign + grounding + training","model","containment","Working","not-causally-relevant","added-after","high",timeliness="in-time",basis="direct-artifact"),
 ],
 relationships=[R("S6","S2","enabling","high"),R("S2","S1","enabling","high"),R("S4","S5","enabling","high"),R("S3","S5","masking","medium"),R("S8","S1","enabling","medium")],
 factors=[F("Schedule/competitive pressure vs Airbus A320neo","incentive-structure","harm-enabling","aggravating","medium")],
 sources=[S("https://democrats-transportation.house.gov/imo/media/doc/final_boeing_737_max_report1.pdf","primary","US House T&I Committee final report (2020)"),
          S("https://www.justice.gov/opa/pr/boeing-charged-737-max-fraud-conspiracy-and-agrees-pay-over-25-billion","primary","US DOJ deferred-prosecution (2021)")])

add("2013-2021-nl-toeslagen",
 title="Dutch childcare benefits scandal (Toeslagenaffaire) risk-classification system",
 domain="government-benefits", domain_detail="", date_start="2013", date_end="2021",
 incident_scope="systemic-program",
 observation_boundary="The childcare-benefit fraud risk-classification system and its safeguards (~2013-2020) and resulting harms; excludes the separate FSV blacklist.",
 harm_primary="rights-discrimination", harm_secondary="financial-loss;psychological-social", outcome_class="realized-harm",
 system_type="probable-ML", era="legacy", agentic=0,
 ai_causal_contribution="major-contributor", attributed_primary_cause="organizational",
 incident_confidence="medium",
 safeguards=[
  SG("S1","Human-rights / data-protection impact assessment (pre-deployment)","organizational-process","assurance-governance","Absent","latent-condition","incident-time","high",basis="regulation-policy;post-incident-finding"),
  SG("S2","Bias mitigation / removal of nationality feature","model","preventive","Absent","primary","incident-time","high",basis="post-incident-finding;regulation-policy"),
  SG("S3","Model transparency / explainability","application","detective","Absent","latent-condition","incident-time","high"),
  SG("S4","Meaningful individual human review of flagged cases","human-operator","detective","Bypassed","primary","incident-time","high"),
  SG("S5","Proportionality safeguard on benefit reclamation","application","containment","Absent","primary","incident-time","high"),
  SG("S6","Legal basis / GDPR compliance","organizational-process","preventive","Failed","primary","incident-time","high",basis="regulation-policy;post-incident-finding"),
  SG("S7","Internal accountability / honest disclosure to regulator","organizational-process","assurance-governance","Failed","aggravating","incident-time","high"),
  SG("S8","External oversight: Data Protection Authority","external-ecosystem","detective","Working","mitigating","incident-time","high",timeliness="too-late",basis="direct-artifact"),
  SG("S9","External oversight: courts / parliament","external-ecosystem","recovery","Working","mitigating","incident-time","high",timeliness="too-late",basis="direct-artifact"),
 ],
 relationships=[R("S3","S4","enabling","high"),R("S2","S4","enabling","medium"),R("S1","S2","enabling","medium"),R("S7","S8","masking","medium")],
 factors=[F("Cost-recovery / fraud-savings incentive","incentive-structure","harm-enabling","aggravating","medium")],
 sources=[S("https://www.amnesty.org/en/documents/eur35/4686/2021/en/","primary","Amnesty International, Xenophobic Machines (2021)"),
          S("https://autoriteitpersoonsgegevens.nl/uploads/imported/boetebesluit_belastingdienst.pdf","primary","Autoriteit Persoonsgegevens fine decision")])

add("2020-williams-detroit-facerec",
 title="Wrongful arrest of Robert Williams after a false facial-recognition match",
 domain="criminal-justice", domain_detail="", date_start="2020-01-09", date_end="2020-01-09",
 incident_scope="discrete-event", observation_boundary="",
 harm_primary="rights-discrimination", harm_secondary="psychological-social", outcome_class="realized-harm",
 system_type="confirmed-ML", era="legacy", agentic=0,
 ai_causal_contribution="major-contributor", attributed_primary_cause="organizational",
 incident_confidence="high",
 safeguards=[
  SG("S1","'Investigative lead only, not probable cause' policy","organizational-process","preventive","Bypassed","primary","incident-time","high",basis="direct-artifact;post-incident-finding"),
  SG("S2","Independent human corroboration before arrest","human-operator","preventive","Absent","primary","incident-time","high",basis="established-practice;post-incident-finding"),
  SG("S3","Photo-lineup integrity (untainted witness)","human-operator","detective","Inadequate","contributing","incident-time","high",inad="operation"),
  SG("S4","Image-quality / match-confidence threshold","application","preventive","Absent","contributing","incident-time","medium",basis="comparable-system",evstatus="inferred-indirect"),
  SG("S5","FR analyst / examiner verification","human-operator","detective","Inadequate","contributing","incident-time","medium",inad="operation",evstatus="multiply-reported"),
  SG("S6","Warrant / judicial pre-arrest check","external-ecosystem","preventive","Bypassed","contributing","incident-time","medium"),
  SG("S7","Prosecutorial review / charge dismissal","external-ecosystem","recovery","Working","mitigating","incident-time","high",timeliness="too-late",basis="direct-artifact"),
  SG("S8","Detroit PD facial-recognition policy","organizational-process","preventive","Working","not-causally-relevant","added-after","high",timeliness="in-time",basis="direct-artifact"),
 ],
 relationships=[R("S1","S2","enabling","high"),R("S4","S1","enabling","medium"),R("S3","S6","enabling","medium")],
 factors=[F("Higher facial-recognition misidentification rates for people of colour","other","harm-amplifying","contributing","medium")],
 sources=[S("https://www.aclu.org/cases/williams-v-city-of-detroit-face-recognition-false-arrest","primary","ACLU, Williams v. City of Detroit"),
          S("https://www.aclu.org/press-releases/civil-rights-advocates-achieve-the-nations-strongest-police-department-policy-on-facial-recognition-technology","primary","2024 settlement / DPD policy")])

add("2023-mata-avianca-chatgpt",
 title="Lawyers file ChatGPT-fabricated case citations (Mata v. Avianca)",
 domain="other", domain_detail="legal", date_start="2023-03", date_end="2023-06-22",
 incident_scope="discrete-event", observation_boundary="",
 harm_primary="information-integrity", harm_secondary="", outcome_class="realized-harm",
 system_type="confirmed-ML", era="genai", agentic=0,
 ai_causal_contribution="major-contributor", attributed_primary_cause="human-operator",
 incident_confidence="high",
 safeguards=[
  SG("S1","Attorney verification of cited cases vs a real database (Rule 11)","human-operator","preventive","Bypassed","primary","incident-time","high",basis="direct-artifact"),
  SG("S2","Signing-attorney gatekeeping inquiry","human-operator","preventive","Bypassed","contributing","incident-time","high",basis="direct-artifact"),
  SG("S3","Firm AI-use / tool-appropriateness policy","organizational-process","preventive","Unknown","latent-condition","incident-time","low",suspected=1,basis="inferred-indirect",evstatus="inferred-indirect"),
  SG("S4","Detection (opposing counsel + court)","external-ecosystem","detective","Working","mitigating","incident-time","high",timeliness="too-late",basis="direct-artifact"),
  SG("S5","Accountability / Rule 11 sanctions","external-ecosystem","recovery","Working","mitigating","incident-time","high",timeliness="too-late",basis="direct-artifact"),
  SG("S6","Court standing orders on AI disclosure","external-ecosystem","preventive","Working","not-causally-relevant","added-after","high",timeliness="in-time",basis="direct-artifact"),
 ],
 relationships=[R("S1","S2","common-cause","medium"),R("S1","S4","temporal-precedence","high")],
 factors=[F("Asking ChatGPT to self-confirm the cases (illusory verification)","other","harm-enabling","contributing","high")],
 sources=[S("https://law.justia.com/cases/federal/district-courts/new-york/nysdce/1:2022cv01461/575368/54/","primary","Mata v. Avianca, sanctions opinion (SDNY 2023)")])

add("2025-echoleak-m365-copilot",
 title="EchoLeak zero-click prompt-injection data exfiltration in M365 Copilot",
 domain="security-cyber", domain_detail="", date_start="2025", date_end="2025-06",
 incident_scope="discrete-event", observation_boundary="",
 harm_primary="privacy-data", harm_secondary="", outcome_class="near-miss",
 system_type="confirmed-ML", era="genai", agentic=1,
 ai_causal_contribution="major-contributor", attributed_primary_cause="AI-system",
 incident_confidence="medium",
 safeguards=[
  SG("S1","Prompt-injection classifiers (XPIA)","application","detective","Bypassed","primary","incident-time","medium",basis="operator-claim;direct-artifact",evstatus="multiply-reported"),
  SG("S2","Data-scope / trust-boundary isolation (least privilege)","infrastructure-environment","containment","Inadequate","primary","incident-time","medium",inad="design",basis="direct-artifact",evstatus="single-source-reported"),
  SG("S3","Markdown link/image redaction","application","containment","Inadequate","contributing","incident-time","medium",inad="design",basis="direct-artifact",evstatus="single-source-reported"),
  SG("S4","CSP / URL egress allowlist","infrastructure-environment","containment","Bypassed","contributing","incident-time","medium",basis="direct-artifact",evstatus="single-source-reported"),
  SG("S5","Human-in-the-loop confirmation at exfiltration","human-operator","preventive","Absent","contributing","incident-time","medium",basis="comparable-system",evstatus="inferred-indirect"),
  SG("S6","Detection (Aim Labs responsible disclosure)","external-ecosystem","detective","Working","mitigating","incident-time","high",timeliness="in-time",basis="direct-artifact"),
  SG("S7","Remediation (Microsoft server-side fix)","application","recovery","Working","not-causally-relevant","added-after","high",timeliness="in-time",basis="operator-claim",evstatus="multiply-reported"),
 ],
 relationships=[R("S1","S2","enabling","medium"),R("S3","S4","enabling","medium"),R("S2","S5","enabling","low")],
 factors=[F("Immature prompt-injection defence tooling / scarce detection datasets","other","harm-enabling","contributing","low")],
 sources=[S("https://nvd.nist.gov/vuln/detail/cve-2025-32711","primary","NVD CVE-2025-32711"),
          S("https://www.catonetworks.com/blog/breaking-down-echoleak/","secondary","Aim/Cato technical disclosure")])

add("2016-tesla-autopilot-williston",
 title="Tesla Autopilot fatal crash (Williston, FL; Joshua Brown)",
 domain="autonomous-vehicle", domain_detail="", date_start="2016-05-07", date_end="2016-05-07",
 incident_scope="discrete-event", observation_boundary="",
 harm_primary="physical-safety", harm_secondary="", outcome_class="realized-harm",
 system_type="confirmed-ML", era="legacy", agentic=0,
 ai_causal_contribution="major-contributor", attributed_primary_cause="multiple",
 incident_confidence="high",
 safeguards=[
  SG("S1","Perception / crossing-object detection","application","preventive","Inadequate","primary","incident-time","high",inad="design"),
  SG("S2","Automatic emergency braking","application","containment","Inadequate","primary","incident-time","high",inad="design"),
  SG("S3","Driver-attention monitoring","application","detective","Inadequate","primary","incident-time","high",inad="design"),
  SG("S4","Operational-design-domain enforcement / geofence","application","preventive","Absent","contributing","incident-time","high",basis="comparable-system;post-incident-finding"),
  SG("S5","Driver attention / intervention (human)","human-operator","recovery","Failed","primary","incident-time","high",timeliness="too-late"),
  SG("S6","Post-incident hands-on escalation + Autosteer strike-out","application","detective","Working","not-causally-relevant","added-after","high",timeliness="in-time",basis="direct-artifact"),
 ],
 relationships=[R("S1","S2","enabling","high"),R("S3","S5","enabling","high"),R("S4","S1","enabling","medium")],
 factors=[F("Truck driver's failure to yield the right of way","other","harm-causing","primary","high"),
          F("Driver operating above the speed limit","other","harm-amplifying","contributing","high")],
 sources=[S("https://www.ntsb.gov/Investigations/Accidentreports/Reports/Har1702.pdf","primary","NTSB HAR-17/02"),
          S("https://static.nhtsa.gov/odi/inv/2016/INCLA-PE16007-7876.PDF","primary","NHTSA ODI PE16-007")])

add("2016-compas-recidivism",
 title="COMPAS recidivism risk scoring and the fairness dispute",
 domain="criminal-justice", domain_detail="", date_start="2016", date_end="2016",
 incident_scope="systemic-program",
 observation_boundary="COMPAS pretrial/sentencing risk scoring as examined by ProPublica (Broward County) and State v. Loomis; excludes other risk tools.",
 harm_primary="rights-discrimination", harm_secondary="", outcome_class="realized-harm",
 system_type="algorithmic-nonML", era="legacy", agentic=0,
 ai_causal_contribution="disputed", attributed_primary_cause="disputed",
 incident_confidence="medium",
 safeguards=[
  SG("S1","Independent pre-deployment disparate-impact validation","organizational-process","assurance-governance","Absent","latent-condition","incident-time","high"),
  SG("S2","Algorithmic transparency (non-proprietary scoring)","application","detective","Absent","latent-condition","incident-time","high",basis="direct-artifact;post-incident-finding"),
  SG("S3","Model fairness constraint (equalized error rates)","model","preventive","Disputed","unknown","incident-time","medium",basis="research-evidence",evstatus="disputed"),
  SG("S4","Human oversight (judge in the loop)","human-operator","containment","Inadequate","contributing","incident-time","medium",inad="design"),
  SG("S5","Due-process protections (State v. Loomis restrictions)","external-ecosystem","assurance-governance","Working","mitigating","incident-time","high",timeliness="too-late",basis="direct-artifact"),
  SG("S6","Loomis-mandated warning advisement","external-ecosystem","assurance-governance","Working","not-causally-relevant","added-after","high",timeliness="in-time",basis="direct-artifact"),
 ],
 relationships=[R("S2","S4","enabling","high"),R("S1","S3","temporal-precedence","low")],
 factors=[F("Differing group base rates make calibration and equalized error rates incompatible","other","harm-enabling","primary","high")],
 sources=[S("https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing","secondary","ProPublica, Machine Bias (2016)"),
          S("https://www.wicourts.gov/sc/opinion/DisplayDocument.pdf?content=pdf&seqNo=171690","primary","State v. Loomis, 2016 WI 68")])

add("2016-microsoft-tay",
 title="Microsoft Tay chatbot manipulated into abusive output",
 domain="consumer-chatbot", domain_detail="", date_start="2016-03-23", date_end="2016-03-24",
 incident_scope="discrete-event", observation_boundary="",
 harm_primary="information-integrity", harm_secondary="psychological-social", outcome_class="realized-harm",
 system_type="confirmed-ML", era="legacy", agentic=0,
 ai_causal_contribution="major-contributor", attributed_primary_cause="multiple",
 incident_confidence="high",
 safeguards=[
  SG("S1","Output content filter (learning/generation path)","application","preventive","Inadequate","primary","incident-time","medium",inad="design",basis="operator-claim;post-incident-finding",evstatus="multiply-reported"),
  SG("S2","Online-learning poisoning safeguard","application","preventive","Absent","primary","incident-time","high",basis="comparable-system;post-incident-finding"),
  SG("S3","Adversarial testing / red-teaming pre-launch","organizational-process","assurance-governance","Inadequate","latent-condition","incident-time","medium",inad="design",basis="operator-claim",evstatus="single-source-reported"),
  SG("S4","Guard on the 'repeat after me' function","application","preventive","Absent","contributing","incident-time","medium",basis="direct-artifact",evstatus="multiply-reported"),
  SG("S5","Real-time abuse monitoring / auto-halt","application","detective","Unknown","contributing","incident-time","low",suspected=1,basis="inferred-indirect",evstatus="inferred-indirect"),
  SG("S6","Kill-switch / takedown","human-operator","containment","Working","mitigating","incident-time","high",timeliness="too-late",basis="operator-claim",evstatus="multiply-reported"),
 ],
 relationships=[R("S3","S2","enabling","medium"),R("S2","S6","temporal-precedence","high"),R("S5","S6","enabling","medium")],
 factors=[F("Coordinated off-platform adversarial campaign (4chan)","other","harm-causing","primary","high")],
 sources=[S("https://blogs.microsoft.com/blog/2016/03/25/learning-tays-introduction/","primary","Microsoft, Learning from Tay's introduction")])

add("2020-clearview-ai-scraping",
 title="Clearview AI non-consensual facial-recognition scraping",
 domain="security-cyber", domain_detail="privacy", date_start="2017", date_end="2022",
 incident_scope="systemic-program",
 observation_boundary="Clearview's non-consensual scraping of billions of facial images (~2017 onward) and 2021-2022 regulatory findings; excludes post-2022 appeals.",
 harm_primary="privacy-data", harm_secondary="", outcome_class="realized-harm",
 system_type="confirmed-ML", era="legacy", agentic=0,
 ai_causal_contribution="major-contributor", attributed_primary_cause="organizational",
 incident_confidence="high",
 safeguards=[
  SG("S1","Consent / lawful basis for biometric processing","organizational-process","preventive","Absent","primary","incident-time","high",basis="regulation-policy;post-incident-finding"),
  SG("S2","Data-protection-by-design / DPIA","organizational-process","assurance-governance","Absent","latent-condition","incident-time","medium"),
  SG("S3","Transparency / notice / opt-out","organizational-process","preventive","Absent","contributing","incident-time","high",basis="regulation-policy;post-incident-finding"),
  SG("S4","Purpose-limitation & retention limits","organizational-process","containment","Absent","contributing","incident-time","high",basis="regulation-policy;post-incident-finding"),
  SG("S5","External oversight: data-protection authorities","external-ecosystem","detective","Working","mitigating","incident-time","high",timeliness="too-late",basis="direct-artifact"),
  SG("S6","Structural restraint: US BIPA / ACLU settlement","external-ecosystem","containment","Working","mitigating","incident-time","high",timeliness="too-late",basis="direct-artifact"),
  SG("S7","Enforcement of deletion / cease orders","external-ecosystem","recovery","Failed","not-causally-relevant","incident-time","high",timeliness="too-late",basis="direct-artifact",evstatus="multiply-reported"),
 ],
 relationships=[R("S2","S1","enabling","medium"),R("S1","S3","common-cause","medium"),R("S5","S7","temporal-precedence","high")],
 factors=[F("Absence of an international enforcement convention","political","harm-enabling","contributing","medium")],
 sources=[S("https://ico.org.uk/action-weve-taken/enforcement/clearview-ai-inc-mpn/","primary","UK ICO enforcement"),
          S("https://www.oaic.gov.au/news/media-centre/clearview-ai-breached-australians-privacy","primary","OAIC determination")])

add("2020-uk-ofqual-alevel",
 title="UK Ofqual A-level grading algorithm and its withdrawal",
 domain="education", domain_detail="", date_start="2020-03-18", date_end="2020-08-17",
 incident_scope="bounded-episode",
 observation_boundary="The 2020 England A-level/GCSE algorithmic standardisation and its withdrawal (Mar-Aug 2020); England-focused; excludes SQA/Wales/NI parallel episodes.",
 harm_primary="rights-discrimination", harm_secondary="psychological-social", outcome_class="realized-harm",
 system_type="algorithmic-nonML", era="legacy", agentic=0,
 ai_causal_contribution="major-contributor", attributed_primary_cause="organizational",
 incident_confidence="high",
 safeguards=[
  SG("S1","Equality / fairness impact assessment","organizational-process","assurance-governance","Inadequate","primary","incident-time","high",inad="design",basis="direct-artifact;post-incident-finding"),
  SG("S2","Individual-level validation / testing","organizational-process","assurance-governance","Inadequate","primary","incident-time","high",inad="design"),
  SG("S3","Appeals / redress mechanism","organizational-process","recovery","Inadequate","contributing","incident-time","high",timeliness="too-late",inad="operation",basis="direct-artifact"),
  SG("S4","External expert review & oversight (RSS, Education Committee)","organizational-process","assurance-governance","Bypassed","primary","incident-time","high",basis="direct-artifact"),
  SG("S5","Transparency (model published for scrutiny pre-results)","application","assurance-governance","Inadequate","contributing","incident-time","high",inad="design",basis="direct-artifact;post-incident-finding"),
  SG("S6","Recovery / rollback to teacher-assessed grades","external-ecosystem","recovery","Working","mitigating","incident-time","high",timeliness="too-late",basis="direct-artifact"),
  SG("S7","Post-incident: code publication + OSR review","organizational-process","assurance-governance","Working","not-causally-relevant","added-after","high",timeliness="in-time",basis="direct-artifact"),
 ],
 relationships=[R("S4","S1","enabling","high"),R("S4","S5","enabling","medium"),R("S2","S3","enabling","medium")],
 factors=[F("Political mandate to prevent grade inflation / preserve aggregate comparability","political","harm-enabling","primary","medium")],
 sources=[S("https://publications.parliament.uk/pa/cm5801/cmselect/cmeduc/617/61705.htm","primary","House of Commons Education Committee report"),
          S("https://osr.statisticsauthority.gov.uk/our-regulatory-work/osr-review-of-approach-to-developing-statistical-models-designed-for-awarding-2020-exam-results/","primary","OSR review")])

add("2013-2015-us-mi-midas",
 title="Michigan MiDAS automated unemployment-fraud false accusations",
 domain="government-benefits", domain_detail="", date_start="2013-10", date_end="2015-08",
 incident_scope="systemic-program",
 observation_boundary="MiDAS auto-adjudication of unemployment fraud with no human review (Oct 2013-Aug 2015) and the ~40,000 false accusations; excludes broader UIA operations.",
 harm_primary="financial-loss", harm_secondary="psychological-social", outcome_class="realized-harm",
 system_type="algorithmic-nonML", era="legacy", agentic=0,
 ai_causal_contribution="major-contributor", attributed_primary_cause="organizational",
 incident_confidence="high",
 safeguards=[
  SG("S1","Human review before fraud determination / penalty","human-operator","preventive","Disabled","primary","incident-time","high",basis="direct-artifact;post-incident-finding"),
  SG("S2","Evidentiary-basis requirement (real evidence, not inference)","organizational-process","preventive","Absent","primary","incident-time","high",basis="regulation-policy;post-incident-finding"),
  SG("S3","Adequate notice / due process","application","preventive","Failed","primary","incident-time","high",basis="direct-artifact"),
  SG("S4","Pre-deployment testing / validation","organizational-process","assurance-governance","Inadequate","latent-condition","incident-time","medium",inad="design",evstatus="multiply-reported"),
  SG("S5","Internal governance / response to the error signal","organizational-process","detective","Failed","contributing","incident-time","high",timeliness="too-late"),
  SG("S6","External oversight: Auditor General","external-ecosystem","detective","Working","mitigating","incident-time","high",timeliness="too-late",basis="direct-artifact"),
  SG("S7","External oversight: courts (Bauserman/Cahoo)","external-ecosystem","recovery","Working","mitigating","incident-time","high",timeliness="too-late",basis="direct-artifact"),
  SG("S8","Post-incident: human review mandated + refunds + settlement","organizational-process","preventive","Working","not-causally-relevant","added-after","high",timeliness="in-time",basis="direct-artifact"),
 ],
 relationships=[R("S1","S3","enabling","medium"),R("S1","S2","common-cause","high"),R("S5","S6","masking","medium")],
 factors=[F("Fraud-recovery incentive (penalties up to 400%)","incentive-structure","harm-enabling","aggravating","medium")],
 sources=[S("https://law.justia.com/cases/michigan/supreme-court/2022/160813.html","primary","Bauserman v. UIA (Mich. Sup. Ct. 2022)"),
          S("https://www.michigan.gov/ag/news/press-releases/2022/10/20/som-settlement-of-civil-rights-class-action-alleging-false-accusations-of-unemployment-fraud","primary","Michigan AG settlement")])

add("2024-2025-raine-openai",
 title="Raine v. OpenAI (alleged chatbot contribution to a teen suicide)",
 domain="consumer-chatbot", domain_detail="", date_start="2024-09", date_end="2025-04-11",
 incident_scope="discrete-event", observation_boundary="",
 harm_primary="psychological-social", harm_secondary="", outcome_class="realized-harm",
 system_type="confirmed-ML", era="genai", agentic=0,
 ai_causal_contribution="disputed", attributed_primary_cause="disputed",
 incident_confidence="low",
 safeguards=[
  SG("S1","Self-harm refusal / crisis-resource guardrails","model","preventive","Bypassed","primary","incident-time","low",basis="operator-claim;direct-artifact",evstatus="disputed"),
  SG("S2","Long-conversation safety-degradation control","model","preventive","Failed","primary","incident-time","medium",basis="operator-claim"),
  SG("S3","Age verification / minor protections","application","preventive","Absent","contributing","incident-time","medium",basis="established-practice",evstatus="inferred-indirect"),
  SG("S4","Crisis escalation / human handoff","human-operator","recovery","Absent","contributing","incident-time","medium",basis="comparable-system",evstatus="inferred-indirect"),
  SG("S5","Self-harm detection with intervention","application","detective","Failed","primary","incident-time","low",timeliness="too-late",basis="operator-claim",evstatus="disputed"),
  SG("S6","Post-incident: routing, parental controls, age prediction","application","recovery","Working","not-causally-relevant","added-after","medium",timeliness="in-time",basis="operator-claim",evstatus="multiply-reported"),
 ],
 relationships=[R("S2","S1","enabling","low"),R("S5","S4","enabling","low")],
 factors=[],
 sources=[S("https://www.courthousenews.com/wp-content/uploads/2025/08/raine-vs-openai-et-al-complaint.pdf","primary","Raine v. OpenAI complaint (2025)"),
          S("https://openai.com/index/helping-people-when-they-need-it-most/","primary","OpenAI public statement")])

add("2021-facebook-files-instagram",
 title="Facebook Files: Instagram engagement ranking and teen harm",
 domain="content-moderation", domain_detail="", date_start="2019", date_end="2021-10",
 incident_scope="systemic-program",
 observation_boundary="Instagram's engagement-based recommendation/ranking and documented teen-mental-health harms per Meta's internal 2019-2021 research and the 2021 disclosures; excludes the later Teen Accounts era.",
 harm_primary="psychological-social", harm_secondary="", outcome_class="realized-harm",
 system_type="confirmed-ML", era="legacy", agentic=0,
 ai_causal_contribution="contributory-non-necessary", attributed_primary_cause="organizational",
 incident_confidence="medium",
 safeguards=[
  SG("S1","Internal harm-detection research","organizational-process","detective","Working","not-causally-relevant","incident-time","high",timeliness="in-time",basis="direct-artifact"),
  SG("S2","Product-safety response to internal findings","organizational-process","recovery","Failed","primary","incident-time","medium",basis="direct-artifact;post-incident-finding",evstatus="multiply-reported"),
  SG("S3","Vulnerable-user recommendation guardrails","application","preventive","Inadequate","primary","incident-time","medium",inad="operation",evstatus="multiply-reported"),
  SG("S4","Transparency / honest disclosure (public & Congress)","organizational-process","assurance-governance","Failed","aggravating","incident-time","high",timeliness="too-late",basis="direct-artifact"),
  SG("S5","External oversight (SEC complaints, Senate hearings)","external-ecosystem","detective","Working","mitigating","incident-time","medium",timeliness="too-late",basis="direct-artifact"),
  SG("S6","Post-incident: Instagram Kids paused, Take a Break, Teen Accounts","application","preventive","Working","not-causally-relevant","added-after","medium",timeliness="in-time",basis="direct-artifact",evstatus="multiply-reported"),
 ],
 relationships=[R("S1","S2","temporal-precedence","high"),R("S4","S5","masking","medium"),R("S2","S3","enabling","medium")],
 factors=[F("Engagement-maximizing business incentive","incentive-structure","harm-enabling","primary","medium")],
 sources=[S("https://www.wsj.com/articles/facebook-knows-instagram-is-toxic-for-teen-girls-company-documents-show-11631620739","secondary","WSJ, The Facebook Files"),
          S("https://www.documentcloud.org/documents/21055941-facebook_teen-girls-body-image-and-social-comparison","primary","Leaked internal Meta research deck")])

add("2015-vw-dieselgate",
 title="Volkswagen Dieselgate emissions defeat device",
 domain="environmental", domain_detail="", date_start="2009", date_end="2015-09",
 incident_scope="systemic-program",
 observation_boundary="The 2.0L TDI defeat-device software (MY2009-2015, ~475-500k US vehicles) and its defeat of emissions testing; the 3.0L matter and non-US markets are context.",
 harm_primary="environmental", harm_secondary="", outcome_class="realized-harm",
 system_type="algorithmic-nonML", era="legacy", agentic=0,
 ai_causal_contribution="major-contributor", attributed_primary_cause="organizational",
 incident_confidence="high",
 safeguards=[
  SG("S1","Regulatory emissions certification test","external-ecosystem","detective","Bypassed","primary","incident-time","high",basis="direct-artifact;post-incident-finding"),
  SG("S2","On-road / in-use emissions testing","external-ecosystem","detective","Absent","contributing","incident-time","high",basis="comparable-system;post-incident-finding"),
  SG("S3","Internal governance / engineering-ethics controls","organizational-process","preventive","Failed","primary","incident-time","high",basis="direct-artifact"),
  SG("S4","Certification / type-approval oversight (self-certification)","external-ecosystem","assurance-governance","Inadequate","contributing","incident-time","high",inad="enforcement",basis="direct-artifact"),
  SG("S5","Detection (ICCT / WVU on-road study)","external-ecosystem","detective","Working","mitigating","incident-time","high",timeliness="too-late",basis="direct-artifact"),
  SG("S6","Accountability / recovery (EPA/DOJ/SEC)","external-ecosystem","recovery","Working","mitigating","incident-time","high",timeliness="too-late",basis="direct-artifact"),
  SG("S7","Post-incident: recalls + EU Real-Driving-Emissions testing","external-ecosystem","detective","Working","not-causally-relevant","added-after","high",timeliness="in-time",basis="direct-artifact"),
 ],
 relationships=[R("S3","S1","enabling","high"),R("S2","S5","enabling","high"),R("S4","S1","enabling","medium")],
 factors=[F("Commercial mandate to market 'clean diesel' at scale","incentive-structure","harm-causing","primary","medium")],
 sources=[S("https://www.epa.gov/archive/epa/newsreleases/epa-california-notify-volkswagen-clean-air-act-violations-carmaker-allegedly-used.html","primary","US EPA Notice of Violation"),
          S("https://www.justice.gov/archives/opa/pr/volkswagen-ag-agrees-plead-guilty-and-pay-43-billion-criminal-and-civil-penalties-six","primary","US DOJ guilty plea")])

add("2020-pulse-oximeter-bias",
 title="Racial bias in pulse-oximeter oxygen estimation",
 domain="healthcare-clinical", domain_detail="", date_start="2020", date_end="2020",
 incident_scope="systemic-program",
 observation_boundary="Racial bias in pulse-oximeter SpO2 estimation from unrepresentative calibration (surfaced 2020) and resulting occult hypoxemia / treatment delays; focuses on the calibration and regulatory-testing failure.",
 harm_primary="physical-safety", harm_secondary="rights-discrimination", outcome_class="realized-harm",
 system_type="algorithmic-nonML", era="legacy", agentic=0,
 ai_causal_contribution="major-contributor", attributed_primary_cause="organizational",
 incident_confidence="high",
 safeguards=[
  SG("S1","Representative calibration data (diverse skin tones)","model","preventive","Absent","primary","incident-time","high",basis="post-incident-finding;comparable-system"),
  SG("S2","FDA premarket clearance testing standard (skin-tone diversity)","external-ecosystem","assurance-governance","Inadequate","primary","incident-time","high",inad="enforcement"),
  SG("S3","Clinical-awareness / labeling of the bias","application","detective","Inadequate","contributing","incident-time","high",timeliness="too-late",inad="design",basis="direct-artifact"),
  SG("S4","Post-market surveillance / detection","organizational-process","detective","Failed","latent-condition","incident-time","high",timeliness="too-late"),
  SG("S5","Post-incident: FDA panel/guidance (Monk skin-tone scale)","external-ecosystem","assurance-governance","Working","not-causally-relevant","added-after","medium",timeliness="in-time",basis="direct-artifact"),
 ],
 relationships=[R("S2","S1","enabling","high"),R("S4","S3","temporal-precedence","high")],
 factors=[F("Historical under-representation of dark skin in clinical/calibration research","cultural","harm-enabling","primary","high")],
 sources=[S("https://www.nejm.org/doi/full/10.1056/NEJMc2029240","primary","Sjoding et al., NEJM 2020"),
          S("https://www.fda.gov/news-events/fda-brief/fda-brief-fda-warns-about-limitations-and-accuracy-pulse-oximeters","primary","FDA safety communication (2021)")])

add("2010-flash-crash",
 title="2010 Flash Crash (automated trading cascade)",
 domain="finance-trading", domain_detail="", date_start="2010-05-06", date_end="2010-05-06",
 incident_scope="discrete-event", observation_boundary="",
 harm_primary="financial-loss", harm_secondary="", outcome_class="realized-harm",
 system_type="algorithmic-nonML", era="legacy", agentic=0,
 ai_causal_contribution="major-contributor", attributed_primary_cause="multiple",
 incident_confidence="high",
 safeguards=[
  SG("S1","Execution-algorithm price/time limits","application","preventive","Absent","primary","incident-time","high",basis="direct-artifact"),
  SG("S2","Market-wide circuit breakers","external-ecosystem","containment","Inadequate","contributing","incident-time","high",inad="design",basis="direct-artifact"),
  SG("S3","Single-stock circuit breakers","external-ecosystem","containment","Absent","contributing","incident-time","high",basis="direct-artifact"),
  SG("S4","Guard against nonsensical (stub-quote) executions","infrastructure-environment","containment","Absent","contributing","incident-time","high",basis="direct-artifact"),
  SG("S5","Spoofing / manipulation surveillance","external-ecosystem","detective","Failed","contributing","incident-time","medium",timeliness="too-late",basis="direct-artifact"),
  SG("S6","CME Globex stop-logic pause","infrastructure-environment","containment","Working","mitigating","incident-time","high",timeliness="in-time",basis="direct-artifact"),
  SG("S7","Broken-trade cancellation (clearly-erroneous)","external-ecosystem","recovery","Working","mitigating","incident-time","medium",timeliness="too-late",basis="direct-artifact"),
  SG("S8","Post-incident: single-stock CBs, LULD, stub-quote ban, CAT","external-ecosystem","containment","Working","not-causally-relevant","added-after","high",timeliness="in-time",basis="direct-artifact"),
 ],
 relationships=[R("S1","S4","enabling","medium"),R("S2","S3","common-cause","low"),R("S5","S1","temporal-precedence","low")],
 factors=[F("Pre-existing macro stress (European debt-crisis fears)","economic","harm-amplifying","contributing","high")],
 sources=[S("https://www.sec.gov/news/studies/2010/marketevents-report.pdf","primary","CFTC-SEC joint report (2010)"),
          S("https://www.cftc.gov/PressRoom/PressReleases/7156-15","primary","CFTC charges (Sarao, 2015)")])

add("2021-zillow-offers",
 title="Zillow Offers iBuying algorithmic mispricing collapse",
 domain="finance-trading", domain_detail="", date_start="2021-11-02", date_end="2021-11-02",
 incident_scope="discrete-event", observation_boundary="",
 harm_primary="financial-loss", harm_secondary="", outcome_class="realized-harm",
 system_type="probable-ML", era="legacy", agentic=0,
 ai_causal_contribution="major-contributor", attributed_primary_cause="organizational",
 incident_confidence="high",
 safeguards=[
  SG("S1","Price-forecast model accuracy / validation","model","preventive","Failed","primary","incident-time","high",basis="operator-claim"),
  SG("S2","Human oversight of algorithmic buy decisions","human-operator","detective","Bypassed","primary","incident-time","medium",basis="multiply-reported",evstatus="multiply-reported"),
  SG("S3","Risk limits on purchase volume / price","organizational-process","containment","Inadequate","contributing","incident-time","medium",inad="design",evstatus="multiply-reported"),
  SG("S4","Backtesting / stress-testing for volatile markets","organizational-process","assurance-governance","Inadequate","latent-condition","incident-time","medium",inad="design",evstatus="inferred-indirect"),
  SG("S5","Loss detection","organizational-process","detective","Working","mitigating","incident-time","high",timeliness="too-late",basis="operator-claim"),
  SG("S6","Containment: wind-down + inventory sell-off","organizational-process","recovery","Working","mitigating","incident-time","high",timeliness="too-late",basis="direct-artifact"),
 ],
 relationships=[R("S1","S3","enabling","medium"),R("S2","S1","enabling","medium"),R("S4","S1","enabling","low")],
 factors=[F("Competitive pressure in iBuying","incentive-structure","harm-enabling","contributing","medium")],
 sources=[S("https://www.prnewswire.com/news-releases/zillow-group-reports-third-quarter-2021-financial-results--shares-plan-to-wind-down-zillow-offers-operations-301414460.html","primary","Zillow Q3 2021 release / wind-down")])

add("2018-ibm-watson-oncology",
 title="IBM Watson for Oncology unsafe treatment recommendations",
 domain="healthcare-clinical", domain_detail="", date_start="2018-07", date_end="2018-07",
 incident_scope="systemic-program",
 observation_boundary="The MSK-trained commercial Watson for Oncology product, its synthetic-case training and unsafe recommendations per internal 2017 documents; excludes the separate MD Anderson project.",
 harm_primary="information-integrity", harm_secondary="physical-safety", outcome_class="realized-harm",
 system_type="confirmed-ML", era="legacy", agentic=0,
 ai_causal_contribution="major-contributor", attributed_primary_cause="organizational",
 incident_confidence="medium",
 safeguards=[
  SG("S1","Training-data validity (real-world evidence grounding)","model","preventive","Absent","primary","incident-time","high",basis="direct-artifact",evstatus="multiply-reported"),
  SG("S2","Clinical / outcome validation before deployment","organizational-process","assurance-governance","Inadequate","primary","incident-time","high",inad="design",basis="direct-artifact",evstatus="multiply-reported"),
  SG("S3","Marketing / deployment honesty (claims match reality)","organizational-process","assurance-governance","Failed","aggravating","incident-time","high",basis="direct-artifact",evstatus="multiply-reported"),
  SG("S4","Physician oversight / override (human in the loop)","human-operator","containment","Working","mitigating","incident-time","medium",timeliness="in-time",basis="operator-claim",evstatus="multiply-reported"),
  SG("S5","Detection (internal decks + client complaints)","organizational-process","detective","Working","mitigating","incident-time","high",timeliness="too-late",basis="direct-artifact"),
  SG("S6","Incident-time remediation (patching, continued sale)","organizational-process","recovery","Inadequate","not-causally-relevant","incident-time","medium",timeliness="too-late",inad="operation",basis="direct-artifact",evstatus="multiply-reported"),
  SG("S7","Later: wind-down + divestiture","organizational-process","recovery","Working","not-causally-relevant","added-after","high",timeliness="in-time",basis="direct-artifact"),
 ],
 relationships=[R("S1","S2","enabling","high"),R("S3","S4","masking","medium"),R("S5","S6","temporal-precedence","high")],
 factors=[],
 sources=[S("https://www.statnews.com/2018/07/25/ibm-watson-recommended-unsafe-incorrect-treatments/","secondary","STAT News investigation (2018)")])

add("2023-2025-mobley-workday",
 title="Mobley v. Workday (alleged AI hiring discrimination)",
 domain="hiring-HR", domain_detail="", date_start="2023", date_end="2025",
 incident_scope="systemic-program",
 observation_boundary="Allegations and rulings in Mobley v. Workday regarding AI applicant-screening and discrimination; excludes adjudicated liability (none yet).",
 harm_primary="rights-discrimination", harm_secondary="", outcome_class="realized-harm",
 system_type="probable-ML", era="genai", agentic=0,
 ai_causal_contribution="disputed", attributed_primary_cause="disputed",
 incident_confidence="low",
 safeguards=[
  SG("S1","Bias audit / disparate-impact testing","organizational-process","assurance-governance","Absent","primary","incident-time","low",evstatus="disputed"),
  SG("S2","Transparency to applicants (explainability)","application","assurance-governance","Absent","contributing","incident-time","low",evstatus="disputed"),
  SG("S3","Human oversight of automated screening","human-operator","detective","Bypassed","primary","incident-time","low",evstatus="disputed"),
  SG("S4","Vendor accountability ('agent' liability)","external-ecosystem","assurance-governance","Working","mitigating","incident-time","medium",timeliness="too-late",basis="direct-artifact"),
  SG("S5","Regulatory oversight (EEOC amicus; ADEA certification)","external-ecosystem","detective","Working","mitigating","incident-time","medium",timeliness="too-late",basis="direct-artifact"),
  SG("S6","External bias-audit regime (NYC Local Law 144)","external-ecosystem","assurance-governance","Inadequate","not-causally-relevant","added-after","medium",timeliness="in-time",inad="enforcement",basis="research-evidence",evstatus="multiply-reported"),
 ],
 relationships=[R("S1","S3","enabling","low"),R("S3","S2","common-cause","low")],
 factors=[],
 sources=[S("https://www.eeoc.gov/litigation/briefs/mobley-v-workday-inc","primary","EEOC amicus brief"),
          S("https://www.hklaw.com/en/insights/publications/2025/05/federal-court-allows-collective-action-lawsuit-over-alleged","secondary","Holland & Knight, ADEA certification analysis")])

add("2024-gemini-image-generation",
 title="Google Gemini historically inaccurate image generation (over-correction)",
 domain="content-moderation", domain_detail="", date_start="2024-02", date_end="2024-02",
 incident_scope="discrete-event", observation_boundary="",
 harm_primary="information-integrity", harm_secondary="", outcome_class="realized-harm",
 system_type="confirmed-ML", era="genai", agentic=0,
 ai_causal_contribution="major-contributor", attributed_primary_cause="organizational",
 incident_confidence="high",
 safeguards=[
  SG("S1","Demographic-bias fairness tuning","model","preventive","Failed","primary","incident-time","high",basis="operator-claim"),
  SG("S2","Context / historical-accuracy gate","application","preventive","Absent","primary","incident-time","high",basis="operator-claim"),
  SG("S3","Over-refusal safety layer (prompt sensitivity)","model","preventive","Failed","contributing","incident-time","high",basis="operator-claim"),
  SG("S4","Pre-launch testing / red-teaming","organizational-process","assurance-governance","Inadequate","latent-condition","incident-time","medium",inad="design",basis="operator-claim",evstatus="inferred-indirect"),
  SG("S5","Internal detection (pre-public)","organizational-process","detective","Failed","contributing","incident-time","high",timeliness="too-late",basis="direct-artifact"),
  SG("S6","Feature pause / kill-switch","application","containment","Working","mitigating","incident-time","high",timeliness="in-time",basis="direct-artifact"),
  SG("S7","Later: re-release on Imagen 3 with new evals/red-teaming","model","preventive","Working","not-causally-relevant","added-after","high",timeliness="in-time",basis="direct-artifact"),
 ],
 relationships=[R("S1","S2","enabling","high"),R("S1","S3","common-cause","low"),R("S5","S6","enabling","high")],
 factors=[],
 sources=[S("https://blog.google/products/gemini/gemini-image-generation-issue/","primary","Google, Gemini image generation got it wrong")])

add("2018-tesla-autopilot-mountain-view",
 title="Tesla Autopilot fatal crash (Mountain View; Walter Huang)",
 domain="autonomous-vehicle", domain_detail="", date_start="2018-03-23", date_end="2018-03-23",
 incident_scope="discrete-event", observation_boundary="",
 harm_primary="physical-safety", harm_secondary="", outcome_class="realized-harm",
 system_type="confirmed-ML", era="legacy", agentic=0,
 ai_causal_contribution="major-contributor", attributed_primary_cause="multiple",
 incident_confidence="high",
 safeguards=[
  SG("S1","Perception / obstacle (barrier) detection + AEB","application","preventive","Inadequate","primary","incident-time","high",inad="design"),
  SG("S2","Driver-attention monitoring","application","detective","Inadequate","primary","incident-time","high",inad="design"),
  SG("S3","Operational-design-domain restriction","application","preventive","Absent","contributing","incident-time","high",basis="comparable-system;post-incident-finding"),
  SG("S4","Driver attention / intervention (human)","human-operator","recovery","Failed","primary","incident-time","medium",timeliness="too-late"),
  SG("S5","Highway crash attenuator (infrastructure)","external-ecosystem","containment","Failed","contributing","incident-time","high",timeliness="too-late"),
  SG("S6","Federal (NHTSA) oversight of partial automation","external-ecosystem","assurance-governance","Inadequate","latent-condition","incident-time","high",inad="enforcement"),
  SG("S7","Post-incident: NTSB recommendations + attenuator repair","external-ecosystem","assurance-governance","Working","not-causally-relevant","added-after","high",timeliness="in-time",basis="direct-artifact"),
 ],
 relationships=[R("S2","S4","enabling","high"),R("S3","S1","enabling","medium")],
 factors=[F("Employer (Apple) lack of a distracted-driving policy","organizational","harm-enabling","contributing","medium")],
 sources=[S("https://www.ntsb.gov/investigations/pages/hwy18fh011.aspx","primary","NTSB HWY18FH011")])

add("2023-tesla-autopilot-recall",
 title="NHTSA ~2M-vehicle Tesla Autopilot recall (inadequate driver engagement)",
 domain="autonomous-vehicle", domain_detail="", date_start="2023-12-12", date_end="2023-12-12",
 incident_scope="systemic-program",
 observation_boundary="NHTSA's finding (EA22-002) that Autopilot driver-engagement controls were insufficient across ~2M vehicles and the Dec 2023 recall, based on the crash set incl. stationary-emergency-vehicle collisions; excludes individual crash specifics.",
 harm_primary="physical-safety", harm_secondary="", outcome_class="realized-harm",
 system_type="confirmed-ML", era="legacy", agentic=0,
 ai_causal_contribution="major-contributor", attributed_primary_cause="organizational",
 incident_confidence="high",
 safeguards=[
  SG("S1","Driver-engagement monitoring controls","application","detective","Inadequate","primary","incident-time","high",inad="design"),
  SG("S2","Operational-design-domain / misuse limiting","application","preventive","Inadequate","primary","incident-time","high",inad="design"),
  SG("S3","Regulatory oversight (NHTSA EA22-002 investigation)","external-ecosystem","detective","Working","mitigating","incident-time","high",timeliness="too-late",basis="direct-artifact"),
  SG("S4","Recall remedy (OTA update)","application","detective","Inadequate","not-causally-relevant","added-after","medium",timeliness="delayed",inad="operation",basis="direct-artifact",evstatus="multiply-reported"),
 ],
 relationships=[R("S1","S3","temporal-precedence","high"),R("S1","S2","common-cause","medium")],
 factors=[F("'Autopilot'/'Full Self-Driving' naming encouraging over-reliance","other","harm-enabling","contributing","medium")],
 sources=[S("https://static.nhtsa.gov/odi/rcl/2023/RCLRPT-23V838-8276.PDF","primary","NHTSA recall 23V-838")])

add("2017-2021-rotterdam-welfare",
 title="Rotterdam welfare-fraud risk-scoring algorithm",
 domain="government-benefits", domain_detail="", date_start="2017", date_end="2021",
 incident_scope="systemic-program",
 observation_boundary="Rotterdam's gradient-boosting welfare-fraud risk-scoring model (~2017-2021; ~30,000 recipients scored, top ~1,000/yr investigated) and its discriminatory scoring; excludes other municipalities.",
 harm_primary="rights-discrimination", harm_secondary="psychological-social", outcome_class="realized-harm",
 system_type="confirmed-ML", era="legacy", agentic=0,
 ai_causal_contribution="major-contributor", attributed_primary_cause="organizational",
 incident_confidence="high",
 safeguards=[
  SG("S1","Pre-deployment bias / fairness audit","organizational-process","assurance-governance","Absent","primary","incident-time","high"),
  SG("S2","Feature / data governance (proxy & subjective features)","model","preventive","Inadequate","primary","incident-time","high",inad="design"),
  SG("S3","Meaningful individual human review of flagged cases","human-operator","detective","Inadequate","contributing","incident-time","medium",inad="operation",evstatus="disputed"),
  SG("S4","Transparency to affected people","application","assurance-governance","Absent","latent-condition","incident-time","high"),
  SG("S5","Governance / Court-of-Audit oversight (incl. DPIA)","organizational-process","assurance-governance","Inadequate","latent-condition","incident-time","high",inad="design",basis="direct-artifact"),
  SG("S6","Internal detection during operation","organizational-process","detective","Failed","contributing","incident-time","high"),
  SG("S7","External oversight & recovery (Rekenkamer; audit; suspension)","external-ecosystem","recovery","Working","mitigating","incident-time","high",timeliness="too-late",basis="direct-artifact"),
 ],
 relationships=[R("S1","S2","enabling","medium"),R("S4","S3","enabling","medium"),R("S6","S7","temporal-precedence","high")],
 factors=[F("Fraud-detection efficiency / cost pressure","incentive-structure","harm-enabling","contributing","medium")],
 sources=[S("https://www.lighthousereports.com/investigation/suspicion-machines/","secondary","Lighthouse/WIRED, Suspicion Machines"),
          S("https://www.rekenkamers.nl/rapport/gekleurde-technologie/","primary","Rekenkamer Rotterdam, Gekleurde technologie")])

add("2014-erater-babel-aes",
 title="Automated essay scoring validity failure (ETS e-rater / BABEL)",
 domain="education", domain_detail="", date_start="2014", date_end="2018",
 incident_scope="systemic-program",
 observation_boundary="The construct-validity and adversarial-robustness failure of ETS e-rater automated essay scoring as demonstrated by the BABEL generator (2014) and ETS's response; focuses on e-rater, with other AES engines as context.",
 harm_primary="information-integrity", harm_secondary="", outcome_class="realized-harm",
 system_type="confirmed-ML", era="legacy", agentic=0,
 ai_causal_contribution="major-contributor", attributed_primary_cause="organizational",
 incident_confidence="high",
 safeguards=[
  SG("S1","Construct validity (measures writing quality, not surface proxies)","model","preventive","Failed","primary","incident-time","high",basis="research-evidence;direct-artifact"),
  SG("S2","Adversarial / gaming robustness","model","preventive","Absent","primary","incident-time","high",basis="research-evidence"),
  SG("S3","Human-in-the-loop pairing (high-stakes, e.g. GRE)","human-operator","containment","Working","mitigating","incident-time","high",timeliness="in-time",basis="direct-artifact",cg="HUMAN-OVERSIGHT"),
  SG("S4","Human oversight where e-rater scores alone","human-operator","containment","Absent","primary","incident-time","high",basis="direct-artifact",cg="HUMAN-OVERSIGHT"),
  SG("S5","Vendor response: BABEL-advisory detector","application","detective","Inadequate","not-causally-relevant","added-after","high",timeliness="too-late",inad="design",basis="direct-artifact"),
 ],
 relationships=[R("S1","S2","common-cause","high"),R("S2","S5","temporal-precedence","high")],
 factors=[F("Cost/scale incentive to automate high-volume essay scoring","incentive-structure","harm-enabling","primary","medium")],
 sources=[S("https://lesperelman.com/wp-content/uploads/2021/01/Perelman-BABEL-Generator-e-rater.pdf","primary","Perelman, The BABEL Generator and e-rater (JWA)"),
          S("https://wacclearinghouse.org/docs/jwa/vol2/cahill.pdf","primary","Cahill et al. (ETS), BABEL advisory")])

add("2025-amazon-q-injection",
 title="Amazon Q Developer extension supply-chain injection (near-miss)",
 domain="security-cyber", domain_detail="", date_start="2025-07", date_end="2025-07",
 incident_scope="discrete-event", observation_boundary="",
 harm_primary="security-compromise", harm_secondary="", outcome_class="near-miss",
 system_type="confirmed-ML", era="genai", agentic=1,
 ai_causal_contribution="major-contributor", attributed_primary_cause="organizational",
 incident_confidence="medium",
 safeguards=[
  SG("S1","PR review / repo write-access control","organizational-process","preventive","Bypassed","primary","incident-time","high",basis="operator-claim;direct-artifact",evstatus="multiply-reported"),
  SG("S2","Supply-chain / release-integrity vetting","organizational-process","preventive","Failed","primary","incident-time","high",basis="operator-claim",evstatus="multiply-reported"),
  SG("S3","Agent execution guardrails (destructive-command confirmation/sandbox)","application","containment","Unknown","contributing","incident-time","low",suspected=1,basis="inferred-indirect",evstatus="inferred-indirect"),
  SG("S4","Proactive detection (pre-release / at-merge)","organizational-process","detective","Failed","contributing","incident-time","medium",timeliness="too-late",basis="direct-artifact",evstatus="multiply-reported"),
  SG("S5","Containment of destructive payload","infrastructure-environment","containment","Absent","latent-condition","incident-time","high",basis="operator-claim",evstatus="multiply-reported"),
  SG("S6","Response / remediation (revoke token, remove code, pull 1.84, ship 1.85)","organizational-process","recovery","Working","mitigating","incident-time","high",timeliness="delayed",basis="operator-claim",evstatus="multiply-reported"),
 ],
 relationships=[R("S1","S2","enabling","high"),R("S4","S6","temporal-precedence","high")],
 factors=[],
 sources=[S("https://aws.amazon.com/security/security-bulletins/AWS-2025-015/","primary","AWS Security Bulletin AWS-2025-015"),
          S("https://www.404media.co/hacker-plants-computer-wiping-commands-in-amazons-ai-coding-agent/","secondary","404 Media investigation")])

# ============================ EMIT ============================
os.makedirs("data", exist_ok=True)
inc_rows, sg_rows, rel_rows, fac_rows, src_rows = [], [], [], [], []
sg_index = 1; rel_index=1; fac_index=1; src_index=1
for cid, d in INC.items():
    inc_rows.append(dict(incident_id=cid, title=d["title"], domain=d["domain"],
        domain_detail=d.get("domain_detail",""), date_start=d["date_start"], date_end=d["date_end"],
        incident_scope=d["incident_scope"], observation_boundary=d.get("observation_boundary",""),
        harm_primary=d["harm_primary"], harm_secondary=d.get("harm_secondary",""),
        outcome_class=d["outcome_class"], system_type=d["system_type"], era=d["era"], agentic=d["agentic"],
        ai_causal_contribution=d["ai_causal_contribution"], attributed_primary_cause=d["attributed_primary_cause"],
        incident_confidence=d["incident_confidence"], n_safeguards=len(d["safeguards"]),
        dataset_version=DATASET_VERSION))
    for sg in d["safeguards"]:
        iid = f"{cid}::{sg['sid']}"
        row = dict(interaction_id=iid, incident_id=cid, local_sid=sg["sid"], **{k:v for k,v in sg.items() if k!="sid"})
        sg_rows.append(row); sg_index+=1
    for r in d["relationships"]:
        rel_rows.append(dict(relationship_id=f"{cid}::R{rel_index}", incident_id=cid,
            from_interaction=f"{cid}::{r['from_sid']}", to_interaction=f"{cid}::{r['to_sid']}",
            relationship_type=r["relationship_type"], relationship_confidence=r["relationship_confidence"]))
        rel_index+=1
    for f in d["factors"]:
        fac_rows.append(dict(factor_id=f"{cid}::F{fac_index}", incident_id=cid, **f)); fac_index+=1
    for s in d["sources"]:
        src_rows.append(dict(source_id=f"{cid}::SRC{src_index}", incident_id=cid, **s)); src_index+=1

def write_csv(path, rows):
    if not rows: return
    keys = list(rows[0].keys())
    with open(path,"w",newline="") as f:
        w=csv.DictWriter(f, fieldnames=keys); w.writeheader()
        for r in rows: w.writerow(r)

write_csv("data/incidents.csv", inc_rows)
write_csv("data/safeguards.csv", sg_rows)
write_csv("data/relationships.csv", rel_rows)
write_csv("data/contributing_factors.csv", fac_rows)
write_csv("data/sources.csv", src_rows)
with open("data/observatory_dataset.json","w") as f:
    json.dump({"version":DATASET_VERSION,"frozen":FROZEN,"incidents":inc_rows,"safeguards":sg_rows,
               "relationships":rel_rows,"contributing_factors":fac_rows,"sources":src_rows}, f, indent=1)

print(f"incidents={len(inc_rows)} safeguards={len(sg_rows)} relationships={len(rel_rows)} "
      f"factors={len(fac_rows)} sources={len(src_rows)}")
