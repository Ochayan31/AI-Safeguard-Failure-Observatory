#!/usr/bin/env python3
"""
INDEPENDENT clean-room audit. Reads ONLY the frozen data/*.csv files.
Does NOT import or read analysis_results.json. Recomputes every headline number
from raw rows, so any drift between the paper and the dataset is caught.
"""
import csv, os
from collections import Counter, defaultdict
D=os.path.join(os.path.dirname(__file__),"..","data")
def load(n):
    with open(os.path.join(D,n),newline="",encoding="utf-8") as f: return list(csv.DictReader(f))
inc=load("incidents.csv"); sg=load("safeguards.csv"); rel=load("relationships.csv")
fac=load("contributing_factors.csv"); src=load("sources.csv")

print("### CARDINALITY")
print("incidents:",len(inc))
print("safeguards total:",len(sg))
it=[r for r in sg if r["existence_timing"]=="incident-time"]
aa=[r for r in sg if r["existence_timing"]=="added-after"]
other_et=[r for r in sg if r["existence_timing"] not in ("incident-time","added-after")]
print("  incident-time:",len(it)," added-after:",len(aa)," other:",len(other_et))
print("  181+21 check:",len(it),"+",len(aa),"=",len(it)+len(aa),"(should be",len(sg),")")
print("relationships:",len(rel)," factors:",len(fac)," sources:",len(src))

print("\n### OBSERVED-STATE (incident-time) - recomputed from raw")
st=Counter(r["observed_state"] for r in it)
tot=sum(st.values())
for k in ["Working","Inadequate","Failed","Bypassed","Disabled","Absent","Unknown","Disputed"]:
    print(f"  {k:11s} {st.get(k,0):3d}")
print("  SUM:",tot,"(must equal",len(it),")")
nonfunc_states=["Absent","Failed","Inadequate","Bypassed","Disabled"]
nf=sum(st.get(k,0) for k in nonfunc_states)
print(f"  non-functional (Absent+Failed+Inadequate+Bypassed+Disabled) = {nf} / {tot} = {100*nf/tot:.4f}% -> {round(100*nf/tot,1)}%")
print(f"  not-Working (all minus Working) = {tot-st.get('Working',0)} / {tot} = {100*(tot-st['Working'])/tot:.2f}%")
print(f"  Unknown+Disputed (neither working nor 'failed') = {st.get('Unknown',0)+st.get('Disputed',0)}")
print(f"  Working = {st.get('Working',0)} / {tot} = {100*st['Working']/tot:.4f}% -> {round(100*st['Working']/tot,1)}%")

print("\n### WORKING BY LAYER (of the Working safeguards, how many external?)")
work=[r for r in it if r["observed_state"]=="Working"]
wl=Counter(r["system_layer"] for r in work)
print("  Working total:",len(work))
for k,v in wl.most_common(): print(f"    {k}: {v}")
ext=wl.get("external-ecosystem",0)
print(f"  external Working = {ext}/{len(work)} = {100*ext/len(work):.4f}% -> {round(100*ext/len(work),1)}%")

print("\n### FUNCTION TOTALS (incident-time) reconcile to 181?")
fn=Counter(r["primary_function"] for r in it)
print(" ",dict(fn)," sum=",sum(fn.values()))
print("\n### LAYER TOTALS (incident-time) reconcile to 181?")
ly=Counter(r["system_layer"] for r in it)
print(" ",dict(ly)," sum=",sum(ly.values()))

print("\n### STATE x FUNCTION checks")
sf=defaultdict(Counter)
for r in it: sf[r["primary_function"]][r["observed_state"]]+=1
print("  preventive Working =",sf["preventive"].get("Working",0),"(paper: 0)")
print("  assurance-governance Inadequate =",sf["assurance-governance"].get("Inadequate",0),"(paper: 13)")
print("  detective Working =",sf["detective"].get("Working",0))
print("  recovery Working =",sf["recovery"].get("Working",0),f"({100*sf['recovery'].get('Working',0)/fn['recovery']:.0f}%)")

print("\n### STATE x LAYER: model layer detail (claim 3)")
ml=[r for r in it if r["system_layer"]=="model"]
print("  model-layer incident-time rows:",len(ml)," states:",dict(Counter(r['observed_state'] for r in ml)))
print("  model-layer Working:",sum(1 for r in ml if r['observed_state']=='Working'))

print("\n### INCIDENT-LEVEL headline counts")
print("  ai_causal_contribution:",dict(Counter(r["ai_causal_contribution"] for r in inc)))
print("  attributed_primary_cause:",dict(Counter(r["attributed_primary_cause"] for r in inc)))
print("  system_type:",dict(Counter(r["system_type"] for r in inc)))
print("  era:",dict(Counter(r["era"] for r in inc)))
print("  outcome_class:",dict(Counter(r["outcome_class"] for r in inc)))
print("  incident_scope:",dict(Counter(r["incident_scope"] for r in inc)))
print("  agentic:",sum(1 for r in inc if r["agentic"] in ("1","True","true")))

print("\n### ERA=genai incidents with dates (verify 8 and 2022+ criterion)")
for r in inc:
    if r["era"]=="genai":
        print(f"    {r['incident_id']:34s} start={r['date_start']} agentic={r['agentic']}")
print("  legacy incidents dated 2022+ (possible mislabel)?")
for r in inc:
    if r["era"]=="legacy":
        y=r["date_start"][:4]
        if y.isdigit() and int(y)>=2022:
            print(f"    LEGACY but {y}: {r['incident_id']} ({r['date_start']}..{r['date_end']})")

print("\n### incidents with >=1 Absent (incident-time)")
absset={r["incident_id"] for r in it if r["observed_state"]=="Absent"}
print("  =",len(absset),"/",len(inc))

print("\n### detective-Working incidents with realized harm")
outc={r["incident_id"]:r["outcome_class"] for r in inc}
detw=defaultdict(bool)
for r in it:
    if r["primary_function"]=="detective" and r["observed_state"]=="Working":
        detw[r["incident_id"]]=True
cnt=sum(1 for iid in detw if detw[iid] and outc.get(iid)=="realized-harm")
print("  detective-Working incidents:",len(detw))
print("  of those with realized-harm:",cnt,"/",len(inc),f"= {100*cnt/len(inc):.1f}%")

print("\n### RELATIONSHIPS")
rt=Counter(r["relationship_type"] for r in rel)
print(" ",dict(rt)," sum=",sum(rt.values()))
print(f"  enabling = {rt['enabling']}/{len(rel)} = {100*rt['enabling']/len(rel):.4f}% -> {round(100*rt['enabling']/len(rel),1)}%")
rpi=Counter(r["incident_id"] for r in rel)
print(f"  per-incident: min={min(rpi.values())} max={max(rpi.values())} mean={sum(rpi.values())/len(rpi):.4f} incidents_covered={len(rpi)}/{len(inc)}")

print("\n### endpoints all resolve within incident?")
sgset=defaultdict(set)
for r in sg: sgset[r["incident_id"]].add(r["interaction_id"])
bad=0
for r in rel:
    if r["from_interaction"] not in sgset[r["incident_id"]] or r["to_interaction"] not in sgset[r["incident_id"]]: bad+=1
print("  unresolved endpoints:",bad)

print("\n### SELECTION FLOORS/CAPS (from frozen data)")
print("  genai(recency) >=5 :", sum(1 for r in inc if r['era']=='genai'))
print("  agentic >=2 :", sum(1 for r in inc if r['agentic'] in ('1','True','true')))
dom=Counter(r["domain"] for r in inc)
print("  per-domain max (<=5):", max(dom.values()), dict(dom))
