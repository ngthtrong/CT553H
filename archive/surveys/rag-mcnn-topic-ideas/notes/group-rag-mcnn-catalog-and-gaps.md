# Ou–Ho group (Yuan Ze University / Can Tho University): catalog of RAG / mCNN / msCNN papers 2022–2026 and unexploited gaps for new undergraduate thesis topics

> **LƯU TRỮ — không dùng để ra quyết định.** Tài liệu lịch sử; mọi câu "chốt / quyết định / khuyến nghị" bên dưới đã hết hiệu lực. Trạng thái hiện hành: [DECISIONS.md](../../../../DECISIONS.md).

Scope and method (checked 01/10/2026):
- Publication list: Ou's Google Scholar profile, re-fetched ([Scholar SdzxC9AAAAAJ](https://scholar.google.com/citations?user=SdzxC9AAAAAJ&hl=en&view_op=list_works&sortby=pubdate)). Cross-checked with a PubMed E-utilities query (`Ou YY[Author] AND "Yuan Ze"[Affiliation] AND 2025:2026[dp]` OR `Ho QT[Author] AND "Can Tho"[Affiliation] AND 2024:2026[dp]`), which returned 16 records ([PubMed search](https://pubmed.ncbi.nlm.nih.gov/?term=Ou+YY%5BAuthor%5D+AND+%22Yuan+Ze%22%5BAffiliation%5D)). Ho's list comes from the local scrape `docs/common/advisor/Prof Ho/research.md`.
- Full text: the local PDFs of RTK_RAG, RAG-msCNN, NeoGen-BC, msCNN-PLM-FAD, mCNN-GenEfflux and DeepEpiIL13 were read with PyMuPDF. The PMC full texts of RAG_MCNNIL6, IFNg_DeepKG, CFTR_TL, CaBind_MCNN and RTK_RAG were read through a fetch tool, which returns a model-written summary. Facts from those summaries are tagged "VERIFIED (PMC via fetch summary)" and deserve one manual re-read before anyone quotes them.
- Code: GitHub repos of the lab accounts were read through the GitHub API and raw files. Accounts: B1607, mhb1717, s1129108, juanyuune, s1101404, kioenguyen0207 and **Malik-glt**, a new account found in this pass. The unauthenticated API limit (60 requests/hour) was used up partway through, so file listings for a few repos are incomplete. Those are noted.
- Tags: **VERIFIED** means read directly in the source, or simple arithmetic on numbers printed there. **INFERRED** means my own reasoning. No claims are made about anyone's motives.
- Not repeated as new ideas (already proposed in [bioinformatics-topic-survey.md](../../bioinformatics-topic-survey/bioinformatics-topic-survey.md)): (P1) label-free retrieval plus leakage-proof evaluation for DNA/RNA sites; (P2) ProtGPT2 augmentation vs cheap imbalance baselines plus CLEAN for efflux; (P3) multi-task ATP/FAD/NAD; (P4) motif-validated attribution plus conformal prediction for ATP. Section 6 flags any overlap with these.

---

## Q1. Which RAG variants exist across the group's papers, how do their retrieval designs differ, and which design choices were never ablated?

### Takeaway
There are **10 RAG implementations**: 7 published papers (RTK_RAG, RAG_MCNNIL6, RAG-msCNN, DEEPTRANS, IFNg_DeepKG, metal-binding EAAI 2026, NeoGen-BC) and 3 public but apparently unpublished repos (RAG_CRC, DeepRAGIL-2, and the original RAG_DNA_RNA script). All of them share one core: **top-5 nearest neighbours of a frozen-PLM embedding, mean-pooled, then linearly mixed with the query**. They differ only in four things: granularity (whole padded sequence vs 15-residue window), fusion weight (0.5, 0.7 or 0.9), database source, and in one case knowledge-graph weighting of the neighbours. **k = 5 was never varied in any paper.** The distance metric was never compared, except as an unreported CLI option in DeepRAGIL-2. The database source and composition, and whether to retrieve embeddings or labels, were never ablated. Fusion weight was ablated in only 3 of the 7 papers. Two code/paper mismatches exist, both VERIFIED. First, NeoGen-BC's public script fuses 0.5/0.5 but prints "0.9/0.1". Second, the metal-binding repo's first version (Feb 2025) applied RAG only to positive-labelled windows, like RAG-msCNN; the repo was rewritten to label-free in June 2025.

### Cited Findings

**Per-paper RAG catalog (all VERIFIED unless marked)**

| # | Model (venue, year) | Task / level | Data (train/test, source, redundancy filter) | PLM | Retrieved unit, DB, k, metric, fusion | Head | Headline result | Repo / data availability |
|---|---|---|---|---|---|---|---|---|
| 1 | **RTK_RAG** (JCIM 65(13), 2025) | ATP-binding residues in receptor tyrosine kinases | Train ATP-549 (8,502 binding / 205,035 non-binding residues). 313 RTKs from UniProt went through one CD-HIT 40% run against ATP-549, leaving 69 RTKs as validation/test and 244 as the RAG DB (2,676 binding / 261,088 non-binding) | ProtT5 (ESM-2 1280/2560 and TAPE compared) | **Whole-sequence** L×1×1024 query vs precomputed DB embeddings, "top K" (K not stated in the paper), mean of neighbours, **1:1** with query | mCNN; splitting window 9 had the best AUC 0.9696; dropout 0.9 | Independent 69 RTKs: MCC 0.3181 without RAG → **0.6782** with RAG; AUC 0.9868 | [B1607/RTK_RAG](https://github.com/B1607/RTK_RAG): FASTA + labels for train/test/RAG DB, AFL-3.0 license, Colab. The repo has no RAG-building code ([earlier audit](../../bioinformatics-topic-survey/notes/rag-leakage-audit.md)) |
| 2 | **RAG_MCNNIL6** (JCIM 65(5), 2025) | IL-6-inducing peptides (sequence-level binary) | Train 292+ / 2,393−; validation 73+ / 598−; IEDB + IL6Pred benchmark; the fetch summary found no CD-HIT threshold | ProtTrans (ESM-2, ESM-1b compared) | Whole peptide; DB 9,892 peptides (513+ / 9,379−); top-5; L2 in code; fusion **1:1** | mCNN, windows [2,4,16,24,32,34], 512 filters | Independent MCC 0.6407, AUC 0.9074 | [B1607/RAG_MCNNIL6](https://github.com/B1607/RAG_MCNNIL6); `get_rag_dataset.py` is label-free |
| 3 | **RAG-msCNN** (BSPC 115:109407, 2026; Malik, Hussain, **Ho**, Le, Ou) | DNA (and RNA) binding residues | TR646/TE46; TR573/TE181/TE129; RNA-495/117; CD-HIT 30% | ProtT5 | **15-residue window** embeddings; "RAG-DB ... collecting protein sequences from a curated **RNA-binding protein dataset**", CD-HIT 30%; k = 5, L2; α = 0.7; paper says "exclusively to positive residues" | msCNN (SeparableConv2D) | Paper: MCC 0.91/0.95/0.92. Label-free rewrite in the repo: 0.30/0.40/0.41 (see P1) | [mhb1717/RAG_DNA_RNA](https://github.com/mhb1717/RAG_DNA_RNA) (rar/zip, no license) |
| 4 | **DEEPTRANS** (Chem. Phys. Lett. 882, 2026 (online 2025); Le, Malik, Ou) | Primary active transporters vs other membrane proteins (sequence-level binary) | TCDB-derived. The repo defines **two splits**: random (TrainAll/IndAll) and **temporal** (Until 31-12-2019 → After 01-01-2020) | ProtT5 | Whole sequence padded to 500×1024; L2 over (500,1024); top-5; fusion **0.9 query / 0.1 RAG**; DB "retrieved from TCDB" (search abstract) | msCNN windows 2,4,6,8,10 | "94.78% and 93.06% mean accuracy on two independent test sets" (abstract via search) | [s1129108/DEEPTRANS](https://github.com/s1129108/DEEPTRANS) (found in this pass; the earlier survey said "not located"): data.zip, model.zip, ~13k FASTA, baseline code (SVM/RF/KNN/LSTM/GRU/GNN/attention), `TRAIN_TEST_SPLIT.txt`, web server |
| 5 | **IFNg_DeepKG** (JCIM 66(1), 2026; Le, Yuune, Ou) | IFN-γ-inducing epitopes, human and mouse | Human train 20,394/20,394; Ind1 5,098/5,098; Ind2 5,098/33,946. Mouse train 6,387/6,387; Ind1 1,596/1,596; Ind2 1,596/8,139 | ESM-2 650M (ProtT5, TAPE compared) | Top-5 by L2 from a Neo4j **knowledge-graph DB** (169 inducing / 554 non-inducing, CD-HIT 40% vs train/test). Neighbours weighted by KG relations (host 1.0, source-molecule 0.5, organism 0.6, parent 0.4 for human). Fusion **9:1**; 1:1 and 2:1 "exhibited overfitting" | msCNN, separable kernels (1,2),(1,4),(1,6),(1,8), ~7.32M params | H_Ind1 AUC 0.8889 → 0.9878, MCC 0.8703; M_Ind1 AUC 0.8314 → 0.9510 | [s1129108/IFNg_DeepKG](https://github.com/s1129108/IFNg_DeepKG), AFL-3.0; FASTA for the RAG DB provided |
| 6 | **Metal-binding RAG-PLMs-MetalBind** (EAAI 171:114330, 2026; Malik, Le, Ou) | Metal-binding residues | DB from "1948 non-redundant metal-binding proteins" (abstract via search); RAG-DB array shape (18,986, 15, 1024) | ProtTrans (TAPE, ESM, ProstT5 scripts present) | **15-residue window** (w = 7); top-5 L2; **0.7/0.3**. The current script is label-free ("for statistics only"). The **first version (commit `aa9022f`, 14/02/2025) had `if label[1] == 1: # Apply RAG only on positive samples`**, replaced by a uniform version on 07/06/2025 (`563f333`). The DB builder keeps the lowest-cosine-similarity negatives | **PATN** (positional attention Transformer), not CNN | Acc 85.59%, Spec 85.85%, **Sens 77.29%, AUC 88.10%**; "+52% recall, +7% MCC" over baselines; ">200% relative recall" over bindEmbed21 "despite reduced precision" | [Malik-glt/MetalBind_PATN](https://github.com/Malik-glt/MetalBind_PATN): DataSet.tar.gz, Rag_DataSet.tar.gz, notebooks from the revision (Feb 2026), no license |
| 7 | **NeoGen-BC** (BBRC 836:154567, 2026; Le, Yuune, Lai, Ou) | Neoantigen vs self-antigen peptides (pan-cancer → breast cancer), plus ProtGPT2 generation | CEDAR: 6,516 neo / 377,990 self → CD-HIT 40% → 561/2,823 → length < 35 → 558/2,555; train 446/2,044, test 112/511; external set 25 neo + 49 TAA | ProtT5 (ESM-2, TAPE compared) | Whole peptide; top-5 L2; mean pooling; ratios **2:1, 1:1, 9:1 tested, 9:1 chosen**. **RAG_I** (705 neo / 3,579 other); **RAG_II** homology-purged with CD-HIT-2D vs test (462 / 2,636) | MCNN-BiLSTM | AUC 0.8940 → 0.8712 (CV) and 0.9053 → 0.8790 (independent) when moving RAG_I → RAG_II; PR-AUC 0.6610 under RAG_II | [s1129108/NeoGenBC](https://github.com/s1129108/NeoGenBC), AFL-3.0. **Repo `get_RagEmb_Batch_N.py` computes `(query * 0.5) + (avg_embedding * 0.5)` but prints "Fusing with ratio: Query 0.9 and RAG 0.1"** |
| 8 | **DeepRAGIL-2** (repo only; no journal record found; Yuune, Le, Ou) | IL-2-inducing peptides | IEDB, 3,825 after CD-HIT 40% (738+ / 3,087−), 80:20; test 766 sequences (1:4) | ESM-2 (ProtTrans, Ankh scripts) | Whole peptide (35×1280); top_k = 5; `query_weight` 0.5; **`--metric cosine`** (L2 is an option); separate DB of 3,092 sequences | MCNN windows 8, 16 | Sens 0.7501, Spec 0.9708, MCC 0.7605, AUC 0.8654 | [juanyuune/DeepRAGIL-2](https://github.com/juanyuune/DeepRAGIL-2): IDs only ("can't redistribute the raw sequences"); weights on Google Drive; extra scripts `rag_identity_distribution.py`, `multiseed_exp.py` (seeds 1–10), `mlp_baseline.py`, `stratified_specificity.py` |
| 9 | **RAG_CRC** (repo only; Liu, Chang, Chuang, Ou) | MHC-agnostic colorectal-cancer neoantigen immunogenicity | Experiment set 754 neo / 6,226 general → <40%: 295/307 → train 236/245, test 59/62. RAG DB 3,032 / 120,599 → 1,057 / 5,652 | README says **ProstT5** (structure-aware); the notebook paths read `prottrans` | Whole peptide padded 35×1024; top-5 L2; `(target + avg)/2` = 1:1; DB `CDNO_hybrid.npy` | MC-LSTM (mCNN + BiLSTM) | ROC-AUC 0.8762; 11/13 clinically relevant neoantigens | [B1607/RAG_CRC](https://github.com/B1607/RAG_CRC), LICENSE.txt present |

Sources for the table: [RTK_RAG PDF / PMC12264935](https://pmc.ncbi.nlm.nih.gov/articles/PMC12264935/); [RAG_MCNNIL6 PMC11898070](https://pmc.ncbi.nlm.nih.gov/articles/PMC11898070/) (fetch summary); [RAG-msCNN doi](https://doi.org/10.1016/j.bspc.2025.109407) (local PDF); [DEEPTRANS ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0009261425006384) (abstract via search snippet), [DEEPTRANS RAG script](https://github.com/s1129108/DEEPTRANS/blob/main/CODE/get_RagEmb_Batch_N_new.py), [DEEPTRANS README](https://github.com/s1129108/DEEPTRANS), [TRAIN_TEST_SPLIT.txt](https://github.com/s1129108/DEEPTRANS/blob/main/TRAIN_TEST_SPLIT.txt); [IFNg_DeepKG PMC12801304](https://pmc.ncbi.nlm.nih.gov/articles/PMC12801304/) (fetch summary), [get_RAGKGEmb.py](https://github.com/s1129108/IFNg_DeepKG/blob/main/CODE/get_RAGKGEmb.py); [EAAI abstract page](https://www.sciencedirect.com/science/article/abs/pii/S0952197626006111) (403 on direct fetch; facts from the search-engine abstract), [MetalBind_PATN](https://github.com/Malik-glt/MetalBind_PATN), [get_RagEmb_Batch.py @aa9022f](https://github.com/Malik-glt/MetalBind_PATN/blob/aa9022f/get_RagEmb_Batch.py), [@563f333](https://github.com/Malik-glt/MetalBind_PATN/blob/563f333/get_RagEmb_Batch.py); [NeoGen-BC doi](https://doi.org/10.1016/j.bbrc.2026.154567) (local PDF), [NeoGenBC get_RagEmb_Batch_N.py](https://github.com/s1129108/NeoGenBC/blob/main/get_RagEmb_Batch_N.py); [DeepRAGIL-2](https://github.com/juanyuune/DeepRAGIL-2); [RAG_CRC](https://github.com/B1607/RAG_CRC), [get_rag_dataset.ipynb](https://github.com/B1607/RAG_CRC/blob/main/dataset/get_rag_dataset.ipynb).

**Which design choices were (not) ablated (VERIFIED from the sources above)**
- **k:** always 5 (RAG-msCNN, IL6, IFNg, metal, NeoGen-BC, DEEPTRANS, DeepRAGIL-2, RAG_CRC). RTK_RAG does not state K. No paper reports a sweep over k. The fetch summary of RTK_RAG reports "No ablations ... for K parameter selection", and the RAG_MCNNIL6 summary reports "No explicit ablation of k or database composition" ([PMC12264935](https://pmc.ncbi.nlm.nih.gov/articles/PMC12264935/); [PMC11898070](https://pmc.ncbi.nlm.nih.gov/articles/PMC11898070/)).
- **Fusion weight α:** ablated in RAG_MCNNIL6 (1:1, 1:2, 1:5, 2:1, 5:1 → 1:1), IFNg_DeepKG (9:1 vs 1:1/2:1) and NeoGen-BC (2:1/1:1/9:1 → 9:1, "larger contextual contributions tended to increase overfitting on the independent test set"). Fixed without ablation in RTK_RAG (1:1), RAG-msCNN (0.7), metal (0.7) and DEEPTRANS (0.9). The best α thus runs from 0.5 to 0.9 across tasks, and no paper explains the difference.
- **Distance metric:** L2 everywhere. Only DeepRAGIL-2 exposes `--metric cosine` (its README runs cosine), and no comparison is reported ([RAG_retriever.py](https://github.com/juanyuune/DeepRAGIL-2/blob/main/CODE/RAG_retriever.py)).
- **Granularity:** whole-sequence padded matrices for RTK_RAG, DEEPTRANS (500×1024), the peptide tasks (35×1024 / 35×1280) and RAG_CRC. 15-residue windows for RAG-msCNN and metal. No paper compares the two on the same task. Note that **RTK_RAG is a residue-level task that uses sequence-level retrieval**.
- **DB composition:** only NeoGen-BC reports a homology-purged DB (RAG_II). Elsewhere a single DB is used. RAG-msCNN builds its DNA-task DB from an RNA-binding-protein set. Metal and RAG-msCNN keep only the lowest-cosine negatives at 1.2× positives (`get_dataset_RAG_DB.py`). No paper varies DB size, positive/negative ratio, or in-family vs general DB.
- **What is retrieved:** always neighbour **embeddings**, never neighbour **labels** (no kNN vote or label-weighted mean). The fused vector stays in the same embedding space, a convex combination, as RAG-msCNN states.
- **Retrieval space vs classifier space:** NeoGen-BC built "RAG_I ... separately for each corresponding PLM embedding space" ([NeoGen-BC](https://doi.org/10.1016/j.bbrc.2026.154567)). No paper retrieves in one space (e.g. a structure-aware ProstT5/3Di space) and classifies in another.
- **Threshold selection:** the RAG_DNA_RNA and RTK_RAG notebooks pick the threshold by G-mean on the evaluated set (earlier audit, [rag-leakage-audit.md](../../bioinformatics-topic-survey/notes/rag-leakage-audit.md)). DeepRAGIL-2 ships `multiseed_exp.py` with seeds 1–10. No other repo records seeds.

### Inferences
- INFERRED: the "RAG" family is really one design, a kNN feature-smoothing step, re-tuned per task by hand. A study that **varies k, α, metric, granularity and DB source jointly across several of the group's public datasets** has never been done. It is cheap because embeddings are computed once, and it would stay inside the group's own framework.
- INFERRED: the spread of α (0.5 for IL-6, 0.9 for IFN-γ and NeoGen-BC) together with the "overfitting at high context weight" remark suggests the best α depends on how close the DB is to the test distribution. That is a testable hypothesis: α* vs mean top-k similarity.
- INFERRED: DEEPTRANS's ready-made **temporal split** is the only resource in the group where "RAG lets you add new knowledge without retraining" (the main selling point of RAG in NLP) can be tested directly. Nobody in the group has tested it.

### Gaps
- The DEEPTRANS and metal-binding full texts were not readable (ScienceDirect 403). Their exact DB sizes, ablations and stated limitations are unknown beyond the abstract and the repo.
- Because of the GitHub API rate limit, I could not list every file of RAG_MCNNIL6 / IFNg_DeepKG / NeoGenBC, or check what `DataSet.tar.gz` (≈100 KB) in MetalBind_PATN contains.
- I did not check whether NeoGen-BC's published numbers came from the 0.5/0.5 code path or a 0.9/0.1 one.

---

## Q2. Which tasks has the group done with mCNN/msCNN but NOT with RAG (or vice versa)? Dataset availability for each

### Takeaway
More than 15 published or public mCNN/msCNN tasks have **no RAG variant**. Most are either tiny family-specialised residue tasks, the same shape as RTK_RAG (Ca²⁺ in ion channels: 27 proteins; NADP⁺ in chloroplast: 40; Rab GTP: 131; sirtuin NAD⁺: 52; CFTR ATP: 29), or multi-class transporter-family classification. RAG has never been applied to a **multi-class** task: every RAG paper is binary. In the other direction, several RAG papers swapped out the CNN head (metal → PATN Transformer, NeoGen-BC/RAG_CRC → MCNN-BiLSTM), so "RAG without mCNN" also exists. There has been no controlled comparison of heads under RAG.

### Cited Findings (VERIFIED unless marked)

**mCNN/msCNN tasks without RAG**

| Task (paper) | Level | Data size | Public data? | Source |
|---|---|---|---|---|
| ATP sites, general (ATP_mCNN, CBM 185, 2025) | residue | ATP-388/41/17 (per earlier survey) | FASTA.zip in repo | [s1129108/ATP_mCNN](https://github.com/s1129108/ATP_mCNN); [PubMed 39653625](https://pubmed.ncbi.nlm.nih.gov/39653625/) |
| ATP sites, CFTR via transfer learning (CFTR_TL, ACS Omega 10(47), 2025) | residue | ATP-388 (5,657 / 142,086), ABC transporters 176 (1,842 / 142,578), CFTR 29 (298 / 24,878) | Data/Label.zip + seq.zip | [PMC12676287](https://pmc.ncbi.nlm.nih.gov/articles/PMC12676287/); [B1607/CFTR_TL](https://github.com/B1607/CFTR_TL) |
| Ca²⁺ sites in ion channels/transporters (CaBind_MCNN, JCIM 65(4), 2025) | residue | 155 → 27 proteins (CD-HIT 30%): train 21 (111+ / 22,873−), val 6 (31+ / 3,727−); ChEMBL test 23 (177+ / 23,640−) | FASTA + labels, AFL | [PMC11863380](https://pmc.ncbi.nlm.nih.gov/articles/PMC11863380/); [B1607/CaBind_MCNN](https://github.com/B1607/CaBind_MCNN) |
| NAD⁺ sites in deacetylases/sirtuins (NAD_MCNN, CBDD 105(4), 2025) | residue | General NAD 195 (4,772 / 61,256), sirtuin 7, sirtuin-like 45; total 247 proteins | FASTA + labels (the README table header says "ATP Interacting Residues", a copy slip) | [B1607/SirtuinNAD](https://github.com/B1607/SirtuinNAD) |
| NADP⁺ sites in chloroplast proteins (NADP_mCNN) | residue | train 32 (446 / 14,140), test 8 (134 / 3,403) | FASTA + labels | [s1129108/NADP_mCNN](https://github.com/s1129108/NADP_mCNN) |
| GTP sites in Rab/Ras GTPases (**DeepRabGTPSite**, repo 2026-09; Jhang, Wei, Weng, Chung, Ou) | residue | 1,086 vesicle-trafficking proteins → 131 (<40%): train 104 (1,815 / 44,815), test 27 (446 / 10,218) | FASTA + labels, AFL | [B1607/DeepRabGTPSite](https://github.com/B1607/DeepRabGTPSite) |
| FAD sites (msCNN-PLM-FAD, Anal. Biochem. 713, 2026; Ho's line) | residue | 22,506 → 12,850 samples (BLAST 30%) | Repo holds only a toy subset (earlier survey) | [kioenguyen0207/msCNN-PLM-FAD](https://github.com/kioenguyen0207/msCNN-PLM-FAD) |
| DNA-interacting residues (DIRP / "Deciphering the language of protein-DNA interactions", JMB 436, 2024) | residue | per README | FASTA + labels + ProtTrans files, **≈8.5 GB**, AFL | [B1607/DIRP](https://github.com/B1607/DIRP) |
| Protein–peptide sites (JMGM 130, 2024) | residue | not checked | not checked | Scholar entry in `Prof Ou/research.md` |
| Vesicular transporters (VesiMCNN, IJBM 2024) | sequence | train 658 / 5,908; test 165 / 1,478 | ESM-2 features + FASTA, AFL, Colab | [B1607/Vesicular](https://github.com/B1607/Vesicular) |
| Mitochondrial carriers (MCNN_MC, JCIM 64(24), 2024) | sequence | ~389 FASTA in repo | FASTA | [B1607/MCNN_MC](https://github.com/B1607/MCNN_MC) |
| Ion channels / ion transporters (DeepPLM_mCNN, CBC 110, 2024) | sequence, multi-class | Deep_Ion.zip | FASTA + example embeddings (~945 MB) | [s1129108/DeepPLM_mCNN](https://github.com/s1129108/DeepPLM_mCNN) |
| Sodium transporters (NA_mCNN, JPR 24(5), 2025) | sequence | DataSet.rar | yes | [Malik-glt/DeepSodiumTransporters](https://github.com/Malik-glt/DeepSodiumTransporters); [PMC12053934](https://pmc.ncbi.nlm.nih.gov/articles/PMC12053934/) |
| Amino-acid/peptide transporters within SATs (MCNN-AAPT, JBSD 44(2), 2026) | sequence, multi-class | 484 FASTA | yes | [Malik-glt/MCNN-AAPT](https://github.com/Malik-glt/MCNN-AAPT) |
| Secondary active transporters (Methods 220, 2023) | sequence | 7z archives | yes | [Malik-glt/mCNN-SLC-Membrane](https://github.com/Malik-glt/mCNN-SLC-Membrane) |
| Glucose transporter families (mCNN-glucose, IJBM 294, 2025) | sequence, multi-class | not checked | no repo found | [PubMed 39761890](https://pubmed.ncbi.nlm.nih.gov/39761890/) |
| Cytokine receptors (DeepCR, JBSD 44(10), 2026) | sequence | ~8,322 FASTA + validation.npy + model .h5 | yes | [s1129108/DeepCR](https://github.com/s1129108/DeepCR) |
| IL-13 epitopes (DeepEpiIL13, ACS Omega 10(9), 2025) | peptide | MCC 0.52 / AUC 0.86 benchmark; SARS-CoV-2 set MCC 0.63 | yes (model via Git-LFS) | local PDF; [s1101404/DeepEpiIL13](https://github.com/s1101404/DeepEpiIL13) |
| Melanoma neoantigens (DeepNeoAG, IJBM 281, 2024) | peptide | ~7,012 FASTA | yes | [B1607/DeepNeoAG](https://github.com/B1607/DeepNeoAG) |
| TNF-inducing peptides (DeepTNF, repo 2025-11; ProLLaMA generation for imbalance) | peptide | ProtTrans embeddings in repo | yes | [juanyuune/DeepTNF](https://github.com/juanyuune/DeepTNF) |
| Anti-inflammatory peptides (AIPgen, repo 2026-05; label-noise denoising + ProtGPT2 + BindCraft) | peptide | 9 FASTA splits | yes | [juanyuune/AIPgen](https://github.com/juanyuune/AIPgen) |
| Efflux superfamilies (mCNN-GenEfflux, CBC 2025) | sequence, multi-class | Class A 777/102, B 240/19, C 872/95 | Data.zip | local PDF; [mhb1717/efflux](https://github.com/mhb1717/efflux) (taken by P2) |

**RAG with a non-CNN head:** metal-binding uses PATN, a Transformer ([MetalBind_PATN](https://github.com/Malik-glt/MetalBind_PATN)); NeoGen-BC uses MCNN-BiLSTM; RAG_CRC uses MC-LSTM ([RAG_CRC](https://github.com/B1607/RAG_CRC)); DEEPTRANS's repo includes GNN/attention/LSTM/GRU/SVM/RF/KNN baselines ([TRAIN_TEST_SPLIT.txt](https://github.com/s1129108/DEEPTRANS/blob/main/TRAIN_TEST_SPLIT.txt)).

### Inferences
- INFERRED: RTK_RAG's recipe is "train on a large general ligand set, retrieve from a small family-specific DB, test on that family". It maps one-to-one onto **five mCNN-only family datasets**: Rab-GTP, CFTR/ABC-ATP, Ca²⁺ in channels, NADP⁺ in chloroplast, NAD⁺ in sirtuins. All are public with labels, and every one is small (7–131 proteins), which is exactly where retrieval should matter. RTK_RAG itself asserts that it "offers a generalizable framework adaptable for functional site prediction in other challenging protein families" ([PMC12264935](https://pmc.ncbi.nlm.nih.gov/articles/PMC12264935/)), and nobody has tested that claim.
- INFERRED: RAG has never been tried on a multi-class family task (sodium, AAPT, glucose, ion channel/transporter). For multi-class problems, retrieving **labels** (kNN voting, class-prototype distance) is a natural alternative to retrieving embeddings.

### Gaps
- I did not check dataset sizes or availability for the protein–peptide (JMGM 2024) and mCNN-glucose papers.
- Whether the DIRP DNA set equals the TR646/TR573 benchmarks used in RAG-msCNN was not checked.

---

## Q3. What future-work and limitation statements do these papers make? (verbatim)

### Takeaway
Stated future work is mostly generic: wet-lab validation, larger datasets, other families. **None of the RAG papers names retrieval design (k, α, metric, DB) as future work.** The concrete ML-side items are: RAG-msCNN → NARX/adaptive architectures; msCNN-PLM-FAD → 3D structural embeddings or graph models; CFTR_TL → "different window combination strategies" and "refining the transfer learning approach"; IFNg_DeepKG → KG sparsity for rare pathogens; RAG_MCNNIL6 → predicting the *degree* of IL-6 induction; GenEfflux → imbalance mitigation (taken by P2).

### Cited Findings
- **RAG-msCNN** (VERIFIED, local PDF): "Future research will focus on developing the proposed RAG-msCNN framework to include dynamic and temporal modeling techniques, such as nonlinear autoregressive exogenous (NARX) networks, to better reflect sequential dependencies and residue interaction patterns in protein structures. Furthermore, fractional or adaptive intelligent architectures could be investigated to improve biological interpretability and prediction robustness" — [doi 10.1016/j.bspc.2025.109407](https://doi.org/10.1016/j.bspc.2025.109407).
- **RTK_RAG** (VERIFIED, local PDF; PMC summary says there is no explicit limitations section): "RTK_RAG’s approach establishes a generalizable framework for functional site prediction across other specialized protein families, demonstrating broad applicability beyond RTKs" (Key Point 4) — [doi 10.1021/acs.jcim.5c00766](https://doi.org/10.1021/acs.jcim.5c00766).
- **RAG_MCNNIL6** (VERIFIED, PMC via fetch summary): "Future research should focus not only on epitope identification but also on evaluating the degree of IL-6 induction"; "in vitro and in vivo experiments will be necessary to validate the safety and efficacy" — [PMC11898070](https://pmc.ncbi.nlm.nih.gov/articles/PMC11898070/).
- **IFNg_DeepKG** (VERIFIED, PMC via fetch summary): "a significant limitation is that the number of new epitopes for the knowledge graph is not large enough to fully generalize the model's performance to all novel pathogens. This sparsity of relationships for new or rare pathogens may limit the context vectors' performance in those specific cases." and "Future efforts will be directed toward the experimental validation of generated peptides and the continued expansion of the knowledge graph" — [PMC12801304](https://pmc.ncbi.nlm.nih.gov/articles/PMC12801304/).
- **NeoGen-BC** (VERIFIED, local PDF, §4.3): "the availability of experimentally validated neoantigen datasets remains limited, particularly for specific driver mutations and MHC-II-restricted epitopes ... broader validation on larger and more diverse immunopeptidomics datasets will be essential"; "wet-lab validation remains indispensable"; "Integrating additional layers such as antigen processing efficiency, TCR repertoire availability, and tumor microenvironment context represents a promising direction". It also justifies RAG_I over RAG_II because RAG_I "more closely reflects realistic biological retrieval scenarios in which related immunogenic peptides ... are naturally present within expanding epitope databases" — [doi 10.1016/j.bbrc.2026.154567](https://doi.org/10.1016/j.bbrc.2026.154567).
- **msCNN-PLM-FAD** (VERIFIED, local PDF; Ho's line): "By directly integrating 3D structural embeddings or employing graph-based architectures to explicitly model the residue-residue spatial proximity observed here, future models could establish a generalized framework for deciphering complex structure-function relationships directly from sequence data" — [doi 10.1016/j.ab.2026.116092](https://doi.org/10.1016/j.ab.2026.116092).
- **mCNN-GenEfflux** (VERIFIED, local PDF): "future work will investigate imbalance mitigation techniques such as oversampling and class weighting"; "Future work should incorporate experimental validation ... or structure prediction using tools like AlphaFold"; "Future studies should expand taxonomic coverage" (archaea, fungi) — [doi 10.1016/j.compbiolchem.2025.108595](https://doi.org/10.1016/j.compbiolchem.2025.108595). (Already used by P2.)
- **CFTR_TL** (VERIFIED, PMC via fetch summary): "Future research could focus on investigating the effect of different window combination strategies or refining the transfer learning approach to further optimize performance" — [PMC12676287](https://pmc.ncbi.nlm.nih.gov/articles/PMC12676287/).
- **CaBind_MCNN** (VERIFIED, PMC via fetch summary): "While the initial data set of ion channels and transporters is relatively small (27 sequences after redundancy removal), this is due to the stringent requirement for experimentally validated calcium-binding sites"; "increasing only TP while ignoring FP is not appropriate in drug screening" — [PMC11863380](https://pmc.ncbi.nlm.nih.gov/articles/PMC11863380/).
- **DeepEpiIL13** (VERIFIED, local PDF): calls itself "an incremental step in methodological development within the field of immunoinformatics" — [doi 10.1021/acsomega.4c10960](https://doi.org/10.1021/acsomega.4c10960).
- **Metal-binding EAAI**: the abstract (via search) concedes "reduced precision" in exchange for recall — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0952197626006111). Full limitations text not read.
- **AIPgen** (repo README, VERIFIED): "IEDB-derived AIP training datasets carry a previously unreported label noise problem — 432 sequences (26.5% of the positive pool) appear simultaneously as positive and negative across different experimental records, and IEDB-derived negatives are more similar to positives than positives are to each other in ESM-2 embedding space" — [juanyuune/AIPgen](https://github.com/juanyuune/AIPgen).

### Inferences
- INFERRED: the group's own students have begun auditing data. AIPgen found label conflicts in IEDB; DeepRAGIL-2 added multiseed, identity-distribution and MLP-baseline scripts; NeoGen-BC added a homology-purged DB and PR-AUC. An evaluation-quality topic is therefore *on-trend inside the lab*, not only an external critique. The **IEDB label-conflict check has not been run on the RAG peptide tasks (IL-6, IL-2, IL-13, IFN-γ)**, whose DBs are drawn from the same source.
- INFERRED: "degree of IL-6 induction" (regression/ordinal rather than binary) is an explicit future-work item that nobody has picked up. Feasibility depends on whether IEDB assay records carry quantitative responses, which I did not check.

### Gaps
- DEEPTRANS, metal-binding EAAI, NA_mCNN, NAD_MCNN, ATP_mCNN, DeepCR and MCNN-AAPT limitation sections were not read (paywall, or not fetched within the budget).

---

## Q4. Which repos publish data + code so that a student can reproduce the baseline within about a week?

### Takeaway
The best one-week reproductions are DeepRabGTPSite, CaBind_MCNN, CFTR_TL, RTK_RAG, DEEPTRANS, NeoGenBC, IFNg_DeepKG and DIRP. They have FASTA + labels or the data archive in the repo, a short pipeline (embed → window → train) and, for most B1607/s1129108 repos, an AFL-3.0 license. DeepRAGIL-2 has the most complete *evaluation* code but ships only IDs. msCNN-PLM-FAD and RAG_DNA_RNA are harder (toy data; rar/zip with unclear provenance).

### Cited Findings (VERIFIED from repo listings/READMEs on 01/10/2026)
- **Ready (sequences + labels + code, license):** [DeepRabGTPSite](https://github.com/B1607/DeepRabGTPSite) (per-protein `.label` files for 104 train / 27 test, `MCNN_npy.py`, AFL); [CaBind_MCNN](https://github.com/B1607/CaBind_MCNN) (FASTA + labels, AFL); [RTK_RAG](https://github.com/B1607/RTK_RAG) (862 FASTA, 618 labels incl. RAG DB, AFL; RAG-building code missing, and the notebook imports a missing `import_test_die`); [Vesicular](https://github.com/B1607/Vesicular) (AFL, Colab); [DIRP](https://github.com/B1607/DIRP) (FASTA + labels + precomputed ProtTrans files ≈ 8.5 GB, AFL); [NeoGenBC](https://github.com/s1129108/NeoGenBC) and [IFNg_DeepKG](https://github.com/s1129108/IFNg_DeepKG) (AFL, RAG DB FASTA provided); [RAG_CRC](https://github.com/B1607/RAG_CRC) (LICENSE.txt, RAG notebook).
- **Data present, no license file:** [DEEPTRANS](https://github.com/s1129108/DEEPTRANS) (data.zip, model.zip, trained `.h5`, baselines, temporal split); [CFTR_TL](https://github.com/B1607/CFTR_TL) (Label.zip, seq.zip); [SirtuinNAD](https://github.com/B1607/SirtuinNAD); [ATPirP](https://github.com/B1607/ATPirP) (429 FASTA + labels); [NADP_mCNN](https://github.com/s1129108/NADP_mCNN); [MetalBind_PATN](https://github.com/Malik-glt/MetalBind_PATN) (tar.gz + rar); [DeepSodiumTransporters](https://github.com/Malik-glt/DeepSodiumTransporters); [MCNN-AAPT](https://github.com/Malik-glt/MCNN-AAPT); [DeepCR](https://github.com/s1129108/DeepCR) (includes trained model).
- **Partial:** [DeepRAGIL-2](https://github.com/juanyuune/DeepRAGIL-2): IDs only, sequences must be re-downloaded from IEDB, weights on Google Drive, but it has the best robustness tooling. [msCNN-PLM-FAD](https://github.com/kioenguyen0207/msCNN-PLM-FAD): toy subset only ([earlier survey §4](../../bioinformatics-topic-survey/bioinformatics-topic-survey.md)). [RAG_DNA_RNA](https://github.com/mhb1717/RAG_DNA_RNA): archives with unclear provenance (P1).
- **Compute and disk constraints (VERIFIED repo facts):** per-protein ProtTrans/ESM `.npy` files are 5–8 MB each at L = 500–1000 (Vesicular, DeepPLM_mCNN), and DIRP totals ≈ 8.5 GB. The earlier survey's advice holds: store per-residue embeddings once and window them in the dataloader.

### Inferences
- INFERRED: for any residue-level family topic (Section 6, G1/G2), DeepRabGTPSite + CaBind_MCNN + CFTR_TL + RTK_RAG together give four small, licensed or near-licensed, label-complete datasets. A student could reproduce all four mCNN baselines in under a week on a T4: they total < 1,000 proteins.
- INFERRED: the only repo with a built-in temporal split is DEEPTRANS. The only one with multiseed tooling is DeepRAGIL-2.

### Gaps
- No repo was actually run in this pass. "Reproducible within a week" is an estimate from file contents, not a measured result.
- License status of DEEPTRANS, CFTR_TL, MetalBind_PATN and the Malik-glt repos is "no LICENSE file seen", i.e. all rights reserved by default. Data from them must stay in `data/<slug>/` (git-ignored).

---

## Q5. Any 2025–2026 papers or projects from the group not covered by the earlier survey?

### Takeaway
Scholar and PubMed show **no new published paper** beyond the earlier list as of 01/10/2026. Ou's 2026 entries are still NeoGen-BC, DeepCR, metal EAAI, RAG-msCNN, msCNN-PLM-FAD, MCNN-AAPT and IFNg_DeepKG; Ho's is SirtSAGE. GitHub, however, shows **8+ new or unpublished projects (2025-09 → 2026-09)**, two of them RAG-based: RAG_CRC and DeepRAGIL-2. One is a Ho co-authored msCNN project on mass-spectrometry proteomics (DeepMS-HCC). The earlier survey also missed the public repos of DEEPTRANS and the metal-binding paper.

### Cited Findings
- Scholar re-fetch: same 7 entries for 2026 and 12 for 2025 (VERIFIED) — [Scholar SdzxC9AAAAAJ](https://scholar.google.com/citations?user=SdzxC9AAAAAJ&hl=en&view_op=list_works&sortby=pubdate&pagesize=40). PubMed: 16 records, the newest NeoGen-BC (PMID 42721858, 2 Oct 2026 issue date); no RAG_CRC, DeepRAGIL-2, DeepRabGTPSite or DeepTNF records (VERIFIED for this query only).
- New or unpublished repos (VERIFIED by README and last-update date):
  - **RAG_CRC** (B1607, updated 2025-09-15): RAG + MC-LSTM, ProstT5, MHC-agnostic CRC neoantigens, AUC 0.8762 — [B1607/RAG_CRC](https://github.com/B1607/RAG_CRC).
  - **DeepRAGIL-2** (juanyuune, 2026-09-22): RAG + ESM-2 + MCNN for IL-2, MCC 0.7605 — [juanyuune/DeepRAGIL-2](https://github.com/juanyuune/DeepRAGIL-2). A web search found the repo but no journal version ([search](https://github.com/juanyuune/DeepRAGIL-2)).
  - **DeepRabGTPSite** (B1607, 2026-09-29): mCNN for GTP sites in Rab GTPases, no RAG, MCC 0.8219 — [B1607/DeepRabGTPSite](https://github.com/B1607/DeepRabGTPSite).
  - **GTPase-FuncDiv** (juanyuune, 2026-07): "Evolutionary specialization of the GTPase nucleotide-binding pocket is encoded in protein language model representations". ESM-2 + Ankh variance and mutation experiments; no CNN or RAG — [juanyuune/GTPase-FuncDiv](https://github.com/juanyuune/GTPase-FuncDiv).
  - **AIPgen** (juanyuune, 2026-05): IEDB label-noise denoising + MCNN + ProtGPT2 + BindCraft — [juanyuune/AIPgen](https://github.com/juanyuune/AIPgen).
  - **DeepTNF** (juanyuune, 2025-11): ProLLaMA generative augmentation + ProtTrans + MCNN for TNF-inducing peptides — [juanyuune/DeepTNF](https://github.com/juanyuune/DeepTNF).
  - **DeepMS-HCC** (mhb1717, 2026-09; Hussain, Nguyen Viet Thanh, Nguyen Dinh Quy, Ou, **Ho**): mass-spectrometry peptides + PLM embeddings + MsCNN for HCC prognosis — [mhb1717/DeepMS](https://github.com/mhb1717/DeepMS).
  - mhb1717 also has `ProCoDiff-Edit` (2026-08), `Attn-Omics` (2026-01) and `ReSE-VN-3D` (2025-12). Their READMEs returned 404, so their content is unknown.
  - **SirtSAGE** repo exists ([kioenguyen0207/SirtSAGE](https://github.com/kioenguyen0207/SirtSAGE), updated 2026-05-19), but the README was not retrievable.
  - **Malik-glt** account (new to this survey): repos MetalBind_PATN, DeepSodiumTransporters, mCNN-SLC-Membrane, MCNN-AAPT, all updated 2026-08-27 — [Malik-glt](https://github.com/Malik-glt).

### Inferences
- INFERRED: as of autumn 2026 the lab is active on (a) GTPase nucleotide sites (DeepRabGTPSite, GTPase-FuncDiv), (b) cytokine-inducing peptides with RAG or generation (IL-2, TNF, AIP), and (c) for Ho's side, msCNN outside sequence tasks (MS proteomics) plus graph models (SirtSAGE). A thesis inside (a) or (b) sits closest to what current students are doing. That is good for supervision, but it carries a risk of colliding with an unpublished in-house paper. **Ask the advisors which of these repos are already submitted.**

### Gaps
- Publication status of RAG_CRC, DeepRAGIL-2, DeepRabGTPSite, DeepTNF, AIPgen, GTPase-FuncDiv and DeepMS-HCC is unknown (in review vs abandoned). Ho's Scholar profile was not re-fetched in this pass; I relied on the local scrape.

---

## Q6. Concrete unexploited gaps a student could turn into a RAG- and/or CNN-centred topic (excluding P1–P4)

### Takeaway
Seven candidate gaps (G1–G7) survive the de-duplication check. The strongest are **G1** (does RTK_RAG's family-retrieval recipe transfer to the group's other small family datasets, and does it beat CFTR_TL-style transfer learning?), **G2** (does retrieval with a growing DB substitute for retraining on newer proteins, using DEEPTRANS's temporal split?) and **G3** (one systematic retrieval-design benchmark, k/α/metric/granularity/DB, across the group's peptide RAG tasks). All three reuse public lab data, need little GPU and little biology, and extend the group's framework rather than critiquing a specific paper.

### Cited Findings → gap derivation (facts VERIFIED above; each gap statement is INFERRED)

**G1. Family-specialised retrieval vs transfer learning for small binding-site families.** INFERRED gap, high confidence that it is untested.
- Evidence: RTK_RAG (general ATP-549 train + 244-RTK DB) raised MCC 0.32 → 0.68 and claims generality to "other specialized protein families" ([PMC12264935](https://pmc.ncbi.nlm.nih.gov/articles/PMC12264935/)). CFTR_TL solved the same "small family" problem with transfer learning (ATP-388 → ABC 176 → CFTR 29) and lists "refining the transfer learning approach" as future work ([PMC12676287](https://pmc.ncbi.nlm.nih.gov/articles/PMC12676287/)). DeepRabGTPSite (131 proteins), CaBind_MCNN (27 + 23), NADP_mCNN (40) and SirtuinNAD (7 sirtuin + 45 sirtuin-like) are mCNN-only.
- Possible RQ: on ≥ 3 family datasets (Rab-GTP, CFTR-ATP, Ca²⁺-channel, possibly RTK as positive control), compare (a) the mCNN baseline, (b) transfer learning, (c) RTK_RAG-style retrieval from an in-family DB, (d) retrieval from a general DB, (e) TL + RAG. Measure AUPRC/MCC at a validation-chosen threshold.
- Overlap check: P3 is multi-task over ligands and P4 is ATP explanations. G1 is about **family specialisation by retrieval vs TL**, so there is no duplication. Retrieval must be label-free at query time (lesson from P1), but that is a protocol detail, not the topic.
- Risk: DeepRabGTPSite may be unpublished in-house work, so check with the advisor first. Tiny test sets (27 proteins / 446 positives for Rab) give wide confidence intervals.

**G2. "Update the DB, not the model": retrieval under temporal shift.**
- Evidence: the DEEPTRANS repo has a pre-2020/post-2020 split ([TRAIN_TEST_SPLIT.txt](https://github.com/s1129108/DEEPTRANS/blob/main/TRAIN_TEST_SPLIT.txt)) and a TCDB-based DB. NeoGen-BC argues that RAG suits "expanding epitope databases" but never tests DB growth ([NeoGen-BC](https://doi.org/10.1016/j.bbrc.2026.154567)). IFNg_DeepKG's own limitation is DB sparsity for new pathogens ([PMC12801304](https://pmc.ncbi.nlm.nih.gov/articles/PMC12801304/)).
- Possible RQ: with the classifier frozen after training on ≤ 2019 data, how much of the gap to a retrained model on post-2020 proteins is closed by adding post-2020 (non-test) entries to the retrieval DB? Plot the gain vs DB size and vs top-k similarity. This works for DEEPTRANS (sequence level). It could be repeated on IFN-γ (KG growth) if time allows.
- Overlap: none with P1–P4. It is the core NLP-RAG claim and has never been tested in this lab. Low GPU: embeddings once, then re-fusion only.
- Risk: post-2020 TCDB entries may be few, or very similar to the old ones. Check counts in `data.zip` first (not done).

**G3. One retrieval-design benchmark across the lab's peptide RAG tasks (IL-6, IL-2, IFN-γ, neoantigen, plus IL-13/TNF without RAG).**
- Evidence: k fixed at 5 everywhere; α is 0.5/0.9/0.9 with partial ablations; L2 vs cosine never compared; embeddings vs labels never compared; homology-purged DB only in NeoGen-BC (Q1). The NeoGen-BC repo/paper α mismatch shows the setting is fragile (VERIFIED).
- Possible RQ: across 4–6 public peptide datasets, does the optimal (k, α, metric) transfer between tasks, and does a **learned gate** (α predicted from the query–neighbour similarity) or **label-retrieval** (kNN vote / neighbour positive fraction as an extra feature) beat a fixed α? Report everything under a homology-purged DB (NeoGen-BC's RAG_II protocol) with multiseed (DeepRAGIL-2's script).
- Overlap: P1 includes "learned attention vs α" but only for **DNA/RNA residues**. G3 is peptide-level and multi-task, so the overlap is partial. Present G3 as the peptide-domain counterpart, or merge the two if the advisor prefers.
- Risk: IEDB sequences must be re-downloaded (DeepRAGIL-2 has IDs only), and the label-conflict issue (AIPgen) may confound results. That leads to G4.

**G4. IEDB label-conflict audit for retrieval-augmented peptide classifiers.**
- Evidence: AIPgen found 26.5% of the AIP positive pool appears as both positive and negative, and that IEDB negatives sit closer to positives than positives to each other in ESM-2 space ([AIPgen](https://github.com/juanyuune/AIPgen)). The IL-6, IL-2, IL-13 and IFN-γ datasets and RAG DBs are all IEDB-derived (Q1/Q2).
- Possible RQ: what fraction of each IL-x/IFN-γ train, test and RAG-DB entry has conflicting labels, or exact or near duplicates across splits? How much does retrieval gain change after conflict removal? Does retrieval *amplify* noise, i.e. are retrieved neighbours disproportionately conflicting entries?
- Overlap: different data domain from P1, but same "evaluation hygiene" family. Politically softer, because the precedent comes from the lab's own student (AIPgen). Low GPU.
- Risk: it is data-centric, so the advisor may see it as thin unless paired with G3.

**G5. Structure-aware retrieval space with a sequence-space classifier.**
- Evidence: retrieval and classification always share one PLM space (NeoGen-BC builds a DB per PLM). RAG_CRC already reaches for ProstT5. Ho's FAD paper names "3D structural embeddings or graph-based architectures" as future work ([msCNN-PLM-FAD](https://doi.org/10.1016/j.ab.2026.116092)). External context: retrieval inside PLMs is active (e.g. [RAG-ESM, bioRxiv 2025](https://www.biorxiv.org/content/10.1101/2025.04.02.646805.full.pdf); not read in detail).
- Possible RQ: for a residue task (G1 families or the metal set), retrieve neighbours by ProstT5/3Di (Foldseek-style) similarity but fuse ProtT5 embeddings. Does structural retrieval beat sequence-embedding retrieval when sequence identity to the DB is low?
- Overlap: none with P1–P4. Risk: higher engineering cost (ProstT5 3Di generation is sequence-only, so no folding needed; INFERRED from the ProstT5 design in the earlier notes), and a moderate novelty claim.

**G6. Retrieval for multi-class transporter-family tasks.**
- Evidence: every RAG paper is binary. The sodium, AAPT, ion channel/transporter, SAT and glucose-family tasks are mCNN-only and multi-class (Q2).
- Possible RQ: on MCNN-AAPT or DeepPLM_mCNN data, compare mCNN, mCNN + embedding-RAG, and label-retrieval (kNN / class prototypes). Measure per-class MCC and macro-F1 on the rare classes.
- **Overlap warning:** close to P2's CLEAN-style metric learning (efflux). Only take this if the dataset and the claim differ: retrieval-augmentation, not metric learning, on a non-efflux family. Otherwise it is a duplicate.

**G7. Controlled head comparison under RAG (mCNN vs msCNN vs BiLSTM vs Transformer).**
- Evidence: RAG papers changed the head and the RAG at the same time (metal → PATN, NeoGen-BC → MCNN-BiLSTM, RAG-msCNN → msCNN), so the head's contribution is confounded. msCNN-PLM-FAD is the only paper with a statistical test (Welch p = 0.0466 vs single-window CNN) ([earlier notes](../../bioinformatics-topic-survey/notes/advisor-landscape-and-trends.md)).
- Possible RQ: with fixed label-free RAG features, which head gives the best AUPRC per parameter across 3–4 public tasks?
- **Overlap warning:** P3 already includes "is mCNN still useful under LoRA". G7 is the frozen-embedding, under-RAG version. It is weak as a standalone thesis, so use it as a chapter inside G1 or G3.

**Not recommended / already covered:** RAG for FAD (data not public; the FAD part of P3 already faces this); NARX/"fractional adaptive" architectures from RAG-msCNN's future work (no clear ML question, weak fit, INFERRED); regression on "degree of IL-6 induction" (attractive and explicitly stated as future work, but quantitative IEDB labels were not verified to exist, so check before considering).

### Inferences
- INFERRED ranking by novelty-per-risk for an IT student with unverified biology background:
  1. **G2**: cleanest novel question, least biology, one dataset with a built-in split.
  2. **G1**: high fit with the lab's current GTPase/family work, four public labelled datasets, a natural "new named model". Risk of colliding with in-house work.
  3. **G3 (+ G4 as a chapter)**: broadest, uses the most lab repos, partial overlap with P1's design-comparison idea.
  4. **G5**: interesting, but more engineering.
  5. **G6 / G7**: chapter-level only, because of overlap with P2/P3.
- INFERRED: every gap should inherit three protocol rules from the earlier audit: label-free retrieval at query time, a homology-purged DB (CD-HIT-2D vs test, as in NeoGen-BC's RAG_II), and validation-chosen thresholds with multiple seeds. Presented as "the protocol", these keep the work constructive and away from re-litigating RAG-msCNN.

### Gaps
- None of G1–G7 has been checked against the post-2024 external literature as thoroughly as P1–P4 were. A targeted prior-work search is still needed for "retrieval vs transfer learning for protein families" (G1), "retrieval database update under temporal shift, protein" (G2) and "label noise IEDB cytokine peptide" (G4).
- Whether the lab already has unpublished work on G1 (DeepRabGTPSite is fresh) or G3 (DeepRAGIL-2 has robustness scripts) can only be answered by the advisors.
- The post-2020 class counts in DEEPTRANS (G2 feasibility) were not checked: `data.zip` was not downloaded.
