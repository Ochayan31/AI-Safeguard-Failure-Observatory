# Deliverable I - Technical Grounding and Related Work

**AI Safeguard Failure Observatory** · Dataset v1.0

This document grounds the Observatory's descriptive findings in the established safety-science,
human-factors, and AI-safety literatures. Its purpose is not to claim novelty for the *mechanisms*
- most are decades old - but to show that AI/algorithmic safeguard failures in 2010–2025 recapitulate
well-understood failure mechanisms, and to locate the few genuinely new failure surfaces
(agentic/LLM). Citation numbers refer to Deliverable K.

## 1. Layered defenses that fail together (Absent-dominated prevention)

The Observatory finds that among 181 incident-time safeguards, prevention is the function most
often **Absent** (21 of 51 preventive controls) and that **83.3% of incidents (25/30) contain at
least one Absent safeguard**. Reason's Swiss-cheese model [1,2] anticipates exactly this: layered
defenses each carry latent "holes," and accidents occur when holes across layers align. The
Observatory's relationship table operationalizes hole-alignment directly - 58.3% of coded
relationships are **enabling** (one safeguard's failure opens the path for the next), which is the
Swiss-cheese alignment mechanism rendered as data rather than metaphor. Perrow's normal-accident
theory [3] complements this for the tightly coupled cases (Flash Crash, MCAS, agentic tool-use):
in interactively complex, tightly coupled systems some failures are not foreseeable by operators
and no single barrier suffices.

## 2. Detection is rarely the bottleneck; response and escalation are

A central, non-obvious finding: in **36.7% of incidents (11/30) a detective control was Working yet
harm was still realized**, and detection has one of the higher Working shares (13/46, 28%) while
recovery leads (15/25, 60%). The problem is less that systems fail to notice and more that noticing
does not convert into effective action. This is the alarm-fatigue / automation-complacency finding
from human factors: the Joint Commission documented patient deaths where device alarms fired
correctly but were silenced, disabled, or ignored [9]; Parasuraman and colleagues established that
operators under-monitor and over-defer to automation (complacency and automation bias) [7,8]. The
Observatory's **Bypassed** state (15 rows, concentrated in the human-operator layer: 6/26) is the
data-level signature of hollow oversight - review that nominally occurs but does not perform its
function (Toeslagen, Robodebt, Ofqual appeals).

## 3. Governance that exists but is Inadequate

**assurance-governance** controls are dominated by **Inadequate** (13/30 incident-time
assurance-governance rows) rather than Absent. Organizations frequently had validation, impact
assessment, disclosure, or certification processes - they were simply insufficient in design,
operation, or enforcement. Rasmussen's migration-to-the-boundary model [4] explains the temporal
dynamic: under cost and efficiency pressure, organizations drift until governance is present in form
but hollow in substance. The High Reliability Organizations literature [5] describes the inverse
disciplines (preoccupation with failure, deference to expertise) whose absence the Inadequate codings
mark. Raji et al.'s internal-audit framework [18] is the prescriptive counterpart: the SMACTR
process names the assurance steps that, in these incidents, were skipped or performed as ritual.

## 4. Systems-theoretic, not component-chain, causation

That failures are multi-safeguard (mean 2.8 relationships/incident, every incident ≥2) and that
**attributed_primary_cause is "organizational" in 18/30 incidents** rather than "AI-system" (2/30)
supports Leveson's systems-theoretic view [6]: safety is an emergent control property, and accidents
arise from inadequate control across the sociotechnical system, not from a single faulty component.
The Observatory's six-layer model (model → application → infrastructure → human-operator →
organizational-process → external-ecosystem) is a direct operationalization of that stance; the
organizational-process layer carries the most Failed rows (16), and the model layer the fewest rows
overall (14), which is itself a corrective to model-centric framings of AI risk.

## 5. Fairness and validity as safeguard failures

Several incidents fail not by malfunction but by encoding disparate impact or lacking validity.
Obermeyer et al. [10] dissected the exact mechanism in the Optum/Impact Pro case (cost used as a
proxy for health need, systematically under-serving Black patients); the COMPAS dispute [11,12]
is coded as the dataset's showcase **Disputed** precisely because the fairness literature itself
does not agree on the criterion. Coding these as safeguard states (Inadequate/Disputed) rather than
as generic "bias" keeps them commensurable with mechanical failures in the same framework.

## 6. New failure surfaces: agentic and LLM-integrated systems

The generative/agentic-era incidents (8/30, era=genai; 3 agentic) exhibit failure mechanisms with
genuine novelty. Indirect prompt injection [20] - untrusted data hijacking an LLM application's
control flow - is the mechanism behind EchoLeak, Amazon Q, and the Gemini CLI file-destruction
case; OWASP now ranks prompt injection as the top LLM application risk [21]. These map onto older
categories (they are, structurally, an input-validation / privilege-boundary failure) but the attack
surface - natural-language data channels that are simultaneously instructions - is new, and the
Observatory codes it with the same vocabulary, showing both continuity and novelty. The broader
AI-safety framing [16,17,19] supplies the taxonomy of model-layer hazards (distributional shift,
reward misspecification, LLM harms) that these controls were meant to contain.

## 7. Relation to existing incident repositories

The Observatory is complementary to, not a competitor of, the AI Incident Database [13], the OECD AI
Incidents Monitor [14], and AIAAIC [15]. Those repositories catalog *incidents*; the Observatory's
contribution is a **safeguard-level relational coding** - for each incident, which controls existed,
what state they were in, and how they related - which those repositories do not systematically
capture. McGregor's motivation [13] (preventing repeated failures by cataloging them) is the same;
the Observatory adds the layer at which prevention is actually designed.

## Summary

Every mechanism the Observatory surfaces is grounded in prior literature; the value added is (a)
a consistent, denominator-disciplined *coding* of those mechanisms across a mixed AI/algorithmic
sample, and (b) evidence that the newest AI systems fail largely along old fault lines, with a small
but real set of new attack surfaces at the LLM/agentic boundary.
