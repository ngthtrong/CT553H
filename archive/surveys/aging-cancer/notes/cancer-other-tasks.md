# Cancer computational-biology tasks OTHER THAN neoantigen prediction — fit for a PLM + deep-learning + web-app thesis

> **LƯU TRỮ — không dùng để ra quyết định.** Tài liệu lịch sử; mọi câu "chốt / quyết định / khuyến nghị" bên dưới đã hết hiệu lực. Trạng thái hiện hành: [DECISIONS.md](../../../../DECISIONS.md).

> Research date: 2026-10-02. All link tests were run on 2026-10-02 from the student's machine (WSL2, Vietnam).
> Verification markers used throughout: **[FULL]** = I read the full text / full page; **[ABS]** = abstract or search-result snippet only; **[TITLE]** = only the title/metadata confirmed; **[NOT VERIFIED]** = could not confirm; **[LINK-TESTED]** = I actually issued an HTTP request and report the status code.
> Where a number came only from a search-engine summary of a paper I could not open, it is marked **[ABS]** and must be re-checked before it goes into a thesis.

---

## KQ1 — Enumerate and assess the candidate cancer subdomains (task definition, data, independent test set, SOTA, crowding, 8–9-week feasibility)

### Takeaway
Of the 14 candidate subdomains, only three clear the student's hard data gate (public + downloadable today + a genuine *independent* test set, not just cross-validation) **and** stay inside the advisor's method family: (1) kinase-specific phosphorylation-site prediction using dbPTM's non-homologous benchmark sets, (2) ligand/nucleotide-binding-site prediction on a cancer-relevant protein family (ABC multidrug-efflux transporters / oncogenic kinases), and (3) variant-effect prediction evaluated on the ProteinGym clinical (ClinVar) benchmark restricted to cancer genes. Everything else fails on data access, on being a gene-pair/omics problem rather than a sequence problem, on crowding, or on compute.

### Cited findings — per task

#### T1. Missense variant-effect / pathogenicity prediction (AlphaMissense, ESM-1v, EVE, ProteinGym)
- **Task shape:** input = protein sequence + a single amino-acid substitution at position *i*; output = a continuous fitness/pathogenicity score, binarised against ClinVar benign/pathogenic. This is a *position-conditioned* prediction, so a window around residue *i* is a legitimate representation.
- **Data, LINK-TESTED 2026-10-02:** `https://proteingym.org/` → **HTTP 200**, 0.43 s. `https://proteingym.org/download` → **HTTP 200** (but the page body my fetcher received contained only the title, so I could not read the per-file table from the site itself). The legacy mirror `https://marks.hms.harvard.edu/proteingym/` → **HTTP 403**.
- **Benchmark contents [FULL — ProteinGym GitHub README, https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/README.md]:** substitution benchmark ≈ **2.7 M missense variants across 217 DMS assays and 2,525 clinical proteins**; indel benchmark ≈ **300 k mutants across 74 DMS assays and 1,555 clinical proteins**. Downloadable archives: `DMS_ProteinGym_substitutions.zip` **1.0 GB**, `DMS_ProteinGym_indels.zip` **200 MB**, `clinical_ProteinGym_substitutions.zip` **123 MB**, `clinical_ProteinGym_indels.zip` **2.8 MB**. Current version **v1.3**. The README lists 40+ baselines but gives no comparative Spearman table (those live on the website and in CSVs).
- **Independent test set: YES.** The ProteinGym *clinical* benchmark is a separate held-out evaluation from the DMS benchmark; reported as **2.57 × 10⁴ benign and 2.68 × 10⁴ pathogenic variants across 2,227 genes** — [ABS, via search summary of the VESM paper, https://pmc.ncbi.nlm.nih.gov/articles/PMC13076216/]. **Re-verify this count in the paper's own text before citing.**
- **SOTA numbers:** ESM-1v zero-shot **ClinVar auROC 0.891**, rising to **0.902** after "NLR" fine-tuning — [ABS, https://arxiv.org/html/2405.06729v1]. VESM models (3B / 650M / 150M / 35M) are claimed to **surpass AlphaMissense** on the ProteinGym ClinVar benchmark in AUC and other binary metrics; AlphaMissense's performance on a newer ClinVar release (Mar 2025) is reported to depend strongly on minor allele frequency (gnomAD v4) — [ABS, https://pmc.ncbi.nlm.nih.gov/articles/PMC13076216/]. AlphaMissense primary paper: [ABS, https://www.science.org/doi/pdf/10.1126/science.adg7492].
- **Crowding:** PubMed, `("variant effect prediction"[TIAB]) AND (deep learning[TIAB] OR language model[TIAB]) AND 2024:2026[dp]` → **42 records** [FULL — I ran this E-utilities query myself on 2026-10-02].
- **Feasibility in 8–9 weeks:** MEDIUM-HIGH risk. Downloading 1.0 GB + 123 MB is fine. Scoring the *whole* clinical benchmark with ESM-2 650M on Colab free tier is many GPU-hours; a **cancer-gene-restricted subset** (e.g. only COSMIC Cancer Gene Census genes) makes it tractable. Web app = "paste sequence + mutation, get score + flag" — easy.

#### T2. Cancer driver vs passenger missense mutation classification
- **Task shape:** input = a somatic missense mutation in a tumour; output = driver vs passenger.
- **Data, LINK-TESTED:** `https://www.intogen.org/search` → **HTTP 200**; `https://www.intogen.org/download` → **HTTP 200**. `https://cancer.sanger.ac.uk/census` → **HTTP 200**; `https://cancer.sanger.ac.uk/cosmic/download` → **HTTP 200** *(the page loads; COSMIC file downloads themselves require free academic registration and a licence click — I did **not** complete a registered download, so treat actual file access as **[NOT VERIFIED]**)*. `https://www.cbioportal.org/` → **HTTP 200**.
- **Independent test set: YES, but tool-specific rather than community-standard.** CDMPred reports **AUC 0.83 on training and 0.80 on its independent test set**, benchmarked against CHASMplus, CHASM, CanDrA, FATHMM, TransFIC and CScape-somatic — [ABS, https://pmc.ncbi.nlm.nih.gov/articles/PMC11382650/]. For *synonymous* driver mutations, EPEL reports **AUC 85.7 %, AUPR 88.3 %** on consensus independent test datasets — [ABS, https://pmc.ncbi.nlm.nih.gov/articles/PMC11737855/]. A 2020 Genome Biology assessment states each benchmark uses an independent information source to define driver/passenger candidates — [ABS, https://genomebiology.biomedcentral.com/articles/10.1186/s13059-020-01954-z].
- **Crowding:** PubMed `(cancer driver mutation[TIAB] OR driver variant[TIAB]) AND (machine learning[TIAB] OR deep learning[TIAB]) AND 2024:2026[dp]` → **3 records** [FULL, my own query]. This looks *uncrowded*, but the query is narrow (title/abstract-only, exact phrases) — the true literature is larger. Treat "3" as a lower bound, not a field census.
- **Feasibility:** MEDIUM. The hard part is *defining the negative set* (passengers), which is where every paper differs and where leakage creeps in — the same failure mode that killed the RTK–ATP candidate. Web app easy.

#### T3. Driver gene vs passenger gene classification
- Same data sources as T2 (IntOGen HTTP 200, COSMIC CGC page HTTP 200). **No community independent test set found** — the labels *are* the gold-standard lists (CGC, IntOGen), so any split is a self-referential cross-validation. **[NOT VERIFIED]** that a held-out, time-stamped gene list benchmark exists.
- **Judgement:** fails the data gate on "independent test set". Also gene-level, not residue-level → no reuse of the student's pipeline.

#### T4. Oncogene vs tumour-suppressor classification from sequence/structure
- **Prior work:** a CNN on PDB 3-D structures to classify TSGs vs proto-oncogenes — [ABS, bioRxiv 2017, https://www.biorxiv.org/content/10.1101/177378.full.pdf]. Feature-based ML using OncoKB oncogene/TSG status, PPI counts, gene essentiality and pathway membership with Random Forest / SVM — [ABS, https://www.sciencedirect.com/science/article/pii/S3051115126000059]. Network-based Naïve Bayes reported at **92.5 % accuracy for tumour suppressors and 94.2 % for oncogenes** — [ABS, search summary; original source not pinned down, **do not cite without finding the paper**].
- **Known conceptual problem [ABS]:** the oncogene/TSG dichotomy is increasingly unreliable — TP53 is described as "an oncogene in disguise" (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4495363/), and many genes have both functions. Label noise is intrinsic.
- **Dataset size:** ~tens to low hundreds of genes per class → far too small for a PLM+CNN thesis with a credible independent test set.
- **Judgement:** RULE OUT (label noise + tiny N + no independent test set).

#### T5. TCR–pMHC binding prediction
- **Task shape:** input = TCR CDR3 (± V/J, ± full chains) + peptide (± MHC allele); output = binds / does not bind.
- **Independent test set: YES — the strongest community benchmark in this list.** IMMREP22 and IMMREP23 challenges.
- **Numbers [ABS, mixed sources — see conflict note]:** on "seen" peptides multiple methods reach **median AUC₀.₁ ≥ 0.7**, and a trivial **TCR-count baseline** reaches **average AUC₀.₁ > 0.7**; on "unseen" peptides earlier rounds showed methods **not better than random**, while the best IMMREP23 methods reached **macro-AUC₀.₁ 0.60**, significantly better than random. Separately reported: an **ESM-1b backbone at ROC-AUC@FPR<0.1 = 0.602**, and **NetTCR-2.2 at AUC₀.₁ = 0.600 on the IMMREP23 "Seen" group**. Sources: https://www.sciencedirect.com/science/article/pii/S2667119024000156 (IMMREP23 lessons learned), https://www.biorxiv.org/content/10.1101/2022.10.27.514020.full.pdf (IMMREP22), https://arxiv.org/html/2606.04994v1 (2026 re-benchmarking, "limited generalization power").
  - **CONFLICT / SUSPECT:** the figures 0.600 (NetTCR-2.2 on *Seen*) and 0.60 (best macro on *Unseen*) are implausibly identical in the search summary. One of the two is probably mis-attributed by the summariser. **Do not use either number without reading the IMMREP23 paper.**
- **Crowding:** PubMed `TCR[TIAB] AND (epitope[TIAB] OR pMHC[TIAB]) AND prediction[TIAB] AND 2024:2026[dp]` → **107 records** [FULL, my own query]. Crowded.
- **Killer finding:** the honest, published state of the field is that models **do not generalise to unseen peptides**, and the best IMMREP23 entries needed **structural modelling** to do better — [ABS, IMMREP23 lessons learned]. Structure prediction is explicitly outside the student's compute budget.
- **Judgement:** RULE OUT as a primary topic. Good benchmark, but the realistic outcome in 9 weeks is "my model is also near random on unseen peptides", which cannot satisfy advisor criterion 2.

#### T6. MHC class I and class II antigen presentation
- **Data, LINK-TESTED:** `https://www.iedb.org/` → **HTTP 200**; `https://www.iedb.org/database_export_v3.php` → **HTTP 200**. `https://services.healthtech.dtu.dk/services/NetMHCpan-4.1/` → **HTTP 200**.
- **SOTA [ABS]:** OnmiMHC, a deep-learning model integrating large-scale MS data, reports **PR-AUC 0.606** and **TOP20 %-PPV 0.690** in the MHC-II domain, claimed to beat baselines — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11906482/. MHC-II is described as the weaker, scarcer side: "predictive accuracy on rare and less characterized MHC alleles remains poor and Class II predictors are scarce"; class-II ligand lengths mainly **13–25 aa** — [ABS, https://www.biorxiv.org/content/10.1101/752469.full.pdf and https://arxiv.org/pdf/2512.14011].
- **Crowding:** PubMed `MHC[TIAB] AND presentation[TIAB] AND prediction[TIAB] AND 2024:2026[dp]` → **80 records** [FULL, my own query].
- **Judgement:** MHC-I is saturated (NetMHCpan is a 20-year-old moving target). MHC-II is less saturated but is also exactly where Prof. Ou's **neoantigen** line sits (see KQ4), i.e. it re-enters the subdomain the student was told to step away from. Also arguably still "neoantigen-adjacent".

#### T7. Tumour-associated antigen (TAA) / tumour T-cell antigen (TTCA) prediction
- **Resources [ABS]:** TumorAgDB2.0 at `https://tumoragdb.com.cn` with **187,223 entries**, released alongside NeoTImmuML (https://pubmed.ncbi.nlm.nih.gov/41200173/). Cancer Antigens Database (CAD) at `http://cad.bio-it.cn/`. A 2025 review of ML approaches for **tumour T-cell antigen (TTCA)** identification covers core algorithms, benchmark datasets, feature encodings and web-server usability — https://www.sciencedirect.com/science/article/abs/pii/S1476927125001008. Expression-state-based TAA inference across 33 cancer types from RNA-seq — [ABS, https://pubmed.ncbi.nlm.nih.gov/39561714/].
- I did **not** link-test tumoragdb.com.cn or cad.bio-it.cn — **[NOT VERIFIED]** whether they resolve from Vietnam.
- **Shape note:** TTCA prediction is *whole-peptide/whole-protein* binary classification from sequence — the same shape as Prof. Ou's **RAG_MCNNIL6** (IL-6 inducing epitopes). That makes it a template match but also means the group has already published that template.
- **Judgement:** plausible but (a) benchmark sets are small and heterogeneous, (b) it is immunology-adjacent, i.e. close to the neoantigen line the student wants to avoid, (c) data access unverified.

#### T8. Cancer-context PTM site prediction (phosphorylation, acetylation, ubiquitination) ★ STRONGEST DATA POSITION
- **Data, LINK-TESTED:** the working dbPTM mirror is `https://biomics.lab.nycu.edu.tw/dbPTM/` → **HTTP 200**, 0.10 s. The older `https://awi.cuhk.edu.cn/dbPTM/` → **HTTP 403** (dead for this purpose). `https://www.phosphosite.org/` → **HTTP 200**. `https://activedriverdb.org/` → **HTTP 200**.
- **dbPTM experimental site counts [FULL — I scraped https://biomics.lab.nycu.edu.tw/dbPTM/download.php myself]:**
  | PTM type | experimental sites | supporting literatures |
  |---|---|---|
  | Phosphorylation | **1,615,054** | 44,986 |
  | Ubiquitination | **348,307** | 669 |
  | Acetylation | **138,169** | 19,451 |
  | Dephosphorylation | **133** | 95 |
  Download links are offered per PTM type in Windows and MAC/Linux variants. Each record provides UniProt ID, modified position, PTM type, and **the sequence with 10 residues upstream and 10 downstream** (dashes used at protein termini) — i.e. **dbPTM ships pre-windowed data**.
- **dbPTM "benchmark dataset" section — this is the independent test set [FULL, same page]:** dbPTM explicitly states that because cross-validation numbers are not comparable across tools, "this update compiles **non-homologous benchmark datasets** to evaluate the predictive power for PTM site prediction tools", with guidance for high-Sn, high-Sp or balanced operating points. The benchmark is broken down **by kinase group**, with three unlabeled numeric columns per row (the header row was not captured by my scrape; the columns are *plausibly* proteins / positive sites / negative sites — **column meaning NOT CONFIRMED**):
  | Kinase | col1 | col2 | col3 |
  |---|---|---|---|
  | CDK | 1,020 | 1,503 | 29,823 |
  | MAPK | 857 | 1,270 | 22,436 |
  | PKA | 905 | 1,209 | 29,813 |
  | PKC | 691 | 943 | 24,207 |
  | CK2 | 511 | 819 | 15,387 |
  | CAMKL | 454 | 556 | 20,129 |
  | GSK | 291 | 397 | 10,328 |
  | AKT | 351 | 380 | 14,617 |
  | CAMK2 | 254 | 366 | 12,575 |
  | CK1 | 174 | 339 | 5,808 |
  | RSK | 221 | 215 | 6,985 |
  | GRK | 77 | 147 | 2,310 |
  | PKG | 126 | 145 | 7,311 |
  | DYRK | 109 | 142 | 3,470 |
  | MAPKAPK | 100 | 125 | 3,096 |
  | DMPK | 99 | 109 | 3,533 |
  | PKD | 88 | 97 | 3,401 |
  | PDK1 | 77 | 93 | 2,274 |
  | SGK | 63 | 77 | 3,057 |
  **The cancer angle is built in:** CDK, MAPK, AKT, PKC, CK2, GSK3, PDK1, SGK and RSK are all core oncogenic signalling kinases (PI3K–AKT–mTOR, RAS–MAPK, cell-cycle CDKs).
- **Cancer-mutation-meets-PTM resource [ABS]:** ActiveDriverDB uses **more than 260,000 experimentally detected PTM sites** to predict the functional impact of genetic variation, and reports that **16–21 % of known amino-acid substitutions affect PTM sites** across pathogenic disease mutations, cancer somatic mutations and population germline variants — https://academic.oup.com/nar/article/46/D1/D901/4566599 and https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8021862/ (2021 update).
- **Existing methods / SOTA [ABS]:** DeepPhos (CNN, better than other DL architectures on S/T and Y sites, https://www.researchgate.net/publication/335190575_DeepPhos...); DeepPPSite (stacked LSTM, https://www.sciencedirect.com/science/article/abs/pii/S0003269720304875); DeepPhosPPI (attention-CNN + transformer, uses the **Betts dataset, 306 records** and **Dset_308, 308 records** as independent benchmarks, https://academic.oup.com/bib/article/26/5/bbaf462/8248860); a 2025 autoregressive-transformer kinase-substrate predictor using **ESM-2 650M**, trained on **5,385 unique substrates**, validated on **969**, with three test sets including a **"Rare-Group Test Set" of 14 samples from two kinase groups entirely excluded from training** — https://www.biorxiv.org/content/10.1101/2025.03.12.642740v1.full.
- **Crowding:** PubMed `((phosphorylation site[TIAB] OR ubiquitination site[TIAB] OR acetylation site[TIAB]) AND prediction[TIAB] AND deep learning[TIAB]) AND 2024:2026[dp]` → **14 records** [FULL, my own query]. **Least crowded of the tasks with real benchmarks.**
- **Feasibility:** HIGH. Pre-windowed text data, tiny files, no structure prediction, embeddings cacheable. Web app = "paste sequence → highlighted predicted sites per kinase" — directly analogous to the RTK–ATP app the student already designed.

#### T9. PPI perturbation by cancer mutations (ΔΔG)
- **Data, LINK-TESTED:** `https://life.bsc.es/pid/skempi2` → **HTTP 200**; `https://life.bsc.es/pid/skempi2/database/index` → **HTTP 200**. `http://biosig.unimelb.edu.au/mcsm_ppi2/` → **HTTP 200**.
- **Crowding query artifact:** my PubMed query `(protein-protein interaction[TIAB] AND mutation[TIAB] AND "binding affinity change"[TIAB]) AND 2024:2026[dp]` → **0 records** [FULL, my own query]. This is a **query artifact from an over-specific phrase**, not evidence the field is empty. I did not re-run with better terms — **GAP**.
- **Blocking issue:** SKEMPI 2.0 is a **structure-keyed** database (mutations mapped to PDB complexes). Doing it from sequence alone discards the thing that makes the task work; doing it with structure needs complexes the student cannot predict on free Colab. ΔΔG is also a regression task, not window classification.
- **Judgement:** RULE OUT (structure dependence + wrong task shape + no PLM-sequence-only standard benchmark confirmed).

#### T10. Drug–target interaction / drug-response prediction in oncology
- **Data, LINK-TESTED:** `https://www.cancerrxgene.org/downloads/bulk_download` (GDSC) → **HTTP 410 Gone** — the bulk-download URL I tried is retired; a different GDSC path may work but I did not find it. `https://depmap.org/portal/data_page/?tab=allData` → **HTTP 200**.
- **Benchmarks [ABS]:** "Davis is the most widely used dataset for benchmarking DTI and DTA models, consisting of interaction information from the **selectivity assay of the kinase protein family**"; KIBA "contains the largest collection of binding information for kinase family proteins", sourced from ChEMBL and STITCH — https://academic.oup.com/bib/article/26/5/bbaf491/8260789. A modification-aware, "complete" DAVIS re-release exists — [ABS, https://arxiv.org/pdf/2512.00708].
- **Crowding:** PubMed `((drug-target interaction[TIAB] OR drug-target affinity[TIAB]) AND deep learning[TIAB]) AND 2024:2026[dp]` → **240 records** [FULL, my own query]. **The most crowded task in this whole list.**
- **Judgement:** RULE OUT. 240 papers in 3 years, requires a chemistry/molecular branch the advisor has never published, and Davis/KIBA splits are a known leakage minefield.

#### T11. Kinase inhibitor selectivity prediction
- **SOTA [ABS]:** PDCNet on a benchmark of **141,086 unique compounds** reports test-set **AUC 0.9213, F1 0.7656, MCC 0.7071, BA 0.8388** — search summary of https://pmc.ncbi.nlm.nih.gov/articles/PMC10829268/ ("Large-scale comparison of machine learning methods for profiling prediction of kinase inhibitors"). MMCLKin (contrastive learning) is reported to beat baselines on **3DKDavis** and to lead Pearson correlations on the **low-similarity LSKIBA** split — [ABS, https://pmc.ncbi.nlm.nih.gov/articles/PMC12675671]. 3-D CNNs have been used to predict the target landscape of kinase inhibitors — [ABS, https://pmc.ncbi.nlm.nih.gov/articles/PMC10508635/].
- **Judgement:** RULE OUT. Same reasons as T10, plus the input is dominated by the *compound*, not the protein sequence — it leaves the advisor's method family entirely.

#### T12. Cancer subtype classification
- **Crowding:** PubMed `cancer subtype[TIAB] AND classification[TIAB] AND deep learning[TIAB] AND 2024:2026[dp]` → **50 records** [FULL, my own query].
- **Blocking issue:** this is a *multi-omics / expression* problem (TCGA RNA-seq, methylation), not a protein-sequence problem. TCGA open-tier expression is downloadable, but the clinically interesting layers are controlled-access (dbGaP/EGA) — explicitly out of scope per the brief. Zero overlap with PLM + window CNN.
- **Judgement:** RULE OUT (wrong data modality, zero advisor fit).

#### T13. Synthetic lethality prediction
- **Data, LINK-TESTED:** `https://synlethdb.sist.shanghaitech.edu.cn/` → **HTTP 200**. The older `https://awi.cuhk.edu.cn/~SynLethDB/` → **HTTP 404**.
- **Contents [ABS]:** SynLethDB 2.0 holds **9,845 unique genes and 35,913 positive SL gene pairs**; of those, **26,591** came from CRISPR, RNAi and text mining and **9,322** were themselves *computationally predicted* (i.e. label noise baked in). It ships a knowledge graph, SynLethKG, with PPI, GO, pathway, complex and protein-sequence layers — https://www.researchgate.net/publication/360608408_SynLethDB_20... A Nature Communications 2024 benchmark evaluated **11 methods (3 matrix-factorisation + 8 deep-learning)** — https://www.nature.com/articles/s41467-024-52900-7.
- **Crowding:** PubMed `synthetic lethality[TIAB] AND prediction[TIAB] AND 2024:2026[dp]` → **56 records** [FULL, my own query].
- **Judgement:** RULE OUT. It is a **gene-pair link-prediction / graph** task. The advisor's newest paper (SirtSAGE) is a graph model, so the *architecture* is not alien — but there is no residue-level reuse, and 9,322 of 35,913 positives are predictions rather than measurements.

#### T14. Cancer-related protein-family classification (incl. binding sites on cancer-relevant families) ★ BEST ADVISOR FIT
- **Reference point — ATP-binding-site prediction is a live, *under-solved* residue-level problem.** PFDCNN (Scientific Reports 2025) [FULL — https://pmc.ncbi.nlm.nih.gov/articles/PMC12647579/]:
  - Method: **P**retrained **F**ractional-order **D**eep **CNN**, features from **ESM-2**.
  - Training sets: **ATP-227** (227 sequences), **ATP-388** (388), **PATP-1930** (1,930). Independent test sets: **ATP-17** (17 sequences) and **ATP-41** (41 sequences).
  - ATP-17: **AUC 0.965, Accuracy 0.990, Sensitivity 0.391, Specificity 0.997, Precision 0.642, MCC 0.497.**
  - ATP-41: **AUC 0.941, Accuracy 0.984, Sensitivity 0.194, Specificity 0.999, Precision 0.857, MCC 0.403.**
  - Code: `https://github.com/Yswangustb/PFDCNN`.
  - **Read the sensitivity numbers.** 0.391 and 0.194 recall mean the published SOTA *misses 61–81 % of real ATP-binding residues*. The headline "accuracy 0.990" is the class imbalance talking. **This is a large, honest, defensible contribution gap** and directly supports advisor criterion 2.
- **Residue-level multiview work on exactly this, with an explicit kinase application [TITLE only]:** "Residue-Level Multiview Deep Learning for ATP Binding Site Prediction and Applications in Kinase Inhibitors", PMID 39690486 — https://pubmed.ncbi.nlm.nih.gov/39690486/. **My fetch was blocked by PubMed's cookie wall, so I confirmed only the title/PMID.** From the title: Multiview-ATPBind integrates 1-D sequence and 3-D structure and introduces "ResiBoost", a residue-level boosting algorithm for the rare-positive imbalance — [ABS, from search summary, not from the paper]. **This paper is the single most important one for the student to read**, because it is simultaneously the nearest competitor and the proof that "ATP sites → kinase inhibitors" is an accepted cancer framing.
- **Crowding:** PubMed `ATP-binding site prediction[TIAB] AND 2024:2026[dp]` → **6 records**; `(binding site prediction[TIAB]) AND (protein language model[TIAB]) AND 2024:2026[dp]` → **27 records** [FULL, both my own queries]. Very uncrowded.
- **Data, LINK-TESTED:** `https://zhanggroup.org/BioLiP/` → **HTTP 200**; `https://zhanggroup.org/BioLiP/download.html` → **HTTP 200**. UniProt REST query for reviewed protein-kinase-superfamily entries → **HTTP 200** (`https://rest.uniprot.org/uniprotkb/search?query=family:"protein kinase superfamily" AND reviewed:true&size=1`).
- **Cancer-relevant families available [ABS]:** human ABC transporters: **49 ABC proteins in 7 subfamilies (A–G)**; the three main multidrug-resistance efflux pumps are **ABCB1 (P-glycoprotein/MDR1, ~170 kDa)**, **ABCC1 (MRP1)** and **ABCG2 (BCRP, chromosome 4q22, ~75 kDa)** — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7649427/, https://pmc.ncbi.nlm.nih.gov/articles/PMC4287283/, https://www.oaepublish.com/articles/cdr.2021.19. Mechanistically: "The **NBDs are highly conserved** across the superfamily … P-loop NTPase superfamily with a RecA-type binding core along with a unique ABC signature motif, **LSGGQ**. The TMDs are far less conserved" — [ABS, same sources].
- **Warning on the ABC-transporter angle:** 49 human ABC proteins is a very small label set, and existing ABC-transporter ML work is almost entirely **compound-side** (predicting whether a *drug* is a substrate/inhibitor), not sequence-side: MolMM reports **AUC-ROC 83.33 % for ABCB1 inhibitors and 81.26 % for substrates**; a Pdr5p-trained model transferred to human P-gp at **87 % accuracy**; SHAP was used to expose polar/hydrophobic motifs separating substrates from inhibitors — all [ABS], https://pmc.ncbi.nlm.nih.gov/articles/PMC13064662/, https://doi.org/10.3390/molecules31122084, https://pubs.acs.org/mpohbp/article/22/11/7022/3750445/. **I found no established independent test set for sequence-level ABC-family classification** → this sub-angle fails the data gate unless the student builds the split themselves with CD-HIT, which is exactly what the advisor's own papers do but is *not* a pre-existing independent benchmark.

### Inferences
- Only T8 (kinase-specific PTM sites via dbPTM) and T14 (residue-level binding-site prediction on a cancer-relevant family) simultaneously satisfy: data downloadable today, a pre-existing non-homologous/independent evaluation set, uncrowded, no structure prediction needed, and reuse of the student's existing PLM + windowed multi-CNN code.
- T1 (ProteinGym clinical) is the only candidate with a **genuinely community-standard, large, independent clinical test set**. It is the strongest answer to "the data gate", and the weakest on advisor fit.
- Every drug/compound-centric task (T10, T11) and every gene-pair/omics task (T12, T13, T3) should be dropped: they leave the advisor's method family and force the student to learn cheminformatics or multi-omics from scratch in 9 weeks.
- The PFDCNN sensitivity figures (0.391 / 0.194) are the most useful single fact in this report for criterion 2: a thesis whose stated goal is "recover the positives the SOTA misses, measured by MCC and recall rather than accuracy" has a built-in, quantified target.

### Gaps
- Could not read the Multiview-ATPBind (PMID 39690486) abstract or full text — PubMed served only a cookie notice and I did not try the JCIM/DOI route. Its exact datasets and metrics are unknown to me.
- Could not read the ProteinGym download table from proteingym.org itself (the page body my fetcher received held only the title); file names/sizes come from the GitHub README instead.
- Did not verify an actual registered COSMIC download, nor locate a working GDSC bulk-download URL (the one I tried returned HTTP 410).
- Did not link-test tumoragdb.com.cn or cad.bio-it.cn.
- The dbPTM kinase-benchmark table's three numeric columns are unlabeled in my scrape; their meaning is inferred, not confirmed.
- My PubMed crowding counts are title/abstract phrase queries and systematically **undercount**; they are comparable to each other but are not field censuses. The PPI-ΔΔG count of 0 is a query artifact.

---

## KQ2 — Which of these are RESIDUE-LEVEL window-classification problems (direct reuse of the student's existing pipeline)?

### Takeaway
Four tasks are true residue-level window-classification problems — kinase-specific PTM site prediction, ligand/nucleotide-binding-site prediction, protein–peptide interaction site prediction, and (in a looser sense) position-conditioned variant-effect scoring. Of these, **kinase-specific phosphorylation-site prediction is the cheapest possible port** of the student's pipeline, because dbPTM distributes the data *already windowed at ±10 residues*.

### Cited findings
- **RESIDUE-LEVEL — YES, direct reuse:**
  - **PTM site prediction (T8).** dbPTM records ship "the sequence with upstream 10 amino acids to downstream 10 amino acids", with dashes at termini — [FULL, https://biomics.lab.nycu.edu.tw/dbPTM/download.php]. Positive = modified residue, negative = unmodified residue of the same amino-acid type. Identical in shape to the ATP-site task.
  - **Ligand / ATP / nucleotide binding-site prediction (T14).** PFDCNN is explicitly a residue-level binary classifier over ATP-227/ATP-388/PATP-1930 with ATP-17/ATP-41 held out — [FULL, https://pmc.ncbi.nlm.nih.gov/articles/PMC12647579/]. Multiview-ATPBind is titled "**Residue-Level** Multiview Deep Learning for ATP Binding Site Prediction" — [TITLE, https://pubmed.ncbi.nlm.nih.gov/39690486/].
  - **Protein–peptide interaction sites.** Prof. Ou's group published "ProtTrans and multi-window scanning convolutional neural networks for the prediction of **protein–peptide interaction sites**", *J Mol Graph Model*, 2024 Jul — [FULL metadata, PubMed E-utilities esummary, retrieved 2026-10-02]. This is the group's own residue-level template.
  - **Nucleic-acid-binding residue prediction.** ESM-NBR does residue-level nucleic-acid-binding prediction from PLM features with multi-task learning — [ABS, https://arxiv.org/pdf/2312.00842]. Relevant because the advisor has a protein–DNA branch.
- **PARTIALLY residue-level (position-conditioned, but the label depends on the substituted amino acid, not just the position):**
  - **Variant-effect / pathogenicity prediction (T1, T2).** A window around the mutated residue is a valid encoder input, but the model must also consume the wild-type → mutant identity pair, so the output head differs from a plain binary window classifier.
- **NOT residue-level (no reuse):** driver/passenger *gene* classification (T3), oncogene/TSG classification (T4), TCR–pMHC (T5 — pairwise sequence-to-sequence), MHC presentation (T6 — whole-peptide classification), TAA/TTCA (T7 — whole-peptide/protein classification), PPI ΔΔG (T9 — structure-keyed regression), DTI/DTA (T10) and kinase-inhibitor selectivity (T11 — compound × protein pair), cancer subtype (T12 — sample-level omics), synthetic lethality (T13 — gene-pair graph link prediction).

### Inferences
- The port cost ranking for the student's existing code is: **PTM sites (lowest — data arrives pre-windowed) < binding sites on a new family (low — same FASTA + annotation format as the RTK–ATP work) < protein–peptide sites (low, but already done by the group) << variant effect (medium, new output head) << everything else (rewrite)**.
- Because T8 and T14 share the student's exact evaluation vocabulary (per-residue Sn/Sp/MCC/AUC under heavy class imbalance, non-homologous splits by CD-HIT), the "leakage-controlled protocol" work already drafted for RTK–ATP transfers almost verbatim. That protocol work is reusable intellectual capital — it should not be thrown away with the topic.

### Gaps
- I did not verify whether dbPTM's ±10 window is wide enough for a multi-window CNN (the advisor's papers typically scan several window widths up to ±(15–25)); if the distributed file is capped at 21 residues, the student would need to re-extract windows from UniProt sequences using dbPTM positions. **This is a concrete, checkable risk to resolve before week 6.**

---

## KQ3 — Have QT Ho or YY Ou published in any of these? Which task sits closest to QT Ho's actual expertise?

### Takeaway
Prof. QT Ho's PubMed-indexed co-authored record contains **no cancer/oncology paper** — the only tumour-named item is TNFPred (tumour necrosis factors, a cytokine family, not oncology). The cancer-adjacent work (neoantigens, IL-6 epitopes) belongs to **Prof. Ou's** group *without* QT Ho as an author. The task closest to QT Ho's own expertise is **residue-level ligand/nucleotide-binding-site prediction**, followed by **kinase-specific PTM site prediction** and **membrane/transport-protein family classification**.

### Cited findings
All publication metadata below was retrieved by me on 2026-10-02 via NCBI E-utilities (`esearch` + `esummary`, db=pubmed) — **[FULL metadata]**.

- **PubMed `Ho QT[Author] AND Ou YY[Author]` → 17 records.** In reverse date order:
  1. 2026 Jun — **msCNN-PLM-FAD**: FAD binding sites, protein language representation + multiple **separable** windows CNN — *Analytical Biochemistry*
  2. 2025 Dec — **mCNN-GenEfflux**: efflux proteins and superfamilies, **generative proteins** + multi-window CNN — *Computational Biology and Chemistry*
  3. 2023 Dec — review: features for membrane protein sequences, from MSA to pre-trained language models — *Proteomics*
  4. 2022 Sep — **MFPS_CNN**: ion transporters, multi-filter pattern scanning from PSSM + CNN — *Molecular Informatics*
  5. 2022 Jul — **ATP-binding sites in transport proteins** via multiple convolutional window scanning — *Proteins*
  6. 2022 Jan 17 — **mCNN-ETC**: electron transporters and functional families — *Briefings in Bioinformatics*
  7. 2021 Apr — **FAD-BERT**: FAD binding sites with pre-trained bidirectional transformers — *Computers in Biology and Medicine*
  8. 2021 Apr — **GT-Finder**: classify the family of **glucose transporters** with pre-trained BERT — *Computers in Biology and Medicine*
  9. 2021 Sep 2 — BERT + 2-D CNN to identify **DNA enhancers** — *Briefings in Bioinformatics*
  10. 2020 Oct 22 — **TNFPred**: identifying **tumour necrosis factors** using hybrid features based on word embeddings — *BMC Medical Genomics*
  11. 2022 Mar–Apr — Chou's 5-steps rule + word embeddings for electron transport protein prediction — *IEEE/ACM TCBB*
  12. 2020 Oct — language representation learning for protein complex categories in the electron transport chain — *Molecular Informatics*
  13. 2019 Jul 15 — word embeddings for substrate specificities of **transporters** — *Analytical Biochemistry*
  14. 2019 Feb — 2-D CNNs for **GTP binding sites in Rab proteins** — *J Bioinform Comput Biol*
  15. 2019 Apr 15 — **iEnhancer-5Step** — *Analytical Biochemistry*
  16. 2018 Aug 15 — molecular functions of **Rab GTPases** with deep CNNs — *Analytical Biochemistry*
  17. 2017 Sep 5 — CNN + PSSM for **electron transport proteins** — *J Computational Chemistry*
- **Cancer check on QT Ho:** none of the 17 co-authored records is an oncology paper. `Ho QT[Author] AND (cancer[TIAB] OR tumor[TIAB])` → **9 records**, but **`Ho QT[Author]` alone returns 71 records**, i.e. the initials collide with multiple different authors, so those 9 cannot be attributed to the advisor. **[Attribution NOT VERIFIED — do not claim "QT Ho has 9 cancer papers".]** The only safe statement: *within his co-authored record with Prof. Ou, the only tumour-named paper is TNFPred, and TNF is a cytokine family, not a cancer-genomics topic.* This agrees with the repo's own note that his 14-paper Google Scholar scrape has no cancer/tumour/neoantigen paper (`project/advisor-research.md`).
- **PubMed `Ou YY[Author] AND (cancer OR tumor OR neoantigen)[TIAB]` → 19 records.** The relevant ones (authors as listed by PubMed):
  - 2026 Oct 22 — **NeoGen-BC**: generative protein language models + multi-window deep learning for designing **shared neoantigens in breast cancer** — *Biochem Biophys Res Commun* — Le VT, Yuune JPT, Lai JI, **Ou YY**. *(No QT Ho.)*
  - 2024 Nov — **DeepNeoAG**: neoantigen epitope prediction from **melanoma** antigens, PLM + multi-window scanning CNN — *Int J Biol Macromol* — Chuang CC, Liu YC, **Ou YY**. *(No QT Ho.)*
  - 2025 Jul 14 — **RTK_RAG**: retrieval-augmented generation + multi-window CNN for **ATP binding site prediction in receptor tyrosine kinases** — *J Chem Inf Model* — Wei SS, Jhang WE, Liu YC, Chuang CC, **Ou YY**. **QT Ho is NOT an author.** (Important: the student's abandoned topic was built on a paper the *advisor did not write*.)
  - 2025 Mar 10 — **RAG_MCNNIL6**: retrieval-augmented multi-window CNN for **IL-6 inducing epitopes** — *J Chem Inf Model* — Chuang CC, Liu YC, Jhang WE, Wei SS, **Ou YY**.
  - 2025 May 2 — **NA_mCNN**: classification of **sodium transporters**, multi-window DL + ProtTrans, framed around "therapeutic potential" — *J Proteome Res* — Malik MS, Le VT, **Ou YY**.
  - 2026 Feb — **MCNN-AAPT**: classification and functional prediction of **amino-acid and peptide transporters** in secondary active transporters, PLM + multi-window DL — *J Biomol Struct Dyn* — Malik MS, Le VT, Shah SMA, **Ou YY**.
  - 2024 Sep 26 — **VesiMCNN**: PLM + multi-window scanning CNN to identify **vesicular transport proteins** — *Int J Biol Macromol*.
  - 2024 Jul — **ProtTrans + multi-window scanning CNN for protein–peptide interaction sites** — *J Mol Graph Model*.
  - 2023 Dec — PLM + multi-window DL for **secondary active transporters** — *Methods*.
  - 2021 Oct — **TRP-BERT**: discriminating **TRP channels** with BERT — *Comput Biol Med*.
- **Repo-internal corroboration [FULL — `/home/ngthtrong/CT553H/docs/common/advisor/README.md`]:** QT Ho's 14-paper Google Scholar scrape contains no cancer/tumour/neoantigen paper; his newest paper is **SirtSAGE** (2026, *J Comput Biophys Chem*), ESM-2 → GATv2 graph attention with AlphaFold pLDDT gating, on **sirtuins**; the XAI precedent in his own record is **BERT-Promoter** (2022, *Comput Biol Chem*) using **SHAP**.

### Inferences
- **Closest-to-QT-Ho ranking, from his own authorship record:**
  1. **Residue-level ligand/cofactor/nucleotide binding-site prediction** — he has FAD (×2), ATP in transport proteins, GTP in Rab proteins. This is his single densest methodological lane.
  2. **Membrane / transport protein family classification** — efflux, ion transporters, electron transporters, glucose transporters, SNARE. Densest *subject* lane.
  3. **PTM-adjacent residue prediction** — he has no PTM paper, but PTM sites are the same residue-level windowed problem as binding sites, and his group's protein–peptide-interaction-site paper shows the port is routine for them.
  4. **Protein–DNA / DNA elements** — promoters, enhancers, 6mA; this is where his XAI (SHAP) precedent lives.
  5. **Sirtuins / aging** — his newest paper, and graph-based.
- **Strategic consequence:** a cancer topic framed as *"residue-level binding-site or PTM-site prediction on a cancer-relevant protein family"* lets the student honestly say "this is your method family, extended to a disease area you have not published in" — which scores criterion 1 (novelty, including novelty *within the advisor's own record*) without asking the advisor to supervise a field he does not work in.
- **Risk to name out loud:** the advisor's group has *already* done multi-window CNN + PLM on neoantigens (×2), IL-6 epitopes, protein–peptide sites, RTK ATP sites, and at least five transporter families. Any new "mCNN + PLM on family X" is template application, i.e. weak on criterion 1 unless the method itself changes (criterion 2/3) or the explanation is the contribution (criterion 4).

### Gaps
- The `Ho QT[Author]` initials are ambiguous in PubMed (71 records for the initial form) and I could not disambiguate by ORCID or affiliation in the time available. His solo/other-collaborator publications may therefore include items I have not seen.
- SirtSAGE did not appear in my PubMed queries — it may not be PubMed-indexed (*J Comput Biophys Chem*). I relied on the repo's own record for it.

---

## KQ4 — Cancer tasks that are the SAME SHAPE as the advisor's existing work, on a cancer-relevant protein family

### Takeaway
Three concrete "same shape, cancer-relevant family" formulations exist, and they are ordered by how defensible their data gate is: (A) kinase-group-specific phosphorylation-site prediction on oncogenic signalling kinases using dbPTM's non-homologous benchmark; (B) ATP/nucleotide-binding-site prediction pushed beyond the published SOTA's very poor recall, framed around oncogenic kinases; (C) sequence-level classification of the ABC multidrug-resistance efflux family — maximum advisor fit, but no pre-existing independent test set, so it fails the student's own go/no-go gate as a *primary* topic.

### Cited findings

#### Option A — Phospho-site prediction for oncogenic kinase groups (advisor shape: residue-level windows; cancer relevance: oncogenic signalling)
- dbPTM provides **per-kinase non-homologous benchmark datasets** explicitly built "to evaluate the predictive power for PTM site prediction tools" because cross-validation numbers are not comparable across tools — [FULL, https://biomics.lab.nycu.edu.tw/dbPTM/download.php]. Oncogenic kinase groups present with usable sizes: **CDK, MAPK, PKA, PKC, CK2, AKT, GSK, RSK, PDK1, SGK** (counts in the table under T8).
- Phosphorylation has **1,615,054** experimental sites in dbPTM; ubiquitination **348,307**; acetylation **138,169** — [FULL, same page]. Data arrive with ±10-residue windows.
- Cancer link is quantified: **16–21 %** of known amino-acid substitutions affect PTM sites across pathogenic disease mutations, cancer somatic mutations and population variants, over a base of **>260,000** PTM sites — [ABS, https://academic.oup.com/nar/article/46/D1/D901/4566599].
- Crowding is the lowest of any task with a real benchmark: **14** PubMed records 2024–2026 for DL-based PTM site prediction [FULL, my own query].
- Nearest competitor is recent and uses the student's exact ingredients: an **ESM-2 650M** autoregressive-transformer kinase-substrate site predictor, 5,385 training / 969 validation substrates, with a **14-sample rare-kinase-group test set held fully out of training** — [ABS, https://www.biorxiv.org/content/10.1101/2025.03.12.642740v1.full]. It is a bioRxiv preprint, so the space is not closed.

#### Option B — ATP / nucleotide binding sites, attacking the recall failure, framed on oncogenic kinases
- The published SOTA's own numbers show the gap: PFDCNN **Sn 0.391 (ATP-17)** and **Sn 0.194 (ATP-41)** despite AUC 0.965/0.941 and accuracy 0.990/0.984 — [FULL, https://pmc.ncbi.nlm.nih.gov/articles/PMC12647579/]; code at https://github.com/Yswangustb/PFDCNN.
- The "ATP sites → kinase inhibitors" cancer framing is already accepted in the literature by title: "Residue-Level Multiview Deep Learning for ATP Binding Site Prediction and **Applications in Kinase Inhibitors**" — [TITLE, https://pubmed.ncbi.nlm.nih.gov/39690486/].
- Advisor precedent is exact: "Using multiple convolutional window scanning of CNN for an efficient prediction of **ATP-binding sites in transport proteins**", *Proteins*, 2022 Jul, with QT Ho as co-author — [FULL metadata, PubMed].
- Annotation source is live: BioLiP at `https://zhanggroup.org/BioLiP/` → **HTTP 200** and its download page → **HTTP 200** [LINK-TESTED]. UniProt REST kinase-superfamily query → **HTTP 200** [LINK-TESTED].
- **Caveat the student must state:** RTK_RAG (Ou group, 2025) already did ATP sites on receptor tyrosine kinases — so the *RTK* slice is taken. A different cancer-relevant slice (non-receptor kinases, ABC-transporter NBDs, GTP sites in RAS-superfamily GTPases) is needed for novelty. Note the advisor already has GTP-site papers on Rab GTPases (2019 ×2), and **RAS is the same superfamily as Rab** — "GTP/GDP-binding-site prediction in the RAS superfamily, with KRAS/HRAS/NRAS as the cancer hook" is the tightest same-shape-plus-cancer formulation I found.

#### Option C — ABC multidrug-resistance efflux family classification (maximum advisor fit, weakest data gate)
- Advisor's **mCNN-GenEfflux** (2025 Dec, *Comput Biol Chem*) already classifies **efflux proteins and their superfamilies** with generative proteins + multi-window CNN — [FULL metadata, PubMed]. Cancer link: **ABCB1 (P-gp/MDR1), ABCC1 (MRP1), ABCG2 (BCRP)** are "the major efflux transporters responsible for multidrug resistance in cancer cells" — [ABS, https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7649427/].
- Family size: **49 human ABC proteins in 7 subfamilies (A–G)** — [ABS, same source]. Conserved **LSGGQ** signature in the NBDs, far less conserved TMDs — [ABS].
- Existing ML in this space is compound-side, not sequence-side (MolMM ABCB1 **AUC-ROC 83.33 % inhibitors / 81.26 % substrates**; Pdr5p→human P-gp transfer at **87 %**; SHAP used for motif interpretation) — all [ABS], sources under T14.
- **Blocking issue:** I found **no established independent test set** for sequence-level ABC-family prediction, and 49 proteins is too few. **This fails the student's go/no-go gate.** It can be a *secondary* analysis or a case-study page in the web app, not the primary benchmark.

### Inferences
- The highest-scoring single formulation on *both* advisor fit and novelty is a hybrid: **residue-level site prediction (advisor's exact shape) + a cancer-relevant family the group has not covered + a method change that targets the imbalance/recall failure the SOTA numbers expose + SHAP-style explanation of which window positions and which residues drive the prediction (criterion 4, with BERT-Promoter as in-record precedent) + a per-residue visualisation web app (criterion 5)**. That is four of the five criteria without hand-waving.
- Criterion 3 ("go beyond PLM") has a ready answer inside the advisor's own trajectory: his newest paper replaced mCNN with **GATv2 graph attention gated by AlphaFold pLDDT** (SirtSAGE). A student proposal that says "PSSM → PLM → PLM+retrieval → PLM+structure-gated graph attention, and I will test whether the graph step is what actually helps or whether it is the pLDDT gate" is a direct, flattering extension of his own latest work. **Caution:** AlphaFold structures must be *downloaded* from the AlphaFold DB, never predicted — predicting them is outside the compute budget.
- Option C's weakness is informative: it shows that "maximum advisor fit" and "has an independent benchmark" pull in opposite directions in this field, because the advisor's own papers build their own CD-HIT splits rather than using community benchmarks. The student should expect to argue the gate on *dbPTM's* or *ATP-17/ATP-41's* authority, not on the advisor's precedent.

### Gaps
- I did not search specifically for existing GTP/GDP-binding-site predictors on the RAS superfamily, so I cannot say whether that slice is already taken. **This is the single highest-value follow-up search.**
- I did not establish whether an independent (non-homologous, pre-defined) test set exists for any cancer-relevant transporter or receptor family classification task.

---

## KQ5 — Ranking by (public data with a genuine independent test set) × (contribution room) × (feasibility in 8–9 weeks) × (advisor fit), and explicit rule-outs

### Takeaway
Ranked 1st is kinase-group-specific PTM site prediction (dbPTM); 2nd is residue-level nucleotide-binding-site prediction on a cancer-relevant family not yet covered by the group; 3rd is cancer-gene-restricted variant-effect prediction on the ProteinGym clinical benchmark. Seven candidates should be ruled out outright.

### Cited findings — the ranking
Scores below are **my judgement**, each on 1–5, with the driving evidence named. The product is a decision aid, not a measurement.

| # | Task | Data + independent test set | Contribution room | Feasibility 8–9 wks | Advisor fit | Product | Residue-level? |
|---|---|---|---|---|---|---|---|
| 1 | **PTM sites for oncogenic kinase groups (dbPTM)** — T8 | **5** — dbPTM mirror HTTP 200, per-kinase **non-homologous benchmark** explicitly built for cross-tool comparison [FULL] | **4** — only 14 DL papers 2024–26 [FULL]; nearest competitor is a bioRxiv preprint [ABS] | **5** — pre-windowed ±10 text data, no structures, tiny files | **4** — same residue-level shape; no PTM paper in his record (= novelty) but adjacent to protein–peptide-site work | **400** | **YES — direct reuse** |
| 2 | **Nucleotide-binding sites on a cancer-relevant family (GTP in RAS superfamily / NBDs)** — T14 | **4** — ATP-17/ATP-41 are real independent sets [FULL]; BioLiP + UniProt HTTP 200 [LINK-TESTED]; a RAS-specific set may need building | **5** — SOTA recall is **0.391 / 0.194** [FULL] — a quantified, honest gap | **4** — same pipeline; risk is building a clean cancer-family split | **5** — FAD ×2, ATP-in-transporters, GTP-in-Rab are all his | **400** | **YES — direct reuse** |
| 3 | **Variant effect on cancer genes (ProteinGym clinical)** — T1 | **5** — the only community-standard large independent clinical benchmark; 123 MB clinical zip [FULL README] | **3** — 42 papers 2024–26 [FULL]; AlphaMissense/VESM/ESM-1v are strong (ClinVar auROC ~0.89–0.90) [ABS] | **3** — 1.0 GB + heavy PLM inference; needs a cancer-gene subset to fit Colab | **2** — no variant-effect paper in his record; different output head | **90** | Partially |
| 4 | **Driver vs passenger missense mutation** — T2 | **3** — IntOGen HTTP 200, COSMIC needs registration [LINK-TESTED / NOT VERIFIED]; test sets are tool-specific (CDMPred AUC 0.80 indep.) [ABS] | **4** | **3** — negative-set definition is the leakage trap | **2** | **72** | Partially |
| 5 | **TAA / TTCA prediction** — T7 | **2** — benchmark sets small/heterogeneous; TumorAgDB2.0 and CAD **not link-tested** | **3** | **4** | **3** — same shape as RAG_MCNNIL6, but that is Ou's, not Ho's, and it is neoantigen-adjacent | **72** | No |
| 6 | **MHC class II presentation** — T6 | **4** — IEDB export HTTP 200 [LINK-TESTED]; established benchmarks | **3** — MHC-II "predictors are scarce" [ABS]; OnmiMHC PR-AUC 0.606 [ABS] | **3** | **1** — this is Ou's neoantigen lane, and the student is trying to leave it | **36** | No |
| 7 | **ABC multidrug-resistance family classification** — T14-C | **1** — **no established independent test set found**; only 49 human ABC proteins [ABS] | **3** | **4** | **5** — mCNN-GenEfflux is literally this | **60** | No (protein-level) |
| 8 | **TCR–pMHC binding** — T5 | **5** — IMMREP22/23 is the best benchmark in the list | **2** — field's own verdict: no generalisation to unseen peptides; best macro-AUC₀.₁ **0.60**; winners needed structure [ABS] | **2** — structure modelling is out of compute budget | **1** | **20** | No |
| 9 | **Synthetic lethality** — T13 | **3** — SynLethDB HTTP 200; Nat Commun 2024 benchmark of 11 methods [ABS]; but **9,322 of 35,913 positives are themselves predictions** [ABS] | **3** | **3** | **1** — gene-pair graph, not sequence | **27** | No |
| 10 | **Cancer subtype classification** — T12 | **2** — open TCGA tiers only; richer layers are controlled-access | **2** — 50 papers 2024–26 [FULL] | **3** | **1** | **12** | No |
| 11 | **PPI perturbation ΔΔG** — T9 | **2** — SKEMPI 2.0 / mCSM-PPI2 HTTP 200 but **structure-keyed** | **3** | **2** | **1** | **12** | No |
| 12 | **Kinase inhibitor selectivity** — T11 | **3** — Davis/KIBA/3DKDavis/LSKIBA public | **2** — PDCNet test AUC **0.9213** on 141,086 compounds [ABS]; crowded | **2** — needs a chemistry branch | **1** | **12** | No |
| 13 | **DTI / DTA in oncology** — T10 | **3** — but GDSC bulk URL returned **HTTP 410** [LINK-TESTED]; DepMap HTTP 200 | **1** — **240 papers 2024–26** [FULL] | **2** | **1** | **6** | No |
| 14 | **Driver gene vs passenger gene (T3); oncogene vs TSG (T4)** | **1** — the gold-standard lists *are* the labels; no independent benchmark found | **2** — TP53 "oncogene in disguise" = intrinsic label noise [ABS] | **3** | **1** | **6** | No |

### Explicit RULE-OUTs and the reason for each
1. **DTI / drug-response prediction (T10)** — 240 PubMed records 2024–2026 [FULL, my query]; the GDSC bulk-download URL I tried is **HTTP 410 Gone**; requires a compound-encoding branch the advisor has never published. Crowding + wrong method family.
2. **Kinase inhibitor selectivity (T11)** — the predictive signal lives in the *molecule*, not the protein sequence; strong published baselines (PDCNet test AUC 0.9213 over 141,086 compounds [ABS]). Leaves the advisor's method family entirely.
3. **Cancer subtype classification (T12)** — wrong data modality (bulk omics, not protein sequence); the informative clinical layers are controlled-access, which the brief rules out. Zero reuse of the student's pipeline.
4. **TCR–pMHC binding (T5)** — the benchmark is excellent but the field's own published conclusion is that models **do not beat random on unseen peptides**, and IMMREP23's best entries required structural modelling [ABS]. A 9-week project here most likely reproduces a known failure.
5. **PPI perturbation ΔΔG (T9)** — SKEMPI 2.0 is structure-keyed; sequence-only framing throws away the signal, structure framing exceeds the compute budget; and it is regression, not window classification.
6. **Synthetic lethality (T13)** — gene-pair graph link prediction, no residue-level reuse, and **9,322 of 35,913 "positive" pairs in SynLethDB 2.0 are computational predictions rather than measurements** [ABS] — the labels are partly other models' output.
7. **Driver gene vs passenger gene (T3) and oncogene vs TSG (T4)** — the curated lists (COSMIC CGC, IntOGen, OncoKB) *are* the labels, so no genuinely independent test set exists; N is in the hundreds of genes; and TP53-style dual-function genes make the labels intrinsically noisy [ABS].
8. **Conditional rule-out — ABC multidrug-resistance family classification (T14-C)** — best advisor fit of anything in this report, but **no established independent test set** and only 49 human ABC proteins. Keep it as a *case study inside the web application* or a secondary experiment, **not** as the benchmark the thesis is evaluated on.
9. **Conditional rule-out — MHC class II (T6) and TAA/TTCA (T7)** — both are defensible on data, but both sit inside the immuno-oncology lane the student is explicitly trying to leave, and both are Prof. Ou's territory rather than Prof. Ho's.

### Inferences
- Candidates 1 and 2 tie on my scoring, and they are **combinable**: one thesis can predict two kinds of residue-level functional site (a phospho-site head and a nucleotide-binding-site head) from one shared PLM encoder with multi-task learning — which is itself a method contribution (criterion 2) and has in-field precedent (ESM-NBR uses multi-task learning for nucleic-acid-binding residues [ABS]).
- Whichever is chosen, the five criteria map cleanly: **(1) novelty** = cancer-relevant family the group has not covered; **(2) method** = attack the recall/imbalance failure the SOTA's own Sn figures expose (0.391 / 0.194), e.g. ResiBoost-style residue boosting, focal loss, or separable multi-window CNN; **(3) beyond PLM** = PLM + retrieval (RAG) vs PLM + structure-gated graph attention, i.e. an ablation that tests the advisor's own SirtSAGE claim; **(4) XAI** = SHAP over window positions, with BERT-Promoter as the in-record precedent; **(5) web app** = per-residue score track with an "outside applicable domain" flag, reusing the UI design already drafted for RTK–ATP.
- The leakage-control protocol, metric vocabulary (per-residue MCC/Sn/Sp under extreme imbalance) and applicability-domain idea the student already developed for RTK–ATP all transfer to candidates 1 and 2 **without modification**. Switching to candidate 3 (ProteinGym) would discard most of that.

### Gaps
- The scores in the table are my judgement, not measured quantities; only the bracketed evidence is sourced.
- I could not determine whether a GTP/GDP-binding-site predictor already exists specifically for the RAS superfamily, which is the one fact that would decide between formulation B's variants.
- I could not read Multiview-ATPBind, which is the most direct competitor to formulation B.
- I did not investigate whether dbPTM's distributed window (±10) suffices for multi-window scanning, or whether re-extraction from UniProt is required.
