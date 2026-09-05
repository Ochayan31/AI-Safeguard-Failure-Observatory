// Build the AI Safeguard Failure Observatory research paper as a .docx
// Publication-quality: title, abstract, numbered sections, 6 tables, 6 embedded figures, references.
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType, ImageRun, PageBreak
} = require('docx');

const ROOT = path.join(__dirname, '..');
const FIG = path.join(ROOT, 'figures');
const OUT = path.join(ROOT, 'paper', 'AI_Safeguard_Failure_Observatory_v1.0_paper.docx');

const INK = '111111', MUT = '555555', ACC = '1F3A5F', HDR = 'E8EDF3', RULE = 'CCCCCC';
const FONT = 'Calibri', SERIF = 'Georgia';

// ---------- helpers ----------
function h1(text, num) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 320, after: 140 },
    children: [new TextRun({ text: (num ? num + '  ' : '') + text, bold: true, size: 30, color: ACC, font: FONT })],
  });
}
function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 200, after: 90 },
    children: [new TextRun({ text, bold: true, size: 24, color: INK, font: FONT })],
  });
}
function body(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 140, line: 276 },
    alignment: AlignmentType.JUSTIFIED,
    children: parseRuns(text, opts),
  });
}
// simple **bold** and *italic* parser
function parseRuns(text, opts = {}) {
  const runs = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*)/g;
  let last = 0, m;
  const base = { size: opts.size || 21, color: opts.color || INK, font: opts.font || SERIF };
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) runs.push(new TextRun({ text: text.slice(last, m.index), ...base }));
    const tok = m[0];
    if (tok.startsWith('**')) runs.push(new TextRun({ text: tok.slice(2, -2), bold: true, ...base }));
    else runs.push(new TextRun({ text: tok.slice(1, -1), italics: true, ...base }));
    last = re.lastIndex;
  }
  if (last < text.length) runs.push(new TextRun({ text: text.slice(last), ...base }));
  return runs.length ? runs : [new TextRun({ text, ...base })];
}
function caption(text) {
  return new Paragraph({
    spacing: { before: 60, after: 200 },
    children: parseRuns(text, { size: 17, color: MUT, font: FONT }),
  });
}
function figure(file, capText, widthPx = 560) {
  const data = fs.readFileSync(path.join(FIG, file));
  return [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 120, after: 40 },
      children: [new ImageRun({ type: 'png', data, transformation: { width: widthPx, height: Math.round(widthPx * 0.55) } })],
    }),
    caption(capText),
  ];
}
function tbl(headers, rows, colW) {
  const total = colW.reduce((a, b) => a + b, 0);
  const mkCell = (txt, i, isHead, boldRow) => new TableCell({
    width: { size: colW[i], type: WidthType.DXA },
    shading: isHead ? { type: ShadingType.CLEAR, fill: HDR, color: 'auto' } : undefined,
    margins: { top: 40, bottom: 40, left: 80, right: 80 },
    children: [new Paragraph({
      alignment: i === 0 ? AlignmentType.LEFT : AlignmentType.LEFT,
      children: [new TextRun({ text: String(txt), bold: isHead || boldRow, size: 16, font: FONT, color: INK })],
    })],
  });
  const border = { style: BorderStyle.SINGLE, size: 2, color: RULE };
  const borders = { top: border, bottom: border, left: border, right: border, insideHorizontal: border, insideVertical: border };
  const trs = [new TableRow({ tableHeader: true, children: headers.map((h, i) => mkCell(h, i, true)) })];
  for (const r of rows) {
    const boldRow = /TOTAL/i.test(String(r[0]));
    trs.push(new TableRow({ children: r.map((c, i) => mkCell(c, i, false, boldRow)) }));
  }
  return new Table({ columnWidths: colW, width: { size: total, type: WidthType.DXA }, borders, rows: trs });
}
function tcap(text) {
  return new Paragraph({ spacing: { before: 60, after: 220 }, children: parseRuns(text, { size: 17, color: MUT, font: FONT }) });
}
function spacer() { return new Paragraph({ spacing: { after: 80 }, children: [] }); }

// ---------- content ----------
const children = [];

// Title block
children.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { before: 240, after: 80 },
  children: [new TextRun({ text: 'How AI and Algorithmic Safeguards Fail', bold: true, size: 40, color: ACC, font: FONT })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 160 },
  children: [new TextRun({ text: 'A Relational Coding of 30 Real-World Incidents', size: 26, color: INK, font: FONT })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 40 },
  children: [new TextRun({ text: 'The AI Safeguard Failure Observatory', bold: true, size: 22, color: INK, font: FONT })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 240 },
  children: [new TextRun({ text: 'Dataset v1.0 (frozen 2026-09-05)  ·  n = 30 incidents  ·  Exploratory descriptive study', size: 18, color: MUT, font: FONT })],
}));

// Abstract
children.push(h1('Abstract'));
children.push(body('Public discussion of AI risk tends to ask whether a system failed. This study asks a different question: when an AI or algorithmic system contributes to harm, what happened to the safeguards that were supposed to prevent it? We built a relational dataset of 30 real-world incidents (2010-2025) spanning autonomous vehicles, welfare automation, healthcare, criminal justice, consumer chatbots, agentic LLM tools, finance, hiring, content moderation, and more. For each incident we coded every identifiable safeguard as a structured interaction (its system layer, its control function, its observed state at the time of the incident, the evidentiary basis for that coding, and its causal role) and coded the typed relationships between safeguards. The result is 202 safeguard-interaction rows (181 present at incident time), 84 inter-safeguard relationships, and 25 contributing factors, each traceable to primary or authoritative sources.'));
children.push(body('The findings are descriptive and exploratory, not statistically representative. Across the 181 incident-time safeguards, 75.7% were non-functional (Absent, Failed, Inadequate, Bypassed, or Disabled) and only 20.4% were Working; of those Working, 70.3% sat in the external-ecosystem layer (journalists, regulators, litigation, researchers) rather than inside the operator’s own controls. Prevention was the most-Absent function; governance controls, when present, were most often Inadequate rather than missing. In 11 of 30 incidents a detective control was Working at incident time yet harm still occurred, suggesting (within this sample only) that detection can be insufficient where downstream escalation, intervention, and authority-to-act are weak. Failures were consistently multi-safeguard (mean 2.8 typed relationships per incident, every incident at least two), and the dominant relationship type was enabling (58.3%), the data-level signature of Reason’s Swiss-cheese hole alignment. Primary responsibility was attributed to organizational rather than model-level causes in 18 of 30 incidents. The newest generative and agentic systems (8 of 30) fail largely along old fault lines, with a small but real set of new attack surfaces at the LLM/agentic boundary (indirect prompt injection). We release the dataset, coding manual, selection protocol, and analysis code so the coding can be scrutinized, corrected, and extended.'));
children.push(new Paragraph({ spacing: { after: 200 }, children: [
  new TextRun({ text: 'Keywords: ', bold: true, size: 19, font: FONT, color: INK }),
  new TextRun({ text: 'AI safety; algorithmic accountability; safeguard failure; defense-in-depth; sociotechnical systems; incident analysis; automation bias; prompt injection; AI incident dataset.', size: 19, italics: true, font: SERIF, color: MUT }),
]}));

// 1 Introduction
children.push(h1('Introduction', '1.'));
children.push(body('The catalog of AI and algorithmic harms is now large enough that individual cases no longer surprise. What remains poorly understood is systematic: across many incidents, in what state were the safeguards? A safeguard can be entirely absent, present but poorly designed, present but deliberately switched off, present but circumvented by a rushed human reviewer, or working exactly as intended and still insufficient. These are different failures with different remedies, and lumping them together as “the AI failed” obscures where intervention would actually help.'));
children.push(body('This study treats the safeguard, not the incident, as the primary unit of interest, and asks three questions. First, what is the distribution of safeguard states when AI or algorithmic systems contribute to harm? Second, how do safeguards relate to one another in a failure, and can those relationships be coded reliably rather than described anecdotally? Third, do the newest AI systems (generative and agentic) fail in new ways, or do they recapitulate old failure mechanisms on new substrates?'));
children.push(body('We answer these with a purpose-built coding framework (the Control-Incident-Relationship, or CIR, framework) applied to a deliberately, reproducibly selected sample of 30 incidents. The contribution is not a new theory of failure; it is a disciplined, transparent, safeguard-level dataset that lets existing safety theory be checked against a mixed AI/algorithmic sample, and that others can correct and build on.'));
children.push(body('We state the central caveat up front. With n = 30, and a sample selected on the occurrence of realized harm or credible near-miss, nothing here is statistically representative of AI systems in general, and several distributions are shaped by that selection. Every quantitative claim below carries its denominator and its unit of analysis, and Section 7 is devoted to the limitations this design imposes.'));

// 2 Related work
children.push(h1('Related work and technical grounding', '2.'));
children.push(body('The mechanisms this dataset surfaces are, with one exception, well established. Reason’s model of organizational accidents [1,2] describes layered defenses that fail when latent holes align, which is precisely what the Observatory’s dominant enabling relationships encode. Perrow’s normal-accident theory [3] and Leveson’s systems-theoretic model [6] explain why, in tightly coupled and complex sociotechnical systems, single barriers are insufficient and causation is distributed rather than component-local. Rasmussen’s migration-to-the-boundary model [4] and the High Reliability Organizations literature [5] account for the temporal drift by which governance becomes present in form but hollow in substance. Human-factors work on automation bias and complacency [7,8] and on alarm fatigue [9] explains the recurring pattern of detection that works while response fails. The algorithmic-fairness literature [10,11,12] supplies the mechanism for the incidents that fail by disparate impact rather than malfunction. AI-specific safety framings [16,17,19] and the internal-audit literature [18] name the model-layer hazards and the assurance steps involved. Prompt-injection research [20] and the OWASP LLM risk list [21] cover the clearest new surface, the LLM/agentic boundary. Finally, existing incident repositories [13,14,15] catalog incidents; the Observatory is complementary, adding the safeguard-level relational coding those repositories do not systematically capture.'));

// 3 Framework
children.push(h1('Framework (CIR)', '3.'));
children.push(body('The CIR framework (v0.3) models each incident as a set of safeguard interactions plus a set of typed relationships between them, with contributing factors held in a separate table so they never contaminate safeguard statistics. Three design decisions do most of the analytical work.'));
children.push(body('First, eligibility is set at “the AI or algorithmic system materially contributed to the harm, attempted harm, or credible near-miss,” and the system’s causal contribution is coded separately (ai_causal_contribution) from where blame was attributed (attributed_primary_cause). This keeps causal weight and responsibility distinct, which matters because they frequently diverge: the AI was a major contributor in 26 of 30 incidents, yet primary responsibility was attributed to organizational causes in 18.'));
children.push(body('Second, the observed state of a safeguard is separated from the evidentiary basis for that coding. A safeguard is coded Absent only when there is positive evidence it should have existed and did not (the “evidentiary fence”); where absence cannot be evidenced, the safeguard is coded Unknown, with an optional suspected_absent flag that is explicitly barred from ever being counted as Absent. This prevents the dataset from inventing counterfactual controls, at the cost of some conservatism.'));
children.push(body('Third, relationships are typed (enabling, masking, temporal-precedence, common-cause, and others) with an explicit rule that temporal precedence alone can never justify a causal relationship. This lets the dataset represent structure without overclaiming causation.'));
children.push(body('The state vocabulary distinguishes Working, Inadequate, Failed, Bypassed, Disabled, Absent, Disputed, and Unknown. The distinction between Bypassed (present but circumvented, including hollow rubber-stamp review), Disabled (deliberately switched off), and Absent (never existed) is central to the findings and was calibrated on the pilot and Batch-1 incidents.'));

// 4 Selection
children.push(h1('Selection methodology', '4.'));
children.push(body('The sample was drawn by a pre-registered, reproducible protocol designed to prevent selection favorable to the framework. A discovery pool of 108 candidates was assembled by a fixed-source sweep, separate from the coded sample. Eligibility screening removed cases with no AI or algorithmic decision system in the causal chain (the same principle that excludes Therac-25 and, at coding, the 2025 Iberian blackout). From the eligible pool, cases were selected by a frozen “Hybrid E then R” rule: within predefined strata, cases were ranked by a pre-specified evidence-quality rubric, and the highest-ranked were taken up to quota, with a seeded random draw (seed AISFO-2026-08-24) only for ties at the selection boundary. Evidence quality was explicitly barred from incorporating whether a case looked interesting, contained many safeguards, or supported any anticipated finding. Selection preceded all outcome and relational analysis.'));
children.push(body('Frozen floors ensured variation without cherry-picking: at least 8 omission-dominated cases, at least 5 generative-era cases, and at least 2 agentic cases, with per-domain caps of 5. The locked sample satisfies every floor and cap. One case (the Iberian blackout) was found ineligible during coding and deterministically replaced by re-running the selection script with it marked ineligible; all other 29 held. This is the only change to the locked sample and is logged.'));
children.push(body('The resulting 30 incidents span 13 domains (autonomous-vehicle 4, government-benefits 4, security-cyber 3, healthcare-clinical 3, consumer-chatbot 3, and eight further domains with 1-2 each), three system types (confirmed-ML 17, algorithmic-nonML 8, probable-ML 5), and two eras (legacy 22, generative 8), with 14 discrete events, 14 systemic programs, and 2 bounded episodes. Table 1 lists the full sample.'));

// Table 1
children.push(h2('Table 1. The 30 coded incidents'));
const t1head = ['incident_id','domain','system_type','era','outcome','scope','ai_causal','conf','n'];
const t1 = [
['2023-cruise-drag-sf','autonomous-vehicle','confirmed-ML','legacy','realized-harm','discrete-event','major','high','8'],
['2015-2020-au-robodebt','government-benefits','algorithmic-nonML','legacy','realized-harm','systemic-program','major','high','8'],
['2013-2019-optum-impact-pro','healthcare-clinical','probable-ML','legacy','realized-harm','systemic-program','major','high','7'],
['2022-air-canada-chatbot','consumer-chatbot','probable-ML','genai','realized-harm','discrete-event','major','high','7'],
['2025-gemini-cli-file-destruction','enterprise-agent','confirmed-ML','genai','realized-harm','discrete-event','major','medium','6'],
['2018-2019-boeing-737max-mcas','other','algorithmic-nonML','legacy','realized-harm','bounded-episode','major','high','9'],
['2013-2021-nl-toeslagen','government-benefits','probable-ML','legacy','realized-harm','systemic-program','major','medium','9'],
['2020-williams-detroit-facerec','criminal-justice','confirmed-ML','legacy','realized-harm','discrete-event','major','high','8'],
['2023-mata-avianca-chatgpt','other','confirmed-ML','genai','realized-harm','discrete-event','major','high','6'],
['2025-echoleak-m365-copilot','security-cyber','confirmed-ML','genai','near-miss','discrete-event','major','medium','7'],
['2016-tesla-autopilot-williston','autonomous-vehicle','confirmed-ML','legacy','realized-harm','discrete-event','major','high','6'],
['2016-compas-recidivism','criminal-justice','algorithmic-nonML','legacy','realized-harm','systemic-program','disputed','medium','6'],
['2016-microsoft-tay','consumer-chatbot','confirmed-ML','legacy','realized-harm','discrete-event','major','high','6'],
['2020-clearview-ai-scraping','security-cyber','confirmed-ML','legacy','realized-harm','systemic-program','major','high','7'],
['2020-uk-ofqual-alevel','education','algorithmic-nonML','legacy','realized-harm','bounded-episode','major','high','7'],
['2013-2015-us-mi-midas','government-benefits','algorithmic-nonML','legacy','realized-harm','systemic-program','major','high','8'],
['2024-2025-raine-openai','consumer-chatbot','confirmed-ML','genai','realized-harm','discrete-event','disputed','low','6'],
['2021-facebook-files-instagram','content-moderation','confirmed-ML','legacy','realized-harm','systemic-program','contrib-non-nec','medium','6'],
['2015-vw-dieselgate','environmental','algorithmic-nonML','legacy','realized-harm','systemic-program','major','high','7'],
['2020-pulse-oximeter-bias','healthcare-clinical','algorithmic-nonML','legacy','realized-harm','systemic-program','major','high','5'],
['2010-flash-crash','finance-trading','algorithmic-nonML','legacy','realized-harm','discrete-event','major','high','8'],
['2021-zillow-offers','finance-trading','probable-ML','legacy','realized-harm','discrete-event','major','high','6'],
['2018-ibm-watson-oncology','healthcare-clinical','confirmed-ML','legacy','realized-harm','systemic-program','major','medium','7'],
['2023-2025-mobley-workday','hiring-HR','probable-ML','genai','realized-harm','systemic-program','disputed','low','6'],
['2024-gemini-image-generation','content-moderation','confirmed-ML','genai','realized-harm','discrete-event','major','high','7'],
['2018-tesla-autopilot-mountain-view','autonomous-vehicle','confirmed-ML','legacy','realized-harm','discrete-event','major','high','7'],
['2023-tesla-autopilot-recall','autonomous-vehicle','confirmed-ML','legacy','realized-harm','systemic-program','major','high','4'],
['2017-2021-rotterdam-welfare','government-benefits','confirmed-ML','legacy','realized-harm','systemic-program','major','high','7'],
['2014-erater-babel-aes','education','confirmed-ML','legacy','realized-harm','systemic-program','major','high','5'],
['2025-amazon-q-injection','security-cyber','confirmed-ML','genai','near-miss','discrete-event','major','medium','6'],
];
children.push(tbl(t1head, t1, [2140,1500,1400,620,1180,1360,1120,560,360]));
children.push(tcap('Table 1. The 30 coded incidents. Unit of analysis: incident. (“major” = major-contributor; “contrib-non-nec” = contributory-non-necessary.)'));

// 5 Coding & QA
children.push(h1('Coding process and quality assurance', '5.'));
children.push(body('The 30 incidents were coded in six batches of five, following a pilot of three deliberately different cases (one high-evidence, one messy sociotechnical, one technically complex) whose purpose was to surface every field that failed, required judgment, or produced ambiguity before the full sample was touched. Two calibration decisions from Batch 1 were locked and applied sample-wide: deliberate suppression of a control is coded Disabled rather than Bypassed, and controls representing one underlying safeguard are coded as one row rather than split. Twelve coding calls were flagged for scrutiny and individually adjudicated against their primary sources.'));
children.push(body('The frozen dataset passes an automated integrity validator with zero errors: referential integrity across all tables, ID uniqueness, controlled-vocabulary validity, and a set of denominator-contamination guards (suspected_absent only within Unknown and never counted as Absent; inadequacy_type only where Inadequate; added-after rows flagged for exclusion from incident-time distributions; contributing factors held out of safeguard statistics). Evidentiary quality is recorded per row: of 202 safeguard rows, 146 are confirmed-authoritative and 8 are disputed; 134 are coded at high confidence and 13 at low. Sub-judice cases (Raine v. OpenAI, Mobley v. Workday) are coded conservatively at low confidence and disputed status and are not adjudicated by the coding.'));

// 6 Results
children.push(h1('Results', '6.'));
children.push(body('All distributions below use explicit denominators. State, function, and layer distributions use the 181 incident-time safeguards (the 21 added-after rows are excluded, since a control added in response to an incident cannot describe the incident’s own defenses). Relationship statistics use the 84 coded relationships; incident-level statistics use the 30 incidents.'));

children.push(h2('6.1  Most safeguards were not functioning, and most that were sat outside the operator'));
children.push(body('Of 181 incident-time safeguards, 137 (75.7%) were non-functional and 37 (20.4%) were Working (Figure 1; Table 2). The single most common state was Absent (44), followed by Inadequate (41), Working (37), Failed (32), Bypassed (15), Unknown (6), Disabled (5), and Disputed (1). The Working share is not distributed evenly across the system: of the 37 Working safeguards, 26 (70.3%) sit in the external-ecosystem layer, meaning the control that “worked” was frequently a journalist, a regulator, a court, or an academic surfacing the harm after the fact, rather than any control the operator built. This is a sobering pattern: in this sample, the safeguards most often found Working were external to the operator. It should be read with its selection effect in mind, because incidents partly enter the sample when external actors surface them, which inflates the external-ecosystem Working share; the claim is about where Working safeguards concentrated in these 30 cases, not an unconditional ranking of which safeguards are most reliable.'));
figure('fig1_state_distribution.png', 'Figure 1. Observed state of AI/algorithmic safeguards at incident time (denominator: 181 incident-time safeguards; 21 added-after rows excluded).').forEach(p => children.push(p));

// Table 2
children.push(h2('Table 2. Observed state of incident-time safeguards'));
children.push(tbl(['observed_state','n','% of incident-time safeguards'],
[['Working','37','20.4%'],['Inadequate','41','22.7%'],['Failed','32','17.7%'],['Bypassed','15','8.3%'],['Disabled','5','2.8%'],['Absent','44','24.3%'],['Unknown','6','3.3%'],['Disputed','1','0.6%'],['TOTAL','181','100%']],
[3600,1400,4240]));
children.push(tcap('Table 2. Denominator: 181 incident-time safeguards. Non-functional = Absent + Failed + Inadequate + Bypassed + Disabled = 137 (75.7%); Unknown and Disputed (7 rows) are excluded from “non-functional.”'));

children.push(h2('6.2  Prevention is most often Absent; governance is most often Inadequate'));
children.push(body('Broken out by control function (Figure 2; Table 3), the two most-coded functions fail in characteristically different ways. Preventive controls (51 rows) are dominated by Absent (21) and contain zero Working rows at incident time. That zero is partly definitional and we flag it as such: in a sample selected on realized harm, prevention by construction did not fully hold, so this is not a discovered effect so much as a property of the sample. What is informative is the composition of preventive failure, which is more Absent (structurally missing) than Failed (present but malfunctioning). Assurance-governance controls (30 rows), by contrast, are dominated by Inadequate (13) rather than Absent (7): organizations frequently had validation, impact-assessment, disclosure, or certification processes that were present but hollow, consistent with drift-to-the-boundary [4] and with governance performed as ritual [18].'));
figure('fig2_state_by_function.png', 'Figure 2. Observed state by control function; shares within each function, incident-time.').forEach(p => children.push(p));

// Table 3
children.push(h2('Table 3. Observed state by control function'));
children.push(tbl(['function','n','Work','Inad','Fail','Byp','Disb','Abs','Unk','Disp'],
[['preventive','51','0','6','10','6','3','21','4','1'],
['detective','46','13','8','10','7','1','6','1','0'],
['containment','29','7','10','2','1','0','8','1','0'],
['recovery','25','15','4','4','0','0','2','0','0'],
['assurance-governance','30','2','13','6','1','1','7','0','0']],
[2600,560,620,620,620,620,620,620,620,620]));
children.push(tcap('Table 3. Counts. Denominator per row = row n (incident-time). Row totals sum to 181.'));

children.push(h2('6.3  Detection was frequently insufficient to prevent harm'));
children.push(body('In this sample, detection was frequently insufficient to prevent harm: 11 of 30 incidents involved at least one detective safeguard that was Working at incident time despite harm subsequently occurring. The system, or someone in it, noticed, and harm followed anyway. Detection was also far from always intact elsewhere in the sample (32 of 46 detective controls were themselves non-functional, with a further one Unknown), so this is not a claim that detection never fails; the point is the narrower one that, in these 11 cases, a Working detective control did not suffice. Read cautiously, and only of these 30 incidents, this suggests that detection alone may be insufficient where the escalation, intervention, or authority-to-act mechanisms downstream of it are weak, which is consistent with the human-factors record on alarm fatigue and automation complacency [7,8,9]. The Bypassed state (15 rows, 6 of them in the human-operator layer) is the data-level signature of hollow oversight: a human or process nominally in the loop but structurally prevented from meaningful engagement.'));
figure('fig6_working_share_by_function.png', 'Figure 6. Share of safeguards coded Working, by control function, incident-time.').forEach(p => children.push(p));

children.push(h2('6.4  Failures are multi-safeguard, and the dominant relationship is enabling'));
children.push(body('No incident failed through a single safeguard. Every incident carries at least two typed relationships (mean 2.8, range 2-5; 84 total). The dominant type is enabling (49 of 84, 58.3%), where one safeguard’s failure opens the path for the next, followed by temporal-precedence (18, 21.4%), common-cause (10, 11.9%), and masking (7, 8.3%) (Figure 4; Table 5). The predominance of enabling relationships is the Swiss-cheese alignment mechanism [1,2] expressed as data: harm arrives not because one barrier failed but because the failure of one barrier removed the protection that would have caught the next. We report enabling as a coded structural relationship, not as proof of counterfactual causation; the framework separates it explicitly from temporal-precedence, which encodes sequence alone.'));
figure('fig4_relationship_types.png', 'Figure 4. Types of inter-safeguard relationship (denominator: 84 coded relationships).').forEach(p => children.push(p));

// Table 5
children.push(h2('Table 5. Types of inter-safeguard relationship'));
children.push(tbl(['relationship_type','n','% of relationships'],
[['enabling','49','58.3%'],['temporal-precedence','18','21.4%'],['common-cause','10','11.9%'],['masking','7','8.3%'],['TOTAL','84','100%']],
[3600,1400,4240]));
children.push(tcap('Table 5. Denominator: 84 coded relationships. Unit: directed relationship.'));

children.push(h2('6.5  Blame lands on organizations, not models'));
children.push(body('At the incident level, the AI or algorithmic system was a major causal contributor in 26 of 30 incidents (Figure 5), yet primary responsibility was attributed to organizational causes in 18 of 30, to multiple causes in 6, to the AI system itself in only 2, to a human operator in 1, and disputed in 3. Consistent with this, the organizational-process layer carries the most Failed rows (16), while the model layer is the least-coded layer overall (14 of 181; Figure 3; Table 4). This is not a claim that models are reliable: the 14 model-layer controls were, where present, uniformly non-functional (0 Working). The point is narrower and about where safeguards and blame sit: few safeguards live at the model layer, and responsibility was attributed organizationally far more often than to the AI system. A purely model-centric reading of AI risk is therefore not well supported by this sample; the failures are predominantly organizational and sociotechnical [6].'));
figure('fig3_state_by_layer.png', 'Figure 3. Observed state by system layer, incident-time.').forEach(p => children.push(p));

// Table 4
children.push(h2('Table 4. Observed state by system layer'));
children.push(tbl(['layer','n','Work','Inad','Fail','Byp','Disb','Abs','Unk','Disp'],
[['model','14','0','2','5','1','0','5','0','1'],
['application','43','2','13','6','1','1','17','3','0'],
['infrastructure-environment','8','1','2','0','1','0','4','0','0'],
['human-operator','26','3','7','2','6','2','5','1','0'],
['organizational-process','50','5','11','16','3','2','11','2','0'],
['external-ecosystem','40','26','6','3','3','0','2','0','0']],
[2600,560,620,620,620,620,620,620,620,620]));
children.push(tcap('Table 4. Counts (incident-time). Row totals sum to 181.'));
figure('fig5_sample_composition.png', 'Figure 5. Composition of the coded sample (n=30 incidents): system type, outcome class, era, and AI causal contribution.').forEach(p => children.push(p));

children.push(h2('6.6  New systems, mostly old fault lines'));
children.push(body('The eight generative-era incidents (three of them agentic) fail largely along mechanisms already in the framework: absent input validation, missing privilege boundaries, inadequate testing. The clearest new attack surface is indirect prompt injection, where untrusted data doubles as instructions and hijacks an LLM application’s control flow (EchoLeak, Amazon Q, the Gemini CLI file-destruction case) [20,21]; a second candidate for genuine novelty is LLM confabulation presented as authoritative output (the fabricated legal citations in Mata v. Avianca, the invented policy in the Air Canada case), which has no clean pre-2022 analogue. Coded in the same vocabulary as a 2010 trading control or a 2016 aviation sensor, these appear as preventive and containment controls that were Absent or Failed, which is the point: the substrate is new, the failure grammar is not.'));

children.push(h2('6.7  Contributing factors'));
children.push(body('Twenty-five contributing factors were coded across the sample and held out of the safeguard statistics. The most common types were incentive-structure (9) and a catch-all other (9), followed by cultural (2), economic (2), and political (2). These are conditions that shaped the incidents (deployment pressure, cost incentives, political commitments) without themselves being controls; they contextualize the safeguard failures without inflating them.'));

// Table 6
children.push(h2('Table 6. Descriptive headline findings'));
children.push(tbl(['finding','value','rate'],
[['Non-functional safeguards at incident time','137 / 181 safeguards','75.7%'],
['Safeguards coded Working','37 / 181','20.4%'],
['  of which external-ecosystem layer','26 / 37 Working','70.3%'],
['Incidents with ≥1 Absent safeguard','25 / 30 incidents','83.3%'],
['Omission-dominated incidents','8 / 30 incidents','26.7%'],
['Detective control Working yet realized harm','11 / 30 incidents','36.7%'],
['Preventive controls coded Working','0 / 51 preventive','0.0%'],
['assurance-governance coded Inadequate','13 / 30','43.3%'],
['Relationships per incident (mean; all ≥2)','2.8','min 2 / max 5']],
[4400,2440,1400]));
children.push(tcap('Table 6. Descriptive headline findings, each with explicit denominator. n = 30 incidents; exploratory, not representative.'));

// 7 Limitations
children.push(h1('Limitations', '7.'));
children.push(body('This is an exploratory descriptive study on a small, purposively selected sample, and its results must be read accordingly. Four limitations are structural. First, the sample is selected on realized harm or credible near-miss, which mechanically shapes several distributions, most obviously the zero Working preventive controls; such results describe the sample, not AI systems at large. Second, the evidence-quality rubric favors institutionally documented harms, so the sample skews toward incidents with official investigations, partly offset but not eliminated by the recency floor; three domains (scientific research, industrial robotics, consumer finance) received no slots. Third, coding involves judgment; while the framework, pilot, calibration decisions, and per-row evidence codings are designed to make that judgment inspectable, we did not compute a formal inter-rater reliability statistic, and we do not report one rather than invent it. Fourth, two operationalizations of “omission” exist in the project (a selection-time dominant-mode label and an analysis-time measure that Absent is the top non-Working state, which holds for 8 of 30 incidents); we keep them separate and never conflate them. Retrospective reconstruction from public documentation cannot recover controls that were never documented, and causal claims are limited to what authoritative sources support. The dataset is a starting point for scrutiny and extension, not a settled measurement.'));

// 8 Ethics
children.push(h1('Ethics and responsible-use note', '8.'));
children.push(body('Every incident is drawn from public, primary, or authoritative sources; no private data was used. The coding is deliberately conservative on contested and unresolved matters, coding disputes as Disputed or at low confidence rather than resolving them. The dataset should not be used to assign individual blame; its unit is the safeguard, and its consistent finding is that failure is organizational and distributed. The two active legal matters are coded as allegations and should be treated as such.'));

// 9 Implications
children.push(h1('Implications', '9.'));
children.push(body('If these patterns hold under extension, the practical implication is that safeguard investment concentrated at the model layer addresses the layer that carries the fewest controls in this sample, while the assurance-governance and human-operator layers, where Inadequate and Bypassed concentrate, are where controls most often existed but failed to perform. The enabling-relationship dominance implies that independent-barrier reasoning understates real risk, because barriers in these incidents were not independent; the failure of one routinely removed the protection of the next. And the detection finding implies that adding more detection is unlikely to help where the downstream escalation and authority-to-act are the weak links. These are hypotheses the dataset generates, not conclusions it proves.'));

// 10 Conclusion
children.push(h1('Conclusion', '10.'));
children.push(body('Asking what happened to the safeguards, rather than whether the system failed, changes the picture of AI risk. In these 30 incidents the safeguards were mostly not working; the ones that worked were mostly outside the operator; prevention was missing more often than it malfunctioned; governance existed but was hollow; a Working detective control did not prevent harm in 11 of the 30 incidents; and harm arrived through chains of enabling failures rather than single points. The newest AI systems mostly reproduce these old fault lines on new substrates, with indirect prompt injection as the notable new surface. None of this is representative in a statistical sense, and all of it is offered for correction. The dataset, framework, selection protocol, and code are released so that the coding can be checked and the sample extended, which is the only way a descriptive artifact like this earns its conclusions.'));

// 11 MATS
children.push(h1('Positioning for MATS and safety research', '11.'));
children.push(body('For a MATS-style research program, the Observatory is best read as infrastructure and as a source of testable hypotheses rather than as a finished empirical result. Three directions follow directly. First, the safeguard-level coding turns qualitative incident narratives into a structure amenable to measurement, which is a prerequisite for any quantitative science of AI safeguards; extending the sample under the frozen protocol would let several of the descriptive patterns here (the external-ecosystem Working concentration, the detection-response gap, the enabling-relationship dominance) be tested for stability. Second, the finding that failures are organizational and multi-safeguard, not model-local, argues for safety work that targets the assurance and human-oversight layers, not only model alignment; the Bypassed and Inadequate codings are concrete places to intervene. Third, the agentic and prompt-injection cases isolate the surfaces where the failure grammar is most distinctly new (indirect prompt injection above all), which is a natural focus for technical safety research. The artifact is designed to make each of these directions reproducible: the coding manual makes the judgments teachable, the selection protocol makes extension unbiased, and the validator makes the dataset’s integrity checkable by anyone.'));

// References
children.push(h1('References', '12.'));
const refs = [
'Reason, J. (1990). Human Error. Cambridge University Press. DOI: 10.1017/CBO9781139062367.',
'Reason, J. (1997). Managing the Risks of Organizational Accidents. Ashgate.',
'Perrow, C. (1984/1999). Normal Accidents: Living with High-Risk Technologies. Basic Books (1984); Princeton University Press revised edition (1999).',
'Rasmussen, J. (1997). Risk management in a dynamic society: a modelling problem. Safety Science, 27(2-3), 183-213. DOI: 10.1016/S0925-7535(97)00052-0.',
'Weick, K. E., & Sutcliffe, K. M. (2015). Managing the Unexpected (3rd ed.). Wiley.',
'Leveson, N. G. (2011). Engineering a Safer World: Systems Thinking Applied to Safety. MIT Press (open access).',
'Parasuraman, R., & Riley, V. (1997). Humans and automation: Use, misuse, disuse, abuse. Human Factors, 39(2), 230-253. DOI: 10.1518/001872097778543886.',
'Parasuraman, R., & Manzey, D. H. (2010). Complacency and bias in human use of automation. Human Factors, 52(3), 381-410. DOI: 10.1177/0018720810376055.',
'The Joint Commission (2013). Sentinel Event Alert, Issue 50: Medical device alarm safety in hospitals.',
'Obermeyer, Z., Powers, B., Vogeli, C., & Mullainathan, S. (2019). Dissecting racial bias in an algorithm used to manage the health of populations. Science, 366(6464), 447-453. DOI: 10.1126/science.aax2342.',
'Angwin, J., Larson, J., Mattu, S., & Kirchner, L. (2016). Machine Bias. ProPublica, May 23, 2016.',
'Dressel, J., & Farid, H. (2018). The accuracy, fairness, and limits of predicting recidivism. Science Advances, 4(1), eaao5580. DOI: 10.1126/sciadv.aao5580.',
'McGregor, S. (2021). Preventing repeated real world AI failures by cataloging incidents: The AI Incident Database. AAAI, 35(17), 15458-15463. (arXiv:2011.08512.)',
'OECD. OECD AI Incidents and Hazards Monitor (AIM). OECD.AI Policy Observatory. https://oecd.ai/en/incidents.',
'AIAAIC. AIAAIC Repository. https://www.aiaaic.org/aiaaic-repository.',
'Amodei, D., et al. (2016). Concrete Problems in AI Safety. arXiv:1606.06565.',
'Hendrycks, D., Carlini, N., Schulman, J., & Steinhardt, J. (2021). Unsolved Problems in ML Safety. arXiv:2109.13916.',
'Raji, I. D., et al. (2020). Closing the AI accountability gap. FAccT ’20, 33-44. DOI: 10.1145/3351095.3372873.',
'Weidinger, L., et al. (2022). Taxonomy of risks posed by language models. FAccT ’22, 214-229. DOI: 10.1145/3531146.3533088.',
'Greshake, K., et al. (2023). Not what you’ve signed up for: indirect prompt injection. AISec ’23, 79-90. DOI: 10.1145/3605764.3623985. (arXiv:2302.12173.)',
'OWASP Gen AI Security Project (2025). OWASP Top 10 for LLM Applications (2025).',
'U.S. House Committee on Transportation and Infrastructure (2020). Final Committee Report: The Design, Development & Certification of the Boeing 737 MAX.',
'Komite Nasional Keselamatan Transportasi (KNKT) (2019). Aircraft Accident Investigation Report: Lion Air Boeing 737-8 (MAX), PK-LQP (KNKT.18.10.35.04).',
'Royal Commission into the Robodebt Scheme (2023). Report of the Royal Commission into the Robodebt Scheme. Commonwealth of Australia.',
];
refs.forEach((r, i) => children.push(new Paragraph({
  spacing: { after: 70 }, indent: { left: 360, hanging: 360 },
  children: [new TextRun({ text: (i+1) + '. ', bold: true, size: 18, font: FONT, color: INK }),
             new TextRun({ text: r, size: 18, font: SERIF, color: INK })],
})));
children.push(new Paragraph({ spacing: { before: 120 }, children: [new TextRun({ text: 'Author-choice notes: ref 3 exists in a 1984 and a 1999 edition; ref 19 exists as a 2021 arXiv report and the 2022 peer-reviewed FAccT version cited here. Per-incident primary sources (52) are in data/sources.csv.', italics: true, size: 17, font: SERIF, color: MUT })] }));

// ---------- assemble ----------
const doc = new Document({
  creator: 'AI Safeguard Failure Observatory',
  title: 'How AI and Algorithmic Safeguards Fail',
  styles: { default: { document: { run: { font: SERIF, size: 21, color: INK } } } },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1180, bottom: 1180, left: 1440, right: 1440 } } },
    children,
  }],
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync(OUT, buf); console.log('WROTE', OUT, buf.length, 'bytes'); });
