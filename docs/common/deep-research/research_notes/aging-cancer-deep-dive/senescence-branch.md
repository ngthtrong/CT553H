# Cellular senescence prediction from protein sequence — SenSeqNet benchmark stress-test

> Research notes for topic selection (CT553H), compiled 2026-10-02. Verification markers used throughout:
> **[FULL TEXT]** = read the full text of the source; **[ABSTRACT ONLY]**; **[NOT VERIFIED]**; **[OWN MEASUREMENT]** = I downloaded the file and computed the number myself (command output preserved in session, files fetched from GitHub raw on 2026-10-02).
>
> **Two different versions of SenSeqNet exist and they disagree with each other.** Keep them apart in any write-up:
> - **v1 = bioRxiv preprint** `10.1101/2024.10.28.620702` (v1/v2): CD-HIT 0.4, 238,634/217,696 → 24,914/28,752, accuracy **83.55%**.
> - **v2 = published Aging Cell 2026** `10.1111/acel.70344`: MMseqs2 0.3, 292,759/373,098 → 43,381/32,673, accuracy **86.43%**.
> The 238,634 / 217,696 figures in the research brief are the **preprint** numbers, not the published ones.

---

## Q1. SenSeqNet: task, architecture, reported metrics, baselines

### Takeaway
SenSeqNet is a binary sequence-level classifier (senescence-associated protein vs not) built from ESM-2 mean-pooled embeddings fed to a BiLSTM → CNN head. Published accuracy is 86.43% on a 20% split that the paper calls "independent testing"; there is **no separately constructed independent test set with both classes**. Architecture novelty is low and it is a close cousin of the advisor's own PLM→CNN family.

### Cited Findings
- Published paper: Jiang et al., "SenSeqNet: A Deep Learning Framework for Cellular Senescence Detection From Protein Sequences", *Aging Cell*, 2026; DOI 10.1111/acel.70344; PubMed 41432347; PMC12724000. First published online 23 December 2025, issue dated January 2026 — [PMC12724000](https://pmc.ncbi.nlm.nih.gov/articles/PMC12724000/) **[FULL TEXT, via PMC]**; [Wiley DOI](https://onlinelibrary.wiley.com/doi/full/10.1111/acel.70344) returned **HTTP 403 Forbidden** to automated fetch (Wiley paywall/bot block) — use PMC.
- Task: classify a protein sequence as senescence-associated (positive) or non-senescent (negative); whole-sequence binary classification, **not** residue-level — [PMC12724000](https://pmc.ncbi.nlm.nih.gov/articles/PMC12724000/) **[FULL TEXT]**
- Final embedding: `ESM-2_t33` — 33 layers, 650M parameters, 1280-dim embeddings; downstream head = Bidirectional LSTM → CNN — [PMC12724000](https://pmc.ncbi.nlm.nih.gov/articles/PMC12724000/) **[FULL TEXT]**
- Verbatim: "The ESM‐2_t33 model achieved the highest accuracy at 86.43%, outperforming the other variants." and "SenSeqNet achieved the highest accuracy of 86.43%, an AUC of 0.94, and an MCC of 0.7221." — [PMC12724000](https://pmc.ncbi.nlm.nih.gov/articles/PMC12724000/) **[FULL TEXT]**
- Full published metric set: Accuracy 86.43%, Sensitivity 90.51%, Specificity 81.01%, F1 88.38%, MCC 0.7221, AUC 0.94 — [PMC12724000](https://pmc.ncbi.nlm.nih.gov/articles/PMC12724000/) **[FULL TEXT]**
- Preprint metrics (different dataset): independent-test accuracy **83.55%**, AUC 0.92, cross-validation accuracy 83.28% ± 0.58% — [bioRxiv v2 full text](https://www.biorxiv.org/content/10.1101/2024.10.28.620702v2.full) **[FULL TEXT]**
- Baselines beaten (published): deep learning — CNN, RNN, LSTM, BiLSTM, CNN-LSTM, pLSTM-CNN (parallel CNN-LSTM); classical ML — Logistic Regression, Random Forest, XGBoost, SVM, Bagging; alternative PLMs — ProtTrans, ProteinBERT, ESM-1b, ESM-1v — [PMC12724000](https://pmc.ncbi.nlm.nih.gov/articles/PMC12724000/) **[FULL TEXT]**
- **No XAI of any kind.** Verbatim limitation in the paper: "a key limitation of this study is the model's interpretability, particularly in identifying biologically significant motifs within protein sequences." — [PMC12724000](https://pmc.ncbi.nlm.nih.gov/articles/PMC12724000/) **[FULL TEXT]**
- **No web server / web application.** The paper mentions only the GitHub repo. The repo README offers a PyPI package (`pip install senseqnet`), a CLI (`senseqnet-predict --fasta ... --device cuda`) and a Colab demo notebook (https://colab.research.google.com/drive/1e9lMOIIvppdpAYRy7LUYUPh2xpzpp8cr) — [README](https://raw.githubusercontent.com/HanliJiang13/SenSeqNet/HEAD/README.md) **[FULL TEXT]**
- Committed v2 feature-extraction notebook hard-codes `ESM_MODEL = 'esm2_t6_8M_UR50D'` (the 8M model), not t33/650M; long sequences are chunked at `MAX_RESIDUES_PER_CHUNK = 1000` and chunk embeddings averaged into one per-sequence vector — [All_code_v2/ESM2_features.ipynb](https://github.com/HanliJiang13/SenSeqNet/blob/HEAD/All_code_v2/ESM2_features.ipynb) **[FULL TEXT of notebook]**

### Inferences
- The representation is a **single mean-pooled vector per protein** (1280-d). A BiLSTM and CNN applied on top of one pooled vector (or on top of a short chunk-sequence) cannot be learning real amino-acid order; the "sequential + spatial features" framing is weaker than it sounds. This is a concrete methodological opening.
- The ESM-2 size discrepancy (paper: t33 650M; committed notebook default: t6 8M) means the public code as committed does **not** reproduce the headline number without editing. Phrase this carefully: it may simply be that the committed default was left at the cheap model used for debugging. Do **not** claim the paper's numbers are fabricated.
- Because there is no XAI and no web app, those two of the advisor's five criteria are *unclaimed territory* on this benchmark.

### Gaps
- Supplementary tables (Table S3 = the negative gene list) were not retrievable: the Wiley site 403s automated requests, and PMC's rendering did not expose the supplement contents. The exact 148-gene negative list and the exact 163+47 positive gene list are **not verified** from the supplement; they are partly reconstructible from the GitHub FASTA headers (see Q2).

---

## Q2. THE CENTRAL QUESTION — how did a few hundred genes become ~240,000–290,000 sequences?

### Takeaway
**Answer: per-gene-name queries against UniParc, not UniProtKB.** Each senescence gene symbol was used as a text query to pull every UniParc record matching that symbol — all species, all isoforms, all fragments, all source-database copies — and every returned sequence inherited the gene's label. I confirmed this directly from the FASTA headers in the repo, which literally read `Seq_uniparc_PEX19.xlsx_2`, `Seq_TUBB4A共207条.xlsx_33`, `Sequence_56_uniparc_CDK5R1_AND_database_facet_100_2024_11_26`. The published paper says "UniProtKB" and **never mentions UniParc**.

### Cited Findings
- Published positive genes, verbatim: "163 high‐confidence senescence‐inducing genes" from CellAge + "47 additional in vivo‐supported senescence signature genes" from SASP Atlas, SenMayo and SenPy (genes present in ≥2 sources) = "210 senescence‐associated genes" — [PMC12724000](https://pmc.ncbi.nlm.nih.gov/articles/PMC12724000/) **[FULL TEXT]**
- Published negative genes, verbatim: "148 non‐senescent genes" representing "cytoskeletal maintenance, housekeeping and ribosomal functions, cell cycle and proliferative signaling, programmed cell death (apoptosis), core metabolic processes, and receptor‐mediated signaling" — [PMC12724000](https://pmc.ncbi.nlm.nih.gov/articles/PMC12724000/) **[FULL TEXT]**
- Published raw counts, verbatim: "The initial dataset of 292,759 positive and 373,098 negative protein sequences was clustered using MMSeqs2 … with an identity threshold of 0.3." Retrieved "from UniProtKB, including all isoforms." — [PMC12724000](https://pmc.ncbi.nlm.nih.gov/articles/PMC12724000/) **[FULL TEXT]**
- Preprint raw counts, verbatim: "a dataset comprising 238,634 positive and 217,696 negative protein sequences"; "Protein sequences related to cell senescence were downloaded from the Universal Protein Knowledgebase (UniProtKB)" — [bioRxiv v2](https://www.biorxiv.org/content/10.1101/2024.10.28.620702v2.full) **[FULL TEXT]**
- **FASTA headers prove UniParc, not UniProtKB.** First headers of `Data/Protein_sequences_cdhit_0.4/positive_0.4.fasta`: `>Seq_uniparc_PEX19.xlsx_2`, `>Seq_uniparc_PEX19.xlsx_4`, … Negative file: `>Seq_TUBB4A共207条.xlsx_33`, `>Seq_uniparc_ADRB2.xlsx_122`. External set: `>Sequence_56_uniparc_CDK5R1_AND_database_facet_100_2024_11_26` — [repo raw files](https://github.com/HanliJiang13/SenSeqNet/tree/HEAD/Data) **[OWN MEASUREMENT]**
- Headers contain **no UniProt accession, no organism field (`OS=`), no gene field (`GN=`)** — I grepped for `OS=` and `GN=` and got zero matches in both v1 files. The only provenance kept is the gene-symbol filename and a row index — **[OWN MEASUREMENT]**
- `共207条` is Chinese for "207 entries in total", i.e. the filename of a per-gene spreadsheet export of UniParc search results. `_AND_database_facet_100_` in the external-set headers is a UniParc/UniProt **search-facet** string, confirming the data came from web-UI search exports — **[OWN MEASUREMENT / inference from the literal strings]**
- **Gene-level composition of the v1 positive set (I parsed all 24,914 headers):** 149 distinct gene symbols. Top: CKB 4,894; SYK 3,482; AAK1 2,294; DAO 1,784; TOM1 1,494; ATR 1,483; MOS 718; CDC6 706; HIRA 555; EHF 492. **Top 5 genes = 56.0% of all positive sequences.** — **[OWN MEASUREMENT]**
- **Gene-level composition of the v1 negative set (28,752 headers):** 82 distinct gene symbols. Top: VIM 4,694; TF 4,588; IGH 4,520; GH1 2,481; BPI 2,083; LEP 1,999; TNF 1,991; MICA5 1,634; FERR 916; FTH1 562 — **[OWN MEASUREMENT]**
- **147 of the 149 v1 positive gene symbols are CellAge build-3 genes with `Senescence Effect = Induces`** (I cross-joined against the downloaded `cellage3.tsv`). The two non-matches, `KLF46` and `MEOX16`, are almost certainly my regex clipping a trailing digit off `KLF4`/`MEOX1` followed by a Chinese count suffix — treat them as parsing artifacts, not as real genes — **[OWN MEASUREMENT]**
- Sequence lengths in the v1 sets: positives min 39 / median 352 / max 10,251 residues; negatives min 38 / median 309.5 / max 10,210 — **[OWN MEASUREMENT]**

### Inferences
- **The mechanism is label propagation from gene symbol to every homolog/variant/fragment in UniParc.** UniParc is the non-redundant *archive* of every sequence from every source database (including TrEMBL, patents, model-organism databases, and obsolete records) across **all organisms**. A text query on a human gene symbol therefore returns orthologs from hundreds of species plus partial fragments plus patent sequences. That — not isoform expansion in human — is how ~210 genes become ~290,000 sequences (≈1,400 sequences per gene).
- **Consequence: the labels are gene-family labels, not senescence labels.** Any model trained on this can reach high accuracy by solving "which of these ~230 gene families does this sequence belong to?", a task PLM embeddings solve almost trivially. The biology claim ("detects senescence from sequence") does not follow from the measurement.
- **Internal arithmetic inconsistency between the two versions, worth pointing out to the advisor:** v1 clustered 238,634 positives at the *looser* CD-HIT 0.4 threshold and kept 24,914 (10.4%); v2 clustered 292,759 positives at the *stricter* MMseqs2 0.3 threshold and kept 43,381 (14.8%). A stricter identity threshold retaining 1.74× more representatives is not possible on the same data unless the coverage parameters differ sharply (MMseqs2 `easy-cluster` defaults to `-c 0.8`, so length-discordant fragments form their own clusters, whereas CD-HIT's default `-aL/-aS` behaviour differs). This is a strong hint that the v2 "representative" set is inflated by **fragments**, and that fragments of the same protein family survive as separate "representatives".
- Even granting the clustering, **43,381 mutually <30%-identical representatives cannot come from 210 gene families**. Real orthologous families collapse hard at 30% identity. 43,381 clusters implies either (a) the queries pulled in large numbers of unrelated proteins, or (b) coverage settings let fragments escape clustering. Either way the positive class is not "the 210 senescence genes".

### Gaps
- I could not confirm the exact UniParc/UniProt query string used (the header fragment `_AND_database_facet_100_2024_11_26` is suggestive but the full query is not recorded anywhere in the repo or paper). **Not found.**
- I could not count v2's gene-level composition: `Data_v2/Data_v2.zip` is a **Git LFS pointer** (`oid sha256:e643ab726797e441097a2c83aea5905bb151a336b9a186f62608da6debc78908`, declared size **1,414,069,895 bytes ≈ 1.41 GB**), too large to pull in this session. The v2 feature notebook shows the v2 FASTA headers *do* carry a parsed `gene=` field (`META_KEYS = ['source','gene','entry','file','idx']`), so the same analysis is reproducible by a student who downloads the LFS object.

---

## Q3. Was any redundancy removal done, and does it prevent leakage? (the single most important question)

### Takeaway
**Yes, redundancy removal WAS done — this part of the brief's hypothesis is wrong.** v1 used CD-HIT at 0.4; the published v2 used MMseqs2 at 0.3, and the paper explicitly says this was "to avoid data leakage". **But the protection is defective in three independent ways**, and one of them is catastrophic and fully verified: in the v1 release, **94.8% of the "external validation" negative sequences are byte-identical duplicates of training negatives**, and **100% of the external-negative genes (26/26) are already training-negative genes**. The split is a plain random `train_test_split`, never a gene-level/group split, even though gene labels are present in the headers.

### Cited Findings — what the papers say (verbatim)
- Published v2, verbatim: "MMSeqs2 (Steinegger and Söding [2017]) with an identity threshold of 0.3. This clustering procedure yielded a final representative dataset … Only these representative sequences were used for subsequent model training and validation to avoid data leakage" — [PMC12724000](https://pmc.ncbi.nlm.nih.gov/articles/PMC12724000/) **[FULL TEXT]**
- Published v2, verbatim: "This clustering procedure yielded a final representative dataset of 43,381 positive and 32,673 negative sequences." — [PMC12724000](https://pmc.ncbi.nlm.nih.gov/articles/PMC12724000/) **[FULL TEXT]**
- Published v2 split, verbatim and **complete** — this is the entirety of what the paper says about splitting: "The dataset was divided into a training set (80%) and a validation set (20%) for model development." The paper **does not state** whether the split is random, stratified, or grouped — [PMC12724000](https://pmc.ncbi.nlm.nih.gov/articles/PMC12724000/) **[FULL TEXT]**
- Preprint v1, verbatim: "we employed CD-HIT with a threshold of 0.4, ultimately leaving 24,914 positive and 28,752 negative sequences"; "The dataset will be divided into a training set (80%) and a validation set (20%)" — [bioRxiv v2](https://www.biorxiv.org/content/10.1101/2024.10.28.620702v2.full) **[FULL TEXT]**
- There is **no separately constructed two-class independent test set**. The published v2 external validation is **positives only**: "26 senescence‐related genes were collected from these datasets, and their corresponding protein sequences were processed using the same UniProtKB retrieval"; 52,227 sequences; "SenSeqNet classified 40,502 of these 52,227 sequences as senescence‐associated, achieving a true positive rate of 77.55%". Sources: GSE13330 and GSE63577 (human fibroblasts, in vitro) and SenCID (in vivo) — [PMC12724000](https://pmc.ncbi.nlm.nih.gov/articles/PMC12724000/) **[FULL TEXT]**
- The paper makes **no statement** that this external set was clustered or filtered against the training set — [PMC12724000](https://pmc.ncbi.nlm.nih.gov/articles/PMC12724000/) **[FULL TEXT]**

### Cited Findings — what I measured myself on the released v1 files
All four files downloaded from `https://raw.githubusercontent.com/HanliJiang13/SenSeqNet/HEAD/...` on 2026-10-02, all **HTTP 200**, no registration, no LFS needed:

| File | bytes | sequences (`grep -c '^>'`) | unique sequence strings |
|---|---|---|---|
| `Data/Protein_sequences_cdhit_0.4/positive_0.4.fasta` | 12,403,805 | **24,914** | 24,914 |
| `Data/Protein_sequences_cdhit_0.4/negative_0.4.fasta` | 13,355,846 | **28,752** | 28,752 |
| `Data/External_validation_dataset/clustered_external_positive.fasta` | 6,103,151 | **16,524** | 16,524 |
| `Data/External_validation_dataset/clustered_external_negative.fasta` | 2,230,618 | **6,443** | 6,443 |

Counts 24,914 / 28,752 **exactly match the preprint's stated numbers** — **[OWN MEASUREMENT]**

- **Exact-duplicate sequence overlap (byte-identical amino-acid strings), training set vs external validation set:**
  - training negatives ∩ external negatives: **6,110 sequences** — that is **94.83% of the 6,443 external negatives**
  - training positives ∩ external positives: 4 sequences
  - **cross-label** contradictions: training positives ∩ external negatives = 12; training negatives ∩ external positives = 5
  - **within the training set itself**, training positives ∩ training negatives = **16 identical sequences carrying both labels** — **[OWN MEASUREMENT]**
- **Gene-level overlap, training vs external:**
  - external negatives come from **26 gene symbols** — `ARPC1B, ARPC2, B2M, DES, EZR, FLNA, FLNB, GAPDH, HPRT1, KRT1, KRT8, MAP1B, MAP2, MAPT, MSN, MYH10, MYH9, NEFH, NEFL, NEFM, PFN1, PPIA, RDX, RPLP0, RPS18, VIM` — and **all 26 of 26 also appear in the training negative set**. The external negative half is, gene-for-gene, a resample of the training negatives.
  - external positives come from **13 gene symbols** — `ARF1, ARID1A, ARID1B, BIN1, BNIP3L, CASP2, CDK5R1, DMTF1, E2F7, ENTPD7, FASN, HBP1, HIPK2` — and **0 of 13 overlap the training positive genes** (this half is genuinely held out at gene level)
  - `ARPC1B` is a **positive-labelled gene in training** and simultaneously a gene in the **external negative** set — a direct label contradiction — **[OWN MEASUREMENT]**
- **Composition of the external positive set is pathological:** `BIN1` contributes 12,135 of 16,524 sequences and `HBP1` contributes 3,909. **Top 2 genes = 97.1% of the external positives.** The external negative set is likewise 4,985/6,443 = 77.4% `VIM` alone — **[OWN MEASUREMENT]**
- **No gene-level/group split anywhere in the code.** The v2 training notebook imports `from sklearn.model_selection import train_test_split` and, for cross-validation, `from sklearn.model_selection import KFold` — **never** `GroupKFold`, `StratifiedGroupKFold` or any grouping by gene, despite the v2 FASTA headers carrying a `gene=` field that the feature notebook parses (`META_KEYS = ['source','gene','entry','file','idx']`). `random_seed = 42` throughout — [All_code_v2/SenSeqNet.ipynb](https://github.com/HanliJiang13/SenSeqNet/blob/HEAD/All_code_v2/SenSeqNet.ipynb), [All_code_v2/ESM2_features.ipynb](https://github.com/HanliJiang13/SenSeqNet/blob/HEAD/All_code_v2/ESM2_features.ipynb) — **[OWN MEASUREMENT / FULL TEXT of notebooks]**
- v2 clustering was done **separately per class**: the feature notebook reads `reps_30_rep_seq_pos.fasta` and `reps_30_rep_seq_neg.fasta` (the `*_rep_seq.fasta` suffix is MMseqs2 `easy-cluster` output naming, confirming MMseqs2 at 30%). Clustering each class independently does nothing to stop a positive and a negative being near-identical — and indeed v1 has 16 exactly-identical cross-label pairs — [All_code_v2/ESM2_features.ipynb](https://github.com/HanliJiang13/SenSeqNet/blob/HEAD/All_code_v2/ESM2_features.ipynb) **[OWN MEASUREMENT]**

### Inferences
- **Three distinct, nameable defects.** Frame the critique this way rather than "they forgot CD-HIT", which would be false:
  1. **Gene-level (group) leakage in the main split.** Clustering at 30–40% identity removes *near-duplicate pairs* but does not remove *gene-family membership*. A random 80/20 split therefore puts representatives of the same gene family on both sides. The task degenerates into gene-family recognition. The fix is a `StratifiedGroupKFold` grouped by gene symbol — cheap, and the group labels are already in the headers.
  2. **The v1 "external validation" negative half is a copy of the training negatives** — 94.8% exact duplicates, 26/26 gene overlap. Whatever specificity was reported on it is meaningless. This is the hardest, most checkable finding in these notes.
  3. **Class-asymmetric clustering plus a positives-only external test in v2.** The published external validation reports only a true-positive rate (77.55%) over 52,227 sequences from 26 genes; with no negatives there is no specificity, no MCC, no AUC, so "external testing" cannot support the "outperforms" claim.
- **Extra defect: concentration.** With 56% of training positives from 5 genes and 97% of external positives from 2 genes, both the headline and the external number are effectively single-gene measurements with enormous variance. Reporting per-gene (leave-one-gene-out) performance would almost certainly collapse the numbers.
- **A fair re-evaluation is cheap and fits in 8–9 weeks.** The v1 data is 34 MB of FASTA and downloads in seconds; ESM-2 8M/35M embeddings for ~54,000 sequences are feasible on Colab free tier (the authors' own notebook defaults to the 8M model and runs on Colab). So this benchmark can be rebuilt honestly without GPU risk.

### Gaps
- I verified duplicate/gene overlap on the **v1** release only. The **v2** dataset is behind a 1.41 GB Git LFS object I did not pull, so I **cannot state** whether the published v2 external set repeats the v1 duplication defect. The paper's silence on filtering the external set, and the "same UniProtKB retrieval" wording, make it plausible but **unconfirmed** — say so explicitly in any write-up. A student should download `Data_v2/Data_v2.zip` and repeat my three checks (exact-duplicate overlap, gene overlap, per-gene concentration) as day-one work.
- I did not find the exact MMseqs2 command line (coverage `-c`, `--cov-mode`, `--cluster-mode`) anywhere in the paper or the notebooks. **Not found** — this matters because it determines whether fragments escaped clustering.

---

## Q4. The GitHub repository — contents, licence, accessibility

### Takeaway
`https://github.com/HanliJiang13/SenSeqNet` resolves (HTTP 200), is public, needs no registration, and is unusually complete for a bioinformatics paper — v1 and v2 code, v1 FASTA data, the external validation set, trained weights, and a packaged PyPI wheel. **But it has no LICENSE file at all** (GitHub licence API returns 404), and the most important files — the v2 dataset, the original unclustered data, and the 650M-parameter embeddings — are **Git LFS pointers**, one of which is 1.41 GB.

### Cited Findings
- Repo URL `https://github.com/HanliJiang13/SenSeqNet` — resolved, public, repo id 877516477, owner `HanliJiang13`, `"private": false`, `"description": null` — [GitHub API](https://api.github.com/repos/HanliJiang13/SenSeqNet) **[OWN MEASUREMENT]**
- **Licence: none.** `https://api.github.com/repos/HanliJiang13/SenSeqNet/license` → **HTTP 404**; no LICENSE file in the tree. Legally this means "all rights reserved" by default; reuse of the data for a thesis should be described as academic fair use plus citation, and the student should email the author (contact given in README: `hhanli.jiang@mail.utoronto.ca`) — **[OWN MEASUREMENT]**
- Commit history (last 10): most recent **2025-12-27T01:22:59Z** "update"; also 2025-12-27, 2025-12-25, two on 2025-11-12, then a January-2025 cluster (2025-01-14 "Update README.md", 2025-01-13 ×3). So v2 artefacts were pushed Nov–Dec 2025, aligning with the 23 Dec 2025 online publication — **[OWN MEASUREMENT]**
- Directory tree (sizes are git blob sizes in bytes; `~133` indicates a Git LFS pointer file, not the real content):
  - `All_code/` — 11 notebooks, v1: `SenSeqNet.ipynb` 31,066; `pCNNLSTM.ipynb` 26,632; `CNN.ipynb` 17,259; `BiLSTM.ipynb` 15,306; `LSTM.ipynb` 14,987; `ML_models.ipynb` 12,575; `CNN_LSTM.ipynb` 10,944; `Figures.ipynb` 19,709; `RNN.ipynb` 15,306; `ESM2_features.ipynb` 3,008; `Manu_features.ipynb` 4,142
  - `All_code_v2/` — same 11 notebooks, v2: `SenSeqNet.ipynb` 36,532; `pCNNLSTM.ipynb` 30,847; `Figures.ipynb` 23,377; `ESM2_features.ipynb` 10,252; …
  - `Data/Protein_sequences_cdhit_0.4/` — `positive_0.4.fasta` 12,403,805 B, `negative_0.4.fasta` 13,355,846 B — **real files, directly downloadable**
  - `Data/External_validation_dataset/` — `clustered_external_positive.fasta` 6,103,151 B, `clustered_external_negative.fasta` 2,230,618 B, `external_features.npy` 17,593,088 B, `external_labels.npy` 73,432 B — **real files**
  - `Data/ESM2_features/` — `esm_features_35M.npy.zip` 95,823,748 B and `esm_features_8M.npy.zip` 63,897,082 B are real; `esm_features_150M.npy.zip` and `esm_features_650M.npy.zip` are **LFS pointers (134 B)** — i.e. the embeddings for the model the paper actually reports are not directly downloadable
  - `Data/Original_data/` — `positive.zip`, `negative.zip` both **LFS pointers (133 B)**: the unclustered raw data is LFS-only
  - `Data_v2/Data_v2.zip` — **LFS pointer, declared size 1,414,069,895 B (1.41 GB)**
  - `Models/SenSeqNet/SenSeqNet_LSTMCNN_model` 14,728,343 B (real); `Models/SenSeqNet_v2/SenSeqNet_model.pth` 19,362,056 B (real); six baseline `.pth.zip` files are LFS pointers
  - `SenSeqNet/dist/` — `senseqnet-1.1.0-py3-none-any.whl` 49,771,651 B, `senseqnet-1.1.0.tar.gz` 49,700,749 B, `senseqnet-1.1.1-py3-none-any.whl` 49,772,707 B
  - `.gitattributes` (42 B) = `*.zip filter=lfs diff=lfs merge=lfs -text`
  — [GitHub trees API](https://api.github.com/repos/HanliJiang13/SenSeqNet/git/trees/HEAD?recursive=1) **[OWN MEASUREMENT]**
- `.DS_Store` files are committed in `Data/`, `Data/ESM2_features/`, `Data/Manu_features/`, `Models/` — macOS artefacts, a minor housekeeping signal — **[OWN MEASUREMENT]**
- **Preprocessing scripts for dataset construction are absent.** There is no script that performs the UniParc retrieval, the CD-HIT/MMseqs2 call, or the train/test split export. The notebooks start from already-clustered FASTA files (`reps_30_rep_seq_pos.fasta`) that are not in the repo at that path — **[OWN MEASUREMENT]**

### Inferences
- **Data access verdict: GO, with a caveat.** The v1 benchmark (34 MB of FASTA, both classes, plus an external set) downloads today with no registration — this clears the data go/no-go gate that killed the previous candidate topic, *provided* the student is content to work on the v1 release or to pull the 1.41 GB v2 LFS object once.
- The absence of any data-construction script is itself a finding: the dataset is **not reproducible from the repo**, only re-usable as-is. Writing that missing pipeline (UniProt query → clustering → gene-grouped split, all scripted and seeded) is a legitimate, concrete deliverable.
- No LICENSE is a real practical issue for a thesis that redistributes a corrected dataset. Recommend: redistribute only accession lists plus the scripts, not the sequences.

### Gaps
- I did not test whether the Git LFS objects actually download anonymously (LFS bandwidth quotas on free GitHub accounts can make `git lfs pull` fail with "bandwidth exceeded"). **Untested** — this is the one real data-access risk and the student should test it in the first hour.
- The PyPI package `senseqnet` and the Colab demo link were not executed. **Untested.**

---

## Q5. CellAge and GenAge — exact counts, versions, licence, downloadability

### Takeaway
All verified by direct download, no registration: **CellAge Build 3 (23 April 2023) = 866 genes** from genetic manipulations (949 gene–experiment rows, of which only **417 rows / 370 distinct genes are "Induces"**), plus a separate 1,259-gene expression signature. **GenAge Build 21 (28 August 2023) = 307 human genes and 2,205 model-organism genes.** These numbers are exactly what makes the ~240,000–290,000 sequence figure impossible to reach from human genes alone.

### Cited Findings
- `https://genomics.senescence.info/cells/cellAge.zip` → **HTTP 200**, 21,540 bytes, no registration. Contains `cellage3.tsv` (73,627 B, file mtime 22 Apr 2023) and `release.html` — **[OWN MEASUREMENT]**
- CellAge Build 3 release notes, verbatim: "Release date: April 23, 2023 / Number of genes inferred from genetic manipulations: 866 / Number of genes from expression changes: 1,259" and "Build 3 represents a significant update. The number of manually-curated genes associated with cellular senescence has more than tripled compared to the previous build." — [cellAge.zip → release.html](https://genomics.senescence.info/cells/cellAge.zip) **[FULL TEXT]**
- `cellage3.tsv` contents, counted by me: **949 data rows**, **866 distinct gene symbols** (matching the release note). Columns: `Entrez ID, Gene symbol, Gene name, Cancer Cell, Type of senescence, Senescence Effect, Reference`.
  - `Senescence Effect`: **Inhibits 510, Induces 417, Unclear 22** rows → **370 distinct genes with "Induces"**
  - `Type of senescence`: Unclear 363, Oncogene-induced 242, Stress-induced 188, Replicative 156
  - `Cancer Cell`: No 487, Yes 462
  — **[OWN MEASUREMENT]**
- `https://genomics.senescence.info/genes/human_genes.zip` → **HTTP 200**, 9,465 B; contains `genage_human.csv` (22,778 B, mtime 9 Feb 2020) with **307 gene rows**; columns `GenAge ID, symbol, name, entrez gene id, uniprot, why` — **[OWN MEASUREMENT]**
- `https://genomics.senescence.info/genes/models_genes.zip` → **HTTP 200**, 48,796 B; `genage_models.csv` (214,711 B, mtime 3 Oct 2023) with **2,205 rows**; columns include `organism, avg lifespan change (max obsv), lifespan effect, longevity influence` — **[OWN MEASUREMENT]**
- GenAge Build 21 release notes, verbatim: "Release date: August 28, 2023 / Number of genes in model organisms: 2,205 / Number of human genes: 307". Build 21 is "a data update" with a signature of "449 genes overexpressed with age and 162 genes underexpressed" — [human_genes.zip → release.html](https://genomics.senescence.info/genes/human_genes.zip) **[FULL TEXT]**
- Parent resource: Human Ageing Genomic Resources (HAGR), `https://genomics.senescence.info/`, maintained by the Genomics of Ageing and Rejuvenation Lab (João Pedro de Magalhães). Sibling databases on the same portal: GenDR, LongevityMap, DrugAge, AnAge, Digital Ageing Atlas — [HAGR download page](https://genomics.senescence.info/download.html) **[FULL TEXT]**
- Download formats: CellAge as a zipped tab-delimited file; GenAge as "Zipped tab-delimited ASCII files" (actually CSV) — [HAGR download page](https://genomics.senescence.info/download.html) **[FULL TEXT]**
- Licence: "Use of the CellAge is free but subject to the conditions of the Human Ageing Genomic Resources"; HAGR licence text lives at `https://genomics.senescence.info/legal.html`. Required CellAge citation: Avelar, R. A., Ortega, J. G., Tacutu, R., et al. (2020) "A multidimensional systems biology analysis of cellular senescence in aging and disease." *Genome Biology* 21(1):91. Required GenAge citation: Tacutu R, Thornton D, Johnson E, et al. (2018) "Human Ageing Genomic Resources: new and updated databases." *Nucleic Acids Research* 46(D1):D1083–D1090 — [release notes in both zips](https://genomics.senescence.info/cells/cellAge.zip) **[FULL TEXT]**
- Broken URLs I tried, for the record: `cells/cellAge3.zip` → **404**; `cells/signatures.zip` → **404**; `cells/signatures1.zip` → **404**; `cells/CellAge_signatures.zip` → **404**. The working CellAge gene file is `cells/cellAge.zip`. The expression-signature file's URL was **not found** — it must be reached through the "Search signatures" page — **[OWN MEASUREMENT]**

### Inferences
- **The arithmetic that nails the critique:** CellAge Build 3 has only **370 distinct "Induces" genes**; SenSeqNet used 163 of them plus 47 others = 210 genes. 292,759 positive sequences / 210 genes ≈ **1,394 sequences per gene**. No human gene has 1,394 isoforms. The expansion is necessarily cross-species homologs and fragments from UniParc. This single ratio is the cleanest way to present the finding to the advisor.
- Note the deliberate exclusion: CellAge's **510 "Inhibits" rows are used in neither class**. Senescence *inhibitors* are arguably the most informative hard negatives available, and discarding them while using VIM/GAPDH/tubulins as negatives is exactly the trivially-separable-negatives problem.
- Data availability for a thesis is clean: HAGR files are small, versioned, dated, downloadable without registration, with explicit citation requirements. Low go/no-go risk.

### Gaps
- The HAGR `legal.html` licence page content was not fully extracted (the fetched page was dominated by the site navigation menu); I could not confirm whether HAGR uses a named licence such as CC-BY-NC. Report as "free use subject to HAGR conditions, specific licence name **not found**".
- CellAge's own breakdown into inducers/inhibitors is per **gene–experiment row**, not per gene, and genes can appear with both effects. My "370 distinct Induces genes" is computed on distinct symbols with at least one Induces row; the count of genes that are *exclusively* inducers was not computed.

---

## Q6. The negative set: "housekeeping genes" and why that choice inflates accuracy

### Takeaway
The negative set has **no named source database** — not HRT Atlas, not Eisenberg & Levanon's housekeeping list, not any citation. It is a hand-picked list of 148 genes (Table S3) chosen by functional category, and the genes I recovered from the released FASTA are structural/secreted proteins (VIM, TF, IGH, GH1, BPI, LEP, TNF, tubulins, keratins, neurofilaments, actin-related) that are separable from kinases and transcription factors on **protein-family grounds alone**, with no reference to senescence.

### Cited Findings
- Published paper: the negatives are described only functionally — "genes involved in cytoskeletal maintenance, housekeeping and ribosomal functions, cell cycle and proliferative signaling, programmed cell death (apoptosis), core metabolic processes, and receptor‐mediated signaling", selected to represent "non‐senescent physiological or proliferative cellular conditions", with the list in Table S3. **No source database is named.** — [PMC12724000](https://pmc.ncbi.nlm.nih.gov/articles/PMC12724000/) **[FULL TEXT]**
- Preprint: "protein sequences from housekeeping genes were selected as negative samples"; the preprint **does not specify which database** provided them — [bioRxiv v2](https://www.biorxiv.org/content/10.1101/2024.10.28.620702v2.full) **[FULL TEXT]**
- Negative gene symbols I recovered from `negative_0.4.fasta` headers (82 distinct; top by sequence count): VIM 4,694; TF (transferrin) 4,588; IGH (immunoglobulin heavy) 4,520; GH1 (growth hormone) 2,481; BPI 2,083; LEP (leptin) 1,999; TNF 1,991; MICA5 1,634; FERR 916; FTH1 562. External negatives add: TUBB4A, ADRB2, EZR, NEFL, NEFM, NEFH, MAP2, MAPT, MAP1B, MYH9, MYH10, FLNA, FLNB, MSN, RDX, DES, KRT1, KRT8, PFN1, ARPC1B, ARPC2, B2M, GAPDH, HPRT1, PPIA, RPLP0, RPS18 — **[OWN MEASUREMENT]**
- `IGH` as a negative class member is notable: immunoglobulin heavy-chain records in UniParc number in the tens of thousands and are an extremely distinctive, highly repetitive sequence family — 4,520 of the 28,752 negatives (15.7%) — **[OWN MEASUREMENT]**
- `ARPC1B` appears as a **positive** gene in training and as an **external negative** gene — the same gene on both sides of the label — **[OWN MEASUREMENT]**

### Inferences
- **Why this inflates accuracy:** the two classes differ by *protein family*, not by senescence status. Positives are dominated by kinases and DNA-damage/cell-cycle proteins (SYK, AAK1, ATR, CDK5R1, CDC6, HIPK2, MOS, E2F7); negatives are dominated by cytoskeletal filaments, immunoglobulins, secreted hormones and ribosomal proteins. An ESM-2 embedding separates those families almost by construction. 86.43% accuracy is therefore consistent with a model that knows nothing about senescence.
- **Specific falsifiable test a student can run in days:** train a classifier on *amino-acid composition only* (20 features, no PLM). If it reaches anywhere near 86%, the benchmark is demonstrably family-separable rather than senescence-informative. This is the cheapest possible "trivially separable negatives" demonstration and it needs no GPU.
- **The missing hard negatives are obvious and free:** CellAge's 510 "Inhibits" rows (≈ senescence-*inhibiting* genes), and GenAge's 307 human ageing genes that are not in CellAge. A benchmark whose negatives are senescence inhibitors rather than vimentin is a genuinely harder and biologically meaningful task — and building it is a **positive contribution**, not an audit.
- An honest negative set should also be **family-balanced** against the positives (match kinase/TF/structural proportions), which is a concrete, writable methods section.

### Gaps
- Table S3, the authoritative 148-gene negative list, was **not retrieved** (Wiley 403; PMC did not expose supplements to the fetcher). My 82 + 27 recovered symbols are from the released v1 FASTA and are a partial reconstruction, not the official list.
- Whether the authors intended HRT Atlas v1.0 or the Eisenberg–Levanon list is **not found** — neither paper cites a housekeeping-gene source at all.

---

## Q7. Prior and competing work — is sequence-based senescence/ageing prediction crowded or open?

### Takeaway
**Sequence-only senescence prediction is near-empty — SenSeqNet appears to be the only method, and nothing cites it yet.** But the adjacent problem, *ageing*-gene prediction, is a 2018–2026 literature that is mostly **network/annotation-feature based**, and at least one 2025–2026 paper already does **ESM-2 + LoRA for ageing-related human proteins**. So the branch is open but not virgin, and the strongest prior art to position against is the ageing-gene side.

### Cited Findings
- I found **no paper citing SenSeqNet**. Searches returned only the paper itself across Wiley/PubMed/PMC/bioRxiv/ResearchGate mirrors; the only other new hit was an unrelated transcriptomics paper, "SenSet defines cell-type specific senescence signatures in the aged human lung", *EMBO J*-family, DOI 10.1038/s44318-026-00762-8 — [search results](https://pubmed.ncbi.nlm.nih.gov/41432347/) **[ABSTRACT ONLY / search-level]**
- Fernandes et al. (2018), "Prediction and characterization of human ageing-related proteins by using machine learning", *Scientific Reports* 8:4938 — extracted ~21,000 protein features from multiple databases, labelled proteins ageing-related vs not using **GenAge**; found a simple model using **36 features** (e.g. "number of aging-related interaction partners", "response to oxidative stress", "damaged DNA binding", "rhythmic process", "extracellular region"); most predictive features were curated GO/pathway annotations, least predictive were expression/co-expression — [Nature SR](https://www.nature.com/articles/s41598-018-22240-w) / [PMC5840292](https://pmc.ncbi.nlm.nih.gov/articles/PMC5840292/) **[ABSTRACT + search-level summary, not full text]**
- "Fine-Tuning ESM2 for Predicting Ageing-Related Human Proteins", Springer book chapter, DOI 10.1007/978-3-032-13048-8_26 — fine-tunes ESM-2 with **LoRA** for binary classification of ageing-related proteins — [Springer](https://link.springer.com/chapter/10.1007/978-3-032-13048-8_26) **[TITLE + search-snippet ONLY; the page 303-redirects to Springer's IdP and could not be fetched. Authors, year, dataset size, metrics and code availability: NOT VERIFIED]**
- Network-based ageing-gene prediction line: "Supervised prediction of aging-related genes from a context-specific protein interaction subnetwork" ([arXiv 1908.08135](https://arxiv.org/pdf/1908.08135)) and "Towards future directions in data-integrative supervised prediction of human aging-related genes" ([PMC9710570](https://pmc.ncbi.nlm.nih.gov/articles/PMC9710570/)) — both use PPI-network features, not sequence — **[ABSTRACT / search-level]**
- "Genome-wide prediction and prioritization of human aging genes by data fusion: a machine learning approach" ([PMC6842548](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6842548/)) — data-fusion approach, not sequence-only — **[ABSTRACT / search-level]**
- Dietary/caloric-restriction gene prediction on GenAge/GenDR: Barardo-style work, "Machine learning-based predictions of dietary restriction associations across ageing-related genes", *BMC Bioinformatics* 2021 ([Springer](https://link.springer.com/article/10.1186/s12859-021-04523-8), [PMC8729156](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8729156/)) — **[ABSTRACT / search-level]**
- Senescence *detection* methods named in the SenSeqNet paper as data sources, all transcriptomics not sequence: SenCID, SenMayo, SenPy, SASP Atlas — [PMC12724000](https://pmc.ncbi.nlm.nih.gov/articles/PMC12724000/) **[FULL TEXT]**

### Inferences
- **Crowding verdict: the sequence-only senescence niche has exactly one occupant and zero citations.** That is both the opportunity (criterion 1, novelty) and the risk (no competing numbers to beat, so "I improved SOTA" is a one-paper comparison, and the advisor may read a single-paper field as thin).
- The ESM-2+LoRA ageing-protein chapter is the most dangerous overlap: if a student's plan is "fine-tune ESM-2 for senescence", that is one word away from an already-published chapter. The defensible differentiator is **the benchmark and the evaluation protocol**, plus a method the ageing papers do not use.
- The ageing literature's strongest finding — that curated GO/pathway and interaction features dominate, while expression features are weakest — is a warning that *sequence alone* may carry little senescence signal. That is a legitimate research question to pose honestly rather than a reason to avoid the topic: "how much of SenSeqNet's 86% is sequence-family identity versus senescence biology?" is a real, answerable RQ.

### Gaps
- Could not verify any numbers for the ESM-2+LoRA ageing chapter (paywall/IdP redirect). Its dataset size, metrics, and whether it does gene-level splitting are **not found** — a student must obtain it (institutional access or author request) before claiming novelty against it.
- No citation count for SenSeqNet obtained (too recent; Google Scholar not queried). Report as "no citing papers found as of 2026-10-02", not as "zero citations".

---

## Q8. What a single student could defensibly attack in 8–9 weeks, against the advisor's five criteria

### Takeaway
There is a strong thesis here, but **only if the audit is the setup and not the contribution** — the student's previous topic failed for exactly that reason. The defensible shape is: *build the corrected senescence benchmark (SenBench), then propose a method that the corrected benchmark makes necessary*, specifically a gene-family-invariant model with an applicability-domain output and SHAP/attention explanation, delivered as a web app. That hits 4–5 of the five criteria.

### Cited Findings (the facts that make this feasible)
- v1 data is 34 MB total and downloads in seconds with no registration (measured sizes in Q4) — **[OWN MEASUREMENT]**
- The authors' own pipeline runs on **Colab**: the v2 feature notebook sets `PROJECT_ROOT = Path('/content')`, defaults to `esm2_t6_8M_UR50D`, batches at `MAX_TOKENS_PER_BATCH = 2000`, and the README links a Colab demo — so no local GPU is required — [All_code_v2/ESM2_features.ipynb](https://github.com/HanliJiang13/SenSeqNet/blob/HEAD/All_code_v2/ESM2_features.ipynb), [README](https://raw.githubusercontent.com/HanliJiang13/SenSeqNet/HEAD/README.md) **[FULL TEXT]**
- Gene identity needed for a grouped split is already present: v1 headers carry the gene symbol in the filename; v2 headers carry an explicit `gene=` field — **[OWN MEASUREMENT]**
- SenSeqNet has **no XAI** (its own stated limitation) and **no web application** — [PMC12724000](https://pmc.ncbi.nlm.nih.gov/articles/PMC12724000/) **[FULL TEXT]**
- CellAge supplies 510 unused "Inhibits" rows and GenAge 307 human ageing genes, all downloadable, as ready-made hard negatives — **[OWN MEASUREMENT]**

### Inferences — the proposal shape, mapped to the five criteria

**Deliverable 1 (sets up everything, ~2 weeks): SenBench — a gene-grouped senescence benchmark.**
- Re-derive sequences with recorded, scripted queries (fix the UniParc/UniProtKB ambiguity by choosing UniProtKB reviewed + a declared taxonomy scope, e.g. human only or human+mouse, instead of all-species UniParc).
- `StratifiedGroupKFold` grouped by **gene symbol**, so no gene family spans train and test; plus a genuinely held-out two-class independent test set of whole gene families.
- Hard negatives from CellAge "Inhibits" + GenAge, family-balanced against positives.
- Deduplicate across classes and across splits; report the three leakage metrics I used (exact-duplicate overlap, gene overlap, per-gene concentration) as benchmark QC numbers.
- Report SenSeqNet's published weights (`Models/SenSeqNet_v2/SenSeqNet_model.pth`, 19.4 MB, directly downloadable) **on SenBench** — this is the audit, but it is now one table, not the thesis.

**Deliverable 2 (the positive method contribution, ~3 weeks) — criteria 2 and 3.**
Options, strongest first:
- **Family-invariant / family-adversarial training:** add a gene-family (or Pfam-family) discriminator with a gradient-reversal layer, or a family-balanced contrastive loss, so the model is penalised for encoding family identity. This is *directly motivated* by the defect found, which is the cleanest possible story: "the old benchmark let the model cheat by recognising families; here is a model that is explicitly prevented from doing so". Novel for this task, cheap to train on pooled embeddings.
- **Multi-window / multi-scale CNN (mCNN/msCNN) over per-residue ESM-2 embeddings instead of a mean-pooled vector.** SenSeqNet throws away positional information by mean-pooling; the advisor's own mCNN family is built for exactly this. This is a safe, on-brand criterion-2 contribution ("CNN → mCNN") and the advisor will recognise it immediately.
- **Going beyond PLM (criterion 3), cheaply:** the advisor's newest work (SirtSAGE) uses ESM-2 + GATv2 with AlphaFold pLDDT gating. For senescence, the honest cheap version is to add **AlphaFold DB pre-computed** structures (download, no prediction) for the human proteins only and build a residue-contact-graph GNN. Flag the risk: AlphaFold DB coverage is per-UniProt-accession, and the current benchmark headers have **no accessions**, so this only works after Deliverable 1 restores accessions, and only for the human subset. If the human subset is small (hundreds of proteins), a GNN may overfit — treat as a stretch goal, not the core.
- **Applicability-domain output:** report max sequence identity (or embedding distance) from the query to the training set alongside each prediction, so the web app can say "this prediction is outside the training domain". Low cost, and it carries forward the one genuinely good idea from the student's abandoned RTK–ATP topic without repeating the audit-only mistake.

**Deliverable 3 (criterion 4, XAI, ~1.5 weeks).**
- SHAP over the embedding dimensions is weak and uninterpretable. Better: **attention/attribution back onto residues** (integrated gradients or attention rollout on per-residue ESM-2 features), then test whether high-attribution regions overlap known senescence-relevant domains/motifs (e.g. CDK-inhibitor domains, p53/Rb interaction regions, DNA-damage-response kinase domains) using InterPro/Pfam annotations.
- The advisor has an explicit explainability precedent (BERT-Promoter 2022 used SHAP), so SHAP-on-features can be the fallback if residue attribution proves fiddly.
- A second, cheaper XAI angle that doubles as evidence for the leakage story: **show which gene families drive confident predictions**, i.e. explain the *old* model's success as family recognition. This is XAI serving the scientific argument, not decoration.

**Deliverable 4 (criterion 5, mandatory, ~1.5 weeks).**
- Web app: paste/upload FASTA → prediction + calibrated probability + applicability-domain warning + residue attribution heatmap + nearest training gene families. Spring Boot + React front end with a FastAPI `ml-service` holding the exported model, matching the repo conventions already in CT553H. Note that SenSeqNet has **only** a CLI and a Colab notebook, so a real web app is a genuine differentiator, not a box-tick.

**Criterion 1 (novelty).** Defensible claims, in increasing order of safety: (a) first gene-grouped, leakage-controlled benchmark for sequence-based senescence prediction; (b) first family-invariant training objective for this task; (c) first residue-level explanation for senescence prediction; (d) first web service. Avoid the word "first" in favour of "we are not aware of prior work that…".

### Risks to state openly in the week-6 pitch
- **The honest numbers will go DOWN.** On a gene-grouped split with hard negatives, accuracy may fall from 86% to somewhere in the 60s–70s. The thesis must be framed so that a lower, trustworthy number is the *result*, not a failure. Agree this framing with the advisor **before** committing, because advisors who expect "beat SOTA" will be unhappy otherwise.
- **The signal may genuinely be weak.** The ageing-gene literature finds annotation/network features dominate and sequence contributes little. If the gene-grouped AUC lands near 0.6, the thesis becomes "sequence alone is insufficient for senescence prediction, and here is the evidence plus a calibrated, domain-aware predictor" — publishable-grade honesty, but it needs an advisor who accepts a negative result. **Decide this with the advisor at week 6.** Consider a pre-agreed stop-gate: if grouped-split AUC < 0.65 by week 9, pivot the emphasis to the benchmark + web tool + XAI and drop the "improve SOTA" claim.
- **The audit trap.** Keep the leakage analysis to one chapter/one table. The thesis title should name the *method* or the *benchmark*, not the audit.
- **LFS/bandwidth** is the only data-access risk (see Q4 gaps) — test `git lfs pull` in the first hour.
- The v2 dataset defects are **unconfirmed** (only v1 verified). Do not assert in a pitch that the published benchmark leaks; assert that the released v1 benchmark demonstrably leaks and that the v2 release has not been checked, and that checking it is step one.

### Gaps
- I did not estimate actual Colab runtimes for ESM-2 650M embedding of ~76,000 sequences. Rough reasoning only: the authors shipped 8M and 35M embeddings as real files but left 150M and 650M as LFS objects, which hints that the larger runs were expensive. **Not measured** — the student should time a 1,000-sequence batch before committing to 650M.
- No information found on whether the SenSeqNet authors would share the exact UniProt query or Table S3 on request. Emailing `hhanli.jiang@mail.utoronto.ca` is untested.
