# Retrieval-augmented, memory-augmented and kNN-augmented methods in protein ML (outside the Ou–Ho group), 2022–2026, as transplantable ideas for a frozen-PLM + mCNN pipeline

> **LƯU TRỮ — không dùng để ra quyết định.** Tài liệu lịch sử; mọi câu "chốt / quyết định / khuyến nghị" bên dưới đã hết hiệu lực. Trạng thái hiện hành: [DECISIONS.md](../../../../DECISIONS.md).

Scope note for the report writer: the earlier survey (`reports/bioinformatics-topic-survey.md`, sections 2–3) already cites ProtEx, MERA, CLEAN and ProtNote, and already proposes "label-free retrieval + leakage-proof evaluation" for DNA/RNA binding sites. The ideas below are meant to be *different* from that one. Where an item overlaps, it is flagged.

Labels used: **VERIFIED** = read in the primary source during this session (paper text, abstract page or official repo). **INFERRED** = my reasoning or arithmetic from verified facts. **UNVERIFIED-MEMORY** = from background knowledge, not re-checked this session (URL given, but the writer should treat it as softer).

Baseline being compared against (from the earlier survey, VERIFIED there): Ou–Ho "RAG" = for each query embedding, take k = 5 L2 nearest neighbours in a ProtT5 embedding DB, average them, blend 0.7 query / 0.3 neighbour mean, feed to mCNN/msCNN. Neighbour *labels* are not used as features. α and k are fixed by hand and never ablated.

## 1. What retrieval-augmented protein methods exist, what do they retrieve, and how do they fuse?

### Takeaway
There are four families: (a) retrieval-augmented *encoders* that feed retrieved sequences into a transformer (RSA, E1, RAGPLM, Protriever/PoET); (b) *embedding-search tools* that replace BLAST/MMseqs2 for finding homologs (knnProtT5, DHR, PLMSearch, TM-Vec, PROTOCOL); (c) *label-transfer hybrids* that copy annotations from retrieved homologs and combine them with an ML model (bindEmbed21, SPROF-GO, ProtEx, CLEAN-style nearest-centroid); and (d) *prediction-level kNN interpolation* (kNN-LM style), seen in kNN-DTA and RAMMESI. Families (a) need training a transformer and are out of budget. Families (b)–(d) are cheap and can be grafted onto frozen ProtT5 + mCNN.

### Cited Findings

**(a) Retrieval-augmented encoders (retrieve sequences, fuse inside a transformer)**
- RSA (Retrieved Sequence Augmentation, Ma et al., EMNLP 2024; bioRxiv/arXiv 2023). Retriever: frozen ESM-1b mean embeddings of **44 million Pfam-A sequences**, indexed with FAISS IVF-PQ (**4096 centroids, 64-byte PQ codes, nprobe 8**). The index took about 30 min to build from a 0.5% training sample. Computing the embeddings took "16 V100 GPUs ... in a day". L2 distance is used. VERIFIED — [RSA paper (ACL Anthology)](https://aclanthology.org/2024.emnlp-main.104.pdf); [code](https://github.com/HKUNLP/RSA)
- RSA fusion: each (query, retrieved) pair is *concatenated* and passed through the ProtBERT encoder, so self-attention gives "a soft version of MSA alignment". Then the N per-pair predictions are combined with weights p(r|x) = softmax(−L2 distance): `prediction = sum(predictions_i * softmax(distance_i))`. The retriever is frozen and the reader is fine-tuned. Cost is N times the base model. VERIFIED — [RSA paper](https://aclanthology.org/2024.emnlp-main.104.pdf)
- RSA gains with N = 16 (ProtBERT backbone versus plain ProtBERT): secondary structure 0.691 → 0.691 (no gain), contact 0.556 → 0.717, remote homology 0.528 → 0.987, stability 0.651 → 0.778, localisation 0.771 → 0.795, PPI 0.688 → 0.827. Average 0.579 → 0.723, versus MSA Transformer at 0.672. RSA is "373 times faster" than MSA-based augmentation. VERIFIED — [RSA paper, Table 3](https://aclanthology.org/2024.emnlp-main.104.pdf)
- RSA's own failure notes: gains are marginal for N > 16 because softmax-over-L2 gives distant neighbours little weight. The retriever shows "polarized retrieval quality, either finding many evolutionary close sequences or failing to find any homologous sequences". Average pooling over retrieved predictions was worse than max pooling plus a scorer for folding. VERIFIED — [RSA paper, appendix F](https://aclanthology.org/2024.emnlp-main.104.pdf)
- Protriever (Weitzman et al., ICML 2025). An ESM-2 dense retriever is trained *jointly* with a PoET reader, so it learns which homologs help the task. Reported: Spearman 0.479 on 217 ProteinGym substitution assays versus PoET at 0.470. Retrieval is about two orders of magnitude faster than MMseqs2/JackHMMER. The learned retriever "prioritizes 'useful' sequences over those with high raw identity". VERIFIED (abstract and summaries) — [arXiv 2506.08954](https://arxiv.org/pdf/2506.08954); [PMLR](https://proceedings.mlr.press/v267/weitzman25a.html)
- E1 (Profluent, bioRxiv Nov 2025). A retrieval-augmented encoder family (150M–600M parameters) with "block-causal multi-sequence attention" over retrieved homologs. It works in "single-sequence or retrieval-augmented inference mode". Released under CC-BY-NC-ND 4.0. Abstract claims SOTA on zero-shot fitness and unsupervised contact prediction; I did not see numbers. VERIFIED (abstract) — [E1 bioRxiv](https://www.biorxiv.org/content/10.1101/2025.11.12.688125v1); [GitHub](https://github.com/Profluent-AI/E1)
- RAGPLM (bioRxiv 2024). Concatenates the query with aligned homologs into one long sequence (up to 12.8k tokens) for structure prediction. VERIFIED (search snippet only) — [bioRxiv 2024.12.02.626519](https://www.biorxiv.org/content/10.1101/2024.12.02.626519v2.full.pdf)

**(b) Embedding-based homology search (retrieval tools)**
- knnProtT5 (Schütze et al., 2022). Mean-pooled ProtT5 per-protein embeddings (1024-d), kNN via FAISS. It "excels in detecting distantly related domains" and works best *combined with* MMseqs2, but "was not competitive for comparison of multidomain proteins". VERIFIED (secondary summary in a 2024 Genome Research paper) — [ResearchGate](https://www.researchgate.net/publication/365452962_Nearest_neighbor_search_on_embeddings_rapidly_identifies_distant_protein_relations); [Genome Res 2024 (DCTdomain), which summarises it](https://pmc.ncbi.nlm.nih.gov/articles/PMC11529836/)
- DHR (Dense Homolog Retriever, Hong et al., Nat Biotech 2024). A dual-encoder PLM trained contrastively. It is "up to 28,700 times faster" than JackHMMER with a ">10% increase in sensitivity". VERIFIED (abstract) — [Nat Biotech](https://www.nature.com/articles/s41587-024-02353-6); [code](https://github.com/ml4bio/Dense-Homolog-Retrieval)
- PLMSearch (Liu et al., Nat Commun 15:2775, 2024). Pipeline: PfamClan prefilter → SS-predictor, a model trained on TM-score that predicts structural similarity from PLM embeddings → ranking. Its companion PLMAlign builds a residue-level substitution matrix from per-residue embeddings. VERIFIED (search snippets; full text not opened) — [Nat Commun](https://www.nature.com/articles/s41467-024-46808-5)
- PROTOCOL (arXiv, May 2026). ColBERT-style *late interaction*: each protein is kept as a set of residue embeddings and scored by MaxSim. It is aimed at the twilight zone and reported to beat pooled-PLM and single-vector baselines on SCOPe superfamily and Pfam clan. No storage or speed numbers in the abstract. VERIFIED (abstract) — [arXiv 2605.29158](https://arxiv.org/pdf/2605.29158)
- TM-Vec (Hamamsy et al., Nat Biotech 2023) predicts TM-score from sequence embeddings for structure-aware search. UNVERIFIED-MEMORY — [Nat Biotech](https://www.nature.com/articles/s41587-023-01917-2)

**(c) Label transfer from retrieved homologs, combined with ML**
- bindEmbed21 (Littmann et al., Sci Rep 2021; just before the window, but the closest analogue to Ou–Ho: **ProtT5 + 2-layer CNN for binding residues**). bindEmbed21HBI transfers residue binding annotations from MMseqs2 homologs at E-value < 1e-3 when one exists; otherwise bindEmbed21DL predicts. Results: ML only F1 = 43 ± 2%; HBI on the subset with homologs F1 ≈ 56 ± 4%; combined F1 = 48 ± 3%, MCC = 0.46 ± 0.04. The E-value optimum "was not sharp", staying nearly constant over at least six orders of magnitude. Redundancy reduction: no pair >20% identity over 250 aligned residues (HVAL < 0). VERIFIED — [Sci Rep / PMC8668950](https://pmc.ncbi.nlm.nih.gov/articles/PMC8668950/); [code](https://github.com/Rostlab/bindPredict)
- SPROF-GO (Yuan et al., Brief Bioinform 2023). ProtT5 + attention pooling + a *homology-based label diffusion* step over a similarity graph of proteins, for GO prediction. Reported AUPR improvements over the previous SOTA: 14.5% / 27.3% / 10.1% on the three ontologies. It "generalizes well on non-homologous proteins and unseen species". About 7 min for 1000 sequences on an RTX 3090. VERIFIED (abstract) — [Brief Bioinform](https://academic.oup.com/bib/article/24/3/bbad117/7085635); [code](https://github.com/biomed-AI/SPROF-GO)
- ProtEx (Google, bioRxiv 2024; *already cited in earlier survey*). For each candidate label, it BLAST-retrieves up to 100 sequences, picks positive and negative exemplars (sequences with and without the label), and concatenates [label, query, exemplars] into a T5 encoder-decoder that outputs p/n. Clustered-split results: EC F1 0.735 vs BLAST 0.679; GO F1 0.506 vs 0.434; Pfam clustered (<25% identity) family accuracy 0.693 vs ProtNLM 0.525. Removing exemplars causes "considerable" drops. Cost: pretraining about 7 days on 64 TPU v3, so the reader is out of budget, but the *exemplar-with-label* idea is not. VERIFIED — [ProtEx bioRxiv](https://www.biorxiv.org/content/10.1101/2024.05.30.596539v1.full)
- CLEAN (Yu et al., Science 2023; *already cited*). Contrastive projection head on frozen ESM-1b, with EC prediction by distance to class centres (an exemplar-based classifier). UNVERIFIED-MEMORY for details — [Zhao group PDF](https://zhaogroup.chbe.illinois.edu/publications/HZ406.pdf)

**(d) Prediction-level kNN interpolation (kNN-LM style)**
- kNN-LM (Khandelwal et al., ICLR 2020) defines the template: a key–value memory of training contexts → neighbour label distribution, interpolated with the model's distribution using a corpus-level λ. VERIFIED (secondary description in search results) — [arXiv 1911.00172](https://arxiv.org/abs/1911.00172)
- kNN-DTA (drug–target affinity, arXiv 2407.15202). Uses two aggregations, *label aggregation* with pair-wise retrieval and *representation aggregation* with point-wise retrieval, applied "in the inference phase ... with no training cost". Ada-kNN-DTA learns instance-wise adaptive weights and improves further: BindingDB IC50 RMSE 0.684 → 0.675; Ki 0.750 → 0.735. VERIFIED (abstract) — [arXiv 2407.15202](https://arxiv.org/pdf/2407.15202)
- RAMMESI (enzyme–substrate interaction, arXiv June 2026). FAISS memory of *unique training enzymes* with cosine similarity, K = 5 optimal (tested up to 20). Neighbour predictions are similarity-weighted, then **linearly interpolated with the base prediction: P = (1 − λ)·P_model + λ·P_retrieval**. The retrieval module is plug-and-play: it improves other backbones (OmniESI, FusionESP) by AUROC +0.015 to +0.036 at **<20% identity**. VERIFIED — [arXiv html 2606.22823](https://arxiv.org/html/2606.22823); [code](https://github.com/code4luck/RAMMESI.git)

### Inferences
- The Ou–Ho method is a degenerate case in RSA's own taxonomy: an unaligned dense retriever, uniform weights 1/k, and aggregation done *in input space* before the classifier. RSA's design space has more axes the group has not explored: weights = softmax(−distance), aggregation of per-neighbour *predictions*, and a learned reader. INFERRED
- The cheapest family with documented gains under identity-controlled splits is (d), prediction-level interpolation. RAMMESI shows it at <20% identity, and kNN-DTA shows it is training-free. Neither has been applied to residue-level binding-site prediction with frozen ProtT5 + CNN, as far as I found. INFERRED

### Gaps
- I did not open the full texts of PLMSearch, DHR, E1, Protriever or PROTOCOL, so downstream-task numbers for those are missing.
- No numbers verified for CLEAN or TM-Vec this session.

## 2. Fusion choices: averaging vs attention vs concatenation vs gating vs prediction-level interpolation. Which beat fixed-weight averaging?

### Takeaway
No protein paper I found compares fusion operators head-to-head on the same frozen-embedding backbone. That comparison is the missing experiment. The best indirect evidence: (i) TabR's ablation shows *learned L2 similarity + using neighbour labels + a correction term* is what lifts retrieval above an MLP, while vanilla attention does no better than an MLP; (ii) RSA's softmax-distance weighting plus a learned reader beats MSA-style aligned aggregation; (iii) adaptive or learned interpolation weights beat fixed ones in kNN-DTA and in NLP semiparametric LMs.

### Cited Findings
- TabR (Gorishniy et al., ICLR 2024; tabular, not protein). An encoder is followed by a single retrieval-attention module in a residual branch. Similarity is `−‖W_k(x) − W_k(x_i)‖²` (key-only, L2, no query projection). The value is `W_y(y_i) + T(k − k_i)`: a label embedding of the neighbour plus an MLP correction on the key difference. m = 96 candidates. VERIFIED — [arXiv html 2307.14338v2](https://arxiv.org/html/2307.14338v2)
- TabR ablation: vanilla self-attention "performs similarly to MLP". Adding label embeddings *alone* gives no measurable gain ("counter-intuitive"). Switching to L2 + key-only similarity is the "turning point". Adding T brings further gains. Removing any of context labels, key-only representation or L2 "results in a performance drop back to the level of MLP". During training the target is excluded from its own context. VERIFIED — [arXiv html 2307.14338v2](https://arxiv.org/html/2307.14338v2); [ICLR 2024 PDF](https://openreview.net/pdf?id=rhgIgTSSxW)
- RSA: per-pair concatenation + self-attention, then softmax(−L2) weighting of per-pair predictions. It beats the "Accelerated MSA Transformer" (same dense retrieval, but aligned MSA-style aggregation), which "drops a lot". VERIFIED — [RSA paper §4.6, Table 6/7](https://aclanthology.org/2024.emnlp-main.104.pdf)
- RAMMESI: prediction-level interpolation with λ, plus channel-wise softmax *gating* across interaction views. VERIFIED — [arXiv html 2606.22823](https://arxiv.org/html/2606.22823)
- kNN-DTA → Ada-kNN-DTA: going from fixed to instance-adaptive aggregation weights gives a small but consistent RMSE improvement (0.684 → 0.675; 0.750 → 0.735). VERIFIED (abstract) — [arXiv 2407.15202](https://arxiv.org/pdf/2407.15202)
- NLP evidence for learned gating: Adaptive Semiparametric LMs (Yogatama et al., TACL 2021) learn a context-dependent gate between local context, short-term memory and kNN long-term memory. UNVERIFIED-MEMORY for details — [arXiv 2102.02557](https://arxiv.org/pdf/2102.02557)
- Limits of kNN interpolation: "Great Memory, Shallow Reasoning: Limits of kNN-LMs" (2024) reports that kNN-LMs help memorisation-heavy tasks but not reasoning. UNVERIFIED-MEMORY for specifics — [arXiv 2408.11815](https://arxiv.org/pdf/2408.11815)
- bindEmbed21 uses a hard switch: HBI if a homolog exists at E < 1e-3, else ML. This simple rule raised F1 from 43% to 48%. VERIFIED — [PMC8668950](https://pmc.ncbi.nlm.nih.gov/articles/PMC8668950/)

### Inferences
- Ou–Ho's convex blend 0.7·q + 0.3·mean(NN) is linear in input space. A CNN downstream could in principle learn the same thing if given [q ; mean(NN)] as concatenated channels, so concatenation is a strictly more general, equally cheap baseline that has never been tested. INFERRED
- TabR's result is a warning: adding neighbour labels in a naive way did nothing. The gain came from the similarity function. For Ou–Ho this suggests the leverage may lie in *what metric retrieves neighbours* (raw ProtT5 L2 vs a learned projection) more than in how they are averaged. INFERRED
- Prediction-level interpolation has one property input-space blending lacks: λ can be tuned on validation, and it degrades gracefully. When no close neighbour exists, a distance-aware gate can fall back to the CNN. INFERRED

### Gaps
- No protein-specific, same-backbone comparison of average vs attention vs gate vs interpolation was found. This is a genuine gap, not a search failure, as far as ~20 queries could tell.

## 3. Does retrieval help mostly through homology? Evidence under low-identity splits

### Takeaway
Mixed evidence. Most retrieval gains are homology-driven: dense retrievers mostly find alignable homologs, and HBI only fires for about a third of proteins. Yet several papers report retrieval still helping at <20–25% identity: RAMMESI, ProtEx on Pfam-clustered, SPROF-GO on non-homologous proteins. A 2026 diagnostic paper warns that PLM similarity scores are not biologically grounded, which is a direct risk for embedding-only retrieval.

### Cited Findings
- RSA: "our dense retriever retrieved a high percentage of homologous proteins that can be aligned to the original protein sequence, comparable to traditional MSA retrievers." In other words, the gains are explained by evolutionary knowledge. VERIFIED — [RSA §4.7](https://aclanthology.org/2024.emnlp-main.104.pdf)
- RSA on de novo proteins (few homologs): ESMFold 0.678 → ESMFold-RSA 0.693 TM-score; AlphaFold-single 0.335 → 0.359 (full-MSA AlphaFold 0.747). The gains are small when homologs are scarce. VERIFIED — [RSA Table 4](https://aclanthology.org/2024.emnlp-main.104.pdf)
- RAMMESI identity-binned AUROC: <20%: 0.848; 20–30%: 0.942; 30–40%: 0.951. The retrieval module adds +0.015 to +0.036 AUROC to other backbones at <20%. Retrieval still helps under strong shift, but absolute performance drops sharply in the lowest bin. VERIFIED — [arXiv html 2606.22823](https://arxiv.org/html/2606.22823)
- ProtEx: Pfam clustered split (<25% identity to train) family accuracy 0.693 vs 0.525. Performance is "relatively constant across training set family sizes". VERIFIED — [ProtEx](https://www.biorxiv.org/content/10.1101/2024.05.30.596539v1.full)
- bindEmbed21: HBI is available for only a subset of proteins (roughly a third; the tool summary reported 7,199 of 20,386 human proteins ≈ 35% at E ≤ 1e-3). HBI F1 ≈ 56% where it applies, versus 43% for ML. VERIFIED (numbers from tool summary of PMC text; the 35% figure should be double-checked against the paper) — [PMC8668950](https://pmc.ncbi.nlm.nih.gov/articles/PMC8668950/)
- PLM-GUARD (Zhou, Yang, Lu, bioRxiv Apr 2026) tests TM-Vec, PLMSearch, DHR and DCTdomain against BLASTp, DIAMOND and MMseqs2 with six sanity checks. Alignment methods show "remarkable robustness, whereas current PLM-based methods fail broadly". Failures include no monotone score decay with divergence, sensitivity to structure-preserving mutations, and inflated similarity for duplicated or shuffled content. Hybrid NEAR is intermediate. VERIFIED (tool summary of full text) — [bioRxiv 2026.04.26.720921](https://www.biorxiv.org/content/10.64898/2026.04.26.720921v1.full)
- Protriever: a learned retriever beats JackHMMER even though JackHMMER finds higher-identity hits. Task-useful retrieval ≠ highest identity. VERIFIED (abstract/summary) — [arXiv 2506.08954](https://arxiv.org/pdf/2506.08954)

### Inferences
- For Ou–Ho datasets split by CD-HIT at 30%, retrieval from the training DB will mostly find *non-homologous* neighbours, because identity to train is below 30% by construction. Expect retrieval gains to be much smaller than with random splits. A thesis could *quantify* this with identity-binned results (bins <20 / 20–30 / ≥30%, RAMMESI-style), which Ou–Ho never report. Note: this overlaps with the earlier survey's "leakage-proof evaluation", so frame identity-binning as the evaluation lens for a *new* fusion/retriever idea, not as the contribution itself. INFERRED
- Per-residue retrieval is different from per-protein retrieval: residues in similar local motifs, such as Walker A for ATP or HTH for DNA, can be neighbours across non-homologous proteins. So residue-level retrieval might keep some signal under 30% splits that protein-level retrieval loses. This is a testable hypothesis I found no paper on. INFERRED

### Gaps
- No paper found that reports residue-level retrieval gains stratified by train–test identity for binding sites.

## 4. Retrieval DB design: contents, dedup, FAISS, storage and compression

### Takeaway
Published systems put either (i) only labelled training items (RAMMESI, kNN-DTA, TabR, CLEAN-style centroids, bindEmbed21 HBI) or (ii) large unlabelled corpora (RSA: 44M Pfam-A; Protriever/E1: UniRef-scale) into the DB. Option (ii) requires a learned reader, so for a student budget, labelled-train-only DBs with FAISS are the realistic design. Residue-level storage is the main engineering cost, and PQ, fp16 or PCA solve it.

### Cited Findings
- RSA's FAISS config: IVF + PQ with 64-byte codes, 4096 centroids, nprobe 8; L2; index trained on 0.5% sample in about 30 min for 44M vectors. VERIFIED — [RSA appendix F.4.1](https://aclanthology.org/2024.emnlp-main.104.pdf)
- RAMMESI: FAISS index over *unique training enzymes* only, built offline, cosine similarity, K = 5. VERIFIED — [arXiv html 2606.22823](https://arxiv.org/html/2606.22823)
- TabR: candidates are training objects only, excluding the target itself during training. VERIFIED — [TabR](https://arxiv.org/html/2307.14338v2)
- knnProtT5 used FAISS on 1024-d mean ProtT5 embeddings. VERIFIED (secondary) — [Genome Res 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11529836/)
- PROTOCOL keeps all residue embeddings per protein for MaxSim scoring. Storage cost is not stated in the abstract. VERIFIED (abstract) — [arXiv 2605.29158](https://arxiv.org/pdf/2605.29158)
- Compression literature for per-residue PLM embeddings: PCA, iDCT quantization and optimal-transport aggregation have all been studied, and mean pooling often wins for protein-level transfer. VERIFIED (search snippets) — [Sci Rep 2025, medium-sized PLMs](https://www.nature.com/articles/s41598-025-05674-x); [OT aggregation, Bioinf Adv 2025](https://academic.oup.com/bioinformaticsadvances/article/5/1/vbaf060/8088230); [Polynomial trajectory compression, bioRxiv 2026](https://www.biorxiv.org/content/10.64898/2026.06.05.730461v1)

### Inferences
- Storage arithmetic for ProtT5 (1024-d) residue embeddings: float32 = 4 KB/residue; fp16 = 2 KB; PCA-256 fp16 = 512 B; PQ-64 = 64 B. A DNA-binding training set of about 500 proteins × about 250 residues ≈ 125k residues gives about 0.5 GB fp32, about 8 MB with PQ-64. Even a 10M-residue unlabelled DB is about 640 MB with PQ-64. FAISS on CPU or a Kaggle GPU handles this easily. INFERRED (arithmetic)
- Dedup and leakage rules a thesis must state: (1) exclude neighbours from the *same protein* as the query, otherwise adjacent residues are trivially near; (2) during training, exclude neighbours from the same CD-HIT cluster as the query (TabR's "exclude self" generalised); (3) the DB contains only the training fold, rebuilt per CV fold. INFERRED
- Rule (1) is likely why naive residue-level kNN on training data looks unrealistically strong: neighbouring residues in the same chain share overlapping context windows in ProtT5. Whether Ou–Ho's code excludes same-protein neighbours is worth checking. INFERRED; not verified for Ou–Ho code

### Gaps
- I found no paper that reports residue-level FAISS DB sizes or PQ accuracy loss for protein residue tasks specifically.

## 5. Retrieval-augmented methods for peptide tasks (AMP, epitopes, cytokine-inducing) or residue binding sites specifically

### Takeaway
Outside the Ou–Ho group, I found **no** retrieval-augmented method dedicated to AMP, epitope or cytokine-inducing peptide prediction. For residue binding sites, the only retrieval-style precedent outside the group is bindEmbed21HBI's homology label transfer, from before 2022. This absence is itself the opening: the transplantable mechanisms come from neighbouring areas (enzyme–substrate, DTA, tabular, GO).

### Cited Findings
- AMP literature searches returned standard PLM/feature models and benchmarks (AMP-EBiLSTM, Macrel, a 2026 AMP evaluation framework), none retrieval-augmented. VERIFIED (absence in search results) — [AMP evaluation framework, bioRxiv 2026](https://www.biorxiv.org/content/10.64898/2026.05.19.726290v1.full); [AMP-EBiLSTM](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10405519/)
- TCR/pMHC/epitope searches returned PLM, structure and transformer methods, with no retrieval augmentation found. VERIFIED (absence in search results) — [TCR–epitope assessment, PMC12791011](https://pmc.ncbi.nlm.nih.gov/articles/PMC12791011)
- Binding residues: bindEmbed21 (ProtT5 + CNN + MMseqs2 HBI) is the closest analogue; see section 1. VERIFIED — [PMC8668950](https://pmc.ncbi.nlm.nih.gov/articles/PMC8668950/)
- Residue-level embedding alignment exists as a tool: PLMAlign (in PLMSearch) and EBA (embedding-based alignment for the twilight zone). Neither was used for binding-label transfer in what I found. VERIFIED (snippets) — [PLMSearch](https://www.nature.com/articles/s41467-024-46808-5); [EBA bioRxiv](https://www.biorxiv.org/content/10.1101/2022.12.13.520313.full.pdf)

### Inferences
- For short peptides (IL-6/IL-13/IFN-γ inducers, AMPs), whole-peptide retrieval *is* the natural unit, and label-aware kNN interpolation is trivial to build. With peptide datasets usually split at 40% identity (CD-HIT, per the earlier survey), it is unclear whether near neighbours remain. INFERRED

### Gaps
- I may have missed Chinese-journal or conference papers using "retrieval" for peptides under different terms ("similarity-based", "memory network", "prototype network"). Prototype or few-shot networks for peptides were not searched.

## 6. Which approaches fit Colab Pro + Kaggle in 4–6 months, and a ranked list of transplantable ideas

### Takeaway
Ruled out: anything that trains a retrieval-augmented transformer reader (RSA fine-tuning of ProtBERT × N = 16, ProtEx, Protriever, E1 pretraining). Feasible: everything that keeps ProtT5 frozen and adds a FAISS lookup plus a small trainable head. The six ideas below are ranked by (novelty vs Ou–Ho) ÷ (risk × compute). All share one evaluation design: cluster-aware CV, same-protein neighbour exclusion, and identity-binned reporting. They differ in the retrieval or fusion mechanism, so none repeats "label-free retrieval" from the earlier survey.

### Cited Findings
(The supporting citations are in sections 1–5; each idea names its closest prior work with links.)

### Inferences — ranked transplantable ideas (all INFERRED as proposals)

**Idea 1: kNN-LM-style prediction-level interpolation for residue binding sites ("kNN-mCNN")**
- *Idea*: keep the mCNN unchanged. Build a FAISS DB of training-fold residue embeddings *with their labels*. At inference, p_kNN = similarity-weighted fraction of positive neighbours, and the final score is p = (1 − λ)·p_mCNN + λ·p_kNN, with λ and k tuned on a validation fold. Variant: λ(d) depends on the nearest-neighbour distance, so it falls back to the CNN when nothing is close.
- *Closest prior work*: [RAMMESI](https://arxiv.org/html/2606.22823) (same formula, enzyme–substrate); [kNN-DTA](https://arxiv.org/pdf/2407.15202) (training-free); [kNN-LM](https://arxiv.org/abs/1911.00172); [bindEmbed21HBI](https://pmc.ncbi.nlm.nih.gov/articles/PMC8668950/) (hard-switch label transfer).
- *New vs Ou–Ho*: fuses at prediction level, not input level; uses *training* labels legitimately; λ and k are tuned on validation instead of set by hand; the result can be stratified by identity bin. It has not been applied to residue binding sites with frozen ProtT5 + CNN, as far as found.
- *Compute*: very low. FAISS on CPU; no extra training beyond the existing mCNN. Roughly 1–3 GPU-hours total for embeddings if they are not already cached.
- *Risk*: low–medium. The gain may be about zero under 30% splits, but that is still a publishable, falsifiable answer. Must exclude same-protein neighbours.

**Idea 2: TabR-style learned retrieval head on frozen ProtT5 (attention over labelled neighbours)**
- *Idea*: replace the fixed 0.7/0.3 average with a trainable retrieval module. Similarity is −‖W_k q − W_k n_i‖² (learned projection, L2). The value is a label embedding of the neighbour plus an MLP of (k_q − k_i). Its output is added residually to the mCNN's penultimate features. Train end-to-end, with neighbours from other clusters only.
- *Closest prior work*: [TabR, ICLR 2024](https://arxiv.org/html/2307.14338v2); [RSA](https://aclanthology.org/2024.emnlp-main.104.pdf) (softmax-distance weighting).
- *New vs Ou–Ho*: learned similarity, learned weights and the use of neighbour labels; it directly tests whether attention beats averaging. The TabR ablation gives a ready-made, step-by-step ablation plan (average → +labels → +L2 key-only → +T).
- *Compute*: low–moderate. Retrieval inside the training loop needs precomputed neighbour candidates, e.g. top-96 per residue, refreshed every few epochs because W_k changes. Kaggle T4/P100 is sufficient, about 10–30 GPU-hours total.
- *Risk*: medium. Overfitting on small datasets (some have only tens of proteins). There is a leakage trap if neighbour exclusion is sloppy. More code complexity than Idea 1.

**Idea 3: A controlled fusion-operator benchmark (average vs concat vs softmax-distance vs gate vs attention vs interpolation)**
- *Idea*: on 2–3 of the group's residue tasks (e.g. DNA, ATP, metal), compare six fusion operators under the same retriever, DB and split, plus a grid over α and k for the group's own operator. Ideas 1 and 2 become two rows of this table.
- *Closest prior work*: RSA Table 1's taxonomy of aggregation forms; Ada-kNN-DTA (fixed vs adaptive); RAMMESI gating.
- *New vs Ou–Ho*: the group never ablated α or k, and no protein paper compares these operators on one backbone (section 2 gap).
- *Compute*: low. Many small CNN trainings, roughly 30–60 GPU-hours on Kaggle across all runs.
- *Risk*: low. The result is guaranteed to be informative, but novelty is "empirical study" rather than "new method". It pairs well with Idea 1 or 2 as the thesis core.

**Idea 4: Task-tuned retriever, a contrastive projection head on frozen ProtT5 (CLEAN/Protriever idea, made cheap)**
- *Idea*: train a small MLP projection with supervised contrastive loss at residue level (binding vs non-binding, across proteins). Use the projected space for retrieval in Idea 1 or 2 instead of raw ProtT5 L2. Compare retrieval with the raw metric against the learned one.
- *Closest prior work*: [Protriever](https://arxiv.org/pdf/2506.08954) (end-to-end retriever, expensive); [DHR](https://www.nature.com/articles/s41587-024-02353-6) (contrastive dual encoder); CLEAN (contrastive head on frozen ESM-1b).
- *New vs Ou–Ho*: the group retrieves with raw L2 on ProtT5. TabR suggests the similarity function is the main lever.
- *Compute*: low. The MLP trains on precomputed embeddings in minutes to hours.
- *Risk*: medium. Contrastive training on residues with 4–10% positives needs careful sampling. It may simply re-learn what the mCNN already learns.

**Idea 5: Residue-aligned homology label transfer + mCNN hybrid (bindEmbed21 modernised)**
- *Idea*: for each test protein, find training proteins via MMseqs2 or embedding search (knnProtT5/PLMSearch). Transfer binding labels *through a residue alignment*, either a classic alignment or an embedding-based one (PLMAlign/EBA). Combine with the mCNN by hard switch (bindEmbed21) or soft interpolation (Idea 1). Report what fraction of test proteins have a usable template at 30% CD-HIT.
- *Closest prior work*: [bindEmbed21](https://pmc.ncbi.nlm.nih.gov/articles/PMC8668950/); [SPROF-GO label diffusion](https://academic.oup.com/bib/article/24/3/bbad117/7085635); [PLMSearch/PLMAlign](https://www.nature.com/articles/s41467-024-46808-5).
- *New vs Ou–Ho*: retrieval at the protein level with positionally aligned label transfer, rather than unaligned per-residue neighbours. It also brings a classic homology baseline, which the group's papers do not report.
- *Compute*: CPU-dominated (MMseqs2 is fast), so very low GPU need.
- *Risk*: medium. Needs bioinformatics tooling (MMseqs2, alignment parsing). Under strict splits few templates exist (bindEmbed21: only about a third of proteins have homologs), so gains may be small. Moderate biology demand.

**Idea 6: Two-stage protein→residue retrieval vs flat residue retrieval, with storage-compression study**
- *Idea*: compare (a) flat per-residue global kNN, as in RAG-msCNN, with (b) protein-level prefilter (mean-pooled ProtT5, top-M proteins) followed by residue-level kNN or ColBERT-style MaxSim inside those proteins, as in PROTOCOL. Also measure accuracy loss under fp16, PCA-256 and FAISS PQ-64 compression.
- *Closest prior work*: [PROTOCOL](https://arxiv.org/pdf/2605.29158); [knnProtT5](https://www.researchgate.net/publication/365452962_Nearest_neighbor_search_on_embeddings_rapidly_identifies_distant_protein_relations); [RSA FAISS IVF-PQ](https://aclanthology.org/2024.emnlp-main.104.pdf).
- *New vs Ou–Ho*: retrieval granularity and DB engineering, neither of which has been studied by the group or, for residue tasks, found elsewhere.
- *Compute*: very low.
- *Risk*: medium–high on novelty. It may read as an engineering ablation. Best as a secondary chapter of Idea 1 or 3, not standalone.

**Deprioritised (stated so the writer does not re-propose them)**
- *Unlabelled UniRef retrieval for representation augmentation (RSA-style)*: overlaps with the earlier survey's label-free retrieval idea. Also, the RSA reader (ProtBERT × N per query) is costly. Excluded.
- *Retrieval-augmented PLM backbones (E1, Protriever)*: E1 could be used as a frozen feature extractor in place of ProtT5, but its CC-BY-NC-ND licence, its 600M size and the need to supply homologs make it a "swap the embedding" study, not a retrieval contribution. Medium–low priority.
- *Retrieval-distance as an OOD/uncertainty signal for abstention or conformal prediction*: a natural add-on to Idea 1. It overlaps with the earlier survey's Proposal 4 (conformal), so mention it only as an extension.

### Gaps
- Compute estimates are my own order-of-magnitude reasoning from dataset sizes typical of the group's tasks (hundreds of proteins, ~10^5 residues). They are not measured.
- I did not verify whether Ou–Ho's code excludes same-protein neighbours in residue-level retrieval. This matters for Ideas 1, 2 and 6 and should be checked in the [RAG_DNA_RNA repo](https://github.com/mhb1717/RAG_DNA_RNA) before the advisor meeting.
- The PLM-GUARD finding (PLM similarity is not biologically grounded) is a risk for all embedding-retrieval ideas. Its implications for *supervised* residue-level retrieval are untested.
