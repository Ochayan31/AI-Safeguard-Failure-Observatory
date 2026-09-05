#!/usr/bin/env python3
"""
AI Safeguard Failure Observatory - Phase 1B stratified selection.
Implements the FROZEN selection protocol (incident_selection_protocol.md, Section 11):
  N=30; Hybrid E->R (evidence-quality rank, seeded random tie-break at boundaries);
  omission floor >=8; per-domain cap <=5; system_type floor >=4 each & cap <=18;
  top-documentation-tier cap <=21 (<=70% of 30).
Rubric (6.1): source_authority + corroboration + completeness + verifiability, each 0-3.
  We encode each candidate's src tier and a documentation level (high/med/low), then derive
  the four axes deterministically (mapping documented below). This is CIR-BLIND:
  no axis references CIR structure, safeguard count, or expected findings.
"""
import random

SEED = "AISFO-2026-08-24"

# --- AMENDMENT 2026-08-24 (logged): mechanism/recency floor ---
# Reason: v1 mechanical draw covered zero agentic/recent-generative cases because the
# evidence-quality rubric structurally favors older, institutionally-documented harms.
# Fix (structural, not hand-picked): >=5 of the 30 from the 2022+ generative/agentic era,
# of which >=2 agentic tool-use. Applied BEFORE the omission and system_type floors.
GENAI_IDS = {"C055","C060","C063","C064","C066","C067","C068","C069","C070","C071",
             "C072","C073","C074","C075","C076","C077","C078","C081","C084","C085",
             "C086","C087","C089","C096","C097","C102","C103","C104","C105","C106",
             "C107","C108"}
AGENTIC_IDS = {"C066","C071","C072","C102","C103","C104","C105","C107","C108"}
GENAI_FLOOR = 5
AGENTIC_FLOOR = 2

# axis mappings from (src, doc)
AUTH = {"P": 3, "F": 2, "J": 1, "partial": 1}
VERIF = {"P": 3, "F": 2, "J": 2, "partial": 1}
DOCV = {"high": 3, "med": 2, "low": 1}  # used for BOTH corroboration and completeness

def rubric(src, doc):
    return AUTH[src] + VERIF[src] + 2 * DOCV[doc]  # 0..12

# Each candidate: (id, domain, stype, mode, eligible, reason_if_excluded, src, doc)
# mode: 'O' omission-dominated, 'A' active-failure, 'U' unclear (not counted for omission floor)
# stype: cML confirmed-ML, pML probable-ML, anML algorithmic-nonML, unk unknown
C = [
 ("C001","autonomous-vehicle","cML","A",1,"","P","high"),
 ("C002","autonomous-vehicle","cML","A",1,"","P","high"),
 ("C003","autonomous-vehicle","cML","A",1,"","P","high"),
 ("C004","autonomous-vehicle","cML","A",1,"","P","high"),
 ("C005","autonomous-vehicle","cML","A",1,"","P","med"),
 ("C006","autonomous-vehicle","cML","A",1,"","P","med"),
 ("C007","autonomous-vehicle","cML","O",1,"","P","high"),
 ("C008","autonomous-vehicle","cML","A",1,"","P","med"),
 ("C009","autonomous-vehicle","cML","A",1,"","P","med"),
 ("C010","aviation-other","anML","A",1,"","P","high"),
 ("C011","aviation-other","anML","A",0,"control-software config fault; no algorithmic decision/inference (E1 scope)","partial","low"),
 ("C012","robotics-industrial","anML","A",0,"deterministic industrial robot; no algorithmic decision component (E1 scope)","J","med"),
 ("C013","robotics-industrial","anML","A",1,"","J","low"),
 ("C014","robotics-industrial","anML","A",0,"deterministic industrial robot; no algorithmic decision component (E1 scope)","partial","low"),
 ("C015","robotics-industrial","anML","A",0,"deterministic industrial robot; no algorithmic decision component (E1 scope)","J","low"),
 ("C016","robotics-industrial","unk","O",1,"","J","low"),
 ("C017","finance-trading","anML","A",1,"","P","high"),
 ("C018","finance-trading","anML","A",1,"","P","high"),
 ("C019","finance-trading","pML","A",1,"","J","med"),
 ("C020","finance-consumer","pML","O",1,"","P","med"),
 ("C021","finance-consumer","pML","O",1,"","P","med"),
 ("C022","healthcare-clinical","pML","O",1,"","P","high"),
 ("C023","healthcare-clinical","cML","O",1,"","P","high"),
 ("C024","healthcare-clinical","cML","O",1,"","J","med"),
 ("C025","healthcare-clinical","anML","A",0,"control-software race condition; no algorithmic decision/inference (E1 scope)","P","high"),
 ("C026","healthcare-clinical","anML","U",0,"teleoperated device; no algorithmic decision system in causal path (E1)","J","med"),
 ("C027","healthcare-clinical","anML","O",1,"","P","high"),
 ("C028","healthcare-clinical","pML","A",1,"","J","med"),
 ("C029","healthcare-clinical","cML","O",1,"","J","med"),
 ("C030","scientific-research","cML","O",0,"systematic-review finding, not a bounded incident; no realized/attempted harm to identifiable parties","P","high"),
 ("C031","criminal-justice","pML","O",1,"","J","high"),
 ("C032","criminal-justice","cML","O",1,"","P","high"),
 ("C033","criminal-justice","cML","O",1,"","P","med"),
 ("C034","criminal-justice","cML","O",1,"","P","med"),
 ("C035","criminal-justice","pML","O",1,"","J","med"),
 ("C036","criminal-justice","anML","O",1,"","J","med"),
 ("C037","criminal-justice","pML","O",1,"","P","med"),
 ("C038","criminal-justice","anML","O",1,"","J","med"),
 ("C039","government-benefits","pML","O",1,"","P","high"),
 ("C040","government-benefits","anML","O",1,"","P","high"),
 ("C041","government-benefits","anML","O",1,"","P","high"),
 ("C042","government-benefits","anML","O",1,"","P","high"),
 ("C043","government-benefits","anML","O",1,"","P","med"),
 ("C044","government-benefits","anML","O",1,"","P","med"),
 ("C045","government-benefits","anML","O",1,"","P","med"),
 ("C046","government-benefits","pML","O",1,"","J","med"),
 ("C047","government-benefits","cML","O",1,"","J","high"),
 ("C048","government-benefits","pML","O",1,"","J","med"),
 ("C049","government-benefits","pML","O",1,"","J","med"),
 ("C050","government-benefits","pML","O",1,"","P","med"),
 ("C051","government-benefits","anML","O",1,"","P","med"),
 ("C052","government-benefits","anML","O",1,"","J","med"),
 ("C053","education","anML","O",1,"","P","med"),
 ("C054","government-benefits","anML","O",1,"","P","med"),
 ("C055","government-benefits","cML","O",1,"","J","med"),
 ("C056","education","anML","O",1,"","P","high"),
 ("C057","hiring-HR","cML","O",1,"","J","med"),
 ("C058","hiring-HR","anML","A",1,"","P","med"),
 ("C059","hiring-HR","pML","A",1,"","P","med"),
 ("C060","consumer-chatbot","pML","O",1,"","P","high"),
 ("C061","consumer-chatbot","cML","O",1,"","F","med"),
 ("C062","consumer-chatbot","pML","O",1,"","J","med"),
 ("C063","consumer-chatbot","cML","O",1,"","P","med"),
 ("C064","consumer-chatbot","cML","O",1,"","J","med"),
 ("C065","consumer-chatbot","cML","O",1,"","P","med"),
 ("C066","enterprise-agent","cML","A",1,"","J","low"),
 ("C067","consumer-chatbot","cML","O",1,"","J","med"),
 ("C068","consumer-chatbot","cML","O",1,"","J","med"),
 ("C069","consumer-chatbot","cML","A",1,"","J","med"),
 ("C070","consumer-chatbot","cML","O",1,"","P","med"),
 ("C071","enterprise-agent","cML","O",1,"","J","low"),
 ("C072","enterprise-agent","cML","A",1,"","J","med"),
 ("C073","llm-other","cML","O",1,"","P","high"),
 ("C074","llm-other","cML","A",1,"","P","med"),
 ("C075","llm-other","cML","A",1,"","J","med"),
 ("C076","llm-other","cML","A",1,"","J","low"),
 ("C077","llm-other","cML","A",1,"","J","med"),
 ("C078","llm-other","cML","A",1,"","J","med"),
 ("C079","llm-other","pML","A",1,"","J","low"),
 ("C080","content-moderation","cML","O",1,"","J","med"),
 ("C081","content-moderation","cML","A",1,"","F","med"),
 ("C082","content-moderation","cML","O",1,"","P","high"),
 ("C083","content-moderation","cML","O",1,"","J","high"),
 ("C084","content-moderation","cML","A",1,"","J","med"),
 ("C085","content-moderation","cML","A",1,"","J","med"),
 ("C086","security-cyber","cML","A",1,"","J","med"),
 ("C087","security-cyber","cML","O",1,"","J","med"),
 ("C088","security-cyber","cML","O",1,"","P","high"),
 ("C089","education","cML","A",1,"","J","med"),
 ("C090","education","cML","A",1,"","J","med"),
 ("C091","education","cML","A",1,"","J","med"),
 ("C092","education","anML","O",1,"","J","low"),
 ("C093","education","anML","O",1,"","J","med"),
 ("C094","education","cML","A",1,"","P","low"),
 ("C095","scientific-research","cML","O",0,"demonstrative dual-use study; no real-world instantiation (exclusion: demonstrative)","P","med"),
 ("C096","scientific-research","cML","O",1,"","J","med"),
 ("C097","scientific-research","cML","O",1,"","J","low"),
 ("C098","scientific-research","cML","A",1,"","P","med"),
 ("C099","environmental","anML","A",1,"","P","high"),
 ("C100","environmental","anML","O",1,"","P","med"),
 ("C101","environmental","unk","A",0,"on close research: conventional grid-engineering/voltage-control failure; only classical protective-relay automation (static thresholds) in the causal chain; no AI/ML or algorithmic DECISION system (E1 fail). Spanish Senate: not an automated-system breakdown.","P","low"),
 ("C102","enterprise-agent","cML","A",1,"","P","med"),
 ("C103","enterprise-agent","cML","A",1,"","J","low"),
 ("C104","security-cyber","cML","A",1,"","J","med"),
 ("C105","security-cyber","cML","A",1,"","P","med"),
 ("C106","consumer-chatbot","cML","A",1,"","J","med"),
 ("C107","enterprise-agent","cML","A",1,"","J","low"),
 ("C108","enterprise-agent","cML","A",1,"","J","low"),
]

cands = []
for cid, dom, st, mode, elig, reason, src, doc in C:
    cands.append({"id": cid, "domain": dom, "stype": st, "mode": mode,
                  "eligible": bool(elig), "reason": reason, "src": src, "doc": doc,
                  "score": rubric(src, doc)})

eligible = [c for c in cands if c["eligible"]]
excluded_screen = [c for c in cands if not c["eligible"]]

# seeded tie-break: deterministic random key per candidate id
rng = random.Random(SEED)
tiekey = {}
for cid in sorted(c["id"] for c in eligible):
    tiekey[cid] = rng.random()
for c in eligible:
    c["tie"] = tiekey[c["id"]]
    c["genai"] = c["id"] in GENAI_IDS
    c["agentic"] = c["id"] in AGENTIC_IDS

# rank: higher score first; ties broken by seeded random
ranked = sorted(eligible, key=lambda c: (-c["score"], c["tie"]))

N = 30
DOMAIN_CAP = 5
STYPE_CAP = 18
STYPE_FLOOR = {"cML": 4, "pML": 4, "anML": 4}
OMISSION_FLOOR = 8
TOPTIER_CAP = 21          # score>=10
TOPTIER_MIN_SCORE = 10

selected = []
dom_count = {}
st_count = {}
toptier = 0
omission = 0
genai = 0
agentic = 0

def can_add(c):
    if len(selected) >= N: return False
    if dom_count.get(c["domain"], 0) >= DOMAIN_CAP: return False
    if st_count.get(c["stype"], 0) >= STYPE_CAP: return False
    if c["score"] >= TOPTIER_MIN_SCORE and toptier >= TOPTIER_CAP: return False
    return True

def add(c):
    global toptier, omission, genai, agentic
    selected.append(c)
    dom_count[c["domain"]] = dom_count.get(c["domain"], 0) + 1
    st_count[c["stype"]] = st_count.get(c["stype"], 0) + 1
    if c["score"] >= TOPTIER_MIN_SCORE: toptier += 1
    if c["mode"] == "O": omission += 1
    if c["genai"]: genai += 1
    if c["agentic"]: agentic += 1

sel_ids = set()
# Phase A - agentic tool-use floor (amendment)
for c in ranked:
    if agentic >= AGENTIC_FLOOR: break
    if c["agentic"] and c["id"] not in sel_ids and can_add(c):
        add(c); sel_ids.add(c["id"])
# Phase B - genai/recency floor (amendment); agentic already added count toward this
for c in ranked:
    if genai >= GENAI_FLOOR: break
    if c["genai"] and c["id"] not in sel_ids and can_add(c):
        add(c); sel_ids.add(c["id"])
# Phase 1 - omission floor
for c in ranked:
    if omission >= OMISSION_FLOOR: break
    if c["mode"] == "O" and c["id"] not in sel_ids and can_add(c):
        add(c); sel_ids.add(c["id"])
# Phase 2 - system_type floors
for st, floor in STYPE_FLOOR.items():
    for c in ranked:
        if st_count.get(st, 0) >= floor: break
        if c["stype"] == st and c["id"] not in sel_ids and can_add(c):
            add(c); sel_ids.add(c["id"])
# Phase 3 - fill to N by rank
for c in ranked:
    if len(selected) >= N: break
    if c["id"] in sel_ids: continue
    if can_add(c):
        add(c); sel_ids.add(c["id"])

excluded_eligible = [c for c in ranked if c["id"] not in sel_ids]

# ---- report ----
print("SEED:", SEED)
print("Pool:", len(cands), "| Eligible:", len(eligible), "| Excluded at screen:", len(excluded_screen))
print("Selected:", len(selected))
print()
print("=== CONSTRAINT CHECK ===")
print("genai/recency-era selected:", genai, "(floor 5) ->", "OK" if genai >= GENAI_FLOOR else "FAIL")
print("agentic tool-use selected:", agentic, "(floor 2) ->", "OK" if agentic >= AGENTIC_FLOOR else "FAIL")
print("omission-dominated selected:", omission, "(floor 8) ->", "OK" if omission >= 8 else "FAIL")
for st in ("cML","pML","anML"):
    print(f"  system_type {st}:", st_count.get(st,0), "(floor 4, cap 18) ->",
          "OK" if 4 <= st_count.get(st,0) <= 18 else "CHECK")
print("  system_type unk:", st_count.get("unk",0))
over = [d for d,n in dom_count.items() if n>DOMAIN_CAP]
print("domain cap <=5 ->", "OK" if not over else f"VIOLATION {over}")
print("top-tier (score>=10) selected:", toptier, "(cap 21) ->", "OK" if toptier<=21 else "FAIL")
print()
print("=== DOMAIN SPREAD (selected) ===")
for d in sorted(dom_count, key=lambda k:-dom_count[k]):
    print(f"  {d}: {dom_count[d]}")
print()
print("=== SELECTED 30 ===")
for c in sorted(selected, key=lambda c: c["id"]):
    tag = "AGENTIC" if c["agentic"] else ("genai" if c["genai"] else "")
    print(f'  {c["id"]}  score={c["score"]:>2}  {c["mode"]}  {c["stype"]:>4}  {c["domain"]:<20} {tag}')
print()
print("=== EXCLUDED AT SCREEN (with reason) ===")
for c in sorted(excluded_screen, key=lambda c: c["id"]):
    print(f'  {c["id"]}: {c["reason"]}')
print()
print("=== EXCLUDED-BUT-ELIGIBLE (stratum-full / not-drawn) ===")
print("  count:", len(excluded_eligible))
for c in sorted(excluded_eligible, key=lambda c: c["id"]):
    print(f'  {c["id"]}  score={c["score"]:>2}  {c["mode"]}  {c["stype"]:>4}  {c["domain"]}')
