"""Build a 34-slide faculty research briefing and 16 visual appendices."""
from pathlib import Path
from html import escape as esc
import json
import math
import textwrap
HERE = Path(__file__).resolve().parent
TOPIC = next((p for p in HERE.parents if (p / 'data/README.md').exists()))
R = TOPIC / 'research'
evidence = json.loads((HERE / 'evidence.json').read_text(encoding='utf8'))
a = json.loads((R / 'kaggle-roadmap-2026-10-31/output-analysis.json').read_text(encoding='utf8'))
d = json.loads((R / 'kaggle-roadmap-2026-10-31/output-analysis-details.json').read_text(encoding='utf8'))
hif = json.loads((R / 'slide-figures-2026-10-15/example-matrix.json').read_text(encoding='utf8'))
GREEN = '#18974C'
DARK = '#0A5032'
CORAL = '#C76242'
BLUE = '#477CA7'
INK = '#193A2B'
SAGE = '#D0DEBB'
LINE = '#D6DFD3'
slides = []
NOTE_OVERRIDES = {1: 'This is an introduction and research progress discussion with a lecturer, rather than a final thesis defense. The opening visual uses measured HIF1A mutation labels. The aim is to explain the task, present the evidence available so far and discuss the next research steps.', 2: 'The diagram is a simplified illustration of the ubiquitin–proteasome system. The Fam188a GIF by Nikolakhs, licensed CC BY-SA 3.0, illustrates a folded protein; it is not a measured HIF1A or degron structure. A peptide assayed in isolation may behave differently within the full protein.', 3: 'WT is the reference sequence. The display has 28 positions and 20 amino acids; WT-to-WT cells are masked, leaving up to 532 genuine substitutions. This diagram explains the output format and does not show model predictions.', 4: 'The histogram illustrates the measurement principle rather than actual counts. The Zhang assay uses six bins and a PSI scale from 1 to 6; lower PSI indicates a less stable reporter. A positive ΔPSI means the mutant reporter is more stable than WT. The sign alone does not establish an E3 mechanism or pathogenicity.', 5: 'The example is Q16665_HIF1A_25, residues 553–580 of HIF1A. Intrinsic WT PSI is 2.1865; 529 substitutions were measured and 186 have ΔPSI ≥ 1. Selection required at least 500 measured cells, then the highest positive-cell count, with ID as the tie-breaker. The connection to the HIF1A/VHL motif is a literature cross-check, not a newly discovered mechanism. WT and missing cells are masked.', 6: 'Predicted ranking helps design experiments but does not replace them. ClinVar supplies annotations and motivation; a residue-level relationship to pathogenicity has not been established. The schematic cells represent prioritization, not numerical model scores.', 7: 'An effect map or a web application is not an exclusive novelty claim. AUROCs for different endpoints and prediction units cannot be directly compared. Degformer already provides mutation maps. MetaDegron uses a shared classifier with motif/E3 choices; menu entries are not separately learned E3 classes. The defensible focus is measured labels, evaluation, strong baselines and practical utility.', 8: 'The main task is predicting single-substitution effects in 28-residue reporter peptides. E3 specificity and clinical classification are outside the primary task. No new biological measurements were collected. The tool supports hypothesis generation and experimental prioritization.', 9: 'These are related research questions, not a timeline of runs. Findings are grouped by the question addressed rather than by experiment codes or execution dates. Source transfer, representations and practical reliability each require their own comparisons.', 10: 'The core full-range dataset contains Zhang measurements and UniProt sequence information. It does not contain ClinVar, Koren, Larsen, MetaDegron or model weights. Voutsinos supplies a tile-level transfer task and PAP baseline resources. Keep downloaded, audited and fitted sources conceptually separate.', 11: 'The scanning replacement is determined by the WT amino acid, with targets R, A or S. It therefore covers 20 directed substitution types out of 380 non-synonymous types. The schematic shows the design, not a claim that every cell passes QC. Saturation provides the broader substitution matrix needed for this task.', 12: 'Saturation has no direct mut0 reference, so the WT reference is the median of synonymous constructs within each half. Scanning uses mut0 from the correct replicate. BAG6 WT must not be used as the saturation reference. Reconstructing 261,865 published PSI values matched within 5 × 10⁻⁷ when the published processing conditions were reproduced.', 13: 'The Pearson correlation of ΔPSI between the two saturation halves is 0.8335 on the audited cohort. Peptide-level reliability is different from position- or cell-level reproducibility. Noise as a fraction of residual variance must not be compared with noise as a fraction of total variance as though they had the same denominator. Replicates describe measurement reliability rather than a universal ceiling for every possible estimator.', 14: 'The restricted-domain and full-range designs differ in population, eligibility and preprocessing; their AUROCs must not be joined into a single progression curve. The full-range design uses five outer folds and three inner-validation seeds. Transformations are fitted within training data. Neural epochs are selected on inner validation before reinitialization and outer-training refit. Homology control is heuristic, not proof of complete biological independence.', 15: 'Full-range MAE uses all 235 peptides. Positive events, measured ΔPSI ≥ 1, have 184 eligible peptides; negative events, ΔPSI ≤ −1, have 110. Both classes need at least three cells. Confidence intervals use 5,000 protein-group bootstrap resamples, not 122,412 independent mutation cells. AUROC is not accuracy, and AP must be read with event prevalence.', 16: 'On the scanning evaluation, substitution plus composition achieves AUROC 0.8393; unordered local composition reaches 0.8625; ordered local context reaches 0.8682. The paired ordered-context improvement is 0.0289, with a 95% interval from 0.0264 to 0.0313. This source reports mean seed AUROC, not the full-range prediction ensemble. A composition-only linear term cannot independently distinguish positions with the same substitution within a peptide.', 17: 'The comparison uses the same 235 test peptides and 221 protein groups. Full-range training reduces MAE by 5.94% relative to training only at PSI ≤ 4. The two primary comparisons use adjusted 97.5% confidence intervals. The bound nearest zero does not establish a minimum reduction of 0.02 PSI. Restricted training still uses full-range validation. WT PSI is metadata, not a model feature or a test-time clipping input.', 18: 'The four PSI strata contain 91, 85, 36 and 23 peptides. Balancing helps high-PSI peptides but can trade off low-PSI performance. PSI > 5 cannot have a positive event ΔPSI ≥ 1, so positive AUROC is undefined there. Ridge guardrails do not automatically transfer to CNN: compared with a CNN trained only at PSI ≤ 4, full-range CNN increases low-PSI MAE by about 0.00870, and its AUROC interval does not establish the 0.01 guardrail.', 19: 'Adding ESM to context Ridge improves positive AUROC by about 0.01255, with a descriptive 95% interval from 0.00622 to 0.01967. Validation-based nested selection reaches MAE 0.397525, but its AUROC gain remains unresolved. A fixed recipe cannot substitute for evaluation of the selection procedure. Only ESM2-35M has been evaluated on the full-range benchmark.', 20: 'With the same representation and full-range training, CNN reduces MAE by 0.00534 versus pointwise, with a descriptive 95% interval from −0.01017 to −0.00090. Positive AUROC increases by about 0.01129. Pointwise and CNN heads have 36,833 and 57,185 parameters, respectively, so this is not a complete isolation of position mixing from model capacity.', 21: 'The balanced multi-window model has MAE 0.383846 versus 0.384354 for the full-range CNN. The difference, −0.000508, has a descriptive 95% interval from −0.003157 to +0.002223; the two training distributions also differ. With the same full-range training, multiple windows likewise have no demonstrated advantage. A CNN trained only at PSI ≤ 4 remains relevant when prioritizing the low-PSI domain.', 22: 'The comparison uses the same encoder, fine-tuning procedure and 91-peptide evaluation domain. Pretraining on 212,616 tiles learns its own task well, with Pearson correlation around 0.864. After fine-tuning, AUROC is 0.8098 versus 0.8175 from random initialization; the difference interval still includes zero. The negative conclusion applies to this tile-label transfer design, not to all pLMs or all transfer strategies.', 23: 'This is a one-hot CNN, not an ESM-plus-scanning experiment. The 20-type cohort has 6,433 cells and the remaining 360 types have 115,979 cells; both cover 235 peptides and 221 groups. Both MAE intervals favor improvement, but these are descriptive posthoc diagnostics. Averaging replicates has no clear advantage over replicate 1, and quality weighting increases MAE by about 0.00401. These are saturation OOF findings, not held-source T results.', 24: 'The published checkpoint has 42,163 of the 47,847 mutation cells and WT sequences for all 91 peptides in its training data. Removing duplicate cells does not produce a peptide holdout. Group-clean retraining reaches AUROC 0.806775 versus 0.820822 for Ridge with expanded training; the difference interval includes zero. Do not interpret the checkpoint/retraining difference as a causal effect of leakage alone because training conditions also change.', 25: 'Positive precision is macro-averaged over 184 eligible peptides. At the top 5%, CNN reaches 58.24% versus 51.89% for Ridge; at the top 10%, the values are 49.04% and 44.29%. Positive AP is 0.50947 with macro prevalence 0.124697. For negative events, AP is 0.213667 over 110 peptides and top-5% precision is about 16.77%. These are ranking utilities, not whole-dataset accuracy or calibrated probabilities.', 26: 'CNN improves MAE over Ridge on 156 of 235 peptides and across all five folds. Completed task time totals 9.3265 hours, including 7.23 hours for two frozen-backbone tasks. The frozen branch has seed 17 with five folds; LoRA has no complete OOF output. A saved running status does not establish that a remote process is still alive. Do not merge results from a different local runtime into this Kaggle snapshot.', 27: 'This calibration evidence belongs to Ridge, evaluated out of fold on 91 peptides. Platt calibration has Brier score about 0.0925 versus 0.1139 for the prevalence baseline. A ΔPSI regression score is not itself a probability. Reliability remains somewhat biased low because calibration-pool and test-domain distributions differ; it is not perfect calibration. CNN needs its own calibrator and evaluation procedure.', 28: 'The gate was studied for the training domain PSI ≤ 4. Peptidome-screen PSI differs from intrinsic WT PSI by about 0.9, so the raw threshold 4 cannot be directly reused. In-domain, borderline and out-of-domain states describe data applicability, not guaranteed ΔPSI accuracy. Full-range training also does not establish applicability to every protein. Correct integration of the gate into the baseline app remains open.', 29: 'The screenshot shows the current Workspace UI v2 design prototype, cropped to the effect map and inspector. Every displayed score and probability is a synthetic fixture; there is no model inference or backend. The React/FastAPI baseline is separate code. This image illustrates the workflow and does not certify the expanded features.', 30: 'The selected stack is local React/TypeScript and FastAPI. SQLite has been used for the baseline; PostgreSQL and durable workspace storage still require implementation and verification. Public hosting is not required. The diagram explains architecture and provenance rather than claiming that every module is complete.', 31: 'The tests recorded in the documentation cover the baseline and were not rerun while building this deck. Projects/history, durable batch jobs, whole-protein web workflows and experimental-data import still require implementation under the expanded scope. The new domain gate has not been correctly integrated into the baseline. A designed endpoint is not an accepted implementation.', 32: 'Connect the available artifacts and findings back to the three initial objectives. The developing contribution includes data/benchmark construction, experimental methodology, evaluation and software. A new architecture is not required to explain the research value. This is a progress discussion rather than a claim that the thesis is complete.', 33: 'Automatic final promotion currently supports context Ridge; CNN needs architecture-specific final refitting and export. Lock the recipe and calibration before reading T. Scanning has previously been explored, so T must be described with its held-source scope and exposure history. Model research and tool development can proceed in parallel. Completing LoRA is not a prerequisite for the core benchmark.', 34: 'Invite feedback on research objectives and priorities: overall regression versus strong-event prioritization, the appropriate generalization test, and software scope. This is an introduction/progress meeting, not final acceptance. Use the overview and appendices when a detailed comparison is useful.', 35: 'Residue means an amino acid at a specific position; WT is the reference sequence. OOF predictions come from the fold in which that peptide or protein group was held out. MAE, AUROC/AP and top-k precision address different objectives and may use different eligible peptide populations.', 36: 'Use the WT reference appropriate to the assay. Synonymous constructs provide intrinsic WT estimates for saturation. Missing cells are masked rather than labelled zero. Source, condition, replicate and QC information remain attached to derived labels.', 37: 'Scanning ΔPSI Pearson correlation is 0.7229; saturation is 0.8335. Scanning Jaccard is position-based whereas saturation Jaccard is cell-based. Cohorts and denominators differ, so this is a description of reliability rather than a paired source comparison. Residual-noise and total-variance noise fractions are not interchangeable.', 38: 'The invariance applies to composition-only models within the same peptide and for the same substitution type. It does not apply to all of PAP, which has a C-terminal channel, or to models using local context. The baseline named composition in the source also contains WT and mutant one-hot features. An oracle reading test labels describes representation limits, not model test performance.', 39: 'The curve reports mean single-seed MAE. At fractions below 100%, different seeds use different training subsets; their ensemble may therefore see a larger union of examples than each member. Read single-fit data sensitivity from the individual-seed summary. Clustering sensitivity is separate, and repeated identical partitions are not additional independent evidence.', 40: 'These interaction designs were tested on the restricted 91-peptide evaluation. The baseline and each candidate must be compared under the stated training conditions. The gate effect changes sign across seeds, and the tested FiLM/bilinear variants did not consistently improve over Ridge. This does not rule out all nonlinear interactions or future designs.', 41: 'The published Degformer checkpoint has 42,163 of 47,847 mutation cells in its training data, and all 91 WT peptides have been seen. Filtering exact mutant overlap leaves other mutations from the same peptides. Group-based retraining is needed for an unseen-peptide generalization claim. The figure uses the group-clean comparison and its corresponding baselines.', 42: 'This table describes ESM-augmented Ridge models on the 91-peptide design, not the full-range population. None of the size comparisons established a benefit under its stated criterion. Many checkpoint entries in a registry do not mean all have been evaluated. The full-range output currently evaluates only ESM2-35M.', 43: 'The interactive appendix switches among MAE, positive AUROC and positive AP without changing model candidates or numerical values. All scores are computed from mean per-cell predictions of seeds 17, 29 and 43. The table remains development evidence rather than an unbiased estimate after model selection. For printing, a static MAE/AUROC figure is provided.', 44: 'For each peptide, only cells in the cohort being evaluated are included. The 20-type cohort has 114 peptides eligible for positive AUROC, versus 184 for the remaining 360 types. Do not directly compare those macro AUROCs as though the populations were identical. The plotted MAE intervals are descriptive posthoc intervals from 5,000 protein-group bootstrap resamples.', 45: 'The protein-stratified Mantel–Haenszel odds ratio is about 2.14783, with 95% interval 2.07193–2.22651 over 3,114 informative strata. This is a region-level association, not causality. The exact-substitution saturation analysis has few classified variants, and its AUC interval still includes 0.5. ClinVar is not used as the model-selection target for ΔPSI.', 46: 'The E3/adaptor audit found only one group with at least five peptides. KLHL15 has 13 peptides, BAG6 has four, ASB7 and FEM1B have two each, and most remaining groups have one. The number of reported E3s or menu options is not evidence of enough examples to learn E3-conditioned specificity.', 47: 'Koren has not provided a completed model evaluation here; its scale and peptide length differ and it adds only five new groups, so it was not included in training. Larsen supplies tile scores rather than complete mutation ΔPSI labels. MaveDB structure analyses are exploratory, with endpoint and dimer issues still requiring review. SaProt true-3Di has no completed output; weights do not replace structure mapping.', 48: 'Calibration asks whether predicted event probabilities match observed frequencies. Domain assessment asks whether the input resembles the conditions covered by the model and data. The two questions are different, and both require reassessment after changing models or scope. The displayed calibration evidence belongs to the tested Ridge model.', 49: 'Checksums and sizes were verified for 2,986 snapshot files, including 83 OOF files across 47 recipes. Recomputed analysis matches the stored numbers. Baseline app tests in the documentation are historical evidence, not a new test run during slide creation. Results from a different local runtime must not be silently merged into the Kaggle campaign.', 50: 'Sources are kept in Notes, the appendix, slide-sources.json and evidence.json instead of per-slide footnotes. The template/style websites informed the visual design, not model-performance claims. Asset notices identify the protein GIF, fonts and Chart.js. The English edition preserves the numerical sources and research scope of the Vietnamese edition.'}

def text(x, y, value, size=22, color=INK, anchor='middle', weight=400):
    vals = value if isinstance(value, list) else str(value).split('\n')
    return ''.join((f'<text x="{x}" y="{y + i * (size * 1.32)}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{esc(str(v))}</text>' for i, v in enumerate(vals)))

def box(x, y, w, h, label, sub='', color=GREEN):
    lines = label if isinstance(label, list) else textwrap.wrap(label, width=max(11, int(w / 12)))
    sy = y + h / 2 - (len(lines) - 1) * 14 + 7
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="white" stroke="{color}" stroke-width="2"/>'
    s += text(x + w / 2, sy, lines, 22, color, weight=600)
    if sub:
        s += text(x + w / 2, y + h + 32, textwrap.wrap(sub, 22), 18)
    return s

def edge(x1, y1, x2, y2, color=GREEN, moving=True, delay=0):
    angle = math.atan2(y2 - y1, x2 - x1)
    wing = 9
    p1 = (x2 - wing * math.cos(angle - 0.45), y2 - wing * math.sin(angle - 0.45))
    p2 = (x2 - wing * math.cos(angle + 0.45), y2 - wing * math.sin(angle + 0.45))
    s = f'<path d="M{x1} {y1} L{x2} {y2} M{p1[0]} {p1[1]} L{x2} {y2} L{p2[0]} {p2[1]}" stroke="{color}" stroke-width="2.2" fill="none"/>'
    if moving:
        s += f'<circle class="flow" cx="{x1}" cy="{y1}" r="5" fill="{color}" style="--dx:{x2 - x1}px;--dy:{y2 - y1}px;animation-delay:-{delay}s"/>'
    return s

def svg(contents, label='Schematic illustration', w=1100, h=430):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label, quote=True)}"><title>{esc(label)}</title>{contents}</svg>'

def process(labels, subs=None, colors=None):
    n = len(labels)
    gap = 34
    w = min(210, (1080 - (n - 1) * gap) / n)
    total = n * w + (n - 1) * gap
    x0 = (1100 - total) / 2
    s = ''
    for i, label in enumerate(labels):
        x = x0 + i * (w + gap)
        col = (colors or [GREEN] * n)[i]
        s += box(x, 142, w, 100, label, (subs or [''] * n)[i], col)
        if i < n - 1:
            s += edge(x + w + 2, 192, x + w + gap - 5, 192, col, delay=i)
    return svg(s, 'Process:' + '; '.join(labels))

def sequence(x=50, y=130, sequence=None, step=30, highlight=11, mutant=False):
    seq = sequence or hif['sequence']
    s = ''
    for i, aa in enumerate(seq):
        hot = i == highlight
        fill = CORAL if hot else SAGE
        s += f'<rect x="{x + i * step}" y="{y}" width="{step - 3}" height="34" rx="3" fill="{fill}"/>'
        s += text(x + i * step + (step - 3) / 2, y + 24, 'D' if mutant and hot else aa, 18, 'white' if hot else INK, weight=600)
    return s

def heat(x=0, y=0, cw=16, ch=12, design=False, scan=False):
    aa = hif['aa_order']
    s = ''
    for j, letter in enumerate(aa):
        for i, row in enumerate(hif['matrix']):
            v = row.get(letter)
            if design:
                target = 'R' if hif['sequence'][i] in 'ACDEGILSTV' else 'A' if hif['sequence'][i] in 'HKNQRY' else 'S'
                fill = GREEN if (not scan or letter == target) and letter != hif['sequence'][i] else '#E3E8DF'
            elif v is None:
                fill = '#DCE4D7'
            elif v < 0:
                fill = BLUE
            elif v < 0.5:
                fill = '#E1E7D3'
            elif v < 1:
                fill = '#E6CDB0'
            elif v < 2:
                fill = '#DE9472'
            else:
                fill = '#BC5038'
            s += f'<rect x="{x + i * cw}" y="{y + j * ch}" width="{cw - 1}" height="{ch - 1}" fill="{fill}"/>'
    return s

def mutation_diagram():
    s = sequence(45, 70, step=33) + text(45, 48, 'Reference sequence', 20, anchor='start')
    s += edge(425, 120, 425, 190, CORAL) + box(300, 195, 250, 78, 'Replace P with D', 'At position 12', CORAL)
    s += edge(560, 234, 660, 234, CORAL) + heat(690, 128, 12, 9, design=True)
    s += f'''<rect class="pulse" x="{690 + 11 * 12}" y="{128 + hif['aa_order'].index('D') * 9}" width="11" height="8" fill="{CORAL}"/>'''
    s += text(855, 360, ['One substitution', 'one effect-map cell'], 24, DARK, weight=600)
    return svg(s, 'One substitution at one position corresponds to one matrix cell')

def protein_process():
    s = ''
    for i in range(14):
        x = 60 + i * 22
        y = 190 + 28 * math.sin(i * 0.75)
        if i:
            s += f'<line x1="{60 + (i - 1) * 22}" y1="{190 + 28 * math.sin((i - 1) * 0.75)}" x2="{x}" y2="{y}" stroke="{SAGE}" stroke-width="9"/>'
        s += f'<circle cx="{x}" cy="{y}" r="10" fill="{(CORAL if 5 <= i <= 7 else GREEN)}"/>'
    s += text(210, 280, 'Protein mang degron', 24, weight=600)
    s += edge(370, 190, 485, 190, delay=1)
    s += f'<path class="pulse" d="M500 125 Q620 85 640 170 L580 170 L580 212 L640 212 Q610 300 500 255Z" fill="{SAGE}" stroke="{DARK}" stroke-width="3"/>'
    s += text(565, 340, ['Recognition', 'and ubiquitination'], 21)
    for i in range(4):
        s += f'<circle class="flow" cx="660" cy="{160 + i * 20}" r="7" fill="{CORAL}" style="--dx:190px;animation-delay:-{i + 1}s"/>'
    s += edge(660, 190, 820, 190, delay=2)
    for i in range(5):
        s += f'<ellipse cx="{870 + i * 19}" cy="190" rx="27" ry="64" fill="none" stroke="{DARK}" stroke-width="10" opacity="{0.45 + i * 0.1}"/>'
    s += text(906, 310, 'Proteasome', 23, weight=600)
    for i in range(5):
        s += f'<circle class="flow" cx="980" cy="{155 + i * 18}" r="5" fill="{GREEN}" style="--dx:90px;animation-delay:-{i}s"/>'
    return svg(s, 'Schematic of degron recognition, ubiquitination and protein degradation')

def assay_diagram():
    s = box(25, 120, 180, 98, ['Peptide-linked', 'reporter'], 'Fluorescence ratio') + edge(215, 170, 300, 170)
    for i, h in enumerate([35, 80, 125, 100, 60, 30]):
        x = 330 + i * 66
        s += f'<rect x="{x}" y="{270 - h}" width="42" height="{h}" fill="{GREEN}" opacity="{0.35 + i * 0.1}"/>'
        s += text(x + 21, 305, str(i + 1), 19)
        s += f'<circle class="flow" cx="300" cy="90" r="5" fill="{CORAL}" style="--dx:{x - 279}px;--dy:{170 - h}px;animation-delay:-{i * 0.7}s"/>'
    s += text(520, 350, 'Sort into six bins', 23, weight=600) + edge(745, 170, 815, 170)
    s += box(830, 120, 235, 98, 'PSI', 'Reporter stability index')
    return svg(s, 'Reporter, sorting bins and PSI; the histogram is schematic')

def priority_diagram():
    s = ''
    for i in range(12):
        for j in range(8):
            x = 80 + i * 26
            y = 80 + j * 26
            hot = (i, j) in [(2, 2), (5, 5), (8, 1), (10, 6)]
            s += f'''<rect x="{x}" y="{y}" width="21" height="21" rx="3" fill="{(CORAL if hot else SAGE)}" class="{('pulse' if hot else '')}"/>'''
    s += text(230, 345, 'Many substitutions to test', 22) + edge(415, 185, 575, 185)
    for i in range(4):
        s += box(605 + i * 109, 140, 88, 88, ['Pick'] if i == 0 else str(i + 1), color=CORAL)
    s += text(820, 300, 'Prioritize for experiments', 26, DARK, weight=600)
    return svg(s, 'Schematic prioritization under an experimental budget; no model scores are shown')

def designs():
    s = heat(30, 85, 16, 12, True, True) + heat(620, 85, 16, 12, True, False)
    s += text(250, 45, 'Scanning', 28, DARK, weight=600) + text(840, 45, 'Saturation', 28, DARK, weight=600)
    s += text(250, 365, ['One substitution per position', '20 WT-to-mutant types'], 23)
    s += text(840, 365, ['Many substitutions per position', '380 WT-to-mutant types'], 23)
    return svg(s, 'Scanning and saturation designs; green cells indicate assayed substitution types')

def label_pipeline():
    s = box(10, 120, 155, 100, 'Read theo bin') + edge(175, 170, 225, 170)
    s += box(235, 120, 155, 100, 'PSI per replicate')
    s += edge(400, 170, 470, 95) + edge(400, 170, 470, 260)
    s += box(480, 45, 275, 90, 'Measured WT', 'Scanning') + box(480, 225, 275, 90, 'WT from synonymous cells', 'Saturation')
    s += edge(765, 90, 850, 170) + edge(765, 270, 850, 170)
    s += box(860, 120, 210, 100, 'Effect: ΔPSI', 'QC retains valid cells')
    return svg(s, 'Reconstructing labels with the appropriate WT reference for each assay')

def sources_diagram():
    s = ''
    for x, y, label, role, col in [(15, 55, 'Zhang', 'Mutation labels', GREEN), (590, 55, 'UniProt', 'Sequences / groups', DARK), (15, 260, 'Voutsinos', 'Tile / baseline', BLUE), (590, 260, 'ClinVar', 'Annotations', CORAL)]:
        s += box(x, y, 185, 90, label, color=col) + edge(x + 195, y + 45, x + 265, y + 45, col)
        s += box(x + 275, y, 225, 90, role, color=col)
    return svg(s, 'Four distinct data sources with different roles')

def groups_diagram():
    s = ''
    cols = [GREEN, BLUE, CORAL, DARK]
    for j, col in enumerate(cols):
        x = 70 + j * 100
        for i in range(3):
            s += f'<circle cx="{x + 24 * math.cos(i * 2.1)}" cy="{120 + 24 * math.sin(i * 2.1)}" r="12" fill="{col}"/>'
    s += text(210, 210, 'Keep protein groups intact', 24, weight=600)
    s += edge(430, 120, 600, 120) + edge(430, 140, 600, 290, CORAL)
    s += box(620, 65, 390, 105, 'Training and validation', 'Fit and tune here')
    s += box(620, 250, 390, 105, 'Outer test groups', 'Evaluation only', CORAL)
    return svg(s, 'Protein groups remain intact across training, validation and outer test sets')

def context_diagram():
    s = sequence(35, 110, sequence='MLAPYIPMDDDFQLRS', step=55, highlight=7)
    s += f'<rect class="scan-window" x="160" y="88" width="235" height="80" fill="none" stroke="{DARK}" stroke-width="4" rx="4"/>'
    s += text(400, 250, ['Same substitution', 'local contexts may differ'], 28, weight=600)
    return svg(s, 'A local context window around the mutation site', w=950, h=350)

def head_diagram(multi=False):
    s = ''
    for i in range(12):
        for j in range(4):
            s += f'<rect x="{45 + i * 39}" y="{65 + j * 30}" width="30" height="22" fill="{BLUE}" opacity="{0.25 + j * 0.15}"/>'
    s += text(260, 225, 'Representation ESM', 23)
    if multi:
        for j, (width, col) in enumerate([(105, GREEN), (183, BLUE), (261, CORAL)]):
            s += f'<rect class="scan-window" x="75" y="{45 + j * 5}" width="{width}" height="145" fill="none" stroke="{col}" stroke-width="3"/>'
    else:
        s += f'<rect class="scan-window" x="75" y="45" width="183" height="145" fill="none" stroke="{DARK}" stroke-width="4"/>'
    s += edge(545, 125, 650, 125) + box(665, 80, 235, 90, 'Predict ΔPSI', 'Train the mutation head')
    return svg(s, 'Convolution filters scan the representation', w=950, h=310)

def transfer_diagram():
    s = box(35, 45, 230, 95, 'Tile labels', 'Whole-tile activity', BLUE) + box(35, 235, 230, 95, 'Mutation labels', 'Substitution effects', GREEN)
    s += edge(280, 90, 450, 90, BLUE) + edge(280, 280, 450, 280, GREEN)
    s += box(465, 45, 230, 95, 'Pretraining', 'Learns the tile task well', BLUE) + box(465, 235, 230, 95, 'Fine-tuning', 'Predict ΔPSI', GREEN)
    s += edge(710, 90, 880, 190, CORAL) + edge(710, 280, 880, 190, GREEN)
    s += box(885, 140, 185, 100, 'Evaluation', 'Match the encoder baseline', CORAL)
    return svg(s, 'Tile labels and mutation labels have different targets')

def domain_diagram():
    s = box(20, 150, 220, 100, 'Input peptide') + edge(250, 200, 405, 200)
    s += box(420, 150, 220, 100, 'Domain assessment')
    for y, label, col in [(55, 'In domain', GREEN), (180, 'Borderline', BLUE), (305, 'Out of domain', CORAL)]:
        s += edge(650, 200, 805, y + 36, col) + box(820, y, 245, 76, label, color=col)
    return svg(s, 'Domain assessment determines the appropriate prediction or warning')

def architecture():
    s = box(20, 140, 220, 105, ['Interface', 'React'], 'Input / inspect / export') + edge(250, 190, 400, 190)
    s += box(415, 140, 235, 105, 'FastAPI', 'Validation / orchestration')
    s += edge(660, 190, 820, 85) + edge(660, 205, 820, 300, BLUE)
    s += box(830, 30, 245, 110, ['Inference', 'and model card'], 'Version / scope')
    s += box(830, 255, 245, 110, ['Local data', 'and provenance'], 'Sources / snapshot', BLUE)
    return svg(s, 'Local application architecture and result provenance')

def metrics_diagram():
    s = ''
    for i, (label, desc, col) in enumerate([('Error', 'MAE', GREEN), ('Ranking', 'AUROC / AP', BLUE), ('Experimental priorities', 'Precision top-k', CORAL)]):
        x = 30 + i * 365
        s += text(x + 165, 60, label, 25, col, weight=600)
        if i == 0:
            s += f'<line x1="{x + 70}" y1="240" x2="{x + 260}" y2="120" stroke="{LINE}" stroke-width="2"/>'
            for j in range(4):
                yy = 215 - j * 24
                s += f'<circle cx="{x + 95 + j * 42}" cy="{yy}" r="8" fill="{GREEN}"/><line x1="{x + 95 + j * 42}" y1="{yy}" x2="{x + 95 + j * 42}" y2="{yy - 26}" stroke="{CORAL}" stroke-width="3"/>'
        elif i == 1:
            for j, h in enumerate([140, 115, 90, 55, 30]):
                s += f'<rect x="{x + 65 + j * 43}" y="{265 - h}" width="27" height="{h}" fill="{col}" opacity="{1 - j * 0.13}"/>'
        else:
            for j in range(20):
                s += f'<circle cx="{x + 65 + j % 5 * 45}" cy="{130 + j // 5 * 40}" r="13" fill="{(CORAL if j < 4 else SAGE)}"/>'
        s += text(x + 165, 340, desc, 26, col, weight=600)
    return svg(s, 'Error, ranking and experimental prioritization are distinct evaluation goals')

def table(headers, rows, compact=False):
    return '<table class="table' + (' compact' if compact else '') + '"><thead><tr>' + ''.join(('<th>' + esc(str(x)) + '</th>' for x in headers)) + '</tr></thead><tbody>' + ''.join(('<tr>' + ''.join(('<td>' + str(x) + '</td>' for x in row)) + '</tr>' for row in rows)) + '</tbody></table>'

def image(name, alt, short=False):
    return f'''<img class="figure{(' short' if short else '')}" src="assets/{name}.svg" alt="{esc(alt, quote=True)}">'''

def split(visual, aside, kind=''):
    return f'<div class="split {kind}"><div class="visual">{visual}</div><div class="aside">{aside}</div></div>'

def full(visual):
    return f'<div class="visual">{visual}</div>'

def metric(value, label):
    return f'<p><span class="number">{value}</span><span class="label">{label}</span></p>'

def context(s, warn=False):
    return f"""<div class="context{(' warn' if warn else '')}">{s}</div>"""

def add(title, section, body, insight='', notes='', sources=(), dark=False, appendix=False):
    i = len(slides) + 1
    srcs = list(sources) if not isinstance(sources, str) else [sources]
    notes = NOTE_OVERRIDES.get(i, notes or insight)
    source_html = ''.join((f'<li><a href="../../research/{esc(p, quote=True)}" target="_blank" rel="noopener">{esc(p)}</a></li>' for p in srcs))
    note_html = f'<p>{esc(notes)}</p>' + (f'<h3>Evidence sources</h3><ul>{source_html}</ul>' if srcs else '')
    slides.append(dict(number=i, title=title, section=section, insight=insight, notes=notes, sources=srcs, appendix=appendix))
    return f'''<section class="slide{(' dark' if dark else '')}" data-title="{esc(title, quote=True)}" data-section="{esc(section, quote=True)}" data-appendix="{str(appendix).lower()}" aria-label="{esc(title, quote=True)}"><header><p class="eyebrow">{esc(section)}</p><h2>{title}</h2></header><div class="body">{body}</div>''' + (f'<div class="insight">{insight}</div>' if insight else '') + f'<aside class="speaker-notes">{note_html}</aside></section>'
NEW = 'kaggle-roadmap-2026-10-31/output-analysis.json'
DETAIL = 'kaggle-roadmap-2026-10-31/output-analysis-details.json'
SOURCES = [NEW, DETAIL]
parts = []
coverart = svg('<g transform="translate(28 95)">' + heat(0, 0, 17, 13) + f'<rect class="scan-window" x="80" y="-14" width="86" height="288" fill="none" stroke="#D0DEBB" stroke-width="3"/>' + text(235, 325, 'One substitution per cell', 24, '#D0DEBB') + '</g>', 'Measured HIF1A mutation effects used as the opening image', w=560, h=480)
cover = f'<div class="hero"><div><p class="eyebrow">CT553H · Research briefing</p><h1>Predicting degron<br>mutation effects<br>at residue level</h1><p class="subtitle">Topic introduction, current findings<br>and next research steps</p><div class="identity">Nguyễn Thanh Trọng · B2305615<br>Supervisor: Dr. Hồ Quang Thái<br>Can Tho University</div></div><div class="hero-art">{coverart}<div class="hero-label">From sequence to a map of effects</div></div></div>'
parts.append(add('Degron mutation effects at residue level', 'Introduction', cover, notes='Buổi giới thiệu đề tài và trao đổi tiến độ; không phải bảo vệ hoàn tất. Hình mở đầu dùng ma trận nhãn đo HIF1A. Mục tiêu: người nghe hiểu bài toán, thấy bằng chứng và góp ý hướng tiếp theo.', sources='slide-figures-2026-10-15/example-matrix.json', dark=True))
protein_photo = '<div style="position:absolute;left:2%;top:0;width:170px;text-align:center"><img class="protein-photo animated-gif" style="width:140px;height:140px" src="assets/fam188a.gif" data-gif="assets/fam188a.gif" data-poster="assets/fam188a-poster.png" alt="Rotating Fam188a model illustrating a folded protein"><img class="protein-photo gif-poster" style="width:140px;height:140px;margin:auto" src="assets/fam188a-poster.png" alt="Static Fam188a protein model"><p class="photo-label" style="font-size:16px;white-space:nowrap">Folded protein</p></div>'
parts.append(add('Degrons participate in protein degradation', 'Introduction', full(protein_process() + protein_photo), 'An amino acid substitution can alter the recognition signal.', notes='Sơ đồ là nguyên lý đơn giản hóa UPS. GIF Fam188a của Nikolakhs, CC BY-SA 3.0, chỉ minh họa một protein gấp cuộn, không phải HIF1A/degron đã đo. Hoạt tính của đoạn peptide tách rời có thể khác trong protein nguyên vẹn.'))
parts.append(add('One substitution corresponds to one cell in the effect map', 'Introduction', full(mutation_diagram()), 'Input: WT sequence, position and replacement amino acid. Output: ΔPSI.', notes='WT là trình tự tham chiếu. Ma trận hiển thị 28 vị trí và 20 amino acid; ô WT→WT được mask, có 532 phép thay thật khi đủ dữ liệu. Đây là sơ đồ đầu ra, không phải dự đoán mô hình.', sources='model-selection-pipeline-2026-10-24/README.md'))
parts.append(add('GPS converts reporter measurements into ΔPSI labels', 'Introduction', full(assay_diagram()), '<strong>ΔPSI = PSI(mutant) − PSI(WT).</strong> Positive: a more stable reporter in this assay.', notes='Histogram là minh họa cách đo, không phải số liệu thực nghiệm. PSI của Zhang dùng sáu bin, thang 1–6; thấp là reporter kém bền. Không tự suy dấu ΔPSI thành cơ chế E3 hay khả năng gây bệnh.', sources='full-data-audit/psi-build.json'))
parts.append(add('HIF1A illustrates position-specific mutation effects', 'Introduction', split(image('hif-measured', 'Measured ΔPSI heatmap for the HIF1A peptide'), metric('529 / 532', 'substitutions with measured labels') + '<p>Region <strong>L–A–P–Y–I</strong> stands out in the measured map.</p>' + context('Measured labels, not predictions')), 'Within one peptide, mutation effects differ substantially across positions.', notes='Peptide Q16665_HIF1A_25, vị trí protein 553–580. WT nội tại PSI2.1865; 186 ô ΔPSI≥1. Ví dụ được chọn theo ≥500 ô, nhiều ô dương nhất, hòa lấy ID nhỏ nhất. Đối chiếu motif HIF1A/VHL là y văn, không phải phát hiện cơ chế mới. Ô WT và ô thiếu đều được mask.', sources='slide-figures-2026-10-15/example-matrix.json'))
parts.append(add('The practical goal is to prioritize mutations for experiments', 'Introduction', full(priority_diagram()), 'Effect map → shortlist → experimental validation.', notes='Không coi xếp hạng dự đoán là thay thế thực nghiệm. ClinVar là annotation và động lực nghiên cứu; liên hệ bệnh ở mức residue chưa thiết lập. Các ô trong hình chỉ mô tả lựa chọn, không phải điểm mô hình.', sources='variant-coverage-2026-10-15/README.md'))
parts.append(add('Related approaches address different questions', 'Background and objectives', table(['Approach', 'Main target', 'Role in this project'], [['PAP', 'Whole-peptide activity', 'Score difference after a substitution'], ['Degformer', 'PSI from sequence', 'Already provides mutation-effect maps'], ['MetaDegron', 'Motifs / candidate degrons', 'Adds annotations and E3 context'], ['This project', 'Effects of individual substitutions', 'Measured labels, baselines and group-based evaluation']]), 'Focus: predictive evidence, evaluation and a useful analysis tool.', notes='Không nhận ma trận hoặc web là tính mới độc quyền. Khác endpoint thì không so trực tiếp AUROC. MetaDegron có một classifier dùng chung với lựa chọn motif/E3; không phải mọi menu là một lớp E3 học độc lập.', sources='metadegron-analysis-2026-10-21/comparison-and-positioning.md'))
parts.append(add('Three objectives connect research to an analysis tool', 'Background and objectives', full(process(['Traceable data', 'Evaluated methods', 'Analysis tool'], ['Reconstruction / QC', 'Baselines / stability', 'Effect map / ranking / export'])), 'Main scope: single-substitution effects in 28-residue reporter peptides.', notes='Không đặt dự đoán E3 hay chẩn đoán biến thể gây bệnh làm nhiệm vụ chính. Không có phép đo sinh học mới. Công cụ phục vụ hình thành giả thuyết và lựa chọn thí nghiệm.', sources='model-selection-pipeline-2026-10-24/README.md'))
parts.append(add('Questions guiding the current research', 'Background and objectives', full(process(['Label distribution', 'Context and ESM', 'Prediction head', 'Source transfer', 'Practical utility'], ['Which training domain?', 'Where is the signal?', 'Does convolution help?', 'Can transfer help?', 'Useful and reliable?'])), 'Each question needs an appropriate comparison and clear limits of inference.', notes='Sơ đồ là quan hệ nghiên cứu, không là lịch chạy. Các kết quả được tổ chức theo câu hỏi, không theo mã phiên hay thứ tự thời gian.', sources='kaggle-roadmap-2026-10-31/EXECUTION-PROTOCOL.md'))
parts.append(add('Each data source serves a defined role', 'Data and approach', full(sources_diagram()), 'Tile-level scores and annotations are not mutation-effect labels.', notes='Core v3 chỉ chứa Zhang và UniProt, không chứa ClinVar/Koren/Larsen/MetaDegron hoặc weights. Larsen/MaveDB là nguồn khảo sát với endpoint khác. Phân biệt nguồn đã tải, đã audit và đã dùng fit.', sources=['kaggle-roadmap-2026-10-31/DATASET.md', 'full-data-audit/README.md']))
parts.append(add('The two mutation designs provide complementary coverage', 'Data and approach', full(designs()), 'Scanning expands context coverage; saturation covers all substitution types.', notes='Scanning có phép thay là hàm của WT: hướng R/A/S, tổng20 cặp có hướng trong380 cặp không đồng nghĩa. Hình biểu thị thiết kế lý tưởng, không khẳng định mọi ô đều qua QC.', sources='scan-sat-merge-2026-10-23/README.md'))
parts.append(add('Each assay needs the correct WT reference', 'Data and approach', full(label_pipeline()), 'Keep sources, conditions and replicates separate when deriving effect labels.', notes='Saturation không có mut0; dùng trung vị ô đồng nghĩa từng nửa. Scanning dùng mut0 đúng replicate. Không lấy BAG6 WT làm mốc saturation. PSI dựng lại261865 giá trị khớp tác giả trong5e-7 khi mô phỏng điều kiện tái lập.', sources=['full-data-audit/psi-build.json', 'full-data-audit/saturation-matrix.json']))
noise = svg(box(15, 120, 185, 95, 'Same substitution') + edge(210, 165, 340, 65) + edge(210, 165, 340, 265, BLUE) + box(350, 20, 225, 95, 'First measurement') + box(350, 220, 225, 95, 'Second measurement', color=BLUE), 'Repeated measurements and label reliability', w=600, h=350)
parts.append(add('Label reproducibility constrains how results should be interpreted', 'Data and approach', split(noise, metric('0.8335', 'correlation of ΔPSI across the two saturation halves') + '<p>235 peptides · 122,412 cells</p><p class="small">Peptide-level reliability differs from position-level reliability.</p>'), 'Model residuals can contain both signal and measurement noise.', notes='0.8335 là Pearson giữa hai nửa trên cohort saturation theo audit. Không so noise_share của tổng phương sai với noise_share của phần dư như cùng đại lượng. Replicate là mốc độ tin cậy của phép đo, không phải trần tuyệt đối cho mọi estimator.', sources=['full-data-audit/saturation-matrix.json', 'full-data-audit/replicate-audit.json']))
parts.append(add('Split by protein group to assess generalization', 'Data and approach', full(groups_diagram()), 'Restricted domain: 91 peptides. Full range: 235 peptides in 221 protein groups.', notes='Hai thiết kế có population, eligibility và preprocessing khác, không nối AUROC thành một đường tiến bộ. V3 dùng5outer folds và3seed inner-validation; các transform chỉ fit trong train, epoch chọn rồi khởi tạo lại refit. Nhóm có homology heuristic, không chứng minh độc lập sinh học tuyệt đối.', sources='kaggle-roadmap-2026-10-31/EXECUTION-PROTOCOL.md'))
parts.append(add('Prediction error, ranking and experimental budget are distinct goals', 'Data and approach', full(metrics_diagram()), 'Compute metrics per peptide; bootstrap confidence intervals by protein group.', notes='V3 MAE có235 peptide; event dương Δ≥1 có184peptide đủ điều kiện, âm Δ≤−1 có110. Mỗi lớp phải có≥3ô. Bootstrap5000 theo nhóm, không theo122412ô. AUROC không là accuracy; AP cần đọc với tần suất event.', sources=NEW))
parts.append(add('Local context adds information beyond the substitution itself', 'Findings and interpretation', split(image('context', 'Context ablation on scanning data'), '<p><strong>Most of the gain</strong> comes from local amino acid composition.</p><p>Retaining order adds a smaller benefit.</p>' + context('Evaluation on scanning')), 'A context baseline is essential before adding model complexity.', notes='M0 pair+composition0.8393; unordered0.8625; ordered±3 0.8682. Ordered−M0 +.0289 CI[.0264,.0313]. Trung bình AUROC các seed trong nguồn này, không gán là ensemble v3. Mô hình tuyến tính composition hằng trong peptide không tự đổi thứ hạng giữa vị trí có cùng phép thay.', sources='residue-task-derisk-2026-10-15/model.json'))
parts.append(add('Training across the PSI range reduces Ridge regression error', 'Findings and interpretation', split(image('training-range', 'Ridge MAE by the training PSI range'), metric('5.94%', 'lower MAE: full range versus training only at PSI ≤ 4') + '<p class="small">MAE difference: −0.0258 PSI<br>Adjusted CI: −0.0338 to −0.0183.</p>'), 'Error improves, but the adjusted interval does not establish a minimum 0.02 PSI reduction.', notes='Cùng235peptide test,221nhóm. Hai contrast Q1 dùng CI97.5% Bonferroni. Arm hẹp vẫn dùng validation toàn dải. Không đưa PSI(WT) vào feature hoặc dùng nó clip dự đoán.', sources=NEW))
parts.append(add('Full-range training benefits high-PSI peptides most', 'Findings and interpretation', split(image('strata', 'MAE across four PSI strata for three training distributions'), '<p>High-PSI peptides benefit more.</p><p><strong>Balancing the data</strong> can trade off performance in the low-PSI domain.</p>'), 'Choose the training distribution for both the overall objective and the intended domain.', notes='Các strata có91/85/36/23peptide. Ridge full ở miền≤3 không thấy giảm quáguardrail. Cân bằng có cận CI AUROC hơi vượt−.01. >5 không có eventdươngΔ≥1 nên Positive-event AUROCnull đúng. Khi soCNN toàn dải/chỉ≤4, miền≤3 MAE tăng.00870 CI[.00329,.01411], không suy guardrailRidge sangCNN.', sources=SOURCES))
parts.append(add('ESM adds signal to the context baseline', 'Findings and interpretation', split(image('esm-linear', 'Positive-event AUROC for context Ridge, ESM features and nested selection'), '<p>ESM-only and context-plus-ESM trade off MAE against ranking.</p><p><strong>Validation-based selection</strong> evaluates a selection procedure.</p>'), 'Only ESM2-35M was evaluated on the full-range benchmark; pLM families cannot yet be ranked.', notes='W5+ESM−W5 AUROC+.012548 CI95[.006216,.019670]. Nested selection MAE.397525 vsW5.407803, AUROC improvementCIphủ0. Không lấy fixedrecipe tốt nhất thay cho nested procedure. Bảng nhiều cỡ ESM trên thiết kế khác để phụ lục.', sources=NEW))
parts.append(add('A CNN adds value after the ESM representation', 'Findings and interpretation', split(image('heads', 'MAE of one-hot and ESM heads trained across the full PSI range'), '<div style="height:190px">' + head_diagram() + '</div><p>Compared with pointwise:<br><strong>MAE decreases by 0.00534 PSI.</strong></p>'), 'The matched-input comparison supports position mixing; one-hot results remain unresolved.', notes='ESMCNN−pointwise MAE CI95[−.010173,−.000899], AUROC+.011289CI[.003434,.019133]. Head parameter36833vs57185 nên chưa cô lập sức chứa. CI khácQ1 là mô tả, chưa điều chỉnh toàn khảo sát.', sources=NEW))
parts.append(add('Multiple windows have not shown a clear advantage over one', 'Findings and interpretation', f"""<div class="stack"><div style="height:185px">{head_diagram(True)}</div>{image('mcnn-ci', 'MAE-difference CI: balanced multi-window model versus full-range CNN')}</div>""", 'The best development MAE alone is insufficient to select a final model.', notes='mCNNE MAE.383846vsCNND.384354, chênh−.000508CI95[−.003157,+.002223]. CùngD mCNN−CNN +.000639CIphủ0. B/D/E là lựa chọn phân bốtrain nội bộ, màn chiếu dùng tên đầy đủ. CNN chỉPSI≤4 đánggiữ nếuưu tiênmiềnthấp; toàn dải so nó chưađảm bảoguardrail.', sources=SOURCES))
parts.append(add('Learning tile scores well does not guarantee mutation-effect transfer', 'Findings and interpretation', split(transfer_diagram(), metric('0.8098', 'AUROC after tile pretraining') + metric('0.8175', 'same encoder, random initialization')), 'The negative result applies to the tested transfer design, not to all pretraining strategies.', notes='Cùngthiếtkế ext4 trên91peptide. Sources212616tile; encoderpretrainPearson.864 nhưng downstreampre−rand−.0077CI[−.0163,+.0006]. Nhánhpre−ridge−.011CIâm. Không so thẳng với số v3 hoặc quy thành pretraining pLM vô ích.', sources='pretrain-p3-2026-10-22/results.json'))
parts.append(add('Scanning pretraining helps beyond the observed substitution types', 'Findings and interpretation', split(image('transfer', 'MAE of scratch and scanning-pretrained CNNs'), '<p><strong>20 observed types:</strong><br>MAE decreases by 0.00772.</p><p><strong>360 remaining types:</strong><br>MAE decreases by 0.00631.</p>' + context('Both descriptive CIs favor improvement')), 'Quality weighting increases error; averaging replicates has no clear advantage over replicate 1.', notes='Transfer onehotCNN, không làESM+scanning. Cohort20 có6433ô;360 có115979ô,cùng235peptide221nhóm. Mean12−rep1CIphủ0. Quality−satonly +.004010. Scan_T không thamgiafit; kếtquả ởsaturationOOF khônglàtransferT.', sources=SOURCES))
parts.append(add('Degformer comparisons require overlap and training-data audits', 'Findings and interpretation', split(image('degformer', 'Group-clean Degformer and Ridge evaluated on the same 91 peptides'), metric('91 / 91', "WT peptides seen in the published checkpoint's training data") + '<p>Masking duplicate cells does not create unseen peptides.</p>'), 'Group-clean retraining reaches AUROC 0.8068, with no demonstrated advantage over Ridge.', notes='Checkpoint.9248có88.12%ôtrùng. Retrainsạch.806775, Ridgeext.820822, delta−.014CI[−.0283,+.0010]=>khôngphânbiệtđược. Retrainkiếntrúcchỉ47knhãn.749978làthiếtkếriêng. Không coi chênhcheckpoint/retrain là causal leakage-only effect vì các điều kiện thay đổi.', sources='r1-degformer-clean-2026-10-22/run-kaggle-20261022/results.json'))
parts.append(add('Ranking focuses the experimental budget on promising substitutions', 'Findings and interpretation', split(image('utility', 'Positive-event precision by top-k budget for Ridge and the ESM CNN'), metric('58.24%', 'positive-event precision in the top 5%') + '<p>Context Ridge: 51.89%.</p><p class="small">Negative events remain harder; consider their lower prevalence.</p>'), 'This demonstrates prioritization utility, not calibrated probabilities.', notes='Precision macro trong184peptideeligibleplus. Top10CNN49.04%vsRidge44.29%. AP+.50947,rate+.124697 trêncùngcohort. AP−.213667,rate−.027336trên110peptide;precisiontop5−16.77%. Không dùngtopkzero-scorephụthuộctiebreaklàmrandom.', sources=NEW))
parts.append(add('Model selection also depends on stability and cost', 'Findings and interpretation', split(image('folds', 'Ridge and ESM CNN MAE across five outer folds'), metric('156 / 235', 'peptides with lower MAE than Ridge') + '<p><strong>9.33 hours</strong> of completed task time.</p><p class="small">The two frozen tasks account for 7.23 hours.<br>LoRA has no complete OOF results yet.</p>'), 'Ensembling reduces variance; seeds and folds are not independent datasets.', notes='Tổngtaskseconds9.3265h,77.52%stage11frozen; chưa gồmLoRAdở. Chỉseed17frozenB/D. 35taskcomplete,1runningtrongsnapshotkhôngchứngminhremotecònsống. Frozenstage11chạybackbonemỗibatch; cache làhướngtốiưucầnparity, không cóbenchmarktăngtốc. Sources chốt ởsnapshotKaggle, khônggộpjoblocalđangchuẩnbị.', sources=SOURCES))
parts.append(add('Calibration maps regression scores to event probabilities', 'Findings and interpretation', f"""<div class="charts-two"><div>{context('Ridge evaluated on the 91-peptide domain')}{image('calibration', 'Reliability plot for Ridge with Platt calibration')}</div><div>{image('brier', 'Brier scores for prevalence and calibrated Ridge')}</div></div>""", 'Calibration evidence belongs to the tested model; the CNN needs its own calibration procedure.', notes='RidgeM3ext4PlattBrier.0925vsconst.1139,BSS.188. ScoreΔPSIclippedkhôngtựlàprobability. Reliabilitythiênthấpdo fitpoolkhácmiềntest; khônggọicalibrationhoànhảo. Protocolv3crossfitcalibrationkhácchitiếtP6, khôngmangnguyêncalibratorsangCNN.', sources='calibration-p6-2026-10-22/results.json'))
parts.append(add('Assess the applicability domain alongside predictions', 'Findings and interpretation', full(domain_diagram()), 'PSI differs across sources; a peptide model does not establish whole-protein effects.', notes='CổngR3khảosátchomiềntrainPSI≤4. PSIpeptidomescreenlệchWTintrinsic~.9,khôngdùngrawthreshold4trực tiếp. ÁpquaR3khoảng26%in9%border65%out. FullPSIkhôngtựchocổngđộcậymớivàkhôngchứngminhphục vụmọiprotein. Tíchhợpgateappcònmở.', sources='r3-domain-gate-2026-10-22/run-kaggle-20261022/results.json'))
ui = '<div class="ui-frame"><img src="assets/workspace-prototype.png" alt="Workspace design prototype showing the substitution map and cell inspector"><div class="ui-highlight" style="left:2%;top:15%;width:70%;height:76%"></div><div class="ui-badge">Design prototype · illustrative data · no backend connection</div></div>'
parts.append(add('The tool combines the effect map and shortlist in one workflow', 'Analysis tool', ui, 'Enter a peptide → inspect the map → select substitutions → annotate → export.', notes='Ảnhchụpprototypeworkspaceuiv2hiệnhành. Tấtcảscore/probabilitydemo làsyntheticfixture; khônglàmodeloutput. BaselineReact/FastAPIđãcómãriêng; prototypekhôngnghiệmthubatchprojectsimports. Chỉdùngảnhthiếtkếđểminhhọaluồng.', sources='../system/design/workspace-ui-v2/README.md'))
parts.append(add('A local application keeps results with their provenance', 'Analysis tool', full(architecture()), 'Each result carries its model version, data sources and intended scope.', notes='StackđãchốtReactTypeScriptFastAPIlocal. SQLiteđãdùngchobaseline; PostgreSQLvàdurableworkspacelàphạmvicầntriểnkhaikiểm. KhôngcóyêucầupublishVPS. Sơđồkiếntrúcđịnhhướng, khônglàxácnhậnmọimoduleđãhoànthành.', sources='../system/README.md'))
parts.append(add('The software baseline provides a foundation for extension', 'Analysis tool', table(['Implemented baseline', 'In development / integration needed'], [['Single peptide · effect map · ranking', 'Batch and whole-protein workflows'], ['Exports · model and source pages', 'Persistent projects and history'], ['Inference checked against the runner', 'Import and compare experimental data'], ['React / FastAPI baseline code', 'New model · calibration · domain assessment']]), 'Baseline tests retain their original scope; extensions require separate verification.', notes='Baselinebackend149pytest/frontend131vitestlàbằngchứnglịchsửghiởsystemREADME,chưachạylạitrongphiêndựngslide. Scopev0.2đãthiếtkếchưatriểnkhaixong; R3gatechưaloadđúngtrongapp. Tránhtrìnhtấtcảplannedendpointlàđãcó.', sources='../system/README.md'))
parts.append(add('Completed work provides a foundation for the next research steps', 'Progress and next steps', full(process(['Data and evaluation', 'Experimental findings', 'Analysis tool'], ['Labels / QC / protein groups', 'Context / ESM / source transfer', 'Inference / UI / provenance'])), 'Development findings and explicit limitations now guide the next steps.', notes='KhôngtựđóngG2/G3hoặctuyênbốhoàntấtluậnvăn. Closegópđangxâydựnggồmbenchmark/phươngpháp/đánhgiá/phầnmềm,khôngbắtbuộckiếntrúcmới. Các kết quả âm có vai trò thu hẹp hướng nghiên cứu.', sources=[NEW, 'model-selection-pipeline-2026-10-24/README.md']))
nextsvg = svg(text(50, 60, 'Model research', 26, DARK, anchor='start', weight=600) + box(30, 100, 225, 90, 'Lock the candidate') + edge(265, 145, 370, 145) + box(385, 100, 290, 90, 'Refit and calibrate') + edge(685, 145, 790, 145) + box(805, 100, 250, 90, 'Evaluate transfer') + text(50, 290, 'Software development', 26, BLUE, anchor='start', weight=600) + box(30, 330, 225, 76, 'Model integration', color=BLUE) + edge(265, 368, 370, 368, BLUE) + box(385, 330, 290, 76, 'Workflows and storage', color=BLUE) + edge(685, 368, 790, 368, BLUE) + box(805, 330, 250, 76, 'Verify practical use', color=BLUE), 'Research and software development follow their respective dependencies', h=450)
parts.append(add('Next priorities: lock the model choice and evaluate transfer', 'Progress and next steps', full(nextsvg), 'LoRA and structure remain optional branches, guided by the question and available resources.', notes='FinalpromotiontựđộnghiệnchỉW5; CNNcầnmodel-specificrefitexport. Khóarecipe/calibrationtrướckhiđọcT. Sourcesscanningđãthăm dòtronglịchsử,khônggọiđộclậphoàntoàn. KhôngcầnchờLoRAđểhoànthiệnbenchmarklõi.', sources='kaggle-roadmap-2026-10-31/EXECUTION-PROTOCOL.md'))
questions = svg(text(50, 75, 'Research priorities', 34, '#FFFFFF', anchor='start', weight=600) + text(50, 125, 'Full-range accuracy or prioritizing strong effects?', 25, '#D0DEBB', anchor='start') + text(50, 230, 'Validation scope', 34, '#FFFFFF', anchor='start', weight=600) + text(50, 280, 'Which source and generalization scope are appropriate?', 25, '#D0DEBB', anchor='start') + text(50, 385, 'Software scope', 34, '#FFFFFF', anchor='start', weight=600) + text(50, 435, 'Which features should be prioritized next?', 25, '#D0DEBB', anchor='start'), 'Three topics for discussion with the lecturer', h=480)
parts.append(add('Discussion: research direction and next steps', 'Faculty discussion', full(questions), notes='Mời giảng viên góp ý mục tiêu và hướng ưu tiên. Đây là buổi giới thiệu/tiến độ, không phải nghiệm thu toàn bộ đề tài. Có thể mở overview hoặc phụ lục để trao đổi chi tiết.', dark=True))
assert len(slides) == 34

def ap(title, body, insight='', notes='', sources=()):
    return add(title, 'Reference appendix', body, insight, notes, sources, appendix=True)
parts.append(ap('Terminology and how to read the metrics', full(metrics_diagram()), 'Residue: an amino acid at a position. WT: reference sequence. OOF: out-of-fold predictions.', sources='model-selection-pipeline-2026-10-24/README.md'))
parts.append(ap('Label construction and quality-control details', full(label_pipeline()), 'Synonymous constructs provide intrinsic WT references; missing cells are masked and conditions kept separate.', sources=['full-data-audit/psi-build.json', 'full-data-audit/saturation-matrix.json']))
parts.append(ap('Reliability depends on the level of analysis', table(['Measure', 'Scanning', 'Saturation'], [['ΔPSI across replicates', 'Pearson 0.7229', 'Pearson 0.8335'], ['Reproducibility of positive labels', 'Position Jaccard: 0.4965', 'Cell Jaccard: 0.6596'], ['Population', 'Scanning-specific filters', '235 peptides / 122,412 cells']]), 'Cohorts and position/cell definitions differ; this is not a paired comparison.', notes='SốpsiAgreement0.9239trongREADMEfullauditlàmốcsoWTkhôngphảiđúngrep1rep2; dùngđúngtrườngΔPSI. Khônggọi75.9%phầndưnhiễuvà16.7%tổngphươngsailàcùngmẫusố.', sources=['full-data-audit/replicate-audit.json', 'full-data-audit/saturation-matrix.json']))
parts.append(ap('Composition models cannot distinguish every position', full(context_diagram()), 'Within a peptide, a composition-only model assigns the same score to the same substitution type.', notes='Bấtbiếnápdụngchocompositionthuầntúy; khônggánchotoànPAPcókênhCterminal. M0thực tếcó40chiềupair+20composition. Oracleđọctestkhôngphảitestperformance.', sources=['composition-context-audit.md', 'residue-task-derisk-2026-10-15/model.json']))
parts.append(ap('Learning curves must distinguish individual models from ensembles', split(image('learning-curve', 'Mean single-seed MAE by the fraction of training groups'), '<p>Training subsets differ across seeds.</p><p>An ensemble may see a larger union of data than each member.</p>'), 'Clustering sensitivity is a separate check; identical partitions are not additional evidence.', sources=[DETAIL, 'recluster-sensitivity-2026-10-22/results.json']))
parts.append(ap('The tested interaction designs did not consistently beat the baseline', table(['Design', 'AUROC on the 91-peptide domain', 'Interpretation'], [['Ridge', '0.8082', 'Baseline under the same design'], ['Gate + residual PAP', '0.8002', 'The gate effect changes sign across seeds'], ['FiLM', '0.8028', 'No demonstrated improvement over Ridge'], ['Bilinear', '0.7933', 'Lower performance than Ridge']]), 'These results concern the tested designs, not all possible nonlinear interactions.', sources=['g2-saturation-2026-10-18/results.json', 'g2-extension-2026-10-18/e2-candidates.json']))
parts.append(ap('Removing duplicate cells does not remove peptide-level overlap', split(image('degformer', 'Group-clean Degformer retraining and baselines'), '<p>The published checkpoint contains 42,163 / 47,847 mutation cells in training.</p><p>WT sequences of all 91 peptides have already been seen.</p>'), 'Evaluate on held-out peptides or protein groups.', sources=['g2-saturation-2026-10-18/results.json', 'r1-degformer-clean-2026-10-22/run-kaggle-20261022/results.json']))
parts.append(ap('ESM scale comparisons belong to a separate evaluation design', table(['Additional Ridge representation', 'AUROC · 91-peptide domain', 'Finding'], [['ESM2 8M', '0.8214', 'Confidence interval remains inconclusive'], ['ESM2 35M', '0.8234', 'Confidence interval remains inconclusive'], ['ESM2 150M', '0.8207', 'Confidence interval remains inconclusive'], ['ESM2 650M', '0.8230', 'Confidence interval remains inconclusive']]), 'Do not directly compare these AUROCs with the full-range benchmark.', notes='SốlấytừR6D,bổsungchoM3ext4. Cáccheckpointkháctrongregistrykhôngđồngnghĩađãđánhgiá. V3fullWchỉESM235M. 35Mpreflightforwardshape2x28x480vàfinite/repeatpass.', sources='r6-ladder-scan-2026-10-23/run-kaggle-20261023/results.json'))
explorer = '<div class="metric-picker"><button data-metric="mae" aria-pressed="true">MAE</button><button data-metric="auroc" aria-pressed="false">Positive-event AUROC</button><button data-metric="ap" aria-pressed="false">Positive-event AP</button></div><div class="chart-explorer"><canvas id="recipeChart" role="img" aria-label="Interactive comparison of model configurations; switch metrics using the three buttons"></canvas><img class="figure print-fallback" src="assets/tradeoff.svg" alt="MAE and AUROC comparison of model candidates"></div>'
parts.append(ap('Inspect several metrics for the same candidates', explorer, 'Scores use mean predictions from three seeds and remain development analysis.', sources=NEW))
parts.append(ap('Scanning transfer: assess observed and remaining substitution types', full(image('transfer-pairs', 'Confidence intervals for scanning transfer across 20 and 360 substitution types')), 'The 20-type cohort has 6,433 cells; the 360-type cohort has 115,979 cells. Both cover 235 peptides.', notes='Mỗi peptidechỉtínhôtrongcohort. AUROCdươngeligible114và184nênkhôngsotrực tiếpmacrogiữahai cohort. HaiCIởhìnhlàhậukiểmmôtảkhôngđiềuchỉnhđa kiểmđịnh.', sources=DETAIL))
parts.append(ap('ClinVar supports region-level motivation, not residue-level validation', split(priority_diagram(), metric('2.15', 'region-level pathogenic-versus-benign odds ratio') + '<p>Stratified by protein.</p><p class="small">A residue-level link between ΔPSI and pathogenicity has not been established.</p>'), 'ClinVar provides context and annotation, not ΔPSI ground truth.', notes='ORmh2.14783CI[2.07193.2.22651],3114tầng. Khôngliênhệnhânquả. Sat_exactAUC.6738CI[.489,.831]n51chưađạt; scan_posAUC.5166CIphủ.5. SourcesClinicalkhôngdùngchọnmodel.', sources=['variant-coverage-2026-10-15/enrichment.json', 'variant-coverage-2026-10-15/README.md']))
parts.append(ap('E3 labels are too sparse for an E3-conditioned task', table(['Adaptor / E3', 'Peptides in the audit'], [['KLHL15', '13'], ['BAG6', '4'], ['ASB7 / FEM1B', '2 per group'], ['Other groups', 'Mostly one peptide each']]), 'Only one group has at least five peptides; menu choices are not learnable class counts.', sources='e3-labels-audit/README.md'))
parts.append(ap('External sources need endpoint and usability audits', table(['Sources', 'Potential use', 'Limitations'], [['Koren', 'Mutations in C-terminal degrons', 'Different scale / length; only 5 new groups'], ['Larsen', 'Nuclear tile activity', 'No additional mutation ΔPSI labels'], ['MaveDB', 'Whole-protein variant effects', 'Endpoint and structure need separate audits']]), 'Auditing a source does not establish external validation of the current model.', notes='Korenchưađánhgiámôhình,vaitròcandidatetestnhỏvàquyềnsửdụngnộibộ. MaveDBexposureexploratorycònGCKassay/dimerconfound,cầnchạylạitrướckếtluậnmạnh. SaProttrue3Di chưaoutput; weightskhôngthaymappingstructure.', sources=['koren-s4-audit-2026-10-22/results.json', 'larsen-nuclear-and-risks-2026-10-15/README.md', 'architecture-check/README.md']))
parts.append(ap('Calibration and domain assessment answer different questions', f"""<div class="charts-two"><div>{context('Are event probabilities reliable?')}{image('calibration', 'Reliability of the Ridge model')}</div><div>{context('Is the peptide within the applicability domain?')}{domain_diagram()}</div></div>""", 'Reassess both when the model or data scope changes.', sources=['calibration-p6-2026-10-22/results.json', 'r3-domain-gate-2026-10-22/run-kaggle-20261022/results.json']))
parts.append(ap('Reproducibility connects data, models and served results', full(process(['Hashed sources', 'Code / protocol', 'OOF and checkpoints', 'Inference / export'], ['Data version', 'Configuration / splits', 'Mode official / smoke', 'Model card / provenance'])), 'The manifest verified 2,986 files; baseline app tests do not validate new features.', notes='Integrity2986files3065290891bytes83OOF47recipes; reproducedanalysisexact. Những con sốtestapp149backend131frontendlàhistoricalbaselinekhôngchạylạitrongtaskslides. SnapshotKaggleupdated2026-11-01T11:18:07Z,khônggộplocalruntimekhác.', sources=[NEW, '../system/README.md']))
refs = '<div class="references"><div><a href="../../../../resources/papers/analyzed-papers/README.md">Related work</a><p>Zhang · Voutsinos · Degformer · MetaDegron · Larsen</p></div><div><a href="evidence.json">Results and source hashes</a><p>Research JSON, standalone figures and chart data</p></div><div><a href="slide-sources.json">Slide-level evidence</a><p>Comparison conditions, interpretation notes and result sources</p></div><div><a href="design-research.md">Template and style research</a><p>Penn State / Harvard Catalyst · Slidev Academic · EMBL</p></div><div><a href="asset-notices.md">Asset credits and licenses</a><p>Protein GIF · fonts · Chart.js · original diagrams</p></div><div><a href="../../system/README.md">Software scope</a><p>Existing baseline and features in development</p></div></div>'
parts.append(ap('References and evidence are organized by topic', refs, "Open Notes for the current slide's sources and interpretation limits.", notes='Khônggắnfootnotelênmọislidetheoyêucầu. Toànbộnguồnđượctậptrungtạiphụlục,notevàJSON. Websiteđượcdùngkhảosátdesigntrướckhidựng,khôngbổsungclaimhiệunăngmodel.', sources=NEW))
assert len(slides) == 50
html = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>Degron-footprint · Introduction and research discussion</title><link rel="stylesheet" href="deck.css"><script src="data.js" defer></script><script src="vendor/chart.umd.js" defer></script><script src="deck.js" defer></script></head><body><main id="viewport" aria-label="Topic introduction and research discussion slide deck"><div id="deck">' + ''.join(parts) + '</div></main><div id="progress" aria-hidden="true"></div><nav id="toolbar" aria-label="Presentation controls"><button id="prev" aria-label="Previous slide">←</button><span class="counter" id="counter"></span><button id="next" aria-label="Next slide">→</button><button id="overview-button">Overview</button><button id="notes-button">Notes</button><button id="motion" aria-pressed="false">Pause motion</button><button class="long" id="full-button">Fullscreen</button><button id="help-button" aria-label="Keyboard shortcuts">?</button></nav><div id="status" role="status" aria-live="polite"></div><dialog id="overview"><button class="close">Close</button><h2>Overview · 34 main slides + 16 appendices</h2><div id="overview-grid"></div></dialog><dialog id="notes"><button class="close">Close</button><h2 id="notes-title"></h2><div id="notes-body"></div></dialog><dialog id="help"><button class="close">Close</button><h2>Presentation controls</h2><p>← → / Space: change slides<br>O: overview · N: notes and sources<br>M: pause / resume motion · F: fullscreen<br>Home: first slide · End: discussion<br>On a phone: swipe horizontally or use the arrow buttons.<br>Print from the browser for a static PDF of all 50 slides.</p></dialog></body></html>'
start = html.find('<header>')
end = html.find('</header>', start)
html = html[:start] + html[end + 9:]
(HERE / 'index.html').write_text(html, encoding='utf8')
(HERE / 'slide-sources.json').write_text(json.dumps(slides, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
(HERE / 'speaker-notes.md').write_text('# Speaker notes\n\n' + ''.join((f"## {s['number']}. {s['title']}\n\n{s['notes']}\n\nSources: " + ', '.join(s['sources']) + '\n\n' for s in slides)), encoding='utf8')
print(f'Built {len(slides)} slides: 34 main, 16 appendices.')
