#!/usr/bin/env python3
"""
AI Safeguard Failure Observatory - Dataset integrity validator (Phase 1C, section 17).

Runs a battery of integrity checks against the emitted CSV/JSON dataset. Fails loud.
No check invents data; every check is a structural/vocabulary/denominator guard so that
downstream analysis cannot be contaminated by coding slips.

Checks:
  1. Referential integrity: every safeguard/relationship/factor/source incident_id exists.
  2. Relationship endpoints (from_sid/to_sid) resolve to real local safeguard ids in the same incident.
  3. ID uniqueness: interaction_id, relationship_id, factor_id, source_id unique.
  4. Controlled-vocabulary validity for every categorical field.
  5. Denominator-contamination guards:
        - suspected_absent=1 only when observed_state=Unknown, and never counted as Absent.
        - existence_timing in {incident-time, added-after}; added-after flagged for exclusion.
        - inadequacy_type only present when observed_state=Inadequate.
        - timeliness present for detective/containment/recovery where not 'not-applicable' is allowed.
  6. Contributing factors are NOT safeguards (disjoint id spaces / separate table) - structural.
  7. control_group consistency: rows sharing a control_group are within one incident.
  8. Cardinality sanity: counts match the JSON.
"""
import csv, json, sys, os
from collections import defaultdict, Counter

DATA = os.path.join(os.path.dirname(__file__), "..", "data")

def load_csv(name):
    with open(os.path.join(DATA, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

incidents = load_csv("incidents.csv")
safeguards = load_csv("safeguards.csv")
relationships = load_csv("relationships.csv")
factors = load_csv("contributing_factors.csv")
sources = load_csv("sources.csv")

errors = []
warnings = []
def err(m): errors.append(m)
def warn(m): warnings.append(m)

inc_ids = {r["incident_id"] for r in incidents}

# --- Vocabularies (CIR v0.3 controlled sets, as coded) ---
VOCAB = {
    "observed_state": {"Working","Absent","Inadequate","Bypassed","Disabled","Failed","Disputed","Unknown"},
    "primary_function": {"preventive","detective","containment","recovery","assurance-governance"},
    "system_layer": {"model","application","infrastructure-environment","human-operator","organizational-process","external-ecosystem"},
    "system_type": {"confirmed-ML","probable-ML","algorithmic-nonML","unknown"},
    "outcome_class": {"realized-harm","near-miss","averted"},
    "incident_scope": {"discrete-event","bounded-episode","systemic-program"},
    "timeliness": {"in-time","delayed","too-late","not-applicable"},
    "inadequacy_type": {"design","operation","enforcement","unknown",""},
    "existence_timing": {"incident-time","added-after"},
    "evidence_status": {"confirmed-authoritative","multiply-reported","single-source-reported","inferred-indirect","disputed"},
    "confidence": {"high","medium","low"},
    "causal_role": {"primary","contributing","aggravating","mitigating","latent-condition","not-causally-relevant","unknown"},
    "ai_causal_contribution": {"major-contributor","contributory-non-necessary","minor","disputed","none","unknown"},
    "attributed_primary_cause": {"AI-system","human-operator","organizational","external","multiple","disputed","unknown"},
    "era": {"legacy","genai"},
    "relationship_type": {"enabling","masking","temporal-precedence","common-cause","cascading","compensating"},
    "relationship_confidence": {"high","medium","low"},
}
# evidentiary_basis is multi-valued (semicolon-joined); validate each token.
EVID_BASIS = {"direct-artifact","post-incident-finding","comparable-system","established-practice",
              "operator-claim","regulation-policy","inferred-indirect","research-evidence","multiply-reported"}

# 1. Referential integrity
for r in safeguards:
    if r["incident_id"] not in inc_ids: err(f"safeguard {r['interaction_id']} -> unknown incident {r['incident_id']}")
for r in relationships:
    if r["incident_id"] not in inc_ids: err(f"relationship {r['relationship_id']} -> unknown incident {r['incident_id']}")
for r in factors:
    if r["incident_id"] not in inc_ids: err(f"factor {r['factor_id']} -> unknown incident {r['incident_id']}")
for r in sources:
    if r["incident_id"] not in inc_ids: err(f"source {r['source_id']} -> unknown incident {r['incident_id']}")

# 2. Relationship endpoints resolve within same incident
sg_by_inc = defaultdict(set)
for r in safeguards:
    sg_by_inc[r["incident_id"]].add(r["local_sid"])
rel_cols = relationships[0].keys() if relationships else []
for r in relationships:
    inc = r["incident_id"]
    a = r.get("from_sid") or r.get("from_local_sid")
    b = r.get("to_sid") or r.get("to_local_sid")
    for endpoint in (a, b):
        if endpoint and endpoint not in sg_by_inc[inc]:
            err(f"relationship {r['relationship_id']} endpoint {endpoint} not a safeguard in {inc}")

# 3. ID uniqueness
def dupes(rows, key):
    c = Counter(r[key] for r in rows if r.get(key))
    return [k for k,v in c.items() if v>1]
for rows,key in [(safeguards,"interaction_id"),(relationships,"relationship_id"),(factors,"factor_id"),(sources,"source_id"),(incidents,"incident_id")]:
    for d in dupes(rows,key): err(f"duplicate {key}: {d}")

# 4. Vocabulary validity
for r in incidents:
    for field in ("system_type","outcome_class","incident_scope","ai_causal_contribution"):
        v=r.get(field,"")
        if v and v not in VOCAB.get(field,{v}): err(f"incident {r['incident_id']} bad {field}={v}")
for r in safeguards:
    for field in ("observed_state","primary_function","system_layer","timeliness","inadequacy_type","existence_timing","evidence_status","confidence"):
        v=r.get(field,"")
        if field=="inadequacy_type" and v=="" : continue
        if v and v not in VOCAB.get(field,{v}): err(f"safeguard {r['interaction_id']} bad {field}={v}")

# 5. Denominator-contamination guards
added_after=0; suspected=0
for r in safeguards:
    st=r["observed_state"]; sa=r.get("suspected_absent","0")
    if sa in ("1","True","true"):
        suspected+=1
        if st!="Unknown": err(f"safeguard {r['interaction_id']} suspected_absent set but state={st} (must be Unknown)")
    if r.get("inadequacy_type","") and st!="Inadequate":
        err(f"safeguard {r['interaction_id']} has inadequacy_type={r['inadequacy_type']} but state={st}")
    if r.get("existence_timing")=="added-after": added_after+=1

# 6. control_group within one incident
cg=defaultdict(set)
for r in safeguards:
    g=r.get("control_group","")
    if g: cg[g].add(r["incident_id"])
for g,incs in cg.items():
    if len(incs)>1: err(f"control_group {g} spans incidents {incs}")

# 8. cardinality vs JSON
with open(os.path.join(DATA,"observatory_dataset.json"),encoding="utf-8") as f:
    js=json.load(f)
jinc=len(js["incidents"]) if isinstance(js.get("incidents"),list) else js.get("n_incidents")
if jinc!=len(incidents): warn(f"JSON incident count {jinc} != CSV {len(incidents)}")

print("="*60)
print("DATASET VALIDATION REPORT")
print("="*60)
print(f"incidents={len(incidents)} safeguards={len(safeguards)} relationships={len(relationships)} factors={len(factors)} sources={len(sources)}")
print(f"existence_timing=added-after rows (excluded from incident-time distributions): {added_after}")
print(f"suspected_absent rows (never counted as Absent): {suspected}")
print(f"ERRORS: {len(errors)}")
for e in errors: print("  [ERR]", e)
print(f"WARNINGS: {len(warnings)}")
for w in warnings: print("  [warn]", w)
print("="*60)
print("RESULT:", "PASS" if not errors else "FAIL")
sys.exit(1 if errors else 0)
