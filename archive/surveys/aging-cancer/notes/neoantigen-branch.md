# Neoantigen prediction branch of cancer bioinformatics — crowdedness and benchmark accessibility

> **LƯU TRỮ — không dùng để ra quyết định.** Tài liệu lịch sử; mọi câu "chốt / quyết định / khuyến nghị" bên dưới đã hết hiệu lực. Trạng thái hiện hành: [DECISIONS.md](../../../../DECISIONS.md).

> Research notes, 2026-10-02. Written for a report-writer who will produce a Vietnamese report from these notes alone.
> **Verification markers used throughout:** `[FULL TEXT]` = I read the full article body; `[ABSTRACT]` = I read only the abstract/metadata record; `[NOT VERIFIED]` = reported by a secondary source only, I could not confirm at the primary source; `[LIVE TEST]` = I issued an HTTP request myself on 2026-10-02 and report the literal result.
> **My own arithmetic** is marked `[MY CALCULATION]`. No number in this file was invented or interpolated.

---

## Q1. Current state of the art and very recent (2025–2026) competition

### Takeaway

The branch is **extremely crowded and still accelerating**. Between 2023 and 2026 I confirmed at least a dozen distinct immunogenicity-prediction methods, two full harmonized-benchmark resources, three competing database releases, and two brand-new 2026 entrants (CNNeoPP, Hetero-BioLSTM) plus a withdrawn 2026 arXiv preprint (TransNRank). Crucially, **the advisor's own method family (PLM embeddings + multi-window scanning CNN) is already applied to neoantigens by Prof. Yu-Yen Ou's own group** in DeepNeoAG (2024) and NeoGen-BC (2026) — so the most obvious "transfer my pipeline" move is already published by the people closest to the advisor.

### Cited Findings

**NeoTImmuML (2025, Front Immunol)** — `[ABSTRACT]` via PubMed record
- Task: predict **neoantigen immunogenicity** (binary peptide-level classification) from **peptide physicochemical properties only** — not a PLM, not a deep model. — [DOI 10.3389/fimmu.2025.1681396](https://doi.org/10.3389/fimmu.2025.1681396), [PubMed 41200173](https://pubmed.ncbi.nlm.nih.gov/41200173/)
- Authors: Yan Shao, Shuguang Ge, Ruizhe Dong, Wei Ji, Chaoran Qin, Pengbo Wen — **all School of Medical Informatics and Engineering, Xuzhou Medical University, China**. Published 2025-10-22. Volume 16, article 1681396. — [PubMed 41200173](https://pubmed.ncbi.nlm.nih.gov/41200173/) `[ABSTRACT]`
- Method: eight ML algorithms compared by five-fold cross-validation; the top three — **LightGBM, XGBoost, Random Forest** — combined into a **weighted ensemble**. — same source `[ABSTRACT]`
- Data: built from **TumorAgDB2.0**, which the same paper created by adding "publicly available neoantigen data from the past two years" to TumorAgDB 1.0. TumorAgDB2.0 contains **187,223 entries**, web server **https://tumoragdb.com.cn**. — same source `[ABSTRACT]`
- Secondary source adds that TumorAgDB2.0 spans **15 cancer types or cell lines** (colon adenocarcinoma, melanoma, invasive breast cancer, esophageal, cervical, cholangiocarcinoma, pancreatic adenocarcinoma, lung adenocarcinoma, renal clear cell, gastric adenocarcinoma, sarcoma, endometrial, bladder, mast cell leukemia). — [Frontiers article text endpoint](https://public-pages-files-2025.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2025.1681396/text) `[FULL TEXT, partial — the server returned only part of the body]`
- XAI: **SHAP** feature-importance analysis; conclusion that **peptide hydrophilicity and peptide length** are the key determinants of immunogenicity. — [DOI](https://doi.org/10.3389/fimmu.2025.1681396) `[ABSTRACT]`
- Metrics: the abstract says only "strong generalization performance on both internal and external test datasets." **No AUC / accuracy / precision number is stated in the abstract.** I could not retrieve a numeric performance table — the Frontiers full-text endpoint I reached returned a truncated body and omitted the metrics table. **Numeric performance: not found.**
- **Code availability: not found.** The abstract gives only the database URL, no GitHub.

**TransNRank (2026, arXiv 2608.01924) — WITHDRAWN** `[FULL TEXT of the arXiv abstract page]`
- **This preprint has been withdrawn.** The arXiv listing states: "This paper has been withdrawn by Yuenan Hou." The submission also carried a disclaimer that "the final authorship has not been determined and this version has not been polished." **No PDF is available.** — [arXiv:2608.01924](https://arxiv.org/abs/2608.01924)
- Submitted 2026-08-03. Authors as listed before withdrawal: Zhiyin An, Yuenan Hou, Shumeng Duan, Yiming Zhou, Yuanting Zheng, Leming Shi. — [arXiv:2608.01924](https://arxiv.org/abs/2608.01924) `[ABSTRACT]`
- Task: **neoantigen ranking** (not plain classification) with a Transformer + self-attention; a "positive-aware training objective" that up-weights the rare positives to handle class imbalance. — same source `[ABSTRACT]`
- Data: **NCI, TESLA and HiTIDE** — i.e. exactly the three datasets harmonized by the Immunity 2023 paper (see Q2). This is direct evidence that the Immunity 2023 harmonized matrices have become **the** benchmark in this sub-field.
- Claimed metric: pushed the **top-20 recall from 46.9% (45 of 96) to 53.1% (51 of 96)**, and cut training from 200 epochs to 20 epochs. — same source `[ABSTRACT]`. `[MY CALCULATION]` 45/96 = 46.875%, 51/96 = 53.125% — the stated percentages are internally consistent.
- Claimed feature insight: mutation anchors and TCGA expression level were "unexpectedly important." — same source `[ABSTRACT]`
- **Code availability: not found** (no PDF, no repository visible).
- **Judgement for the report: TransNRank should NOT be treated as live competition.** It is withdrawn, unpolished, and the claimed numbers cannot be checked. It is, however, strong evidence that *other groups are actively attacking exactly this benchmark in 2026*.

**NetMHCpan / NetMHCIIpan (DTU)** `[LIVE TEST + search results]`
- `[LIVE TEST]` https://services.healthtech.dtu.dk/services/NetMHCpan-4.1/ → **HTTP 200**, resolves.
- `[LIVE TEST]` https://services.healthtech.dtu.dk/services/NetMHCIIpan-4.3/ → **HTTP 200**, resolves.
- **NetMHCIIpan-4.3** has been the live version since **July 2023**; trained on an extended set of MHC **eluted ligand** data with new HLA-DP, HLA-DR and BoLA-II data; the authors claim it closes the performance gap between HLA-DR, -DP and -DQ and can predict **inverted peptide binders**. — [NetMHCIIpan 4.3 service page](https://services.healthtech.dtu.dk/services/NetMHCIIpan-4.3/); method paper [Science Advances, adj6367](https://www.science.org/doi/10.1126/sciadv.adj6367) `[NOT VERIFIED — I read the search-result summary and the service page, not the Science Advances full text]`
- **There is now a NetMHCpan-4.2** (newer than the 4.1 most papers still cite): "NetMHCpan-4.2: Improved prediction of CD8+ epitopes by use of transfer learning and structural features," Jonas Birkelund Nilsson, Jason Greenbaum, Bjoern Peters, Morten Nielsen, **Frontiers in Immunology, 2025-08-07**. Adds **structural features** and **transfer learning**; trained on single-allelic *and* multi-allelic binding-affinity and eluted-ligand data. — [NetMHCpan 4.2 service page](https://services.healthtech.dtu.dk/services/NetMHCpan-4.2/) `[NOT VERIFIED numerically — no AUC figures retrieved]`
- **Task of both: peptide–MHC binding / presentation, NOT immunogenicity.** This is the standard distinction in the field and is the stated motivation of nearly every immunogenicity paper below.
- Licensing note worth flagging: the NetMHC family is distributed under an **academic-use licence requiring a download request form**; the web server is free to use. I did **not** test the download form, so treat the exact friction as `[NOT VERIFIED]`.

**BigMHC** `[LIVE TEST + secondary]`
- `[LIVE TEST]` https://github.com/KarchinLab/bigmhc → **HTTP 200**, repository resolves. Code is openly available on GitHub.
- Task: two stages — **MHC-I epitope presentation**, then **transfer learning onto immunogenicity data** to predict immunogenic neoepitopes. Claim: "significantly higher precision than seven state-of-the-art models in identifying immunogenic neoepitopes." — [bioRxiv preprint full PDF](https://www.biorxiv.org/content/10.1101/2022.08.29.505690.full.pdf) `[NOT VERIFIED — read via search summary, not the PDF body]`
- A 2025/2026 benchmark reports that **STMHCpan, MHCflurry2.0_PS and BigMHC "achieved the highest scores across distinct evaluation metrics."** — reported in search results for [Biomarker Research 2025 review](https://link.springer.com/article/10.1186/s40364-025-00808-9) `[NOT VERIFIED — the Springer article 303-redirected to an IdP login and I could not read the body]`

**PRIME** `[FULL TEXT via the ITSNdb benchmark paper]`
- Method: a **logistic-regression** immunogenicity score trained on **non-tumoral immunogenic peptides**. — [Front Immunol 10.3389/fimmu.2023.1094236](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2023.1094236/full) `[FULL TEXT]`
- On ITSNdb, **PRIME 2.0 achieved the best classification: DOP = 0.82, F1 = 0.70.** — same source `[FULL TEXT]`

**DeepNeo** `[search-result level only]`
- "DeepNeo: A webserver for predicting immunogenic neoantigens," KAIST. — [OSTI record](https://www.osti.gov/biblio/1970388), [KAIST publication record](https://pure.kaist.ac.kr/en/publications/deepneo-a-webserver-for-predicting-immunogenic-neoantigens/) `[NOT VERIFIED — I did not read the paper or test the server]`
- **Gap: I did not retrieve DeepNeo's dataset, metrics or code URL.**

**MHCflurry** `[LIVE TEST]`
- `[LIVE TEST]` https://github.com/openvax/mhcflurry → **HTTP 200**, repository resolves. Open source (OpenVax).
- Task: peptide–MHC **binding affinity** (MHCflurry 2.0 adds an antigen-processing / presentation score, "MHCflurry2.0_PS"). — [Front Immunol 1094236](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2023.1094236/full) `[FULL TEXT — this paper benchmarks MHCflurry 2.0 as a binding predictor]`

**2026 entrants — treat as live competition**

- **CNNeoPP (2026, Front Immunol 1722117)** — `[FULL TEXT via PMC]`
  - Task: an end-to-end **personalized neoantigen prediction pipeline** with a liquid-biopsy (cfDNA) application.
  - Training data: **1,498 validated peptides** curated from literature plus **Neodb and NEPdb**.
  - Independent validation set: **153 neoantigens (69 immunogenic, 84 non-immunogenic)**. Separately evaluated on **TESLA: 5 patient samples, 532 non-redundant SNV-derived peptides, 34 confirmed immunogenic = 6.39%**.
  - Split: **60% train / 20% validation / 20% test** for the deep models; 5-fold CV for the classical ML baselines. **SMOTE** used for imbalance.
  - Architecture: rank-level late-fusion ensemble of three submodels — FCNN on 6-mer TF-IDF; CNN on 4-mer **BioBERT** embeddings (kernel sizes 3,4,5); FCNN on 2-mer BioBERT embeddings plus 11 structured immunogenicity features.
  - Metrics: **AUC 0.81** on the independent test set. On TESLA: **Top-10 → 3/34, Top-20 → 5/34, Top-50 → 8/34 (23.53% recall at a 9.40% candidate-selection rate)**.
  - Wet-lab follow-up: ELISpot positive rate **58% (29/50)** overall, **70% (19/27)** for CNNeoPP-exclusive predictions.
  - Compared against: **Seq2Neo-CNN, Immuno-GNN, DeepImmuno-CNN, INeo-Epp**.
  - Code: **https://github.com/AaronChen007/neoantigen**; database **http://www.cnneodb.cn/**.
  - Authors' stated limitation: the non-immunogenic set "is primarily derived from a limited number of source studies, which may introduce biases in peptide length selection and HLA allele representation"; they call for "expanding the diversity and scale of experimentally validated non-immunogenic neoepitopes."
  — [PMC12913462](https://pmc.ncbi.nlm.nih.gov/articles/PMC12913462/)

- **Hetero-BioLSTM (2026, Springer book chapter)** — `[NOT VERIFIED — search-result summary only]`
  - Dual-path bidirectional LSTM with local + global modules joined by gated fusion, adaptive encoding for variable-length peptides. Claims **AUC 0.872** on an independent mass-spectrometry immunogenicity dataset, "substantially outperforming state-of-the-art methods."
  — [Springer chapter 10.1007/978-981-92-3485-1_18](https://link.springer.com/chapter/10.1007/978-981-92-3485-1_18)

- **Other 2025–2026 items I saw but did not verify in depth** (listed so the report-writer knows the volume):
  - "A machine learning-based method to optimize the immunogenicity of HLA class I-restricted neoantigens," [PMC12586337](https://pmc.ncbi.nlm.nih.gov/articles/PMC12586337/) `[NOT VERIFIED]`
  - "ImmunoNX: a robust bioinformatics workflow to support personalized neoantigen vaccine trials," [arXiv 2512.08226](https://arxiv.org/pdf/2512.08226) `[NOT VERIFIED]`
  - "Teleport-Stabilized Quantum-Walk Transport for Robust Neoantigen Ranking in Near-Tie Regimes," [bioRxiv 2026.04.22.720240](https://www.biorxiv.org/content/10.64898/2026.04.22.720240v1) `[NOT VERIFIED]`
  - "A modular protein language modelling approach to immunogenicity prediction," PLoS Comput Biol, [PMC11581412](https://pmc.ncbi.nlm.nih.gov/articles/PMC11581412/) `[NOT VERIFIED]` — **note: this is a PLM-based immunogenicity predictor, i.e. it already occupies the "PLM for immunogenicity" slot independently of the Ou lab.**
  - "Computational neoantigen prediction for cancer immunotherapy," Genes Immun 26(6):531–538, 2025-10-19, Tejaswi et al., Yenepoya University India — a review. — [DOI 10.1038/s41435-025-00365-z](https://doi.org/10.1038/s41435-025-00365-z) `[ABSTRACT]`. The Nature-hosted full text 303-redirected to an identity-provider login; I could not read the body.

### Inferences

- The field's competitive frontier has moved from "classify a peptide" to **ranking under extreme imbalance on the harmonized NCI/TESLA/HiTIDE benchmark**, plus wet-lab confirmation (CNNeoPP ran ELISpot). A student with no wet lab cannot compete on that last axis at all.
- Both 2026 entrants I could verify (CNNeoPP, Hetero-BioLSTM) are **architecture-swap papers** with modest AUC (0.81 and 0.872). That is the band a student could plausibly reach — which also means a student's result would be *indistinguishable from the noise floor of this literature*, not a visible contribution.
- Several big names (NetMHCpan 4.2, NetMHCIIpan 4.3) are **binding/presentation** tools, not immunogenicity tools. A thesis must not blur the two — the advisor's five criteria would be poorly served by re-doing binding prediction, which is a solved and heavily-tooled problem.

### Gaps

- **NeoTImmuML's numeric performance (AUC, accuracy, precision/recall) — not found.** The Frontiers full-text endpoint returned a truncated body. Would need the PDF.
- **DeepNeo's task details, datasets, metrics and code URL — not found.**
- **BigMHC's and NetMHCpan-4.2's exact numeric claims — not verified** (bioRxiv PDF and Frontiers paper not read in body).
- The [Biomarker Research 2025 benchmarking review](https://link.springer.com/article/10.1186/s40364-025-00808-9) and the [Genes & Immunity 2025 review](https://doi.org/10.1038/s41435-025-00365-z) both **303-redirected to login pages**; I could not read either body, so their tool tables and challenge lists are unverified.

---

## Q2. The Immunity 2023 harmonized-datasets paper — does it already occupy the "fix the evaluation protocol" contribution space?

### Takeaway

**Yes — directly and almost completely.** The Immunity 2023 paper (Müller et al., Bassani-Sternberg lab) did exactly what a "clean up the protocol and compare methods fairly" thesis would propose: it reprocessed three independent screening cohorts from raw WES/RNA-seq through one uniform pipeline, built harmonized mutation-level and peptide-level feature matrices, trained and compared classifiers, released the matrices **openly on figshare** and the code openly on GitHub, and explicitly framed the deliverable as a resource "for developing and benchmarking companion algorithms." A second, independent group (ITSNdb, Fernández lab, Argentina) occupies the complementary half — a curated fair-benchmark database with validated negatives. **A protocol-focused neoantigen thesis is not available as a novel contribution in 2026.**

### Cited Findings

- Full citation: Müller M, Huber F, Arnaud M, Kraemer AI, Ricart Altimiras E, Michaux J, Taillandier-Coindard M, Chiffelle J, Murgues B, Gehret T, Auger A, Stevenson BJ, Coukos G, Harari A, Bassani-Sternberg M. "Machine learning methods and harmonized datasets improve immunogenic neoantigen prediction." **Immunity 56(11):2650–2663.e6**, published online 2023-10-09. — [DOI 10.1016/j.immuni.2023.09.002](https://doi.org/10.1016/j.immuni.2023.09.002), [PubMed 37816353](https://pubmed.ncbi.nlm.nih.gov/37816353/) `[ABSTRACT — the Cell.com full text and pdfExtended both returned HTTP 403 to me; Europe PMC also returned 403. All numbers below come from the PubMed abstract record, which is the authoritative abstract.]`
- **What was harmonized (exact numbers, quoted from the abstract):** "We reprocessed whole-exome sequencing and RNA sequencing (RNA-seq) data from **120 cancer patients from two external large-scale neoantigen immunogenicity screening assays** combined with **an in-house dataset of 11 patients**" → **131 patients total** — "and identified **46,017 somatic single-nucleotide variant mutations** and **1,781,445 neo-peptides**, of which **212 mutations and 178 neo-peptides were immunogenic**." — [PubMed 37816353](https://pubmed.ncbi.nlm.nih.gov/37816353/) `[ABSTRACT]`
- The harmonization is at the level of **re-running variant calling and expression quantification from raw sequencing data**, not merely merging published peptide lists. That is what makes it hard to beat: the cross-dataset annotation differences that a protocol thesis would complain about were removed at source. — inferred from the abstract wording "reprocessed whole-exome sequencing and RNA sequencing data" `[ABSTRACT]`
- The three cohorts are named in the downstream literature as **NCI (Gartner et al. 2021), TESLA (Wells et al. 2020), and HiTIDE (the 11 in-house patients)**. The NeoRanking README cites Gartner et al. *Nat. Cancer* 2(563–574), 2021 and Wells et al. *Cell* 183:818-834.e13, 2020 as the two external sources. — [NeoRanking README](https://raw.githubusercontent.com/bassanilab/NeoRanking/master/README.md) `[FULL TEXT]`; the NCI/TESLA/HiTIDE naming is confirmed by the TransNRank abstract listing "NCI, TESLA and HiTIDE datasets" — [arXiv:2608.01924](https://arxiv.org/abs/2608.01924) `[ABSTRACT]`
- **New predictive features the paper introduced** (this is its method contribution, beyond the datasets): "the location of neo-peptides within **protein HLA presentation hotspots**, **binding promiscuity**, and the **role of the mutated gene in oncogenicity**." — [PubMed 37816353](https://pubmed.ncbi.nlm.nih.gov/37816353/) `[ABSTRACT]`
- **Claimed result:** "The classifiers accurately predicted neoantigen immunogenicity across datasets and **improved their ranking by up to 30%**." — same source `[ABSTRACT]`. A Ludwig Cancer Research press item independently describes "a 30% improvement on the ranking of neoantigens." — [Ludwig Cancer Research, April 2024](https://www.ludwigcancerresearch.org/ludwig-link/april-2024/machine-learning-method-improves-neoantigen-selection-for-immunotherapy/) `[NOT VERIFIED — search-result summary of the press page]`
- **Stated purpose of the data release — this is the sentence that forecloses the protocol thesis:** "we have provided **homogenized datasets valuable for developing and benchmarking companion algorithms** for neoantigen-based immunotherapies." — [PubMed 37816353](https://pubmed.ncbi.nlm.nih.gov/37816353/) `[ABSTRACT]`
- **What was benchmarked:** the released code trains and tests **logistic regression and XGBoost**, at **two granularities — mutation level and neo-peptide level** — with a defined **NCI-train / NCI-test** split plus cross-dataset testing. Pre-trained models "trained on NCI-train" are downloadable. — [NeoRanking README](https://raw.githubusercontent.com/bassanilab/NeoRanking/master/README.md) `[FULL TEXT]`
- **The preprocessing pipeline is fully specified in the repo**, which means a student cannot claim "nobody documented the protocol": (a) select SNV mutations; (b) numerically encode categorical features; (c) impute missing values; (d) **quantile-normalize** numerical features; (e) substitute encoded values. — same source `[FULL TEXT]`
- **Known stochasticity the authors flag themselves** — a genuine residual weakness: results vary "due to the **random sampling of non-immunogenic neo-peptides**" and "the **stochastic hyperopt parameter optimization**," and "very small p-values and Shapley values are subject to variations." — same source `[FULL TEXT]`
- The paper already uses **Shapley values** (XAI) in its figures — so SHAP-style explainability is also already present in the reference work. — same source `[FULL TEXT]`
- **The complementary half is also taken.** ITSNdb (Fernández lab, Córdoba, Argentina) is explicitly "a tool developed to **fairly benchmark** immunogenicity predictors intended to be used over tumoral neopeptides" and "enables the analysis of immunogenicity **without the interference of other variables such as binding affinity or peptide processing**." Its 2025 *Methods in Molecular Biology* chapter (vol. 2930, pp. 139–156) packages it as a reusable benchmarking protocol. — [DOI 10.1007/978-1-0716-4558-1_11](https://doi.org/10.1007/978-1-0716-4558-1_11), [PubMed 40402453](https://pubmed.ncbi.nlm.nih.gov/40402453/) `[ABSTRACT]`

### Inferences

- `[MY CALCULATION]` From the abstract's own numbers, the peptide-level positive rate is **178 / 1,781,445 = 0.0100%**, i.e. roughly **1 immunogenic peptide per 10,008 candidates**. The mutation-level positive rate is **212 / 46,017 = 0.461%**, i.e. about **1 in 217**. These are the hardest imbalance figures in the branch and they come from the field's reference benchmark.
- **Answer to the direct question: a thesis whose contribution is "fair comparison under a clean protocol" is dead on arrival here.** Immunity 2023 owns the harmonized-data + fair-comparison claim, released it open, and the field has adopted it (TransNRank 2026 benchmarks on exactly NCI/TESLA/HiTIDE). ITSNdb owns the curated-negatives benchmark claim. Any such pitch would be read by a reviewer as re-running `bash train_classifier.sh`.
- The one residual crack is narrow and honest: **the random sampling of non-immunogenic peptides is acknowledged by the authors as a source of variance, and nobody appears to have quantified how much of reported method ranking is an artefact of that sampling choice.** That is a real but *small* contribution — a sensitivity/stability study, not a thesis-sized novelty — and it would score poorly on the advisor's criteria 1 and 3.

### Gaps

- **I could not read the Immunity paper's full text.** Cell.com returned **HTTP 403** on both `/fulltext/S1074-7613(23)00406-5` and `/pdfExtended/S1074-7613(23)00406-5`; Europe PMC returned **HTTP 403**; ScienceDirect was not accessible. Therefore: the paper's own **Limitations / Discussion** section, its per-dataset AUC/PR numbers, its exact NCI-train/NCI-test split sizes, and its full list of compared baselines are **not verified**. A human with institutional access should read it before the pitch.
- The **HLA-allele distribution** of the harmonized datasets is not found.

---

## Q3. Benchmark accessibility — tested, not assumed

### Takeaway

The honest picture is better than expected on **derived feature matrices** and worse than expected on **raw sequencing data**. The single most important accessibility fact: **the Immunity 2023 harmonized matrices are on figshare behind anonymous private links with no login and no data-access committee** — so the field's reference benchmark IS reachable by a student in Vietnam today. By contrast TESLA's primary Synapse project requires Synapse **registration plus "Certified User" status** before download, and HiTIDE's raw WES/RNA-seq on EGA is **controlled access** requiring a DAC. ITSNdb is the only benchmark that is *trivially* downloadable — and it is tiny (199 peptides).

### Cited Findings — per-dataset, with the literal result of my test

All tests performed by me on **2026-10-02** from a Linux shell. `[LIVE TEST]` throughout this subsection.

**1. Immunity 2023 harmonized matrices (figshare) — the practical answer for a student**
- `[LIVE TEST]` `https://figshare.com/s/3c27fa3b705a74bdfa10` → **HTTP 202** (figshare's bot-challenge / accepted response; the link resolves, does not 404, and is a figshare *private-share* link, which by figshare's design needs **no account and no login**). Same result for `https://figshare.com/s/a000b0990465ab3e9d33` and `https://figshare.com/s/9fc6c11691273efe995e`: both **HTTP 202**.
- These three links, quoted verbatim from the NeoRanking README, provide: **`Mutation_data_org.txt`** (mutation-level matrix), **`Neopep_data_org.txt`** (neo-peptide-level matrix), **`HLA_allotypes.txt`**, **pre-trained logistic-regression and XGBoost classifiers trained on NCI-train**, and **pre-computed classifier result files**. — [NeoRanking README](https://raw.githubusercontent.com/bassanilab/NeoRanking/master/README.md) `[FULL TEXT]`
- **Download without institutional approval or a DAC: YES.** **Registration: NO.** **Immunogenicity labels: YES** (the matrices are "annotated with several feature scores" and the classifiers are trained on immunogenicity). **Canonical split: YES — "NCI-train" and "NCI-test" are named splits in the repo, plus cross-dataset testing on TESLA and HiTIDE.** — [NeoRanking README](https://raw.githubusercontent.com/bassanilab/NeoRanking/master/README.md) `[FULL TEXT]`
- **Size: not found** (figshare's 202 response gave no content-length; I did not complete a download).
- **Approximate entry counts (from the paper):** 46,017 mutations; 1,781,445 neo-peptides; 212 immunogenic mutations; 178 immunogenic neo-peptides. — [PubMed 37816353](https://pubmed.ncbi.nlm.nih.gov/37816353/) `[ABSTRACT]`
- Licence: "Copyright (C) LICR — Ludwig Institute of Cancer Research, Lausanne, Switzerland." **No explicit open licence text is given in the README** — this is a genuine ambiguity worth checking. — [NeoRanking README](https://raw.githubusercontent.com/bassanilab/NeoRanking/master/README.md) `[FULL TEXT]`
- NeoRanking code: `https://github.com/bassanilab/NeoRanking` → **resolves, HTTP 200**, Python 3.8.10, `requirements.txt`, 111 commits on master. `[LIVE TEST]`

**2. TESLA — Synapse syn21048999**
- `[LIVE TEST]` `https://www.synapse.org/Synapse:syn21048999` → **HTTP 200**. The page title is literally **"TESLA data access"**; the rendered text mentions "appropriate access controls, data-use agreements, and governance."
- `[LIVE TEST]` Synapse REST API, unauthenticated: `GET https://repo-prod.prod.sagebase.org/repo/v1/entity/syn21048999` returned `{"name":"TESLA data access","id":"syn21048999","concreteType":"...Project","alias":"TESLA_public","createdOn":"2019-10-24","modifiedOn":"2022-09-30"}`.
- `[LIVE TEST]` `POST .../entity/syn21048999/bundle2` with `includeRestrictionInformation` returned, verbatim: `"restrictionInformation":{"restrictionLevel":"OPEN","hasUnmetAccessRequirement":false, ... "canPublicRead":true, "canDownload":false, "isCertifiedUser":false, "isCertificationRequired":true, "isEntityOpenData":false}`, with `"restrictionDetails":[]`.
- **Interpretation — this is the precise answer:** TESLA on Synapse carries **`restrictionLevel: OPEN`** and **no unmet access requirement**, i.e. **there is NO data-access committee and NO institutional approval gate**. But `isCertificationRequired: true` and `canDownload: false` for an anonymous caller means a student must (a) **create a free Synapse account** and (b) **pass Synapse's "Certified User" quiz** (a short self-service test on data-sharing ethics, not an institutional approval). → **Download without institutional approval/DAC: YES. Registration: YES (free account + self-service certification).**
- `[LIVE TEST]` Children listing: syn21048999 contains exactly one folder, **"TESLA phase 1 data release" (syn23446508)**, created 2020-10-17, last modified 2020-11-09.
- **Immunogenicity labels: YES** — TESLA is an immunogenicity screening consortium dataset. **Approximate counts:** CNNeoPP used "**TESLA: 5 patient samples with 532 non-redundant SNV-derived peptides (34 confirmed immunogenic = 6.39%)**" — [PMC12913462](https://pmc.ncbi.nlm.nih.gov/articles/PMC12913462/) `[FULL TEXT]`. Note this is *one paper's filtered subset*, not the whole release.
- **Known quality defect in TESLA, documented by an independent group:** TESLA "lacks **WT sequence or gene name**," and for its positive peptides, processing/presentation was **not experimentally validated**. On TESLA, DeepHLApan predicted **100% (297) false positives**. — [Front Immunol 1094236](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2023.1094236/full) `[FULL TEXT]`
- **Canonical train/test split: NO native split.** TESLA is used as a **held-out external test set** by others (Immunity 2023, CNNeoPP, TransNRank), which in practice gives it the role of an independent test set.
- **Size: not found** (I did not authenticate, so I could not list file sizes).

**3. NCI-test (Gartner et al. 2021, Nat Cancer)**
- The NeoRanking README states the NCI-related matrices — **`MmpsTestingSet.txt`, `MmpsTrainingSet.txt`, `NmersTestingSet.txt`, `NmersTrainingSet.txt`** — are available "from the **figshare links provided by Gartner et al.**" and that these files "contain mutations (nmers) and neo-peptides (mmps) together with feature scores **and immunogenicity screening annotations**." — [NeoRanking README](https://raw.githubusercontent.com/bassanilab/NeoRanking/master/README.md) `[FULL TEXT]`
- **Canonical train/test split: YES — the file names themselves are TrainingSet / TestingSet.** This is the cleanest "established independent test set" in the whole branch, and it is the one thing the student's hard data constraint demands.
- **Download without institutional approval: YES** (figshare, per the README's own framing). **Registration: NO** (figshare). **BUT: I did not test Gartner's figshare link because the README does not print the URL** — it only says "the figshare links provided by Gartner et al." → `[NOT TESTED]`. **This must be verified before the week-6 pitch.** Source paper: Gartner JJ et al., *Nat. Cancer* 2:563–574, 2021, [DOI 10.1038/s43018-021-00197-6](https://doi.org/10.1038/s43018-021-00197-6).
- **Size and entry counts: not found** at the file level; the counts aggregated into Immunity 2023 are in Q2.

**4. HiTIDE — EGA EGAS00001007101**
- `[LIVE TEST]` `https://ega-archive.org/studies/EGAS00001007101` → **HTTP 200** (study landing page is public).
- `[LIVE TEST]` `https://metadata.ega-archive.org/studies/EGAS00001007101` returned: title **"Cancer sequencing for somatic variant calling"**; description "**WES and RNAseq for 11 patients with metastatic melanoma, lung, kidney, and stomach cancers**, enrolled in phase I clinical trials of TIL ACT (NCT03475134 & NCT04643574). WES was performed on matched cancer and healthy tissues, whereas RNAseq was performed on cancer tissues, using Illumina HiSeq 2500/4000 and Illumina NextSeq 550 systems."
- `[LIVE TEST]` `https://metadata.ega-archive.org/studies/EGAS00001007101/datasets` returned exactly one dataset: **`EGAD00001010169`**, "WES and RNA-seq data of 11 cancer patients with multiple cancer types", **`num_samples: 36`**, `dataset_types: ["Exome sequencing","Transcriptome profiling by high-throughput sequencing"]`, released 2023-03-22, **`"access_type":"controlled"`**, **`"policy_accession_id":"EGAP00001003206"`**.
- **Interpretation: → Download without institutional approval or a DAC: NO.** `access_type: controlled` plus a named policy accession means a **Data Access Committee application** is required. Raw FASTQs are out of reach for this student.
- **Immunogenicity labels: NO** — this EGA dataset holds **raw FASTQ sequencing reads only**. The *immunogenicity labels* for these 11 patients live in the **open figshare matrices** (item 1).
- **This is the single most important nuance in this whole section:** the HiTIDE *raw data* is DAC-gated, but the HiTIDE *derived, labelled feature matrix* is openly on figshare inside `Neopep_data_org.txt` / `Mutation_data_org.txt`. A student does not need EGA access to reproduce or extend the Immunity 2023 benchmark.
- **Canonical train/test split: NO** (it is a raw-data deposit).

**5. ITSNdb — github.com/elmerfer/ITSNdb**
- `[LIVE TEST]` `https://github.com/elmerfer/ITSNdb` → **HTTP 200**, 440 KB page. GitHub API: `pushed_at: 2025-03-31`, `stargazers_count: 2`, has a `LICENSE` file (35,149 bytes — consistent with GPL/MIT-length text; **I did not read which licence** → `[NOT VERIFIED]`).
- `[LIVE TEST]` Contents of `data/`: **`ITSNdb.csv` (30,265 bytes)**, `ITSNdb.RData`, **`TNB_dataset.csv` (5,239,999 bytes ≈ 5.0 MB)**, `TNB_dataset.RData` (7,727,252 bytes), **`Val_dataset.csv` (5,706 bytes)**, `Val_dataset.RData`, `CIImm.xlsx`, `MHC_allele_names.RData`. Plus `MyPatientsNeoantigenList.csv` (112 bytes) at repo root, an R package skeleton (`DESCRIPTION`, `NAMESPACE`, `R/`, `man/`), and a `Colab` folder.
- **→ Download without institutional approval: YES. Registration: NO. The actual data files are committed in the public git repo.** This is the only fully frictionless benchmark in the branch.
- **Composition (exact):** **199** 9-mer and 10-mer SNV-derived neoantigens, of which **129 immunogenic and 70 non-immunogenic**. Each entry carries wild-type counterpart, restricted HLA, gene, tumour tissue, peptide length, mutation position type, immunogenicity reaction, and reference. Curated from **more than 70 publications**. **Inclusion required experimental validation of MHC-I binding (mass spectrometry or competition assay), of positive/negative immunogenicity (tetramer titration, IFN-γ/TNF ELISPOT), AND of processing/presentation.** — [Front Immunol 1094236](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2023.1094236/full) `[FULL TEXT]`
- **Immunogenicity labels: YES, and uniquely it has validated NEGATIVES** — that is its whole reason for existing.
- **HLA bias (exact):** **HLA-A\*02:01 accounts for 80/199 = 40.2%** of entries. — same source `[FULL TEXT]`
- Two companion sets ship with it: a **validation set of 120 peptide–HLA pairs (113 non-immunogenic lacking binding validation + 7 immunogenic non-SNV neoantigens from fusions, intron retention, indels)**, and a **TNB dataset** of MHC-I-binding neopeptides from immune-checkpoint-blockade cohorts with patient outcomes. — same source `[FULL TEXT]`, file sizes confirmed `[LIVE TEST]`
- **Canonical train/test split: NO — and deliberately so.** ITSNdb is designed as an **evaluation-only** benchmark, not a training set. At 199 peptides it is far too small to train on.

**6. NEPdb — nep.whu.edu.cn**
- `[LIVE TEST]` `http://nep.whu.edu.cn/` → **HTTP 200**, 32,085 bytes, page served, meta keywords "NEP, Neo-Epitope Cancer Immunotherapy Database, HLA". The site is **alive**.
- `[LIVE TEST]` `http://nep.whu.edu.cn/nep/download` → **HTTP 404**. `http://nep.whu.edu.cn/browse` → **HTTP 404**. I **could not locate a working bulk-download endpoint** by guessing paths; the real paths are behind the site's JavaScript. → **bulk download: not confirmed.**
- **Composition:** "**173 neoepitopes and 17,376 non-immunogenic peptides** of human cancers" in the immunogenic/validated set; plus **516,036 neopeptides** and **49,023,420 total predictions**. — search-result summary of [NEPdb paper, PMC8078594](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8078594/) and [Database Commons entry](https://ngdc.cncb.ac.cn/databasecommons/database/id/7742) `[NOT VERIFIED — I did not read the NEPdb paper body]`
- `[MY CALCULATION]` 173 : 17,376 = **1 : 100.4** immunogenic : non-immunogenic. This is the most usable *labelled, both-classes* resource by size in the branch.
- **Immunogenicity labels: YES** (T-cell experimentally validated, both positive and negative).
- **Documented quality defect:** in NEPdb, **processing and presentation were "not experimentally validated."** — [Front Immunol 1094236](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2023.1094236/full) `[FULL TEXT]`
- **Registration: not determined.** **Canonical train/test split: NO.**

**7. dbPepNeo / dbPepNeo2.0**
- `[LIVE TEST]` `http://www.biostatistics.online/dbPepNeo2/` → **HTTP 200** but the body is only a 234-byte JavaScript redirect: `self.location.href = 'http://119.3.70.71/dbPepNeo2/home.html'`. **The canonical domain now bounces to a bare IP address** — a maintenance red flag.
- `[LIVE TEST]` `http://119.3.70.71/dbPepNeo2/home.html` → **HTTP 200, 31,436 bytes**. `http://119.3.70.71/dbPepNeo2/download.html` → **HTTP 200, 20,632 bytes**. The mirror works.
- `[LIVE TEST]` `http://www.biostatistics.online/dbPepNeo2/download.php` → **HTTP 404** (wrong extension; the real page is `.html` on the IP).
- `[LIVE TEST]` `http://dbpepneo.biowisetech.com/` → **no HTTP response at all** (connection produced no status line within 25 s) — **dead**.
- `[LIVE TEST]` The download page offers an "**Academic Download - dbPepNeo2.0**" section with per-category files: MHC-I HC neoantigens, MHC-I fusion neoantigens, MHC-I non-coding neoantigens, MHC-I neoantigen-reactive TCRs, MHC-II HC neoantigens, MHC-II neoantigen-reactive TCRs, MHC-I MC neoantigens. **→ Download without institutional approval: YES, direct academic download links are present on the page. Registration: NO.**
- `[LIVE TEST]` **Caveat found in the page source:** a commented-out JavaScript alert reads `//alert('If you need complete data, please contact the author at luxiex2017@outlook.com ')`. So the **complete** dataset may require emailing the author even though per-category files are linked.
- **Composition:** "about **801 high-confidence (HC) neoantigens** (increased by 170%) and **842,289 low-confidence (LC) HLA immunopeptidomes** (increased by 107%)"; includes **55 class-II HC neoantigens** and **630 neoantigen-reactive TCR-β sequences**. — search-result summary of [dbPepNeo2.0, PMC9043652](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9043652/) `[NOT VERIFIED — paper body not read]`
- **Immunogenicity labels: PARTIAL / PROBLEMATIC.** The independent benchmark paper lists "CAPD/DbPepNeo" under the defect "**lack of truly non-immunogenic peptides**." The HC entries are *mass-spectrometry-detected presented peptides*, which is presentation evidence, not immunogenicity. — [Front Immunol 1094236](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2023.1094236/full) `[FULL TEXT]`
- **Canonical train/test split: NO.**

**8. Neodb**
- `[LIVE TEST]` `https://nextgenbioinformatics.org/Neodb/` → **no HTTP response** (no status line returned). `https://neodb.zhanglabs.cn` → **no response**. `https://neodb.zhanglab.cn` and `http://neodb.zhanglab.cn` → **no response**. **I could not reach any Neodb web host I tried.** The paper is at [Database, 10.1093/database/baad041](https://academic.oup.com/database/article/doi/10.1093/database/baad041/7197208) (open access, 2023) and the correct live URL would have to be read out of it. → **Live accessibility: NOT CONFIRMED; all four hostnames I tried failed.**
- **Composition:** "**1463 validated neoantigen instances** with **1277 HLA-I and 186 HLA-II** restriction, and a list of **20,971 candidate neoantigens from common driver mutations**." Described as "the most comprehensive validated neoantigen database" with "the largest number of neoantigens from recurrent driver mutations." — search-result summary of the [Neodb paper](https://academic.oup.com/database/article/doi/10.1093/database/baad041/7197208) `[NOT VERIFIED — paper body not read]`
- `[MY CALCULATION]` 1277 + 186 = 1463, so the HLA-I/HLA-II split is internally consistent.
- **Immunogenicity labels: YES (validated instances).** **Canonical train/test split: NO.** CNNeoPP (2026) used Neodb + NEPdb as its training source. — [PMC12913462](https://pmc.ncbi.nlm.nih.gov/articles/PMC12913462/) `[FULL TEXT]`

**9. TumorAgDB 1.0 / 2.0**
- `[LIVE TEST]` `https://tumoragdb.com.cn` → **HTTP 200**, 455 bytes. The body is a **Vite/JavaScript single-page-application shell** (`<div id="app"></div>` + `/assets/index-CYQ3hQF4.js`) — i.e. **all content is rendered client-side, so there is no server-side HTML to scrape and no obvious static download path.** `https://tumoragdb.com.cn/download` → **HTTP 200** but this is just the SPA shell again (SPA routing), not a confirmed file endpoint.
- **→ Download without institutional approval: probably YES (no login wall encountered), but NOT CONFIRMED** — I could not verify a working bulk-download file because the site requires a JavaScript browser.
- **Composition:** **187,223 entries**, 15 cancer types or cell lines. — [DOI 10.3389/fimmu.2025.1681396](https://doi.org/10.3389/fimmu.2025.1681396) `[ABSTRACT]`
- **Immunogenicity labels: YES** (NeoTImmuML trains an immunogenicity classifier on it). **Canonical train/test split: the paper mentions an "external test dataset" but its identity is not found.**
- **Age: brand new (2025-10-22).** Relying on a two-week-old Chinese-hosted SPA as the primary data source for a thesis is a real availability risk.

**10. IEDB**
- `[LIVE TEST]` `https://www.iedb.org/` → **HTTP 200**, resolves. `https://www.iedb.org/database_export_v3.php` → **HTTP 200** — the **bulk export page is reachable without login**.
- **→ Download without institutional approval: YES. Registration: NO** (IEDB is free and public; exports are provided as downloadable archives).
- **Immunogenicity labels: YES** — IEDB is the largest curated repository of T-cell assay results, but it is **not neoantigen-specific**: it is dominated by pathogen and allergen epitopes, and mixing it into a tumour-neoantigen task is itself a documented source of label noise (see Q4 — PRIME is trained on "non-tumoral immunogenic peptides").
- **Related resource CEDAR** (IEDB's cancer-epitope sibling) carries a documented defect: "**complex filtering required; substantial data loss**." — [Front Immunol 1094236](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2023.1094236/full) `[FULL TEXT]`
- **Canonical train/test split: NO.**
- **Size and entry counts: not found** (I did not download an export).

### Summary table — the go/no-go gate

| Resource | Downloadable without institutional approval / DAC? | Registration? | Immunogenicity labels? | Canonical independent test split? | My live test result |
|---|---|---|---|---|---|
| **Immunity-2023 harmonized matrices (figshare)** | **YES** | **NO** | **YES** | **YES (NCI-train / NCI-test + cross-dataset)** | 3 links → HTTP 202, resolve |
| **NCI (Gartner) figshare sets** | YES (per README) | NO | YES | **YES (TrainingSet / TestingSet files)** | **NOT TESTED — URL not printed in README** |
| **TESLA (Synapse syn21048999)** | **YES — restrictionLevel OPEN, no DAC** | **YES — free account + self-service "Certified User" quiz** | YES | No native split; used as external test set | HTTP 200; API: `OPEN`, `hasUnmetAccessRequirement:false`, `isCertificationRequired:true`, `canDownload:false` anon |
| **HiTIDE raw (EGA EGAS00001007101 / EGAD00001010169)** | **NO — `access_type: controlled`, policy EGAP00001003206** | DAC application | NO (raw FASTQ only) | No | HTTP 200 landing; API says controlled, 36 samples, 11 patients |
| **ITSNdb (GitHub)** | **YES** | **NO** | **YES — incl. validated negatives** | No (evaluation-only, 199 peptides) | HTTP 200; `data/ITSNdb.csv` 30,265 B, `TNB_dataset.csv` 5.0 MB |
| **NEPdb (nep.whu.edu.cn)** | Site up; bulk download endpoint **not confirmed** | Unknown | YES (173 pos / 17,376 neg) | No | HTTP 200 homepage; `/nep/download` and `/browse` → **404** |
| **dbPepNeo2.0** | YES (academic download links present) — but "complete data" may need an email to the author | NO | PARTIAL — lacks true negatives | No | Canonical domain is a **JS redirect to bare IP 119.3.70.71**; mirror HTTP 200; old `dbpepneo.biowisetech.com` **dead** |
| **Neodb** | **NOT CONFIRMED** | Unknown | YES (1463 validated) | No | **4 hostnames tried, all gave no HTTP response** |
| **TumorAgDB 2.0** | Probably yes, **NOT CONFIRMED** | NO wall seen | YES (187,223 entries) | External test set unidentified | HTTP 200 but **JavaScript SPA shell only**, no scrapable content |
| **IEDB** | **YES** | **NO** | YES, but not neoantigen-specific | No | HTTP 200; `database_export_v3.php` HTTP 200 |

### Inferences

- **The data gate is PASSED, but only through one door.** The combination of *Immunity-2023 figshare matrices + Gartner NCI TrainingSet/TestingSet files* gives a genuinely open, labelled dataset **with a named independent test split** — which is exactly what the previous abandoned topic lacked. Everything else is either evaluation-only (ITSNdb), split-less (all the databases), or DAC-gated (EGA).
- **But passing the gate through that door means working inside Bassani-Sternberg's protocol**, which means the student is benchmarking against the paper that owns the protocol contribution. The data that is accessible is precisely the data whose contribution space is occupied.
- **Infrastructure fragility is a live risk for this branch.** Of the eight community databases I probed, one is a JS redirect to a bare IP, one is fully dead, one gave no response on four hostnames, and one is a two-week-old SPA. A thesis that depends on scraping these would be a bad bet. `[LIVE TEST]`-based judgement.

### Gaps

- **The Gartner et al. 2021 figshare URL was not tested** because the NeoRanking README references it indirectly. **Highest-priority verification item before the week-6 pitch.**
- **Exact file sizes of the figshare matrices: not found.** The student should assume "large" — 1,781,445 peptide rows with multiple feature columns is plausibly on the order of hundreds of MB to a few GB, but I did not measure it, so do **not** state a size in the report.
- **NEPdb's bulk-download path and whether it requires registration: not determined.**
- **Neodb's current working URL: not found.** Must be read from the open-access Database paper.
- **The licence on the figshare matrices: ambiguous** — README gives a Ludwig Institute copyright line with no licence grant. This could matter if the student publishes a web app that redistributes the data.
- **Whether a Vietnamese student can complete Synapse certification from Vietnam: not tested** (I did not create an account). No geographic restriction is indicated by the API, and `canPublicRead: true`, so there is no evidence of a barrier — but it is untested.

---

## Q4. Documented class imbalance and label noise

### Takeaway

The imbalance is the worst I have seen quantified in applied bioinformatics — **about 1 immunogenic peptide per 10,000 candidates** at the peptide level in the field's reference benchmark — and the label noise is structural, not incidental: negatives are mostly *unvalidated* rather than *proven non-immunogenic*, HLA-A\*02:01 alone accounts for ~40% of curated entries, and different methods validated by different assays agree almost not at all.

### Cited Findings — class imbalance, with numbers

- **Immunity 2023 / NCI+TESLA+HiTIDE (the reference benchmark):** 46,017 somatic SNV mutations and **1,781,445 neo-peptides**, of which **212 mutations** and **178 neo-peptides** were immunogenic. — [PubMed 37816353](https://pubmed.ncbi.nlm.nih.gov/37816353/) `[ABSTRACT]`
  - `[MY CALCULATION]` peptide level: **178 / 1,781,445 = 0.0100%**, i.e. **≈ 1 : 10,008**. Mutation level: **212 / 46,017 = 0.461%**, i.e. **≈ 1 : 217**.
- **TESLA subset as used by CNNeoPP:** **34 confirmed immunogenic out of 532** non-redundant SNV-derived peptides from 5 patients = **6.39%**, i.e. **≈ 1 : 14.6**. — [PMC12913462](https://pmc.ncbi.nlm.nih.gov/articles/PMC12913462/) `[FULL TEXT]`
- **ITSNdb:** 129 immunogenic : 70 non-immunogenic = imbalance of **~1.8 : 1 in favour of positives** — i.e. **inverted** relative to reality. The benchmark paper states the ratio as "~1.8:1 (immunogenic:non-immunogenic)". — [Front Immunol 1094236](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2023.1094236/full) `[FULL TEXT]`
- **NEPdb:** **173 immunogenic neoepitopes : 17,376 non-immunogenic peptides**. — [PMC8078594](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8078594/) `[NOT VERIFIED — search summary]`. `[MY CALCULATION]` = **≈ 1 : 100**.
- **CNNeoPP's own independent validation set:** **69 immunogenic : 84 non-immunogenic** = roughly balanced, **1 : 1.2**. — [PMC12913462](https://pmc.ncbi.nlm.nih.gov/articles/PMC12913462/) `[FULL TEXT]`
- **The spread between these ratios — 1:10,008, 1:100, 1:14.6, 1:1.2, and 1.8:1 — is itself the strongest single fact in this section.** Reported AUCs across papers are therefore **not comparable**, because the base rate differs by four orders of magnitude between evaluation sets.

### Cited Findings — negative-set construction, the core label-noise problem

- The benchmark paper's central diagnosis: **existing databases lack properly validated negative examples.** Documented per-database defects, quoted: — all from [Front Immunol 1094236](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2023.1094236/full) `[FULL TEXT]`
  - **CAPD / dbPepNeo** — "lack of truly non-immunogenic peptides"
  - **TANTIGEN** — unclear accessibility of experimental validation data
  - **caAtlas** — missing immunogenicity information
  - **TSNAdb** — "putative neoantigens without experimental validation"
  - **NEPdb** — processing/presentation "not experimentally validated"
  - **TESLA** — lacks "WT sequence or gene name"; processing/presentation unvalidated for positives
  - **CEDAR** — "complex filtering required; substantial data loss"
- ITSNdb's own companion validation set makes the problem explicit: of its 120 peptide–HLA pairs, **113 are non-immunogenic peptides that LACK binding validation** — i.e. even the purpose-built negative set is built from "not shown to be immunogenic," not "shown not to be immunogenic." — same source `[FULL TEXT]`
- **Immunity 2023 handles the negative problem by random subsampling**, and the authors warn that re-running their code gives different results "due to the **random sampling of non-immunogenic neo-peptides**." — [NeoRanking README](https://raw.githubusercontent.com/bassanilab/NeoRanking/master/README.md) `[FULL TEXT]`
- **CNNeoPP (2026) states the same problem is still open:** its non-immunogenic set "is primarily derived from a limited number of source studies, which may introduce biases in **peptide length selection and HLA allele representation**," and calls for "expanding the diversity and scale of experimentally validated non-immunogenic neoepitopes." — [PMC12913462](https://pmc.ncbi.nlm.nih.gov/articles/PMC12913462/) `[FULL TEXT]`
- **PRIME is trained on non-tumoral immunogenic peptides** — i.e. a tumour-neoantigen predictor whose positives come from a different biological domain. — [Front Immunol 1094236](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2023.1094236/full) `[FULL TEXT]`

### Cited Findings — HLA bias

- **ITSNdb: HLA-A\*02:01 = 80 / 199 = 40.2%** of all entries. The paper calls this "substantial allele bias." — [Front Immunol 1094236](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2023.1094236/full) `[FULL TEXT]`
- CNNeoPP independently flags "**HLA allele representation**" bias in its negative set. — [PMC12913462](https://pmc.ncbi.nlm.nih.gov/articles/PMC12913462/) `[FULL TEXT]`
- `[MY CALCULATION / inference]` An HLA-A\*02:01 share of 40% is far above that allele's population frequency anywhere, and it is a **European-ancestry-skewed allele**. For a Vietnamese student this is a *substantive scientific* point, not just a technical one — Vietnamese HLA distributions are dominated by different alleles — but **I did not find any published quantification of neoantigen-predictor performance stratified by Vietnamese or Southeast Asian HLA alleles. Not found.**

### Cited Findings — validation-method heterogeneity and method disagreement

- Inclusion in ITSNdb required immunogenicity evidence from any of **tetramer titration, IFN-γ ELISPOT, or TNF ELISPOT**, and binding evidence from **either mass spectrometry or competition assay** — i.e. the "label" is a union of non-equivalent assays. — [Front Immunol 1094236](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2023.1094236/full) `[FULL TEXT]`
- **Method agreement is near zero:** "almost no overlapping among predicted immunogenic peptides was observed between methods," and **only 7 immunogenic neoantigens were predicted as such by ALL methods.** Cross-method agreement in the heatmap analysis was "very poor." — same source `[FULL TEXT]`
- **Absolute performance on a clean benchmark is barely above chance:** across the seven benchmarked predictors, **ROC AUC ranged between 0.52 and 0.60** on ITSNdb, which the authors say shows "difficulty in distinguishing immunogenicity." The seven were **NetMHCpan 4.1, MHCflurry 2.0, MixMHCpred 2.1, PRIME 2.0, DeepImmuno, DeepHLApan 1.1.1, CIImm**. Best by average rank: **DeepHLApan (AR = 3.5)**; best classification: **PRIME (DOP = 0.82, F1 = 0.70)**; best on the validation set: **DeepImmuno (FPR = 16.81%, FNR = 14.29%)**. — same source `[FULL TEXT]`
- **Catastrophic failure mode documented:** on TESLA, **DeepHLApan predicted 100% (297) false positives** — the same method that ranked best overall by average rank. — same source `[FULL TEXT]`
- **Downstream clinical consequence documented:** Tumour Neoantigen Burden computed with immunogenicity predictors **never outperformed plain Tumour Mutation Burden** as an immune-checkpoint-blockade biomarker, and TNB "may result in an inappropriate ICB biomarker" because of "high false discovery rates." — same source `[FULL TEXT]`

### Inferences

- **AUCs reported in this literature cannot be compared across papers.** The base rate ranges from 0.01% to 65%. CNNeoPP's 0.81 (on a 45%-positive set) and Hetero-BioLSTM's 0.872 are not commensurable with the 0.52–0.60 observed on ITSNdb. A thesis that reports "we got AUC 0.9" here would be making a claim the field's own benchmark shows to be meaningless without the base rate.
- **This is the one genuinely open technical problem in the branch**: the negatives are unlabelled, not negative. In machine-learning terms the task is a **positive-unlabelled (PU) learning** problem that the entire literature treats as supervised binary classification. I found **no** paper in this branch that frames it as PU learning. That is a real, specific, cheap-to-execute idea — see Q6.
- The 0.52–0.60 ITSNdb ceiling, combined with near-zero inter-method overlap, strongly suggests the published "state of the art" in this branch is substantially **benchmark-specific overfitting**. A student should read any "we beat SOTA" claim here with suspicion, including their own.

### Gaps

- **No HLA-stratified performance data for Southeast Asian / Vietnamese alleles — not found.**
- **No quantification of how much reported method ranking is an artefact of the Immunity-2023 random negative subsampling — not found.** (This absence is itself an opportunity.)
- The two 2025 review articles that would have consolidated these figures were **both behind IdP login redirects** ([Genes & Immunity](https://doi.org/10.1038/s41435-025-00365-z), [Biomarker Research](https://link.springer.com/article/10.1186/s40364-025-00808-9)).

---

## Q5. NeoGen-BC and DeepNeoAG — what they leave open, who cites them

### Takeaway

**NeoGen-BC has ZERO citations** (published 2026-09-09, too recent) and **no follow-up work, no criticism, and no public code exists yet** — which means there is nothing to build on and no community reception to point at. **DeepNeoAG has 12 citations**, but almost all are reviews, not methodological follow-ups; the only methodological descendant is NeoGen-BC itself, by the same lab. The pair occupies exactly the architectural niche (PLM + multi-window scanning CNN, applied to neoantigens) that the student's existing pipeline shape would map onto.

### Cited Findings — NeoGen-BC

- Full record: Le Van The, Yuune Juan Peter Timothy, Lai Jiun-I, Ou Yu-Yen. "NeoGen-BC: A synergistic framework combining generative protein language models and multi-window deep learning for designing shared neoantigens in breast cancer." **Biochem Biophys Res Commun 836:154567**, published **2026-09-09**. Affiliations: Le, Yuune, Ou = **Dept. Computer Science and Engineering, Yuan Ze University, Chung-Li 32003, Taiwan**; Lai = Comprehensive Breast Health Center, Taipei Veterans General Hospital + Institute of Clinical Medicine, NYCU. Corresponding: jilai@nycu.edu.tw and yien@saturn.yzu.edu.tw. — [DOI 10.1016/j.bbrc.2026.154567](https://doi.org/10.1016/j.bbrc.2026.154567), [PubMed 42721858](https://pubmed.ncbi.nlm.nih.gov/42721858/) `[ABSTRACT]`
- **Citation count: 0.** Semantic Scholar API, queried 2026-10-02: `"citationCount": 0`, and the `/citations` endpoint returned `{"offset": 0, "data": []}` — **an empty list**. `referenceCount: 50`. — [Semantic Scholar API, DOI:10.1016/j.bbrc.2026.154567](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1016/j.bbrc.2026.154567) `[LIVE TEST]`
- **Open access: NO.** Semantic Scholar reports `"openAccessPdf": {"url": "", "status": "CLOSED"}`. — same source `[LIVE TEST]`
- **PubMed search for citing/related work found exactly ONE record matching "NeoGen-BC"** — the paper itself. — PubMed search via API, 2026-10-02 `[LIVE TEST]`
- Task, from the abstract: identify and **design shared (public) MHC class-II neoantigens** from **recurrent driver mutations in ESR1 and PIK3CA** in HR-positive and triple-negative breast cancer, for **off-the-shelf** vaccines rather than patient-specific ones. — [PubMed 42721858](https://pubmed.ncbi.nlm.nih.gov/42721858/) `[ABSTRACT]`
- Pipeline, from the abstract: **PLM embeddings + Retrieval-Augmented Generation (RAG) + multi-scale MCNN-BiLSTM classifier**; a **sliding-window strategy** maps epitopes from driver mutations; a **controlled ProtGPT2 generative module** explores immunogenic peptide space; candidates refined by **biophysical filtering, structural validation, and immunogenicity screening**. — same source `[ABSTRACT]`
- Headline metric: **AUC 0.9053 on an independent test set**, "outperforming other machine learning models." — same source `[ABSTRACT]`
- It positions itself specifically **against NetMHCIIpan 4.3**: it "identified immunogenic peptides difficult to assess by MHC-II binding tools like NetMHCIIpan 4.3" and "accurately detected validated MHC class II-restricted shared neoantigens from **ESR1 (Y537S, D538G)** and **PIK3CA (H1047R)** mutations, often missed by conventional predictors." — same source `[ABSTRACT]`
- **What the authors themselves say is forward-looking / unfinished** (this is the closest thing to a future-work statement available without the PDF): the framework "provides a **computational foundation** for next-generation '**tunable antigen**' vaccine design"; it "**enables scalable identification of candidate** peptide vaccines"; and it "**may complement** emerging therapeutic strategies, including **oral SERD-based approaches** aimed at enhancing immune modulation." The hedged verbs ("foundation", "candidate", "may complement") indicate **no experimental validation of the generated peptides was performed**. — same source `[ABSTRACT]`
- **Code availability: not found.** Neither the abstract nor the PubMed record gives a GitHub URL or web server. For comparison, DeepNeoAG from the same lab also has no code URL visible in its abstract. **This is a notable fact: the student cannot inspect, reuse, or reproduce NeoGen-BC's pipeline.**

### Cited Findings — DeepNeoAG

- Full record: "DeepNeoAG: Neoantigen epitope prediction from melanoma antigens using a synergistic deep learning model combining protein language models and multi-window scanning convolutional neural networks." **Int J Biol Macromol**, Volume 281 Part 1, November 2024. PMID 39366619. — [DOI 10.1016/j.ijbiomac.2024.136252](https://doi.org/10.1016/j.ijbiomac.2024.136252), [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0141813024070612) `[ABSTRACT]`
- **Citation count: 12.** `referenceCount: 31`. **Open access: NO** (`"openAccessPdf": {"url": "", "status": "CLOSED"}`). — [Semantic Scholar API, DOI:10.1016/j.ijbiomac.2024.136252](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1016/j.ijbiomac.2024.136252) `[LIVE TEST]`
- Task and distinguishing claim: combines **global sequence-level information from a pretrained PLM** with **local features from a multi-window scanning CNN**; crucially it **"predicts neoantigens without MHC allele information, reducing complexity and costs."** — [ScienceDirect abstract](https://www.sciencedirect.com/science/article/abs/pii/S0141813024070612) `[NOT VERIFIED — read via search-result summary of the abstract page, not the page itself]`
- **The complete list of the 12 citing papers**, from the Semantic Scholar citations endpoint, 2026-10-02 `[LIVE TEST]` — [API call](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1016/j.ijbiomac.2024.136252/citations):
  1. **NeoGen-BC**, BBRC, 2026 — [10.1016/j.bbrc.2026.154567](https://doi.org/10.1016/j.bbrc.2026.154567) — *same lab; the only methodological successor*
  2. "Therapeutic melanoma vaccines: Platforms, neoantigen strategies, and emerging combination immunotherapies," Ther Adv Vaccines Immunother, 2026 — [10.1177/25151355261488241](https://doi.org/10.1177/25151355261488241) — *review*
  3. "Neoantigen Targeting as a Novel Approach for Therapy-Resistant Tumors," Mol Diagn Ther, 2026 — [10.1007/s40291-026-00842-9](https://doi.org/10.1007/s40291-026-00842-9) — *review*
  4. "Artificial intelligence in immunotherapy: revolutionizing diagnostic and therapeutic applications in cancer and autoimmune diseases," Clin Exp Med, 2026 — [10.1007/s10238-026-02107-5](https://doi.org/10.1007/s10238-026-02107-5) — *review*
  5. "Leveraging Artificial Intelligence and Large Language Models for Cancer Immunotherapy," Adv Sci, 2026 — [10.1002/advs.202521936](https://doi.org/10.1002/advs.202521936) — *review*
  6. "Strategies of AI-Driven CAR-T Cell Therapy Towards Solid Tumours," Immunology, 2026 — [10.1111/imm.70124](https://doi.org/10.1111/imm.70124) — *review*
  7. "Protein foundation models: a comprehensive survey," Sci China Life Sci, 2026 — [10.1007/s11427-025-3147-2](https://doi.org/10.1007/s11427-025-3147-2) — *survey*
  8. "T-cell receptor therapy in ovarian cancer: concepts and challenges," J Ovarian Res, 2025 — [10.1186/s13048-025-01831-y](https://doi.org/10.1186/s13048-025-01831-y) — *review*
  9. **"Computational neoantigen prediction for cancer immunotherapy," Genes Immun, 2025** — [10.1038/s41435-025-00365-z](https://doi.org/10.1038/s41435-025-00365-z) — *the field review; DeepNeoAG is inside the canon*
  10. "Artificial Intelligence in Dermatology Research and Drug Discovery," Dermatol Clin, 2025 — [10.1016/j.det.2025.05.008](https://doi.org/10.1016/j.det.2025.05.008) — *review*
  11. "Deep learning in next-generation vaccine development for infectious diseases," Mol Ther Nucleic Acids, 2025 — [10.1016/j.omtn.2025.102586](https://doi.org/10.1016/j.omtn.2025.102586) — *review*
  12. "Enhanced inhibitor-kinase affinity prediction via integrated multimodal analysis," Int J Biol Macromol, 2025 — [10.1016/j.ijbiomac.2025.142871](https://doi.org/10.1016/j.ijbiomac.2025.142871) — *unrelated task, methodological citation*

### Inferences

- **11 of DeepNeoAG's 12 citations are reviews or unrelated.** Nobody outside the Ou lab has built a method on top of DeepNeoAG in two years. That cuts both ways: it means the niche is not swarming — but it also means **there is no community momentum, no shared benchmark, no leaderboard and no reusable code** for a student to plug into. A thesis here would be building alone.
- **The "what it leaves open" question is largely unanswerable from outside, and that is itself a finding.** NeoGen-BC is closed access, uncited, and has no published code. The student *does* have the PDF locally — so the authors' own Discussion/Future Work section is the single highest-value thing to extract, and it is the only place those gaps are written down. **I could not add to it from outside sources: zero citing papers, zero criticisms, zero follow-ups exist.**
- **The most strategically important inference in this whole report:** NeoGen-BC was published **three weeks before** the student's week-6 deadline, by the lab of **Prof. Yu-Yen Ou — who is NOT the advisor but is the advisor's frequent co-author**. If the student proposes a neoantigen topic in the advisor's method family, they are proposing to compete with, or to be seen as derivative of, a brand-new paper by the advisor's closest collaborator. Both outcomes are bad. Either the advisor cannot supervise it (no cancer publications in his 14-paper record) or the project is effectively Prof. Ou's, not the student's — and the student would be working in a domain where their own advisor cannot check their biology.

### Gaps

- **NeoGen-BC's dataset identity, size, train/test split, and the composition of its "independent test set" behind AUC 0.9053 — not found from outside sources.** Must come from the local PDF.
- **NeoGen-BC's and DeepNeoAG's code: no repository found.** If none exists, reproduction is impossible and any comparison a student makes would be against reported numbers only — a weak position.
- **DeepNeoAG's dataset, metrics (AUC etc.), and stated limitations — not found** (closed access, abstract only read via search summary).
- **No criticism or negative commentary on either paper exists in the literature.** Both are too recent and too lightly cited.

---

## Q6. What ONE student could realistically do in 8–9 weeks, and what is over-reach

### Takeaway

**Blunt verdict: this branch is a poor fit for this student, and the reason is not difficulty — it is supervision and positioning.** The data gate is passable (figshare + NCI splits), the imbalance problem is genuinely open, and a web app is easy. But the advisor has **zero cancer/tumour/neoantigen publications**, the nearest expertise belongs to a different professor at a different university, the obvious architectural move is already published by that professor's own lab three weeks ago, and the "fix the protocol" move is owned by Immunity 2023. Of the advisor's five criteria, a neoantigen thesis can plausibly score on **2, 4 and 5** and will struggle badly on **1 and 3**.

### Cited Findings bearing on feasibility

- **Compute feasibility is fine for the classifier, fatal for the generator.** NeoGen-BC's pipeline is PLM embeddings + RAG + MCNN-BiLSTM + sliding windows + **controlled ProtGPT2 generation** + biophysical filtering + **structural validation** + immunogenicity screening. — [PubMed 42721858](https://pubmed.ncbi.nlm.nih.gov/42721858/) `[ABSTRACT]`. ProtGPT2 generation and structural validation are the two components that need serious GPU and, for structure, AlphaFold-class resources — exactly what the student does not have (Colab/Kaggle free tier only).
- **Benchmark numbers prove the headroom is small and the metric is treacherous:** seven published predictors score **ROC AUC 0.52–0.60** on the clean ITSNdb benchmark, with **only 7 peptides predicted immunogenic by all methods**, and the best-ranked method (DeepHLApan) produced **100% (297) false positives** on TESLA. — [Front Immunol 1094236](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2023.1094236/full) `[FULL TEXT]`
- **The negative-set problem is openly stated as unsolved by a 2026 paper**: CNNeoPP calls for "expanding the diversity and scale of experimentally validated non-immunogenic neoepitopes" and admits biases in "peptide length selection and HLA allele representation." — [PMC12913462](https://pmc.ncbi.nlm.nih.gov/articles/PMC12913462/) `[FULL TEXT]`
- **The Immunity-2023 authors themselves flag the random negative subsampling as a source of variance** in their own released pipeline. — [NeoRanking README](https://raw.githubusercontent.com/bassanilab/NeoRanking/master/README.md) `[FULL TEXT]`
- **An open, reproducible baseline exists that a student can actually run:** NeoRanking ships `preprocess_data.sh`, `train_classifier.sh`, `test_classifier.sh`, pre-trained logistic-regression and XGBoost models on NCI-train, and pre-computed result files; Python 3.8.10 + `requirements.txt`. — same source `[FULL TEXT]`. This is logistic regression and XGBoost on tabular features — **CPU-feasible, no GPU needed**.
- **The web-app requirement is trivially satisfiable in this branch** — the field's norm is a web server (TumorAgDB at https://tumoragdb.com.cn, CNNeoDB at http://www.cnneodb.cn/, DeepNeo webserver, the DTU NetMHC servers). A "paste a mutated protein sequence → ranked candidate list with a confidence/abstention flag → SHAP explanation" app is a straightforward 2-week build.

### Inferences — what is realistically achievable (concrete)

Ranked by honesty-of-contribution per unit of risk:

1. **Reframe the task as positive-unlabelled (PU) learning on the open Immunity-2023 matrices, and quantify how much published method ranking is an artefact of negative subsampling.** `[Strongest defensible idea I found.]` The negatives in every dataset are "not shown immunogenic," not "shown non-immunogenic" (ITSNdb's own validation set: **113 of 120 negatives lack binding validation**). The Immunity authors admit their results shift with random negative resampling. **I found no paper in this branch that treats the problem as PU learning — not found.** Deliverables: a PU-learning baseline (e.g. non-negative risk estimation or bagging-based PU) vs the released LR/XGBoost baseline on the **NCI-train / NCI-test** split, plus a stability analysis across many negative resamplings. CPU-feasible. Scores on criteria **2** (improving the method), **3** (arguably a genuinely different learning framework, not just a new architecture), **4** (SHAP is already wired into the reference code), **5** (web app). Weak on **1**.
2. **An abstention / applicability-domain layer**: because methods disagree almost completely (only 7 unanimous positives) and false-positive rates reach 100% on out-of-distribution data (DeepHLApan on TESLA), a predictor that **declines to answer** outside its domain is a real clinical-utility contribution, and it is cheap. **Note: this is conceptually the same contribution the student already designed for the RTK–ATP topic** — which makes it credible to execute but weakens the novelty claim for this branch specifically.
3. **An HLA-stratified fairness/generalization audit, with a Vietnamese-population angle.** HLA-A\*02:01 is **40.2% of ITSNdb**. No published analysis stratifies predictor performance by Southeast Asian HLA alleles (**not found**). This is a genuinely under-occupied, locally-motivated question. Risk: the labelled data for non-A\*02:01 alleles may be too thin to support conclusions — this must be checked against the figshare matrices in week 1 before committing.
4. **A web app serving a reproducible re-implementation with calibrated probabilities and SHAP.** Safe, satisfies criterion 5, satisfies criterion 4, contributes little on 1–3 on its own. Fine as the *delivery layer* for ideas 1–3; **not** sufficient as the thesis.

### Inferences — what is over-reach (be explicit with the student)

- **Rebuilding or extending NeoGen-BC's pipeline. Hard no.** Controlled ProtGPT2 generation plus structural validation plus biophysical filtering is a multi-person, GPU-heavy pipeline; there is **no public code** (not found); it is **closed access**; and it is **three weeks old and uncited**, so there is no scaffolding. Attempting it in 8–9 weeks on Colab free tier would fail.
- **Any de novo peptide/vaccine design.** Generative design with no wet lab produces claims that cannot be validated. NeoGen-BC itself only reaches "matched experimentally validated ESR1 neoantigens in physicochemical and structural properties" — i.e. a similarity argument, not validation — and that is with a clinical co-author at Taipei Veterans General Hospital. The student has no such partner.
- **"Harmonize the datasets and compare methods fairly."** Owned by [Immunity 2023](https://doi.org/10.1016/j.immuni.2023.09.002) and, for the evaluation-database half, by [ITSNdb](https://doi.org/10.1007/978-1-0716-4558-1_11). Proposing this would be re-running `bash train_classifier.sh`.
- **Anything requiring HiTIDE raw sequencing data.** `access_type: controlled`, policy EGAP00001003206 — DAC application, measured in months, not weeks. `[LIVE TEST]`
- **Beating state of the art.** On the only clean benchmark, SOTA is **AUC 0.52–0.60**; on papers' own curated sets it is 0.81–0.905. The student cannot tell which number they are competing with, and neither can a reviewer. Any "we beat SOTA" framing here is a trap.
- **Building on Neodb, dbPepNeo or TumorAgDB as the primary data source.** `[LIVE TEST]`: Neodb unreachable on four hostnames; dbPepNeo's canonical domain is a JS redirect to a bare IP with a "contact the author for complete data" note; TumorAgDB is a two-week-old JavaScript SPA with no confirmed download endpoint.

### Scoring against the advisor's five criteria — honest assessment

| Criterion | Neoantigen branch verdict |
|---|---|
| **1. Novelty of the direction (nobody has done it)** | **Weak.** ≥12 methods 2021–2026, two 2026 entrants, two harmonized-benchmark resources, five competing databases. The PLM+multi-window-CNN slot is taken by the advisor's own frequent co-author ([DeepNeoAG 2024](https://doi.org/10.1016/j.ijbiomac.2024.136252), [NeoGen-BC 2026](https://doi.org/10.1016/j.bbrc.2026.154567)); the PLM-for-immunogenicity slot is also taken independently ([PLoS Comput Biol](https://pmc.ncbi.nlm.nih.gov/articles/PMC11581412/)); the protocol slot is taken by Immunity 2023. The one genuinely open slot I found is **PU learning / negative-set construction**. |
| **2. Proposing or improving a method** | **Achievable.** A PU-learning or abstention layer on top of the open NeoRanking baseline is a defensible methodological improvement, CPU-feasible. |
| **3. A genuinely new method (beyond PLM)** | **Weak-to-moderate.** "Beyond PLM" in this branch now means graph networks, Transformers, BioBERT ensembles, generative models — all already present in 2026 work. PU learning is a different *learning paradigm* rather than a new architecture, which the student could argue as "going further than PLM," but it is a rhetorical stretch. |
| **4. XAI** | **Achievable but NOT novel.** [NeoTImmuML 2025 already did SHAP](https://doi.org/10.3389/fimmu.2025.1681396) and concluded hydrophilicity + length drive immunogenicity; Immunity 2023 already plots **Shapley values** in its figures. SHAP here is table stakes, not a contribution. |
| **5. Web application** | **Easy and well-precedented.** The field's norm is a web server. 2 weeks. |

### Q6 bottom-line judgement

- **Data gate: PASS**, but only via the Immunity-2023 figshare matrices + Gartner NCI TrainingSet/TestingSet. That is the one path with a true independent test split, and it is open. **Verify the Gartner figshare URL first — it is the single untested link that the whole plan rests on.**
- **Time gate: PASS** for a tabular/PU/abstention thesis on CPU; **FAIL** for anything generative or structural.
- **Supervision gate: FAIL.** The advisor has no cancer, tumour or neoantigen publication. The biology of MHC class I/II presentation, T-cell recognition assays, and what makes an immunogenicity label trustworthy is exactly where a student most needs supervision, and it is exactly where this advisor cannot provide it. The nearest expert is Prof. Yu-Yen Ou at a different institution, who **is not the supervisor** and whose lab published in this space 23 days ago.
- **Positioning gate: FAIL or near-fail.** A student pitching PLM + multi-window CNN on neoantigens in October 2026 is pitching NeoGen-BC's abstract back to a professor who co-authors with NeoGen-BC's senior author. That is the worst possible framing for criterion 1.

### Gaps

- I did **not** evaluate the aging branch and cannot compare the two; that was outside my scope.
- Whether the advisor would *accept* a neoantigen topic despite having no publications in it is a human question I cannot answer from the literature.

---

## Q7. Is there a residue-level or window-classification framing of any neoantigen task?

### Takeaway

**Yes — and that is bad news, not good news, because the Ou lab already occupies it.** The "multi-window scanning CNN over a protein sequence" framing the student already has working is precisely DeepNeoAG's (2024) and NeoGen-BC's (2026) architecture, and NeoGen-BC additionally uses a **sliding-window strategy to map epitopes from driver mutations along the protein** — which is residue/window-level scanning in the exact sense the student means.

### Cited Findings

- **DeepNeoAG (2024)** combines "global sequence-level information captured by a pre-trained protein language model (PLM) with **local sequence-based information features extracted by a multi-window scanning convolutional neural network (CNN)**." — [ScienceDirect, DOI 10.1016/j.ijbiomac.2024.136252](https://www.sciencedirect.com/science/article/abs/pii/S0141813024070612) `[NOT VERIFIED — read via search summary of the abstract]`. The title itself contains "multi-window scanning convolutional neural networks." `[ABSTRACT — title verified via PubMed/Semantic Scholar]`
- **NeoGen-BC (2026)**: "A **sliding-window strategy maps epitopes from driver mutations**," combined with "a multi-scale **MCNN-BiLSTM** classifier." — [PubMed 42721858](https://pubmed.ncbi.nlm.nih.gov/42721858/) `[ABSTRACT]`
- **DeepNeoAG's distinguishing design choice is directly relevant:** it "predicts neoantigens **without MHC allele information**," which is what makes a pure sequence-window framing possible at all in this branch. — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0141813024070612) `[NOT VERIFIED]`
- **Hetero-BioLSTM (2026)** uses "an **adaptive encoding strategy for variable-length peptides**" with local and global modules joined by gated fusion — a different solution to the same variable-window problem. — [Springer 10.1007/978-981-92-3485-1_18](https://link.springer.com/chapter/10.1007/978-981-92-3485-1_18) `[NOT VERIFIED]`
- **CNNeoPP (2026)** uses **k-mer windows** explicitly: 6-mer tokenization with TF-IDF, 4-mer subsequences into BioBERT→CNN with kernel sizes [3,4,5], and 2-mer subsequences into BioBERT→FCNN. — [PMC12913462](https://pmc.ncbi.nlm.nih.gov/articles/PMC12913462/) `[FULL TEXT]`
- **What the dominant framing is NOT:** the mainstream neoantigen task is **peptide-level binary classification or ranking** of 8–11-mers (class I) or ~15-mers (class II), paired with an HLA allele. ITSNdb consists of **9-mers and 10-mers**; Immunity 2023 works at two granularities, **mutation level** and **neo-peptide level** — neither is residue level. — [Front Immunol 1094236](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2023.1094236/full) `[FULL TEXT]`; [PubMed 37816353](https://pubmed.ncbi.nlm.nih.gov/37816353/) `[ABSTRACT]`

### Inferences

- **There is no true per-residue labelled neoantigen task** in the sense of "label every amino acid position" (as in the student's ATP-binding-site pipeline). Immunogenicity labels attach to a **peptide–HLA pair**, not to a residue. The closest thing is **sliding-window scanning of a mutated protein to enumerate candidate peptides**, which is a *data-generation* step, not a labelled prediction task.
- So the student's existing pipeline shape transfers **mechanically** (the sliding-window + MCNN code would run) but **not scientifically** (the output unit changes from "is this residue a binding site" to "is this peptide immunogenic given this HLA"). The HLA-pairing requirement is a genuine structural addition the existing pipeline does not have — except in the DeepNeoAG framing, which drops HLA, and which is already published.
- **The reuse argument cuts against the student here.** "My pipeline already has this shape" is attractive for feasibility and fatal for novelty, because the two papers that already have that shape in this exact domain are by the advisor's frequent co-author. If the student wants to reuse the window-CNN machinery, a domain where Ou's lab has *not* already published is strictly better.

### Gaps

- **DeepNeoAG's exact window sizes, label granularity and whether it predicts a score per window position or per peptide — not found** (closed access; abstract only).
- **Whether any paper formulates neoantigen prediction as sequence labelling / token classification over a whole protein — I found none. Not found.** I cannot rule out that such a paper exists; my searches surfaced only window-scanning-as-preprocessing.

---

## Cross-cutting note on verification quality

Things I could **not** read, so that the report-writer does not over-claim:

| Source | What happened when I tried |
|---|---|
| Immunity 2023 full text | `https://www.cell.com/immunity/fulltext/S1074-7613(23)00406-5` → **HTTP 403**; `/pdfExtended/...` → **HTTP 403**; `https://europepmc.org/article/MED/37816353` → **HTTP 403**. Only the PubMed abstract record was readable. |
| Genes & Immunity 2025 review | `https://www.nature.com/articles/s41435-025-00365-z` → **HTTP 303 redirect to idp.nature.com login**. Abstract only. |
| Biomarker Research 2025 benchmarking review | `https://link.springer.com/article/10.1186/s40364-025-00808-9` → **HTTP 303 redirect to idp.springer.com login**. Not read. |
| NeoTImmuML metrics table | Frontiers text endpoint returned a **truncated body**; the AUC/accuracy table was absent. |
| NeoGen-BC full text | **Closed access** (`openAccessPdf: CLOSED`). The student has the PDF locally; I did not re-extract it, per instructions. |
| DeepNeoAG full text | **Closed access**. Abstract via search summary only. |

Things I verified by **direct live test on 2026-10-02** (highest-confidence items in this report): all Synapse / EGA / figshare / GitHub / database-portal results in Q3, the citation counts and citing-paper lists in Q5, and the `restrictionLevel: OPEN` vs `access_type: controlled` distinction that decides the data gate.
