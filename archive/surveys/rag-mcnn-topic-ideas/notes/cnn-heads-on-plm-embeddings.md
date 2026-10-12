# Lightweight CNN heads (mCNN / msCNN / TextCNN-style) on frozen PLM embeddings: what is known, what is open, and CNN-centred thesis ideas (2021–2026)

> **LƯU TRỮ — không dùng để ra quyết định.** Tài liệu lịch sử; mọi câu "chốt / quyết định / khuyến nghị" bên dưới đã hết hiệu lực. Trạng thái hiện hành: [DECISIONS.md](../../../../DECISIONS.md).

Scope note: written 1 Oct 2026 for a CTU undergraduate choosing a thesis under Yu-Yen Ou and Quang-Thai Ho. Baseline being compared against is the "Ou–Ho pipeline": frozen ProtT5-XL-U50 per-residue embeddings (1024-d), then a sliding fragment (often 15 residues) or the full sequence, then mCNN (parallel convs with several window sizes, max-pooling, dense layers) or msCNN (depthwise-separable multi-scale convs). LoRA is deliberately treated as a side comparison only, following the earlier survey (`reports/bioinformatics-topic-survey.md`, section 2).
Labels: **VERIFIED** = read in the cited source (full text, abstract or official README). **INFERRED** = my reasoning or arithmetic, not a measured result. Where a fact comes only from a search-engine snippet of the paper, that is stated.

---

## Q1. Systematic comparisons of heads on frozen PLM embeddings: when does a CNN head actually help?

### Takeaway
The field's de facto per-residue head on ProtT5 has been a **shallow 2-layer CNN over the full sequence** since 2021 (Rostlab: ProtTrans secondary structure, bindEmbed21DL, SETH, and Schmirler 2024's frozen baselines). For per-protein tasks the default is mean pooling + small FFN or Light Attention. **No study I found compares, on the same frozen embeddings and the same split, linear / MLP / 2-layer full-sequence CNN / multi-window CNN (mCNN) / BiLSTM / light attention for residue-level *binding-site* tasks.** The Ou–Ho mCNN papers compare mCNN only against classical ML (SVM/KNN/RF), never against other neural heads. That missing ablation is the cleanest CNN-centred gap.

### Cited Findings
- **VERIFIED.** Schmirler et al. used a "two-layer CNN" as the frozen-embedding head for per-residue tasks: secondary structure ("matching prior work") and disorder (the SETH architecture). For per-protein tasks they used "a single fully connected layer of size 32" on mean-pooled embeddings, and also tested Light Attention, which "substantially improves over such coarse-grained averaging". They did **not** systematically compare head architectures. Embeddings were generated in half precision. — [Schmirler et al., bioRxiv v2](https://www.biorxiv.org/content/10.1101/2023.12.13.571462v2.full); published as [Nat Commun 2024](https://www.nature.com/articles/s41467-024-51844-2)
- **VERIFIED.** bindEmbed21DL predicts binding residues for metal ions, nucleic acids and small molecules from ProtT5 last-layer 1024-d embeddings with a "relatively shallow two-layer CNN", outperforming MSA-based predictions (F1 ≈ 43%). — [Littmann et al., Sci Rep 2021](https://www.nature.com/articles/s41598-021-03431-4); [bindPredict GitHub](https://github.com/Rostlab/bindPredict)
- **VERIFIED.** Light Attention (LA): two parallel 1D convolutions (filter size 9) give attention coefficients and values. Softmax over positions produces a weighted sum, concatenated with max pooling, then an FFN. With ProtT5 it reached Q10 = 86.0% on DeepLoc (~8 pp above the previous SOTA), but dropped ~22 pp to 65.2% on the new "setHARD" set, which the authors attribute to benchmark redundancy and bias. — [Stärk et al., Bioinformatics Advances 2021](https://academic.oup.com/bioinformaticsadvances/article/1/1/vbab035/6432029)
- **VERIFIED (search snippet of the paper).** LA costs about 29.5 M extra parameters to produce a 1280-d sequence embedding (ESM-2 650M input). Pool PaRTI is a parameter-free PageRank-on-attention alternative. — [Pool PaRTI, Bioinformatics 2025](https://academic.oup.com/bioinformatics/article/41/6/btaf330/8155125)
- **VERIFIED (search snippet of the paper).** PEER benchmark: "shallow CNN is a decent baseline model with competitive performance and low computational cost". It evaluates both frozen-PLM-plus-head and fine-tuned settings. — [PEER, NeurIPS 2022 D&B](https://papers.neurips.cc/paper_files/paper/2022/file/e467582d42d9c13fa9603df16f31de6d-Paper-Datasets_and_Benchmarks.pdf)
- **VERIFIED.** ProtBench (ddofer, GitHub, undated working paper) runs 62 tasks, including residue-level SS3/SS8, conservation and contacts, with only linear / torch-linear / kNN / gradient-boosted-tree probes. Linear and torch-linear "match within ~0.01 on six of eight tasks", and the README claims frozen probes "consistently outperform" costlier fine-tuning. No CNN head is included. — [ProtBench GitHub](https://github.com/ddofer/ProtBench)
- **VERIFIED.** Li et al. (ICML 2024) ran 370 transfer experiments using **linear / ridge** heads on per-layer representations. Most function tasks gain from pretraining but do not scale with it, relying instead on "low-level features learned early in pretraining". — [Li et al., PMLR 235](https://proceedings.mlr.press/v235/li24a.html); [bioRxiv full text](https://www.biorxiv.org/content/10.1101/2024.02.05.578959v2.full)
- **VERIFIED.** PMSFF (Biomolecules 2024) on ProtT5 1024-d: multi-size *windows* (5/15/25) with additive attention, multi-size *kernels* (3/5/7) with max-pool 5, and a BiGRU. Ablation on NSP448: kernels only gave F1 0.669 / AUROC 0.764 / AUPRC 0.469. Windows only gave 0.677 / 0.769 / 0.482. Both plus GRU gave 0.694 / 0.800 / 0.514. So multi-scale fusion adds roughly +0.03–0.045 AUPRC on protein-protein binding residues. This is the closest published "multi-window vs multi-kernel" ablation to mCNN. — [PMSFF, PMC11506650](https://pmc.ncbi.nlm.nih.gov/articles/PMC11506650/)
- **VERIFIED.** CFTR_TL (Ou group, ACS Omega 2025): mCNN on ProtT5-XL-U50 with parallel windows 6/8/10/12, chosen after testing window lengths 2–12; max-pool per branch, concatenation, then FC. 512 filters was optimal. The only baselines were **SVM, KNN, RF**, with no other neural head. Reported MCC 0.4284 alongside AUC 0.9863 and sensitivity/specificity ≈ 0.95 on heavily imbalanced data (e.g., ATP-388: 4,706 positive vs 117,599 negative residues). — [CFTR_TL, PMC12676287](https://pmc.ncbi.nlm.nih.gov/articles/PMC12676287/); code [B1607/CFTR_TL](https://github.com/B1607/CFTR_TL)
- **VERIFIED (search snippet).** One DNA-binding-site study found CNN beat MLP and RNN backbones on the same PLM features ("CNN was more suitable for this residue-level prediction task"). — [arXiv 2306.15912](https://arxiv.org/pdf/2306.15912)
- **VERIFIED.** PIPENN-EMB, an ensemble of U-Net, ResNet and RNN on ProtT5-XL embeddings for protein-protein interfaces, reached MCC 0.313 vs 0.249 for the older handcrafted-feature PIPENN and generalised to <30% and <15% identity test sets. The comparison is embeddings vs handcrafted features, not head vs head. — [PIPENN-EMB, Sci Rep 2025](https://www.nature.com/articles/s41598-025-88445-y); [bioRxiv](https://www.biorxiv.org/content/10.1101/2024.10.31.621117v1)

### Inferences
- **INFERRED.** A CNN head should help when the label depends on a *local* window of residues: binding residues, PTM sites, disorder. Per-residue PLM embeddings already encode context, so the head's job is to sharpen local consistency. Evidence: Rostlab's consistent 2-layer CNN choice, the PMSFF ablation, and CNN > MLP/RNN in arXiv 2306.15912. For per-protein classification (transporter families, localisation), LA or mean-pool + FFN is the stronger comparison, and an mCNN there needs to beat LA, not just SVM/RF.
- **INFERRED.** Because the Ou–Ho papers never compare mCNN against (a) a linear probe on the centre-residue embedding, (b) an MLP on the flattened 15×1024 window, or (c) a bindEmbed21DL-style 2-layer full-sequence CNN, it is unknown how much of their reported performance comes from the multi-window head and how much from ProtT5 itself. This is a falsifiable, cheap question.
- **INFERRED.** CFTR_TL's numbers (AUC 0.986, MCC 0.43) show the AUC/MCC gap typical of ~4% positive data. Any head comparison must report AUPRC and MCC at a validation-chosen threshold, or differences between heads will be invisible.

### Gaps
- I found no paper that benchmarks linear / MLP / CNN / mCNN / BiLSTM / LA / small transformer heads on identical frozen embeddings for **ligand-binding residues** under a similarity-aware split. PEER and ProtBench cover only a few heads, and their residue tasks are mostly SS and contacts.
- I could not verify bindEmbed21DL's exact kernel size or parameter count (paper not fetched in full).
- Schmirler's supplementary may include head ablations. Only the main text was checked.

---

## Q2. Window size and receptive field: sliding fragment vs full-sequence convolution, dilated convs, multi-scale fusion, attention vs max pooling

### Takeaway
Published multi-scale evidence is consistent but modest: combining several kernel or window sizes adds a few AUPRC points (PMSFF), and the Ou group's own ablation picks 6–12-residue windows. **The sliding-fragment input format is the main cause of the ~6 GB-per-dataset storage problem.** For a stride-1, per-residue mCNN it can, by my analysis, be rewritten as a full-sequence convolution with identical receptive field and about 15× less storage. Dilated stacks (emb2dis, AlloPED) and attention pooling (LA) are the published alternatives for widening context. None has been compared head-to-head against mCNN.

### Cited Findings
- **VERIFIED.** CFTR_TL tested window lengths 2–12; the combination {6, 8, 10, 12} "achieved the best balance". — [CFTR_TL](https://pmc.ncbi.nlm.nih.gov/articles/PMC12676287/)
- **VERIFIED.** PMSFF uses windows 5/15/25 and kernels 3/5/7. Each alone underperforms the combination (see Q1 numbers). — [PMSFF](https://pmc.ncbi.nlm.nih.gov/articles/PMC11506650/)
- **VERIFIED.** Light Attention uses convolution filter size 9 and runs in linear time in sequence length. Its pooling is softmax-weighted attention plus max-pool, not max-pool alone. — [Stärk et al. 2021](https://academic.oup.com/bioinformaticsadvances/article/1/1/vbab035/6432029)
- **VERIFIED (abstract).** emb2dis (bioRxiv, Mar 2026): disorder prediction from PLM embeddings with ResNets plus **dilated convolutions** to "enlarge the receptive field" and capture extended context. — [emb2dis](https://www.biorxiv.org/content/10.64898/2026.03.30.715414v1)
- **VERIFIED (abstract).** AlloPED-site (2025): dilated CNN on ProtT5 embeddings plus attention, for allosteric sites. — [AlloPED](https://www.biorxiv.org/content/10.1101/2025.03.28.645953v1.full)
- **VERIFIED (existing project note).** The group's `get_dataset.py -w 7` builds a (residues × 15 × dim) tensor. For TR735 (196,736 residues, 1024-d, fp16) that is ~6.0 GB for one dataset and one model, and "window expansion, not the raw embeddings, is what blows past Colab's disk". — [datasets-and-compute.md](../../bioinformatics-topic-survey/notes/datasets-and-compute.md) (arithmetic, not a measurement)
- **VERIFIED.** RAG-msCNN replaces mCNN's standard convs with depthwise-separable multi-scale convs to cut parameters. — [RAG-msCNN, BSPC 2025](https://doi.org/10.1016/j.bspc.2025.109407) (as summarised in [bioinformatics-topic-survey.md §1](../../bioinformatics-topic-survey/bioinformatics-topic-survey.md))

### Inferences
- **INFERRED (exact-equivalence argument, should be checked in code).** Consider an mCNN applied to a 15-residue fragment centred on residue *i*, with kernel *k*, "valid" convolution, then global max-pool over the fragment. It produces the same number as a convolution over the whole (zero-padded) sequence, followed by a stride-1 max-pool of width 15−k+1 centred at *i*. This holds provided terminal padding is handled identically (zero vectors in both). Two consequences:
  - Storage drops from 15 × L × 1024 to L × 1024 per protein, i.e. ~6 GB → ~0.4 GB for TR735.
  - Overlapping windows share convolution computation, so training should also be several times faster.
- **INFERRED.** Because ProtT5 per-residue embeddings already integrate whole-sequence context through self-attention, the head's receptive field probably matters less than for one-hot input. The open empirical question is whether 15 residues is "too much" (overfitting with 1024-d inputs on a few hundred proteins) or "too little" (missing info that dilated or full-sequence context would add).
- **INFERRED.** Max-pool over the window discards *where* in the window the signal is. Attention pooling (LA-style) or centre-weighted pooling might help residue-level tasks where the centre residue matters most. Nobody has ablated this for mCNN.

### Gaps
- No paper reports mCNN vs dilated CNN vs full-sequence 2-layer CNN on the same binding-site datasets.
- No published measurement of storage or training time of fragment vs full-sequence formulations for these pipelines. The ~6 GB figure is arithmetic.
- Not verified whether msCNN's depthwise-separable version changes accuracy on non-RAG settings (no ablation found in public sources).

---

## Q3. Efficiency directions: compression, smaller PLMs, half precision, layer selection, multi-layer fusion, distillation

### Takeaway
**Half precision is free** (Rostlab README, ProtT5). **Channel-wise compression of PLM embeddings is plausible** (CHEAP: intrinsic dimension far below 1024), but function information degrades first, and all published compression tests are protein-level or structure reconstruction, **not residue-level binding**. **Medium PLMs (ESM-2 150M/650M, ESM C 600M) match larger ones on protein-level transfer.** Layer evidence conflicts:
- Joeres 2026 and Li 2024 say the last layer is often not best, and early layers suffice for many function tasks.
- Vieira 2025 found the last layer most often best for ESM-C on DMS.
- For residue-level tasks, Joeres reports performance rising steadily across layers.

Distilled PLMs exist (DistilProtBert, MTDP 20M), but they are evaluated only on protein-level tasks and SS. All these together leave a clear "efficient mCNN" gap at residue level.

### Cited Findings
- **VERIFIED.** The ProtT5 half-precision encoder: embeddings "produced the same performance (established empirically by comparing on several downstream tasks)", "without any measurable performance-decrease", and the model is "fully usable on 8 GB of video RAM". No storage numbers are given. — [Rostlab/prot_t5_xl_half_uniref50-enc README](https://huggingface.co/Rostlab/prot_t5_xl_half_uniref50-enc)
- **VERIFIED.** CHEAP (Lu et al., Patterns 2025):
  - It compresses ESMFold-trunk embeddings by up to 128× along channels (1024 → 8) and up to 8× along length.
  - Sequence and backbone information "can be preserved nearly perfectly" down to 8 channels.
  - Function prediction varies by task (solubility robust, β-lactamase activity less so).
  - The source embeddings have "massive activations" (some channels ~3000× larger than others).
  - Code: [amyxlu/cheap-proteins](https://github.com/amyxlu/cheap-proteins). — [bioRxiv v2](https://www.biorxiv.org/content/10.1101/2024.08.06.606920v2.full); [Patterns](https://www.sciencedirect.com/science/article/pii/S2666389925001370)
- **VERIFIED (abstract).** Sahni, Chen, Estrada (bioRxiv, Jun 2026): low-dimensional PCA plus cubic-polynomial trajectories across layers lets protein-level embeddings at *any layer* be reconstructed without rerunning the PLM. Tested on ESM-35M and ESM-3B for PPI and localisation, it retains downstream performance. The abstract gives no exact ratio. — [Polynomial Trajectory Compression](https://www.biorxiv.org/content/10.64898/2026.06.05.730461v1)
- **VERIFIED.** Vieira et al. (Sci Rep 2025) compared ESM-2 8M→15B, ESM C 300M/600M/6B and AMPLIFY using LassoCV on 36–41 DMS sets and PISCES-derived targets.
  - Medium models (ESM-2 150M/650M, ESM C 600M) were "consistently good", often matching larger ones.
  - Mean pooling beat max pooling, BOS, PCA, kernel PCA and iDCT, by +5–20 pp R² on DMS and +20–80 pp on diverse sequences.
  - For ESM-C 300M, "the last layer was most commonly the top-performing layer".
  - ProtT5 was not included. — [Vieira et al., PMC11601519](https://pmc.ncbi.nlm.nih.gov/articles/PMC11601519/)
- **VERIFIED (abstract).** Joeres, Senatorov, Kolchina, Klakow, Kalinina (arXiv, Aug/Sep 2026) studied 13 PLMs × 15 tasks × 9 datasets.
  - "The last layers of PLMs rarely produced embeddings that led to the best results".
  - For residue-level tasks there is "a steady increase in performance across almost all PLM layers".
  - Their PLMSommelier tool predicts the best layer with ~98% accuracy and truncates the model, cutting inference time and memory. — [arXiv 2608.12090](https://arxiv.org/abs/2608.12090). *Conflict:* this contradicts Vieira 2025's last-layer finding for ESM-C on DMS. The difference is probably task-dependent (protein-level regression vs a broad mix).
- **VERIFIED.** Li et al. (ICML 2024): for thermostability and GB1, "the largest gains in performance occur in the first 3-5 layers" and then plateau. Secondary structure keeps improving with deeper layers and larger models. — [bioRxiv full text](https://www.biorxiv.org/content/10.1101/2024.02.05.578959v2.full)
- **VERIFIED.** DistilProtBert: 50% smaller and faster than ProtBert, with 98% less pretraining compute. Within ≤3 points of ProtBert on SS (CASP12 0.72, TS115 0.81, CB513 0.79) and on membrane vs soluble (0.86). — [Geffen et al., Bioinformatics 2022](https://academic.oup.com/bioinformatics/article/38/Supplement_2/ii95/6701995)
- **VERIFIED.** MTDP (Shang et al., Bioinformatics 2024): a 6-layer T5 student of ~20M parameters ("3% of ESM2-33, 1.6% of ProtT5-XL"), distilled from ESM-2 650M and ProtT5-XL with RL-based adaptive teacher selection and KL loss.
  - Within ±1.5% of teachers on protein-level tasks (membrane, localisation, GO, Tm, solubility).
  - ~70% less compute; runs on an RTX 2080Ti.
  - Code: [KennthShang/MTDP](https://github.com/KennthShang/MTDP). — [MTDP](https://academic.oup.com/bioinformatics/article/40/9/btae567/7772445). *(The fetch summary also called ProtT5-XL "~120M parameters", which is inconsistent with the 1.6% ratio. ProtT5-XL has ~1.2B parameters in the encoder–decoder, about half in the encoder. Treat the 120M figure as an extraction error.)*
- **VERIFIED.** Wijaya (bioRxiv 2026) distilled ProtGPT2 (738M, generative) into 37–194M students. Peak GPU memory fell from 3.2 GB to 170 MB and inference was 2.4–5.3× faster. Only generative and fine-tuning metrics were evaluated, not residue-level classification. — [Distilling PLMs with Complementary Regularizers](https://www.biorxiv.org/content/10.64898/2026.02.17.706304v3.full)
- **VERIFIED (project note).** Under the existing budget, embedding *extraction* is cheap (a few GPU-hours for 5 PLMs × 4 datasets). The binding constraints are storage and the number of training runs. Colab Pro's 100 CU ≈ 18.5 A100-hours per month. — [datasets-and-compute.md](../../bioinformatics-topic-survey/notes/datasets-and-compute.md)

### Inferences
- **INFERRED.** For the group's datasets, the largest storage saving is not compression but avoiding window expansion (Q2, ~15×). fp16 adds 2× over fp32, int8 2× over fp16, and PCA 1024 → 128 gives 8×. Stacked, these could take a ~6 GB dataset to tens of MB, small enough to run many seeds and many datasets on Kaggle.
- **INFERRED.** For residue-level binding, ProtT5 layer choice is genuinely open. Joeres says residue tasks improve towards later layers; Li says function tasks saturate early. A layer sweep (or learned scalar mix over layers) feeding the mCNN is cheap if done per-protein at full-sequence storage. It is also directly useful to the group: a truncated encoder (e.g., 12 of 24 layers) halves extraction cost, fitting their "accept less accuracy for half the compute" stance in RTK_RAG.
- **INFERRED.** No paper tests whether a 20–150M backbone (ESM-2 35M/150M, MTDP) plus mCNN stays within ~0.02 AUPRC of ProtT5 plus mCNN on binding residues. This is a low-risk Pareto study whose result is publishable either way.

### Gaps
- No protein-specific study of **int8 or product quantization of per-residue PLM embeddings** was found. Search results were all about generic text-embedding retrieval (e.g., [Sentence-Transformers docs](https://sbert.net/examples/sentence_transformer/applications/embedding-quantization/README.html)). This is genuine open space, but nothing can be cited for its effect.
- No residue-level binding evaluation of CHEAP, polynomial-trajectory compression, DistilProtBert or MTDP was found.
- No ProtT5-specific layer sweep for binding residues was found. Joeres 2026's per-model details (whether ProtT5 is included, which residue tasks) were seen only through the abstract.
- A search snippet claimed fp16 cut storage "from 3.1 TB to 406 GB", but I could not trace it to a primary source. It is excluded.

---

## Q4. Robustness, interpretability and calibration of CNN heads on PLM embeddings

### Takeaway
Robustness is the weakest-studied axis. LA's 22-pp drop on setHARD shows how much benchmark redundancy can inflate head results. Classic CNN filter interpretation (filters as PWMs) **does not transfer directly**, because filters act on 1024-d contextual embeddings, not one-hot amino acids. Interpretation therefore has to go through attribution to residues or through SAE/concept probes in embedding space. Calibration of mCNN heads has not been reported.

### Cited Findings
- **VERIFIED.** LA + ProtT5 fell from 86.0% (DeepLoc test) to 65.2% (setHARD, a new non-redundant set). The authors warn that static benchmarks mask real limitations. — [Stärk et al. 2021](https://academic.oup.com/bioinformaticsadvances/article/1/1/vbab035/6432029)
- **VERIFIED.** PIPENN-EMB reports stable AUC-ROC on test sets with <30% and even <15% identity to training, for ProtT5 embeddings plus a CNN/RNN ensemble. — [PIPENN-EMB](https://www.nature.com/articles/s41598-025-88445-y)
- **VERIFIED (abstract/snippet).** For DNA one-hot CNNs, motif information is distributed across multiple filters "in a non-trivial way, preventing immediate interpretation". — [Circularly shifted filters, bioRxiv](https://www.biorxiv.org/content/10.1101/312959.full.pdf)
- **VERIFIED (abstract).** InterPLM: sparse autoencoders on ESM-2 find up to 2,548 interpretable latent features per layer, correlated with binding sites, motifs and domains. — [InterPLM, bioRxiv 2024](https://www.biorxiv.org/content/10.1101/2024.11.14.623630v1.full)
- **VERIFIED (title/snippet).** Concept Activation Vectors have been used to localise motifs directly in PLM embedding space. — [arXiv 2511.21614](https://arxiv.org/pdf/2511.21614)
- **VERIFIED (earlier survey).** Calibration and conformal prediction for protein function: CPEC. — [CPEC, PLOS Comput Biol 2024](https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1012135)

### Inferences
- **INFERRED.** A CNN-specific interpretability question unique to mCNN: **which window branch carries the signal?** A per-branch ablation or attribution (e.g., integrated gradients per branch) is cheap and novel for this architecture family. It overlaps with the earlier survey's "motif + conformal for ATP" idea, so it is better as a chapter than as the whole thesis.
- **INFERRED.** Heads with many parameters (mCNN with 512 filters × 4 windows on 1024-d) trained on a few hundred proteins are likely to be over-confident. Temperature scaling plus expected calibration error is a one-day add-on to any of the ideas below.

### Gaps
- No study of CNN filter visualisation on PLM-embedding inputs, and no robustness study (e.g., homology-stratified performance) specific to mCNN/msCNN heads, was found.

---

## Q5. Combining embeddings from multiple PLMs (ProtT5 + ESM-2 + ProstT5) in CNN heads: fusion strategies

### Takeaway
Multi-PLM fusion is common but almost always naive (concatenation or late score/decision fusion), with small and inconsistently measured gains. It also multiplies storage, which conflicts with the group's compute-saving taste. The open, group-compatible question is **fusion at a fixed storage or parameter budget**, e.g., compress each PLM before fusing.

### Cited Findings
- **VERIFIED.** LM-OGlcNAc-Site (IJMS 2023) fused Ankh, ESM-2 and ProtT5 by score averaging or hard voting over per-PLM FFNNs. Decision fusion raised accuracy from 71.4–71.5% to 85.9%, but MCC only from 0.133 to 0.166, so the accuracy jump is largely a threshold/imbalance effect. — [PMC10650050](https://pmc.ncbi.nlm.nih.gov/articles/PMC10650050/)
- **VERIFIED.** ESM-SECP (BMC Genomics 2025) fuses ESM-2 650M with PSSM via separate 1D-CNN branches and 8-head cross-attention. On TE46, AUC 0.8978 vs 0.8821 (ESM-2 alone) and MCC 0.4946 vs 0.4502. On TE129, AUC 0.9149 vs 0.9011 and MCC 0.4891 vs 0.4358. — [PMC12577266](https://pmc.ncbi.nlm.nih.gov/articles/PMC12577266/)
- **VERIFIED (snippet).** Concatenating ProtT5 and ProstT5 residue embeddings is reported to improve binding residue prediction (GraphPBSP). MPBind uses ProtTrans + ProstT5 with an EGNN for multi-ligand prediction. — [GraphPBSP, IJBM 2024](https://www.sciencedirect.com/science/article/abs/pii/S0141813024077420); [MPBind, Bioinformatics 2025](https://academic.oup.com/bioinformatics/article/41/11/btaf589/8300842)
- **VERIFIED (snippet).** FusPB-ESM2 fuses ProtBERT and ESM-2 for cell-penetrating peptides. — [FusPB-ESM2](https://www.researchgate.net/publication/380692823_FusPB-ESM2_Fusion_Model_of_ProtBERT_and_ESM-2_for_Cell-Penetrating_Peptide_Prediction)
- **VERIFIED (snippet).** With identical ML heads, ProtT5 slightly beat ESM-2 for binding in disordered regions, and ProtT5-XL beat ESM-2 for interface prediction (F1 0.492 vs 0.440, MCC 0.376 vs 0.312). — [Sci Rep 2024, disordered binding](https://www.nature.com/articles/s41598-024-64211-4); [PIPENN-EMB](https://www.nature.com/articles/s41598-025-88445-y)

### Inferences
- **INFERRED.** Fusion gains of ~0.03–0.05 MCC are of the same order as seed variance on small test sets of ~40–130 proteins. Without multiple seeds and confidence intervals, published fusion gains are hard to trust.
- **INFERRED.** In an mCNN, a natural CNN-native fusion design is one branch per PLM (or per PLM × window) with a learned gate, compared against early concatenation at equal total channels after PCA. This is cheap to run on stored embeddings.

### Gaps
- No paper found comparing early / late / gated fusion of ProtT5 + ESM-2 + ProstT5 inside a multi-window CNN, or at equal storage budget.

---

## Q6 (objective). Ranked CNN-centred thesis ideas

### Takeaway
The strongest CNN-centred ideas reuse the group's own pipeline and datasets, ask a falsifiable question about the head or the input representation, and save compute. They avoid adding another bolt-on module. Ideas 1 and 2 can be merged into one thesis (an "efficient and justified mCNN"), with Idea 3 or 4 as a chapter. LoRA appears only as an optional side comparison.

### Cited Findings
(The ideas below are built on the findings cited in Q1–Q5. No additional sources.)

### Inferences
All entries are **INFERRED** recommendations. Compute estimates are my estimates under Kaggle T4/P100 plus a small Colab Pro budget. Ranking is by novelty-to-risk for a 4–6-month IT student; the decision is the student's.

**1. Storage-efficient, fragment-free mCNN with compressed embeddings ("same accuracy, ~100× less disk")**
- *Idea:*
  - Re-implement mCNN/msCNN as a full-sequence convolution with centred max-pool, provably equivalent to the 15-residue fragment version.
  - Then stack fp16 → int8 → PCA (1024 → 512/256/128/64) and, optionally, product quantization on stored per-residue ProtT5 embeddings.
  - Measure accuracy (AUPRC, MCC at a validation threshold), disk, RAM, training time and inference latency on 3–4 of the group's datasets (e.g., DNA TR735/TE, ATP-388, FAD, NAD).
- *Closest prior work:* Ou group's fragment pipeline (RAG_DNA_RNA `get_dataset.py`); bindEmbed21DL's full-sequence 2-layer CNN; CHEAP (protein-level and structure compression); polynomial trajectory compression (protein-level); ProtT5 fp16 README.
- *New vs Ou–Ho:* removes the ~6 GB/dataset bottleneck the group actually has. First residue-level binding-site evaluation of quantization and PCA on PLM embeddings.
- *Compute:* very low. Extraction once (<1 GPU-h per dataset); each training run takes minutes.
- *Risk:* low technically. Moderate "too engineering-y" risk for a research thesis, so it should be paired with Idea 2 or 3.
- *Kill criterion:* if the equivalence check fails (outputs differ beyond fp tolerance) and the full-sequence version loses >0.01 AUPRC, report it as a negative result and pivot to Idea 2. If PCA-128 loses >0.03 AUPRC on all datasets, keep only fp16/int8.

**2. "Does the multi-window CNN matter?" A controlled head ablation for binding residues**
- *Idea:* on identical frozen ProtT5 embeddings, identical similarity-aware splits, ≥5 seeds, and AUPRC + MCC (validation-chosen threshold) + parameters + FLOPs, compare:
  - logistic regression on the centre residue
  - MLP on centre residue and on the flattened window
  - 2-layer full-sequence CNN (bindEmbed21DL-style)
  - mCNN (group's settings)
  - msCNN (depthwise-separable)
  - dilated CNN
  - LA-style attention pooling
  - BiLSTM/BiGRU
  - one small transformer layer

  Also vary window (7/15/25/full) and pooling (max / attention / centre-weighted).
- *Closest prior work:* PMSFF ablation; PEER (shallow CNN baseline); Schmirler (2-layer CNN default); LA; CFTR_TL (mCNN vs SVM/KNN/RF only).
- *New vs Ou–Ho:* the group has never compared mCNN against other neural heads. This answers "is mCNN's gain real, and when?" and yields an accuracy-vs-parameters Pareto front.
- *Compute:* low. About 10 heads × 4 datasets × 5 seeds × 5 folds ≈ 1,000 short runs, feasible on Kaggle within weeks if Idea 1's storage fix is applied first.
- *Risk:* scientific risk low, since any outcome is reportable. Relational risk moderate if mCNN ≈ 2-layer CNN, so frame it as "characterising the design space", not "debunking".
- *Kill criterion:* none in the classic sense. If all heads fall within seed variance, that itself is the finding. Shift the emphasis to efficiency (smallest head that matches).

**3. Which ProtT5 layer(s) should feed the mCNN? Layer selection, multi-layer fusion, truncated encoder**
- *Idea:* extract all 24 ProtT5 encoder layers for one or two datasets (full-sequence storage, fp16, possibly PCA). Compare last layer, best single layer, a learned scalar mix (ELMo-style), and a **truncated encoder** (first *n* layers) feeding mCNN. Report accuracy against extraction cost.
- *Closest prior work:* Joeres et al. 2026 (PLMSommelier, last layer rarely best); Li et al. ICML 2024 (early layers suffice for function); Vieira 2025 (last layer best for ESM-C on DMS).
- *New vs Ou–Ho:* the group always uses the last layer. A truncated ProtT5 halving extraction compute is exactly the trade-off the group values.
- *Compute:* low–medium. 24× storage if all layers are kept, so use a small dataset or store PCA'd layers. Extraction is a few GPU-hours.
- *Risk:* moderate. Joeres 2026 may already include ProtT5 and residue-level binding tasks, so check the full text first.
- *Kill criterion:* if the last layer is within one seed-SD of the best layer on all datasets, and truncating to ≤18 layers loses >0.02 AUPRC, report it briefly and fold it into Idea 1 or 2 as a chapter.

**4. How small can the backbone be? Small/distilled PLMs + mCNN vs ProtT5 + mCNN (Pareto study)**
- *Idea:* replace ProtT5-XL (≈1.2B) with ESM-2 8M/35M/150M/650M, ESM C 300M/600M, MTDP (20M distilled) and DistilProtBert, keeping the same mCNN. Plot AUPRC against extraction time, GPU memory and embedding size for 3–4 binding datasets.
- *Closest prior work:* Vieira 2025 (protein-level only, no ProtT5); MTDP and DistilProtBert (protein-level/SS only); RTK_RAG embedding table (group rejected ESM-2 3B on compute grounds).
- *New vs Ou–Ho:* the first residue-level binding Pareto front, the natural complement to the group's ESM-2-3B decision.
- *Compute:* low. Small models extract in minutes.
- *Risk:* low. A possible "boring" result if ProtT5 wins clearly, but the Pareto front is still a deliverable.
- *Kill criterion:* if every model ≤150M loses >0.05 AUPRC on all datasets, stop adding models after three and merge into Idea 2's paper as a section.

**5. Fusion of multiple PLMs at a fixed storage budget inside mCNN**
- *Idea:* ProtT5 + ProstT5 (AA mode) + ESM-2 650M, each PCA-reduced so the total channels equal 1024 (or 512). Compare early concatenation, per-PLM branches with a learned gate, and late score fusion against ProtT5 alone at the same budget.
- *Closest prior work:* LM-OGlcNAc (late fusion; small MCC gain); ESM-SECP (cross-attention fusion with PSSM); GraphPBSP and MPBind (ProtT5 + ProstT5 concatenation).
- *New vs Ou–Ho:* fusion "for free" in storage terms. Directly addresses the group's reason for rejecting bigger embeddings.
- *Compute:* low–medium (3 extractions per dataset).
- *Risk:* moderate. Gains may sit within seed variance.
- *Kill criterion:* if equal-budget fusion beats ProtT5-alone by less than the 95% CI of seed variance on ≥3 of 4 datasets, conclude "no free lunch" and stop.

**6. Distilling ProtT5 + mCNN into a tiny sequence-only CNN (no PLM at inference)**
- *Idea:* train a teacher (ProtT5 + mCNN). Then train a small student that takes one-hot or ESM-2 8M input, using the teacher's soft per-residue labels and (optionally) feature matching to the teacher's mCNN features. Measure the gap and the inference speed-up.
- *Closest prior work:* MTDP and Wijaya 2026 (PLM-level distillation, not task-head distillation); DistilProtBert.
- *New vs Ou–Ho:* produces a deployable predictor without ProtT5, a strong efficiency story.
- *Compute:* medium (student training on many residues, still small).
- *Risk:* high. One-hot students may fall far short. Unlabelled proteins for distillation would need to be sourced (e.g., UniProt subsets), which adds data work.
- *Kill criterion:* if after ~4 weeks the student (ESM-2 8M input) is >0.10 AUPRC below the teacher on the main dataset, stop and keep it as a negative-result section.

**7. Interpretable and calibrated mCNN: which window branch matters, and are probabilities trustworthy? (chapter-sized)**
- *Idea:* per-branch ablation and attribution, residue-level integrated gradients compared against known motifs (e.g., Walker A for ATP), and temperature scaling plus ECE for each head from Idea 2.
- *Closest prior work:* the earlier survey's Idea 4 (MotifAE, InterPLM, CPEC); circular-filter work on DNA CNNs.
- *New vs Ou–Ho:* the group shows SHAP figures but no quantitative attribution or calibration.
- *Compute:* very low.
- *Risk:* biology knowledge needed for motif validation; overlaps with the existing proposal.
- *Kill criterion:* not stand-alone. Attach to Idea 2.

**Suggested combination (INFERRED, the student decides):** a thesis titled roughly "Efficient multi-window CNN heads on frozen protein-language-model embeddings for binding-residue prediction". Chapter A = Idea 1 (fragment-free plus compression), chapter B = Idea 2 (head ablation), chapter C = Idea 3 or 4 (layer or backbone Pareto), optional chapter D = calibration (Idea 7), plus a LoRA side comparison only if time remains. This uses one pipeline and the same datasets throughout, and every chapter saves compute or justifies a design choice the group already makes.

### Gaps
- Joeres et al. 2026 and emb2dis were read only at abstract level. Before committing to Idea 3, check whether Joeres already evaluates ProtT5 on binding residues.
- Whether the group's datasets (TR735/TE, ATP-388, FAD/NAD sets) can be re-split by sequence similarity without too few positives in the test set is unverified. See the leakage notes in the earlier survey.
- The advisors' appetite for an "ablation/efficiency" thesis vs a "new module" thesis is unknown. Only their publication behaviour (accepting lower accuracy for half the compute; msCNN built to cut parameters) suggests efficiency ideas are welcome.
