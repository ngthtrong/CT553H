# Aging-related computational biology tasks OTHER THAN sirtuin classification and cellular-senescence protein classification

> **LƯU TRỮ — không dùng để ra quyết định.** Tài liệu lịch sử; mọi câu "chốt / quyết định / khuyến nghị" bên dưới đã hết hiệu lực. Trạng thái hiện hành: [DECISIONS.md](../../../../DECISIONS.md).

> Research notes for the CT553H topic decision. Written 2026-10-02. Scope: candidate aging subdomains with sequence- or structure-based prediction tasks that could carry a PLM + deep-learning thesis for ONE student with ~8–9 weeks of execution, free Colab/Kaggle compute, and a mandatory web application.
>
> **Verification markers used throughout:** `[FULL TEXT]` = I retrieved and read the article page (PMC/MDPI/journal HTML) via automated page read; `[ABSTRACT]` = only abstract/metadata (e.g. PubMed record); `[SNIPPET]` = only a search-engine snippet quoting the paper, page itself not retrieved; `[LINK-TESTED]` = I issued an HTTP request myself on 2026-10-02 and report the status code; `[NOT VERIFIED]` = reported by a secondary source, I could not confirm.
>
> **Conventions:** exact numbers only. Where I could not find a number I write "not found". Where sources disagree I say so.

---

## KQ1. Which aging subdomains have well-defined computational prediction tasks with PUBLIC benchmarks?

### Takeaway

Of the twelve subdomains named in the brief, only **four** have a sequence-based prediction task with a genuinely public, downloadable dataset AND an established independent test set: **autophagy protein classification**, **protein carbonylation site prediction** (oxidative-damage hallmark), **protein aggregation / amyloidogenic region prediction** (proteostasis hallmark), and **lysine glycation site prediction** (AGE hallmark). Two more are public-and-downloadable but have **no** standard split: **aging/longevity gene–protein prediction from GenAge/HAGR**, and **anti-aging peptide prediction from AagingBase**. The rest (SASP, telomere/telomerase, klotho/mTOR/AMPK/IGF1, DNA repair, progeria/laminopathy) have **no established sequence-level benchmark** and should be ruled out as primary topics.

### Cited Findings — data-availability gate, tested today

The Human Ageing Genomic Resources portal is fully open and I downloaded every file myself on 2026-10-02. All returned HTTP 200. Exact record counts are line counts of the extracted files (first line is a header, so genes ≈ lines − 1):

| HAGR dataset | URL | HTTP | zip bytes | extracted file | lines |
|---|---|---|---|---|---|
| GenAge human | `https://genomics.senescence.info/genes/human_genes.zip` | 200 | 9,465 | `genage_human.csv` | 308 |
| GenAge model organisms | `https://genomics.senescence.info/genes/models_genes.zip` | 200 | 48,796 | `genage_models.csv` | 2,206 |
| DrugAge | `https://genomics.senescence.info/drugs/dataset.zip` | 200 | 45,365 | `drugage.csv` | 3,424 |
| CellAge | `https://genomics.senescence.info/cells/cellAge.zip` | 200 | 21,540 | `cellage3.tsv` | 951 |
| GenDR (dietary restriction) | `https://genomics.senescence.info/diet/dataset.zip` | 200 | 8,209 | `gendr_manipulations.csv` | 216 |
| LongevityMap | `https://genomics.senescence.info/longevity/longevity_genes.zip` | 200 | 24,769 | `longevity.csv` | 551 |

— [HAGR download page](https://genomics.senescence.info/download.html) `[FULL TEXT]` + `[LINK-TESTED]`, counts measured by me.

- **Critical:** none of the six HAGR archives contains a train/test split. Each zip holds exactly one data file plus a `release.html`. Any "independent test set" on HAGR data must be constructed by the student, which is exactly the failure mode that killed the previous candidate topic. — measured by me, 2026-10-02 `[LINK-TESTED]`
- Other databases underpinning the residue-level tasks all resolve today (HTTP 200, 2026-10-02): **CarbonylDB** `http://carbonyldb.missouri.edu/CarbonylDB/`; **CPLM** (glycation/PTM) `http://cplm.biocuckoo.cn/`; **WaltzDB** (amyloid hexapeptides) `http://waltzdb.switchlab.org/`; **AagingBase** `https://project.iith.ac.in/cgntlab/aagingbase`; **Peptipedia v2.0** `https://peptipedia.cl/`. `[LINK-TESTED]`

### Cited Findings — subdomain by subdomain

**(a) Aging/longevity gene–protein prediction (GenAge / HAGR).** Task exists and has two published attempts, with a very low performance ceiling when restricted to sequence.
- Kerepesi et al. used **304 ageing-related proteins from GenAge (version 18)** against **19,879 non-ageing human proteins from Swiss-Prot** (20,183 proteins total), extracted ~21,000 features from UniProt + Gene Ontology + GeneFriends, reduced to **36 binary features**, and reported **AUC 0.9322** (XGBoost), **accuracy 98.39% at threshold 0.24**, **F1 0.46458**, **MCC 0.45641**, validated by **5-fold cross-validation repeated 20 times with NO separate independent test set**. Code at `https://github.com/kerepesi/aging_ml`. *Scientific Reports*, published 6 March 2018, DOI 10.1038/s41598-018-22240-w. — [PMC5840292](https://pmc.ncbi.nlm.nih.gov/articles/PMC5840292/) `[FULL TEXT]`
  - Note the F1 of 0.46 next to the 98.39% accuracy: the accuracy figure is an artefact of 304-vs-19,879 imbalance. The honest signal is F1 0.465 / MCC 0.456.
  - Note also that the informative features ("number of ageing-related interaction partners", "response to oxidative stress", "damaged DNA binding") are **annotation/network features, not sequence**. This is circular with respect to a sequence-only task.
- "Fine-Tuning ESM2 for Predicting Ageing-Related Human Proteins" used **320 GenAge sequences + 320 non-ageing UniProtKB/Swiss-Prot sequences = 640**; after preprocessing/filtering the **training set was 160 positive + 160 negative and the test set 34 positive + 30 negative**; fine-tuned **ESM2-t33 with LoRA on attention projections**; reported **accuracy 0.625, F1 0.700, ROC-AUC 0.743**. Published 2026 in the ECC 2025 proceedings *Advances in Intelligent Data Analysis and Applications*, Springer, DOI 10.1007/978-3-032-13048-8_26. — [Springer chapter](https://link.springer.com/chapter/10.1007/978-3-032-13048-8_26) `[SNIPPET]` — the page itself 303-redirects to a Springer IdP login, so I could NOT read the full text; all these numbers come from the search snippet quoting the chapter.
- Pro-longevity vs anti-longevity classification of model-organism genes (mouse, worm, fly, yeast) using "enhanced Gaussian noise augmentation-based contrastive learning (EGsCL)" on **protein–protein interaction networks**, not sequences. — [PMC11616696](https://pmc.ncbi.nlm.nih.gov/articles/PMC11616696/) `[SNIPPET]`
- Dietary-restriction-related gene prediction among ageing-related genes via Positive-Unlabelled Learning. — [arXiv 2406.09898](https://arxiv.org/pdf/2406.09898) `[SNIPPET]`

**(b) Autophagy protein prediction.** The single best-defined aging-adjacent protein-classification benchmark, with a fixed independent test set — but the ceiling is already at the top.
- **PLM-ATG**: training **393 positive (ATGs) / 357 negative**; **independent test 100 positive / 100 negative**; **ESM-2 1280-dim embeddings + AADP-PSSM features**, reduced to a **400-dim optimal subset via SHAP**; independent-test **accuracy 99.5%, MCC 0.990, AUC 0.9998, sensitivity 99.5%, specificity 99.0%**; claimed improvements over ATGPred-FL and EnsembleDL-ATG of "5.0–9.0% Acc, 3.1–9.4% Pre, 6.5–10.5% Sen, 3.0–7.0% Spe, 5.1–7.7% F1, 10–18% MCC". *Molecules* 30(8):1704, 10 April 2025, DOI 10.3390/molecules30081704. Code `https://github.com/YangyingWang/PLM-ATG`. — [PMC12029579](https://pmc.ncbi.nlm.nih.gov/articles/PMC12029579/) `[FULL TEXT]`
  - `https://github.com/YangyingWang/PLM-ATG` → **HTTP 200** `[LINK-TESTED]`
  - Its advertised web server `https://www.cciwyy.top` → **connection failed (curl exit, code 000)** on 2026-10-02. **The published PLM-ATG web server is down.** `[LINK-TESTED]`
- **EnsembleDL-ATG**: independent-test **accuracy 94.5%, F-value 94.4%, recall 93.0%, specificity 96.0%, precision 95.9%, MCC 0.890**; described as "the first autophagy-related gene (ATG) machine learning predictor based on ensemble deep learning", combining CNN + BiLSTM + BiGRU on sequence and evolutionary information; reported ~4% accuracy and 0.08 MCC above ATGPred-FL. *Computational and Structural Biotechnology Journal*, 2023, PMID 37854634, DOI 10.1016/j.csbj.2023.09.036. — [PubMed 37854634](https://pubmed.ncbi.nlm.nih.gov/37854634/) / [publisher](https://spj.science.org/doi/10.1016/j.csbj.2023.09.036) `[SNIPPET]`
- **StackAPP**: "Advancing autophagy protein identification with ensemble learning", *Analytical Biochemistry* 2025, DOI 10.1016/j.ab.2025.116220-family (article ID S0003269725002209). Exact numbers **not found** — I did not retrieve the full text. — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0003269725002209) `[NOT VERIFIED]`
- Crowdedness: a PubMed query `autophagy protein identification machine learning predictor sequence` limited to 2023–2026 returned **total_count = 1** (PMID 37854634). The query is narrow so this undercounts, but combined with manual inspection the field is **three or four predictors total (ATGPred-FL → EnsembleDL-ATG 2023 → PLM-ATG 2025 → StackAPP 2025)**. Uncrowded. — PubMed via MCP, [DOI 10.1016/j.csbj.2023.09.036](https://doi.org/10.1016/j.csbj.2023.09.036) `[ABSTRACT]`

**(c) SASP (senescence-associated secretory phenotype) protein prediction.** **No sequence-based benchmark exists.** Every SASP resource I found is proteomic or transcriptomic: GDF-15 / IGFBP-2 / Cystatin-C associations with aging traits ([PMC10876076](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10876076/)); four SASP component classes identified by unbiased proteomics after genotoxic stress ([aging-us 8:1316](https://www.aging-us.com/full/8/1316)); a senescence gene set that "identifies senescent cells and predicts senescence-associated pathways across tissues" ([Nat Commun 2022](https://www.nature.com/articles/s41467-022-32552-1)); a 7-gene SASP prognostic signature in pancreatic cancer ([PMC12786131](https://pmc.ncbi.nlm.nih.gov/articles/PMC12786131)). `[SNIPPET]` for all four. There is no "predict whether this amino-acid sequence is a SASP factor" task with a public train/test split.

**(d) Telomere / telomerase prediction.** No established benchmark. The only sequence-ML work found is from 2008: structure prediction + machine learning on TERT N-terminal domains from human and yeast, "identified specific amino acids likely to play a role in binding DNA or RNA" — [PubMed 18229711](https://pubmed.ncbi.nlm.nih.gov/18229711/) `[SNIPPET]`. Recent telomere ML papers are transcriptomic prognostics (e.g. telomerase-activation genes in neuroblastoma, [PMC12288417](https://pmc.ncbi.nlm.nih.gov/articles/PMC12288417); telomere-maintenance biomarkers in COPD, [Sci Rep 2025](https://www.nature.com/articles/s41598-025-11347-6)) `[SNIPPET]`. **Rule out.**

**(e) Proteostasis / chaperone / aggregation.** Strong and residue-level, but crowded. See KQ4 for details. Key 2025–2026 entries: **AggrescanAI** predicts residue-level aggregation propensity from **ProtT5** embeddings with no structural input ([PubMed 41548690](https://pubmed.ncbi.nlm.nih.gov/41548690), *J Mol Biol*) `[SNIPPET]`; **AggNet** combines **ESM2 + AlphaFold2** physicochemical/evolutionary/structural information to separate amyloid from non-amyloid peptides and locate aggregation-prone regions (APRs), *Protein Science* 2025, DOI 10.1002/pro.70031 ([PMC11751882](https://pmc.ncbi.nlm.nih.gov/articles/PMC11751882/)) `[SNIPPET]`; **PALM** uses transfer learning from PLM embeddings, trained on **WaltzDB-2.0**, at **single-residue resolution** ([PMC13170650](https://pmc.ncbi.nlm.nih.gov/articles/PMC13170650/)) `[SNIPPET]`; **FA-Amy** uses **ESM C** + attention fusion for amyloid protein prediction ([ScienceDirect S0141813025098241](https://www.sciencedirect.com/science/article/abs/pii/S0141813025098241)) `[SNIPPET]`. A 2025 review warns of "a persistent gap ... driven by limited high quality datasets, class imbalance, weak interpretability, and insufficient experimental validation" `[SNIPPET]`. No dedicated chaperone-client-prediction benchmark was found.

**(f) DNA-repair protein prediction.** Only network-based, no sequence benchmark. "Network-based characterization and prediction of human DNA repair genes and pathways": SVM with RBF kernel, best **precision 0.74 and AUC 0.96**, predicted **32 new DNA repair candidates** — [Sci Rep srep45714](https://www.nature.com/articles/srep45714) `[SNIPPET]`. The adjacent, well-benchmarked task is *DNA-binding protein* prediction, which is a different biology and extremely crowded: benchmark **PDB14189 (7,129 DBPs / 7,060 non-DBPs)** with **independent test PDB2272 (1,153 DBPs / 1,119 non-DBPs)**, plus **PDB186** where a model-stacking framework reached **81.72% accuracy** — [PeerJ 11262 / PMC8101451](https://pmc.ncbi.nlm.nih.gov/articles/PMC8101451/), [PMC6116045](https://pmc.ncbi.nlm.nih.gov/articles/PMC6116045/) `[SNIPPET]`. **Rule out on aging-framing and crowding.**

**(g) Klotho / mTOR / AMPK / insulin-IGF1 pathway protein prediction.** No dedicated public sequence benchmark found. The only mTOR-specific computational work is pathway-structure inference from **phosphorylation data** using hierarchical Bayesian regression with smoothing splines — [PMC10956916](https://pmc.ncbi.nlm.nih.gov/articles/PMC10956916/) `[SNIPPET]`. "Is this protein in the mTOR pathway?" collapses into generic protein function prediction. **Rule out.**

**(h) Anti-aging peptide prediction.** See KQ6 — this is a real, small, public, uncrowded task.

**(i) Caloric-restriction mimetic / senolytic small molecules.** See KQ6 — real and tractable but **cheminformatics (SMILES), not protein sequence**, so it does not fit the advisor's method family.

**(j) Age-related disease protein prediction.** Exists mostly as amyloid/Alzheimer's sequence classification, overlapping (e) and crowded: **ALyzer3D.AI** (PLM embeddings + AlphaFold features for light-chain amyloidogenicity, "generalizes better to independent datasets", *Amyloid* 2025, DOI 10.1080/13506129.2025.2605534); an attention-based BiLSTM amyloid predictor with **AUROC 0.9126** ([PMC11888867](https://pmc.ncbi.nlm.nih.gov/articles/PMC11888867/)); **AD-ProteinNet**, a deep framework classifying protein sequences as AD-related vs healthy ([Springer 10.1007/s42044-025-00331-y](https://link.springer.com/article/10.1007/s42044-025-00331-y)); an ESM-2 + BiLSTM/GRU amyloidogenic-region model ([arXiv 2508.12575](https://arxiv.org/pdf/2508.12575)). All `[SNIPPET]`.

**(k) Mitochondrial aging.** The best-benchmarked proxy is submitochondrial localization, which has established independent test sets. **Mito-Mixer** puts a parameter-efficient **MLP-Mixer on frozen ESM-2 embeddings** with a multi-scale design that preserves N-terminal targeting motifs in long sequences; it "outperformed the latest benchmarks by 9.4% and 16.1% on the **SubMitoPred** dataset" and reached **GCC 0.6945 on the independent M983 test set, a 9.9% improvement over state of the art**. *Algorithms* 19(3):212, DOI 10.3390/a19030212. — [MDPI](https://www.mdpi.com/1999-4893/19/3/212) `[SNIPPET]` — the MDPI page returned HTTP 403 to my automated read, so I could not confirm authors, dataset sizes, or publication month. Predecessors: **DeepMito** (BMC Bioinformatics 2020, [10.1186/s12859-020-03617-z](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-020-03617-z)), **iDeepSubMito** (*Brief Bioinform* 22(6):bbab288, 2021), **DeepPred-SubMito** ([PMC7460811](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7460811/)). `[SNIPPET]`

**(l) Progeria / laminopathy.** No dedicated public prediction benchmark found. The natural framing would be LMNA missense variant-effect prediction, which is a handful of genes and a few hundred variants — far too small, and it is a clinical-genetics task, not a PLM+CNN task. **Rule out.** (This one I searched least; see Gaps.)

### Inferences

- The brief's twelve subdomains collapse to a much smaller real list once "has a public benchmark with a fixed independent test split" is applied as a gate. Five of the twelve (SASP, telomere, klotho/mTOR, DNA repair as *repair*, progeria) have no such task at all.
- There is a systematic pattern: aging subdomains where the biology is a *cellular state or pathway membership* (SASP, senescence, pathway proteins, longevity genes) do not yield good sequence tasks, because the label is not encoded in the sequence. Aging subdomains where the biology is a *molecular damage or binding event* (carbonylation, glycation, aggregation, ATP/NAD binding) do, because the label is local chemistry. The student's existing residue-window pipeline is aligned with the second group, not the first.
- The ESM2+LoRA GenAge result (accuracy 0.625, AUC 0.743, on a 64-sequence test set) is the clearest warning sign in this whole survey: it is not that nobody tried, it is that the sequence signal for "is this protein ageing-related" appears weak. A thesis that beats 0.625 by a few points on 64 test proteins would not be defensible.

### Gaps

- I could not read the full text of the ESM2+LoRA GenAge chapter (Springer login wall), so its redundancy filtering (CD-HIT or not) and whether its 34/30 test split is reusable by others are unknown.
- I could not read the MDPI Mito-Mixer page (HTTP 403), so I do not know its authors (relevant: could it be the Ou group?), nor SubMitoPred / M983 exact sizes.
- Progeria/laminopathy was searched only once and shallowly. If the student wants that angle, it needs a dedicated search.
- No chaperone-client / Hsp70-binding benchmark was searched for specifically.

---

## KQ2. Aging clocks (DNA-methylation, proteomic, transcriptomic) — are these protein-sequence tasks?

### Takeaway

**No. State this plainly to the advisor.** None of the three clock families takes an amino-acid sequence as input. Their input is a per-individual measurement vector (CpG beta values, plasma protein abundances, or transcript counts) and their label is the person's chronological age. The advisor's PLM + multi-window CNN family is architecturally inapplicable, and the data are cohort data behind an application process, not a download. Rule out all three as thesis cores.

### Cited Findings

- **DNA-methylation clocks** quantify methylation at CpG-rich regions, trained on **methylation array data (Illumina Infinium HumanMethylation450K and Infinium MethylationEPIC BeadChips)** against chronological age. Scale example: **DeepStrataAge**, a DNN-based DNAm clock, was "trained on **12,234 CpG sites from 29,167 individuals** using both EPICv1 and EPICv2 methylation arrays". — [npj Aging s41514-026-00358-w](https://www.nature.com/articles/s41514-026-00358-w) and [epigenetic-clock review PMC12905613](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12905613/) `[SNIPPET]`
- **Proteomic clocks** use plasma proteomics (Olink/SomaScan-style abundance panels), not sequences. Organ-specific proteomic aging clocks were developed in **UK Biobank (n = 43,616)** and validated in **China (n = 3,977)** and the **USA (n = 800)**; organ age estimates associate with **heart failure (heart age HR = 1.83)**, **COPD (lung age HR = 1.39)**, **type II diabetes (kidney age HR = 1.58)**, **Alzheimer's disease (brain age HR = 1.81)**. — [Nature Aging s43587-025-01016-8](https://www.nature.com/articles/s43587-025-01016-8) `[SNIPPET]`
- A related plasma-protein organ-aging study reported that having **2–4, 5–7 and 8+ extremely aged organs conferred 2.3-fold, 4.5-fold and 8.3-fold increased risk of death**, and that "a youthful brain and immune system are key to longevity". Another analysed **45,821 UK Biobank adults** across **12 major organs**. — [Cell Metabolism S1550-4131(24)00401-7](https://www.cell.com/cell-metabolism/fulltext/S1550-4131(24)00401-7), [Nature Medicine s41591-025-03798-1](https://www.nature.com/articles/s41591-025-03798-1) `[SNIPPET]`
- **Transcriptomic clocks** need per-sample expression matrices (GEO/ArrayExpress or cohort RNA-seq) — same data shape, same problem. No specific 2024–2026 figure retrieved. `[NOT VERIFIED]`

### Inferences

- The data each clock needs is: (i) a cohort of individuals, (ii) a molecular measurement per individual, (iii) each individual's chronological age. UK Biobank requires an approved application with a fee and a months-long review; this cannot be inside an 8–9-week window. Public GEO methylation series exist and could in principle be assembled into a small clock, but then the student is doing feature selection on tabular data with elastic net — no PLM, no mCNN, no residue windows, and no relationship to the advisor's five criteria except the web app.
- A clock project would score **0 of criteria 2 and 3** (no method improvement within the advisor's lineage, no "beyond PLM" argument), which is exactly the opposite of what the advisor asked for.
- The one defensible use of clocks in this thesis is **as framing in the introduction** ("aging is measurable; here is the molecular-damage side of it"), not as the task.

### Gaps

- I did not test whether any specific GEO methylation series is downloadable today, because the architectural mismatch already decides the question.

---

## KQ3. Per-candidate task sheets: input/output, data today, independent test, SOTA numbers, crowding, 8–9-week feasibility

### Takeaway

Six candidates survive the data gate. Of these, **protein carbonylation site prediction** has the best combination of a public independent test set, a residue-level shape matching the student's existing pipeline, a genuine performance headroom, and an aging hallmark framing. **Autophagy protein classification** has the cleanest data but almost no headroom. **Anti-aging peptide prediction** is the most tractable but the smallest and already near ceiling.

### Candidate 1 — Protein carbonylation site prediction (oxidative damage hallmark). RESIDUE-LEVEL.

- **Task / I/O:** input = protein sequence + a position occupied by K, R, P or T; output = binary, is this residue carbonylated. Four separate models, one per residue type, is the field convention.
- **Public data today:** **CarbonylDB** `http://carbonyldb.missouri.edu/CarbonylDB/` → **HTTP 200** on 2026-10-02 `[LINK-TESTED]`. It "stores **1,495 experimentally validated carbonylation proteins and 3,781 carbonylation sites**". Negative/decoy residues in the current SOTA come from **BioLiP2** (**29,992 ligand-interaction proteins**). — [PMC12199415](https://pmc.ncbi.nlm.nih.gov/articles/PMC12199415) `[FULL TEXT]`
- **Independent test set: YES, established and published.** SCANS training sites: **K 654, P 242, R 293, T 259**. SCANS independent testing sites: **K 323, P 114, R 145, T 124**. Benchmark datasets and source code at `https://github.com/jianzhang-xynu/SCANS` → **HTTP 200** `[LINK-TESTED]`. — [PMC12199415](https://pmc.ncbi.nlm.nih.gov/articles/PMC12199415) `[FULL TEXT]`
- **SOTA, exact numbers (SCANS, *Advanced Science* 12(23):2500581, published 27 March 2025, DOI 10.1002/advs.202500581):** AUROC **K 0.823 / P 0.885 / R 0.900 / T 0.881**; MCC reported in the comparison table as **17.612 / 16.980 / 27.644 / 23.403** (percent scale, i.e. 0.176–0.276); F1 **10.924 / 10.903 / 14.627 / 13.156**; AUCPC **0.118 / 0.067 / 0.055 / 0.060**. Competitor **iCarPS** AUROC **0.627–0.629**. — [PMC12199415](https://pmc.ncbi.nlm.nih.gov/articles/PMC12199415) `[FULL TEXT]`
- **CONFLICT, must be flagged in any report:** the same article's abstract/text states "SCANS records maximum **MCC values ranging from 0.712 to 0.779** across the four datasets, and compared to the second-best method **CarSitePred**, improves the predictive performance by **2.8% to 5.8%**" — [PMC12199415](https://pmc.ncbi.nlm.nih.gov/articles/PMC12199415) `[SNIPPET]`, whereas the comparison table I extracted gives MCC 0.176–0.276 and names **iCarPS** as top competitor. These are almost certainly two different evaluation settings (cross-validated benchmark vs independent test with ligand-site decoys), but I could not confirm which is which. **Do not quote a single MCC for SCANS without saying which setting.**
- **Crowding:** PubMed `carbonylation site prediction`, 2021–2026 → **total_count = 71**, but the query translation expands "carbonylation" to organic-chemistry carbonylation reactions, so this count is heavily inflated. Actual named predictors in the lineage: **CarSitePred, iCarPS, PreCar_Deep (2021, Borderline-SMOTE + deep learning, [ScienceDirect S0169743921001969](https://www.sciencedirect.com/science/article/abs/pii/S0169743921001969)), SCANS (2025)** — roughly four. **Uncrowded.** — PubMed via MCP `[ABSTRACT]`; [DOI 10.1002/advs.202500581](https://doi.org/10.1002/advs.202500581)
- **Feasibility 8–9 weeks + web app:** high. Data is small (hundreds to low thousands of sites per residue type); ProtT5/ESM-2 embeddings over a few thousand windows are minutes-to-hours on free Colab; mCNN training is cheap. A FastAPI + React site that takes a FASTA, scores every K/R/P/T, and renders a per-residue track is well within scope.
- **Advisor-criteria fit:** 1 novelty — PLM+mCNN has NOT been applied to carbonylation (SCANS is attention+transfer learning, earlier work is handcrafted features); 2 method improvement — direct, mCNN/msCNN on carbonylation; 3 beyond-PLM — the RAG retrieval layer from RAG-msCNN transfers directly; 4 XAI — SCANS itself only did ablation + motif analysis, leaving SHAP/attribution room, and BERT-Promoter is the in-house precedent; 5 web app — yes. **Scores 5/5.**
- **Aging framing:** protein carbonylation is the canonical irreversible oxidative-damage modification; "loss of proteostasis" and oxidative damage are hallmarks of aging. Framing is honest but needs one sentence of care: carbonylation is a damage marker, not an aging clock.

### Candidate 2 — Autophagy protein classification. SEQUENCE-LEVEL (whole protein).

- **Task / I/O:** input = full protein sequence; output = binary, autophagy-related protein (ATG) or not.
- **Public data today:** the PLM-ATG repository `https://github.com/YangyingWang/PLM-ATG` → **HTTP 200** `[LINK-TESTED]`, and it is stated to carry data and code.
- **Independent test set: YES**, fixed at **100 positive / 100 negative**; training **393 positive / 357 negative**. — [PMC12029579](https://pmc.ncbi.nlm.nih.gov/articles/PMC12029579/) `[FULL TEXT]`
- **SOTA:** PLM-ATG independent test **Acc 99.5%, MCC 0.990, AUC 0.9998, Sn 99.5%, Sp 99.0%** (*Molecules* 30(8):1704, 10 April 2025). Previous: EnsembleDL-ATG **Acc 94.5%, MCC 0.890** (CSBJ 2023). — `[FULL TEXT]` / `[SNIPPET]`
- **Crowding:** ~4 predictors total. Uncrowded.
- **Feasibility:** very high — 950 sequences total, trivial compute.
- **The problem:** **there is essentially no headroom.** 99.5% accuracy and MCC 0.990 on a 200-sequence independent test leaves nothing to improve, and PLM-ATG already used ESM-2 **plus SHAP**, i.e. it already occupies criteria 3 and 4.
- **The counter-opportunity:** 99.5% on 200 sequences with 393/357 training is a strong smell of **sequence redundancy between train and test**. The student's existing leakage-control protocol (CD-HIT clustering, identity-stratified evaluation) applied to the ATG benchmark could show the reported number collapses under identity control. That is a defensible contribution of exactly the kind the student already prepared for RTK–ATP — and the dead `cciwyy.top` server means a working web app is also a real deliverable. **But** it is a negative-result thesis, which is riskier to defend at undergraduate level, and it does not propose a new method.

### Candidate 3 — Anti-aging peptide prediction. SEQUENCE-LEVEL (short peptides).

See KQ6 for full numbers. Summary: data public (**AagingBase, 282 validated AAPs**), independent test sets exist but are **small and inconsistent across papers (40 sequences in one; two unnamed sets in another)**, SOTA already **AUC 0.99 on independent test**, field **uncrowded (6 PubMed hits 2023–2026, only ~3 real predictors)**, feasibility **very high**, but the **window/mCNN shape does not apply** (peptides are 2–80 aa, so there is no residue-window problem to solve) and the headroom is near zero.

### Candidate 4 — Aggregation-prone region / amyloidogenicity prediction. RESIDUE-LEVEL.

- **Task / I/O:** input = sequence; output = per-residue aggregation propensity, or binary APR membership; a second variant is whole-peptide amyloid vs non-amyloid (hexapeptides).
- **Public data today:** **WaltzDB-2.0** `http://waltzdb.switchlab.org/` → **HTTP 200** `[LINK-TESTED]`. Also AmyPro and CPAD are referenced in the literature (not tested).
- **Independent test set:** the field has conventional benchmarks (WaltzDB splits, and each paper's own held-out sets), but I did **not** find a single canonical independent test set the way ATG or carbonylation have. `[NOT VERIFIED]`
- **SOTA:** **AggNet** claims state-of-the-art on protein aggregation prediction with ESM2 + AlphaFold2 (*Protein Science* 2025, DOI 10.1002/pro.70031); **AggrescanAI** does residue-level propensity from **ProtT5** embeddings (*J Mol Biol*, PubMed 41548690); **PALM** works at single-residue resolution on WaltzDB-2.0; an attention-BiLSTM amyloid predictor reports **AUROC 0.9126** ([PMC11888867](https://pmc.ncbi.nlm.nih.gov/articles/PMC11888867/)). Exact head-to-head numbers **not found**. `[SNIPPET]`
- **Crowding: HIGH.** AggNet (2025), AggrescanAI (2026), PALM (2025), FA-Amy (2025), ALyzer3D.AI (2025), arXiv ESM-2+BiLSTM (2025) — at least six 2025–2026 entries, and **AggrescanAI already uses ProtT5, the student's exact embedding**. This is the most saturated of the residue-level options.
- **Feasibility:** high compute-wise, but the literature-positioning work alone would eat weeks.

### Candidate 5 — Lysine glycation site prediction (advanced glycation end products). RESIDUE-LEVEL.

- **Task / I/O:** input = sequence + a lysine position; output = binary glycated or not.
- **Public data today:** **CPLM** `http://cplm.biocuckoo.cn/` → **HTTP 200** `[LINK-TESTED]`; PLMD is the other source cited in the literature (not tested separately).
- **Independent test sets: YES, multiple published ones.** Glypre used an independent set of **20 proteins with 37 lysine glycation sites** from PLMD. **BERT-Kgly** used a dataset of **3,969 positive and 82,270 negative samples**, trained on ~**3,573 positives plus an equal number of negatives**, with an **independent test set of 200 positive + 200 negative**. A 2025 RNN approach split **4,830 training sequences / 1,000 internal validation / 1,000 independent test**. — [Glypre, Molecules 2017](https://doi.org/10.3390/molecules22111891), [BERT-Kgly, PMC9580886](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9580886/), [PMC12436683](https://pmc.ncbi.nlm.nih.gov/articles/PMC12436683/) `[SNIPPET]` for all three
- **SOTA:** **PredGly** (*Bioinformatics* 35(16):2749, 2019) reported **sensitivity 0.887, specificity 0.899, accuracy 0.893, MCC 0.785**. — [Bioinformatics](https://academic.oup.com/bioinformatics/article/35/16/2749/5259189) `[SNIPPET]`. BERT-Kgly's exact independent-test numbers **not found**. The 2025 RNN paper's numbers **not found**.
- **Crowding: LOW-MODERATE** — Gly-PseAAC (2016), Glypre (2017), PredGly (2019), BERT-Kgly (2022), RNN approach (2025). Five predictors in nine years.
- **Opportunity:** I found **no published ProtT5/ESM-2 + multi-window CNN** glycation predictor. BERT-Kgly uses a BERT-style model but is 2022 and pre-dates the current PLM generation. This is a real criterion-1/2/3 opening.
- **Aging framing:** glycation produces advanced glycation end products (AGEs), a classic aging and diabetes-complication mechanism. Honest framing, but weaker than carbonylation because glycation is often framed as diabetes rather than aging.
- **Feasibility:** high. Data small, residue-window shape identical to the student's pipeline.

### Candidate 6 — Submitochondrial localization (mitochondrial aging proxy). SEQUENCE-LEVEL with positional signal.

- **Independent test set: YES — the M983 set**, plus the SubMitoPred benchmark. `[SNIPPET]`
- **SOTA:** Mito-Mixer, **GCC 0.6945 on M983**, +9.9% over prior SOTA; +9.4% and +16.1% on SubMitoPred. *Algorithms* 19(3):212. `[SNIPPET]` — MDPI page returned 403 to me.
- **Crowding:** moderate (DeepMito 2020, DeepPred-SubMito 2020, iDeepSubMito 2021, a GO-based 2023 method, Mito-Mixer 2026).
- **The blocking problem:** Mito-Mixer is **already** "multi-scale feature mixing over frozen ESM-2 embeddings" — which is the advisor's msCNN idea in MLP-Mixer clothing, published before the student would start. And the aging framing is weak (mitochondrial *localization* is not mitochondrial *aging*). **Plus** the wider group already owns an adjacent paper: see KQ5 (MCNN_MC, mitochondrial carriers, PLM+CNN, JCIM 2024). Novelty is squeezed from both sides.

### Inferences

- Ranking the six by headroom alone: carbonylation (large headroom, AUROC 0.82–0.90 and MCC well under 0.3 on independent test) > glycation (no modern PLM baseline exists) > aggregation (crowded, ProtT5 already used) > submitochondrial (msCNN-equivalent already published) > anti-aging peptides (AUC 0.99) > autophagy (MCC 0.990).
- Carbonylation and glycation are the only two where the student can simultaneously claim a method contribution AND report a number that is not already saturated.

### Gaps

- SCANS's conflicting MCC figures could not be reconciled without reading the supplementary material.
- StackAPP (autophagy, 2025) numbers not retrieved — the student should check it before claiming PLM-ATG is SOTA.
- No exact head-to-head table for aggregation predictors.

---

## KQ4. Which candidates are RESIDUE-LEVEL window-classification problems (the student's existing pipeline shape)?

### Takeaway

Four: **carbonylation sites**, **lysine glycation sites**, **aggregation-prone regions**, and **LIR/AIM motifs**. Carbonylation and glycation map onto the student's existing PLM-embedding + windows-around-a-residue + multi-window-CNN code with essentially no architectural change — only the label file and the residue filter change.

### Cited Findings

- **Carbonylation (K, R, P, T): residue-level, four-way-split, with published independent test sites (K 323, P 114, R 145, T 124).** This is the same problem shape as ATP-binding-site prediction: a sequence, a position, a binary label, with heavy negative imbalance. — [PMC12199415](https://pmc.ncbi.nlm.nih.gov/articles/PMC12199415) `[FULL TEXT]`
- **Lysine glycation: residue-level**, windows around K, with published independent test sets (200+200 in BERT-Kgly; 1,000 in the 2025 RNN work). Known positional signal: "abundance of alanine (A), valine (V), glycine (G), and methionine (M) upstream and downstream, while lysine (K) and arginine (R) were depleted at positions +1 through +4" — directly a window-feature story that an mCNN can exploit and SHAP can explain. — [search synthesis over Glypre/PredGly/BERT-Kgly](https://academic.oup.com/bioinformatics/article/35/16/2749/5259189) `[SNIPPET]`
- **Aggregation-prone regions: residue-level.** "AggrescanAI ... predicts **residue-level** aggregation propensity directly from sequence, leveraging contextual embeddings from the **ProtT5** protein language model ... without requiring structural data"; "PALM ... identify aggregation-prone regions within a sequence at **single-residue resolution**". — [PubMed 41548690](https://pubmed.ncbi.nlm.nih.gov/41548690), [PMC13170650](https://pmc.ncbi.nlm.nih.gov/articles/PMC13170650/) `[SNIPPET]`
- **LIR / AIM motif in autophagy: motif-level, i.e. a short window.** The core motif is **[W,Y,F][X][X][L,I,V]** — "an aromatic amino acid followed by any two amino acids and a hydrophobic residue". "Since the canonical AIM/LIR sequence can be found in many proteins, identifying **functional** AIM/LIR motifs has proven challenging" — i.e. the task is exactly discrimination of true positives among regex matches, which is a window-classification problem. Resources: **iLIR** web server (regex-based, 2014, [PMC5119064](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5119064/)); **LIRcentral**, "a manually curated online database of experimentally validated functional LIR-motifs" ([bioRxiv 2022.06.21.496832](https://www.biorxiv.org/content/10.1101/2022.06.21.496832v1.full)); **AlphaFold2-Multimer-guided prediction** of typical and atypical ATG8-binding motifs, with AF2 and Uni-Fold both reported to show "high accuracy" ([PMC9907853](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9907853/), [PLOS Biology 2023](https://journals.plos.org/plosbiology/article?id=10.1371%2Fjournal.pbio.3002002)); an AF2 SLiM screen for LC3–LIR interactions ([PMC12582063](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12582063/)). All `[SNIPPET]`.
- **NOT residue-level:** autophagy protein classification (whole protein), anti-aging peptide prediction (whole short peptide), aging/longevity gene prediction (whole protein), submitochondrial localization (whole protein, though the N-terminal targeting signal is positional), all aging clocks (not sequences at all), senolytic compound prediction (molecules).

### Inferences

- **LIR motif prediction is the most intellectually attractive residue-level aging task that nobody has done with a PLM**: the current best method is AlphaFold2-Multimer, which is expensive, and a PLM+mCNN classifier over regex-matched windows would be a legitimately novel, cheap alternative. **But** three things block it for an 8–9-week undergraduate project: (i) LIRcentral's positive set is on the order of hundreds of motifs, so statistics will be fragile; (ii) there is **no established independent test set** — which is the exact gate that killed the previous topic; (iii) the honest baseline comparison is AF2-Multimer, which the student cannot run at scale on free Colab. I would keep it as a *secondary* research question, not the core.
- Carbonylation and glycation are the two that let the student reuse code rather than write it. For a week-6 pitch, "I already have this pipeline running on ATP sites; I am re-pointing it at oxidative-damage sites with a published independent test set" is a much stronger story than any from-scratch plan.

### Gaps

- I did not verify LIRcentral's exact record count or whether its download resolves today.

---

## KQ5. Has QT Ho's group — or the wider Ou group — published in any of these aging subdomains?

### Takeaway

**Almost none.** Across both publication lists available locally, there is exactly **one** aging-domain paper: QT Ho's **SirtSAGE (2026, sirtuins)**. Neither list contains anything on autophagy, carbonylation, glycation, aggregation, telomeres, aging clocks, anti-aging peptides, DNA repair, or progeria. The wider group does own **two adjacent non-aging papers** that matter for novelty positioning: **MCNN_MC** (mitochondrial carriers, PLM+CNN) and **mCNN-ETC** (electron transport chain).

### Cited Findings

Source for both lists: the repository's own Google Scholar scrapes, `/home/ngthtrong/CT553H/docs/common/advisor/Prof Ho/research.md` (14 works) and `/home/ngthtrong/CT553H/docs/common/advisor/Prof Ou/research.md`. I ran a case-insensitive keyword scan for sirtuin|aging|ageing|senescen|autophag|telomer|longevity|lifespan|mitochondr|cancer|neoantigen|tumor over both. `[FULL TEXT — local files]`

**QT Ho (advisor) — aging-relevant entries in the 14-work list:**
- **SirtSAGE: A Structural-Gated Graph Attention Framework for the Unified Classification and Evolutionary Mapping of Sirtuin Proteins**, DQ Nguyen, VT Nguyen, M Hussain, QT Ho, *Journal of Computational Biophysics and Chemistry*, 1–28, **2026**. The only aging-domain paper in his record.
- **Nothing else** in the 14 touches aging. No autophagy, no PTM-damage sites, no telomeres, no clocks, no peptides.

**QT Ho — residue-level window-classification precedents (why carbonylation/glycation fit him):**
- *Using multiple convolutional window scanning of convolutional neural network for an efficient prediction of ATP-binding sites in transport proteins*, TTD Nguyen, S Chen, QT Ho, YY Ou, *Proteins* 90(7):1486–1492, **2022**.
- *msCNN-PLM-FAD: Enhanced predicting FAD binding sites by using protein language representation combined with multiple separable windows convolutional neural networks*, DQ Nguyen, VT Nguyen, CH Ly, YY Ou, QT Ho, *Analytical Biochemistry*, 116092, **2026**.
- *RAG-msCNN: predicting protein-DNA binding sites by integration of retrieval-augmented generation (RAG) with protein language models and the multi-scale separable convolutional …*, MS Malik, M Hussain, QT Ho, VT Le, YY Ou, *Biomedical Signal Processing and Control* 115:109407, **2026**.

**QT Ho — XAI precedent (criterion 4):**
- *BERT-Promoter: An improved sequence-based predictor of DNA promoter using BERT pre-trained model and **SHAP** feature selection*, NQK Le, QT Ho, VN Nguyen, JS Chang, *Computational Biology and Chemistry* 99:107732, **2022** (124 citations).

**QT Ho — mitochondria-adjacent (relevant to the mitochondrial-aging candidate):**
- *mCNN-ETC: identifying electron transporters and their functional families by using multiple windows scanning techniques in convolutional neural networks with evolutionary …*, QT Ho, NQK Le, YY Ou, *Briefings in Bioinformatics* 23(1):bbab352, **2021**.

**YY Ou (wider group, NOT the advisor) — keyword-scan hits:**
- *MCNN_MC: computational prediction of **mitochondrial carriers** and investigation of bongkrekic acid toxicity using **protein language models and convolutional neural networks***, MS Malik, YY Chang, YC Liu, VT Le, YY Ou, *Journal of Chemical Information and Modeling* 64(24):9125, **2024** (7 citations). **This is PLM + CNN on a mitochondrial protein class — the wider group already occupies the mitochondrial-protein niche.**
- *NeoGen-BC: A Synergistic Framework Combining Generative Protein Language Models and Multi-Window Deep Learning for Designing Shared Neoantigens in **Breast Cancer***, VT Le, JPT Yuune, JI Lai, YY Ou, *Biochemical and Biophysical Research Communications*, 154567, **2026**.
- *DeepNeoAG: Neoantigen epitope prediction from **melanoma** antigens using a synergistic deep learning model combining protein language models and multi-window scanning …*, CC Chuang, YC Liu, YY Ou, *International Journal of Biological Macromolecules* 281:136252, **2024** (16 citations).
- *RTK_RAG: leveraging retrieval augmented generation with multi-window convolutional neural networks for superior ATP binding site prediction in receptor tyrosine kinases*, SS Wei, WE Jhang, YC Liu, CC Chuang, YY Ou, *Journal of Chemical Information and Modeling* 65(13):7277.
- **Correction to a naive keyword scan:** my "aging" keyword hit on the Ou list was a false positive — it matched the word "le**verag**ing" in the RTK_RAG title. **The Ou list contains no aging paper at all.** `[FULL TEXT — local file]`

### Inferences

- **Supervision quality by subdomain:** the advisor can supervise the *method* (PLM → mCNN/msCNN → RAG, SHAP for XAI, residue-window framing) extremely well for any of the residue-level candidates, because that is literally what his 2022 ATP-sites and 2026 FAD-sites papers are. He can supervise the *aging biology* only for sirtuins. For carbonylation, glycation, autophagy or aggregation, the student will be the one bringing the domain reading — which is acceptable and even desirable at thesis level, but the student must prepare a one-page biology briefing for the week-6 meeting so the advisor is not asked to evaluate unfamiliar biology cold.
- **Novelty is wide open in every one of these subdomains**, measured against the advisor's own record: there is no QT Ho paper on carbonylation, glycation, autophagy, aggregation, telomeres, peptides or clocks. Criterion 1 is easy to argue.
- **The mitochondrial candidate is the one to be careful about**: between MCNN_MC (Ou, 2024, PLM+CNN, mitochondrial carriers), mCNN-ETC (Ho, 2021, electron transporters) and Mito-Mixer (2026, multi-scale over ESM-2, submitochondrial localization), a "PLM + multi-window CNN for mitochondrial protein X" pitch would be met with "we did that". Avoid.
- Framing opportunity for the week-6 pitch: SirtSAGE is about *the enzymes that reverse* a damage modification (sirtuins are deacylases). A thesis on carbonylation or glycation is about *the damage modifications themselves*. That is a clean "adjacent to your newest paper, not duplicating it" story — and the student can say it in one sentence.

### Gaps

- Both lists are local Google Scholar scrapes (14 works for Ho; the Ou file is longer but I did not count it). They may be incomplete. "No aging paper besides SirtSAGE" means "none in these scrapes", not a certainty. This is already flagged in the repo's own `advisor/README.md`.
- I could not determine the authors of Mito-Mixer (MDPI 403), so I cannot rule out that it is an Ou-group paper. **The student should check this before considering any mitochondrial topic.**

---

## KQ6. Anti-aging / senolytic PEPTIDE and small-molecule prediction tasks with curated public datasets

### Takeaway

Both exist and both are small and tractable. **Peptides** fit the advisor's protein-sequence world but are already at AUC 0.99 and are too short for a window/mCNN contribution. **Small molecules** (senolytics, caloric-restriction mimetics) are cheminformatics on SMILES — tractable and genuinely under-explored, but architecturally outside the advisor's method family, so they score 0 on criteria 2 and 3.

### Cited Findings — peptides

- **AagingBase** (the source database): "houses experimentally validated **282 anti-aging peptides** collected from **54 research articles and 236 patents**"; of the 282, "**144 are natural, 136 are synthetic peptides, and 2 peptides have unknown origins**"; "can be accessed without any restriction" at `https://project.iith.ac.in/cgntlab/aagingbase`. *Database (Oxford)* 2024, baae016. — [Database article](https://academic.oup.com/database/article/doi/10.1093/database/baae016/7627161), [PMC10930205](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10930205/) `[SNIPPET]`; link → **HTTP 200** on 2026-10-02 `[LINK-TESTED]`
- **Antiaging-FL / ESM_GAN / ESM_CNN** (Zhang et al., *BMC Biology* 23(1):362, published 24 December 2025, PMID 41444580, DOI 10.1186/s12915-025-02469-4):
  - Dataset: **220 positive + 220 negative** peptides (positives filtered down from the 282 in AagingBase; negatives assembled from pro-inflammatory peptides, then inactive peptide precursors, then cytotoxic peptides, **CD-HIT at 90% similarity**), called **AAP400**; **independent test set of 40 sequences**. — [PMC12729081](https://pmc.ncbi.nlm.nih.gov/articles/PMC12729081/) `[FULL TEXT]`
  - **CONFLICT:** a search snippet for the same work says the benchmark is "**440 peptide sequences** (referred to as AAP400 dataset)", while the full-text read gives 220+220 with a 400-sequence training set and 40 held out. 220+220 = 440, and 440 − 40 = 400, so the most likely reconciliation is **440 total = 400 train (AAP400) + 40 independent test**, but I could not confirm this explicitly. `[SNIPPET]` vs `[FULL TEXT]`
  - Performance: **Antiaging-FL — AAP400 accuracy 99.7%, AUC 1.00, MCC 0.995; independent test AUC 0.99**. **ESM_GAN — AUC 0.99 (AAP400) / 0.95 (independent)**. **ESM_CNN — AUC 0.96 / 0.94**. (The paper's own abstract gives ESM_CNN as 0.96/0.94 and the comparison table also lists "CNN_9x AUC 0.94" and "ESM_9x AUC 0.95" on the independent test.) Optimal feature subset: **4 dimensions (DDE, AAC+TPC, CTriad k=4, CKSAAP k=2)** from **40 handcrafted descriptors plus ESM embeddings**, selected by recursive feature elimination over SVM/RF/LR/XGBoost/KNN. — [PMC12729081](https://pmc.ncbi.nlm.nih.gov/articles/PMC12729081/) `[FULL TEXT]`, [PubMed 41444580](https://pubmed.ncbi.nlm.nih.gov/41444580/) `[ABSTRACT]`
  - Code `https://github.com/zhangzhiyuan257/anti_aging` → **HTTP 200** `[LINK-TESTED]`. Web servers listed as `http://124.222.115.164/` and `http://www.stay67.com`; **`http://124.222.115.164/` failed to connect (curl code 000)** on 2026-10-02 `[LINK-TESTED]`.
- **AagingPEPred** (IIT Hyderabad CGNT Lab server, `https://project.iith.ac.in/cgntlab/aagingpepred/` → **HTTP 200** `[LINK-TESTED]`): accepts FASTA peptides of **5–50 amino acids**; built on "**216 positive peptides from AagingBase and an equivalent negative dataset of 216 peptides**" generated with Python's random library, **432 sequences total**; best model **XGBoost, accuracy 80%** on both training and test. — [AagingPEPred](https://project.iith.ac.in/cgntlab/aagingpepred/) `[FULL TEXT]`
- **AAGP** (*Scientific Reports* 15:29036, 2025, DOI 10.1038/s41598-025-12759-0): considered **4,305 features across 57 feature types**, with customised feature subsets from a heuristic subset-selection algorithm; on **two independent test datasets** it reports **MCC 0.692 and 0.580** and **AUC 0.963 and 0.808**; physicochemical features mattered more for the first dataset, compositional for the second. — [Nature](https://www.nature.com/articles/s41598-025-12759-0) `[SNIPPET]` — the page returns HTTP 200 to curl but 303-redirects my automated reader to a Nature IdP login, so the numbers are snippet-sourced.
- **BioPepAE** (*Food Chemistry* 523:150193, 2026, DOI 10.1016/j.foodchem.2026.150193): auto-encoder framework using **peptide atomic 3D information from AlphaFold 3**, multi-task over anti-hypertensive, anti-oxidant and anti-aging peptides; **AAP accuracy 92.86%** (AHP 94.65%, AOP 95.47%); "demonstrated strong generalization on independent tests"; identified 5 AAPs from wheat germ protein hydrolysates with in-vitro confirmation. — PubMed 42364472, [DOI](https://doi.org/10.1016/j.foodchem.2026.150193) `[ABSTRACT]`
- **Peptipedia v2.0** (*Database* 2024, baae113, PMID 39514414): expanded by >45%; the activity tree now includes an "**antiageing**" category; "**more than 90 binary classification models**" using protein language models, with average **sensitivity 0.877 ± 0.0530 and specificity 0.873 ± 0.054**, used to annotate >3.6 million peptides. `https://peptipedia.cl/` → **HTTP 200** `[LINK-TESTED]`. — [DOI 10.1093/database/baae113](https://doi.org/10.1093/database/baae113) `[ABSTRACT]`
- **PepBenchmark** provides a standardised **"antiaging" dataset of 558 datapoints, sequences 2 to 80 amino acids** — i.e. a ready-made split, which is the most useful thing for the independent-test-set gate. — [arXiv 2604.10531](https://arxiv.org/html/2604.10531v1) `[SNIPPET]`
- **Crowding:** PubMed query `(anti-aging peptide[Title] OR antiaging peptide[Title]) AND (prediction OR machine learning OR deep learning)`, 2023–2026 → **total_count = 6**: PMIDs 42364472 (BioPepAE, *Food Chem* 2026), 42090918 (salty-peptide EEG study, **not relevant**), 41180303 (methyl-jasmonate peptide docking study, **not a predictor**), 39514414 (Peptipedia v2.0), 37579838 (EQ-9 peptide virtual screening, *Peptides* 2023), 37349941 (Syn-Ake docking/MD, **not a predictor**). Only **two or three** of the six are actual AAP classifiers; Antiaging-FL (PMID 41444580, Dec 2025) and AAGP (Sci Rep 2025) did not appear in this exact query. **Field is genuinely small.** — PubMed via MCP; DOIs [10.1016/j.foodchem.2026.150193](https://doi.org/10.1016/j.foodchem.2026.150193), [10.1093/database/baae113](https://doi.org/10.1093/database/baae113), [10.1016/j.peptides.2023.171078](https://doi.org/10.1016/j.peptides.2023.171078), [10.1080/07391102.2023.2223681](https://doi.org/10.1080/07391102.2023.2223681), [10.1155/ijog/9783996](https://doi.org/10.1155/ijog/9783996), [10.1016/j.foodchem.2026.149460](https://doi.org/10.1016/j.foodchem.2026.149460) `[ABSTRACT]`

### Cited Findings — small molecules (senolytics, CR mimetics)

- **Senolytic predictor** (*Molecules* 30(12):2653, 2025): training set of "**111 positive and 3,951 negative compounds**" curated from the literature; models used "traditional molecular fingerprints, molecular descriptors, and **MoLFormer molecular embeddings**"; final predictor an **SVM + MLP** ensemble; virtual screening applied to **DrugBank and TCMbank**. — [PMC12196162](https://pmc.ncbi.nlm.nih.gov/articles/PMC12196162/), [MDPI](https://www.mdpi.com/1420-3049/30/12/2653) `[SNIPPET]`
- **SenolyticSynergy** (bioRxiv 2025.05.28.655258): multimodal attention model trained on "**1,624 core aging-related genes**", used **63 established senolytic compounds** to build "**1,953 potential drug combinations**", of which "**190 high-confidence drug combinations**" survived filtering; code and data on a Gitee repository. — [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.05.28.655258v1.full) `[SNIPPET]`
- **Discovery of senolytics using machine learning**, *Nature Communications* 2023, DOI 10.1038/s41467-023-39120-1 — the landmark paper in this line. Exact dataset sizes and performance **not found** (I did not retrieve it). — [Nature Communications](https://www.nature.com/articles/s41467-023-39120-1) `[NOT VERIFIED]`
- **Caloric-restriction mimetics / lifespan-extending compounds:** **DrugAge** is the public dataset and is downloadable (**drugage.csv, 3,424 lines**, verified by me). A 2024 *Aging* paper, "Predicting lifespan-extending chemical compounds for C. elegans with machine learning and biologically interpretable features", exists at [aging-us article 204866](https://www.aging-us.com/article/204866/text), but the page returned **HTTP 403** to my automated reader, so **its dataset size, methods and performance numbers are not found.** `[NOT VERIFIED]`

### Inferences

- The peptide line has one genuine, defensible gap: **the published web servers are dying.** `124.222.115.164` (Antiaging-FL) and `cciwyy.top` (PLM-ATG) both failed to connect today, and AagingPEPred's model is only 80% accurate. "The field's tools are unavailable or weak; I built a working, documented one" is a real criterion-5 contribution and a credible thesis motivation — but on its own it is a software contribution, not a research one.
- The small-molecule senolytic line is attractive on tractability (111 positives, a few thousand negatives, SMILES fingerprints train in minutes on CPU) and on being less crowded than protein tasks. **But** it requires the student to learn RDKit/cheminformatics from zero, it uses no protein language model, and it cannot be framed as an extension of mCNN/msCNN/RAG. Against the advisor's five criteria it scores 1 (novelty) and 5 (web app) and nothing else. **Rule out on method-fit, and say so explicitly rather than silently.**

### Gaps

- The *Nature Communications* 2023 senolytics numbers and the *Aging* 2024 C. elegans numbers are both unverified (one not fetched, one 403).
- AAGP's exact dataset sizes and whether its two independent test sets are published as files were not confirmed.
- Whether PepBenchmark's antiaging split is downloadable today was not link-tested.

---

## KQ7. Final ranking: (public data with a genuine independent test set) × (room for a real contribution) × (feasibility in 8–9 weeks)

### Takeaway

**Rank 1: protein carbonylation site prediction.** It is the only candidate that scores high on all three factors simultaneously, it is residue-level so the student reuses existing code, and it hits all five of the advisor's criteria. **Rank 2: lysine glycation site prediction** — same shape, slightly weaker aging framing, no modern PLM baseline to beat. **Rank 3: autophagy protein classification reframed as a leakage audit.** Everything else I would rule out, and the reasons differ.

### Cited Findings — the ranking, with the reasoning made explicit

Scoring key: **Data** = public + downloadable today + established independent test set (verified by me where marked `[LINK-TESTED]`). **Room** = headroom against published SOTA + how many of the advisor's criteria 1–4 remain open. **Feas** = 8–9 weeks on free Colab including a web app.

| # | Candidate | Residue-level? | Data | Room | Feas | Advisor criteria covered |
|---|---|---|---|---|---|---|
| **1** | **Carbonylation sites (K/R/P/T)** | **YES** | **HIGH** — CarbonylDB 200 OK, SCANS GitHub 200 OK, published independent test (K 323 / P 114 / R 145 / T 124) | **HIGH** — SOTA AUROC 0.823–0.900 with independent-test MCC in the 0.18–0.28 range; no PLM+mCNN, no RAG, no SHAP applied | **HIGH** — hundreds-to-thousands of windows | **1, 2, 3, 4, 5** |
| **2** | **Lysine glycation sites** | **YES** | **HIGH** — CPLM 200 OK; multiple published independent test sets (200+200; 1,000) | **HIGH** — best published MCC 0.785 (PredGly 2019); **no ProtT5/ESM-2 + mCNN predictor found** | **HIGH** | **1, 2, 3, 4, 5** |
| **3** | **Autophagy proteins, as a leakage-control audit + working web server** | No (whole protein) | **HIGHEST** — PLM-ATG GitHub 200 OK, fixed 100/100 independent test | **LOW on accuracy** (MCC 0.990 already), **MEDIUM as a protocol/validity contribution**; the official web server `cciwyy.top` is **dead** | **HIGHEST** — 950 sequences | 1 (weakly), 4, 5; **not 2, not 3** |
| 4 | Anti-aging peptides | No (short peptides) | MEDIUM — AagingBase 200 OK, code 200 OK, but independent test sets are 40 sequences and differ per paper | **LOW** — independent-test AUC already 0.99; peptides too short for a window contribution | HIGHEST | 1 (weakly), 5 |
| 5 | Aggregation-prone regions | **YES** | MEDIUM — WaltzDB 200 OK but no single canonical independent split found | **LOW** — ≥6 papers in 2025–2026 and **AggrescanAI already uses ProtT5 at residue level** | HIGH | 1 (hard to argue), 2, 4, 5 |
| 6 | LIR / AIM motifs | **YES (motif windows)** | **LOW** — LIRcentral is curated but small; **no established independent test set** | HIGH in principle (no PLM method exists) | MEDIUM — honest baseline is AF2-Multimer, not runnable at scale on free Colab | 1, 2, 3, 4, 5 — but blocked by data |
| 7 | Submitochondrial localization | No | HIGH — SubMitoPred + M983 independent test | **LOW** — Mito-Mixer (2026) is already multi-scale-over-ESM-2; **Ou group already published MCNN_MC (PLM+CNN, mitochondrial carriers, JCIM 2024)** | HIGH | 2, 5; novelty contested |
| 8 | Aging/longevity gene–protein prediction (GenAge) | No | **MEDIUM-LOW** — HAGR fully downloadable (307 human genes verified) but **no train/test split in any archive** | Headroom is huge (ESM2+LoRA: accuracy **0.625**, AUC **0.743**) but that is because **the signal may not be there** | HIGH | 1, 2, 3, 4, 5 on paper — **high risk of an unpublishable null result** |
| — | Senolytic / CR-mimetic small molecules | No (SMILES) | MEDIUM-HIGH — DrugAge verified downloadable (3,424 rows); senolytic predictor data described in-paper | MEDIUM | HIGH | **1, 5 only — no PLM, no mCNN** |
| — | SASP protein prediction | — | **NONE** — no sequence benchmark exists | — | — | **RULE OUT** |
| — | Telomere / telomerase | — | **NONE** — nothing since a 2008 structure+ML study | — | — | **RULE OUT** |
| — | Klotho / mTOR / AMPK / IGF1 pathway proteins | — | **NONE** — collapses into generic function prediction | — | — | **RULE OUT** |
| — | DNA repair proteins | — | LOW as *repair*; the DNA-binding-protein benchmarks (PDB14189/PDB2272/PDB186) are a different task and saturated | LOW | HIGH | **RULE OUT** |
| — | Progeria / laminopathy | — | **NONE found** | — | — | **RULE OUT (low confidence, under-searched)** |
| — | Aging clocks (DNAm / proteomic / transcriptomic) | **No — not sequence tasks at all** | **BLOCKED** — UK Biobank-class cohort data, application + fee + months | — | — | **RULE OUT; explain the input-shape mismatch to the advisor explicitly** |

Supporting numbers for the table, each already cited above: CarbonylDB 1,495 proteins / 3,781 sites and the SCANS splits — [PMC12199415](https://pmc.ncbi.nlm.nih.gov/articles/PMC12199415) `[FULL TEXT]`; PLM-ATG 393/357 train, 100/100 test, 99.5% Acc, MCC 0.990, dead server — [PMC12029579](https://pmc.ncbi.nlm.nih.gov/articles/PMC12029579/) `[FULL TEXT]` + `[LINK-TESTED]`; PredGly MCC 0.785 — [Bioinformatics 35(16):2749](https://academic.oup.com/bioinformatics/article/35/16/2749/5259189) `[SNIPPET]`; Antiaging-FL independent AUC 0.99 on 40 sequences — [PMC12729081](https://pmc.ncbi.nlm.nih.gov/articles/PMC12729081/) `[FULL TEXT]`; AggrescanAI = ProtT5 residue-level — [PubMed 41548690](https://pubmed.ncbi.nlm.nih.gov/41548690) `[SNIPPET]`; Mito-Mixer GCC 0.6945 on M983 — [MDPI a19030212](https://www.mdpi.com/1999-4893/19/3/212) `[SNIPPET]`; MCNN_MC (Ou, JCIM 64(24):9125, 2024) — local Scholar scrape `[FULL TEXT — local file]`; ESM2+LoRA GenAge accuracy 0.625 / AUC 0.743 on a 34+30 test set — [Springer 10.1007/978-3-032-13048-8_26](https://link.springer.com/chapter/10.1007/978-3-032-13048-8_26) `[SNIPPET]`; HAGR archives contain no splits — measured by me `[LINK-TESTED]`.

### Inferences — what I would actually recommend, and what I would say no to

- **Recommend as the week-6 pitch: carbonylation site prediction with a PLM + multi-window CNN, a RAG/retrieval branch, SHAP-based explanation of the window features, and a web server.** Rationale the student can defend in one breath: the input/output shape is identical to the ATP-site work the advisor already published (so the pipeline exists and the risk is low); the data is public with a *published* independent test set (so the gate that killed RTK–ATP is cleared); the published SOTA is attention-based, not mCNN-based, and reports independent-test MCC well under 0.3, so there is real room; and carbonylation is the canonical irreversible oxidative-damage mark, which sits one step away from — not on top of — the advisor's SirtSAGE sirtuin work.
- **Keep glycation as the designated fallback.** Same shape, same reuse, and the gap is cleaner (no modern PLM predictor at all), but the aging framing requires more care because the literature frames glycation as diabetes as often as aging. If the advisor pushes back on "is carbonylation really aging?", glycation is the swap, not a redesign.
- **Rule out the aging-clock family loudly rather than quietly.** It is the single most likely thing for a well-meaning reader to suggest ("aging clocks are the hot topic"), and the reason it fails is not difficulty but **input shape**: a clock eats a measurement vector per person, not an amino-acid sequence, so nothing in the advisor's PLM→mCNN→RAG lineage applies and criteria 2 and 3 cannot be addressed at all.
- **Rule out GenAge/longevity-gene prediction as the core task** despite its being the most obviously "aging" option. The published sequence-only result is accuracy 0.625 / AUC 0.743 on a 64-protein test set, and the only strong result (AUC 0.9322) was obtained with GO and interaction-network features, i.e. by using annotations that already encode the answer. A thesis here risks either a null result or an accidentally circular one. It can still appear in the thesis as a *secondary* analysis ("do our carbonylation-site predictions enrich in GenAge proteins?"), which is cheap and adds an aging-biology story.
- **Rule out senolytic/CR-mimetic small molecules on method-fit, not on quality.** The data is fine and the field is small; it simply is not a protein-sequence problem, so the advisor cannot supervise the method and four of his five criteria go unmet.
- **Rule out mitochondrial protein prediction specifically because of group overlap**, which is the opposite of the usual reason — the data and feasibility are both good, but MCNN_MC (Ou, 2024) and Mito-Mixer (2026) between them already occupy "PLM + multi-scale CNN for a mitochondrial protein class".
- One cross-cutting asset: the leakage-control protocol the student built for RTK–ATP transfers to **every** candidate on this list, and in at least two cases (autophagy at MCC 0.990 on 200 sequences; anti-aging peptides at AUC 0.99 on 40 sequences) the published numbers are suspicious enough that an identity-controlled re-evaluation is a legitimate secondary research question. That lets the student carry forward work already done rather than discarding it.

### Gaps

- **Headroom on carbonylation is inferred from a contradictory source.** If the "MCC 0.712–0.779" reading of SCANS is the correct one for the independent test set, then the headroom I claim for rank 1 shrinks substantially. **This single number should be resolved from the SCANS supplementary material or GitHub before the week-6 pitch.** It is the most decision-relevant unverified fact in these notes.
- I did not test whether the SCANS GitHub repository actually contains the benchmark files (only that the repository page returns 200). Same for PLM-ATG.
- No numbers retrieved for StackAPP (autophagy 2025), the *Nature Communications* 2023 senolytics paper, or the *Aging* 2024 C. elegans lifespan-compound paper.
- Mito-Mixer authorship unresolved (MDPI 403) — matters only if the mitochondrial option is revisited.
- Progeria/laminopathy and chaperone-client prediction were searched shallowly or not at all.
