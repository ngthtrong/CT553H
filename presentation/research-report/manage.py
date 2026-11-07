#!/usr/bin/env python3
"""Maintain the single official editable CT553H PowerPoint and its PDF.

build creates the first deck only. revise --slides <semantic ids> replaces only
explicitly named slides in the existing PPTX. render always exports that PPTX.
The PPTX, including manual edits, is the maintained document of record.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import uuid
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'CLAUDE.md').exists())
PRES = ROOT / 'presentation'
PPTX = PRES / 'Degron_Research_Report.pptx'
PDF = PPTX.with_suffix('.pdf')
SKILL = PRES / 'templateCTU/ctu-slides'
V3 = ROOT / 'research/kaggle-roadmap-2026-10-31'
TAG = 'CT553H:'
EN_TITLE_SOURCE = ROOT / 'report/config/metadata.tex'
VI_TITLE_SOURCE = ROOT / 'proposal/proposal.md'

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def write(path, obj):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def project_titles():
    """Read the author-approved titles from their document metadata authorities."""
    match=re.search(r'\\newcommand\{\\ThesisTitle\}\{([^}]+)\}',EN_TITLE_SOURCE.read_text())
    if not match:raise ValueError('English thesis title is missing from report metadata.')
    header=VI_TITLE_SOURCE.read_text().split('---',2)[1].splitlines()
    start=next(i for i,line in enumerate(header) if line.startswith('subtitle:'))
    lines=[]
    for line in header[start+1:]:
        if line and not line.startswith((' ','\t')):break
        if line.strip():lines.append(line.strip())
    if not lines:raise ValueError('Vietnamese thesis title is missing from proposal metadata.')
    return match.group(1),' '.join(lines)

def engine():
    spec = importlib.util.spec_from_file_location('ctu_slides', SKILL / 'scripts/ctu_slides.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def inputs():
    """Read existing evidence only; no training, checkpoint loading or bootstrap."""
    import pandas as pd
    d = {
        'local': read(V3 / 'local-output-analysis.json'),
        'kaggle': read(V3 / 'output-analysis.json'),
        'details': read(V3 / 'output-analysis-details.json'),
        'build': read(V3 / 'dataset-build.json'),
        'review': read(ROOT / 'research/output-review-2026-11-06/results.json'),
        'audit': read(ROOT / 'research/progress-review-2026-11-06/local-audit.json'),
        'priority': read(ROOT / 'research/oof-prioritization-2026-11-07/results.json'),
    }
    base = ROOT / 'data/processed/v3-fullpsi/tables'
    d['sat'] = pd.read_parquet(base / 'saturation-cells.parquet')
    d['peptides'] = pd.read_parquet(base / 'peptides.parquet')
    d['record'] = d['sat'].sort_values(['peptide_id','position_1based','mut_aa']).iloc[0]
    assert d['record'].cell_id == 'sat:A2RUQ5_C17orf102_2:1:A'
    assert len(d['sat']) == 122412 and d['sat'].peptide_id.nunique() == 235
    assert d['local']['data_identity'] == d['kaggle']['data_identity']
    assert d['priority']['cohort'] == {'cells': 122412, 'peptides': 235, 'groups': 221}
    assert len(d['review']['recipes']) == 88
    return d

def source_records():
    # Every local locator is resolved against this file, not historical topics/ paths.
    rows = [
        ('P1', 'Zhang et al. (2023)', 'Z. Zhang, B. Sie, A. Chang, Y. Leng, C. Nardone, R. T. Timms, S. J. Elledge. Elucidation of E3 Ubiquitin Ligase Specificity Through Proteome-wide Internal Degron Mapping. Molecular Cell 83(18), 3377–3392.e6 (2023).', '10.1016/j.molcel.2023.08.022', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC10594193/'),
        ('P2', 'Voutsinos et al. (2026)', 'V. Voutsinos et al. A near-complete map of human cytosolic degrons and their relevance for disease. Science Advances 12(6), eadz3483 (2026).', '10.1126/sciadv.adz3483', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC12880521/'),
        ('P3', 'Zheng et al. (2024)', 'M. Zheng et al. MetaDegron: multimodal feature-integrated protein language model for predicting E3 ligase targeted degrons. Briefings in Bioinformatics 25(6), bbae519 (2024).', '10.1093/bib/bbae519', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC11491831/'),
        ('P4', 'Szulc et al. (2024)', 'N. A. Szulc et al. DEGRONOPEDIA: a web server for proteome-wide inspection of degrons. Nucleic Acids Research 52(W1), W221–W232 (2024).', '10.1093/nar/gkae238', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC11223883/'),
        ('P5', 'Lin et al. (2023)', 'Z. Lin et al. Evolutionary-scale prediction of atomic-level protein structure with a language model. Science 379(6637), 1123–1130 (2023).', '10.1126/science.ade2574', 'https://doi.org/10.1126/science.ade2574'),
        ('P6', 'Hu et al. (2022)', 'E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, W. Chen. LoRA: Low-Rank Adaptation of Large Language Models. ICLR (2022); arXiv:2106.09685.', '', 'https://arxiv.org/abs/2106.09685'),
        ('P7', 'Hoerl & Kennard (1970)', 'A. E. Hoerl, R. W. Kennard. Ridge regression: biased estimation for nonorthogonal problems. Technometrics 12(1), 55–67 (1970).', '10.1080/00401706.1970.10488634', 'https://doi.org/10.1080/00401706.1970.10488634'),
        ('P8', 'Bernett et al. (2024)', 'J. Bernett et al. Guiding questions to avoid data leakage in biological machine learning applications. Nature Methods 21(8), 1444–1453 (2024).', '10.1038/s41592-024-02362-y', 'https://doi.org/10.1038/s41592-024-02362-y'),
        ('P9', 'Larsen et al. (2025)', 'F. B. Larsen et al. Comprehensive degron mapping in human transcription factors. bioRxiv, version 1 (2025); preprint cited, not a confirmed peer-reviewed version.', '10.1101/2025.05.16.654404', 'https://doi.org/10.1101/2025.05.16.654404'),
        ('P10', 'Yen et al. (2008)', 'H.-C. S. Yen, Q. Xu, D. M. Chou, Z. Zhao, S. J. Elledge. Global protein stability profiling in mammalian cells. Science 322(5903), 918–923 (2008).', '10.1126/science.1160489', 'https://doi.org/10.1126/science.1160489'),
        ('P11', 'Balch et al. (2008)', 'W. E. Balch, R. I. Morimoto, A. Dillin, J. W. Kelly. Adapting Proteostasis for Disease Intervention. Science 319(5865), 916–919 (2008).', '10.1126/science.1141448', 'https://doi.org/10.1126/science.1141448'),
        ('P12', 'Steinegger & Söding (2017)', 'M. Steinegger, J. Söding. MMseqs2 enables sensitive protein sequence searching for the analysis of massive data sets. Nature Biotechnology 35(11), 1026–1028 (2017).', '10.1038/nbt.3988', 'https://doi.org/10.1038/nbt.3988'),
        ('P13', 'Efron (1979)', 'B. Efron. Bootstrap methods: another look at the jackknife. Annals of Statistics 7(1), 1–26 (1979).', '10.1214/aos/1176344552', 'https://doi.org/10.1214/aos/1176344552'),
        ('P14', 'Alpine2048 / Degformer', 'Alpine2048. Degformer: Transformer model for internal and C-terminal degron prediction. Software snapshot 49ee52459967; publication year not established.', '', 'https://github.com/Alpine2048/Degformer'),
        ('P15', 'Zhang et al. / Mendeley v2', 'Z. Zhang et al. Data accompanying proteome-wide internal degron mapping. Mendeley Data, version 2, 21 September 2023; CC BY 4.0.', '10.17632/32h94v2yv2.2', 'https://data.mendeley.com/datasets/32h94v2yv2/2'),
    ]
    records = [dict(id=i, label=i, title=t, citation=c, doi=doi, url=url) for i,t,c,doi,url in rows]
    local = [
        ('D1', 'Core v3 dataset', 'data/processed/v3-fullpsi/tables/saturation-cells.parquet', '122,412 mutation cells; labels/sequences; real example and distributions'),
        ('D2', 'Dataset build v3', 'research/kaggle-roadmap-2026-10-31/dataset-build.json', 'counts, fold strata, hit rules; historical specifications remain in DATASET.md'),
        ('D3', 'QC / WT references', 'research/residue-task-derisk-2026-10-15/residue_data.py', 'load_psi, build_saturation, build_scanning'),
        ('D4', 'Six-bin PSI', 'research/full-data-audit/build_psi.py', 'bin normalization and weighted index'),
        ('M1', 'Execution protocol v3.1', 'research/kaggle-roadmap-2026-10-31/EXECUTION-PROTOCOL.md', 'arms, fits, hyperparameters, metrics, stages'),
        ('M2', 'Sequence features', 'research/kaggle-roadmap-2026-10-31/degron_v3/features.py', 'features, crop_inputs; W5 has 260 dimensions'),
        ('M3', 'Convolutional heads', 'research/kaggle-roadmap-2026-10-31/degron_v3/neural.py', 'ConvHead, fit_head, transfer_stage'),
        ('M4', 'Frozen / LoRA', 'research/kaggle-roadmap-2026-10-31/degron_v3/finetune.py', 'LoRALinear, MutationRegressor; rank8 alpha16'),
        ('K1', 'Kaggle v3 (02/11)', 'research/kaggle-roadmap-2026-10-31/output-analysis.json', 'recipes, contrasts; run 369cb2fe6a1e31e0'),
        ('K2', 'Kaggle diagnostics', 'research/kaggle-roadmap-2026-10-31/output-analysis-details.json', 'learning_curve, pair_diagnostics, fold_mae, selected_epochs'),
        ('L1', 'Local v3 (06/11)', 'research/kaggle-roadmap-2026-10-31/local-output-analysis.json', 'local_recipes, contrasts, calibration, transfer; ef138c84579c842e'),
        ('L2', 'OOF audit / residuals', 'research/progress-review-2026-11-06/local-audit.json', 'core_diagnostics, matched_lora_minus_frozen; saved audit'),
        ('L3', 'Output review / recorded computation', 'research/output-review-2026-11-06/results.json', '88 recipes, timing and inventory; durations are not GPU-active time'),
        ('U1', 'Prioritization replay (7 Nov)', 'research/oof-prioritization-2026-11-07/results.json', 'primary_summary, primary_contrasts, secondary_contrasts'),
        ('U2', 'Protocol replay', 'research/oof-prioritization-2026-11-07/PROTOCOL.md', 'equal budget k10, analytic random, grouped bootstrap'),
        ('H1', 'G2 saturation (18/10)', 'research/g2-saturation-2026-10-18/results.json', 'H-sat; DeltaPAP, ridge, gate and checkpoint overlap'),
        ('H2', 'P0/P1 learning curve', 'research/learning-curve-2026-10-22/results.json', 'H-sat train PSI threshold, same test'),
        ('H3', 'R1 cleaned Degformer', 'research/r1-degformer-clean-2026-10-22/run-kaggle-20261022/results.json', '3 seeds × 5 folds; paired comparison intervals'),
        ('H4', 'R2 frozen ESM', 'research/r2-esm-features-2026-10-22/run-kaggle-20261022/results.json', 'PCA64/Ridge ESM2-650M, restricted H-sat'),
        ('H5', 'R6 ladder', 'research/r6-ladder-scan-2026-10-23/run-kaggle-20261023/results.json', '23 recipes; primary vs secondary vs G families'),
        ('H6', 'P3 pretraining', 'research/pretrain-p3-2026-10-22/results.json', 'tile-score pretraining; ext/ridge/rand/pre'),
        ('H7', 'P6 calibration', 'research/calibration-p6-2026-10-22/results.json', 'binary event ΔPSI≥1; different from multiclass v3 Brier'),
        ('H8', 'R3 domain gate', 'research/r3-domain-gate-2026-10-22/run-kaggle-20261022/results.json', 'domain WT PSI≤4; different endpoint'),
        ('H9', 'Scan–sat merge', 'research/scan-sat-merge-2026-10-23/results.json', 'pooling/source/prior and neural transfer controls'),
        ('H10', 'Scanning Ridge M0–M4', 'research/residue-task-derisk-2026-10-15/model.json', 'scanning seed-mean vs held saturation value; populations differ'),
        ('S1', 'G2 acceptance dossier', 'research/g2-acceptance-2026-11-07/evidence.json', 'review-ready development; no recorded closure decision'),
        ('S2', 'Wet-lab source review', 'research/wet-lab-evidence-plan-2026-11-07/results.json', 'external biological precedents; no direct CT553H wet-lab cost evidence'),
        ('S3', 'Serving baseline', 'system/app/README.md', 'baseline scope and historical software checks; serving m3-ext4.0-platt-v1'),
        ('S4', 'Workspace UI prototype', 'system/design/workspace-ui-v2/README.md', 'synthetic fixtures; not connected to backend'),
    ]
    for i,t,p,loc in local:
        records.append(dict(id=i,label=i,title=t,citation=f'CT553H. {t}. {loc}.',path=os.path.relpath(ROOT/p,HERE),locator=loc,repo_path=p))
    return records

def num(x, n=4):
    return '—' if x is None else f'{x:.{n}f}'

def recipe(d, name, origin='kaggle'):
    return d[origin]['local_recipes' if origin=='local' else 'recipes'][name]['ensemble']['all']

def make_plan(d):
    """Initial authoring plan; PPTX edits remain authoritative after creation."""
    slides=[]
    title_en,title_vi=project_titles()
    import textwrap
    def add(id,title,kind='cards',sources=(),scope='',notes='',**kw):
        slides.append(dict(id=id,title=title,layout='title' if kind=='title' else 'references' if kind=='references' else 'cards',kind=kind,source_ids=list(sources),subtitle=scope,notes=notes or title,**kw))
    def cards(id,title,items,sources=(),scope='',notes=''):
        add(id,title,'cards',sources,scope,notes,items=[dict(heading=h,body=b) for h,b in items])
    def table(id,title,headers,rows,sources=(),scope='',notes='',widths=None,size=17):
        add(id,title,'table',sources,scope,notes,headers=headers,rows=rows,widths=widths,font_size=size)

    add('cover','\n'.join(textwrap.wrap(title_en,width=49,break_long_words=False,break_on_hyphens=False)),'title',('S1','L1','U1'),notes=f'Official English title: {title_en}\nOfficial Vietnamese title: {title_vi}\n\nResearch progress as of 7 November 2026. Student: Nguyen Thanh Trong, B2305615. Supervisor: Ho Quang Thai, Ph.D. This presentation reports development evidence, not an acceptance decision or wet-lab validation.')
    add('overview','From biology to prediction evidence','overview',scope='Full research report; detailed result tables are retained in the appendix',items=[{'heading':h,'body':b} for h,b in [('Biological foundations and prediction task','Protein → UPS → degron → mutation → ΔPSI'),('Related work and experimental data','Assay, provenance, quality control and observation units'),('Methods and evaluation design','Ridge, pLMs, CNN/mCNN, LoRA and leakage controls'),('Available experimental results','Historical H-sat; full-PSI W; scanning T; OOF replay'),('Provisional findings and next steps','Supported claims, limitations and unresolved evaluations'),('Appendix and verifiable sources','All 88 v3 recipes; historical controls; references')]],notes='The appendix is for reference and need not be presented in full. Results are development evidence unless stated otherwise. Dates identify saved evidence snapshots.')
    add('protein','Proteins: amino-acid chains with cellular functions','protein',('P1','P11'),scope='A · Biological foundations',notes='Proteins are chains of amino acids joined by peptide bonds. A residue is an amino acid within a chain; a peptide is a short segment. Here the model receives a 28-residue peptide, not the entire protein or its cellular environment. This schematic was drawn by CT553H and is not a measured structure.')
    cards('stability','Stability must be defined by its measurement',[('Protein abundance','The amount of protein at a given time depends on both synthesis and degradation.'),('Protein lifetime','Turnover and half-life describe replacement or degradation over time.'),('Structural stability','Thermodynamic stability concerns protein folding; it differs from reporter PSI.')],('P11','P10','P1'),'A · Three related concepts describe different quantities',notes='A single PSI value does not determine half-life or folding free energy. Reporter abundance can reflect several biological processes. CT553H predicts a specific assay endpoint.')
    add('ups','UPS: recognition, ubiquitination and degradation','ups',('P1','P11'),scope='A · Ubiquitin–Proteasome System',notes='CT553H conceptual schematic: E1 activates ubiquitin, E2 carries it, E3 recognizes the substrate and catalyzes ubiquitin transfer, and the proteasome degrades appropriately tagged proteins. This simplified workflow does not identify the E3 responsible for a CT553H variant effect.')
    add('degron','A degron acts within a protein context','degron',('P1','P2'),scope='A · A sequence segment can contribute to targeting a protein for degradation',notes='A degron is not the whole protein. Its activity can depend on exposure, structure, post-translational modifications and E3/cellular context. A peptide reporter may expose a segment buried in the native protein. The diagram is a conceptual schematic drawn for this report.')
    add('mutation','A single substitution changes one residue','mutation',('D1','P1'),scope='A · Wild type (WT): reference sequence; mutant: sequence after substitution',notes='Wild type (WT) is the reference sequence; the mutant contains the substitution. The example is selected first by peptide_id, numerical position and mutant amino acid in the saturation table. WT: RSLHLPQLRFSRVDATAVTDVPFQRMHA; mutant: ASLHLPQLRFSRVDATAVTDVPFQRMHA. A substitution may disrupt a signal, create one or alter context; its effect cannot be inferred from amino-acid names alone.')
    add('gps','The GPS assay turns reporter behavior into data','gps',('P1','P10','D4'),scope='A · HEK293T; GFP–28-AA peptide reporter; DsRed reference; six FACS bins',notes='Global Protein Stability profiling uses a library of GFP-linked peptides. The GFP/DsRed ratio assigns cells to six FACS bins, then sequencing counts each construct in each bin. A constant C-terminal segment limits artificial C-degrons. This figure illustrates the workflow; it is not a new wet-lab image or measurement.')
    add('psi','PSI is a reporter index on a scale from 1 to 6','psi',('P1','D4'),scope='A · Protein Stability Index in the Zhang assay; not a time unit',notes='build_psi.py normalizes counts by bin and computes a weighted mean of bin indices. p(b) is the normalized proportion of a construct in bin b, summing to 1; PSI=sum b*p(b). Higher PSI indicates a more stable reporter within this assay. This is not a splicing PSI or a generic protein-stability measure.')
    add('delta','WT and mutant measurements define ΔPSI','delta',('D1','D3'),scope='A → B · Real R1A record; displayed values are rounded',notes='Saturation has two halves, sat_a and sat_b. Each WT reference is the median of valid synonymous cells in its own half. Mean ΔPSI = mean(PSI_mut_a−WT_a, PSI_mut_b−WT_b). For R1A, Δa=0.289803860 and Δb=0.471006817; mean=0.3804053385. PSI(WT)=4.0427815905 and mean mutant PSI=4.423186929. This observation does not validate an E3 mechanism.')
    cards('problem','The task is mutation-effect regression',[('Input x','WT sequence of 28 AA, site i and replacement amino acid a. Exactly one substitution generates the mutant.'),('Target y','f(x) ≈ ΔPSI = PSI(mutant) − PSI(WT).\nΔ > 0: higher reporter stability; Δ < 0: lower reporter stability.'),('Scope','Sequence-only input; single substitutions in peptide reporters. Measured PSI, read counts and fold IDs are not model features.')],('M1','M2','D1'),'B · This endpoint differs from degron / non-degron classification',notes='Training minimizes MSE; the primary evaluation metric is peptide-macro MAE. Events Δ≥1 and Δ≤−1 support secondary ranking analyses derived from the same regression labels. The model does not directly predict pathogenicity, E3 identity or intact-protein half-life.')
    table('questions','Five questions organize the progress report',['RQ','Intervention to evaluate','Control / evidence'],[
        ['1','Does broader training PSI coverage help?','Ridge B/D/E; identical W test population'],['2','Do representations / positional mixing help?','one-hot ↔ ESM; k1 ↔ CNN ↔ mCNN'],['3','Does scanning help saturation prediction?','sat-only ↔ pooling / pretrain'],['4','Does backbone adaptation help?','frozen ↔ LoRA matched B/D'],['5','Does performance transfer or support prioritization?','grouped OOF; calibration; T; replay k10']],('M1','K1','L1','U2'),'B · Current organizing questions; the complete history was not preregistered',widths=[.5,4,5],notes='These questions organize the implemented protocol and its history. The v3 protocol was written after earlier data/results were known. The prioritization replay is also a post-hoc development analysis.')
    table('related-primary','Prior work already addresses several endpoints',['Source','Data / method','Contribution and relevance to CT553H'],[
        ['Zhang 2023 [P1]','GPS 28-AA; scan + saturation; DegronID','Measured footprints / E3 pairs; primary label source, not CT553H model performance'],
        ['Voutsinos 2026 [P2]','30-AA peptides; CNN-based PAP; ΔPAP','Abundance prediction and variant follow-up; ΔPAP is not automatically calibrated in ΔPSI units'],
        ['Degformer [P14]','Transformer PSI prediction, including mutant mode','Training exposure must be audited; the public checkpoint overlaps the benchmark'],
        ['Zheng 2024 [P3]','MetaDegron: pLM with multimodal features','E3-targeted degron prediction; endpoint differs from substitution ΔPSI']],('P1','P2','P3','P14','H1','H3'),'C · Compare task, data and exposure; published scores use different protocols',widths=[1.65,3.2,4.35],size=16,notes='Do not claim that previous work only detects motifs or never predicts variant effects: PAP includes ΔPAP and Degformer supports mutant PSI. Author-reported scores on different datasets do not establish matched CT553H performance.')
    table('related-methods','Method choices are hypotheses to test',['Source / approach','Core idea','Bounded use in this study'],[
        ['Hoerl–Kennard 1970 [P7]','Ridge: linear regression with an L2 penalty','Simple control to assess representation value'],
        ['Lin 2023 [P5]','ESM-2 learns protein-sequence representations','Frozen embeddings do not guarantee better ΔPSI prediction'],
        ['Hu 2022 [P6]','LoRA learns low-rank updates to a frozen base','Test rank-8 Q/V adaptation; NLP resource savings do not transfer automatically'],
        ['Szulc 2024 [P4]','DEGRONOPEDIA inspects motifs / context','Biological case evidence; not the same regression benchmark'],
        ['Larsen 2025 [P9]','Degron mapping in transcription factors','Preprint / potential external source; not included in the benchmark']],('P4','P5','P6','P7','P9'),'C · A scoped evaluation question; absolute novelty is not established',widths=[2.2,3.1,4.2],size=16,notes='Author/year/DOI metadata follow the bibliography and literature audit of 6 November; selected primary sources were checked online on 7 November. The ESM publisher and OpenReview had access gaps; LoRA arXiv was accessible. This is not a complete systematic review.')
    add('lineage','From original sources to the v3 data bundle','lineage',('P1','P15','D2','D4'),scope='D · Mendeley v2 / GSE240610 → PSI / QC → tables → splits',notes='The label source is Zhang et al. and Mendeley Data version 2, CC BY 4.0. data/README.md records hashes and provenance. Bundle SHA-256: f4a6542f3786de420108861975eae0c58534e5f60a529bce315de9d00bd872a8. The 1 November build is current; the unbuilt specification retained below it in DATASET.md is historical. No data were downloaded again for this presentation.')
    add('sat-scan','Saturation covers 19 replacements; scanning is sparse','sat_scan',('P1','D2','M1'),scope='D · A mutation cell is a site × amino-acid observation, not a biological cell',notes='Complete saturation yields 28×19=532 nonsynonymous substitutions per peptide. Scanning uses a WT-dependent R/A/S replacement rule, with source-specific C-terminal exceptions; it is not 19 mutants per site. The scanning union has 224,470 cells. Peptide partitions: overlap 1,278; dev 5,489; T 1,414. Only 1,410 T peptides have valid rep1 observations for scoring.')
    add('qc','Full-PSI training retains technical quality control','qc',('D2','D3','M1'),scope='D · Missing cells are not imputed; test data do not fit quality weights',notes='Reads≥10. Saturation requires at least 10 valid synonymous cells per half; each half uses its own WT median, then matched mutation cells are averaged across halves. Scanning uses the correct replicate-specific _mut0 and retains rep1/rep2/mean12 separately; BAG6 WT is not pooled. Seventeen unmapped scanning peptides are excluded; 45 saturation peptides missing legacy groups are mapped using the full proteome. See the data-method audit and the loader/builder code.')
    add('matrix','A measured mutation matrix for one peptide','matrix',('D1',),scope='D · A2RUQ5_C17orf102_2; color shows measured ΔPSI; gray marks WT cells',notes='Select the first peptide by peptide_id rather than a favorable example. The editable matrix is reconstructed from saturation-cells.parquet. Each colored cell is a measured substitution. The display uses a symmetric −3 to +3 PSI palette, saturating extreme colors without altering labels. WT→WT is not a mutation in evaluation.')
    add('distribution','Full-PSI W: 235 peptides, 122,412 mutations','distribution',('D1','D2'),scope='D · 221 protein groups; 12,053 cells with Δ≥1 and 1,577 with Δ≤−1',notes='These distributions are calculated directly from the current core table. WT-PSI strata: ≤3:91; (3,4]:85; (4,5]:36; >5:23 peptides. Cells within peptides/proteins are dependent; 122,412 mutation cells are not independent CI units. Neutral cells satisfy −1<Δ<1 and number 108,782.')
    cards('data-quality','Measurement quality and coverage bound inference',[('Missing measurements','Not every peptide has all 532 cells. Use QC-passing observations; a missing cell does not mean Δ = 0.'),('Replicate differences','scan_dev has 152,004 paired rep1/rep2 cells; Pearson r = 0.7074. Disagreement is a quality indicator, not a known variance.'),('Assay floor / ceiling','1 − PSI(WT) ≤ ΔPSI ≤ 6 − PSI(WT). WT PSI >5 cannot support a positive event Δ≥1.')],('D1','K1','M1'),'D · Ranking metrics use their own eligible-peptide populations',notes='The sequence-only model does not clip predictions using measured WT PSI. Replicate correlation is recorded in the replicate audit cited by output-analysis.json. Rep1 and rep2 are not asserted to have fully verified identical conditions; assay provenance remains separate.')
    add('group-split','Protein-group splitting reduces leakage risks','split',('D2','M1','P8','P12'),scope='D · cov80 + bidirectional cov50 protein hits + exact-sequence unions',notes='The builder combines proteome cov80 groups with MMseqs hits at identity≥0.30, alignment length≥50 AA and bidirectional coverage≥0.50: 12,863 hit edges leave 221 saturation groups. Each group belongs to one outer fold. This heuristic does not exclude every remote homolog or shared motif. Zero additional exact-sequence edges do not prove biological independence.')
    add('nested','Tune inside; evaluate out of fold outside','nested',('M1','L2'),scope='D / F · 5 outer folds; inner validation ≈20% of groups; seeds 17, 29, 43',notes='Outer-test data do not choose alpha, PCA, epochs or calibration. Arms share inner assignments. Fit transformations on inner-train, select hyperparameters by inner MSE, then reinitialize neural models and refit the eligible outer-train for the selected epochs. OOF predictions come from the fold where the sample/group is held out. Outer-test labels have been inspected during development summaries, so this is not an untouched final test.')
    table('arms','Five training arms share the full W test set',['Arm','Train saturation','Validation / test','Question'],[
        ['A','PSI(WT) ≤3','Full range','Historical domain'],['B','PSI(WT) ≤4','Full range','Primary reference'],['C','PSI(WT) ≤5','Full range','Wider coverage'],['D','Full range','Full range','Broader data'],['E','Full range; balance stratum → peptide','Full range','Coverage + weighting']],('M1','D2'),'D / F · Arms restrict training only; B still uses high-PSI inner validation',widths=[.5,3.6,2.3,2.3],size=17,notes='PSI is metadata for constructing views/weights and strata, not an input feature. Arm B does not mean that the whole selection procedure only knows PSI≤4 data. Q1 thresholds for D−B/E−B do not become universal LoRA acceptance thresholds.')
    add('pipeline','One data contract, multiple representations','pipeline',('M1','M2','M3','M4'),scope='E · Data → features / encoder → regression → evaluation → calibration',notes='WT sequence, site i and replacement amino acid form the shared input. Branches include context Ridge, frozen pLM with Ridge or CNN, and frozen/LoRA encoders with newly trained heads. Each predicts ΔPSI; three-class probabilities are calibrated separately. Full fine-tuning is supported by code but has no completed benchmark arm in this campaign.')
    add('ridge','Ridge W5 is an ordered-context baseline','ridge',('M2','M1','P7'),scope='E · x ∈ R²⁶⁰ → scaling → Ridge → ΔPSI',notes='features.py builds 40 WT/mutant one-hot features, 20 whole-peptide composition features and 10 ordered neighbors×20 AA=200 features for radius±5, excluding the center: 260 total. Pair+composition has 60 dimensions; unordered context adds 20, giving 80. Fit MSE with an L2 penalty, selecting alpha from {0.1,1,10,100,1000} by inner MSE. This baseline includes positional context, not composition alone.')
    add('plm','Frozen pLMs represent the WT-to-mutant change','plm',('M1','P5','M2'),scope='E · ESM2-35M: 28 × 480; Δsite + meanΔ gives 960 dimensions',notes='Encode WT and mutant with the same model and remove special tokens, leaving 28 residue vectors. ΔH=Hmut−Hwt. Ridge uses [ΔH at the mutated site; mean ΔH]→PCA64; context models retain the 260-dimensional W5 block separately. Fit scaling/PCA on training data only; PCA uses at most 20,000 seeded training rows. Hidden dimension or published structure performance is not evidence of ΔPSI accuracy.')
    add('cnn','CNNs learn from a crop around the mutation site','cnn',('M3','M1'),scope='E · ESM crop ±7: 15 × 480; all modules are verified against code',notes='ConvHead projects Δhidden 480→32 with Linear+GELU. WT one-hot20 and a center indicator add 21 channels, giving 53 per site; padding is masked. Conv k5 with 96 filters→ReLU; global-max96 and center96 pooling are concatenated with auxiliary60, giving 252→Linear64→ReLU/dropout→1. Dropout=0.3; AdamW lr=0.001, weight decay=0.01, batch=256, max 40 epochs, patience 6. mCNN uses kernels 3/5/7 with 32 filters each; pooled total192 and final input252 are retained.')
    table('heads','Positional-mixing ablation: k1, k5 and multi-scale',['Head','Kernel / filters','After pooling','Hypothesis'],[
        ['Pointwise','k1 ×96','96 max + 96 center','No positional mixing in the convolution'],['CNN','k5 ×96','96 max + 96 center','Local context helps prediction'],['mCNN','k3 / k5 / k7; 32 filters per branch','3 × (32 max + 32 center)','Multiple scales may add information']],('M3','M1','K2'),'E / F · Shared crop, auxiliary inputs and splits; parameter counts differ',widths=[1.15,2.8,2.7,3.3],size=17,notes='Artifact head counts are 36,833 for pointwise and 57,185 for CNN on ESM. Different kernel sizes change capacity, so this is not a perfectly parameter-matched isolation of positional mixing. k1 still uses pooling and auxiliary context; it is not a context-free MLP.')
    add('lora-method','LoRA updates Q/V while preserving base weights','lora',('M4','M1','P6'),scope='E · ESM2-35M; rank 8, alpha 16; frozen and LoRA share the head design',notes='W′=W+(alpha/r)BA. Inject adapters into query/value linear projections only. [Δsite;meanΔ;pair+composition] has 480+480+60=1,020 inputs→MLP64/ReLU/dropout 0.2→1. Frozen training learns the head; LoRA learns adapters and head. Splits, head initialization and backbone eval dropout policy are matched; LoRA gradients remain active. AdamW lr=1e−4, weight decay=0.01, batch 8, gradient clip 1, max 20 epochs, patience 4. This is neither pLM pretraining from scratch nor full fine-tuning.')
    add('scan-method','Scanning supports transfer; T stays outside fitting','scan_transfer',('M1','M3','D2'),scope='E · scan_dev → 5 pretraining epochs → saturation fine-tuning; scratch control',notes='Stage06 CNN transfer uses one-hot inputs, not ESM+scanning. Ridge source weight is 0.1; quality weights use training disagreement and are capped at 0.1..1. Rep1 and mean12 remain separate arms. scan_overlap is excluded from source training. T is excluded from pretraining, calibration and tuning, but its source was explored historically, so it is not an independent external test.')
    table('experiment-design','Implemented comparisons retain matched conditions',['Experiment','Intervention','Fixed conditions / objective'],[
        ['Q1 / stage01','A–E; pair / unordered / ordered','W folds; full-range validation/test; primary MAE'],['Q2 / stage04–05','pLM family; head k1/k5/3,5,7','Matched head / feature conditions within each contrast'],['Q3 / stage06','sat-only / scan / quality / pretrain','Same W cohort; T excluded from fitting'],['Q4 / stage11 local','frozen ↔ LoRA; arms B and D','Same runtime, head initialization and splits'],['Q5 / stage07','Calibrate; lock W5-D before scoring T','Inner-only calibration; separate T cohort'],['Replay 07/11','LoRA-D ↔ W5-D ↔ random','10 selections/peptide; 2 primary contrasts']],('M1','K1','L1','U2'),'F · OOF / post-hoc development analysis; run and seed details are in Notes',widths=[1.6,3.6,4.8],size=16,notes='Kaggle run369cb2fe6a1e31e0 contains stages00–06 and stage11 frozen seed17. Local successor ef138c84579c842e completed 633 jobs. External and structure inputs remain pending. Synthetic smoke tests are excluded from scientific benchmark tables.')
    add('metrics','Three evaluation views answer different questions','metrics',('M1','K1','U2'),scope='F · MAE: 235 peptides; AUROC/AP+: 184, AUROC/AP−: 110',items=[dict(name='MAE ↓',direction='PSI units; peptide-macro averaging',meaning='How large are effect-size errors? Calculate MAE within each peptide, then average across peptides.'),dict(name='AUROC / AP ↑',direction='Δ≥1 or Δ≤−1; at least 3 cells in each class',meaning='How well are events ranked? AP depends on event prevalence and is not accuracy.'),dict(name='Precision@10 ↑',direction='Replay retains all 235 peptides',meaning='How many known hits are found in exactly 10 selections per peptide? Keep peptides with no hits.')],notes='RMSE and Spearman are available in the appendix/evidence JSON. Replay recall uses 198 peptides with positive hits; its population differs from AUROC eligibility and full-population precision. Three-class Brier measures squared probability errors; ECE depends on binning.')
    add('uncertainty','Resample protein groups, not mutation cells','uncertainty',('M1','P13','L1','U2'),scope='F · 5,000 paired bootstrap draws; ensemble predictions precede metric calculation',notes='Both models use the same sampled groups for paired differences. Folds and seeds share data and are not independent experimental studies. Q1 uses 97.5% Bonferroni intervals for 2 contrasts; matched LoRA uses 98.75% post-hoc intervals for 4; replay uses 97.5% for 2 primary contrasts. Other 95% intervals are descriptive. An interval crossing 0 is unresolved, not evidence of equivalence.')
    table('inventory','What evidence is available as of 7 November?',['Component','Status','Evidence scope'],[
        ['Local v3','633 completed jobs; 41 recipes','3 seeds; 5 outer folds; 122,412 cells/seed'],['Kaggle v3','47 recipes; separate snapshot','45 recipes with 3 seeds; 2 frozen recipes with seed17 only'],['Locked T','W5-D scored','39,234 cells / 1,410 peptides / 730 groups'],['Replay OOF','Measured on 7 November','235 peptides; equal budget: 2,350'],['External / structure','source_pending / structure_pending','No valid benchmark yet'],['G2 / serving / wet lab','Decision / implementation pending','Not inferred from development rankings']],('K1','L1','L3','U1','S1'),'G · Saved 6 November audits; no new model training or scoring in this update',widths=[1.9,3.2,4.8],size=16,notes='Hashes of presentation input JSON files are checked. The large audit of 4,278 local and 2,986 Kaggle artifacts is cited from saved evidence, not rerun here. All 88 table rows retain their runtime and seed support.')
    table('history','Historical results use the same H-sat test set',['Recipe / control','AUROC+','Bounded interpretation'],[
        ['ΔPAP (published weights)','0.7693','Reference score; not a newly fitted matched-unit predictor'],['Ridge train WT PSI≤3','0.8082','91 peptides / 89 groups / 47,847 cells'],['Ridge train WT PSI≤4','0.8208','Δ +0.0126; 95% CI [+0.0061; +0.0190]'],['Degformer public checkpoint','0.9248','Training overlap; not a clean generalization comparator'],['Degformer cleaned training','0.8068','3 seeds ×5 folds; CI versus Ridge includes 0'],['R6 ESM35-mCNN / W5','0.8305 / 0.8286','mCNN−M3 primary contrast unresolved; G2 not closed']],('H1','H2','H3','H5'),'G · H-sat and full-PSI W differ in population, grouping and protocol',widths=[3.4,1.5,5],size=17,notes='Public Degformer training contains 42,163/47,847 mutant cells and WT sequences for all 91 peptides. Cleaned R1 training has already been evaluated. Historical gate/PAP acceptance criteria do not transfer unchanged to LoRA v3. The appendix retains R2/P3/merge/R6/calibration details.')
    add('fullpsi-result','Broader training coverage improves Ridge W5','fullpsi_result',('K1',),scope='G · Identical W test set; peptide-macro MAE ↓; 3-seed prediction ensemble',notes='A/B/C/D/E MAEs are read from output-analysis.json. Q1 retains all 235 test peptides. D−B=−0.025774 and E−B=−0.029963; gains concentrate at high WT PSI. Training coverage and protein groups change together, so this does not isolate a biological mechanism.')
    add('fullpsi-ci','Q1 improves MAE; the practical margin is unresolved','fullpsi_ci',('K1','M1'),scope='G · 97.5% CIs for D−B/E−B; the −0.02 margin belongs to Q1 only',notes='Adjusted D−B CI=[−0.033806;−0.018286] and E−B=[−0.041656;−0.018817]. Both exclude 0 but are not entirely below −0.02. For WT PSI≤3, AUROC+ D−B95% CI=[−0.002967;+0.001807]; E−B=[−0.010121;−0.001370], reaching losses beyond 0.01. Q1 criteria are not universal LoRA thresholds.')
    add('family-results','Larger pLMs do not yield monotonically lower error','family_results',('L1',),scope='G · Frozen pLM + PCA64/Ridge; arm D; same local runtime',notes='Nine checkpoints have actual results, not all 20 registry entries. The plot reports only-D and context-D. Local nested selection reaches MAE 0.394454 and evaluates an inner-fold selection procedure, not an independently validated fixed-family winner. Ankh uses an FP32 encoder; precision policies differ across models, so parameter count alone cannot explain differences.')
    table('conv-results','ESM CNN helps; mCNN superiority remains unresolved',['ESM2-35M / D','MAE ↓','AUROC+ ↑','Paired comparison'],[
        ['Pointwise k1','0.3897','0.8375','Reference without convolutional positional mixing'],['CNN k5','0.3844','0.8488','ΔMAE −0.00534; 95% CI [−0.01017; −0.00090]'],['mCNN k3/5/7','0.3850','0.8463','mCNN−CNN: CI95 MAE [−0.00171; +0.00307]'],['mCNN / E (different arm)','0.3838','0.8470','mCNN-E−CNN-D: CI95 [−0.00316; +0.00222]']],('K1','K2'),'G · Development; descriptive CIs; k1 and k5 heads differ in parameter count',widths=[2.1,1,1.2,5.7],size=16,notes='CNN−pointwise AUROC+ increases by 0.011289.95% CI[0.003434; 0.019133]. One-hot-D CNN−pointwise MAE has a CI crossing 0. CNN is not universally better. CNN-D−B MAE on W has 95% CI[−0.007739;+0.000420], and the low-PSI guardrail is unresolved. mCNN-E versus CNN-D changes both scale and training arm.')
    add('scan-results','Scanning pretraining helps its tested control','scan_results',('K1','K2'),scope='G · One-hot CNN; same W; descriptive 95% CIs; quality weighting worsens MAE',notes='Ridge quality−sat=+0.004010; Ridge scan rep1−sat=−0.003072; CNN pretrain rep1−scratch=−0.006385 and mean12−scratch=−0.006326. Mean12−rep1=+0.000059 has a CI crossing 0. This is not ESM+scanning. Benefits appear in both 20 scanning-type pairs and 360 other pairs, still on saturation development OOF predictions.')
    add('learning-curve','Learning curves: single fits versus ensembles','learning_curve',('K2',),scope='G · Ridge W5-D; 25/50/75/100% of training groups; fixed W test set',notes='The two series are mean_seed_mae and ensemble_mae from learning_curve. Below 100%, seeds use different subsets, so an ensemble may see a larger union than the nominal fraction of one model. A complete equivalent neural sample-size curve is unavailable. Selected epochs do not replace train/validation loss curves.')
    rows=[]
    for name in ['esm2_35m-frozen-B','esm2_35m-lora-B','esm2_35m-frozen-D','esm2_35m-lora-D']:
        m=recipe(d,name,'local');rows.append([name.replace('esm2_35m-',''),num(m['mae']),num(m['auroc_plus']),num(m['auprc_plus']),num(m['auroc_minus'])])
    table('lora-results','LoRA improves matched frozen models in B and D',['ESM2-35M local','MAE ↓','AUROC+ ↑','AP+ ↑','AUROC− ↑'],rows,('L1','M4'),'G · Matched runtime / head / split; three-seed prediction ensemble',widths=[2.4,1.6,1.8,1.6,1.8],size=18,notes='The comparator is the same-runtime stage11 frozen encoder with an MLP head, not the frozen Kaggle CNN-D. MAE uses 235 peptides, AUROC/AP+ on 184 and AUROC/AP− on 110. Each of three seeds lowers MAE and raises AUROC+ against its matched arm. There is no completed full-fine-tuning arm.')
    add('lora-ci','Group-level intervals support the LoRA gains','lora_ci',('L1',),scope='G · LoRA − frozen; 98.75% post-hoc Bonferroni CIs across four contrasts',notes='The MAE↓ and AUROC+↑ panels read intervals from local-output-analysis.json.contrasts. These are not preregistered confirmatory tests. The intervals are conditional on the available data/split and do not include a new assay source.')
    add('lora-domain','LoRA-B and D trade off across WT-PSI strata','lora_domain',('L1',),scope='G · Whole-W D−B MAE = +0.00133; 95% CI [−0.00295; +0.00554]',notes='B versus D MAE: le3=0.388442/0.400193; gt3_le4=0.381162/0.381508; gt4_le5=0.309171/0.303302; gt5=0.286305/0.261280. B should not be selected solely by whole-W point rank. Appendix seed results share the outer split and are not three independent studies.')
    add('residuals','Average gains coexist with peptide-level failures','residuals',('L2',),scope='G · LoRA-B improves 184/235 peptides; LoRA-D improves 164/235',notes='Each scatter point is a peptide MAE for frozen versus LoRA. B worsens 51 peptides and D worsens 71. The worst LoRA-B peptide, CCDC17 tile9, has MAE 0.9035 versus frozen 0.8486. Positive/negative effect classes have higher MAE than neutral cells. LoRA-B cell-micro signed residuals are −0.9504 for positive and +1.0449 for negative effects, consistent with effect-size shrinkage but not an identified cause. Failure cases remain included.')
    add('calibration','Lower Brier does not improve every calibration metric','calibration',('L1','M1'),scope='G · Three-class calibration CV; inner-only; no final LoRA serving model',notes='Three-class Brier averages the summed squared errors of three probabilities; it differs from binary P6. Cell-micro Brier: LoRA-B 0.163071, LoRA-D 0.165899, frozen-B 0.178879, frozen-D 0.179495, inner-prior 0.200569. LoRA ECE+ is higher than frozen for this binning. Reliability bins retain sample counts. Empty model_ids in current cards require provenance completion before serving.')
    add('transfer','Locked T: W5-D only; MAE gain remains unresolved','transfer',('L1',),scope='G · 39,234 cells / 1,410 peptides / 730 groups; rep1; R/A/S mutants',notes='W5-D MAE 0.399147 versus zero 0.402403; difference −0.003256.95% CI[−0.009249;+0.002760]. AUROC+=0.840546 on 338 eligible peptides; AUROC−=0.517600 on 85. Three-class Brier micro=0.129119; positive prevalence=0.051155 versus mean predicted probability=0.089529. T shares the lab/source and was historically explored; it is not an independent external test. LoRA has not been evaluated on T.')
    add('priority-design','OOF replay uses an equal mutation-selection budget','priority_design',('U1','U2'),scope='F / G · Primary: LoRA-D ↔ Ridge W5-D ↔ random; k = 10 per peptide',notes='The 235 peptides have 216..532 candidates each; every policy selects 2,350 substitutions. Ranking occurs within each peptide using the three-seed prediction ensemble. Precision retains 37 peptides without positive hits; recall uses 198 with hits. Random uses the analytic expectation of uniform sampling without replacement, not a favorable trial. D was locked for this replay, but models/data had already been explored; this is not independent preregistration.')
    add('priority-results','LoRA-D recovers 173 more hits at the same budget','priority_results',('U1',),scope='G · Positive hit: measured ΔPSI≥1; 2,350 selections per policy',notes='primary_summary gives 1,260 LoRA-D hits,1,087 W5-D hits and 229.857 expected random hits. Peptide-macro precision is 53.6170%,46.2553% and 9.7812%. These are previously measured labels recovered retrospectively, not 1,260 newly validated wet-lab predictions. Frozen-D: 1,124 and LoRA-B: 1,268 are secondary controls and do not reselect the primary recipe.')
    add('priority-ci','The replay supports a prioritization benefit','priority_ci',('U1',),scope='G · ΔPrecision@10 in percentage points; 97.5% CIs for two primary contrasts',notes='LoRA-D−W5=+7.3617 percentage points, adjusted CI[3.3608; 11.3913]; versus random=+43.8359,[38.6350; 48.8341]. Bootstrap: 5,000 protein groups. Mean selections to recover 50% of known hits: LoRA-D: 71.318; W5: 81.990; random: 255.509 on 198 hit-containing peptides. Total hits are known retrospectively and cannot define a prospective stopping rule. No avoided assays/hours/costs were measured.')
    table('priority-limits','Replay utility varies across the PSI domain',['PSI(WT)','Peptides (n)','LoRA-D P@10','W5-D P@10'],[
        ['≤3','91','71.10%','62.64%'],['(3;4]','85','63.76%','52.59%'],['(4;5]','36','19.72%','19.44%'],['>5','23','0.00%','0.00%']],('U1','D1'),'G · Retain all peptides; WT PSI >5 has no observed positive hits',widths=[2,1.5,3,3],size=19,notes='Subgroup results are descriptive and do not replace whole-W findings. Positive Recall@10 is 16.62% for D,13.41% for W5 and 1.93% for random on 198 peptides with hits. LoRA-D−B precision has 95% CI[−2.06;+1.34] percentage points and remains unresolved; keep D as primary. Negative-event evaluation is a separate secondary endpoint.')
    table('resources','Logged computation is not measured wet-lab cost',['Local component','Jobs','Recorded hours','Median minutes / job'],[[name,str(d['review']['timing'][key]['jobs']),num(d['review']['timing'][key]['recorded_seconds_sum']/3600,2),num(d['review']['timing'][key]['median_recorded_seconds']/60,2)] for name,key in [('Probe','probe'),('Extract','extract'),('Ridge','ridge'),('Frozen tuning','tune-frozen'),('LoRA tuning','tune-lora')]],('L3','S2'),'G · Worker-attempt durations; resumed jobs may omit earlier attempts',widths=[2.6,1.5,3,3],size=18,notes='Summed durations are neither elapsed campaign time nor GPU-active time. Frozen and LoRA each have 30 B/D×3-seed×5-fold jobs; scheduling and attempt history affect fair cost comparisons. Energy, deployment latency and cost-normalized utility remain unmeasured. No wet-lab monetary savings are inferred.')
    cards('software','The analysis tool has a baseline; extensions remain open',[('Implemented baseline','FastAPI + React; ETL, API and baseline inference. Serving model: m3-ext4.0-platt-v1.'),('Current prototype','Workspace UI v2 uses interactive fixtures and tab memory; it is not connected to the backend.'),('Still required','Projects/history, protein/batch jobs, import/comparison, PostgreSQL acceptance and correct R3 integration.')],('S3','S4','S1'),'G · Historical software checks do not validate the expanded workflows',notes='Do not promote LoRA to production from development rankings alone. Final refit, export, calibration, inference parity and software acceptance are separate. The slide describes research scope and does not expose internal file paths in the product UI.')
    table('rq-assessment','What do the research questions currently support?',['RQ','Supported evidence','Unresolved questions'],[
        ['1','Broader training helps Ridge, especially at high PSI','Not guaranteed for every head or LoRA arm'],['2','ESM CNN improves its matched pointwise control','No universal architecture winner established'],['3','Scanning pretraining helps one-hot CNN on W','Not external validation or ESM+scan transfer'],['4','LoRA improves matched frozen B/D models','Full tuning, independent validation and cost benefit untested'],['5','Positive k10 replay; calibration quantified','No LoRA-T, external-source or prospective wet-lab result']],('K1','K2','L1','U1'),'H · Provisional synthesis; favorable and unfavorable results are retained',widths=[.5,4.2,4.5],size=17,notes='Lack of a new architecture does not imply lack of contribution. The protocol allows methodological, benchmark, evaluation and software contributions. Development improvements do not themselves create a G2/G3 acceptance decision.')
    cards('limitations','Scientific limits accompany every result',[('Generalization','Grouping is heuristic. Assays/labs are related; peptide context differs from native proteins.'),('Model selection','Many recipes have been inspected on development data. Post-hoc CIs do not include new splits or assays.'),('Practical utility','Replay utility is retrospective. CT553H has no prospective wet-lab, half-life, E3 or measured monetary/time benefit.')],('M1','L1','L2','U1','S2'),'H · External / structure inputs remain pending; published results cannot fill them',notes='Available results do not establish final scientific novelty. The literature review has scope/access limits and cannot support a first-ever claim. Final model export and clinical inference are outside the current evidence.')
    cards('conclusion','Progress conclusions remain open to revision',[('Completed work','Traceable labels, QC and splits; Ridge–pLM–CNN–LoRA controls; 88 v3 recipes and an equal-budget replay.'),('Current support','LoRA improves matched frozen models on W. LoRA-D recovers more positive hits than W5/random in development replay.'),('Not yet decided','No final production model or overall conclusion. The G2 dossier is ready for review; no closure decision is recorded.')],('M1','L1','U1','S1'),'H · Provisional conclusions; not an acceptance record',notes='This structure can become a final conclusion when appropriate evidence and decisions are available. Do not use a best-model or cost-saved template. Methodological and empirical contributions do not require claiming a novel architecture.')
    add('future','Next steps should answer explicit questions','future',('M1','L1','U1','S1'),scope='H · Proposed work; this presentation update runs no training or wet-lab experiment',notes='(1) Confirm the current G2 scope/criteria and record the student/supervisor decision. (2) Lock recipe and intended domain before further evaluation; do not select on inspected T. (3) Audit a new compatible source for homology, assay, errors and calibration. (4) Refit/export with tokenizer/precision/calibrator provenance and inference parity, then assess G3. (5) For real utility claims, run controlled prospective selection and measure resources. Pending branches are not automatically universal requirements for recognizing development contributions.')
    cards('appendix','Appendix: retain evidence for review and updates',[('Complete v3 results','47 Kaggle + 41 local recipes; seed/runtime retained. W MAE, RMSE, AUROC+ and AP+.'),('Historical controls','R6, R2, P3, merge, binary calibration and domain gates retain their own protocols.'),('Source lookup','[P]: primary papers; [D/M]: data/code; [K/L/U/H/S]: internal artifacts. Notes and the evidence map provide locators and hashes.')],('L3',),'Reference material; not every appendix slide needs an oral presentation',notes='Current repository paths start at the root after the 7 November move. Historical topics/degron-footprint locators retain their original context. The official PPTX remains the editing source; do not create parallel v2/final/updated reports.')

    # Exhaustive current benchmark appendix: every verified v3 recipe, separated by runtime.
    for origin in ['Kaggle','Local']:
        rr=[r for r in d['review']['recipes'] if r['origin'].lower()==origin.lower()]
        for offset in range(0,len(rr),7):
            rows=[]
            for r in rr[offset:offset+7]:
                m=r['ensemble']['all']; rows.append([r['recipe'],','.join(map(str,r['seeds'])),num(m['mae']),num(m['rmse']),num(m['auroc_plus']),num(m['auprc_plus'])])
            table(f'v3-{origin.lower()}-{offset // 7 + 1}',f'V3 {origin}: recipe {offset + 1}–{min(offset + 7, len(rr))}/{len(rr)}',['Recipe','Seed','MAE ↓','RMSE ↓','AUC+ ↑','AP+ ↑'],rows,('L3','K1' if origin=='Kaggle' else 'L1'),'W: 235 peptides / 221 groups; AUC+/AP+: 184 eligible peptides; runtimes remain separate',widths=[4.1,1.3,1.05,1.05,1.1,1.1],size=15,notes='Every row is read from results.json.recipes with origin/recipe/seeds retained. Ensemble metrics average predictions before scoring. Seed17-only support stays explicit. Nested selection evaluates a procedure, not a fixed model or a new independent cohort.')
    add_history(add, table, d)
    for i in range(0,len(source_records()),4):
        ids=[r['id'] for r in source_records()[i:i+4]]
        add(f'references-{i // 4 + 1}',f'References / verifiable sources {i // 4 + 1}','references',ids,scope='Full DOI / URL / locators; internal evidence includes repository paths',notes='References support individual claims; this is not a complete systematic review. Legacy metadata follow the 6 November literature audit; targeted online checks from 7 November are recorded in source-verification.json. All diagrams use editable PowerPoint objects; no paper figures are copied.')
    return {'schema':'ctu-slides/1','deck':{'slug':PPTX.stem,'title':title_en,'title_vi':title_vi,'authors':['Nguyễn Thanh Trọng'],'affiliation':'Faculty of Software Engineering · Can Tho University','event':'CT553H · Research Progress Report · 7 November 2026','language':'en'},'sources':source_records(),'slides':slides}

def add_history(add, table, d):
    """Historical artifacts are kept distinct from the current full-PSI cohort."""
    table('history-r2-p3','H-sat: frozen ESM and tile-score pretraining',['Recipe','AUROC+','Limitation'],[
        ['R2 M3 / M3+ESM / ESM','0.8208 / 0.8230 / 0.7853','ESM2-650M + PCA64/Ridge; different from v3 CNN heads'],
        ['P3 ext ridge / random / pretrained','0.8208 / 0.8175 / 0.8098','Tested Voutsinos pretraining did not establish a benefit'],
        ['Merge sat / scan-only','0.8208 / 0.7277','Different populations do not isolate a source effect'],
        ['Merge naive / source / prior','0.8189 / 0.8203 / 0.8197','Pooling did not outperform the saturation Ridge control'],
        ['Merge neural random / pretrain','0.8154 / 0.8168','Separate from the newer stage06 one-hot CNN']],('H4','H6','H9'),'Appendix · H-sat test: 91 peptides / 89 groups / 47,847 cells',widths=[3.6,2.3,4.5],size=16,notes='Values come from historical JSON files and result-comparison.md. Interventions use different architectures/fit policies; cross-experiment ranks do not isolate causes. A failed P3 recipe does not refute every pretraining approach.')
    old=read(ROOT/'research/residue-task-derisk-2026-10-15/model.json')
    table('history-scan','Scanning M0–M4: context and population transfer',['Representation','H-scan AUROC','H-transfer AUROC'],[[n,num(old['scanning']['macro_auroc'][n]['mean']),num(old['saturation_transfer']['macro_auroc'][n]['value'])] for n in old['scanning']['macro_auroc']],('H10',),'Appendix · H-scan: mean metric across seeds; H-transfer: saved score on 91 peptides',widths=[4.9,2.7,2.7],size=17,notes='H-scan has 2,994 peptides before AUROC eligibility. H-transfer uses 91 peptides/47,847 cells after removing scanning groups overlapping the test set. The columns differ in population, source and replacement distribution; they are not treatment effects. M0 composition_only still includes pair40+composition20. Legacy M3 uses±3 context and v3 W5 uses±5. Transfer scores are not current-W ensembles.')
    g2=read(ROOT/'research/g2-saturation-2026-10-18/results.json')
    table('history-gate','G2 saturation retains every gate / PAP control',['Recipe','AUROC+','Scope'],[[n,num(v,6),'Checkpoint overlap' if n=='Degformer' else 'H-sat; development'] for n,v in g2['macro_auroc'].items()],('H1',),'Appendix · 91 peptides / 89 groups; public Degformer has training exposure',widths=[3.7,2.2,4.4],size=18,notes='Public Degformer is not a clean superiority comparator. Clean R1 was evaluated and is reported separately. Historical gate/PAP criteria do not become a universal requirement for a new architecture in LoRA v3.')
    r6=read(ROOT/'research/r6-ladder-scan-2026-10-23/run-kaggle-20261023/results.json')
    # R6 has a different serialized schema; use its artifact-backed comparison
    # inventory, whose original values are cross-checked in verify_numbers().
    historical=[('esm150_mcnn',.821244),('esm35_cnn1',.826394),('esm35_mcnn',.830490),('esm35_mcnn+scan_ft',.829874),('esm35_mcnn+scan_pool',.836670),('esm650_mcnn',.824286),('esm8_mcnn',.826500),('oh_cnn1',.812747),('oh_mcnn',.816805),('oh_mcnn+scan_ft',.831466),('oh_mcnn+scan_pool',.824152),('ridge_M3',.820822),('ridge_W10',.818231),('ridge_W5',.828637),('ridge_W7',.825471),('ridge_esm150',.820682),('ridge_esm35',.823387),('ridge_esm650',.823038),('ridge_esm8',.821393),('ridge_scan_pool',.813758),('ridge_scan_pool_t3',.817291),('ridge_scan_prior',.819041),('ridge_scan_prior_t3',.819173)]
    historical=[(n,r6['summaries'][n]['macro_auroc_ensemble']) for n,_ in historical]
    for start in range(0,len(historical),7):
        table(f'history-r6-{start // 7 + 1}',f'R6: recipe {start + 1}–{min(start + 7, len(historical))}/23',['Recipe','AUROC+ ensemble','Scope'],[[n,num(v,6),'H-sat; 3 seeds × 5 folds'] for n,v in historical[start:start+7]],('H5',),'Appendix · Fixed legacy folds; not directly comparable with full-PSI W',widths=[4.5,2,4],size=17,notes='Retain all 23 R6 recipes, not only the highest point rank. Primary mCNN−M3 is unresolved; W5 context and one scanning-transfer contrast are positive within their specified families. Scores/verdicts belong to R6, not v3 acceptance.')
    table('history-r6-ci','R6 primary and contrast families retain separate verdicts',['Contrast','ΔAUROC','Interval used for inference','Status'],[
        ['P: ESM35 mCNN−M3','+0.00967','[−0.00252; +0.02326]','Primary unresolved'],['A: W5−W3','+0.00781','[+0.00212; +0.01392]','Supported; family A, m=3'],['S1: ESM−one-hot mCNN','+0.01369','[+0.00253; +0.02617]','Positive secondary contrast'],['S6: mCNN−CNN','+0.00410','[−0.00050; +0.00868]','Unresolved'],['G: one-hot scan FT−scratch','+0.01466','[+0.00272; +0.02759]','Supported; family G, m=4']],('H5',),'Appendix · A secondary / G-family gain does not replace the primary verdict',widths=[3.5,1.2,3.1,2.2],size=16,notes='Intervals retain family-specific multiplicity from JSON. Contrasts are not all independent confirmatory tests. Report improvements and negative results together.')
    table('history-calibration','P6 and R3 evaluate different endpoints',['Experiment / recipe','Binary Brier ↓','AUROC or ECE','Endpoint'],[
        ['P6 raw','0.1272','ECE 0.1437','P(ΔPSI≥1), H-sat'],['P6 constant','0.1139','ECE 0.0154','P(ΔPSI≥1), H-sat'],['P6 Platt','0.0925','ECE 0.0163','P(ΔPSI≥1), H-sat'],['P6 isotonic','0.0925','ECE 0.0164','P(ΔPSI≥1), H-sat'],['R3 tier1 domain gate','0.0915','AUC 0.9111','WT PSI≤4; 235 peptides'],['R3 tier2 stageB','0.1434','AUC 0.8154','WT PSI≤4; 222 groups']],('H7','H8'),'Appendix · Binary Brier values are not directly comparable with three-class v3 Brier',widths=[3.1,1.7,2.0,3.2],size=16,notes='Domain-gate AUC is not mutation-effect AUC. Correct R3 integration in the app is still incomplete. Only artifact-backed values are cited; calibration is not rerun here.')
    add('extra-pair-epochs','Additional transfer and training diagnostics','pair_epochs',('K2',),scope='Appendix · Replacement-pair cohorts and selected epochs remain development analyses',notes='There are 6,433 cells in 20 scanning-type pairs and 115,979 in 360 other pairs. CNN pretrain−scratch MAE differences are −0.007723.95% CI[−0.012104;−0.003399], and −0.006311,[−0.009841;−0.002942]. Pointwise/CNN-D selects epoch 1 in 9/15 fits; mCNN-D median=3. These selected epochs are not complete training/validation loss traces.')
    add('extra-seeds','Each LoRA seed improves its matched frozen control','seed_results',('L1',),scope='Appendix · W peptide-macro MAE; seeds share the outer partition',notes='Per-seed MAE comes from local_recipes. Ensemble metrics differ from mean seed metrics, especially for LoRA. Three seeds are not three independent experiments.')
    add('extra-priority','Replay: recall, negative events and tie sensitivity','priority_extra',('U1',),scope='Appendix · Secondary analyses do not reselect the primary recipe',notes='Positive Recall@10 is 16.62% for D,13.41% for W5 and 1.93% for random on 198 hit-containing peptides. Negative Precision@10 is 14.00%,4.34% and 1.326% on all 235 peptides. Retrospective budgets to 50%/80% recall are 71.32/154.36 for D and 81.99/170.53 for W5. No policy has a k10 cutoff tie; 100 hash seeds preserve precision. BTR is not a measured prospective count of avoided assays.')


class Painter:
    """Editable native PowerPoint diagrams, charts, interval plots and tables."""
    def __init__(self, deck, data):
        self.b, self.d = deck, data

    def t(self,s,text,x,y,w,h,size=20,color='ink',bold=False,align='left',name=None):
        return self.b.text(s,text,x,y,w,h,size,color,bold,align,name)

    def box(self,s,x,y,w,h,heading,body='',size=19,color='blue'):
        self.b.box(s,x,y,w,h)
        self.t(s,heading,x+.17,y+.13,w-.34,.66,20,color,True)
        if body:self.t(s,body,x+.17,y+.91,w-.34,h-1.02,size)

    def arrow(self,s,x,y,w=.33,h=.21):
        from pptx.enum.shapes import MSO_SHAPE
        from pptx.util import Inches
        sh=s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW,Inches(x),Inches(y),Inches(w),Inches(h))
        sh.name='CTU process arrow';sh.fill.solid();sh.fill.fore_color.rgb=self.b.color('cyan');sh.line.fill.background()

    def flow(self,s,items,y=2.5,h=2.55):
        n=len(items);gap=.32;w=(11.65-gap*(n-1))/n
        for i,(title,body) in enumerate(items):
            x=.85+i*(w+gap);self.box(s,x,y,w,h,title,body,18)
            if i<n-1:self.arrow(s,x+w+.035,y+h/2-.1,gap-.07)

    def table(self,s,headers,rows,widths=None,size=17,x=.85,y=2.07,w=11.65,h=4.25):
        from pptx.util import Inches,Pt
        from pptx.enum.text import MSO_ANCHOR
        widths=widths or [1]*len(headers)
        sh=s.shapes.add_table(len(rows)+1,len(headers),Inches(x),Inches(y),Inches(w),Inches(h))
        sh.name='CT553H data table'
        t=sh.table
        for c,width in zip(t.columns,widths):c.width=Inches(w*width/sum(widths))
        for i,row in enumerate([headers]+rows):
            for j,value in enumerate(row):
                c=t.cell(i,j);c.text=str(value);c.vertical_anchor=MSO_ANCHOR.MIDDLE
                c.margin_top=c.margin_bottom=Inches(.05);c.margin_left=c.margin_right=Inches(.10)
                c.fill.solid();c.fill.fore_color.rgb=self.b.color('blue' if i==0 else 'pale' if i%2 else 'FFFFFF')
                for p in c.text_frame.paragraphs:
                    p.space_before=Pt(0);p.space_after=Pt(0);p.line_spacing=1.10
                    for r in p.runs:
                        r.font.name='K2D' if i==0 else 'Readex Pro';r.font.size=Pt(size);r.font.bold=i==0
                        r.font.color.rgb=self.b.color('FFFFFF' if i==0 else 'ink')
        return sh

    def chart(self,s,labels,series,x=.9,y=2.12,w=7.25,h=4.05,kind='bar',fmt='0.000',low=None,high=None,legend=True):
        from pptx.chart.data import CategoryChartData
        from pptx.enum.chart import XL_CHART_TYPE,XL_LEGEND_POSITION,XL_LABEL_POSITION,XL_TICK_MARK
        from pptx.util import Inches,Pt
        typ={'bar':XL_CHART_TYPE.BAR_CLUSTERED,'column':XL_CHART_TYPE.COLUMN_CLUSTERED,'line':XL_CHART_TYPE.LINE_MARKERS}[kind]
        data=CategoryChartData();data.categories=list(labels)
        for name,vals in series:data.add_series(name,[float(v) for v in vals])
        sh=s.shapes.add_chart(typ,Inches(x),Inches(y),Inches(w),Inches(h),data)
        sh.name='CT553H editable chart';c=sh.chart
        c.has_legend=legend and len(series)>1
        if c.has_legend:
            c.legend.position=XL_LEGEND_POSITION.BOTTOM;c.legend.include_in_layout=False
            c.legend.font.name='Readex Pro';c.legend.font.size=Pt(12)
        c.chart_style=10;c.has_title=False
        for axis in [c.category_axis,c.value_axis]:
            axis.tick_labels.font.name='Readex Pro';axis.tick_labels.font.size=Pt(12)
            axis.tick_labels.font.color.rgb=self.b.color('ink')
            axis.major_tick_mark=XL_TICK_MARK.NONE;axis.minor_tick_mark=XL_TICK_MARK.NONE
        c.value_axis.tick_labels.number_format=fmt
        c.value_axis.minimum_scale=float(low) if low is not None else 0.0
        if high is not None:c.value_axis.maximum_scale=float(high)
        c.value_axis.has_major_gridlines=True
        colors=['blue','teal','orange','cyan']
        for i,ser in enumerate(c.series):
            ser.format.fill.solid();ser.format.fill.fore_color.rgb=self.b.color(colors[i%len(colors)])
            ser.format.line.color.rgb=self.b.color(colors[i%len(colors)])
        if kind!='line' and len(labels)<=7:
            plot=c.plots[0];plot.has_data_labels=True
            dl=plot.data_labels;dl.number_format=fmt;dl.font.name='Readex Pro';dl.font.size=Pt(11)
            dl.font.color.rgb=self.b.color('ink');dl.position=XL_LABEL_POSITION.OUTSIDE_END
        return sh

    def intervals(self,s,rows,x,y,w,h,lo,hi,title,decimals=4,threshold=None):
        # Each row=(label,estimate,lower,upper). Exact values stay in Notes/evidence.
        self.t(s,title,x,y,w,.42,20,'blue',True)
        axx=x+2.25;axw=w-2.45
        fy=lambda v:axx+(v-lo)/(hi-lo)*axw
        top=y+.72;step=(h-1.08)/len(rows)
        self.line(s,fy(0),top-.12,fy(0),y+h-.32,'muted',.8)
        if threshold is not None:self.line(s,fy(threshold),top-.12,fy(threshold),y+h-.32,'orange',1.3)
        for i,(label,v,a,b) in enumerate(rows):
            yy=top+i*step
            self.t(s,label,x,yy-.10,2.05,.47,17)
            self.line(s,fy(a),yy+.10,fy(b),yy+.10,'blue',2.2)
            self.line(s,fy(a),yy+.04,fy(a),yy+.16,'blue',1.5)
            self.line(s,fy(b),yy+.04,fy(b),yy+.16,'blue',1.5)
            self.dot(s,fy(v),yy+.10,.085,'teal')
            self.t(s,f'{v:+.{decimals}f}  [{a:+.{decimals}f}; {b:+.{decimals}f}]',axx,yy+.27,axw,.38,13,'muted')
        ticks=[0]
        for v in [lo,hi]:
            if abs(fy(v)-fy(0))>.65:ticks.append(v)
        for v in ticks:self.t(s,f'{v:g}',fy(v)-.27,y+h-.10,.54,.25,11,'muted',align='center')

    def line(self,s,x1,y1,x2,y2,color='cyan',width=1.5):
        from pptx.enum.shapes import MSO_CONNECTOR
        from pptx.util import Inches,Pt
        sh=s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,Inches(x1),Inches(y1),Inches(x2),Inches(y2))
        sh.name='CTU diagram line';sh.line.color.rgb=self.b.color(color);sh.line.width=Pt(width)
        return sh

    def dot(self,s,x,y,r,color='blue'):
        from pptx.enum.shapes import MSO_SHAPE
        from pptx.util import Inches
        sh=s.shapes.add_shape(MSO_SHAPE.OVAL,Inches(x-r),Inches(y-r),Inches(r*2),Inches(r*2))
        sh.name='CTU amino acid / data point';sh.fill.solid();sh.fill.fore_color.rgb=self.b.color(color);sh.line.fill.background()
        return sh

    def draw(self,s,a):
        k=a['kind'];d=self.d
        if k=='title':
            self.b.cover(s,{**a,'authors':['Nguyễn Thanh Trọng · B2305615\nSupervisor: Hồ Quang Thái, Ph.D.']})
        elif k=='overview':
            for i,it in enumerate(a['items']):
                y=2.05+i*.72
                self.t(s,f'{i + 1:02d}',.98,y,.60,.34,21,'cyan',True)
                self.t(s,it['heading'],1.86,y,10.35,.34,20,'ink',True)
                self.t(s,it['body'],1.87,y+.38,10.35,.24,12.5,'muted')
        elif k=='cards':self.b.cards(s,a['items'])
        elif k=='table':self.table(s,a['headers'],a['rows'],a.get('widths'),a.get('font_size',17))
        elif k=='metrics':self.b.metrics(s,a['items'])
        elif k=='references':self.references(s,a)
        elif k=='protein':
            self.t(s,'20 amino-acid types → sequence → structure / interactions → function',.98,2.09,11.2,.55,24,'blue',True)
            aa='M A L E K L V D A G P R T F S W'.split()
            for i,v in enumerate(aa):
                x=1.13+i*.68;yy=3.13+(.24 if i%2 else 0)
                if i:self.line(s,x-.68,3.13+(.24 if (i-1)%2 else 0),x,yy)
                self.dot(s,x,yy,.24,'teal' if i in range(6,10) else 'blue')
                self.t(s,v,x-.21,yy-.15,.42,.35,16,'FFFFFF',True,'center')
            self.box(s,1.0,4.25,3.45,1.75,'Protein','A molecule with functions in the cell.',18)
            self.box(s,4.89,4.25,3.45,1.75,'Peptide','A short chain segment; the core data use 28 AA.',18)
            self.box(s,8.78,4.25,3.45,1.75,'Residue','One amino acid at one position in a chain.',18)
        elif k=='ups':
            self.flow(s,[('E1','Activates ubiquitin (Ub).'),('E2','Carries Ub to the tagging machinery.'),('E3 + substrate','Recognizes the degron / compatible context.'),('Proteasome','Recognizes tagged protein and degrades it.')],h=2.8)
            self.t(s,'Degrons contribute to recognition; ΔPSI prediction does not identify an E3.',1.0,5.70,11.1,.60,21,'ink')
        elif k=='degron':
            self.t(s,'THE SAME SEQUENCE SEGMENT',1.04,2.08,11,.55,23,'blue',True)
            self.box(s,1.0,2.94,5.2,2.65,'In the native protein','May be buried, masked by interactions or dependent on post-translational modifications.',20)
            self.box(s,6.68,2.94,5.2,2.65,'In the peptide reporter','The 28-AA segment is placed in a construct; context and exposure may differ from the native protein.',20)
            self.t(s,'Reporter effects therefore provide assay-specific evidence.',1.05,5.94,11.0,.48,21)
        elif k=='mutation':
            r=d['record'];self.t(s,r.peptide_id,1.0,2.07,11,.5,22,'blue',True)
            for yy,label,seq in [(2.98,'WT',r.wt_sequence),(4.15,'R1A',r.mutant_sequence)]:
                self.t(s,label,.95,yy,1,.46,20,'blue',True)
                for j,v in enumerate(seq):
                    x=2+j*.35;self.b.box(s,x,yy-.03,.32,.50,'teal' if j==0 else 'pale')
                    self.t(s,v,x+.025,yy+.06,.27,.33,15,'FFFFFF' if j==0 else 'ink',j==0,'center')
            self.t(s,'One substitution at site 1: Arginine (R) → Alanine (A).',1.0,5.39,11.2,.55,22)
            self.t(s,'Recognition or context may change; measurements establish the effect.',1.0,6.00,11.2,.4,18,'muted')
        elif k=='gps':
            self.flow(s,[('Construct','GFP–28-AA peptide\n+ constant C-end'),('Cells','HEK293T\nDsRed reference'),('FACS','Sort by\nGFP / DsRed'),('Sequencing','Count constructs\nin 6 bins')],h=2.8)
            self.t(s,'The measurement is specific to the reporter, construct and cellular conditions.',1.0,5.76,11.0,.55,22)
        elif k=='psi':
            self.t(s,'PSI = 1 × p(1) + 2 × p(2) + … + 6 × p(6)',1.03,2.10,11.05,.65,27,'blue',True)
            self.t(s,'p(b): bin-normalized read proportion; the proportions sum to 1.',1.04,2.93,11.1,.55,20)
            for i in range(6):
                x=1.35+i*1.75;self.b.box(s,x,3.98,1.35,1.10,'pale')
                self.t(s,str(i+1),x,4.14,1.35,.62,30,'blue',True,'center')
                if i<5:self.arrow(s,x+1.42,4.44,.25)
            self.t(s,'Low PSI: less stable reporter',1.06,5.54,5.25,.55,20)
            self.t(s,'High PSI: more stable reporter',6.62,5.54,5.25,.55,20,align='right')
        elif k=='delta':
            r=d['record'];mut=(r.psi_mut_a+r.psi_mut_b)/2
            self.box(s,1.,2.2,3.3,2.85,'PSI(WT)',f'{r.psi_wt_sat:.4f}\nMedian PSI of synonymous variants per half.',21)
            self.box(s,4.95,2.2,3.3,2.85,'PSI(mutant)',f'{mut:.4f}\nMean of sat_a and sat_b.',21)
            self.box(s,8.90,2.2,3.3,2.85,'ΔPSI',f'+{r.dpsi_mean:.4f}\nHigher reporter stability within this assay.',21)
            self.t(s,'Δ = ½ [(PSI_mut_a − WT_a) + (PSI_mut_b − WT_b)]',1.,5.20,11.4,.60,24,'blue',True)
            self.t(s,'The sign of Δ does not establish degron disruption or a specific E3 mechanism.',1.,6.02,11.4,.4,18,'muted')
        elif k=='lineage':
            self.flow(s,[('Zhang sources','Mendeley v2\nCC BY 4.0\nGSE240610'),('Reconstruct PSI','Read 6 bins\nnormalize → PSI\nQC + WT'),('Bundle v3','Tables / provenance\n122,412 sat cells\n224,470 scan cells'),('Evaluation','Group splits\nfit / OOF / T\nartifact + hash')],h=3.05)
        elif k=='sat_scan':
            self.box(s,1.,2.15,5.18,4.35,'Saturation','19 non-WT amino acids per site.\n\nUp to 28 × 19 = 532 cells/peptide.\n235 peptides; 122,412 QC-passing cells.\n\nPrimary target labels on W.',20)
            self.box(s,6.65,2.15,5.18,4.35,'Scanning','Rule-based R/A/S substitution per site.\n\nMore peptides, fewer replacement types.\n224,470 cells in the replicate union.\n\ndev for training; T held out.',20)
        elif k=='qc':
            self.flow(s,[('Reads / sequence','Reads ≥10\n28 standard AA\nValid mapping'),('Source-specific WT','Sat: median\n≥10 synonymous cells\nScan: _mut0'),('Match observations','Sat: both halves\nScan: retain masks\nrep1 / rep2'),('Retain provenance','Missing ≠ 0\nNo label imputation\nPSI is metadata')],h=3.05)
        elif k=='matrix':self.matrix(s)
        elif k=='distribution':
            import numpy as np
            sat=d['sat'];p=sat[['peptide_id','psi_stratum']].drop_duplicates()
            labels=['≤3','(3;4]','(4;5]','>5'];cts=[int((p.psi_stratum==a).sum()) for a in ['le3','gt3_le4','gt4_le5','gt5']]
            self.t(s,'Peptides by WT PSI',1.,2.04,5.6,.45,20,'blue',True)
            self.chart(s,labels,[('Peptide',cts)],x=.95,y=2.65,w=5.2,h=3.65,kind='column',fmt='0',high=110)
            counts,edges=np.histogram(sat.dpsi_mean,bins=np.linspace(-3.5,4,16))
            self.t(s,'Measured ΔPSI distribution: 122,412 cells',6.65,2.04,5.7,.45,20,'blue',True)
            self.chart(s,[f'{x:.1f}' for x in edges[:-1]],[('Cell count',counts)],x=6.45,y=2.65,w=5.65,h=3.65,kind='column',fmt='0')
        elif k=='split':
            self.flow(s,[('Protein hits','cov80 + cov50\nidentity ≥30%\nalignment ≥50'),('Group union','Exact sequences\n+ homology edges\n221 sat groups'),('5 outer folds','One fold per group\n47 peptides/fold')],y=2.3,h=2.55)
            for i in range(5):
                x=1.4+i*2.1;self.b.box(s,x,5.36,1.75,.66,'blue' if i==2 else 'pale');self.t(s,'TEST' if i==2 else 'TRAIN',x,5.53,1.75,.36,17,'FFFFFF' if i==2 else 'ink',True,'center')
        elif k=='nested':
            self.box(s,.95,2.2,3.05,3.50,'Outer train','Grouped train / val.\n\nFit scaler/PCA on train.\nMSE selects α / epochs.',19)
            self.arrow(s,4.17,3.85,.4)
            self.box(s,4.75,2.2,3.05,3.50,'Refit the recipe','Reinitialize the neural model.\n\nFit eligible outer-train for the selected epochs.',19)
            self.arrow(s,7.97,3.85,.4)
            self.box(s,8.55,2.2,3.05,3.50,'Outer test → OOF','No tuning here.\n\nRepeat 5 folds × 3 seeds; ensemble predictions.',19)
            self.t(s,'Calibration also uses its own fold validation; global OOF fitting can leak labels.',1.,5.78,11.2,.62,19)
        elif k=='pipeline':
            self.flow(s,[('Shared input','WT 28 AA\nsite i + mutant a'),('Representation','One-hot / context\nFrozen pLM / LoRA'),('Regressor','Ridge\nCNN / mCNN / MLP'),('Evaluation','ΔPSI → MAE\nranking / calibration')],h=2.8)
            self.t(s,'Shared labels and W test set; vary components within their matched comparisons.',1.,5.78,11.3,.55,21)
        elif k=='ridge':
            self.flow(s,[('Pair','WT one-hot 20\nMutant one-hot 20\n= 40 dimensions'),('Composition','Whole-WT amino-acid frequencies\n= 20 dimensions'),('Ordered W5','10 neighboring sites\n× 20 AA\n= 200 dimensions'),('Ridge','Concatenate 260\nScaling + L2 penalty\n→ ΔPSI')],h=2.9)
            self.t(s,'Controls: pair = 40; pair+composition = 60; unordered window = 80 dimensions.',1.,5.89,11.3,.5,19)
        elif k=='plm':
            self.flow(s,[('WT / mutant','Shared encoder\n28 × 480\nESM2-35M'),('Hidden difference','ΔH = H_mut − H_WT\nSite + mean\n= 960 dimensions'),('Frozen Ridge','PCA64 on Δ\n+ W5 context 260\n→ regression')],y=2.25,h=2.8)
            self.t(s,'Fit PCA on train only; retain the context block. Frozen encoders do not learn ΔPSI labels.',1.,5.56,11.1,.70,20)
        elif k=='cnn':
            self.flow(s,[('Input crop','WT one-hot 20\n+ center flag 1\n+ Δhidden 480'),('Projection','480 → 32\n15 × (20+1+32)\n= 15 × 53'),('Conv k5','53 → 96 channels\nReLU + mask\n15 positions'),('Pool + MLP','Max96 + center96\n+ auxiliary60\n252 → 64 → 1')],y=2.28,h=3.02)
            self.t(s,'Extract Δhidden from both WT and mutant; auxiliary = pair40 + composition20.',1.,5.78,11.3,.55,20)
        elif k=='lora':
            self.t(s,'W′ = W + (alpha / r) × B × A',1.,2.06,11.1,.66,28,'blue',True)
            self.flow(s,[('Frozen base','ESM2-35M\nW stays fixed'),('Adapter Q/V','r = 8; alpha = 16\nLearn A and B'),('Mutant − WT','Δsite480\n+ meanΔ480\n+ auxiliary60'),('Matched MLP','1,020 → 64 → 1\nMatched head init\nFrozen ↔ LoRA')],y=3.08,h=2.8)
        elif k=='scan_transfer':
            self.flow(s,[('scan_dev','5,489 peptides\nrep1 / mean12\nsource train'),('Pretrain','One-hot CNN\n5 fixed epochs\nExclude T'),('Fine-tune W','Saturation\nCNN scratch control\nSame architecture'),('scan_T','Held-source\n1,410 scored\nW5-D only')],y=2.40,h=3.05)
            self.t(s,'Keep 1,278 peptides overlapping saturation groups outside source training.',1.,5.95,11.3,.40,18,'muted')
        elif k=='uncertainty':
            self.flow(s,[('Prediction','For each cell\n3 seeds → mean\nThen score'),('Macro','MAE per peptide\n→ average\nacross peptides'),('Bootstrap','Sample group_id\nKeep its peptides\n5,000 paired draws'),('Confidence interval','MAE difference <0 helps\nAUROC difference >0 helps\nRetain multiplicity')],h=3.05)
        elif k=='fullpsi_result':
            names=['ordered-w5-'+a for a in 'ABCDE'];vals=[recipe(d,n)['mae'] for n in names]
            self.chart(s,['A ≤3','B ≤4','C ≤5','D full','E balanced'],[('MAE',vals)],high=.53,low=0,fmt='0.000')
            self.t(s,'D versus B\n−0.0258 PSI\n\nE versus B\n−0.0300 PSI\n\nLarger gains at high WT PSI.',8.62,2.43,3.45,3.7,22)
        elif k=='fullpsi_ci':
            contrasts=d['kaggle']['contrasts'];rows=[]
            for arm in 'DE':
                c=contrasts[f'ordered-w5-{arm} minus ordered-w5-B; mae'];rows.append((arm+' − B',c['delta'],*c['ci_adjusted']))
            self.intervals(s,rows,.97,2.12,7.38,3.65,-.05,.005,'ΔMAE: lower is better',threshold=-.02)
            self.t(s,'CIs below 0 support improvement.\n\nNot entirely below −0.02.\n\nE does not establish the low-PSI AUROC+ guardrail.',8.78,2.43,3.3,3.65,20)
        elif k=='family_results':
            families=['esm2_8m','esm2_35m','ankh_base','esmc_300m','esm2_150m','esm1v_650m_1','prott5_encoder','esm1b_650m','esm2_650m']
            self.chart(s,[n.replace('_encoder','').replace('_650m_1','') for n in families],[('only-D',[recipe(d,n+'-only-D','local')['mae'] for n in families]),('context-D',[recipe(d,n+'-context-D','local')['mae'] for n in families])],x=.85,w=8.0,low=.39,high=.413,fmt='0.000')
            self.t(s,'9 evaluated checkpoints\n\nNested selection:\nMAE 0.3945\nAUROC+ 0.8409\n\nThe score evaluates inner-fold selection.',9.15,2.36,3.05,3.9,19)
        elif k=='scan_results':
            keys=[('Quality Ridge','sat-quality-D minus sat-only-D; mae'),('Scan Ridge','scan-rep1-D minus sat-only-D; mae'),('Pretrain rep1','cnn-transfer-dpsi_rep1-D minus cnn-transfer-scratch-D; mae'),('Pretrain mean12','cnn-transfer-dpsi_rep12_mean-D minus cnn-transfer-scratch-D; mae')]
            # Serialized recipe labels are resolved explicitly rather than guessed.
            cs=d['kaggle']['contrasts'];rows=[]
            for label,key in keys:
                if key not in cs:
                    matches=[v for kk,v in cs.items() if (label=='Quality Ridge' and 'quality' in kk and kk.endswith('; mae')) or (label=='Scan Ridge' and 'rep1' in kk and 'ridge' in kk and kk.endswith('; mae'))]
                    if len(matches)!=1:raise ValueError(f'Ambiguous contrast {label}: {[k for k in cs if 'ridge' in k]}')
                    c=matches[0]
                else:c=cs[key]
                rows.append((label,c['delta'],*c['ci95']))
            self.intervals(s,rows,.97,2.08,8.3,4.03,-.014,.007,'ΔMAE: lower is better')
            self.t(s,'Quality weighting worsens MAE.\n\nRep1 and mean12 both help versus scratch; their difference is unresolved.',9.65,2.46,2.45,3.65,18)
        elif k=='learning_curve':
            rr=list(d['details']['learning_curve'].values())
            self.chart(s,['25%','50%','75%','100%'],[('Mean seed MAE',[v['mean_seed_mae'] for v in rr]),('MAE ensemble',[v['ensemble_mae'] for v in rr])],kind='line',low=.39,high=.45,fmt='0.000')
            self.t(s,'Seeds use different subsets below 100%.\n\nA 25% ensemble may see a union larger than 25%.\n\nNo equivalent LoRA sample-size curve yet.',8.65,2.43,3.4,3.65,20)
        elif k=='lora_ci':
            for j,metric in enumerate(['mae','auroc_plus']):
                rows=[]
                for arm in 'BD':
                    c=d['local']['contrasts'][f'local:esm2_35m-lora-{arm} minus local:esm2_35m-frozen-{arm}; {metric}'];rows.append((f'Arm {arm}',c['delta'],*c['ci_adjusted']))
                self.intervals(s,rows,.98+j*6.03,2.21,5.43,3.25,-.055 if j==0 else -.005,.005 if j==0 else .045,'ΔMAE ↓' if j==0 else 'ΔAUROC+ ↑',decimals=3)
            self.t(s,'Matched adaptation on development W; LoRA transfer beyond the source remains untested.',1.,6.00,11.5,.4,18,'muted')
        elif k=='lora_domain':
            strata=['le3','gt3_le4','gt4_le5','gt5'];rr=d['local']['local_recipes']
            self.chart(s,['≤3 (91)','(3; 4] (85)','(4; 5] (36)','>5 (23)'],[(f'LoRA-{a}',[rr[f'esm2_35m-lora-{a}']['ensemble']['strata'][st]['mae'] for st in strata]) for a in 'BD'],kind='column',low=0,high=.46,fmt='0.000')
            self.t(s,'B has lower MAE at low WT PSI.\n\nD has lower MAE in the two high-PSI strata.\n\nSimilar overall scores can hide different behavior.',8.68,2.40,3.35,3.7,20)
        elif k=='residuals':self.residuals(s)
        elif k=='calibration':
            names=['frozen-B','frozen-D','lora-B','lora-D'];rr=d['local']['calibration']
            self.table(s,['Local recipe','Brier3 ↓','ECE+ ↓'],[[n,num(rr['esm2_35m-'+n]['multiclass_brier_cell_micro']),num(rr['esm2_35m-'+n]['positive_ece_cell_micro'])] for n in names],[2.4,1.4,1.4],17,x=.9,y=2.2,w=5.75,h=3.45)
            self.t(s,'LoRA has lower Brier but higher ECE+ than frozen.\n\nInner-prior Brier3 = 0.2006.\n\nCalibration CV is not a final export; model-card provenance remains incomplete.',7.07,2.40,5.0,3.6,22)
            self.t(s,'Cell-micro; classes Δ≤−1 / neutral / Δ≥1. Different from binary P6 Brier.',.99,6.00,11.4,.4,17,'muted')
        elif k=='transfer':
            t=d['local']['transfer'];m=t['population']['all'];z=t['zero_baseline']['all'];ci=t['model_minus_zero_mae']
            self.table(s,['T metric','W5-D','Condition'],[['MAE macro',num(m['mae']),'1,410 peptides'],['MAE zero baseline',num(z['mae']),'Same cohort'],['ΔMAE / CI95',f'{ci['delta']:+.4f}',f'[{ci['ci95'][0]:+.4f}; {ci['ci95'][1]:+.4f}]'],['AUROC+ / AUROC−',num(m['auroc_plus'])+' / '+num(m['auroc_minus']),'338 / 85 eligible peptides'],['P(positive) / observed rate',num(t['mean_positive_probability'])+' / '+num(t['observed_positive_rate']),'Cell-micro; probability shift is present']],[2.9,2.6,4.4],17)
        elif k=='priority_design':
            self.flow(s,[('OOF per cell','W full-PSI\n235 peptides\n3 seeds → mean'),('Rank within peptide','LoRA-D / W5-D\nExpected random\n216–532 candidates'),('Select exactly 10','10 ×235\n=2,350 substitutions\nFor every policy'),('Count known hits','Measured Δ≥1\nP@10: all 235\nRecall:198 with hits')],h=3.05)
        elif k=='priority_results':
            rr={r['policy']:r for r in d['priority']['primary_summary']};names=['random','ridge-w5-D','lora-D']
            self.chart(s,['Expected random','Ridge W5-D','LoRA-D'],[('Hits in 2,350 selections',[rr[n]['hits_total'] for n in names])],high=1450,fmt='0.0')
            self.t(s,'Precision@10\n\nLoRA-D  53.62%\nW5-D     46.26%\nRandom    9.78%\n\n+173 hits versus W5-D\nin OOF replay.',8.7,2.29,3.4,3.9,22)
        elif k=='priority_ci':
            rows=[(r['baseline'],r['delta']*100,r['ci_adjusted'][0]*100,r['ci_adjusted'][1]*100) for r in d['priority']['primary_contrasts']]
            self.intervals(s,rows,1.,2.17,7.7,3.65,-3,52,'LoRA-D minus baseline: percentage points',decimals=2)
            self.t(s,'Both CIs are above 0.\n\nTo recover 50% of known hits:\n71.32 selections/peptide for LoRA-D; 81.99 for W5-D.\n\nRetrospective BTR.',9.0,2.37,3.15,3.75,19)
        elif k=='future':
            self.flow(s,[('Review scope','Read evidence\n+ limitations\nRecord G2 decision'),('Further evaluation','Lock recipe / RQ\nCompatible source\nAudit overlap'),('Serving','Refit / calibrator\nexport + parity\nacceptance G3'),('Prospective utility','For utility claims:\nProspective selection\nMeasure hits/resources')],h=3.05)
        elif k=='pair_epochs':
            self.table(s,['Cohort substitution','Cell count','Scratch MAE','Pretrain MAE'],[['20 scanning-type pairs','6,433','0.3991','0.3913'],['360 other pairs','115,979','0.3933','0.3870']],[3.1,1.5,2.6,2.6],18,h=2.2)
            self.t(s,'CNN / pointwise-D selects epoch 1 in 9/15 fits; mCNN-D median = 3.\n\nRaising the epoch cap has no demonstrated benefit; k1 / k5 heads have 36,833 / 57,185 parameters.',1.,4.75,11.2,1.35,21)
        elif k=='seed_results':
            rows=[]
            for n in ['frozen-B','frozen-D','lora-B','lora-D']:
                r=d['local']['local_recipes']['esm2_35m-'+n]
                seed=r['per_seed'];rows.append([n]+[num(seed[str(a)]['mae']) for a in [17,29,43]]+[num(r['ensemble']['all']['mae'])])
            self.table(s,['Recipe','Seed17','Seed29','Seed43','Ensemble'],rows,[2.1,1.6,1.6,1.6,1.8],18)
        elif k=='priority_extra':
            self.table(s,['Policy','Recall@10 +','P@10 −','BTR50 +','BTR80 +'],[[n,*vals] for n,vals in [('LoRA-D',['16.62%','14.00%','71.32','154.36']),('W5-D',['13.41%','4.34%','81.99','170.53']),('Random',['1.93%','1.33%','255.51','404.48'])]],[2.0,2,2,2,2],18,h=2.8)
            self.t(s,'Positive recall / BTR: 198 hit-containing peptides. Negative precision: all 235.\n\nNo k10 cutoff ties; 100 hash seeds preserve Precision@10.',1.,5.33,11.2,.95,20)
        else:raise ValueError(f'No native painter for {k}')

    def matrix(self,s):
        import numpy as np
        from pptx.enum.shapes import MSO_SHAPE
        from pptx.util import Inches
        d=self.d;r=d['record'];sub=d['sat'][d['sat'].peptide_id==r.peptide_id]
        aa='ACDEFGHIKLMNPQRSTVWY';lookup={(int(q.position_1based),q.mut_aa):q.dpsi_mean for q in sub.itertuples()}
        x0,y0,cw,ch=1.35,2.46,.31,.168
        for j in range(28):self.t(s,str(j+1),x0+j*cw,y0-.33,cw,.24,10,'muted',align='center')
        for i,a in enumerate(aa):
            self.t(s,a,x0-.39,y0+i*ch-.015,.28,ch,9,'blue',True,'center')
            for j in range(28):
                v=lookup.get((j+1,a));color='D7DEE3'
                if v is not None:
                    q=min(abs(v)/3,1);target=(0,112,192) if v<0 else (0,153,136)
                    color=''.join(f'{round(247 + (t - 247) * q):02X}' for t in target)
                sh=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(x0+j*cw),Inches(y0+i*ch),Inches(cw-.012),Inches(ch-.008))
                sh.name=f'measured:{r.peptide_id}:{j + 1}:{a}' if v is not None else 'WT or unobserved cell'
                sh.fill.solid();sh.fill.fore_color.rgb=self.b.color(color);sh.line.fill.background()
        self.t(s,'Peptide position (1-based)',2.9,6.05,6,.34,16,'muted',align='center')
        self.t(s,'Measured ΔPSI\n\nBlue: negative\nWhite: near 0\nTeal: positive\nGray: WT / missing\n\nDisplay scale\n−3 to +3.',10.5,2.55,1.93,3.75,16)

    def residuals(self,s):
        from pptx.chart.data import XyChartData
        from pptx.enum.chart import XL_CHART_TYPE
        from pptx.util import Inches,Pt
        d=self.d;core=d['audit']['core_diagnostics'];x={r['peptide_id']:r['mae'] for r in core['esm2_35m-frozen-B']['per_peptide']}
        data=XyChartData();ser=data.add_series('Peptide')
        for r in core['esm2_35m-lora-B']['per_peptide']:ser.add_data_point(x[r['peptide_id']],r['mae'])
        eq=data.add_series('y = x');eq.add_data_point(0,0);eq.add_data_point(1,1)
        c=s.shapes.add_chart(XL_CHART_TYPE.XY_SCATTER,Inches(.93),Inches(2.18),Inches(6.8),Inches(3.72),data).chart
        c.has_legend=False
        for axis,title in [(c.category_axis,'Frozen-B MAE'),(c.value_axis,'LoRA-B MAE')]:
            axis.minimum_scale=0;axis.maximum_scale=1;axis.tick_labels.font.name='Readex Pro';axis.tick_labels.font.size=Pt(12)
            axis.has_title=True;axis.axis_title.text_frame.text=title
            for p in axis.axis_title.text_frame.paragraphs:
                for r in p.runs:r.font.name='Readex Pro';r.font.size=Pt(14)
        from pptx.enum.chart import XL_MARKER_STYLE
        c.series[0].marker.style=XL_MARKER_STYLE.CIRCLE;c.series[0].marker.size=4
        c.series[0].marker.format.fill.solid();c.series[0].marker.format.fill.fore_color.rgb=self.b.color('teal')
        c.series[0].marker.format.line.fill.background()
        c.series[1].marker.style=XL_MARKER_STYLE.NONE;c.series[1].format.line.color.rgb=self.b.color('muted')
        self.t(s,'One point per peptide.\nBelow y=x favors LoRA.\n\nB worsens 51 peptides.\nD worsens 71 peptides.\n\nCCDC17 tile9: LoRA-B MAE 0.9035 remains a failure case.',8.25,2.30,3.96,3.75,20)
        self.t(s,'Large effects still have higher error and shrinkage; residuals do not establish a mechanism.',1.,6.05,11.25,.35,17,'muted')

    def references(self,s,a):
        for i,rid in enumerate(a['source_ids']):
            r=self.b.sources[rid];y=2.03+i*1.08
            self.t(s,f'[{rid}]',.94,y,.73,.38,15,'blue',True)
            self.t(s,r['citation'],1.84,y,10.4,.70,13.5)
            url=r.get('url') or r.get('repo_path','')
            if r.get('doi'):url='https://doi.org/'+r['doi']
            sh=self.t(s,url,1.84,y+.75,10.4,.28,11,'muted')
            if url.startswith('http'):
                for p in sh.text_frame.paragraphs:
                    for run in p.runs:run.hyperlink.address=url


def create_slide(deck,painter,a,position=None):
    from pptx.util import Pt
    if position is not None:deck.count=position
    s=deck.frame(a['title'],a.get('subtitle',''),a['kind']=='title')
    # python-pptx chooses a part name from the live slide count. Replacement
    # keeps that count constant, so use a unique valid OPC name before the next
    # add_slide; otherwise two slides can silently share a zip entry.
    from pptx.opc.packuri import PackURI
    s.part._partname=PackURI('/ppt/slides/slide-'+uuid.uuid4().hex+'.xml')
    s._element.cSld.set('name',TAG+a['id'])
    for sh in s.shapes:
        if sh.name=='CTU slide title':
            for p in sh.text_frame.paragraphs:
                for r in p.runs:r.font.size=Pt(26)
        if sh.has_text_frame and sh.top>7*914400 and sh.text.isdigit():sh.name='CT553H page number'
    if a['kind'] not in ('title','references'):
        short='Sources: '+' · '.join(f'[{rid}]' for rid in a['source_ids'])
        if a['source_ids']:painter.t(s,short,.97,1.72,11.47,.27,12.5,'muted',name='CT553H visible citations')
    painter.draw(s,a)
    deck.notes(s,a)
    return s


def save_manifest(deck,plan):
    old=read(HERE/'build-manifest.json') if (HERE/'build-manifest.json').exists() else {}
    manifest={
        'schema':'ctu-build/1','spec':str(HERE/'authoring-plan.json'),
        'deck':'../'+PPTX.name,'deck_sha256':sha(PPTX),'slides':len(deck.prs.slides),
        'style':deck.style,'inputs':deck.inputs,'input_roles':deck.input_roles,
        'media':deck.media,'warnings':deck.warnings,'generator_sha256':sha(__file__),
        'original_build_sha256':old.get('original_build_sha256',sha(PPTX)),
        'source_of_truth':'Official PPTX; build refuses to overwrite; revise replaces only explicitly selected semantic slide ids.',
        'visual_defaults':{'bottom_footnotes':False,'bottom_summary_banners':False,'colored_left_box_strips':False,'visible_citations':'under subtitle, explicit user requirement'},
    }
    write(HERE/'build-manifest.json',manifest)


def build(replace_ids=None):
    if PPTX.exists() and not replace_ids:
        raise ValueError(f'Official PPTX exists: {PPTX}. Edit it directly or revise --slides <ids>; no full overwrite.')
    if replace_ids and not PPTX.exists():raise ValueError('No existing official PPTX to revise.')
    d=inputs();plan=make_plan(d);allids={a['id'] for a in plan['slides']}
    if replace_ids and (set(replace_ids)-allids):raise ValueError('Unknown slide id(s): '+str(set(replace_ids)-allids))
    write(HERE/'authoring-plan.json',plan)
    ctu=engine();deck=ctu.Deck(HERE/'authoring-plan.json',HERE);painter=Painter(deck,d)
    # Provenance for all data/code read while authoring, in addition to sources.
    for p in [Path(__file__),SKILL/'scripts/ctu_slides.py',EN_TITLE_SOURCE,VI_TITLE_SOURCE,ROOT/'CLAUDE.md',ROOT/'report/bibliography/references.bib',ROOT/'data/processed/v3-fullpsi/tables/peptides.parquet']:
        deck.inputs[str(p)]=sha(p);deck.input_roles[str(p)]='authoring / evidence input'
    if replace_ids:
        from pptx import Presentation
        deck.prs=Presentation(PPTX);deck.layouts={l.name:l for l in deck.prs.slide_layouts}
        from collections import Counter
        keys=Counter(s._element.cSld.get('name','') for s in deck.prs.slides if s._element.cSld.get('name','').startswith(TAG))
        if any(n>1 for n in keys.values()):raise ValueError('Duplicate authored slide keys. Inspect the PPTX package before scoped revision; no source replaced.')
        for plan_index,a in enumerate(plan['slides']):
            if a['id'] not in replace_ids:continue
            existing={s._element.cSld.get('name','').removeprefix(TAG):i for i,s in enumerate(deck.prs.slides)}
            replace=a['id'] in existing
            if replace:i=existing[a['id']]
            else:
                following=[existing[b['id']] for b in plan['slides'][plan_index+1:] if b['id'] in existing]
                i=following[0] if following else len(deck.prs.slides)
            create_slide(deck,painter,a,i)
            ids=deck.prs.slides._sldIdLst;new=ids[-1];oldid=ids[i] if replace else None
            ids.remove(new);ids.insert(i,new)
            if oldid is not None:ids.remove(oldid);deck.prs.part.drop_rel(oldid.rId)
    else:
        for a in plan['slides']:create_slide(deck,painter,a)
    deck.prs.core_properties.title=plan['deck']['title']
    deck.prs.core_properties.author='Nguyễn Thanh Trọng'
    deck.prs.core_properties.subject='CT553H · Research Progress Report · 7 November 2026'
    deck.prs.core_properties.language='en-US'
    deck.prs.core_properties.keywords='Official Vietnamese title: '+plan['deck']['title_vi']
    deck.prs.core_properties.comments='Editable CTU PowerPoint. Native figures/charts; official PPTX is the maintained source. Evidence scope: development, not gate closure.'
    for i,s in enumerate(deck.prs.slides,1):
        for el in s._element.iter():
            if el.tag.rsplit('}',1)[-1] in ('rPr','defRPr','endParaRPr'):el.set('lang','en-US')
        for el in s.notes_slide._element.iter():
            if el.tag.rsplit('}',1)[-1] in ('rPr','defRPr','endParaRPr'):el.set('lang','en-US')
        for sh in s.shapes:
            if sh.has_text_frame and sh.top>7*914400 and sh.text.isdigit():
                sh.name='CT553H page number'
                sh.text_frame.paragraphs[0].runs[0].text=str(i).zfill(2)
    # Save atomically in the same directory; no alternate report version.
    with tempfile.NamedTemporaryFile(suffix='.pptx',dir=HERE,delete=False) as f:temp=Path(f.name)
    try:
        deck.prs.save(temp)
        with ZipFile(temp) as z:
            names=z.namelist()
            if len(names)!=len(set(names)) or z.testzip() is not None:raise ValueError('Invalid PPTX package; official source was not replaced.')
        os.replace(temp,PPTX)
    finally:temp.unlink(missing_ok=True)
    save_manifest(deck,plan)
    export_notes()
    write_evidence(plan,deck,d)
    print(json.dumps({'pptx':str(PPTX),'slides':len(deck.prs.slides),'revised':replace_ids},ensure_ascii=False))


def export_notes():
    from pptx import Presentation
    prs=Presentation(PPTX);lines=['# Speaker notes — official PPTX','',f'Source: `{PPTX.name}`. Exported from actual PowerPoint Notes; do not edit this file as a competing source.','']
    for i,s in enumerate(prs.slides,1):
        title=next((sh.text for sh in s.shapes if sh.name=='CTU slide title'),s._element.cSld.get('name','Cover'))
        lines.extend([f'## {i:02d}. {title}','',s.notes_slide.notes_text_frame.text,''])
    (HERE/'speaker-notes.md').write_text('\n'.join(lines),encoding='utf-8')


def write_evidence(plan,deck,d):
    write(HERE/'evidence-map.json',{'as_of':'2026-11-07','repository_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'data_identity':d['local']['data_identity'],'scope':'Existing saved evidence, no new model inference/training or experimental bootstrap. Distribution/matrix charts computed from current core table.',
        'slides':[{'number':i,'key':a['id'],'title':a['title'],'source_ids':a['source_ids'],'notes':a['notes']} for i,a in enumerate(plan['slides'],1)],
        'sources':plan['sources'],'sha256':deck.inputs,
        'result_coverage':{'v3_kaggle':47,'v3_local':41,'legacy_r6':23,'new_priority':'OOF k10 replay 07/11','excluded':'synthetic smoke / incomplete LoRA Kaggle / unperformed full finetuning / external / structure'},
        'limits':['Saved artifact audits are cited, not rerun in this slide-authoring task.','PPTX layout verified through LibreOffice export, not Microsoft PowerPoint playback.','Manual PPTX changes remain authoritative; plan/evidence map records the authored snapshot.']})


def renderer_path(explicit=None):
    if explicit:return str(Path(explicit).resolve())
    for name in ['libreoffice','soffice']:
        if shutil.which(name):return shutil.which(name)
    # A previously provisioned relocatable LibreOffice is usable without altering
    # the system, project runtime, or font installation. Fontconfig stays private.
    lo=Path('/tmp/isds-lo/root')
    if (lo/'usr/lib/libreoffice/program/soffice').exists():
        path=HERE/'checks/soffice-local';path.parent.mkdir(exist_ok=True)
        path.write_text('#!/bin/sh\nset -eu\nlo_root=/tmp/isds-lo/root\nexport LD_LIBRARY_PATH="$lo_root/usr/lib/libreoffice/program:$lo_root/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"\nexport UNO_PATH="$lo_root/usr/lib/libreoffice/program"\nexport URE_BOOTSTRAP="vnd.sun.star.pathname:$lo_root/usr/lib/libreoffice/program/fundamentalrc"\nexport SAL_USE_VCLPLUGIN=svp\nexec "$lo_root/usr/lib/libreoffice/program/soffice" "$@"\n',encoding='utf-8')
        path.chmod(0o755)
        return str(path)
    raise ValueError('Provide --soffice /path/to/soffice; no PDF renderer found.')


def render(soffice=None):
    if not PPTX.exists():raise ValueError('Official PPTX missing.')
    from pptx import Presentation
    m=read(HERE/'build-manifest.json');m['deck_sha256']=sha(PPTX);m['slides']=len(Presentation(PPTX).slides)
    # This records the source actually rendered, including intentional manual edits.
    write(HERE/'build-manifest.json',m)
    # Remove only this renderer's stale previews; a shorter deck must not leave
    # extra slide images that could be mistaken for the current source.
    for pattern in ['slides/slide-*.png','review-*.jpg']:
        for p in (HERE/'checks').glob(pattern):p.unlink()
    engine().render(SimpleNamespace(project=str(HERE),soffice=renderer_path(soffice)))
    export_notes()
    make_sheets()


def make_sheets():
    from PIL import Image,ImageDraw,ImageFont
    import fitz
    doc=fitz.open(PDF);font=ImageFont.truetype(str(SKILL/'assets/fonts/k2d/K2D-Regular.ttf'),20)
    # Batches of 8 at a readable scale for visual review of every slide.
    for start in range(0,len(doc),8):
        sheet=Image.new('RGB',(1940,4*580+20),'#e2eaf0');draw=ImageDraw.Draw(sheet)
        for j in range(min(8,len(doc)-start)):
            p=HERE/'checks/slides'/f'slide-{start + j + 1:02d}.png';im=Image.open(p);im.thumbnail((940,529))
            x=20+(j%2)*960;y=20+(j//2)*580
            draw.text((x,y),f'{start + j + 1:02d}',font=font,fill='#17212b');sheet.paste(im,(x,y+30))
        sheet.save(HERE/'checks'/f'review-{start + 1:02d}-{min(start + 8, len(doc)):02d}.jpg',quality=90)


def check():
    rc=engine().check(SimpleNamespace(project=str(HERE)))
    result=validate_rendered_text()
    evidence=validate_numbers()
    language=validate_language()
    return rc or (0 if result['passed'] and evidence['passed'] and language['passed'] else 1)

def validate_language():
    """Check English delivery and the exact canonical bilingual metadata."""
    from pptx import Presentation
    prs=Presentation(PPTX);title_en,title_vi=project_titles();issues=[]
    vietnamese=re.compile('[àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]',re.I)
    allowed=[title_vi,'Nguyễn Thanh Trọng','Hồ Quang Thái']
    def inspect(value,slide,kind):
        for phrase in allowed:value=value.replace(phrase,'')
        if vietnamese.search(value):issues.append({'slide':slide,'kind':kind,'text':value})
        for phrase in ['Input chung','Trong reporter peptide','tra motif','Báo cáo tiến độ','Sau pooling','budget chung','ba seed','hit so W5-D','trong replay']:
            if phrase in value:issues.append({'slide':slide,'kind':kind,'text':value})
    for i,s in enumerate(prs.slides,1):
        for sh in s.shapes:
            if sh.has_text_frame:inspect(sh.text,i,'slide text')
            if sh.has_table:
                for row in sh.table.rows:
                    for cell in row.cells:inspect(cell.text,i,'table')
            if sh.has_chart:
                for c in getattr(sh.chart.plots[0],'categories',[]):inspect(str(c.label),i,'chart label')
                for series in sh.chart.series:inspect(series.name,i,'chart series')
        inspect(s.notes_slide.notes_text_frame.text,i,'speaker notes')
    cover=' '.join(sh.text for sh in prs.slides[0].shapes if sh.has_text_frame)
    checks={'english_title_on_cover':normalize(title_en) in normalize(cover),
            'english_title_metadata':prs.core_properties.title==title_en,
            'english_language_metadata':prs.core_properties.language=='en-US',
            'vietnamese_title_recorded':title_vi in prs.slides[0].notes_slide.notes_text_frame.text and title_vi in prs.core_properties.keywords,
            'english_prose':not issues}
    r={'passed':all(checks.values()),'checks':checks,'issues':issues,'title_en':title_en,'title_vi':title_vi,'language':'en-US','exceptions':'Author/supervisor proper names and the explicitly requested official Vietnamese title in metadata/cover Notes.','pptx_sha256':sha(PPTX)}
    write(HERE/'checks/language-validation.json',r)
    print(json.dumps({'language_validation_passed':r['passed'],'issues':len(issues)},ensure_ascii=False))
    return r


def validate_numbers():
    """Compare actual editable PPTX tables with saved, independently read results."""
    from pptx import Presentation
    from collections import Counter
    prs=Presentation(PPTX);slides={s._element.cSld.get('name','').removeprefix(TAG):s for s in prs.slides}
    checks=[]
    def record(name,ok,detail=None):checks.append(dict(check=name,passed=bool(ok),detail=detail))
    def rows(key):
        return [[c.text for c in row.cells] for sh in slides[key].shapes if sh.has_table for row in sh.table.rows][1:]
    k=read(V3/'output-analysis.json');l=read(V3/'local-output-analysis.json')
    current=read(ROOT/'research/output-review-2026-11-06/results.json')['recipes']
    seen=[]
    for origin in ['kaggle','local']:
        expected=k['recipes'] if origin=='kaggle' else l['local_recipes']
        actual=[r for key in slides if key.startswith('v3-'+origin+'-') for r in rows(key)]
        record(origin+'_recipe_coverage',len(actual)==len(expected) and {r[0] for r in actual}==set(expected),len(actual))
        bad=[]
        for row in actual:
            name,seeds,*vals=row;m=expected[name]['ensemble']['all']
            correct=','.join(map(str,expected[name]['seeds']))==seeds
            correct=correct and all(abs(float(v)-m[col])<=.000050001 for v,col in zip(vals,['mae','rmse','auroc_plus','auprc_plus']))
            if not correct:bad.append(name)
            seen.append(origin+':'+name)
        record(origin+'_PPTX_values_and_seed_support',not bad,bad)
    record('88_distinct_runtime_recipe_rows',len(seen)==len(set(seen))==88,len(seen))
    reconciliation=[]
    for r in current:
        original=k['recipes'][r['recipe']] if r['origin']=='Kaggle' else l['local_recipes'][r['recipe']]
        for col in ['mae','rmse','auroc_plus','auprc_plus']:
            if r['ensemble']['all'][col]!=original['ensemble']['all'][col]:reconciliation.append([r['origin'],r['recipe'],col])
    record('summary_matches_primary_analysis_JSONs',not reconciliation,reconciliation)
    r6=read(ROOT/'research/r6-ladder-scan-2026-10-23/run-kaggle-20261023/results.json')['summaries']
    rr=[r for key in slides if re.fullmatch('history-r6-[0-9]+',key) for r in rows(key)]
    record('23_R6_native_rows',len(rr)==23 and {r[0] for r in rr}==set(r6),len(rr))
    record('R6_values',all(abs(float(r[1])-r6[r[0]]['macro_auroc_ensemble'])<=.000000501 for r in rr))
    g2=read(ROOT/'research/g2-saturation-2026-10-18/results.json')['macro_auroc']
    record('G2_gate_values',all(abs(float(r[1])-g2[r[0]])<=.000000501 for r in rows('history-gate')))
    old=read(ROOT/'research/residue-task-derisk-2026-10-15/model.json')
    record('historical_scanning_columns',all(abs(float(r[1])-old['scanning']['macro_auroc'][r[0]]['mean'])<.000051 and abs(float(r[2])-old['saturation_transfer']['macro_auroc'][r[0]]['value'])<.000051 for r in rows('history-scan')))
    u=read(ROOT/'research/oof-prioritization-2026-11-07/results.json')
    primary={r['policy']:r for r in u['primary_summary']}
    chart=next(sh.chart for sh in slides['priority-results'].shapes if sh.has_chart)
    record('priority_actual_chart_hits',all(abs(a-primary[n]['hits_total'])<1e-9 for a,n in zip(chart.series[0].values,['random','ridge-w5-D','lora-D'])))
    text=' '.join(sh.text for sh in slides['delta'].shapes if sh.has_text_frame)
    record('real_R1A_example',all(v in text for v in ['4.0428','4.4232','+0.3804']))
    counts=Counter(s._element.cSld.get('name') for s in prs.slides)
    record('unique_slide_keys',len(counts)==len(prs.slides))
    with ZipFile(PPTX) as z:
        record('no_duplicate_OPC_entries',len(z.namelist())==len(set(z.namelist())))
        native_charts=len([n for n in z.namelist() if re.fullmatch('ppt/charts/chart[0-9]+.xml',n)])
        record('native_editable_charts_present',native_charts>=8,native_charts)
    plan=read(HERE/'authoring-plan.json');cited={x for s in plan['slides'] if s['kind']!='references' for x in s['source_ids']};refs={x for s in plan['slides'] if s['kind']=='references' for x in s['source_ids']}
    record('zero_citation_orphans',cited==refs,{'cited':len(cited),'referenced':len(refs),'diff':sorted(cited^refs)})
    result={'passed':all(r['passed'] for r in checks),'checks':checks,'scope':'Independent comparison of delivered PPTX numbers against saved source artifacts; not a re-run of training or full scientific validation.','pptx_sha256':sha(PPTX)}
    write(HERE/'checks/numerical-evidence.json',result)
    print(json.dumps({'numerical_evidence_passed':result['passed'],'checks':len(checks),'failures':[r for r in checks if not r['passed']]},ensure_ascii=False))
    return result


def normalize(value):
    import unicodedata
    return re.sub(r'\s+','',unicodedata.normalize('NFKC',value)).replace('\u00ad','')

def retained(text,extracted):
    # LibreOffice PDF fallback glyphs can be emitted as separate runs at the end
    # of a line. Check the textual fragments AND each mathematical glyph.
    glyphs='↔→←↑↓∈α'
    plain=lambda value:re.sub('['+glyphs+']','',normalize(value))
    return plain(text) in plain(extracted) and all(g in extracted for g in text if g in glyphs)


def validate_rendered_text():
    """Check PDF glyph/text retention and text-only overlaps after actual export."""
    import fitz
    from pptx import Presentation
    prs=Presentation(PPTX);doc=fitz.open(PDF);missing=[];small=[];outside=[];overlap=[]
    for i,(s,p) in enumerate(zip(prs.slides,doc),1):
        extracted=normalize(p.get_text())
        boxes=[]
        for sh in s.shapes:
            if sh.has_text_frame:
                if not sh.text.strip():continue
                # Match each paragraph separately, permitting whitespace/reflow.
                for para in sh.text_frame.paragraphs:
                    text=normalize(para.text)
                    if len(text)>2 and not retained(para.text,extracted):missing.append({'slide':i,'shape':sh.name,'text':para.text})
                if sh.name not in ['CTU slide title']:
                    boxes.append((fitz.Rect(sh.left/12700,sh.top/12700,(sh.left+sh.width)/12700,(sh.top+sh.height)/12700),sh.text))
            elif sh.has_table:
                for row in sh.table.rows:
                    for c in row.cells:
                        if not retained(c.text,extracted):missing.append({'slide':i,'shape':'table','text':c.text})
        for j,(a,ta) in enumerate(boxes):
            for b,tb in boxes[j+1:]:
                inter=a&b
                if inter.width>3 and inter.height>3:overlap.append({'slide':i,'a':ta[:55],'b':tb[:55],'intersection':list(inter)})
        for block in p.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                for span in line['spans']:
                    if '\ufffd' in span['text']:missing.append({'slide':i,'replacement_glyph':span['text']})
                    r=fitz.Rect(span['bbox'])
                    if r.x0<-.5 or r.y0<-.5 or r.x1>p.rect.width+.5 or r.y1>p.rect.height+.5:outside.append({'slide':i,'text':span['text'],'bbox':list(r)})
                    inherited_motto=span['text']=='Community - Totality - Uniqueness' and r.y0>p.rect.height*.9
                    if span['size']<8.9 and span['text'].strip() and not inherited_motto:small.append({'slide':i,'text':span['text'],'size':span['size']})
    findings={'passed':not(missing or outside or overlap or small),'pages':len(doc),'text_missing':missing,'outside_canvas':outside,'text_box_overlap':overlap,'small_text_below_8_9pt':small,'pptx_sha256':sha(PPTX),'pdf_sha256':sha(PDF),'scope':'Mechanical retention/geometry only. Text inside chart plots and visual semantics require actual image review. Matrix axis labels 9–10pt are intentional; content tables >=15pt, primary body >=18pt.'}
    write(HERE/'checks/text-layout.json',findings)
    print(json.dumps({'text_layout_passed':findings['passed'],'missing':len(missing),'outside':len(outside),'overlaps':len(overlap),'small':len(small)}))
    return findings


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    sub=ap.add_subparsers(dest='cmd',required=True)
    sub.add_parser('build',help='Create initial deck; refuses existing official PPTX')
    r=sub.add_parser('revise',help='Replace only specified authored slide keys in current PPTX');r.add_argument('--slides',required=True)
    r=sub.add_parser('render',help='Export actual official PPTX to its fixed PDF');r.add_argument('--soffice')
    sub.add_parser('check',help='Structural, source/hash and PDF text/geometry checks')
    sub.add_parser('list',help='List keys for deliberate scoped revision')
    args=ap.parse_args()
    try:
        if args.cmd=='build':build()
        elif args.cmd=='revise':build([x.strip() for x in args.slides.split(',') if x.strip()])
        elif args.cmd=='render':render(args.soffice)
        elif args.cmd=='check':return check()
        else:
            p=read(HERE/'authoring-plan.json')
            for i,s in enumerate(p['slides'],1):print(f'{i:02d}  {s['id']:26s}  {s['title']}')
    except (ValueError,KeyError,OSError) as e:
        print(f'Research report: {e}',file=sys.stderr);return 2
    return 0

if __name__=='__main__':raise SystemExit(main())

