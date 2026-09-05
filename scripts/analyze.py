#!/usr/bin/env python3
"""
AI Safeguard Failure Observatory - descriptive analysis (Phase 3, section 19).

Every statistic here is DESCRIPTIVE/EXPLORATORY on n=30 incidents. Nothing is
inferential; no p-values, no representativeness claims. Every table states its
denominator and its unit of analysis explicitly.

Denominator discipline (G-rules):
  - Safeguard-state / function / layer distributions use INCIDENT-TIME safeguards only
    (existence_timing == 'incident-time'); added-after rows are reported separately.
  - suspected_absent rows are Unknown, never folded into Absent.
  - Multi-valued fields are not exploded into double counts.
  - Relationship-level and factor-level stats carry their own denominators.

Outputs:
  analysis/analysis_results.json     - all computed numbers
  analysis/table_*.csv / .md         - publication tables (deliverable G)
  figures/fig_*.png                  - publication figures (deliverable H)
"""
import csv, json, os
from collections import Counter, defaultdict

ROOT = os.path.join(os.path.dirname(__file__), "..")
DATA = os.path.join(ROOT, "data")
ANA = os.path.join(ROOT, "analysis")
FIG = os.path.join(ROOT, "figures")
os.makedirs(ANA, exist_ok=True); os.makedirs(FIG, exist_ok=True)

def load(name):
    with open(os.path.join(DATA, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

incidents = load("incidents.csv")
safeguards = load("safeguards.csv")
relationships = load("relationships.csv")
factors = load("contributing_factors.csv")
sources = load("sources.csv")

R = {}  # results
def pct(n, d): return round(100.0*n/d, 1) if d else 0.0

# ---------- Incident-level ----------
N = len(incidents)
R["n_incidents"] = N
R["by_system_type"] = dict(Counter(r["system_type"] for r in incidents))
R["by_outcome_class"] = dict(Counter(r["outcome_class"] for r in incidents))
R["by_domain"] = dict(Counter(r["domain"] for r in incidents))
R["by_incident_scope"] = dict(Counter(r["incident_scope"] for r in incidents))
R["by_era"] = dict(Counter(r["era"] for r in incidents))
R["by_ai_causal_contribution"] = dict(Counter(r["ai_causal_contribution"] for r in incidents))
R["by_attributed_primary_cause"] = dict(Counter(r["attributed_primary_cause"] for r in incidents))
R["by_incident_confidence"] = dict(Counter(r["incident_confidence"] for r in incidents))
R["agentic_count"] = sum(1 for r in incidents if r.get("agentic") in ("1","True","true"))

# ---------- Safeguard-level: split by existence_timing ----------
sg_incident_time = [r for r in safeguards if r["existence_timing"] == "incident-time"]
sg_added_after   = [r for r in safeguards if r["existence_timing"] == "added-after"]
D = len(sg_incident_time)  # primary denominator for state/function/layer
R["n_safeguards_total"] = len(safeguards)
R["n_safeguards_incident_time"] = D
R["n_safeguards_added_after"] = len(sg_added_after)

# Observed-state distribution (incident-time denominator)
state_ct = Counter(r["observed_state"] for r in sg_incident_time)
R["state_distribution_incident_time"] = {
    k: {"n": v, "pct_of_incident_time_safeguards": pct(v, D)} for k, v in state_ct.items()
}
# suspected_absent audit: these live inside Unknown, never Absent
R["suspected_absent_in_unknown"] = sum(
    1 for r in sg_incident_time if r.get("suspected_absent") in ("1","True","true"))

# "Non-functional" grouping: safeguard did not perform its function at incident time.
# Absent + Failed + Bypassed + Disabled + Inadequate. (Unknown/Disputed excluded; Working excluded.)
nonfunc = {"Absent","Failed","Bypassed","Disabled","Inadequate"}
n_nonfunc = sum(v for k, v in state_ct.items() if k in nonfunc)
n_working = state_ct.get("Working", 0)
R["nonfunctional_incident_time"] = {"n": n_nonfunc, "pct": pct(n_nonfunc, D)}
R["working_incident_time"] = {"n": n_working, "pct": pct(n_working, D)}

# Control-function distribution (incident-time)
func_ct = Counter(r["primary_function"] for r in sg_incident_time)
R["function_distribution_incident_time"] = {k: {"n": v, "pct": pct(v, D)} for k, v in func_ct.items()}

# System-layer distribution (incident-time)
layer_ct = Counter(r["system_layer"] for r in sg_incident_time)
R["layer_distribution_incident_time"] = {k: {"n": v, "pct": pct(v, D)} for k, v in layer_ct.items()}

# State x Function crosstab (incident-time) - where does each function tend to fail?
sf = defaultdict(Counter)
for r in sg_incident_time:
    sf[r["primary_function"]][r["observed_state"]] += 1
R["state_by_function_incident_time"] = {f: dict(c) for f, c in sf.items()}

# State x Layer crosstab
sl = defaultdict(Counter)
for r in sg_incident_time:
    sl[r["system_layer"]][r["observed_state"]] += 1
R["state_by_layer_incident_time"] = {l: dict(c) for l, c in sl.items()}

# ---------- Omission analysis ----------
# Per incident: does it contain at least one Absent safeguard at incident time? (evidentiary fence:
# Absent requires positive evidence the control should have existed and did not.)
absent_by_inc = defaultdict(int)
for r in sg_incident_time:
    if r["observed_state"] == "Absent":
        absent_by_inc[r["incident_id"]] += 1
R["incidents_with_any_absent"] = {"n": len(absent_by_inc), "pct_of_incidents": pct(len(absent_by_inc), N)}
# "Omission-dominated": Absent is the single most common non-Working state in the incident.
omission_dom = 0
for inc in incidents:
    iid = inc["incident_id"]
    rows = [r for r in sg_incident_time if r["incident_id"] == iid and r["observed_state"] in nonfunc]
    if not rows: continue
    c = Counter(r["observed_state"] for r in rows)
    if c and c.most_common(1)[0][0] == "Absent":
        omission_dom += 1
R["omission_dominated_incidents"] = {"n": omission_dom, "pct_of_incidents": pct(omission_dom, N)}

# "Warnings overridden / detected-but-ignored" emergent pattern:
# incidents that have a detective safeguard Working (harm was detected) yet realized harm occurred.
detected_ignored = 0
for inc in incidents:
    iid = inc["incident_id"]
    det_working = any(r["primary_function"] == "detective" and r["observed_state"] == "Working"
                      for r in sg_incident_time if r["incident_id"] == iid)
    if det_working and inc["outcome_class"] == "realized-harm":
        detected_ignored += 1
R["detected_but_harm_still_realized"] = {"n": detected_ignored, "pct_of_incidents": pct(detected_ignored, N)}

# ---------- Relationship-level ----------
NR = len(relationships)
R["n_relationships"] = NR
R["relationship_type_distribution"] = {
    k: {"n": v, "pct_of_relationships": pct(v, NR)} for k, v in Counter(r["relationship_type"] for r in relationships).items()}
R["relationship_confidence_distribution"] = dict(Counter(r["relationship_confidence"] for r in relationships))
rel_per_inc = Counter(r["incident_id"] for r in relationships)
R["relationships_per_incident"] = {
    "min": min(rel_per_inc.values()), "max": max(rel_per_inc.values()),
    "mean": round(sum(rel_per_inc.values())/len(rel_per_inc), 2),
    "incidents_with_zero_relationships": N - len(rel_per_inc)}

# ---------- Contributing factors (kept OUT of safeguard distributions) ----------
NF = len(factors)
R["n_contributing_factors"] = NF
R["factor_type_distribution"] = dict(Counter(r["factor_type"] for r in factors))

# ---------- Evidence quality ----------
R["evidence_status_distribution_safeguards"] = dict(Counter(r["evidence_status"] for r in safeguards))
R["confidence_distribution_safeguards"] = dict(Counter(r["confidence"] for r in safeguards))
R["n_sources"] = len(sources)
src_per_inc = Counter(r["incident_id"] for r in sources)
R["sources_per_incident"] = {
    "min": min(src_per_inc.values()), "max": max(src_per_inc.values()),
    "mean": round(sum(src_per_inc.values())/len(src_per_inc), 2)}

# ---------- Timeliness (detective/containment/recovery only; preventive+assurance are n/a-heavy) ----------
tl = defaultdict(Counter)
for r in sg_incident_time:
    tl[r["primary_function"]][r["timeliness"]] += 1
R["timeliness_by_function_incident_time"] = {f: dict(c) for f, c in tl.items()}

with open(os.path.join(ANA, "analysis_results.json"), "w", encoding="utf-8") as f:
    json.dump(R, f, indent=2)

print("Analysis complete. Key numbers:")
print(f"  incident-time safeguards (denominator D) = {D}")
print(f"  non-functional at incident time = {n_nonfunc} ({pct(n_nonfunc,D)}%)")
print(f"  state distribution = {dict(state_ct)}")
print(f"  incidents with >=1 Absent = {len(absent_by_inc)}/{N}")
print(f"  omission-dominated = {omission_dom}/{N}")
print(f"  detected-but-harm-realized = {detected_ignored}/{N}")
print(f"  relationships = {NR}, factors = {NF}")
