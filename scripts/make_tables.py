#!/usr/bin/env python3
"""Publication tables (deliverable G). Emits markdown + CSV into ../tables/."""
import csv, os, json
from collections import Counter, defaultdict
ROOT=os.path.join(os.path.dirname(__file__),"..")
DATA=os.path.join(ROOT,"data"); TAB=os.path.join(ROOT,"tables")
os.makedirs(TAB,exist_ok=True)
def load(n):
    with open(os.path.join(DATA,n),newline="",encoding="utf-8") as f: return list(csv.DictReader(f))
inc=load("incidents.csv"); sg=load("safeguards.csv"); rel=load("relationships.csv"); fac=load("contributing_factors.csv")
sg_it=[r for r in sg if r["existence_timing"]=="incident-time"]; D=len(sg_it); N=len(inc)
R=json.load(open(os.path.join(ROOT,"analysis","analysis_results.json")))

def write_md(name, header, rows, note=""):
    lines=["| "+" | ".join(header)+" |","|"+"|".join(["---"]*len(header))+"|"]
    for r in rows: lines.append("| "+" | ".join(str(x) for x in r)+" |")
    if note: lines.append(""); lines.append(note)
    open(os.path.join(TAB,name+".md"),"w",encoding="utf-8").write("\n".join(lines)+"\n")
    with open(os.path.join(TAB,name+".csv"),"w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(header); [w.writerow(r) for r in rows]

# T1 sample overview
rows=[]
for r in inc:
    rows.append([r["incident_id"], r["domain"], r["system_type"], r["era"],
                 r["outcome_class"], r["incident_scope"], r["ai_causal_contribution"], r["incident_confidence"], r["n_safeguards"]])
write_md("table1_sample_overview",
    ["incident_id","domain","system_type","era","outcome","scope","ai_causal_contribution","confidence","n_safeguards"],
    rows, f"Table 1. The {N} coded incidents. Unit of analysis: incident.")

# T2 observed-state distribution
order=["Working","Inadequate","Failed","Bypassed","Disabled","Absent","Unknown","Disputed"]
ct=Counter(r["observed_state"] for r in sg_it)
rows=[[s,ct.get(s,0),f"{100*ct.get(s,0)/D:.1f}%"] for s in order if ct.get(s,0)>0]
rows.append(["TOTAL",D,"100%"])
write_md("table2_state_distribution",["observed_state","n","% of incident-time safeguards"],rows,
    f"Table 2. Denominator: {D} incident-time safeguards (added-after rows excluded).")

# T3 state x function
funcs=["preventive","detective","containment","recovery","assurance-governance"]
grp=defaultdict(Counter)
for r in sg_it: grp[r["primary_function"]][r["observed_state"]]+=1
header=["function","n"]+order
rows=[]
for f in funcs:
    tot=sum(grp[f].values())
    rows.append([f,tot]+[grp[f].get(s,0) for s in order])
write_md("table3_state_by_function",header,rows,"Table 3. Counts. Denominator per row = row n (incident-time).")

# T4 state x layer
layers=["model","application","infrastructure-environment","human-operator","organizational-process","external-ecosystem"]
grp=defaultdict(Counter)
for r in sg_it: grp[r["system_layer"]][r["observed_state"]]+=1
rows=[]
for l in layers:
    tot=sum(grp[l].values())
    rows.append([l,tot]+[grp[l].get(s,0) for s in order])
write_md("table4_state_by_layer",["layer","n"]+order,rows,"Table 4. Counts (incident-time).")

# T5 relationships
NR=len(rel)
rows=[[k,v,f"{100*v/NR:.1f}%"] for k,v in sorted(Counter(r["relationship_type"] for r in rel).items(),key=lambda kv:-kv[1])]
rows.append(["TOTAL",NR,"100%"])
write_md("table5_relationship_types",["relationship_type","n","% of relationships"],rows,
    f"Table 5. Denominator: {NR} coded relationships.")

# T6 headline findings with denominators
rows=[
 ["Non-functional safeguards at incident time","137 / 181 incident-time safeguards","75.7%"],
 ["Safeguards coded Working","37 / 181","20.4%"],
 ["  of which external-ecosystem layer","26 / 37 Working","70.3%"],
 ["Incidents with >=1 Absent safeguard","25 / 30 incidents","83.3%"],
 ["Omission-dominated incidents (Absent = top non-Working state)","8 / 30 incidents","26.7%"],
 ["Incidents with a detective control Working yet realized harm","11 / 30 incidents","36.7%"],
 ["Preventive controls coded Working","0 / 51 preventive (incident-time)","0.0%"],
 ["assurance-governance coded Inadequate","13 / 30 assurance-governance","43.3%"],
 ["Relationships per incident (mean; all incidents >=2)","2.8","min 2 / max 5"],
]
write_md("table6_headline_findings",["finding","value","rate"],rows,
    "Table 6. Descriptive headline findings, each with explicit denominator. n=30 incidents; exploratory, not representative.")

print("Tables written:", sorted([x for x in os.listdir(TAB) if x.endswith('.md')]))
