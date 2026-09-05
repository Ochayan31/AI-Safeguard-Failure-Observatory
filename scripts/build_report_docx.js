// Final production/hand-off report as .docx (sections A, C-N; B is the separate paper docx).
const fs = require('fs'), path = require('path');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType } = require('docx');
const ROOT = path.join(__dirname, '..');
const OUT = path.join(ROOT, 'paper', 'AI_Safeguard_Failure_Observatory_v1.0_production_report.docx');
const INK='111111', MUT='555555', ACC='1F3A5F', HDR='E8EDF3', RULE='CCCCCC', MONO='F4F4F2';
const FONT='Calibri', SERIF='Georgia', CODE='Consolas';

function h1(t,n){return new Paragraph({heading:HeadingLevel.HEADING_1,spacing:{before:300,after:130},children:[new TextRun({text:(n?n+'  ':'')+t,bold:true,size:28,color:ACC,font:FONT})]});}
function h2(t){return new Paragraph({heading:HeadingLevel.HEADING_2,spacing:{before:180,after:80},children:[new TextRun({text:t,bold:true,size:23,color:INK,font:FONT})]});}
function p(t){return new Paragraph({spacing:{after:130,line:270},alignment:AlignmentType.JUSTIFIED,children:runs(t)});}
function runs(t){const o=[];const re=/(\*\*[^*]+\*\*)/g;let last=0,m;const b={size:21,color:INK,font:SERIF};while((m=re.exec(t))){if(m.index>last)o.push(new TextRun({text:t.slice(last,m.index),...b}));o.push(new TextRun({text:m[0].slice(2,-2),bold:true,...b}));last=re.lastIndex;}if(last<t.length)o.push(new TextRun({text:t.slice(last),...b}));return o.length?o:[new TextRun({text:t,...b})];}
function bullet(t){return new Paragraph({bullet:{level:0},spacing:{after:60},children:runs(t)});}
function code(text){return text.split('\n').map(l=>new Paragraph({spacing:{after:0,line:230},shading:{type:ShadingType.CLEAR,fill:MONO,color:'auto'},children:[new TextRun({text:l||' ',font:CODE,size:15,color:INK})]}));}
function tcap(t){return new Paragraph({spacing:{before:60,after:200},children:[new TextRun({text:t,size:17,color:MUT,font:FONT})]});}
function tbl(headers,rows,colW){const total=colW.reduce((a,b)=>a+b,0);const cell=(x,i,head,bold)=>new TableCell({width:{size:colW[i],type:WidthType.DXA},shading:head?{type:ShadingType.CLEAR,fill:HDR,color:'auto'}:undefined,margins:{top:40,bottom:40,left:80,right:80},children:[new Paragraph({children:[new TextRun({text:String(x),bold:head||bold,size:15,font:FONT,color:INK})]})]});const bd={style:BorderStyle.SINGLE,size:2,color:RULE};const borders={top:bd,bottom:bd,left:bd,right:bd,insideHorizontal:bd,insideVertical:bd};const tr=[new TableRow({tableHeader:true,children:headers.map((h,i)=>cell(h,i,true))})];rows.forEach(r=>tr.push(new TableRow({children:r.map((c,i)=>cell(c,i,false,/TOTAL/i.test(String(r[0]))))})));return new Table({columnWidths:colW,width:{size:total,type:WidthType.DXA},borders,rows:tr});}

const c=[];
// header
c.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{before:200,after:60},children:[new TextRun({text:'AI Safeguard Failure Observatory',bold:true,size:38,color:ACC,font:FONT})]}));
c.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:40},children:[new TextRun({text:'Final Production & Hand-off Report — v1.0',size:24,color:INK,font:FONT})]}));
c.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:220},children:[new TextRun({text:'Dataset frozen 2026-09-05  ·  n = 30 incidents  ·  Companion to the research paper',size:18,color:MUT,font:FONT})]}));

// A
c.push(h1('Final project status','A.'));
c.push(p('The Observatory is complete and frozen at v1.0 (2026-09-05). The dataset is the source of truth; the paper is generated from it. Automated QA passes with 0 errors and 0 warnings. Every headline number in the paper was independently recomputed from the frozen CSVs and reconciles exactly. No incidents were added, removed, or recoded; no statistics invented; no denominators changed; no claims strengthened. Frozen counts: 30 incidents, 202 safeguard-interaction rows (181 incident-time + 21 added-after), 84 typed relationships, 25 contributing factors, 52 sources, 24 verified references, 6 figures, 6 tables.'));

// B pointer
c.push(h1('Final research paper','B.'));
c.push(p('The complete research paper (title through references, with all six tables and six figures embedded) is delivered as the companion file **AI_Safeguard_Failure_Observatory_v1.0_paper.docx**. It is byte-generated from the frozen dataset. This report covers the surrounding hand-off material (sections C-N).'));

// C tables note
c.push(h1('Final tables','C.'));
c.push(p('All six tables appear in full in the paper document. They are: Table 1 (the 30 coded incidents), Table 2 (observed state of incident-time safeguards), Table 3 (state by control function), Table 4 (state by system layer), Table 5 (types of inter-safeguard relationship), Table 6 (descriptive headline findings). Each carries an explicit denominator and unit; row totals in Tables 3 and 4 reconcile to 181.'));

// D figure register
c.push(h1('Final figure register','D.'));
[['Figure 1','Observed state of AI/algorithmic safeguards at incident time','181 incident-time safeguards','§6.1'],
['Figure 2','Observed state by control function','row n per function (51/46/29/25/30)','§6.2'],
['Figure 3','Observed state by system layer','row n per layer','§6.5'],
['Figure 4','Types of inter-safeguard relationship','84 relationships','§6.4'],
['Figure 5','Composition of the coded sample','30 incidents','§4'],
['Figure 6','Share Working by control function','row n per function','§6.3']].forEach(f=>c.push(bullet(`**${f[0]}.** ${f[1]} — denominator: ${f[2]}; placement: ${f[3]}.`)));

// E claim audit
c.push(h1('Final claim audit','E.'));
c.push(p('Every major quantitative claim, independently recomputed from the frozen CSVs; all verified.'));
c.push(tbl(['Claim','Num','Denom','Unit','Verified'],
[['Non-functional safeguards','137','181','safeguard','yes'],
['Working safeguards','37','181','safeguard','yes'],
['Working that are external-ecosystem','26','37','safeguard','yes'],
['Preventive Working','0','51','safeguard','yes'],
['Assurance Inadequate','13','30','safeguard','yes'],
['Detective-Working incidents w/ harm','11','30','incident','yes'],
['Incidents with ≥1 Absent','25','30','incident','yes'],
['Omission-dominated incidents','8','30','incident','yes'],
['AI major-contributor','26','30','incident','yes'],
['Organizational attribution','18','30','incident','yes'],
['AI-system attribution','2','30','incident','yes'],
['Enabling relationships','49','84','relationship','yes'],
['Relationships/incident (mean)','2.8','84/30','incident','yes'],
['Generative-era incidents','8','30','incident','yes'],
['Agentic incidents','3','30','incident','yes'],
['Model layer rows (0 Working)','14','181','safeguard','yes'],
['Detective non-functional (+1 Unknown)','32','46','safeguard','yes'],
['Cardinality 181+21','202','—','safeguard','yes']],
[3400,760,900,1300,860]));
c.push(tcap('No claim failed verification. Unknown (6) and Disputed (1) are excluded from "non-functional."'));

// F dataset summary
c.push(h1('Final dataset summary','F.'));
c.push(tbl(['File','Rows','Unit'],
[['data/incidents.csv','30','incident'],
['data/safeguards.csv','202 (181 incident-time + 21 added-after)','safeguard-interaction'],
['data/relationships.csv','84','directed relationship'],
['data/contributing_factors.csv','25','contributing factor'],
['data/sources.csv','52','source'],
['data/observatory_dataset.json','bundle of all five','—']],
[3200,3200,1840]));
c.push(tcap('Keys: incidents.incident_id is parent; child tables carry incident_id; relationship endpoints reference safeguards.interaction_id. Validator: PASS (0/0).'));

// G methodology
c.push(h1('Final methodology summary','G.'));
c.push(h2('Selection (frozen)'));
c.push(p('Discovery pool of 108 candidates from a fixed-source sweep, held separate from the coded sample. Eligibility screen removes cases with no AI/algorithmic decision system in the causal chain. Within predefined strata, eligible cases ranked by a pre-specified evidence-quality rubric (barred from rewarding interesting, safeguard-rich, or finding-favorable cases); highest-ranked taken to quota; seeded random draw (AISFO-2026-08-24) only for boundary ties. Selection precedes analysis. Anti-cherry-pick floors: ≥8 omission-dominated, ≥5 generative-era, ≥2 agentic; per-domain cap 5. One ineligible case (Iberian blackout) deterministically replaced; all other 29 held.'));
c.push(h2('Coding (frozen, CIR v0.3)'));
c.push(p('Each incident bounded (discrete-event / bounded-episode / systemic-program with an explicit observation boundary). One control = one row unless state genuinely diverges by context (shared control_group). Observed state assessed by whether the control performed its intended function ("meaningful engagement"), not nominal presence. Absent requires positive evidence it should have existed (evidentiary fence); otherwise Unknown, with suspected_absent never counted as Absent. Disabled (deliberately switched off) is distinct from Bypassed (circumvented, including hollow oversight) and Absent (never existed). Added-after controls excluded from incident-time distributions. Relationships typed; temporal-precedence never alone implies causation. Contributing factors held separate. ai_causal_contribution (causal weight) is kept separate from attributed_primary_cause (blame). Uncertainty carried per row via evidence_status and confidence.'));

// H framework vocab
c.push(h1('Final coding-framework summary (controlled vocabularies)','H.'));
[['observed_state (8)','Working, Inadequate, Failed, Bypassed, Disabled, Absent, Disputed, Unknown'],
['primary_function (5)','preventive, detective, containment, recovery, assurance-governance'],
['system_layer (6)','model, application, infrastructure-environment, human-operator, organizational-process, external-ecosystem'],
['system_type (4)','confirmed-ML, probable-ML, algorithmic-nonML, unknown (0 unknown in sample)'],
['relationship_type','enabling, masking, temporal-precedence, common-cause, cascading, compensating (four observed)'],
['outcome_class (3)','realized-harm (28), near-miss (2), averted'],
['incident_scope (3)','discrete-event (14), bounded-episode (2), systemic-program (14)'],
['existence_timing (2)','incident-time (181), added-after (21)'],
['inadequacy_type (4)','design, operation, enforcement, unknown (only when Inadequate)'],
['evidence_status (5)','confirmed-authoritative, multiply-reported, single-source-reported, inferred-indirect, disputed'],
['causal_role (7)','primary, contributing, aggravating, mitigating, latent-condition, not-causally-relevant, unknown']].forEach(v=>c.push(bullet(`**${v[0]}:** ${v[1]}`)));

// I QA
c.push(h1('Final QA summary','I.'));
c.push(p('QA status: PASS. Errors: 0. Warnings: 0. Reconciliation: all headline statistics recomputed independently from the frozen CSVs match the paper, tables, and figures; cardinality 181+21=202; all state/function/layer totals reconcile to 181; relationship endpoints resolve with 0 orphans. Coding adjudications: 12 flagged calls resolved and documented; 2 Batch-1 calibration decisions locked and applied sample-wide. Evidence quality: 146/202 confirmed-authoritative, 8 disputed; 134 high confidence, 13 low.'));

// J package tree
c.push(h1('Final public-artifact structure','J.'));
c.push(...code(
`observatory/
  README.md                      [public]
  MANIFEST.txt                   [support: 55-file inventory + sha256]
  data/                          [public: source of truth]
    incidents.csv (30)
    safeguards.csv (202)
    relationships.csv (84)
    contributing_factors.csv (25)
    sources.csv (52)
    observatory_dataset.json
  paper/
    J_research_paper.md          [public]
    AI_Safeguard...paper.docx    [public: Word paper]
  figures/  fig1..fig6.png       [public]
  tables/   table1..table6       [public: .md + .csv]
  analysis/ analysis_results.json[support]
  docs/     B..N + framework, protocol, batches  [support]
  scripts/  build_dataset, validate, analyze,
            make_tables, make_figures,
            audit_independent, select_sample_v2  [support]`));

// K README
c.push(h1('Final README (excerpt)','K.'));
c.push(p('The full README ships as README.md. Its core: the Observatory codes, for 30 real-world incidents, every identifiable safeguard as a structured interaction (system layer, control function, observed state at incident time, evidence, causal role) plus the typed relationships between safeguards; the dataset is the artifact and the paper is generated from it. Headline findings, reproduction commands, limitations, repository structure, and citation instructions are included. Reproduction:'));
c.push(...code(
`cd observatory
python3 scripts/build_dataset.py && python3 scripts/validate.py && \\
python3 scripts/analyze.py && python3 scripts/make_tables.py && \\
python3 scripts/make_figures.py
# validate.py must print RESULT: PASS`));

// L runbook
c.push(h1('Reproducibility runbook','L.'));
c.push(p('Environment: Python 3.11+ with pandas, numpy, matplotlib; standard library otherwise; no network required. Single source of truth: scripts/build_dataset.py encodes all 30 incidents; the CSV/JSON files are generated. To correct a coding, edit build_dataset.py and rebuild; never hand-edit generated files. Determinism: the only stochastic step (selection boundary tie-break) is seeded (AISFO-2026-08-24). Validation gate: validate.py must pass (referential integrity, ID uniqueness, controlled vocabularies, denominator-contamination guards). Independent audit: scripts/audit_independent.py recomputes headline numbers reading only data/*.csv. Versioning: frozen v1.0; any post-freeze change must bump the version, re-pass validate.py, and be logged.'));

// M references
c.push(h1('Final references (24, verified)','M.'));
c.push(p('The complete 24-reference list appears in the paper document (Section 12) and docs/K_references.md. All entries were verified to exist with the exact title and a working locator; none is invented. Per-incident primary sources (52) are in data/sources.csv.'));

// N issue log
c.push(h1('Final change / issue log','N.'));
c.push(p('No unresolved factual or internal-consistency issues remain. Documented limitations (not defects):'));
[['n=30, purposive selection on realized harm/near-miss — not representative; some distributions (0 Working preventive) are partly artifacts of selecting on harm.'],
['No inter-rater reliability computed; per-row evidence_status and confidence are the transparency substitute.'],
['Documentation bias toward investigated harms; three domains uncovered.'],
['Two sub-judice cases (Raine, Workday) coded conservatively as allegations, low confidence, disputed; provisional.'],
['era is a paradigm flag, not a pure date cutoff (two 2023 AV cases are legacy); dataset genai=8 is authoritative.'],
['Prior corrections (domain count, §6.3 and §6.6 wording, §10 alignment, era gloss) are recorded in docs/N_final_integrity_audit.md; this production pass changed no data, methodology, framework, sample, analysis, or findings.']].forEach(x=>c.push(bullet(x[0])));

const doc=new Document({creator:'AI Safeguard Failure Observatory',title:'AISFO v1.0 Production Report',
  styles:{default:{document:{run:{font:SERIF,size:21,color:INK}}}},
  sections:[{properties:{page:{size:{width:12240,height:15840},margin:{top:1180,bottom:1180,left:1440,right:1440}}},children:c}]});
Packer.toBuffer(doc).then(b=>{fs.writeFileSync(OUT,b);console.log('WROTE',OUT,b.length);});
