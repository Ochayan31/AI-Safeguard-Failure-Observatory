#!/usr/bin/env python3
"""
Publication figures (deliverable H). Static PNGs for the paper.
Colors drawn from the dataviz reference palette (pre-validated hues). Observed-state
uses a semantic status mapping; adjacent segments kept distinct. Every figure states
its denominator in the title/caption-line.
"""
import csv, os
from collections import Counter, defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = os.path.join(os.path.dirname(__file__), "..")
DATA = os.path.join(ROOT, "data"); FIG = os.path.join(ROOT, "figures")
os.makedirs(FIG, exist_ok=True)

def load(n):
    with open(os.path.join(DATA, n), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
incidents = load("incidents.csv"); safeguards = load("safeguards.csv")
relationships = load("relationships.csv")
sg_it = [r for r in safeguards if r["existence_timing"] == "incident-time"]
D = len(sg_it); N = len(incidents)

# Semantic state colors (from validated palette hues)
STATE_ORDER = ["Working","Inadequate","Failed","Bypassed","Disabled","Absent","Unknown","Disputed"]
STATE_COLOR = {
    "Working":  "#1baf7a",  # aqua-green: functioning
    "Inadequate":"#eda100", # amber
    "Failed":   "#e34948",  # red
    "Bypassed": "#eb6834",  # orange
    "Disabled": "#e87ba4",  # magenta
    "Absent":   "#4a3aa7",  # violet: structural gap
    "Unknown":  "#b8b7b0",  # light gray
    "Disputed": "#52514e",  # dark gray
}
INK="#0b0b0b"; INK2="#52514e"; GRID="#e6e5e1"

plt.rcParams.update({
    "font.family":"DejaVu Sans","font.size":10,"axes.edgecolor":INK2,
    "axes.linewidth":0.8,"figure.dpi":150,"savefig.dpi":150,
    "text.color":INK,"axes.labelcolor":INK,"xtick.color":INK2,"ytick.color":INK2,
})

def clean(ax):
    for s in ("top","right"): ax.spines[s].set_visible(False)
    ax.tick_params(length=0)

# ---- Fig 1: observed-state distribution (incident-time) ----
ct = Counter(r["observed_state"] for r in sg_it)
states = [s for s in STATE_ORDER if ct.get(s,0)>0]
vals = [ct[s] for s in states]
fig, ax = plt.subplots(figsize=(7.2,4.0))
y = range(len(states))
ax.barh(list(y), vals, color=[STATE_COLOR[s] for s in states], height=0.68, zorder=3)
ax.set_yticks(list(y)); ax.set_yticklabels(states)
ax.invert_yaxis(); clean(ax)
ax.set_xlim(0, max(vals)*1.15)
for i,v in enumerate(vals):
    ax.text(v+max(vals)*0.01, i, f"{v}  ({100*v/D:.0f}%)", va="center", fontsize=9, color=INK)
ax.set_xlabel(f"Number of safeguards (denominator: {D} incident-time safeguards)")
ax.set_title("Figure 1. Observed state of AI/algorithmic safeguards at incident time",
             fontsize=11, fontweight="bold", loc="left")
ax.xaxis.grid(True, color=GRID, zorder=0)
plt.tight_layout(); plt.savefig(os.path.join(FIG,"fig1_state_distribution.png")); plt.close()

# ---- Fig 2 & 3: 100% stacked by function / by layer ----
def stacked(dim, order, fname, fignum, title):
    grp = defaultdict(Counter)
    for r in sg_it: grp[r[dim]][r["observed_state"]] += 1
    cats = [c for c in order if c in grp]
    tot = {c: sum(grp[c].values()) for c in cats}
    fig, ax = plt.subplots(figsize=(8.2,4.4))
    left = [0]*len(cats)
    for st in STATE_ORDER:
        widths = [100*grp[c].get(st,0)/tot[c] for c in cats]
        if sum(widths)==0: continue
        ax.barh(range(len(cats)), widths, left=left, color=STATE_COLOR[st],
                label=st, height=0.66, edgecolor="white", linewidth=1.2, zorder=3)
        for i,w in enumerate(widths):
            if w>=7:
                ax.text(left[i]+w/2, i, f"{grp[cats[i]].get(st,0)}", va="center", ha="center",
                        fontsize=8, color="white" if st not in ("Unknown","Inadequate") else INK)
        left=[left[i]+widths[i] for i in range(len(cats))]
    ax.set_yticks(range(len(cats)))
    ax.set_yticklabels([f"{c}\n(n={tot[c]})" for c in cats])
    ax.invert_yaxis(); clean(ax); ax.set_xlim(0,100)
    ax.set_xlabel("Share of incident-time safeguards within category (%)")
    ax.set_title(title, fontsize=11, fontweight="bold", loc="left")
    ax.legend(ncol=4, fontsize=8, loc="upper center", bbox_to_anchor=(0.5,-0.14), frameon=False)
    plt.tight_layout(); plt.savefig(os.path.join(FIG,fname), bbox_inches="tight"); plt.close()

stacked("primary_function",
        ["preventive","detective","containment","recovery","assurance-governance"],
        "fig2_state_by_function.png", 2,
        "Figure 2. Observed state by control function (incident-time safeguards)")
stacked("system_layer",
        ["model","application","infrastructure-environment","human-operator","organizational-process","external-ecosystem"],
        "fig3_state_by_layer.png", 3,
        "Figure 3. Observed state by system layer (incident-time safeguards)")

# ---- Fig 4: relationship-type distribution ----
rc = Counter(r["relationship_type"] for r in relationships)
NR=len(relationships)
order4=["enabling","temporal-precedence","common-cause","masking"]
order4=[o for o in order4 if o in rc]
vals4=[rc[o] for o in order4]
fig,ax=plt.subplots(figsize=(7.2,3.4))
ax.barh(range(len(order4)), vals4, color="#2a78d6", height=0.62, zorder=3)
ax.set_yticks(range(len(order4))); ax.set_yticklabels(order4)
ax.invert_yaxis(); clean(ax); ax.set_xlim(0,max(vals4)*1.15)
for i,v in enumerate(vals4):
    ax.text(v+max(vals4)*0.01,i,f"{v} ({100*v/NR:.0f}%)",va="center",fontsize=9)
ax.set_xlabel(f"Number of relationships (denominator: {NR} coded relationships)")
ax.set_title("Figure 4. Types of inter-safeguard relationship",fontsize=11,fontweight="bold",loc="left")
ax.xaxis.grid(True,color=GRID,zorder=0)
plt.tight_layout(); plt.savefig(os.path.join(FIG,"fig4_relationship_types.png")); plt.close()

# ---- Fig 5: incident composition (2x2 small multiples) ----
fig,axes=plt.subplots(2,2,figsize=(9.2,6.4))
def small(ax,counter,title,color="#2a78d6"):
    items=sorted(counter.items(), key=lambda kv:-kv[1])
    labels=[k for k,_ in items]; vals=[v for _,v in items]
    ax.barh(range(len(labels)),vals,color=color,height=0.6,zorder=3)
    ax.set_yticks(range(len(labels))); ax.set_yticklabels(labels,fontsize=9)
    ax.invert_yaxis(); clean(ax); ax.set_xlim(0,max(vals)*1.2)
    for i,v in enumerate(vals): ax.text(v+max(vals)*0.02,i,str(v),va="center",fontsize=8)
    ax.set_title(title,fontsize=10,fontweight="bold",loc="left")
    ax.xaxis.grid(True,color=GRID,zorder=0)
small(axes[0,0],Counter(r["system_type"] for r in incidents),"System type","#2a78d6")
small(axes[0,1],Counter(r["outcome_class"] for r in incidents),"Outcome class","#1baf7a")
small(axes[1,0],Counter(r["era"] for r in incidents),"Era","#eb6834")
small(axes[1,1],Counter(r["ai_causal_contribution"] for r in incidents),"AI causal contribution","#4a3aa7")
fig.suptitle(f"Figure 5. Composition of the coded sample (n={N} incidents)",
             fontsize=11,fontweight="bold",x=0.02,ha="left")
plt.tight_layout(rect=[0,0,1,0.96]); plt.savefig(os.path.join(FIG,"fig5_sample_composition.png")); plt.close()

# ---- Fig 6: the "detection is not the bottleneck" view ----
# For each function, share Working vs not-Working (incident-time).
grp=defaultdict(Counter)
for r in sg_it: grp[r["primary_function"]][r["observed_state"]]+=1
funcs=["preventive","detective","containment","recovery","assurance-governance"]
work=[100*grp[f].get("Working",0)/sum(grp[f].values()) for f in funcs]
fig,ax=plt.subplots(figsize=(7.6,3.8))
bars=ax.barh(range(len(funcs)),work,color="#1baf7a",height=0.6,zorder=3)
ax.barh(range(len(funcs)),[100-w for w in work],left=work,color="#d9d8d3",height=0.6,zorder=3)
ax.set_yticks(range(len(funcs)))
ax.set_yticklabels([f"{f}\n(n={sum(grp[f].values())})" for f in funcs])
ax.invert_yaxis(); clean(ax); ax.set_xlim(0,100)
for i,w in enumerate(work):
    ax.text(min(w+1.5,92),i,f"{grp[funcs[i]].get('Working',0)} Working ({w:.0f}%)",va="center",fontsize=8,color=INK)
ax.set_xlabel("Share Working (green) vs not-Working (gray), incident-time")
ax.set_title("Figure 6. Share 'Working' by function (incident-time)",
             fontsize=11,fontweight="bold",loc="left")
plt.tight_layout(); plt.savefig(os.path.join(FIG,"fig6_working_share_by_function.png"),bbox_inches="tight"); plt.close()

print("Figures written:", sorted(os.listdir(FIG)))
