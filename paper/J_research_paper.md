# How AI and Algorithmic Safeguards Fail: A Relational Coding of 30 Real-World Incidents

**The AI Safeguard Failure Observatory**
Dataset v1.0 (frozen 2026-09-05) · n = 30 incidents · Exploratory descriptive study

---

## Abstract

Public discussion of AI risk tends to ask whether a system failed. This study asks a different
question: when an AI or algorithmic system contributes to harm, what happened to the safeguards
that were supposed to prevent it? We built a relational dataset of 30 real-world incidents
(2010-2025) spanning autonomous vehicles, welfare automation, healthcare, criminal justice,
consumer chatbots, agentic LLM tools, finance, hiring, content moderation, and more. For each
incident we coded every identifiable safeguard as a structured interaction (its system layer, its
control function, its observed state at the time of the incident, the evidentiary basis for that
coding, and its causal role) and coded the typed relationships between safeguards. The result is
202 safeguard-interaction rows (181 present at incident time), 84 inter-safeguard relationships,
and 25 contributing factors, each traceable to primary or authoritative sources.

The findings are descriptive and exploratory, not statistically representative. Across the 181
incident-time safeguards, 75.7% were non-functional (Absent, Failed, Inadequate, Bypassed, or
Disabled) and only 20.4% were Working; of those Working, 70.3% sat in the external-ecosystem layer
(journalists, regulators, litigation, researchers) rather than inside the operator's own controls.
Prevention was the most-Absent function; governance controls, when present, were most often
Inadequate rather than missing. In 11 of 30 incidents a detective control was Working at incident time
yet harm still occurred, suggesting (within this sample only) that detection can be insufficient where
downstream escalation, intervention, and authority-to-act are weak. Failures were consistently
multi-safeguard (mean 2.8 typed relationships per
incident, every incident at least two), and the dominant relationship type was enabling (58.3%),
the data-level signature of Reason's Swiss-cheese hole alignment. Primary responsibility was
attributed to organizational rather than model-level causes in 18 of 30 incidents. The newest
generative and agentic systems (8 of 30) fail largely along old fault lines, with a small but real
set of new attack surfaces at the LLM/agentic boundary (indirect prompt injection). We release the
dataset, coding manual, selection protocol, and analysis code so the coding can be scrutinized,
corrected, and extended.

## 1. Introduction

The catalog of AI and algorithmic harms is now large enough that individual cases no longer surprise.
What remains poorly understood is systematic: across many incidents, in what state were the
safeguards? A safeguard can be entirely absent, present but poorly designed, present but deliberately
switched off, present but circumvented by a rushed human reviewer, or working exactly as intended
and still insufficient. These are different failures with different remedies, and lumping them
together as "the AI failed" obscures where intervention would actually help.

This study treats the safeguard, not the incident, as the primary unit of interest, and asks three
questions. First, what is the distribution of safeguard states when AI or algorithmic systems
contribute to harm? Second, how do safeguards relate to one another in a failure, and can those
relationships be coded reliably rather than described anecdotally? Third, do the newest AI systems
(generative and agentic) fail in new ways, or do they recapitulate old failure mechanisms on new
substrates?

We answer these with a purpose-built coding framework (the Control-Incident-Relationship, or CIR,
framework) applied to a deliberately, reproducibly selected sample of 30 incidents. The
contribution is not a new theory of failure; it is a disciplined, transparent, safeguard-level
dataset that lets existing safety theory be checked against a mixed AI/algorithmic sample, and that
others can correct and build on.

We state the central caveat up front. With n = 30, and a sample selected on the occurrence of
realized harm or credible near-miss, nothing here is statistically representative of AI systems in
general, and several distributions are shaped by that selection. Every quantitative claim below
carries its denominator and its unit of analysis, and Section 7 is devoted to the limitations this
design imposes.

## 2. Related work and technical grounding

The mechanisms this dataset surfaces are, with one exception, well established. Reason's model of
organizational accidents [1,2] describes layered defenses that fail when latent holes align, which
is precisely what the Observatory's dominant enabling relationships encode. Perrow's normal-accident
theory [3] and Leveson's systems-theoretic model [6] explain why, in tightly coupled and complex
sociotechnical systems, single barriers are insufficient and causation is distributed rather than
component-local. Rasmussen's migration-to-the-boundary model [4] and the High Reliability
Organizations literature [5] account for the temporal drift by which governance becomes present in
form but hollow in substance. Human-factors work on automation bias and complacency [7,8] and on
alarm fatigue [9] explains the recurring pattern of detection that works while response fails. The
algorithmic-fairness literature [10,11,12] supplies the mechanism for the incidents that fail by
disparate impact rather than malfunction. AI-specific safety framings [16,17,19] and the internal-audit
literature [18] name the model-layer hazards and the assurance steps involved. Prompt-injection
research [20] and the OWASP LLM risk list [21] cover the clearest new surface, the LLM/agentic
boundary. Finally, existing incident repositories [13,14,15] catalog incidents; the Observatory is
complementary, adding the safeguard-level relational coding those repositories do not systematically
capture. Deliverable I develops each of these links in detail.

## 3. Framework (CIR)

The CIR framework (v0.3; full text in `docs/cir_framework_v0.3.md`) models each incident as a set of
safeguard interactions plus a set of typed relationships between them, with contributing factors held
in a separate table so they never contaminate safeguard statistics. Three design decisions do most of
the analytical work.

First, eligibility is set at "the AI or algorithmic system materially contributed to the harm,
attempted harm, or credible near-miss," and the system's causal contribution is coded separately
(`ai_causal_contribution`) from where blame was attributed (`attributed_primary_cause`). This keeps
causal weight and responsibility distinct, which matters because they frequently diverge: the AI was
a major contributor in 26 of 30 incidents, yet primary responsibility was attributed to
organizational causes in 18.

Second, the observed state of a safeguard is separated from the evidentiary basis for that coding.
A safeguard is coded Absent only when there is positive evidence it should have existed and did not
(the "evidentiary fence"); where absence cannot be evidenced, the safeguard is coded Unknown, with an
optional `suspected_absent` flag that is explicitly barred from ever being counted as Absent. This
prevents the dataset from inventing counterfactual controls, at the cost of some conservatism.

Third, relationships are typed (enabling, masking, temporal-precedence, common-cause, and others)
with an explicit rule that temporal precedence alone can never justify a causal relationship. This
lets the dataset represent structure without overclaiming causation.

The state vocabulary distinguishes Working, Inadequate, Failed, Bypassed, Disabled, Absent, Disputed,
and Unknown. The distinction between Bypassed (present but circumvented, including hollow rubber-stamp
review), Disabled (deliberately switched off), and Absent (never existed) is central to the findings
and was calibrated on the pilot and Batch-1 incidents (Section 5).

## 4. Selection methodology

The sample was drawn by a pre-registered, reproducible protocol (`docs/incident_selection_protocol.md`)
designed to prevent selection favorable to the framework. A discovery pool of 108 candidates was
assembled by a fixed-source sweep, separate from the coded sample. Eligibility screening removed
cases with no AI or algorithmic decision system in the causal chain (the same principle that excludes
Therac-25 and, at coding, the 2025 Iberian blackout). From the eligible pool, cases were selected by
a frozen "Hybrid E then R" rule: within predefined strata, cases were ranked by a pre-specified
evidence-quality rubric, and the highest-ranked were taken up to quota, with a seeded random draw
(seed `AISFO-2026-08-24`) only for ties at the selection boundary. Evidence quality was explicitly
barred from incorporating whether a case looked interesting, contained many safeguards, or supported
any anticipated finding. Selection preceded all outcome and relational analysis.

Frozen floors ensured variation without cherry-picking: at least 8 omission-dominated cases (to guard
against selecting only cases with rich relational structure, which would flatter the framework), at
least 5 generative-era cases, and at least 2 agentic cases, with per-domain caps of 5. The locked
sample satisfies every floor and cap. One case (the Iberian blackout) was found ineligible during
coding and deterministically replaced by re-running the selection script with it marked ineligible;
all other 29 held. This is the only change to the locked sample and is logged.

The resulting 30 incidents span 13 domains (autonomous-vehicle 4, government-benefits 4,
security-cyber 3, healthcare-clinical 3, consumer-chatbot 3, and eight further domains with 1-2 each),
three system types (confirmed-ML 17, algorithmic-nonML 8, probable-ML 5), and two eras (legacy 22,
generative 8), with 14 discrete events, 14 systemic programs, and 2 bounded episodes. Table 1
lists the full sample.

## 5. Coding process and quality assurance

The 30 incidents were coded in six batches of five, following a pilot of three deliberately different
cases (one high-evidence, one messy sociotechnical, one technically complex) whose purpose was to
surface every field that failed, required judgment, or produced ambiguity before the full sample was
touched. Two calibration decisions from Batch 1 were locked and applied sample-wide: deliberate
suppression of a control is coded Disabled rather than Bypassed, and controls representing one
underlying safeguard are coded as one row rather than split. Twelve coding calls were flagged for
scrutiny and individually adjudicated against their primary sources; their dispositions are recorded
in Deliverable E.

The frozen dataset passes an automated integrity validator (`scripts/validate.py`) with zero errors:
referential integrity across all tables, ID uniqueness, controlled-vocabulary validity, and a set of
denominator-contamination guards (suspected_absent only within Unknown and never counted as Absent;
inadequacy_type only where Inadequate; added-after rows flagged for exclusion from incident-time
distributions; contributing factors held out of safeguard statistics). Evidentiary quality is
recorded per row: of 202 safeguard rows, 146 are confirmed-authoritative and 8 are disputed; 134 are
coded at high confidence and 13 at low. Sub-judice cases (Raine v. OpenAI, Mobley v. Workday) are
coded conservatively at low confidence and disputed status and are not adjudicated by the coding.

## 6. Results

All distributions below use explicit denominators. State, function, and layer distributions use the
181 incident-time safeguards (the 21 added-after rows are excluded, since a control added in response
to an incident cannot describe the incident's own defenses). Relationship statistics use the 84 coded
relationships; incident-level statistics use the 30 incidents. Table 6 collects the headline numbers.

### 6.1 Most safeguards were not functioning, and most that were sat outside the operator

Of 181 incident-time safeguards, 137 (75.7%) were non-functional and 37 (20.4%) were Working
(Figure 1; Table 2). The single most common state was Absent (44), followed by Inadequate (41),
Working (37), Failed (32), Bypassed (15), Unknown (6), Disabled (5), and Disputed (1). The Working
share is not distributed evenly across the system: of the 37 Working safeguards, 26 (70.3%) sit in
the external-ecosystem layer, meaning the control that "worked" was frequently a journalist, a
regulator, a court, or an academic surfacing the harm after the fact, rather than any control the
operator built. This is a sobering pattern: in this sample, the safeguards most often found Working
were external to the operator. It should be read with its selection effect in mind, because incidents
partly enter the sample when external actors surface them, which inflates the external-ecosystem
Working share; the claim is about where Working safeguards concentrated in these 30 cases, not an
unconditional ranking of which safeguards are most reliable.

### 6.2 Prevention is most often Absent; governance is most often Inadequate

Broken out by control function (Figure 2; Table 3), the two most-coded functions fail in
characteristically different ways. Preventive controls (51 rows) are dominated by Absent (21) and
contain zero Working rows at incident time. That zero is partly definitional and we flag it as such:
in a sample selected on realized harm, prevention by construction did not fully hold, so this is not
a discovered effect so much as a property of the sample. What is informative is the *composition* of
preventive failure, which is more Absent (structurally missing) than Failed (present but
malfunctioning). Assurance-governance controls (30 rows), by contrast, are dominated by Inadequate
(13) rather than Absent (7): organizations frequently had validation, impact-assessment, disclosure,
or certification processes that were present but hollow, consistent with drift-to-the-boundary [4]
and with governance performed as ritual [18].

### 6.3 Detection was frequently insufficient to prevent harm

In this sample, detection was frequently insufficient to prevent harm: 11 of 30 incidents involved at
least one detective safeguard that was Working at incident time despite harm subsequently occurring.
The system, or someone in it, noticed, and harm followed anyway. Detection was also far from always
intact elsewhere in the sample (32 of 46 detective controls were themselves non-functional, with a
further one Unknown), so this is not a claim that detection never fails; the point is the narrower one
that, in these 11 cases, a Working detective control did not suffice. Read cautiously, and only of
these 30 incidents, this suggests that detection alone may be insufficient where the escalation,
intervention, or authority-to-act mechanisms downstream of it are weak, which is consistent with the
human-factors record on alarm fatigue and automation complacency [7,8,9]. The Bypassed state (15 rows,
6 of them in the human-operator layer) is the data-level signature of hollow oversight: a human or
process nominally in the loop but structurally prevented from meaningful engagement.

### 6.4 Failures are multi-safeguard, and the dominant relationship is enabling

No incident failed through a single safeguard. Every incident carries at least two typed
relationships (mean 2.8, range 2-5; 84 total). The dominant type is enabling (49 of 84, 58.3%),
where one safeguard's failure opens the path for the next, followed by temporal-precedence (18,
21.4%), common-cause (10, 11.9%), and masking (7, 8.3%) (Figure 4; Table 5). The predominance of
enabling relationships is the Swiss-cheese alignment mechanism [1,2] expressed as data: harm arrives
not because one barrier failed but because the failure of one barrier removed the protection that
would have caught the next.

### 6.5 Blame lands on organizations, not models

At the incident level, the AI or algorithmic system was a major causal contributor in 26 of 30
incidents (Figure 5), yet primary responsibility was attributed to organizational causes in 18 of
30, to multiple causes in 6, to the AI system itself in only 2, to a human operator in 1, and
disputed in 3. Consistent with this, the organizational-process layer carries the most Failed rows
(16), while the model layer is the least-coded layer overall (14 of 181; Figure 3; Table 4). This is
not a claim that models are reliable: the 14 model-layer controls were, where present, uniformly
non-functional (0 Working). The point is narrower and about where safeguards and blame sit: few
safeguards live at the model layer, and responsibility was attributed organizationally far more often
than to the AI system. A purely model-centric reading of AI risk is therefore not well supported by
this sample; the failures are predominantly organizational and sociotechnical [6].

### 6.6 New systems, mostly old fault lines

The eight generative-era incidents (three of them agentic) fail largely along mechanisms already in
the framework: absent input validation, missing privilege boundaries, inadequate testing. The clearest
new attack surface is indirect prompt injection, where untrusted data doubles as instructions and
hijacks an LLM application's control flow (EchoLeak, Amazon Q, the Gemini CLI file-destruction case)
[20,21]; a second candidate for genuine novelty is LLM confabulation presented as authoritative
output (the fabricated legal citations in Mata v. Avianca, the invented policy in the Air Canada case),
which has no clean pre-2022 analogue. Coded in the same vocabulary as a 2010 trading control or a 2016 aviation sensor, these
appear as preventive and containment controls that were Absent or Failed, which is the point: the
substrate is new, the failure grammar is not.

### 6.7 Contributing factors

Twenty-five contributing factors were coded across the sample and held out of the safeguard
statistics. The most common types were incentive-structure (9) and a catch-all other (9), followed by
cultural (2), economic (2), and political (2). These are conditions that shaped the incidents
(deployment pressure, cost incentives, political commitments) without themselves being controls; they
contextualize the safeguard failures without inflating them.

## 7. Limitations

This is an exploratory descriptive study on a small, purposively selected sample, and its results
must be read accordingly. Four limitations are structural. First, the sample is selected on realized
harm or credible near-miss, which mechanically shapes several distributions, most obviously the zero
Working preventive controls; such results describe the sample, not AI systems at large. Second, the
evidence-quality rubric favors institutionally documented harms, so the sample skews toward incidents
with official investigations, partly offset but not eliminated by the recency floor; three domains
(scientific research, industrial robotics, consumer finance) received no slots and remain in the
excluded-but-eligible log. Third, coding involves judgment; while the framework, pilot, calibration
decisions, and per-row evidence codings are designed to make that judgment inspectable, we did not
compute a formal inter-rater reliability statistic, and we do not report one rather than invent it.
Fourth, two operationalizations of "omission" exist in the project (a selection-time dominant-mode
label and an analysis-time measure that Absent is the top non-Working state, which holds for 8 of 30
incidents); we keep them separate and never conflate them. Sub-judice cases are provisional. The
dataset is a starting point for scrutiny and extension, not a settled measurement.

## 8. Ethics and responsible-use note

Every incident is drawn from public, primary, or authoritative sources; no private data was used. The
coding is deliberately conservative on contested and unresolved matters, coding disputes as Disputed
or at low confidence rather than resolving them. The dataset should not be used to assign individual
blame; its unit is the safeguard, and its consistent finding is that failure is organizational and
distributed. The two active legal matters are coded as allegations and should be treated as such.

## 9. Conclusion

Asking what happened to the safeguards, rather than whether the system failed, changes the picture of
AI risk. In these 30 incidents the safeguards were mostly not working; the ones that worked were
mostly outside the operator; prevention was missing more often than it malfunctioned; governance
existed but was hollow; a Working detective control did not prevent harm in 11 of the 30 incidents;
and harm arrived through
chains of enabling failures rather than single points. The newest AI systems mostly reproduce these
old fault lines on new substrates, with indirect prompt injection as the notable new surface. None of
this is representative in a statistical sense, and all of it is offered for correction. The dataset,
framework, selection protocol, and code are released so that the coding can be checked and the
sample extended, which is the only way a descriptive artifact like this earns its conclusions.

## 10. Positioning for MATS and safety research

For a MATS-style research program, the Observatory is best read as infrastructure and as a source of
testable hypotheses rather than as a finished empirical result. Three directions follow directly.
First, the safeguard-level coding turns qualitative incident narratives into a structure amenable to
measurement, which is a prerequisite for any quantitative science of AI safeguards; extending the
sample under the frozen protocol would let several of the descriptive patterns here (the external-
ecosystem Working concentration, the detection-response gap, the enabling-relationship dominance) be
tested for stability. Second, the finding that failures are organizational and multi-safeguard, not
model-local, argues for safety work that targets the assurance and human-oversight layers, not only
model alignment; the Bypassed and Inadequate codings are concrete places to intervene. Third, the
agentic and prompt-injection cases isolate the surfaces where the failure grammar is most distinctly
new (indirect prompt injection above all), which is a natural focus for technical safety research. The artifact is designed to make each of these
directions reproducible: the coding manual makes the judgments teachable, the selection protocol makes
extension unbiased, and the validator makes the dataset's integrity checkable by anyone.

---

*Deliverables: (A) `data/` machine-readable dataset; (B) data dictionary; (C) coding manual;
(D) selection methodology; (E) QA report; (F) analysis (`analysis/analysis_results.json`);
(G) tables (`tables/`); (H) figures (`figures/`); (I) technical grounding; (J) this paper;
(K) references; (L) reproducibility; (M) README. All code in `scripts/`.*
