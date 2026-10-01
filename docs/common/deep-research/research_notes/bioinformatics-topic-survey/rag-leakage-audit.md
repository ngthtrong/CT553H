# RAG leakage audit: Prof. Yu-Yen Ou's group's retrieval-augmented residue predictors, plus the literature on leakage and evaluation pitfalls in protein ML

Notes compiled 2026-10-01. Labels: **VERIFIED** means a direct quote from code or a paper, or arithmetic done on numbers printed in those sources. **INFERRED** means my own reasoning from that evidence. Everything here describes technical behaviour only. Nothing here alleges misconduct; the authors may have unpublished code or data that explains the differences.

Local text extraction used: `/home/ngthtrong/CT553H/docs/common/advisor/Prof Ho/1-s2.0-S1746809425019184-main.pdf` (RAG-msCNN) and `/home/ngthtrong/CT553H/docs/common/advisor/Prof Ou/ci5c00766.pdf` (RTK_RAG).

---

## Q1. How is the RAG feature built for the TEST set in RAG-msCNN (repo mhb1717/RAG_DNA_RNA), and does any code path select residues by label?

### Takeaway
Yes. The **first public version** of the RAG script (commit `05693c4`, 2025-07-01, about seven weeks before the paper was submitted on 20 Aug 2025) requires a label file and applies retrieval **only where `label[1] == 1`**. There is no separate label-free inference path, so ground-truth labels leak into test features whenever the script is run on test data. In February–March 2026, *after* publication, the repo was rewritten to apply RAG "to ALL samples uniformly". The notebook outputs committed with that version show test MCC of **0.30 / 0.40 / 0.41** on TE181 / TE129 / TE46. That is baseline level, against the paper's 0.91 / 0.95 / 0.92. Separately, the paper's RNA (TE117) numbers match exactly a run on a **4,424-residue label-balanced subset** of TE117, not the 37,345-residue test set the paper describes. Every evaluation notebook also picks the decision threshold **on the test set**.

### Cited Findings

**What the paper says (VERIFIED, local PDF, Section 2.2.3):**
- "We apply our RAG approach exclusively to positive residues and enhance their embeddings by using their vectors (v+) as queries ... we identify the top k = 5 nearest neighbors ... By retrieving the top five similar binding residue embeddings from our database, we compute their average ... c = αv+ + (1−α)c ... α = 0.7 ... The result is a method that enhances the features of positive samples without diluting the context of the original data." The paper never describes how a residue of unknown label is handled at inference. — [RAG-msCNN, BSPC 115 (2026) 109407](https://www.sciencedirect.com/science/article/abs/pii/S1746809425019184)
- On the database it says: "To avoid potential label leakage and data redundancy, CD-HIT was utilized to cluster all protein sequences at a 30% sequence identity level. This guaranteed that the sequences used for RAG retrieval did not overlap with those used for model training or testing." The RAG-DB is "collected from a curated RNA-binding protein dataset". — [RAG-msCNN](https://www.sciencedirect.com/science/article/abs/pii/S1746809425019184)
- Timeline: received 20 Aug 2025, revised 29 Oct 2025, accepted 8 Dec 2025, online 11 Dec 2025. Data availability: "https://github.com/mhb1717/RAG_DNA_RNA". — local PDF
- Reported results (Table 3): TE181 MCC 0.9114 / AUC 0.9998; TE129 MCC 0.9492 / AUC 0.9999; TE46 F1 0.9217 / MCC 0.9163. Table 4 baselines without RAG: ProtTrans TE181 F1 0.2623 / MCC 0.3033; TE129 F1 0.3644 / MCC 0.3884. RNA TE117 (Section 4.6): recall 0.9717, precision 0.9664, F1 0.9690, MCC 0.9431, AUC 0.9963. — local PDF
- Dataset sizes as stated in the paper: TE181 has 75,258 residues (3,208 binding); TE129 has 37,515 (2,240); TE46 has 10,876 (965); TE117 (RNA) has 37,345 (2,031); TR495 has 136,899 (14,609). — local PDF

**Original code, July 2025 (VERIFIED):**
- `get_RagEmb_Batch_N.py`, added in commit `05693c4` (2025-07-01) and deleted in commit `f9f0d1c` (2026-02-28). Argument `-labels` is `required=True`. The core loop:
  ```python
  for i, (query, label) in enumerate(zip(batch_queries, batch_labels)):
      if label[1] == 1:  # Apply RAG only on positive samples (one-hot encoding check)
          fused_embedding = compute_rag_embedding(query, rag_database, maxseq, num_feature)
          fused_embeddings[start_idx + i] = fused_embedding  # Update only positive samples
  ```
  The code comment for the database shape reads `# Shape: (605679, 1, 15, 1024)`. — [get_RagEmb_Batch_N.py @05693c4](https://github.com/mhb1717/RAG_DNA_RNA/blob/05693c4/get_RagEmb_Batch_N.py)
- The only RAG script in the repo between July 2025 and Feb 2026 was this one. The README's Step 3 says the RAG scripts "extract context-aware embeddings for training/testing". Nothing in the repo builds test features without labels. — [RAG_DNA_RNA README](https://github.com/mhb1717/RAG_DNA_RNA/blob/main/README.md); [commit history](https://github.com/mhb1717/RAG_DNA_RNA/commits/main)
- Original notebook `mscnn.ipynb` (commit `43d760c`, July 2025) loads `TE129_RAG.npy` as the DNA test input and `TE117_data.npy` (4,424 rows) for RNA. Its RNA output: "TP=1853, FP=117, TN=2296, FN=158 ... F1=0.9309, MCC=0.8746". — [mscnn.ipynb @43d760c](https://github.com/mhb1717/RAG_DNA_RNA/blob/43d760c/mscnn.ipynb)

**Post-publication rewrite, Feb–Mar 2026 (VERIFIED):**
- Commit `7a47d6a` (2026-03-02) added `get_RagEmb_Batch.py` (348 lines). Labels are now "optional, for statistics only", and the script prints `"Applying RAG to ALL samples uniformly (no label-dependent processing)"`. The file was deleted 22 seconds later in commit `5235871`. — [get_RagEmb_Batch.py @7a47d6a](https://github.com/mhb1717/RAG_DNA_RNA/blob/7a47d6a/get_RagEmb_Batch.py)
- The current `get_RagEmbedding.py` (commit `ca7198d`, 2026-03-02) takes no labels. It flattens each 15×1024 window, finds the top 5 by squared L2 distance, and fuses as `batch_queries_flat * 0.7 + avg_embeddings * 0.3` for **every** query. — [get_RagEmbedding.py](https://github.com/mhb1717/RAG_DNA_RNA/blob/main/get_RagEmbedding.py)
- The current `MSCNN_DNA.ipynb` (commit `50668e4`, 2026-03-02; the 2026-02-28 version `09a8167` has the same outputs) trains on `TR573_rag_common_data.npy` and tests on `TE181_rag_data.npy` / `TE129_rag_data.npy`, and on `TE46_rag_data.npy` after training on TR646. Saved outputs:
  - TE181 (75,258 rows): "F1=0.2626, MCC=0.2995", AUC 0.8864
  - TE129 (37,515 rows): "F1=0.3805, MCC=0.3979", AUC 0.9131
  - TE46 (10,876 rows): "F1=0.4320, MCC=0.4105", AUC 0.8833
  - TE117 (4,424 rows): "F1=0.9303, MCC=0.8727", AUC 0.9791

  — [MSCNN_DNA.ipynb](https://github.com/mhb1717/RAG_DNA_RNA/blob/main/MSCNN_DNA.ipynb)
- Notebook version `b78474f` (2026-02-04) has an RNA cell loading `TE117_RAG.npy` (4,424 rows). Its output is "TP=1954, FP=68, TN=2345, FN=57 ... Precision=0.9664, F1=0.9690, MCC=0.9431", AUC 0.9963, which matches the paper's RNA117 numbers to four decimals. A TE181 cell in the same version (file `TE181_data_tape.npy`, 75,104 rows) printed MCC 0.8602 / AUC 0.9984. — [MSCNN_DNA.ipynb @b78474f](https://github.com/mhb1717/RAG_DNA_RNA/blob/b78474f/MSCNN_DNA.ipynb)

**Label-dependent subsampling (VERIFIED code, plus arithmetic):**
- `get_dataset_RAG_DB.py` splits each protein's windows with `series_features[labels == 1]` / `[labels == 0]`. It keeps `int(len(positive_samples) * 1.2)` negatives chosen by `np.argsort(similarity_scores)[:num_negatives]`, i.e. the negatives with the **lowest** mean cosine similarity to the positives. It saves the result as `data_balanced.npy`. — [get_dataset_RAG_DB.py](https://github.com/mhb1717/RAG_DNA_RNA/blob/main/get_dataset_RAG_DB.py)
- The 4,424-row TE117 test file has 1,954 + 57 = **2,011 positives** and 68 + 2,345 = **2,413 negatives**. int(2,011 × 1.2) = 2,413 exactly. — arithmetic on the notebook outputs above

**Threshold chosen on the test set (VERIFIED):**
- Every `model_test` function computes the ROC on `(y_test, preds)` and sets `best_thresh = thresholds[argmax(sqrt(tpr*(1-fpr)))]`. It then reports Sens/Spec/Pre/F1/MCC at that test-optimal threshold. No validation split is used. — [MSCNN_DNA.ipynb](https://github.com/mhb1717/RAG_DNA_RNA/blob/main/MSCNN_DNA.ipynb)

**Internal inconsistencies in the paper (VERIFIED arithmetic from stated class counts):**
- Table 3 TE181 (Spe 0.9918, Rec 0.9934) implies Pre 0.8436 and MCC 0.9115, which is consistent with the table. The text and Table 4 report MCC **0.8123** with Spe 0.9799 / Rec 0.9855 but the same Pre 0.8434 / F1 0.9123. Those Spe/Rec values imply Pre 0.686 and F1 0.809.
- TE129: Table 3 gives MCC 0.9492 and AUC 0.9999; the text gives MCC 0.9188 and AUC 0.9909.
- TE46: Table 3 gives recall 0.9523; the text gives 0.8725. Only 0.8725 is consistent with the reported F1 0.9217 and MCC 0.9163.

— local PDF; arithmetic mine

### Inferences
- **INFERRED, high confidence:** the student's hypothesis is supported by direct code evidence. With the published-era script, the input of a test residue is changed if and only if its true label is 1. That gives the classifier a label-correlated signal (a 30% pull toward a cluster of "binding" embeddings) that cannot exist at deployment time. This fits the Kapoor & Narayanan category of features that are a proxy for the outcome (see Q4).
- **INFERRED, high confidence:** the repo's own label-free re-run reaches MCC 0.30 / 0.40 / 0.41. That roughly equals the paper's no-RAG ProtTrans baselines (Table 4: TE181 MCC 0.3033, TE129 MCC 0.3884). So, on the public evidence, almost all of the reported gain (MCC around 0.3–0.4 → 0.91–0.95) depends on label-conditioned augmentation and is not reproduced when augmentation is label-free.
- **INFERRED, medium–high confidence:** the RNA TE117 headline result (MCC 0.9431) appears to come from a balanced test subset. That subset was built with labels, and its negatives were chosen as the *least* similar to the positives, which makes the task much easier. The paper describes TE117 as 37,345 residues with 2,031 binding. Balanced, easy-negative test sets also inflate precision/F1/MCC by changing prevalence.
- **INFERRED:** choosing the threshold on the test set adds a further optimistic bias. It is smaller than the label-leak effect, but it is a distinct pitfall worth auditing.
- **INFERRED:** the paper claims the database is disjoint from test proteins (CD-HIT 30%). I could not verify this, because the RAG-DB FASTA/IDs are not in the repo (only `dna_dataset.rar` and zip archives).

### Gaps
- I could not see which exact `.npy` files produced each number in the paper. Generated `.npy` files are not in the repo, and the July 2025 notebook has no saved DNA output.
- I did not unpack `dna_dataset.rar` / `TE180.zip` / `TR735.zip` to check whether the RAG-DB overlaps the test proteins.
- No author statement explains why the RAG script was rewritten in Feb–Mar 2026. Commit messages are generic ("Add files via upload").

---

## Q1b. The group's other RAG repos (RTK_RAG, RAG_MCNNIL6, IFNg_DeepKG, DeepRAGIL-2; DEEPTRANS and the metal-binding paper)

### Takeaway
None of the other public RAG scripts in the group's repos select queries by label: retrieval is applied to every query, against a database that holds both positive and negative examples. The positive-only design therefore appears specific to RAG-msCNN, which the paper itself says "improves on our previous RAG-based frameworks". RTK_RAG's repo does not contain its RAG-building code at all; its Colab inference pipeline applies RAG to whole sequences without labels.

### Cited Findings
- **RAG_MCNNIL6 (JCIM 2025, Chuang, Liu, Jhang, Wei, Ou):** `DATASET/get_rag_dataset.py` loops over every `.prottrans` file in the input folder. It keeps the top 5 by `np.linalg.norm(target_len - i)` and returns `(target_len + avg_embedding) / 2`, i.e. 1:1 fusion. No labels are read. The README lists the RAG database as 9,892 peptides (513 IL-6-inducing, 9,379 not). — [get_rag_dataset.py](https://github.com/B1607/RAG_MCNNIL6/blob/main/DATASET/get_rag_dataset.py); [README](https://github.com/B1607/RAG_MCNNIL6); [paper (PMC)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11898070/)
- **IFNg_DeepKG (JCIM 2026):** `CODE/get_RAGKGEmb.py` computes `compute_rag_embedding` for every `query_idx` with top_k = 5, weights neighbours by Neo4j knowledge-graph relations, and fuses `(query * 0.9) + (weighted_avg * 0.1)`. The script contains no reference to labels. — [get_RAGKGEmb.py](https://github.com/s1129108/IFNg_DeepKG/blob/main/CODE/get_RAGKGEmb.py)
- **DeepRAGIL-2 (Yuune, Le, Ou):** `CODE/RAG_retriever.py` provides `retrieve_batch(queries)` over all queries (top_k = 5, query_weight = 0.5) and contains no reference to labels. The repo also has `rag_identity_distribution.py`, `multiseed_exp.py`, `mlp_baseline.py` and `stratified_specificity.py`, which suggests some evaluation-robustness checks. — [DeepRAGIL-2](https://github.com/juanyuune/DeepRAGIL-2)
- **DEEPTRANS (Chem Phys Lett 2025) and the metal-binding RAG paper (Eng Appl AI 2026):** I could not find public repos through GitHub search ("DEEPTRANS protein", "RAG metal binding ProtTrans").

### Inferences
- **INFERRED:** for an audit thesis, the group's earlier peptide-level RAG papers provide a natural "correct" in-house design to compare against: label-free retrieval of all queries over a mixed-label database. RAG-msCNN is the outlier.

### Gaps
- DEEPTRANS and the metal-binding RAG code were not located, so their test-time behaviour is unknown.
- I did not audit those repos' splits or thresholds; I only checked them for label usage in RAG.

---

## Q2. Does RTK_RAG (JCIM 2025, 65, 7277–7284) apply retrieval to all residues or only positives?

### Takeaway
The paper describes retrieval at the **sequence level**, label-free: the query is the whole protein embedding, the top-K most similar database sequences are averaged, and the result is fused with the query 1:1. The deployed Colab applies RAG to an unlabeled uploaded sequence. **However, the GitHub repo contains no RAG-building or test-feature code.** It only has a training notebook that loads precomputed `rag_prottrans` `.npy` files, so I cannot verify from code how the test features in the paper were generated.

### Cited Findings
- Paper: "when given a target RTK protein sequence, we first convert it into a feature vector using a protein language model ... L × 1 × 1024 embedding ... compare this embedding against a database of precomputed embeddings using a distance metric to search for the top K similar protein sequences ... average the embeddings of these retrieved sequences ... combine it with the original query embedding at a 1:1 ratio." Nothing restricts this to positives. — [RTK_RAG, JCIM 2025 (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12264935/)
- Data split: 313 RTK sequences from UniProt were clustered with CD-HIT at 40% together with ATP-549. That "yielded 69 RTK proteins ... designated for validation, while the remaining 244 sequences formed the final RAG database (2,676 ATP-binding and 261,088 nonbinding residues)". The test set has 69 proteins with 711 binding and 73,270 non-binding residues. — [RTK_RAG (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12264935/)
- Results, Table 5: ProtTrans without RAG gives Sens 0.8498 / Spec 0.9433 / MCC 0.3181 / AUC 0.9497. RAG_ProtTrans gives Sens 0.9747 / Spec 0.9896 / Acc 0.9895 / **MCC 0.6782** / AUC 0.9868. — local PDF ci5c00766.pdf
- Repo contents: `CODE/MCNN_npy.ipynb` and `CODE/import_data.py`. `import_data.py` loads `../dataset/RTK_69/<DATA_TYPE>/<WINDOW>/data.npy`. The notebook sets `DATA_TYPE = "rag_prottrans"` and imports `import_test_die`, a module that is not in the repo. Its saved outputs are 5-fold CV on ATP-549 only (mean MCC 0.4296, ROC-AUC 0.9523); the independent-test cell has no saved output. — [RTK_RAG repo](https://github.com/B1607/RTK_RAG); [import_data.py](https://github.com/B1607/RTK_RAG/blob/main/CODE/import_data.py)
- The notebook's `model_test` also selects the threshold by maximum G-mean on the evaluated fold or test set. — [MCNN_npy.ipynb](https://github.com/B1607/RTK_RAG/blob/main/CODE/MCNN_npy.ipynb)
- The Colab inference notebook runs `embedding = rag_prottrans_GPU.pred_main(embedding)` on each uploaded FASTA sequence, then predicts with a fixed `threshold=0.24920600652694702`. This is label-free. The RAG module itself is in `RTK_RAG_colab.zip` on `http://140.138.155.214/~user4/`, which did not respond when I tried it. — [Colab notebook](https://colab.research.google.com/drive/19pOze_jxxAq3XOQd6yuIiCBLEpbGBI29)

### Inferences
- **INFERRED:** RTK_RAG's described design is label-free and is the conceptually sound version: the database is disjoint from test, mixed-label, and retrieval is per sequence. The MCC gain (0.32 → 0.68) is large but plausible for an in-family database. RTK proteins in the RAG-DB are close homologs of RTK test proteins at under 40% identity to each other (CD-HIT 40% was run jointly). That gives "family-specific retrieval" a real advantage. Whether this counts as leakage depends on the deployment question: are new RTKs always within reach of the DB family? Note too that CD-HIT at 40% is looser than the usual 25–30%.
- **INFERRED:** the 1:1 fusion of a whole-sequence average embedding is mathematically odd for per-residue prediction, because neighbours of different lengths are padded or truncated and averaged position by position. The rag_prottrans_GPU code is needed to confirm what is actually done.

### Gaps
- `rag_prottrans_GPU.py` (inside the Colab zip) could not be retrieved, so test-time RAG for RTK_RAG is VERIFIED only at the paper and Colab-call level, not in the function body.
- No saved independent-test output exists in the repo to compare against Table 5.

---

## Q3. Have any published comments, follow-up papers, or reproductions questioned these results?

### Takeaway
I found no public critique, PubPeer thread, erratum or independent reproduction of RAG-msCNN or RTK_RAG. The only "reproduction" evidence is the authors' own updated notebook outputs in the RAG_DNA_RNA repo (Q1), which do not reach the published numbers.

### Cited Findings
- A web search for PubPeer / comments on RAG-msCNN, RTK_RAG and "retrieval-augmented binding site" returned only the original papers and repos. — [ScienceDirect RAG-msCNN page](https://www.sciencedirect.com/science/article/abs/pii/S1746809425019184); [RTK_RAG on ACS](https://pubs.acs.org/doi/10.1021/acs.jcim.5c00766)
- Basu et al. (2025), a review of 20 years of nucleic-acid-binding residue predictors, uses the same 46-protein DNA test set (965 binding / 9,911 non-binding, i.e. TE46). It warns that "The training datasets of the other methods may share higher levels of similarity, and thus their reported predictive performance might be inflated." It also notes that comparing MCC values computed "at different rates of positive ... to negative predictions" obscures differences. — [Twenty years of advances in prediction of nucleic acid-binding residues, Brief Bioinform 26(1) bbaf016](https://academic.oup.com/bib/article/26/1/bbaf016/7964485)

### Inferences
- **INFERRED:** on TE46, F1 jumps from 0.539 (PDNAPred) to 0.922. A careful 2025 field review treats the same dataset as hard, with realistic state of the art far below 0.9 MCC. A jump that size on a mature benchmark is, by itself, a red flag that a leakage audit should explain.
- **INFERRED:** the absence of critique means an audit would be a first public analysis. It also means the student must be especially careful and courteous: these are the advisors' own papers (see the thesis-framing notes under Q5).

### Gaps
- I did not search the Elsevier comment system, ResearchGate Q&A, or citing papers in Google Scholar exhaustively. The paper went online in Dec 2025, so citations are probably still few.

---

## Q4. What does the literature say about data leakage and evaluation pitfalls in protein / bioinformatics ML?

### Takeaway
Leakage is well documented and highly cited. There is a general taxonomy (Kapoor & Narayanan 2023) and protein-specific demonstrations: in PPI prediction, performance falls to random once homology leakage is removed; PDBbind/CASF scores were inflated; and PLM pretraining contaminates downstream tests. Each of these follows the same pattern seen here: removing the leak makes the "SOTA" gain disappear. Label leakage *through feature construction in retrieval* is a less-covered variant, which leaves a niche.

### Cited Findings
- **Kapoor & Narayanan (Patterns 4(9), 2023):** leakage affected "at least 294 papers across 17 disciplines". They give a taxonomy of eight leakage types and propose "model info sheets". In a civil-war prediction case study, "when they corrected for data leakage, the supposed superiority of ML models disappeared." — [Patterns](https://www.cell.com/patterns/fulltext/S2666-3899(23)00159-9); [open PDF](https://hbiostat.org/papers/kap23lea.pdf)
- **Bernett, Blumenthal & List (Brief Bioinform 25(2) bbae076, 2024):** "overlaps between training and test sets resulting from random splitting lead to strongly overestimated performances. When data leakage is avoided by minimizing sequence similarities between training and test set, performances become random." Simple similarity/topology baselines perform well. — [Brief Bioinform](https://academic.oup.com/bib/article/25/2/bbae076/7621029)
- **Bushuiev et al. (ICLR workshop 2024), "Revealing data leakage in protein interaction benchmarks":** sequence- or metadata-based splits of protein complexes "introduce major data leakage". They recommend splitting by 3D interface similarity. — [mlanthology](https://mlanthology.org/iclrw/2024/bushuiev2024iclrw-revealing/); [OpenReview PDF](https://openreview.net/pdf?id=ORMXYUK5IY)
- **"Resolving data bias improves generalization in binding affinity prediction" (Nature Machine Intelligence 2025; author names not verified here), PDBbind CleanSplit / GEMS:** train–test leakage between PDBbind and CASF "has severely inflated the performance metrics". Retraining GenScore and Pafnucy on CleanSplit made performance "drop substantially". — [Nat Mach Intell](https://www.nature.com/articles/s42256-025-01124-5); [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12552120/)
- **Leak Proof PDBBind (LP-PDBBind)** is another reorganised split of PDBbind for generalisable affinity prediction. — [ResearchGate](https://www.researchgate.net/publication/373245658_Leak_Proof_PDBBind_A_Reorganized_Dataset_of_Protein-Ligand_Complexes_for_More_Generalizable_Binding_Affinity_Prediction)
- **Hermann et al. (MLCB 2024 / PMLR 261), "Beware of Data Leakage from Protein LLM Pretraining":** test proteins often appear in PLM pretraining sets. For thermostability, leakage "distorted measured performance by an average 11.1%" compared with pretraining-aware splits. — [PMLR](https://proceedings.mlr.press/v261/hermann24a.html); [bioRxiv](https://www.biorxiv.org/content/10.1101/2024.07.23.604678.full.pdf)
- **PPI + PLM pretraining flaw (bioRxiv 2025):** because PLMs are trained on UniRef "without regard to downstream task evaluation", most PPI test proteins appear in pretraining. — [bioRxiv 2025.04.21.649858](https://www.biorxiv.org/content/10.1101/2025.04.21.649858.full.pdf)
- **AlphaFold-based ML (Brief Bioinform 26(2) bbaf104, 2025):** many studies did not exclude AF2 training proteins, which caused leakage; the authors provide regularly updated benchmark sets. — [Brief Bioinform](https://academic.oup.com/bib/article/26/2/bbaf104/8069415)
- **Nucleic-acid-binding residue field:** Basu et al. 2025 (Q3) flag inflated performance when train/test similarity exceeds about 30%, and inconsistent MCC comparisons across thresholds. Earlier Kurgan-group reviews ("Review and comparative assessment of sequence-based predictors of protein-binding residues", Brief Bioinform 19(5); "A comprehensive comparative review of sequence-based predictors of DNA- and RNA-binding residues", bbv023; exact author lists not re-verified) set the practice of low-similarity benchmarks and documented cross-prediction between ligand types. — [Basu et al. 2025](https://academic.oup.com/bib/article/26/1/bbaf016/7964485); [Brief Bioinform 19(5)](https://academic.oup.com/bib/article/19/5/821/3059360); [bbv023](https://dx.doi.org/10.1093/bib/bbv023)
- **Large-scale meta-study (arXiv 2604.04199, 2026), "Which Leakage Types Matter? ... 2,047 Benchmark Datasets":** an empirical ranking of leakage types. I saw only the title and snippet, not the full text. — [arXiv](https://arxiv.org/pdf/2604.04199)
- **LIT-PCBA (arXiv 2507.21404, 2025):** data leakage and redundancy found in a widely used virtual-screening benchmark. — [arXiv](https://arxiv.org/pdf/2507.21404)

### Inferences
- **INFERRED:** mapped onto Kapoor & Narayanan's taxonomy, RAG-msCNN's issues are: (a) **label-dependent feature construction at test time**, a feature that is a proxy for the outcome; (b) a **test set re-sampled with labels** (balanced, easy negatives) that does not match the deployment distribution; (c) **hyper-parameters / threshold tuned on the test set**, i.e. no clean separation. Homology leakage and PLM-pretraining leakage are possible additional, smaller factors.
- **INFERRED:** the literature gives strong precedent for a thesis structured as "audit → corrected protocol → honest re-benchmark". Bernett et al. and CleanSplit are both highly visible papers built on exactly that structure.

### Gaps
- I did not find a protein-ML paper specifically about **label leakage inside retrieval augmentation** (RAG features conditioned on labels). This gap is plausibly the student's novelty, but I did not search exhaustively (for example, the kNN-feature / target-encoding leakage literature in tabular ML).
- DOME recommendations (Walsh et al., Nat Methods 2021) and the Kapoor full eight-type list were not re-fetched here; cite from the originals.

---

## Q5. What label-free retrieval designs exist that could serve as a corrected alternative?

### Takeaway
Several sound designs exist. All of them retrieve from the **query embedding alone** and use labels only from the **database side** (training/reference set), never from the query. Options:

- **Retrieve neighbours and fuse their embeddings**, label-free: RSA, RAG_MCNNIL6, IFNg_DeepKG, DeepRAGIL-2.
- **Retrieve neighbours together with their labels** as extra input: a kNN label-propagation feature, i.e. the fraction of retrieved database residues that bind.
- **Condition on positive and negative exemplars**: ProtEx.
- **Use homologs/MSA as retrieval**: E1, RAGPLM.
- **Residue-level retrieval with mixture-of-experts**: MERA.

### Cited Findings
- **RSA (Retrieved Sequence Augmentation, arXiv 2302.12563):** links each query to database sequences "with similar structures or properties" and combines them for downstream prediction. PLMs benefit on structure and property tasks. — [arXiv](https://arxiv.org/pdf/2302.12563)
- **ProtEx (bioRxiv 2024.05.30.596539):** for each candidate label, it retrieves **positive and negative exemplars from the training data** (BLAST-based) and conditions on query + label + exemplars. Labels come only from the database. It generalises to rare and unseen classes and to low-similarity sequences. — [bioRxiv](https://www.biorxiv.org/content/10.1101/2024.05.30.596539v1.full)
- **E1 (bioRxiv 2025.11.12.688125):** a retrieval-augmented protein encoder. Homologs are prepended to the query, with alternating intra-sequence / block-causal attention. It beats ESM in single-sequence mode and other retrieval models on fitness and contact prediction. — [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.11.12.688125v1.full)
- **RAGPLM (bioRxiv 2024.12.02.626519):** a PLM plus retrieved MSA for structure prediction. — [bioRxiv](https://www.biorxiv.org/content/10.1101/2024.12.02.626519.full.pdf)
- **MERA (arXiv 2603.01511, 2026):** "the first retrieval-augmented framework for protein active-site prediction", using residue-level mixture-of-experts. This is a directly relevant per-residue precedent. — [arXiv](https://arxiv.org/pdf/2603.01511)
- **Multimodal retrieval-augmented protein function foundation model (arXiv 2508.04724).** — [arXiv](https://arxiv.org/html/2508.04724v1)
- The group's own label-free implementations (RAG_MCNNIL6, IFNg_DeepKG, DeepRAGIL-2) are given in Q1b. In addition, the current RAG_DNA_RNA `get_RagEmbedding.py` is itself the label-free variant, and it yields MCC around 0.30–0.41 on the DNA tests. — [RAG_DNA_RNA](https://github.com/mhb1717/RAG_DNA_RNA/blob/main/get_RagEmbedding.py)

### Inferences
- **INFERRED: candidate corrected designs for a thesis**, in rising order of difficulty:
  1. Label-free mean fusion over a mixed-label database. This is a replication of the repo's current code and is expected to sit near baseline.
  2. **Label-aware neighbour features**: concatenate the query with the label-weighted mean of the neighbours' embeddings and/or the neighbour binding fraction. Labels are taken only from the training/DB side and the query is excluded from the DB. Close to kNN-LM / ProtEx-style exemplar conditioning.
  3. Separate positive and negative neighbour sets: the mean of the k nearest *binding* DB residues and the mean of the k nearest *non-binding* DB residues, both fed to the model, so the model learns the contrast.
  4. Homolog / MSA-level retrieval (E1-like) at protein level, with residues aligned rather than averaged window by window.
- **INFERRED: a defensible protocol** would include:
  - DB built from training proteins only, or from an external set clustered under 25–30% against test (CD-HIT or MMseqs2);
  - the threshold chosen on a validation split;
  - full, natural-prevalence test sets;
  - reporting of AUPRC alongside MCC, plus multiple seeds;
  - a "label-shuffled DB" negative control and an "oracle positive-only" ablation that measures the size of the leak.
- **INFERRED: novelty and defensibility.** The *audit* part is novel for this specific model family, has a clear expected result (the repo itself shows MCC around 0.3–0.4 without label conditioning), and is cheap to run on CPU or a modest GPU (ProtT5 embeddings + small CNN). The *corrected method* part is incremental but legitimate. The biggest risk is social, not technical: the papers belong to the advisors. The thesis should therefore be framed as "evaluation protocol and label-free retrieval for nucleic-acid-binding residue prediction", with the leakage analysis presented neutrally as an ablation ("positive-only augmentation requires labels at inference; we quantify its effect"). It should be discussed with Dr. Ho / Prof. Ou *before* committing, since they may already know about the March 2026 code rewrite.

### Gaps
- I did not confirm whether a standard kNN-label-feature approach has already been applied to DNA/RNA-binding residue prediction. A targeted search for "kNN" / "nearest neighbor" + "binding residue" + "PLM" is still needed.
- I did not fetch the full texts of RSA, E1 or MERA to extract their exact leakage controls.
