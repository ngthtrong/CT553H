# Cross-cutting capabilities for contribution criteria 3, 4, 5: XAI, "beyond PLM" methods, and web applications

> **LƯU TRỮ — không dùng để ra quyết định.** Tài liệu lịch sử; mọi câu "chốt / quyết định / khuyến nghị" bên dưới đã hết hiệu lực. Trạng thái hiện hành: [DECISIONS.md](../../../../DECISIONS.md).

> Research notes for CT553H thesis topic selection. Date of research: 2026-10-02.
> Scope: toolbox-oriented, not a literature survey. Every quantitative claim carries a URL and a verification marker:
> **[FULL TEXT]** = I fetched and read the article/doc page itself; **[ABSTRACT]** = I only have abstract-level or official-metadata text; **[SEARCH SNIPPET — NOT VERIFIED]** = the figure came from a search-engine summary of a page I did not fetch, so treat it as unconfirmed; **[ESTIMATE — MINE]** = my own engineering judgement, not from a source.
> Constraint frame used throughout: 1 student, Software Engineering dept., 8–9 weeks of execution after topic is fixed at week 6, no confirmed local GPU (Colab/Kaggle free tier only), existing skills = frozen ProtT5 embeddings + residue windows + multi-window CNN + leakage-controlled evaluation + CD-HIT clustering; has NEVER trained a GNN or fine-tuned a PLM.

---

## (a1) Which explainability methods are actually used and publishable in protein-sequence deep learning in 2024–2026?

### Takeaway
The methods that actually appear in 2024–2026 protein-sequence prediction papers are a narrow, cheap subset: **SHAP (GradientExplainer / DeepExplainer / TreeSHAP), integrated gradients (via Captum), attention-weight analysis of the PLM encoder, and attribution mapped onto known functional regions/motifs**. The heavier and more fashionable methods (sparse autoencoders, TCAV-style concept probing, counterfactual optimisation) exist in 2025–2026 but live in high-end venues (Nature Methods, Nature Machine Intelligence) or arXiv preprints, not in the typical msCNN-style application paper.

### Cited Findings

**Field-level review (the single best citation for "XAI in PLMs is a recognised agenda").**
- "Toward the Explainability of Protein Language Models" organises XAI for PLMs around **four information contexts**: training sequences, input prompt, model architecture, input–output pairs; and identifies **five roles** for XAI — Evaluator, Multitasker, Engineer, Coach, Teacher — of which **"Evaluator" is stated to be the only widely adopted role today**. It calls for community benchmarks, open-source tooling, domain-specific visualisations and wet-lab characterisation, and flags security risks, trustworthiness and bias as open concerns. — [arXiv:2506.19532](https://arxiv.org/abs/2506.19532) **[ABSTRACT]** (link resolved; the abstract page did not enumerate individual XAI techniques)
- The same work appears as a journal review: "Towards the explainability of protein language models", Nature Machine Intelligence, article s42256-026-01232-w — [nature.com/articles/s42256-026-01232-w](https://www.nature.com/articles/s42256-026-01232-w) **[SEARCH SNIPPET — NOT VERIFIED]** (I did not fetch this page; the arXiv version above is the verified one)
- A PDF of the full preprint is at [arxiv.org/pdf/2506.19532](https://arxiv.org/pdf/2506.19532) and it states that prior work on protein models "relies on attention visualization, feature attribution, gradient-based structure perturbation, or sparse autoencoders" — **[SEARCH SNIPPET — NOT VERIFIED]** (quoted from search summary of the PDF)

**Attention-weight analysis + SHAP in a predictor almost identical in shape to the advisor's pipeline — see (a3) for detail.**
- LMCrot (ProtT5-XL-UniRef50 + CNN/BiLSTM ensemble, crotonylation site prediction) used **(i)** normalised attention weights from the **final block of the ProtT5 encoder, averaged over heads**, visualised as heatmaps, and **(ii)** SHAP with the **GradientExplainer** (expected-gradients) variant over the 1024 ProtT5 embedding dimensions. — [Bioinformatics 40(5):btae290, May 2024](https://academic.oup.com/bioinformatics/article/40/5/btae290/7658304) **[FULL TEXT]**

**Integrated gradients via Captum is the standard route for PLM-fed networks.**
- Captum is the PyTorch interpretability library containing "general purpose implementations of integrated gradients, saliency maps, smoothgrad, vargrad and others". — [captum.ai/api/integrated_gradients.html](https://captum.ai/api/integrated_gradients.html) and [github.com/meta-pytorch/captum](https://github.com/meta-pytorch/captum) **[SEARCH SNIPPET — NOT VERIFIED]** (official docs; description is uncontroversial)
- Concrete protein use: "Integrated Gradient values were calculated by the Captum package to scrutinize the predictive contribution of each feature in ESM-2 models." — [PMC10818170, interpretable feature extraction in ESM2 for protein localization](https://pmc.ncbi.nlm.nih.gov/articles/PMC10818170/) **[SEARCH SNIPPET — NOT VERIFIED]**
- Captum's own reference paper: [arXiv:2009.07896](https://arxiv.org/pdf/2009.07896) **[SEARCH SNIPPET — NOT VERIFIED]**

**Three XAI methods stacked in one 2025 Briefings in Bioinformatics paper (useful template).**
- ESM2_AMP (binary protein–protein interaction prediction) used **attention weights across Transformer layers**, **integrated gradients (on an autoencoder+DNN variant)**, and **Tree SHAP (on an autoencoder+random-forest variant)**. — [Briefings in Bioinformatics 26(4):bbaf434, 2025, DOI 10.1093/bib/bbaf434](https://academic.oup.com/bib/article/26/4/bbaf434/8242608) **[FULL TEXT]**

**Sparse autoencoders (the 2025 frontier method for PLM interpretability).**
- InterPLM trains sparse autoencoders on **ESM-2** embeddings and "identifies thousands of interpretable features highlighting biological concepts including binding sites, structural motifs and functional domains"; it reports **up to 2,548 human-interpretable latent features per layer** correlating with **up to 143 known biological concepts**; it argues individual neurons show much weaker concept alignment, i.e. PLMs store concepts **in superposition**. Published **Nature Methods 22:2107–2117 (2025)**, authors Elana Simon and James Zou. Code: [github.com/ElanaPearl/interPLM](https://github.com/ElanaPearl/interPLM); paper: [nature.com/articles/s41592-025-02836-7](https://www.nature.com/articles/s41592-025-02836-7); preprint [biorxiv 2024.11.14.623630](https://www.biorxiv.org/content/10.1101/2024.11.14.623630v1) / [arXiv:2412.12101](https://arxiv.org/pdf/2412.12101) **[SEARCH SNIPPET — NOT VERIFIED]** (figures come from a search summary; I did not fetch the Nature Methods page)
- A follow-on applies sparse-autoencoder features of **ESMC** to enzyme function prediction — [arXiv:2606.12209](https://arxiv.org/pdf/2606.12209) **[SEARCH SNIPPET — NOT VERIFIED]**
- A related 2025 line: "Automated Neuron Labelling Enables Generative Steering and Interpretability in Protein Language Models" — [arXiv:2507.06458](https://arxiv.org/pdf/2507.06458) **[SEARCH SNIPPET — NOT VERIFIED]**

**Sequence logos from learned CNN filters (classic, cheap, directly applicable to an mCNN).**
- The standard recipe: "scanning each filter across test sequences, extracting subsequences centered on large activations, and aligning them to construct position frequency matrices visualized as sequence logos"; equivalently, extract kernel weights or maximally-activating subsequences and render as PWMs. — [ScienceDirect S2452310020300032, deep learning for inferring TF binding sites](https://www.sciencedirect.com/science/article/pii/S2452310020300032) **[SEARCH SNIPPET — NOT VERIFIED]**
- Important caveat from the same literature: "Only several best-recovered motifs can be equated to true motifs, as most kernels act during training to increase generalization ability, with such auxiliary kernels producing noise" — same source **[SEARCH SNIPPET — NOT VERIFIED]**
- Reference implementation style for interpretable convolution-based hybrids in genomics: [biorxiv 2021.07.13.452181](https://www.biorxiv.org/content/10.1101/2021.07.13.452181.full.pdf) **[SEARCH SNIPPET — NOT VERIFIED]**

**In-silico (saturation) mutagenesis and counterfactuals.**
- ISM definition: "constructing mutant sequences that each contain one mutation relative to the reference sequence, and attribution values are calculated as the difference in output between the mutant sequences and the reference sequence." — summarised from [arXiv:2602.01230, Toward Interpretable and Generalizable AI in Regulatory Genomics](https://arxiv.org/html/2602.01230v1) **[SEARCH SNIPPET — NOT VERIFIED]**
- Speed-ups exist because naive ISM is expensive: **fastISM** ([ResearchGate 358999265](https://www.researchgate.net/publication/358999265_fastISM_Performant_in-silico_saturation_mutagenesis_for_convolutional_neural_networks)), **compressed-sensing ISM** ([PMC9272795](https://pmc.ncbi.nlm.nih.gov/articles/PMC9272795/)), **first-order Taylor approximation of ISM** ([ScienceDirect S2589004224020327](https://www.sciencedirect.com/science/article/pii/S2589004224020327)) **[SEARCH SNIPPET — NOT VERIFIED]**
- Counterfactuals for proteins (2026, frontier): MCCOP / "Manifold-Constrained Counterfactual Optimization for Proteins" "computes minimal, biologically plausible sequence edits that flip a model's prediction to a desired target state… not just why a protein is predicted to fail, but how to rescue it." — [arXiv:2603.10811](https://arxiv.org/html/2603.10811v1) **[SEARCH SNIPPET — NOT VERIFIED]**

**Attention-guided saliency as an explicit method contribution (2026).**
- AttnGen: "Attention-Guided Saliency Learning for Interpretable Genomic Sequence Classification" — [arXiv:2605.14073](https://arxiv.org/html/2605.14073v1) **[SEARCH SNIPPET — NOT VERIFIED]** (genomic rather than protein, but the framing "learn the saliency, don't just read it off" is directly transferable)

### Inferences
- The publishable-and-cheap core for this student is: **SHAP GradientExplainer over PLM embedding dimensions + PLM attention-weight heatmaps + per-position attribution aligned against known functional annotation + in-silico single-residue mutagenesis**. All four are precedented in *Bioinformatics* and *Briefings in Bioinformatics* in 2024–2025, which is exactly the venue tier the advisor publishes in.
- **LIME, DeepLIFT proper, and layer-wise relevance propagation (LRP) did not surface in any 2024–2026 protein-sequence paper I found.** DeepLIFT appears only indirectly, as the algorithmic basis of SHAP's DeepExplainer. LRP and TCAV appear not at all in my searches of this subfield. Treat them as "defensible to mention, but no local precedent" — using them would be a differentiator but carries reviewer-unfamiliarity risk.
- Sparse autoencoders are the single most "2025-2026 current" XAI direction for PLMs, and InterPLM ships code. But it is an *unsupervised dictionary learning* project on top of a PLM, which is a different workload from the student's window-CNN pipeline — it is a plausible stretch goal, not a safe core.

### Gaps
- I did not find a protein-sequence paper using **TCAV / concept activation vectors** or **layer-wise relevance propagation**. I cannot confirm whether any exist; my searches were method-name based and may have missed them.
- I did not find a head-to-head benchmark comparing XAI methods *on protein residue-level predictors*. Benchmarks I found are genomics/medical-imaging.

---

## (a2) Which XAI methods have ready implementations for ESM-2/ProtT5 → CNN or graph, and what do they cost on a free-tier GPU?

### Takeaway
Everything the student needs is one `pip install` away (`shap`, `captum`, `logomaker`, `torch-geometric` for graph explainers). The cost ordering is stark: gradient-based methods (integrated gradients, saliency, GradientExplainer SHAP) cost a small constant multiple of one forward pass and are trivially affordable; KernelExplainer SHAP and naive saturation mutagenesis are the two traps that can blow a free-tier GPU budget.

### Cited Findings

**Library availability.**
- `shap` (official repo [github.com/shap/shap](https://github.com/shap/shap), PyPI [pypi.org/project/shap](https://pypi.org/project/shap/0.20.2/)) exposes **KernelExplainer** (model-agnostic), **DeepExplainer** (Deep SHAP, NN-specific, based on the connection between SHAP and **DeepLIFT**), **GradientExplainer** (expected gradients, based on the connection between SHAP and **integrated gradients**), and **TreeExplainer/TreeSHAP** (tree models). — [github.com/shap/shap](https://github.com/shap/shap), [shap issue #1687 on DeepExplainer vs GradientExplainer assumptions](https://github.com/shap/shap/issues/1687) **[SEARCH SNIPPET — NOT VERIFIED]**
- `captum` (PyTorch, Meta) provides integrated gradients, saliency, SmoothGrad, VarGrad and more, and works on any `nn.Module`, therefore on a CNN or GNN head fed by frozen ProtT5/ESM-2 embeddings. — [github.com/meta-pytorch/captum](https://github.com/meta-pytorch/captum) **[SEARCH SNIPPET — NOT VERIFIED]**

**Relative compute cost (the key practical ordering).**
- "KernelExplainer is slower than other model type-specific algorithms" because it is model-agnostic; it "computes approximate values in exponential time". — [github.com/shap/shap](https://github.com/shap/shap) **[SEARCH SNIPPET — NOT VERIFIED]**
- "Kernel SHAP is very slow (30–500× slower than TreeSHAP)". — [glassalpha.com/guides/how-to/choose-explainer/](https://glassalpha.com/guides/how-to/choose-explainer/) **[SEARCH SNIPPET — NOT VERIFIED; third-party vendor guide, low source quality — do not quote this ratio in the thesis without re-verification]**
- DeepExplainer "computational time scales linearly with the number of [background] samples"; "GradientExplainer is slower than DeepExplainer and makes different approximation assumptions". — [github.com/shap/shap](https://github.com/shap/shap) and [shap#1687](https://github.com/shap/shap/issues/1687) **[SEARCH SNIPPET — NOT VERIFIED]**
- Gradient-based explanations "can be noisy and sensitive to small perturbations, while perturbation-based methods are often computationally expensive" — i.e. the cost/stability trade-off is acknowledged in the genomics XAI literature. — [arXiv:2605.14073 AttnGen](https://arxiv.org/html/2605.14073v1) **[SEARCH SNIPPET — NOT VERIFIED]**
- Naive in-silico saturation mutagenesis cost is the reason dedicated accelerations were published (fastISM, compressed sensing, Taylor approximation) — see URLs in (a1) **[SEARCH SNIPPET — NOT VERIFIED]**

**Free-tier compute envelope.**
- Google Colab free tier: **NVIDIA T4, 16 GB VRAM**, session cap commonly reported as **12 hours**, weekly usage "approximately 15–30 hours per week", and "Google does not publish a fixed number of free GPU hours". Kaggle Notebooks: "**30 hours per week, often on P100s**". — [joshthompson.co.uk Colab 2026 guide](https://joshthompson.co.uk/ai/google-colab-2026-guide-free-compute-automations-pro-tips/), [hivenet.com Colab GPU limits](https://www.hivenet.com/post/google-colaboratory-gpu-complete-guide-to-free-cloud-gpu-access-and-limitations), [thundercompute.com Colab alternatives](https://www.thundercompute.com/blog/colab-alternatives-for-cheap-deep-learning-in-2025) **[SEARCH SNIPPET — NOT VERIFIED; all three are third-party blogs, not Google/Kaggle official docs. The T4/16GB and Kaggle 30h/week figures are consistent across sources and are the ones I would rely on; the "15–30 h/week" Colab figure is explicitly described by the sources themselves as unpublished/variable.]**

**ESM-2 checkpoint sizes (determines whether attribution is affordable and whether a web app can serve it).**
- Official checkpoint ladder: `esm2_t6_8M_UR50D` (6 layers, 8M params, embed dim 320); `esm2_t12_35M_UR50D` (12 layers, 35M, 480); `esm2_t30_150M_UR50D` (30 layers, 150M, 640); `esm2_t33_650M_UR50D` (33 layers, 650M, 1280). — [huggingface.co/facebook/esm2_t33_650M_UR50D](https://huggingface.co/facebook/esm2_t33_650M_UR50D), [github.com/facebookresearch/esm](https://github.com/facebookresearch/esm), [HF transformers ESM docs](https://huggingface.co/docs/transformers/model_doc/esm) **[SEARCH SNIPPET — NOT VERIFIED]**
- Reported inference memory: 8M ≈ ~1 GB VRAM and CPU-fine-tunable; 35M ≈ 1–2 GB; 150M ≈ 2–4 GB; 650M ≈ 6–8+ GB; CPU-only: 8M and 35M fine, 150M "light batches only", 650M "runs slowly", 3B/15B unrealistic. — [qwe.edu.pl install fair-esm guide](https://www.qwe.edu.pl/ai-tools/install-esm-2-fair-esm-protein-language-model/) **[SEARCH SNIPPET — NOT VERIFIED; low-quality source. Treat as a rough ordering only, and re-measure before quoting.]**
- Counter-intuitive but useful: "The ESM-2 model with 150M parameters performs better than the ESM-1b model with 650M parameters." — [biorxiv 2022.07.20.500902](https://www.biorxiv.org/content/10.1101/2022.07.20.500902v1.full.pdf) **[SEARCH SNIPPET — NOT VERIFIED]**

### Inferences (compute planning, marked as my estimates)
- **[ESTIMATE — MINE]** With frozen embeddings already on disk (the student's current setup), SHAP GradientExplainer or Captum integrated gradients over a small window-CNN is a *minutes-scale* job for a few hundred test windows on a T4 — the embeddings are precomputed, so each attribution step touches only the CNN head, not the 650M-parameter PLM. This is the cheapest credible XAI story available to this student and it costs essentially nothing.
- **[ESTIMATE — MINE]** Attribution *through* the PLM (i.e. attributing to amino acids rather than to embedding dimensions) requires gradients through ProtT5/ESM-2 and is roughly (number of integration steps, typically 20–50) × (one PLM forward+backward) per sequence. On a free T4 that is still feasible for tens-to-low-hundreds of sequences, not for a whole dataset. Plan a *case-study* set, not a whole-test-set run.
- **[ESTIMATE — MINE]** Full saturation mutagenesis is 19 × L forward passes per protein (L = length). For L=400 that is 7,600 PLM forwards for ONE protein. Do not plan this through a PLM on free tier; restrict to a ±15-residue window around the predicted site (≈ 19 × 31 ≈ 589 forwards per site), or do the mutagenesis only on the CNN head using embedding-space substitution.
- **Avoid KernelExplainer entirely.** It is the one SHAP variant that is genuinely dangerous on a deadline, and nothing in this subfield requires it: the precedent paper (LMCrot) used GradientExplainer.
- Graph explainers in PyTorch Geometric (`torch_geometric.explain`, GNNExplainer/PGExplainer style) would be the equivalent toolkit if the student goes graph. I did not verify the current PyG explainer API surface — see Gaps.

### Gaps
- **No measured wall-clock numbers found** for SHAP or integrated gradients applied to ProtT5/ESM-2 on a T4. No paper I read reported XAI runtime. All timing statements above are my labelled estimates.
- I did not verify the current PyTorch Geometric `explain` module contents or version. Marked as a gap rather than asserted.

---

## (a3) What does a REVIEWER-CREDIBLE XAI contribution look like in this subfield? (most important part)

### Takeaway
At this venue tier, "XAI as a contribution" does **not** mean producing a SHAP plot. It means one of three concrete things: **(i) attribution used as a quantified check against independent biological annotation** (e.g. "the top-attention segments cover 54.78% of annotated functional regions"), **(ii) attribution used to justify an architectural decision** (e.g. "attention shows distant residues matter, therefore full-sequence input rather than a peptide window"), or **(iii) an architecture chosen because it is intrinsically interpretable**, with the interpretability stated in the title (KAN papers). Pattern (i) and (ii) are both achievable in 8–9 weeks on the student's existing pipeline.

### Cited Findings — concrete precedents, what they did, where published

**1. LMCrot — the closest possible template to the student's current pipeline.**
- ProtT5-XL-UniRef50 embeddings → three base models (T5ResConvBiLSTM; EmbedCNN = 2D-CNN on a 15×31 supervised embedding layer; PhysicoDNN = 3-layer DNN on **1,343 physicochemical properties**) → stacked generalisation with a 3-layer DNN meta-classifier fusing **56 features**.
- **XAI done:** (a) heatmaps of **normalised attention weights from the final ProtT5 encoder block, averaged over heads**; for protein **O00244** this showed significant attention to residues that are far apart in sequence but **7.83 Å apart in space**, which the authors used to *justify feeding the full sequence instead of only a peptide window*. (b) **SHAP GradientExplainer** over the 1024 ProtT5 embedding dimensions, showing some features push the prediction positively, others negatively, and that "features of adjacent amino acids also weigh in".
- **Stated biological insight:** "relying exclusively on peptide sequences might fail to capture the association of distant residues affecting the site."
- **Performance (HeLa dataset):** LMCrot MCC **0.699**, AUROC **0.922**; DeepCap-Kcr MCC **0.650**, AUROC **0.906** (≈7.6% MCC improvement). On non-histone proteins, **14.8% MCC improvement over CapsNh-Kcr**.
- Code + web server: [github.com/KCLabMTU/LMCrot](https://github.com/KCLabMTU/LMCrot)
- — [Bioinformatics 40(5):btae290, May 2024](https://academic.oup.com/bioinformatics/article/40/5/btae290/7658304) **[FULL TEXT]**

**2. ESM2_AMP — explanation as explicit co-main contribution.**
- ESM-2 features at three granularities (global pooling, CLS/EOS special tokens, and **10 equal segments**) fused by a Transformer with multi-head attention, then an MLP classifier, for binary protein–protein interaction prediction.
- **XAI done:** attention weights across Transformer layers; integrated gradients on an AE+DNN variant; Tree SHAP on an AE+RF variant.
- **Quantified biological validation — the key move:** "higher attention weights were observed for end segments", and the **top three attention-weighted segments covered approximately 54.78% of functional amino-acid regions (Domain, Region, Compositional bias, Repeat, Motif) in true-positive cases.**
- The authors explicitly frame the goal as "enhancing the interpretability of feature representations while maintaining model performance" — i.e. interpretability is stated as a core contribution, not an appendix.
- — [Briefings in Bioinformatics 26(4):bbaf434, 2025, DOI 10.1093/bib/bbaf434](https://academic.oup.com/bib/article/26/4/bbaf434/8242608) **[FULL TEXT]**

**3. IKANbind — interpretability built into the architecture (title-level claim).**
- PLM embeddings + **hypergraph** neural network over 3D structure (capturing multi-residue spatial interactions) + **Kolmogorov–Arnold Network** head, for nucleic-acid binding residue prediction.
- **Interpretability mechanism:** KAN's decomposable basis functions have explicit mathematical meaning; the authors used **symbolic functions sin(πx), cos(πx), tanh(πx), x, x²** instead of opaque B-splines, enabling "basis function weight analysis" to see which learned features drive binding predictions.
- **Performance (DNA-180-Test):** AUC **0.916** vs **0.906** for ATMGBs (second best); AUPR **0.526** vs **0.491**; F1 **0.508** vs **0.489**.
- Code: [github.com/yangfengzhuguet/IKANBind](https://github.com/yangfengzhuguet/IKANBind)
- — [Bioinformatics 42(7):btag433, July 2026, DOI 10.1093/bioinformatics/btag433](https://academic.oup.com/bioinformatics/article/42/7/btag433/8712719) **[FULL TEXT]**

**4. InterPLM — explanation as the entire paper, at the top venue tier.**
- Sparse autoencoders on ESM-2 embeddings; up to **2,548** interpretable latent features per layer correlated with up to **143** known biological concepts (binding sites, structural motifs, functional domains); argues concepts are stored **in superposition** so individual neurons are poor explanatory units; interactive dashboard at InterPLM.ai.
- Published **Nature Methods 22:2107–2117 (2025)**. — [nature.com/articles/s41592-025-02836-7](https://www.nature.com/articles/s41592-025-02836-7), code [github.com/ElanaPearl/interPLM](https://github.com/ElanaPearl/interPLM) **[SEARCH SNIPPET — NOT VERIFIED]**
- Note the venue gap: a pure-explanation paper reached Nature Methods, but it required a genuinely new interpretability apparatus, not an application of SHAP.

**5. Interpretable KAN for enzyme commission number prediction.** — [nature.com/articles/s44387-025-00059-x](https://www.nature.com/articles/s44387-025-00059-x) **[SEARCH SNIPPET — NOT VERIFIED]**

**6. GPS-pPLM (prokaryotic phosphorylation sites)** — used **deep SHAP** for feature contribution plus multi-head attention weights. — [DOI 10.3390/cells13221854](https://doi.org/10.3390/cells13221854) **[SEARCH SNIPPET — NOT VERIFIED]**

**7. XAI-Driven Deep Learning for Protein Sequence Functional Group Classification** — a 2025 arXiv preprint whose framing is XAI-first; relevant as a thesis-scale example rather than a venue precedent. — [arXiv:2511.13791](https://arxiv.org/html/2511.13791) **[SEARCH SNIPPET — NOT VERIFIED]**

**8. TCR-EML: Explainable Model Layers for TCR-pMHC Prediction** — explanation built into model layers, immunology-adjacent. — [arXiv:2510.04377](https://arxiv.org/pdf/2510.04377) **[SEARCH SNIPPET — NOT VERIFIED]**

### Inferences — what the student should actually build for criterion 4
- **The single most reviewer-credible, cheapest XAI contribution available: quantified agreement between attribution and independent annotation.** Copy the ESM2_AMP move exactly, but at residue level: compute per-residue attribution (integrated gradients or SHAP GradientExplainer) on the test set, then measure **enrichment of high-attribution positions inside UniProt-annotated functional features (Domain, Region, Motif, Active site, Binding site, Compositional bias)** against a position-matched random baseline. The output is one number plus a curve, it costs almost nothing, and it is directly comparable to the 54.78% figure already in the literature. Critically, the annotation is *independent of the training labels*, which is what makes it evidence rather than circularity.
- **The second move: use attribution to justify a design decision**, the LMCrot pattern. E.g. "attribution mass outside the ±w window is X%, therefore the multi-window design with a wider outer window is warranted" — this converts XAI from decoration into a *method* contribution, which also feeds criterion 2.
- **The third move, specific to this student's leakage-control expertise: explain the applicability-domain / failure cases.** Compare attribution patterns on high-identity vs low-identity test proteins. If the model's attribution collapses onto a handful of positions for low-identity proteins, that is a publishable, honest, mechanistic explanation of *why* performance drops when leakage is controlled. I found no paper doing exactly this — see Gaps — which is simultaneously the opportunity and the risk.
- A plain "we made a SHAP summary plot" section will read as the BERT-Promoter precedent repeated four years later, and the advisor will recognise it instantly. The student needs one of the three moves above to clear his own 2022 bar.

### Gaps
- **I found no paper that uses XAI specifically to explain the performance gap under redundancy-controlled vs uncontrolled splits.** I searched for interpretability + applicability domain + homology; nothing surfaced. This is either a genuine gap or a search failure — the student should treat it as unconfirmed novelty and re-check before claiming it.
- I could not verify whether LMCrot's web server is actually live (I only confirmed the GitHub URL is cited in the paper as "code & web server").

---

## (a4) Exactly how was SHAP used in the advisor's BERT-Promoter (2022)?

### Takeaway
**SHAP was used as a FEATURE-SELECTION step, not as post-hoc biological interpretation.** The paper's own abstract says SHAP "served as a feature selection step to look at the top-rank BERT encodings"; the downstream classifiers then learned only those top features. This is important: the student can therefore claim a *genuine advance over the advisor's own precedent* simply by doing post-hoc interpretation with biological validation — because the precedent did not do that.

### Cited Findings
Source: PubMed record (retrieved via the PubMed MCP tool). Based on articles retrieved from PubMed. DOI: [10.1016/j.compbiolchem.2022.107732](https://doi.org/10.1016/j.compbiolchem.2022.107732), PMID 35863177, PII S1476-9271(22)00112-8.
- Title: "BERT-Promoter: An improved sequence-based predictor of DNA promoter using BERT pre-trained model and SHAP feature selection." **[ABSTRACT — verbatim official PubMed metadata]**
- Verbatim from the abstract: *"a pre-trained Bidirectional Encoder Representations from Transformers (BERT) model was employed to encode DNA sequences, and SHapley Additive exPlanations (SHAP) analysis served as a feature selection step to look at the top-rank BERT encodings. At the last stage, different machine learning classifiers were implemented to learn the top features and produce the prediction outcomes."* **[ABSTRACT — verbatim]**
- Verbatim framing: *"we proposed a novel architecture that incorporated transformer natural language processing (NLP) and explainable machine learning to address this problem."* **[ABSTRACT — verbatim]**
- Reported performance: *"several experiments showed an accuracy of **85.5%** and **76.9%** for these two levels, respectively"* — level 1 = promoter vs non-promoter, level 2 = strong vs weak promoter. **[ABSTRACT — verbatim]**
- Classifiers: the abstract says only "different machine learning classifiers"; the PubMed **keyword list** includes "EXtreme Gradient Boosting", indicating XGBoost was among them. Other keywords: "BERT multilingual cases", "Contextualized word embedding", "Explainable artificial intelligence", "Promoter region", "SHAP". **[ABSTRACT — official metadata]**
- Availability: *"freely available at https://github.com/khanhlee/bert-promoter"* — note this is a **GitHub repository, not a hosted web server**. **[ABSTRACT — verbatim]**
- Journal: *Computational Biology and Chemistry*, volume **99**, article **107732**, publication date 2022-07-14. Authors: Nguyen Quoc Khanh Le (Taipei Medical University), **Quang-Thai Ho (College of Information & Communication Technology, Can Tho University, Viet Nam; and Dept. of Computer Science and Engineering, Yuan Ze University, Taiwan)**, Van-Nui Nguyen, Jung-Su Chang. **[ABSTRACT — official metadata]**
- MeSH terms assigned: DNA; Machine Learning; Natural Language Processing; Promoter Regions, Genetic. **[ABSTRACT — official metadata]**

### Inferences
- The advisor's XAI precedent is **instrumental** (SHAP as a dimensionality-reduction/feature-ranking tool that improves accuracy), not **explanatory** (SHAP as evidence about biology). That is a *lower* bar than the 2024–2026 papers in (a3), and it means:
  1. The student can present post-hoc interpretation with annotation-based validation as a **step beyond** the advisor's own 2022 work — a politically safe way to satisfy criterion 4 without implying the advisor's work was deficient.
  2. The student should be careful not to simply re-run "SHAP for feature selection", which the advisor will read as a repeat.
  3. Note also that BERT-Promoter shipped **code only, no web server** — so a working deployed web app is an area where the student can exceed the advisor's precedent, which matters for criterion 5 and for the mandatory SE-department requirement.
- The TWO reported accuracies (85.5% / 76.9%) come from a two-stage design. If the student uses a two-stage design, these are the comparable numbers the advisor will have in mind.

### Gaps
- I could not read the BERT-Promoter **full text**. ScienceDirect returned HTTP 403, PubMed's HTML page returned only a cookie wall, EuropePMC returned 403, and the author's institutional page redirected to a 404 (`khanhlee.github.io/publication/2022-07-14-BERT-Promoter` → `aibiomedlab.com/...` → 404). Therefore: **the exact SHAP variant used (KernelExplainer vs TreeExplainer), the number of features retained after SHAP ranking, the full classifier list, and the MCC/AUC values are NOT FOUND.** The student has local library access and should retrieve the PDF to fill this in — it will be the first thing the advisor can check.

---

## (a5) Known pitfalls and criticisms of XAI in biology — what the student must NOT overclaim

### Takeaway
There is a substantial, citable literature showing attribution maps can be plausible-looking yet unfaithful, noisy, and non-causal. The student should pre-empt this with an explicit limitations paragraph and at least one stability check; the honest framing is "attribution agrees with known biology at rate X", never "the model learned mechanism Y".

### Cited Findings
- **Sanity-check failure:** "certain saliency methods may produce visually plausible explanations even when model parameters are randomized, raising concerns about whether these explanations reflect true model behavior or merely plausible artifacts." — [PMC10831517, "Seeing Is Not Always Believing: Discrepancies in Saliency Maps"](https://pmc.ncbi.nlm.nih.gov/articles/PMC10831517/) **[SEARCH SNIPPET — NOT VERIFIED]**
- **Not causal:** "Saliency maps do not necessarily indicate the true causes of predictions"; in medical imaging "none of the saliency maps meet all tested criteria and their credibility should be critically evaluated prior to integration into medical imaging pipelines, especially because many recent deep learning based clinical studies rely on saliency maps for interpretability without critically evaluating their limitations." — [arXiv:2008.02766, "Assessing the (Un)Trustworthiness of Saliency Maps for Localizing Abnormalities in Medical Imaging"](https://arxiv.org/pdf/2008.02766) **[SEARCH SNIPPET — NOT VERIFIED]**
- **Attribution noise is systematic in sequence models, and correctable:** in genomics "attribution maps can be challenging to interpret due to spurious importance scores for seemingly arbitrary nucleotides, with attribution noise arising from how DNNs handle one-hot encoded DNA, [which] is pervasive across various genomic DNNs." The corresponding peer-reviewed treatment is "Correcting gradient-based interpretations of deep neural networks for genomics" — [PubMed 37161475](https://pubmed.ncbi.nlm.nih.gov/37161475/) **[SEARCH SNIPPET — NOT VERIFIED]**
- **Filter-to-motif equivalence is weak:** "Only several best-recovered motifs can be equated to true motifs, as most kernels act during training to increase generalization ability, with such auxiliary kernels producing noise and reducing performance." — [ScienceDirect S2452310020300032](https://www.sciencedirect.com/science/article/pii/S2452310020300032) **[SEARCH SNIPPET — NOT VERIFIED]**
- **"Exploratory not explanatory":** a widely cited critique arguing saliency maps should be treated as hypothesis-generating, not as explanations. — [arXiv:1912.05743](https://arxiv.org/pdf/1912.05743) **[SEARCH SNIPPET — NOT VERIFIED]**
- **Gradient vs perturbation trade-off:** gradient methods are "noisy and sensitive to small perturbations", perturbation methods are "computationally expensive". — [arXiv:2605.14073](https://arxiv.org/html/2605.14073v1) **[SEARCH SNIPPET — NOT VERIFIED]**
- **Faithfulness can be measured with counterfactuals:** "Counterfactuals As a Means for Evaluating Faithfulness of Attribution Methods" — [arXiv:2408.11252](https://arxiv.org/pdf/2408.11252) **[SEARCH SNIPPET — NOT VERIFIED]**
- The PLM-XAI review itself lists trustworthiness and bias as unresolved community concerns. — [arXiv:2506.19532](https://arxiv.org/abs/2506.19532) **[ABSTRACT]**

### Inferences — a concrete, cheap defensive protocol the student can run
- **[ESTIMATE — MINE]** Three checks, each costing hours not days, that convert "we made a SHAP plot" into a defensible XAI section:
  1. **Model-randomisation sanity check** (the test from PMC10831517): recompute attributions with randomly re-initialised weights; if the attribution pattern survives, the method is reading the input, not the model. Report the similarity.
  2. **Agreement across two independent methods** (e.g. integrated gradients vs SHAP GradientExplainer vs occlusion/ISM): report rank correlation of per-residue scores. Disagreement is itself a reportable, honest finding.
  3. **Deletion/insertion faithfulness curve**: mask the top-k attributed residues and measure prediction drop vs masking random residues. This is the standard faithfulness metric and is cheap when the PLM embeddings are cached.
- **Wording discipline** (this matches the topic's existing language convention of never overclaiming): say "high-attribution positions are enriched in annotated functional regions (X% vs Y% baseline)"; do NOT say "the model discovered the binding motif" or "the model learned the mechanism". Correlation with known motifs is consistency evidence, not mechanism.

### Gaps
- I did not find a protein-specific equivalent of the genomics "attribution noise from one-hot encoding" correction. Whether the same artefact applies to PLM-embedding inputs (which are not one-hot) is **not found** — plausibly it does not, but the student should not assert either way.

---

## (b1) Which "beyond PLM" method families could a student realistically adopt in 8–9 weeks?

### Takeaway
Of the twelve families asked about, exactly three are both credibly "new" for this group's subfield and achievable by someone who has never trained a GNN or fine-tuned a PLM: **structure-aware PLM embeddings (SaProt/ProstT5) as a drop-in replacement for ProtT5**, **LoRA/PEFT fine-tuning instead of frozen embeddings**, and **conformal prediction for calibrated applicability-domain guarantees**. GNN-over-AlphaFold-structures is the highest-prestige option but is now the group's OWN newest method (SirtSAGE), so it is no longer novel *for this group* — and it is also the heaviest lift.

### Cited Findings — per-family assessment

**(i) GNNs over predicted structures (GAT, GATv2, GraphSAGE, EGNN) — MATURE, and ALREADY USED BY THIS GROUP.**
- The advisor's own newest work: **SirtSAGE** ("Sirtuin Structural-Aware Graph-Evolutionary framework") "integrates the contextual semantics of ESM-2 into a Graph Attention Network v2 (GATv2), where Predicted Local Distance Difference Test (pLDDT) scores serve as spatial confidence gates to fine-tune the influence of structural interactions." Authors: Dinh-Quy Nguyen, Viet-Thanh Nguyen, Muhammad Hussain, **Quang-Thai Ho**. Journal of Computational Biophysics and Chemistry; received 2026-05-15, accepted 2026-08-07, published 2026-08-27. — [worldscientific.com/doi/abs/10.1142/S2737416527400011](https://www.worldscientific.com/doi/abs/10.1142/S2737416527400011) **[SEARCH SNIPPET — NOT VERIFIED; I did not fetch the publisher page, so the quoted phrasing comes from a search summary of the abstract. The author list and the ESM-2→GATv2→pLDDT-gating design are consistent with the shared context given to me.]**
- Prior art showing residue-level graph methods are a crowded field: **GraphSite** uses a graph transformer on residue graphs built from AlphaFold2 structures, with input features from AlphaFold2 representations + PSSM + HMM + DSSP (RSA, SS, torsion angles), and masks spatially remote residues in the attention computation; reported to surpass the then-SOTA structure-based method by **16.4% in AUPR and 11.2% in MCC** on an independent test set of 181 proteins. — [Briefings in Bioinformatics 23(2):bbab564](https://academic.oup.com/bib/article/23/2/bbab564/6509729), preprint [biorxiv 2021.08.25.457661v2](https://www.biorxiv.org/content/10.1101/2021.08.25.457661v2.full) **[SEARCH SNIPPET — NOT VERIFIED]**
- **GraphBind** "encodes protein structures as graphs and adopts graph neural networks (GNN) to learn the local tertiary patterns for binding residue prediction." **[SEARCH SNIPPET — NOT VERIFIED]**
- More recent entries in the same niche: **RGTBind** ("RBF-gate graph transformer with spatially biased attention for protein–DNA binding-site prediction", [Springer s00894-026-06818-0](https://link.springer.com/article/10.1007/s00894-026-06818-0)); "Genome-scale annotation of protein binding sites via language model and geometric deep learning" ([PMC11023698](https://pmc.ncbi.nlm.nih.gov/articles/PMC11023698/)); **bindNode24**, "competitive binding residue prediction with 60% smaller model" ([PMC11957672](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11957672/)) **[SEARCH SNIPPET — NOT VERIFIED]**

**(ii) Structure-aware PLMs (SaProt, ProstT5, ESM-3, ProtSSN) — MATURE, ready weights, LOW learning curve.**
- SaProt: trained on "approximately 40 million protein sequences and structures"; uses a **structure-aware vocabulary** combining residue tokens with **3Di structure tokens derived from Foldseek**; "surpasses well-established baselines across 10 significant downstream tasks". ICLR 2024. — [ICLR 2024 proceedings PDF](https://proceedings.iclr.cc/paper_files/paper/2024/file/1c42513b8895ab11fbbb5b7e8e6b6b02-Paper-Conference.pdf), code [github.com/westlake-repl/SaProt](https://github.com/westlake-repl/SaProt), preprint [biorxiv 2023.10.01.560349](https://www.biorxiv.org/content/10.1101/2023.10.01.560349.full.pdf) **[SEARCH SNIPPET — NOT VERIFIED]**
- ProstT5: "a bilingual language model for protein sequences and structures" that "utilizes the AlphaFold Protein Structure Database" and can translate between 1-D amino-acid sequences and 1-D 3Di structure sequences; "demonstrated improved performance in various protein function prediction tasks compared to sota sequence-based models such as ProtT5, ESM2 and Ankh." **[SEARCH SNIPPET — NOT VERIFIED]**
- Reported comparison: "for contact prediction, SaProt achieves 77.16% vs ESM-2's 39.16% for long-range contacts, with both SaProt and ProstT5 outperforming sequence-only models on structural classification tasks." — **[SEARCH SNIPPET — NOT VERIFIED; this figure came from a search summary aggregating several benchmark papers and I could not attribute it to one specific paper. Do not quote it without re-verification.]**
- Independent benchmarking exists: "Benchmarking protein language models for protein crystallization" ([Sci Rep s41598-025-86519-5](https://www.nature.com/articles/s41598-025-86519-5)); FLIP-benchmark constrained evaluation ([arXiv:2501.18223](https://arxiv.org/pdf/2501.18223)); "A Benchmarking Platform for Assessing Protein Language Models on Function-Related Prediction Tasks" ([Springer protocol 978-1-0716-4662-5_14](https://link.springer.com/protocol/10.1007/978-1-0716-4662-5_14)); PFMBench Protein Foundation Model Benchmark ([arXiv:2506.14796](https://arxiv.org/pdf/2506.14796)) **[SEARCH SNIPPET — NOT VERIFIED]**
- S-PLM: structure-aware PLM via **contrastive learning between sequence and structure** — [Advanced Science, DOI 10.1002/advs.202404212](https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/advs.202404212) **[SEARCH SNIPPET — NOT VERIFIED]**

**(iii) Parameter-efficient fine-tuning (LoRA, adapters) instead of frozen embeddings — MATURE, cheap, and a clear step beyond the group's frozen-embedding habit.**
- LoRA freezes pre-trained weights and injects trainable rank-decomposition matrices into each Transformer layer. Reported ESM-2 gains (SeqProFT): 35M model +9.02% on EC, +7.28% on Fold, +10.14% on FLU; 150M model max improvement 8.53%; 650M model best overall with +7.48% GO-BP, +2.98% Loc. — [arXiv:2411.11530, SeqProFT](https://arxiv.org/pdf/2411.11530) **[SEARCH SNIPPET — NOT VERIFIED]**
- "Using LoRA shows improved performance over vanilla full finetuning and significantly helps in mitigating overfitting"; "the efficiency of LoRA enables training of larger ESM-2 models on modest hardware". **[SEARCH SNIPPET — NOT VERIFIED]**
- A directly reusable worked example for binding-site prediction: "LoRA, QLoRA, and ESM-2 for Predicting Binding Sites" — [biorxiv 2023.11.13.566930](https://www.biorxiv.org/content/10.1101/2023.11.13.566930v1.full.pdf) **[SEARCH SNIPPET — NOT VERIFIED]**
- The headline peer-reviewed justification: "Fine-tuning protein language models boosts predictions across diverse tasks", Nature Communications — [nature.com/articles/s41467-024-51844-2](https://www.nature.com/articles/s41467-024-51844-2) **[SEARCH SNIPPET — NOT VERIFIED]**
- Also relevant: injecting structure information into a PLM through PEFT, needing "less than 2% tunable parameters" with the ESM-2 backbone frozen — [ScienceDirect S0010482525009588](https://www.sciencedirect.com/science/article/abs/pii/S0010482525009588) **[SEARCH SNIPPET — NOT VERIFIED]**
- And: "Fine-tuning protein language models enhances the identification **and interpretation** of the transcription factors" — a PEFT + XAI combination, i.e. criteria 3 and 4 in one paper — [ScienceDirect S2667318526000218](https://www.sciencedirect.com/science/article/pii/S2667318526000218) **[SEARCH SNIPPET — NOT VERIFIED]**
- Industrial tooling exists: NVIDIA BioNeMo documents LoRA fine-tuning of ESM-2 — [docs.nvidia.com/bionemo-recipes/1.10/lora-finetuning-esm2.html](https://docs.nvidia.com/bionemo-recipes/1.10/lora-finetuning-esm2.html) **[SEARCH SNIPPET — NOT VERIFIED]**

**(iv) Kolmogorov–Arnold Networks — EMERGING BUT ALREADY ESTABLISHED IN BIOINFORMATICS BY 2025–2026; cheap; and it doubles as an XAI story.**
- **CaLMPhosKAN**: phosphorylation site prediction fusing codon-aware and amino-acid-aware embeddings with a **wavelet-based KAN** prediction head (derivative-of-Gaussian wavelet transform); "performs better than existing approaches across multiple datasets." — [Bioinformatics 41(4):btaf124](https://academic.oup.com/bioinformatics/article/41/4/btaf124/8090024) **[SEARCH SNIPPET — NOT VERIFIED]** — *note: this is an extremely close analogue of the advisor's PTM-site/mCNN niche, so a KAN head is demonstrably publishable there.*
- **IKANbind** — see (a3) item 3, full details verified. [Bioinformatics 42(7):btag433](https://academic.oup.com/bioinformatics/article/42/7/btag433/8712719) **[FULL TEXT]**
- **Interpretable KAN for EC number prediction** — [nature.com/articles/s44387-025-00059-x](https://www.nature.com/articles/s44387-025-00059-x) **[SEARCH SNIPPET — NOT VERIFIED]**
- **Kolmogorov–Arnold graph neural networks for molecular property prediction**, Nature Machine Intelligence — [nature.com/articles/s42256-025-01087-7](https://www.nature.com/articles/s42256-025-01087-7) **[SEARCH SNIPPET — NOT VERIFIED]**

**(v) State-space models (Mamba, Hyena) — PRESENT but thinner in protein work.**
- **MAKA-Map** integrates a **Mamba** selective state-space module (to "effectively capture medium- to long-range sequence information") with a **KAN** (for nonlinear structural representation) for real-valued distance prediction in protein folding. — [DOI 10.3390/biom16020194](https://doi.org/10.3390/biom16020194) **[SEARCH SNIPPET — NOT VERIFIED]**
- I found **no Hyena-based protein-sequence predictor** in my searches. **NOT FOUND.**

**(vi) Conformal prediction / UQ — MATURE ENOUGH, peer-reviewed in Nature Communications, and uniquely well-matched to this student's leakage-control expertise.**
- "Functional protein mining with conformal guarantees", Nature Communications 2025 — [nature.com/articles/s41467-024-55676-y](https://www.nature.com/articles/s41467-024-55676-y) **[SEARCH SNIPPET — NOT VERIFIED]**
- "Leveraging conformal prediction to annotate enzyme function space with limited false positives" — [PMC11164347](https://pmc.ncbi.nlm.nih.gov/articles/PMC11164347/) **[SEARCH SNIPPET — NOT VERIFIED]**
- Mechanism as reported: conformal prediction "provides a flexible, data-driven way to find an optimal cutoff to decide whether to predict a function label for an input protein, such that the **false discovery rate on test data is lower than a user-specified upper bound**", and can "transform raw similarity scores into retrieval sets and probabilities." **[SEARCH SNIPPET — NOT VERIFIED]**
- Drug–target variant: [arXiv:2505.18890, Conformal Prediction for Uncertainty Estimation in Drug-Target Interaction Prediction](https://arxiv.org/pdf/2505.18890); protein–ligand affinity UQ: [PMC12678490](https://pmc.ncbi.nlm.nih.gov/articles/PMC12678490/); curated library/tutorial list: [github.com/valeman/awesome-conformal-prediction](https://github.com/valeman/awesome-conformal-prediction) **[SEARCH SNIPPET — NOT VERIFIED]**

**(vii) Geometric/equivariant deep learning (EGNN), (viii) mixture-of-experts, (ix) contrastive/metric learning, (x) retrieval done rigorously, (xi) ensembling.**
- Geometric deep learning for binding-site annotation at genome scale exists ([PMC11023698](https://pmc.ncbi.nlm.nih.gov/articles/PMC11023698/)) **[SEARCH SNIPPET — NOT VERIFIED]**; KA-GNN explicitly frames itself as extending geometric deep learning ([s42256-025-01087-7](https://www.nature.com/articles/s42256-025-01087-7)) **[SEARCH SNIPPET — NOT VERIFIED]**.
- Contrastive sequence–structure learning is realised in S-PLM ([advs.202404212](https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/advs.202404212)) **[SEARCH SNIPPET — NOT VERIFIED]**.
- **Ensembling and stacked generalisation are already standard at this venue tier** — LMCrot's entire architecture is intermediate-fusion stacked generalisation of three base models. — [btae290](https://academic.oup.com/bioinformatics/article/40/5/btae290/7658304) **[FULL TEXT]**
- **Retrieval is already the group's own device** (per the shared context: "retrieval-augmented generation bolted on"), so it cannot be the novelty claim; it can only be the *baseline* that a rigorous leakage-controlled study interrogates.
- **Mixture-of-experts in protein residue-level prediction: NOT FOUND** in my searches. I have no evidence for or against its maturity here.

### Inferences
- **Novelty is relative to this group, and the group has already taken the two most obvious "beyond PLM" steps**: graph attention over AlphaFold structures with pLDDT gating (SirtSAGE, 2026) and retrieval augmentation. Proposing either as "the new method" in week 6 would invite the response "we already do that."
- **The genuinely under-exploited directions for this group**, in descending order of safety: (1) **replacing the frozen ProtT5 embedding with a structure-aware PLM embedding (SaProt/ProstT5)** — this is "beyond PLM" in the advisor's exact framing (PSSM → PLM → structure-aware PLM) while requiring *zero* new modelling skill, because it is a drop-in change to the embedding step of an existing working pipeline; (2) **LoRA/PEFT instead of frozen embeddings** — again a step beyond the group's habit, with a Nature Communications justification and a ready ESM-2 binding-site example; (3) **a KAN head on the existing mCNN** — cheap, fashionable, publishable in this exact niche (CaLMPhosKAN), and it *simultaneously* supplies the XAI contribution via symbolic basis-function analysis; (4) **conformal prediction** — supplies a calibrated applicability-domain guarantee, which is the student's existing research question dressed in a method with formal guarantees.
- **Note the elegant combination:** ProstT5 or SaProt gives "beyond PLM" (criterion 3) while *keeping the sequence-only input*, so the web app does not need AlphaFold structures at inference. That resolves a real tension between criteria 3 and 5 that the GNN route creates.

### Gaps
- **I could not verify the SirtSAGE paper directly** (publisher page not fetched). The DOI 10.1142/S2737416527400011 and the ESM-2→GATv2→pLDDT description come from a search summary only.
- No measured GPU-hour figures for training a GATv2/GraphSAGE residue-graph model on a few thousand proteins were found in any source. All such figures below are my labelled estimates.
- Mixture-of-experts and Hyena in protein residue prediction: not found.
- I did not verify whether ESM-3 weights are freely downloadable under terms a student can use; **NOT FOUND**, and this matters because ESM-3 is frequently gated.

---

## (b2) AlphaFold DB structures and pLDDT: where from, how in bulk, and what does a structure-graph pipeline really cost?

### Takeaway
Bulk AlphaFold data is genuinely free and well-documented (EBI FTP per-proteome tarballs, a REST API for single accessions, and a 23 TiB Google Cloud bucket), and pLDDT is a plain per-residue 0–100 number available either inside the mmCIF/PDB B-factor field or in a `confidence_v4.json`. For a few thousand proteins the download is the easy part; the real cost is per-protein parsing, contact-graph construction and caching, plus the fact that the deployed web app would then need structures for user-submitted sequences it has never seen.

### Cited Findings
- Access routes: "AlphaFold DB provides bulk downloads via FTP, programmatic access via an API, and download of individual predictions on protein-specific web pages." Bulk = "uncompressed archive files (.tar) of compressed PDB/mmCIF files (.gz) **per reference proteome**" from **ftp://ftp.ebi.ac.uk/pub/databases/alphafold**. — [NAR 2022, 50(D1):D439](https://academic.oup.com/nar/article/50/D1/D439/6430488) and [PMC8728224](https://pmc.ncbi.nlm.nih.gov/articles/PMC8728224/) **[SEARCH SNIPPET — NOT VERIFIED]**
- Full dataset on Google Cloud Public Datasets, CC-BY-4.0, "**approximately 23 TiB** in size", bucket **gs://public-datasets-deepmind-alphafold-v4**. — [console.cloud.google.com AlphaFold marketplace](https://console.cloud.google.com/marketplace/product/bigquery-public-data/deepmind-alphafold) and [github.com/google-deepmind/alphafold/blob/main/afdb/README.md](https://github.com/google-deepmind/alphafold/blob/main/afdb/README.md) **[SEARCH SNIPPET — NOT VERIFIED]**
- Coverage: AlphaFold DB 2024 release provides "structure coverage for over **214 million** protein sequences". — [NAR 2024, 52(D1):D368](https://academic.oup.com/nar/article/52/D1/D368/7337620) **[SEARCH SNIPPET — NOT VERIFIED]**
- pLDDT definition and location: "The `confidence_v4.json` file contains a confidence metric output by AlphaFold called pLDDT, which provides **a number for each residue** indicating how confident AlphaFold is in the local surrounding structure, **ranging from 0 to 100** where 100 is most confident." — [afdb README](https://github.com/google-deepmind/alphafold/blob/main/afdb/README.md) **[SEARCH SNIPPET — NOT VERIFIED]**
- A convenience layer exists for accession-based bulk retrieval: "AlphaFoldDB Structure Extractor, a web-based tool and API that enables bulk download of AlphaFold-predicted protein structures using common protein accessions". — [x.com/BiologyAIDaily/status/1920822822097793334](https://x.com/BiologyAIDaily/status/1920822822097793334) **[SEARCH SNIPPET — NOT VERIFIED; the primary source is a social-media post about a paper, which is weak. The student should locate the actual publication before citing.]**
- If structures must be *predicted* rather than looked up, nf-core/proteinfold wraps AlphaFold2/ColabFold/ESMFold and outputs "pLDDT scores per residue for each of the 5 predicted models". — [nf-co.re/proteinfold/1.1.1/docs/output](https://nf-co.re/proteinfold/1.1.1/docs/output/) **[SEARCH SNIPPET — NOT VERIFIED]**
- What a working residue-graph feature set looks like in practice (GraphSite): AlphaFold2 sequence representations + PSSM + HMM + DSSP-derived RSA, secondary structure and torsion angles, with pairwise amino-acid distances used to mask spatially remote residues. — [bbab564](https://academic.oup.com/bib/article/23/2/bbab564/6509729) **[SEARCH SNIPPET — NOT VERIFIED]**

### Inferences — practical cost of a structure-graph pipeline for a few thousand proteins
- **[ESTIMATE — MINE]** Do **not** download the 23 TiB bucket or whole-proteome tarballs. For a few thousand UniProt accessions, fetch individual files from the AlphaFold DB REST API / per-accession URLs. An mmCIF for a typical protein is on the order of a few hundred kB to a few MB compressed, so **a few thousand proteins is roughly single-digit GB and a few hours of polite sequential downloading** — well within Colab disk and within a Google Drive cache.
- **[ESTIMATE — MINE]** Graph construction (parse CIF → Cα coordinates → k-NN or 8–10 Å contact edges → node features = PLM embedding + pLDDT) is CPU-bound, on the order of **tens of milliseconds to a second per protein**, i.e. minutes-to-an-hour for a few thousand. Cache to `.pt`/`.npz` once; never rebuild in the training loop.
- **[ESTIMATE — MINE]** Training a small GATv2/GraphSAGE on a few thousand cached residue graphs on a free T4 is **not** the bottleneck — likely tens of minutes per epoch at worst, often much less. The bottleneck is the student's **learning curve**: PyTorch Geometric batching semantics, `edge_index` conventions, node-level vs graph-level readout, and residue-level class imbalance. For someone who has never trained a GNN, budget **2–3 weeks of the 8–9** just to reach a trustworthy baseline, which is a large fraction of the whole budget.
- **Hard coverage caveat:** not every accession has an AlphaFold DB entry (isoforms, long proteins, non-reference sequences). The student must plan for a coverage figure and a fallback, and must report it — this is exactly the kind of thing the advisor's group would check.
- **Deployment caveat that the GNN route creates:** if the model requires a structure, the web app cannot accept an arbitrary pasted FASTA. Either the app looks the sequence up in AlphaFold DB (works only for known proteins), or it must run ESMFold (too heavy for free hosting), or it degrades to "accession input only". This is a direct conflict with criterion 5 and should be raised with the advisor at week 6.

### Gaps
- No source gave a measured download time, per-protein file size, or GPU-hour figure for a residue-graph pipeline. Everything in the Inferences above is my estimate.
- The AlphaFoldDB Structure Extractor publication could not be located from a citable source.

---

## (b3) Which option gives the best ratio of "credibly novel for this subfield" to "achievable in 8–9 weeks"? — RECOMMENDATION

### Takeaway
**Recommended primary: structure-aware PLM embedding (ProstT5 or SaProt) as a drop-in replacement for frozen ProtT5, combined with a KAN or LoRA upgrade of the prediction head, plus attribution-vs-annotation XAI and a conformal-prediction applicability gate.** This satisfies criterion 3 in the advisor's own historical framing (PSSM → PLM → structure-aware PLM), reuses 100% of the student's existing pipeline and leakage-control machinery, keeps the input sequence-only so the web app stays buildable, and avoids colliding with SirtSAGE.

### Cited Findings supporting the recommendation
- The advisor's framing of criterion 3 is a *historical progression* argument (PSSM loses sequence order and is slow to compare → PLM → can one go further?). A structure-aware PLM is literally the next step in that same progression, with ICLR-2024 and journal-level evidence behind it: SaProt's structure-aware vocabulary over ~40M sequences+structures with Foldseek 3Di tokens ([ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/file/1c42513b8895ab11fbbb5b7e8e6b6b02-Paper-Conference.pdf)), ProstT5's bilingual sequence↔3Di translation trained on AlphaFold DB, reported to beat ProtT5/ESM2/Ankh on function prediction tasks. **[SEARCH SNIPPET — NOT VERIFIED]**
- The KAN head is proven publishable in the advisor's exact niche (PTM site prediction): CaLMPhosKAN, [Bioinformatics 41(4):btaf124](https://academic.oup.com/bioinformatics/article/41/4/btaf124/8090024) **[SEARCH SNIPPET — NOT VERIFIED]**; and KAN is simultaneously an interpretability device via symbolic basis functions, verified in IKANbind ([Bioinformatics 42(7):btag433](https://academic.oup.com/bioinformatics/article/42/7/btag433/8712719), **[FULL TEXT]**).
- LoRA on ESM-2 has a worked binding-site reference implementation ([biorxiv 2023.11.13.566930](https://www.biorxiv.org/content/10.1101/2023.11.13.566930v1.full.pdf)) and a Nature Communications level justification that fine-tuning beats frozen features ([s41467-024-51844-2](https://www.nature.com/articles/s41467-024-51844-2)) **[SEARCH SNIPPET — NOT VERIFIED]**.
- Conformal prediction has Nature Communications standing in protein function work ([s41467-024-55676-y](https://www.nature.com/articles/s41467-024-55676-y)) and delivers a user-specified FDR bound, which is a *formal* version of the applicability-domain warning the student already wants to build. **[SEARCH SNIPPET — NOT VERIFIED]**
- The group has already occupied GATv2+pLDDT (SirtSAGE, [DOI 10.1142/S2737416527400011](https://www.worldscientific.com/doi/abs/10.1142/S2737416527400011)) **[SEARCH SNIPPET — NOT VERIFIED]** and retrieval augmentation (shared context), so neither is available as the novelty claim.

### Inferences — ranked recommendation with reasoning
1. **BEST RATIO — structure-aware PLM embedding swap (ProstT5 / SaProt) as the "new method".** Novelty for this group: high (they use ProtT5 and ESM-2, both sequence-only). Skill delta: near zero — it is a different `AutoModel` call feeding the same window-CNN. Compute: one embedding-extraction pass, same order as the ProtT5 pass the student has already done. Risk: the main risk is that it *doesn't improve* the metric — which is fine and even desirable, because with the student's leakage-controlled protocol a well-executed negative result ("structure-aware tokens do not help once homology is controlled") is a genuine, defensible scientific contribution rather than a failure.
2. **STRONG ADD-ON — KAN prediction head replacing the dense head of the mCNN.** Novelty for this group: high (no KAN in their work). Skill delta: small (`pykan`/`efficient-kan` drop-in, a few hundred lines). Double-counts as criterion 4 via symbolic basis-function inspection. Precedent in PTM-site prediction already exists.
3. **STRONG ADD-ON — conformal prediction wrapper for the applicability-domain warning.** Novelty for this group: high. Skill delta: small (split-conformal calibration is ~50 lines; no new deep learning). Compute: negligible. It converts the student's existing "identity as applicability signal" research question into a method with a guarantee, and it directly powers the web app's confidence warning (criterion 5).
4. **MEDIUM — LoRA/PEFT fine-tuning of ESM-2 (35M or 150M) instead of frozen embeddings.** Novelty for this group: high (they freeze). Skill delta: moderate — new to the student but very well documented. Compute: feasible on a free T4 for the 35M/150M checkpoints; the 650M checkpoint with LoRA is borderline on 16 GB and will need gradient checkpointing and small batches. **[ESTIMATE — MINE]** Budget 1–2 weeks.
5. **AVOID AS PRIMARY — GNN over AlphaFold structures.** It is the group's own newest method, so it is not novel for them; it is the student's biggest skill gap (2–3 of 8–9 weeks); and it breaks the sequence-only web app. It is a good *stretch* comparison arm if time remains, and worth mentioning at week 6 to show awareness of SirtSAGE.
6. **AVOID — Mamba/Hyena, mixture-of-experts, EGNN, sparse autoencoders as primary.** Thin or absent precedent in this niche, highest learning curve, and none of them reuse the student's existing assets.

### Gaps
- I have no measured evidence that ProstT5 or SaProt embeddings help *residue-level site prediction specifically* (the benchmarks I found are function/fold/contact tasks). The student should state this as an open question, not as an expectation.
- I did not verify whether SaProt's structure tokens require having a structure at inference time (Foldseek 3Di tokens are derived FROM a structure). **This is a critical unresolved point: if SaProt needs a structure at inference, it inherits the GNN route's web-app problem, whereas ProstT5's sequence→3Di translation direction may not.** The student must check this before committing — it decides whether the recommendation above actually holds.

---

## (c1) What do recent bioinformatics prediction papers actually ship as their web tool, and what stack?

### Takeaway
There are two distinct worlds. Journal web servers (NAR Web Server Issue tier) ship a classic hosted server with strict free-and-no-login requirements; the ML community ships Gradio/Streamlit demos on Hugging Face Spaces. Crucially, many papers in the advisor's own tier — including his BERT-Promoter — ship **only a GitHub repository and call it availability**, which is a low bar the student can clear visibly.

### Cited Findings
- **NAR Web Server Issue 2025 is the 23rd annual issue**, published as *Nucleic Acids Research* 53(W1), 7 July 2025, and contains **72 servers**. Explicit editorial requirements: servers must be "**free and open-access**", payment or credit-card registration is rejected; "[cloud servers] usually require users to log in—and that is something that we do not allow (unless for sensitive data such as human medical or genetic data)"; documentation is mandatory and must cover "the underlying data and, most importantly, **the limitations of the system**"; a core aim is enabling "researchers who do not want to use the command line"; servers that require extensive pre-processing or output "plain text outputs without contextual information (e.g. gene annotation data or external links)" are rejected; results must offer "**filtering and sorting**" and include external links; and authors are expected to keep maintaining servers "long after publication". — [NAR 53(W1):W1](https://academic.oup.com/nar/article/53/W1/W1/8176964), mirror [PMC12230694](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12230694/) **[FULL TEXT]**
- Named servers in that issue include **FoldScript** (analysis of AI-generated 3D protein models), **HawkDock 2.0** (protein–protein complex structures) and **InDeepNet** (functional binding sites in proteins). — same source **[FULL TEXT]**
- The editorial does **not** state which web frameworks are used; implementation technology is not part of the published criteria. — same source **[FULL TEXT]**
- **Hugging Face Spaces is the de facto ML-demo host**, and concrete protein examples exist: `wwydmanski/esmfold` — "interactive HuggingFace Space providing zero-install 3D protein structure prediction powered by ESMFold… users submit single sequences and immediately receive 3D coordinates, inspect per-residue pLDDT confidence color-maps, and interactively rotate and analyze structures"; `esm2-protein-fitness` — ESM-2 zero-shot mutational fitness, computing 20-amino-acid deep mutational scanning heatmaps; `anshagarwal911/aegis-abp-predictor` — "Tandem ESM2 + RF antibiofilm peptide predictor". — [huggingface.co/spaces/anshagarwal911/aegis-abp-predictor](https://huggingface.co/spaces/anshagarwal911/aegis-abp-predictor), [github.com/KarelBerka/Alphafoldology issue 475](https://github.com/KarelBerka/Alphafoldology/issues/475), [issue 826](https://github.com/KarelBerka/Alphafoldology/issues/826) **[SEARCH SNIPPET — NOT VERIFIED]**
- "Hugging Face Spaces allows anyone to host their Gradio demos freely, and uploading Gradio demos takes a couple of minutes by going to hf.co/new-space, selecting the Gradio SDK, and creating an app.py file." — [gradio.app/guides/using-hugging-face-integrations](https://gradio.app/guides/using-hugging-face-integrations) **[SEARCH SNIPPET — NOT VERIFIED]** — **note this conflicts with current HF policy, see (c3).**
- **Long-lived classic server precedent**: PredictProtein has run for 29 years — [NAR 49(W1):W535](https://academic.oup.com/nar/article/49/W1/W535/6276913) **[SEARCH SNIPPET — NOT VERIFIED]**
- The advisor's own precedent ships **code only**: BERT-Promoter is "freely available at https://github.com/khanhlee/bert-promoter". Based on articles retrieved from PubMed; DOI [10.1016/j.compbiolchem.2022.107732](https://doi.org/10.1016/j.compbiolchem.2022.107732) **[ABSTRACT — verbatim]**
- LMCrot lists "Code & Web Server: https://github.com/KCLabMTU/LMCrot" — i.e. even the stronger 2024 paper points at a repo. — [btae290](https://academic.oup.com/bioinformatics/article/40/5/btae290/7658304) **[FULL TEXT]**

### Inferences
- **The NAR editorial, though it is about a journal the student will not publish in, is the best available specification of what a credible predictor web app must do**, and it is free of framework prescriptions. Use it as the requirements document: free, no login, documented limitations, non-programmer accessible, sortable/filterable results, contextual links, maintained.
- "Shiny" and "custom React app" did not appear in anything I found for this niche. React is the student's own stack per the repo structure (frontend/ = React, backend/ = Spring Boot), so a custom React+API app is defensible **as a Software Engineering deliverable** even though it is not the community norm — and it may actually score better with an SE department than a Gradio one-pager.

### Gaps
- **I found no source that surveys the implementation frameworks (Flask vs FastAPI vs Streamlit vs Gradio) used by recent bioinformatics web servers.** Papers almost never state it. So I cannot give a verified distribution; treat any such claim in the final report as unsupported.

---

## (c2) Typical feature set of a credible predictor web app

### Takeaway
Derived from the NAR editorial requirements plus the protein Spaces I found, the credible minimum is: paste-or-upload FASTA, example input, run, per-residue/per-protein scores in a sortable table, one visualisation, CSV/JSON download, an explicit confidence/applicability warning, and a documented limitations page. Batch mode is a differentiator, not a baseline.

### Cited Findings
- From the NAR editorial, as **requirements** (not merely conventions): free and no-login access; usable without the command line; no requirement for heavy user-side pre-processing; results must include **contextual information, not plain text** (gene annotation data, external links); results must support **filtering and sorting**; documentation must state the system's **limitations**, including when the model may be wrong. — [NAR 53(W1):W1](https://academic.oup.com/nar/article/53/W1/W1/8176964) **[FULL TEXT]**
- Concrete per-residue visualisation precedent: the ESMFold Space lets users "inspect **per-residue pLDDT confidence color-maps**" and rotate structures interactively. — [Alphafoldology issue 475](https://github.com/KarelBerka/Alphafoldology/issues/475) **[SEARCH SNIPPET — NOT VERIFIED]**
- Concrete per-position heatmap precedent: the ESM-2 fitness Space produces "comprehensive 20-amino-acid deep mutational scanning heatmaps, identif[ies] highly deleterious vs benign positions, and rank[s] prospective gain-of-function variants." — [Alphafoldology issue 826](https://github.com/KarelBerka/Alphafoldology/issues/826) **[SEARCH SNIPPET — NOT VERIFIED]**
- An applicability/confidence warning has a formal backing available: conformal prediction gives "a user-specified upper bound" on FDR, i.e. the app can honestly say "at the 10% FDR setting, these are the predicted sites". — [PMC11164347](https://pmc.ncbi.nlm.nih.gov/articles/PMC11164347/), [s41467-024-55676-y](https://www.nature.com/articles/s41467-024-55676-y) **[SEARCH SNIPPET — NOT VERIFIED]**

### Inferences — a concrete feature checklist with build order (my judgement, labelled)
**[ESTIMATE — MINE]** Build in this order so that an early stop still leaves something demonstrable:
1. Paste FASTA + one-click **example input** (an example button is the single highest-value feature for a demo in front of an advisor or examiner).
2. Run → per-residue score table, **sortable and filterable** (NAR requirement).
3. One visualisation: a per-residue score track/lollipop along the sequence, with the predicted sites highlighted. Cheap and reads immediately.
4. **Download CSV and JSON.**
5. **Applicability-domain / confidence banner**: show the max sequence identity of the query against the training set and the conformal-calibrated risk level, with explicit wording that predictions outside the applicability domain are unreliable.
6. FASTA **file upload** + batch mode over multiple records, with a results table per record.
7. An **XAI panel**: per-residue attribution overlaid on the score track, plus the attribution-vs-annotation enrichment figure. This is where criterion 4 becomes *visible* in the product rather than buried in the report — a strong move for an SE department, since it turns the XAI contribution into a user-facing feature.
8. A **Limitations** page (NAR requirement, and it protects against overclaiming).

---

## (c3) Build times, free hosting, model-size and cold-start limits, and whether a PLM fits in free-tier memory

### Takeaway
**There is a 2026 policy change the student must know: creating a Gradio or Docker Space on Hugging Face now requires a paid plan (PRO for personal accounts); only static Spaces are free for everyone, with a narrow exception of up to 2 ZeroGPU Gradio Spaces for free personal accounts in good standing.** On memory, the free envelopes are HF Spaces CPU Basic 2 vCPU / 16 GB RAM / 50 GB non-persistent disk, versus Streamlit Community Cloud roughly 0.078–2 cores and 690 MB–2.7 GB RAM. ESM-2 650M or ProtT5-XL will not fit comfortably in Streamlit's envelope; they *can* fit in HF's 16 GB, but slowly and on CPU.

### Cited Findings
- **Hugging Face Spaces, official docs, verbatim warning:** "Static Spaces are free for everyone. **Gradio and Docker Spaces run on compute and require a paid plan to create: PRO for personal accounts, Team or Enterprise for organizations.** Free personal accounts in good standing can still host up to **2 Gradio Spaces running on ZeroGPU**." — [huggingface.co/docs/hub/en/spaces-overview](https://huggingface.co/docs/hub/en/spaces-overview) **[FULL TEXT]**
- Same page: SDK options offered are **Gradio, Docker, and static HTML**. "Each Spaces environment is limited to **16GB RAM, 2 CPU cores and 50GB of (not persistent) disk space** by default. The default **CPU Basic** hardware has **no hourly cost**". Hardware table: CPU Basic 2 vCPU / 16 GB / FREE; CPU Upgrade 8 vCPU / 32 GB / $0.03 per hour; Nvidia T4-small 4 vCPU / 15 GB / 16 GB GPU / $0.40 per hour; 1× L4 $0.80; A10G-small $1.00; A100-large $2.50. — same source **[FULL TEXT]**
- Same page, cold start / sleep: "On free hardware, your Space will '**go to sleep**' and stop executing after a period of time if unused. If you wish for your Space to run indefinitely, consider upgrading to paid hardware." A Space can also be paused manually; paused time is not billed. — same source **[FULL TEXT]**
- Same page: networking is restricted to ports 80, 443 and 8080 — "Any requests going to other ports will be blocked." Secrets/variables are supported via Settings. **Community GPU grants** can be applied for from the Settings tab. Duplicating a Gradio/Docker Space also requires a paid plan on the target account. — same source **[FULL TEXT]**
- Note the older/secondary sources still claim Spaces are simply free ("Hugging Face Spaces start completely free with CPU Basic hosting (2 vCPU, 16GB RAM)"; "A Space sleeps after 48 hours without visitors") — [metacto.com HF pricing](https://www.metacto.com/blogs/the-true-cost-of-hugging-face-a-guide-to-pricing-and-integration), [eesel.ai HF pricing](https://www.eesel.ai/blog/hugging-face-pricing), [toolfreebie.com](https://toolfreebie.com/hugging-face-spaces-free-gpu/) **[SEARCH SNIPPET — NOT VERIFIED]**. **Conflict:** the official docs page above is authoritative on the paid-plan requirement; the "48 hours" sleep figure appears only in third-party sources and is not in the official page I read, so treat 48 h as unconfirmed.
- **Streamlit Community Cloud limits:** "CPU 0.078 cores minimum and 2 cores maximum; Memory **690MB minimum and 2.7GBs maximum**; Storage no minimum and 50GB maximum"; one source notes the widely repeated "1GB RAM" figure is stale (May 2023) and that the February 2024 caps are 690 MB–2.7 GB. Community Cloud offers "**1 private app plus unlimited public apps**"; "Apps will go to sleep if not visited regularly"; `@st.cache_resource` is described as critical because "without it, concurrent users exhaust server memory"; educational/non-profit users can email support@streamlit.io for additional resources. — [theneuralbase.com streamlit resource limits](https://theneuralbase.com/streamlit-for-ai/learn/intermediate/resource-limits/), [pynions.com Streamlit guide 2026](https://pynions.com/streamlit), [docs.streamlit.io manage-your-app](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app), [discuss.streamlit.io "App over its resource limits"](https://discuss.streamlit.io/t/app-over-its-resource-limits/36667) **[SEARCH SNIPPET — NOT VERIFIED; the 690MB–2.7GB range comes from third-party summaries of Streamlit docs, not from a Streamlit page I fetched. Verify before quoting.]**
- **Model sizes that determine feasibility:** ESM-2 ladder 8M / 35M / 150M / 650M params with embedding dims 320 / 480 / 640 / 1280. Reported CPU verdict: 8M and 35M "work fine on CPU", 150M "light batches only", 650M "runs slowly". — [huggingface.co/facebook/esm2_t33_650M_UR50D](https://huggingface.co/facebook/esm2_t33_650M_UR50D), [qwe.edu.pl guide](https://www.qwe.edu.pl/ai-tools/install-esm-2-fair-esm-protein-language-model/) **[SEARCH SNIPPET — NOT VERIFIED]**
- Relevant encouragement: ESM-2 150M reportedly outperforms ESM-1b 650M — [biorxiv 2022.07.20.500902](https://www.biorxiv.org/content/10.1101/2022.07.20.500902v1.full.pdf) **[SEARCH SNIPPET — NOT VERIFIED]** — i.e. serving a smaller checkpoint is not automatically a scientific concession.

### Inferences — hosting decision and build-time estimates
**Hosting recommendation, given the HF paid-plan change:**
- **[ESTIMATE — MINE]** Ranked free options for this student: **(1) Hugging Face Spaces with the ZeroGPU Gradio exception** (free personal accounts may host up to 2 — verify eligibility first, since "in good standing" is undefined and this is the single point of failure); **(2) Streamlit Community Cloud** — genuinely free, but the 690 MB–2.7 GB memory ceiling effectively forbids serving ProtT5-XL or ESM-2 650M in-process; **(3) Render / Fly.io free or hobby tiers** — small RAM, cold starts; **(4) a Can Tho University server**, which is the only option that removes memory limits and is worth asking the advisor about explicitly at week 6; **(5) a static HF Space** (always free) serving a precomputed-results browser with no live model.
- **Memory arithmetic [ESTIMATE — MINE]:** ESM-2 650M at fp32 ≈ 2.6 GB of weights alone (650M × 4 bytes), plus activations — so it exceeds Streamlit Community Cloud's ceiling outright, and fits HF's 16 GB only with care. ESM-2 **35M** at fp32 ≈ 140 MB and **150M** ≈ 600 MB, which do fit Streamlit. ProtT5-XL (~3B params) is **not** servable on any free tier at fp32; this is a hard fact the student should state plainly rather than discover in week 14.

**Build-time estimates. All of the following are [ESTIMATE — MINE], not sourced:**
| Stack | Realistic build time for a working predictor app | Notes |
|---|---|---|
| Gradio single-file `app.py` on HF Spaces | **1–2 days** | Fastest path to something demonstrable; paste FASTA, table, plot, CSV download. Blocked unless the ZeroGPU free exception applies. |
| Streamlit on Community Cloud | **2–4 days** | Similar effort, genuinely free, but forces a small model (≤150M) or precomputed embeddings. |
| FastAPI backend + minimal HTML/JS frontend | **4–7 days** | Gives a real API (nice for an SE thesis), containerisable, deployable to Render/Fly/university server. |
| FastAPI + React frontend (the student's declared stack) | **1.5–2.5 weeks** | Best fit for a Software Engineering department rubric: real separation of concerns, API docs, job queue, tests. Only choose this if the ML work is on schedule by about week 10. |
| Spring Boot + React + separate FastAPI ml-service (the repo's planned architecture) | **2.5–4 weeks** | The repo structure anticipates this three-service design. It is the most impressive SE artefact and the biggest schedule risk; it is only justified if the three-tier architecture is itself part of the thesis story. |

- **[ESTIMATE — MINE]** Given 8–9 weeks total with ML experiments competing for the same time, the defensible plan is: build the **Gradio or Streamlit version first, in week ~10, as insurance** (1–2 days, always have a working demo), then upgrade to **FastAPI + React** in weeks ~12–13 if the experiments are done. Never leave the app to the last week.

### Gaps
- I did not verify Render's or Fly.io's current free-tier RAM, sleep behaviour or whether a free tier still exists. **NOT FOUND.** Both have changed their free offerings repeatedly; the student must check directly.
- No source gave measured cold-start latency for a Space or Streamlit app loading an ESM-2 checkpoint. **NOT FOUND.**
- I did not verify the ZeroGPU free-tier eligibility details beyond the one sentence in the official docs; the linked `./spaces-zerogpu` page was not fetched.

---

## (c4) Common failure mode of thesis web apps here, and honest workarounds

### Takeaway
The classic failure is exactly as hypothesised: the app cannot actually run the PLM within free hosting limits, so it silently serves precomputed results for a fixed protein list and breaks on any new sequence. The honest fixes, in order of preference, are a smaller PLM checkpoint, a queue-based job model, embedding caching, and — if all else fails — labelling the demo truthfully as a precomputed browser.

### Cited Findings
- The memory ceilings that cause the failure are documented: Streamlit Community Cloud max **2.7 GB** RAM ([theneuralbase](https://theneuralbase.com/streamlit-for-ai/learn/intermediate/resource-limits/), [pynions](https://pynions.com/streamlit)) **[SEARCH SNIPPET — NOT VERIFIED]**; HF Spaces CPU Basic **16 GB RAM, 2 vCPU, 50 GB non-persistent disk**, with sleep on inactivity ([HF docs](https://huggingface.co/docs/hub/en/spaces-overview)) **[FULL TEXT]**.
- The "not persistent" qualifier on HF's 50 GB disk is explicit in the official docs — so a cache written at runtime is lost on restart. — [HF docs](https://huggingface.co/docs/hub/en/spaces-overview) **[FULL TEXT]**
- Streamlit community guidance names the standard mitigation: `@st.cache_resource` "loads resources once and shares them across all users and reruns—without it, concurrent users exhaust server memory"; and the official escape hatch is to email support@streamlit.io for an educational/non-profit resource increase. — [theneuralbase](https://theneuralbase.com/streamlit-for-ai/learn/intermediate/resource-limits/), [discuss.streamlit.io 36667](https://discuss.streamlit.io/t/app-over-its-resource-limits/36667) **[SEARCH SNIPPET — NOT VERIFIED]**
- Small checkpoints genuinely exist and are competitive: ESM-2 8M/35M/150M, with 150M reportedly beating ESM-1b 650M. — [HF ESM docs](https://huggingface.co/docs/transformers/model_doc/esm), [biorxiv 2022.07.20.500902](https://www.biorxiv.org/content/10.1101/2022.07.20.500902v1.full.pdf) **[SEARCH SNIPPET — NOT VERIFIED]**
- The NAR editorial's documentation requirement is the professional norm that makes honesty mandatory rather than optional: documentation must state "the underlying data and, most importantly, **the limitations of the system**", including when models might produce incorrect results. — [NAR 53(W1):W1](https://academic.oup.com/nar/article/53/W1/W1/8176964) **[FULL TEXT]**
- HF offers a legitimate upgrade route without payment: community GPU grants applied for from the Space Settings tab. — [HF docs](https://huggingface.co/docs/hub/en/spaces-overview) **[FULL TEXT]**

### Inferences — ranked honest workarounds (my judgement)
**[ESTIMATE — MINE]**
1. **Train the final model on a small PLM checkpoint on purpose.** Use ESM-2 **35M or 150M** for the deployed model, and report the ProtT5-XL / ESM-2 650M numbers as the research-grade upper bound in a table. Framing this as a deliberate accuracy-vs-deployability study turns the constraint into a *contribution* (a deployability ablation) instead of a confession. This is the single best fix and it also directly serves the SE department's interest in engineering trade-offs.
2. **Queue-based job model.** Submit sequence → job id → poll for result; the heavy embedding step runs in a worker. This is the right answer architecturally and it also makes a good SE deliverable (async API, job states, retries). It does not, however, create memory that is not there — it only hides latency.
3. **Cache embeddings for the evaluation set and for the example inputs**, so the demo is instant and robust for everything the examiner will actually click, while still computing live for novel sequences. Because HF's 50 GB disk is **not persistent**, ship the cache in the repo (or a HF Dataset) rather than building it at runtime.
4. **Length cap and batch cap** on the public app (e.g. reject sequences over some length, cap batch size), stated in the UI. This is standard practice and prevents the OOM that otherwise kills the demo during the defence.
5. **Last resort, done honestly:** a static Space / precomputed-results browser, with a prominent banner saying it serves precomputed predictions for N proteins, plus a Colab notebook link and a Docker image for running on new sequences. This is not a failure if it is *labelled*; the failure mode is pretending otherwise.
6. **Ask the advisor for a Can Tho University server at week 6.** It costs nothing to ask and it removes the entire constraint. Also apply for an HF community GPU grant — it is free to apply and the docs explicitly invite it.
7. **Anti-pattern to avoid:** calling a third-party hosted inference API for the PLM at request time. It introduces a key, a quota, a cost and a dependency the student cannot guarantee for the lifetime of the thesis, and NAR-style norms (no login, free) exist precisely because of this.

### Gaps
- I found **no paper or post that candidly documents a thesis-level predictor web app failing this way**; the failure mode is inferred from the documented memory limits plus the model sizes, not from a source describing it. The report should present it as a reasoned risk, not a cited phenomenon.
- Whether ZeroGPU (the free Gradio exception) can hold an ESM-2 650M model in GPU memory and for how long per request: **NOT FOUND**.

---

## Cross-cutting note for the week-6 pitch (synthesis, my judgement)

**[ESTIMATE — MINE]** The cheapest way to hit criteria 3, 4 and 5 simultaneously, reusing everything the student already has:
- **Criterion 3 (genuinely new method):** replace frozen ProtT5 with a **structure-aware PLM (ProstT5 / SaProt)** and/or move from frozen features to **LoRA fine-tuning** — both are the next step in the advisor's own PSSM→PLM→? narrative, neither collides with SirtSAGE's GATv2+pLDDT, and neither requires skills the student lacks. Add a **KAN head** on the mCNN for a second, orthogonal method increment.
- **Criterion 4 (XAI):** per-residue attribution (Captum integrated gradients or SHAP GradientExplainer) + **quantified enrichment of high-attribution positions in independent UniProt functional annotations** (the ESM2_AMP 54.78% move, at residue level) + the three-check faithfulness protocol + a leakage-stratified attribution comparison. Explicitly position this as going beyond BERT-Promoter, where SHAP was used only for feature selection.
- **Criterion 5 (web app):** Gradio/Streamlit insurance build in week ~10, FastAPI+React upgrade in weeks 12–13, served with a **small ESM-2 checkpoint by design**, carrying a **conformal-prediction applicability warning** and an **XAI panel** — which makes criteria 4 and 5 reinforce each other instead of competing for time.
- **Single biggest open risk to verify before week 6:** whether SaProt/ProstT5 require a 3D structure at inference time. If they do, the structure-aware-PLM recommendation inherits the GNN route's deployment problem and the fallback is LoRA + KAN instead.

## Link resolution log

Resolved and read in full (fetched successfully): huggingface.co/docs/hub/en/spaces-overview; academic.oup.com/nar/article/53/W1/W1/8176964; academic.oup.com/bioinformatics/article/40/5/btae290/7658304; academic.oup.com/bioinformatics/article/42/7/btag433/8712719; academic.oup.com/bib/article/26/4/bbaf434/8242608; arxiv.org/abs/2506.19532 (abstract only).
Resolved via PubMed MCP (official metadata, verbatim abstract): PMID 35863177 / DOI 10.1016/j.compbiolchem.2022.107732.
**Failed to resolve:** pubmed.ncbi.nlm.nih.gov/35863177/ (cookie wall, no content); sciencedirect.com/science/article/abs/pii/S1476927122001323 (HTTP 403); europepmc.org/article/MED/35863177 (HTTP 403); khanhlee.github.io/publication/2022-07-14-BERT-Promoter (301 → aibiomedlab.com/... → HTTP 404).
All other URLs in this document come from search-result listings and were **not individually fetched**; they are marked [SEARCH SNIPPET — NOT VERIFIED] at point of use.
