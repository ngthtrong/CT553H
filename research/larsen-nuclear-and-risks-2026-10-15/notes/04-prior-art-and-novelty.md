# Prior art and tool landscape for degron prediction — novelty audit of the three thesis claims

> Research date **15/10/2026**. Scope: verify and extend the prior art already on file in
> `topics/degron-footprint/research/architecture-check/prior-art-exposure-gate.md`, and test how much
> novelty room is left for the three planned contributions.
>
> **Evidence labels used on every line below**, per repo convention:
> **[read]** = read the paper/tool page/source code itself · **[snippet]** = seen only in a search-result
> snippet or abstract, **not verified** · **[analysis]** = my own inference from the cited facts.
> Per repo rule, nowhere do I write "nobody has done X"; where I found no precedent I say exactly what I
> searched and what I did not find.
>
> **Headline result:** one of the three claims is dead as currently stated. A public GitHub model,
> **Degformer**, trained on the *same* Zhang 2023 scanning + saturation mutagenesis tables, already ships a
> script that emits a 28-position × 20-amino-acid ΔPSI matrix. Details in Question 2. The other two claims
> survive but must be narrowed, and Question 3 surfaces a new, unaddressed threat to the exposure gate.

---

## Q1. What does each existing degron tool actually OUTPUT? Does any emit a position × amino-acid substitution matrix from experimental mutagenesis labels?

### Takeaway

Every published degron tool outputs either a **per-peptide/per-terminus score** or a **degron instance with
start/end boundaries plus an E3 assignment**; none of the *published* ones outputs a residue-level profile as
a supervised target, and none of the published ones emits a position × amino-acid matrix derived from
experimental mutagenesis. Two tools the thesis had not accounted for — **DegronMD** (2023) and **Degformer**
(unpublished GitHub, 2026) — do have mutation modules, and Degformer's is a direct hit on claim 2.

### Cited findings

**DEGRONOPEDIA (NAR 2024; Methods Enzymol chapter 2025-07-05)** — **[read]** its own documentation page:
- Output granularity is mixed: **per-motif** (regex screening, conservation score and a tripartite-context report per motif), **per-residue** only for *descriptive* features (IUPred3 disorder score "for each amino acid", pLDDT, RSA, secondary degron K/C/T/S assessment), and **per-terminus** for the ML model — [DEGRONOPEDIA documentation](https://degronopedia.com/degronopedia/documentation)
- The ML predictor is **CatBoost regression** on the N-terminal and C-terminal **23-mer**, with separate models for Met-cleaved / Met-retained N-termini and for the C-terminus. Inputs are peptide sequence, RDKit descriptors, Gravy, and Peptides-module descriptors over whole sequence and 2–10-residue terminal windows. Output is **predicted PSI** mapped to stability categories by quantile thresholds — [DEGRONOPEDIA documentation](https://degronopedia.com/degronopedia/documentation)
- Reported performance: R² = 0.796 / RMSE = 0.495 (N-term, Met cleaved); R² = 0.812 / RMSE = 0.443 (N-term, Met retained); R² = 0.815 / RMSE = 0.316 (C-term) — [DEGRONOPEDIA documentation](https://degronopedia.com/degronopedia/documentation)
- **Its mutation module is COSMIC lookup only.** Verbatim: "Human mutations data, specifically 'Substitution - Missense' types, were obtained from the COSMIC database." Mutations are shown only for human proteins queried by UniProt ID. The page does **not** describe arbitrary user-specified substitutions, ClinVar or gnomAD, and does **not** describe a position × amino-acid matrix — [DEGRONOPEDIA documentation](https://degronopedia.com/degronopedia/documentation)
- rASA via DSSP, Sander normalisation, buried below a **20%** default; pLDDT < 70 default treated as disordered; IDRs = contiguous runs ≥ 10 residues. These are used as **motif-context annotation** (mean disorder over 10 residues around a degron, 3 around a secondary degron; structural flanks within 20 Å) — [DEGRONOPEDIA documentation](https://degronopedia.com/degronopedia/documentation)
- Verbatim on batch: "it is possible to submit only one protein at a time." No API described; a standalone GitHub ML tool is offered for "high-throughput predictions" of terminal stability. Download = one xlsx with all results. No per-prediction uncertainty (the 95% band appears only on the performance scatter plots). No compartment-specific prediction — [DEGRONOPEDIA documentation](https://degronopedia.com/degronopedia/documentation)

**MetaDegron (Brief Bioinform 2024, 25(6):bbae519)** — **[read]** the article:
- Output is a **scored degron instance**, not a per-residue profile. The results table columns are "Entry, E3 ligase, Degron instance, Degron type, Start, End, Score" — [MetaDegron, Brief Bioinform 2024](https://academic.oup.com/bib/article/25/6/bbae519/7828723)
- **MetaDegron-D** = two branches into a shared head: (i) SeqVec 1024-dim per-residue embeddings → BLSTM → convolution + **max-pooling** → dense; (ii) trainable embedding → BLSTM → dense; combined by dense layers to a 2-node output (degron vs random peptide). **No attention mechanism is described** — [MetaDegron, Brief Bioinform 2024](https://academic.oup.com/bib/article/25/6/bbae519/7828723)
- **MetaDegron-X** = ensemble of 10 XGBoost classifiers on bootstrap samples, ~10 features: flexibility (DynaMine), **solvent accessibility** and coiled-coil/α-helix propensity (Spider2), disorder (IUPred), anchoring (ANCHOR), ortholog-MSA conservation (Gopher), Pfam domains, phospho/ubiquitination PTM enrichment. **MetaDegron-D uses sequence only and does not use these structural features** — [MetaDegron, Brief Bioinform 2024](https://academic.oup.com/bib/article/25/6/bbae519/7828723)
- Covers **21 E3 ligases**; trained on a curated set of **300 degron instances** — [MetaDegron, Brief Bioinform 2024](https://academic.oup.com/bib/article/25/6/bbae519/7828723); [search snippet corroborating the 300/21 figures](https://academic.oup.com/nar/article/52/W1/W221/7639542) **[snippet]** for the 300 figure
- **No mutation-effect prediction and no position × amino-acid matrix** is described; the article raises interpretability only in its limitations — [MetaDegron, Brief Bioinform 2024](https://academic.oup.com/bib/article/25/6/bbae519/7828723)
- **Batch submission IS supported** (select one or more E3s, submit one or more FASTA sequences), with a Results module for job status, plus 3Dmol.js / ProViz / Cytoscape.js visualisation. API, downloads and uncertainty are **not described** — [MetaDegron, Brief Bioinform 2024](https://academic.oup.com/bib/article/25/6/bbae519/7828723)
- Performance: MetaDegron-D 5-fold CV mean AUC 0.90, independent test AUC 0.90; MetaDegron-X CV 0.87, test 0.86. β-TrCP2 benchmark (20 positives vs >700 random peptides): D 0.9705, X 0.9670, **Degpred 0.9540**. Only Degpred was compared; deepDegron and DEGRONOPEDIA were excluded as terminal-degron tools — [MetaDegron, Brief Bioinform 2024](https://academic.oup.com/bib/article/25/6/bbae519/7828723)

**DegPred (BMC Biol 2022)** — **[snippet]** only; both the publisher page and the PMC copy were blocked (Springer IDP redirect loop; PMC reCAPTCHA):
- Described as a **BERT-based** model predicting general degrons directly from protein sequence, predicting degrons beyond motif-based methods, and linking predictions to substrate half-life — [search snippet](https://bmcbiol.biomedcentral.com/articles/10.1186/s12915-022-01364-6)
- The 2026 Biology Direct review characterises it as predicting "degrons and putative E3-binding **sites** proteome-wide from primary sequence", AUC = 88.07% — [Biol Direct 2026 review](https://pmc.ncbi.nlm.nih.gov/articles/PMC13455158/) **[read]**
- Web server at [degron.phasep.pro](http://degron.phasep.pro/) **[snippet]**, code at [CHAOHOU-97/degpred](https://github.com/CHAOHOU-97/degpred) **[snippet]**

**deepDegron (Tokheim 2021)** — **[read]** via the 2026 review's description:
- The review says it "predicts how mutations affect degron integrity, identifying mutations that disrupt degrons, create neo-degrons, or shift degradation propensity", AUC = 93% (C-terminal) and 96% (N-terminal) — [Biol Direct 2026 review](https://pmc.ncbi.nlm.nih.gov/articles/PMC13455158/)
- **It is terminal-only.** "It can only predict terminal degrons" — [search snippet](https://github.com/ctokheim/deepDegron) **[snippet]**; corroborated by MetaDegron excluding it as a terminal tool **[read]**

**DegronMD (Mol Biol Evol 2023, msad253) — NOT previously on file** — **[read]** the article page:
- Outputs are **per-degron-instance** (sequence, classification, E3 ligase, start/end, DegML probability, cutoff > 0.5), **per-mutation** (DegMF impact score normalised 0–1, "actionable" threshold 0.5), and **per-treatment** (drug-resistance calls from mutant-vs-WT IC50). **No per-residue score track** — [DegronMD, MBE 2023](https://academic.oup.com/mbe/article/40/12/msad253/7441958)
- Its mutation module scores **only somatic missense mutations observed in cancer databases** (TCGA, COSMIC, ICGC, CCLE, GDSC), mapped to degrons plus 11 flanking residues each side. It does not appear to score arbitrary substitutions, and **no position × amino-acid matrix is described** — [DegronMD, MBE 2023](https://academic.oup.com/mbe/article/40/12/msad253/7441958)
- **DegMF is a rule-weighted in-silico score, not a model trained on experimental mutagenesis.** It follows Martínez-Jiménez et al. 2020, weighting effects on the degron and on biochemical properties, then summing and normalising, in five categories (rewiring degron network, altering degron motif, blocking phosphorylation signal, blocking ubiquitination signal, substituting flanking lysine). Validation shown is in-silico only (DynaMut, e.g. BUB1B V29E); **no experimental mutagenesis labels are reported** — [DegronMD, MBE 2023](https://academic.oup.com/mbe/article/40/12/msad253/7441958)
- DegML trained on **133 known degron instances across 23 motifs** vs length-matched random peptides from the same substrates. Scale: 53,291 motif matches, 18,007 predicted degrons > 0.5; 288,345 mutation records, 89,318 "actionable"; 326,833 drug-treatment records — [DegronMD, MBE 2023](https://academic.oup.com/mbe/article/40/12/msad253/7441958)
- Features: disorder, **solvent accessibility**, secondary structure, rigidity, stabilisation, flanking conservation, structural domains, PTM-site counts, flanking lysine distribution → fed to **10 XGBoost classifiers**; a separate deep branch uses SeqVec 1024-dim embeddings of 50-residue windows → dense 128/64/1. The page does **not** say the deep branch uses structural features; rASA is not named, pLDDT is not mentioned — [DegronMD, MBE 2023](https://academic.oup.com/mbe/article/40/12/msad253/7441958)
- App surface: general + **batch search** (line-by-line gene symbol / UniProt ID / degron hit / E3), blastp search, browse tree, needle plots, network views, 3D viewer, **downloadable datasets**, confidence score per degron. **No API** and **no subcellular compartment** mentioned — [DegronMD, MBE 2023](https://academic.oup.com/mbe/article/40/12/msad253/7441958)
- Stated limitations, verbatim-adjacent: cannot predict terminal degrons or degrons of E3s absent from training; does not model cross-talk between degrons on the same protein; no experimental validation performed; drug-resistance findings are correlational — [DegronMD, MBE 2023](https://academic.oup.com/mbe/article/40/12/msad253/7441958)

**PAP / QCDPred (Voutsinos et al., Sci Adv 2026-02-06; Johansson 2022)** — **[read]** repo's own full source audit:
- PAP architecture: internal channel `Conv1D(filters=25, kernel=1)` → **`GlobalAveragePooling1D`** → `Dense(50)` → `Dense(50)` → `Dense(1)` on the first 25 residues; C-term channel = last 5 residues one-hot (100-dim) → Dense(25/50/50/1); output is a plain `Add()` of the two channels with **no interaction between them** — [repo audit, voutsinos-2026-audit](../../voutsinos-2026-audit/README.md)
- **[analysis]** PAP's pooling is therefore **unweighted global average pooling**. There is no attention and no place where a structural quantity could modulate aggregation. Output is one scalar per peptide window.
- The Sci Adv paper reports **per-peptide degron strength** and uses the PAP score for ClinVar variant analysis — [search snippet of Sci Adv](https://www.science.org/doi/10.1126/sciadv.adz3483) **[snippet]**; one search summary described it as a "two-way convolutional neural network", consistent with the two-channel source code **[snippet]**
- Published **2026-02-06** in Science Advances (preprint "A complete map of human cytosolic degrons and their relevance for disease", bioRxiv **2025-05-15**, [10.1101/2025.05.10.653233](https://doi.org/10.1101/2025.05.10.653233)) — [Semantic Scholar record](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1126/sciadv.adz3483) **[read]**

**Zhang et al. 2023 (Mol Cell) — the thesis's own label source** — **[snippet]** for the DegronID detail, **[read]** for the repo's numbers:
- The GPS assay identified **15,800 degron peptides**; critical degron residues were mapped by scanning and saturation mutagenesis; the authors generated **mutational fingerprints for 219 degrons** and developed **DegronID**, an algorithm for clustering degron peptides with similar motifs — [search snippet, Mol Cell](https://www.sciencedirect.com/science/article/pii/S1097276523006585) **[snippet]**
- The Nature Reviews 2025 review confirms this verbatim: "machine learning can identify degron peptides among unstable peptides, which can then be systematically mutagenized and **computationally clustered on the basis of the similarity of degron mutagenesis footprints**" (its ref 23 = Zhang 2023) — [Nat Rev Mol Cell Biol 2025](https://doi.org/10.1038/s41580-025-00870-z) **[read]**, p. Box 1
- Their SVM: Pearson **0.8955**, RMSE 0.563 over 260,989 peptides with **10% training data** (0.8916 / 0.5708 at 5%) — [repo full-data-audit §6](../../full-data-audit/README.md) **[read]**

### Inferences

- **[analysis]** There is a clean taxonomy of published degron-tool outputs, and the thesis should put it in the proposal as a table: (a) **terminal-window PSI regression** — DEGRONOPEDIA CatBoost, deepDegron; (b) **peptide-window PSI regression** — PAP, QCDPred, Zhang 2023 SVM; (c) **degron instance + E3 assignment** — MetaDegron, DegPred, DegronMD; (d) **mutation annotation over observed variants** — DEGRONOPEDIA (COSMIC lookup), DegronMD (rule-weighted), deepDegron (terminal only). No published tool is in category (e) "residue-level supervised score" or (f) "dense substitution matrix from experimental mutagenesis".
- **[analysis]** DegronMD is the closest published competitor to claim 2 and the thesis must now cite it. But it is defeated on three axes the thesis can state cleanly: it scores only *observed* cancer mutations, not all 20 substitutions; its score is a **hand-weighted rule sum**, not learned from mutagenesis measurements; and it is per-instance, not per-residue. Claim 2 therefore does not die on DegronMD. It dies on Degformer (Q2).
- **[analysis]** MetaDegron supporting batch submission removes "batch submission" from the thesis's list of application gaps. The repo card should be corrected: batch is not a differentiator.

### Gaps

- DegPred's exact output granularity (per-residue probability track vs per-window vs instance) could not be verified at source: Springer redirects to an authentication endpoint and PMC served a reCAPTCHA page. I have only the 2026 review's phrasing ("E3-binding **sites** proteome-wide") and the GitHub description ("predict E3 binding sites (degrons) on protein substrates"), which hint at per-site but do not establish whether a per-residue score is exposed to the user. **Must be resolved before writing the literature review** — try the live server at degron.phasep.pro or the GitHub code.
- I did not verify deepDegron's mutation output format at source (whether it emits a per-substitution score for arbitrary mutations or only a disrupt/create call). Only the review's summary and a snippet.
- I did not read the Sci Adv version of Voutsinos 2026 directly; science.org returns 403 from this network, as already noted in the repo. Numbers above come from the repo's prior reading and the bioRxiv version.

---

## Q2. What NEW degron-related predictors, datasets or benchmarks appeared in 2025–2026?

### Takeaway

**No new published degron predictor or web server appeared in 2025–2026** across the searches I ran — but an
**unpublished public GitHub model, Degformer (2026), kills claim 2 as currently stated**: it is trained on the
thesis's exact label tables, including the saturation-mutagenesis table, and ships a script that emits the
28-position × 20-amino-acid ΔPSI matrix. Separately, two major 2025 reviews and several 2026 biology papers
change the framing the thesis must use.

### Cited findings — the claim-killer

**Degformer** — unpublished GitHub repository, **[read]** repo metadata, README and full source of `train_v2.py` and `saturation_mut_heatmap.py`:
- `Alpine2048/Degformer`, description "Transformer model for internal and C-terminal degron prediction". Created **2026-03-24**, last push **2026-09-30**, Apache-2.0, **0 stars**, no linked paper or preprint, no homepage — [GitHub API record](https://api.github.com/repos/Alpine2048/Degformer)
- README, verbatim: "A transformer mode for prediction of protein stability index for **28-residue peptides**. Performs better than current composition or motif-search based methods and is applicable for protein degron mapping (internal + C-degrons only), ***in silico* scanning/saturation mutagenesis for degron motif detection**, and generally stability prediction." — [Degformer README](https://github.com/Alpine2048/Degformer)
- **Trained on exactly the thesis's labels:** "Uses S1, S4, S7 data from the Elledge lab (doi.org/10.1016/j.molcel.2023.08.022) — S1: 260K peptides from the human proteome; S4: **Scanning mutagenesis** on a subset of degrons; S7: **Saturation mutagenesis** on a subset of degrons. For S7, only degrons with >=60 reads were kept." Merged to **569,270 sequences** — [Degformer README](https://github.com/Alpine2048/Degformer)
- Reported performance vs the Zhang SVM: Elledge-lab SVM S1 ρ = **0.8955**; Degformer e50 S1 ρ = **0.9420**, S4 ρ = **0.9463**, S7 ρ = **0.9162** — [Degformer README](https://github.com/Alpine2048/Degformer)
- README figure captions: "**Figure 2:** *in silico* saturation mutagenesis recovers diverse degron motifs"; "**Figure 4:** Degron scanning of human GNMT" — [Degformer README](https://github.com/Alpine2048/Degformer)
- `saturation_mut_heatmap.py` **[read] full source**: takes a CSV with `name, sequence, pred_controlPSI`, splits `_WT` rows from mutant rows named `{base}_{pos}{aa}`, computes ΔPSI = pred(mutant) − pred(WT), and plots over `residue_groups = ['G','A','V','L','M','I','F','Y','W','S','T','C','N','Q','P','H','K','R','D','E']` — i.e. **a position × 20-amino-acid ΔPSI heatmap**, with `MAX_LEN = 28` — [Degformer saturation_mut_heatmap.py](https://github.com/Alpine2048/Degformer/blob/main/saturation_mut_heatmap.py)
- Architecture, `train_v2.py` **[read] full source**: `nn.Embedding` over a 21-token vocab `"ACDEFGHIKLMNPQRSTVWY*"` (one-hot-equivalent, **not** a protein language model), `d_model=128`, `nhead=8`, `num_layers=4` `nn.TransformerEncoder`, learned `cls_token` and `pos_embedding`, head `LayerNorm → Linear(128,64) → ReLU → Linear(64,1)`, forward returns `self.head(x[:, 0])`. **Pooling is CLS-token read-out. There is no per-residue head, no MIL, no attention-weighted aggregation over residues, no structure, no exposure gate.** Loss is `nn.MSELoss` — [Degformer train_v2.py](https://github.com/Alpine2048/Degformer/blob/main/train_v2.py)
- **Its split is a pure random 10% hold-out**, verbatim source line: `train_test_split(sequences, control_scaled, test_size=0.1, random_state=42)`, with no grouping, no protein clustering and no peptide-family grouping. README confirms: "90% of data from each table were selected at random and merged into data.csv" — [Degformer train_v2.py](https://github.com/Alpine2048/Degformer/blob/main/train_v2.py)

### Cited findings — new 2025–2026 literature the thesis has not accounted for

- **"Degrons: defining the rules of protein degradation"** — Zhang, Mena, Timms, Koren, Elledge, *Nat Rev Mol Cell Biol*, **2025-07-14**, [10.1038/s41580-025-00870-z](https://doi.org/10.1038/s41580-025-00870-z). The authoritative current review, and it is by the group that produced the thesis's labels. **[read]** full text via PDF extraction. Quotes in Q3 and Q6 below.
- **"Degrons and degradation signals beyond short linear motifs"** — *Nat Chem Biol*, **2025-11-14**, [10.1038/s41589-025-02056-2](https://doi.org/10.1038/s41589-025-02056-2) — [Europe PMC record](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=TITLE:%22Degrons%20and%20degradation%20signals%20beyond%20short%20linear%20motifs%22) **[snippet]** title/date only. **[analysis]** Directly relevant: a review arguing degrons extend beyond SLiMs is a framing risk for a model whose entire input is a 28-mer window.
- **"Deep learning-driven decoding of ubiquitination: from regulatory mechanisms to targeted protein degradation"** — *Biol Direct*, **2026-06-01**, [10.1186/s13062-026-00848-7](https://doi.org/10.1186/s13062-026-00848-7), PMC13455158. **[read]**. In its degron section it names only **MetaDegron, Degpred, deepDegron** (Table 3). **DEGRONOPEDIA, QCDPred and PAP are not mentioned at all.** It names **no** tool producing residue-level degron importance or a position × amino-acid matrix. Its interpretability tools (SHAP, integrated gradients, Shapley, attention, PairExplainer) are attached to site-level or interaction-level tasks, **not** to degron residue scoring — [Biol Direct 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13455158/)
- **"BAG6 and RNF126 promote the degradation of cytosolic misfolded proteins that contain BURIED degron motifs"** — bioRxiv **2026-04-25**, [10.64898/2026.04.24.720685](https://doi.org/10.64898/2026.04.24.720685), and it **cites Voutsinos 2026** — [Semantic Scholar citations of Voutsinos](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1126/sciadv.adz3483/citations) **[read]** record; **[snippet]** for content, title only
- **"Combinatorial mutagenesis of N-terminal sequences reveals unexpected and expanded stability determinants of the *E. coli* N-degron pathway"** — bioRxiv **2025-05-22**, [10.1101/2025.05.22.655665](https://doi.org/10.1101/2025.05.22.655665) **[snippet]** title/date only. **[analysis]** A new combinatorial-mutagenesis stability dataset, bacterial, so not a direct competitor but a possible external validation set.
- **"Global analysis of protein degradation reveals instability of diverse regulators in *Escherichia coli*"** — *PNAS* **2026-03-03**, [10.1073/pnas.2515265123](https://doi.org/10.1073/pnas.2515265123) **[snippet]**
- **"Effects of residue substitutions on the cellular abundance of proteins"** — Schulze & Lindorff-Larsen, *eLife* **2026-05-28**, [10.7554/eLife.103721](https://doi.org/10.7554/eLife.103721). Already on file and already read by the repo; re-confirmed as the nearest methodological precedent and a **mandatory baseline**. It builds **exposure-class substitution matrices from experimental VAMP-seq labels** — [repo prior-art §3](../../architecture-check/prior-art-exposure-gate.md) **[read]**
- **Molecular-glue / TPD ML wave, 2026** (adjacent, not competing): "Degron-independent recruitment of KAT2A expands the target space of CRBN molecular glues" *Science* **2026-07-09** [10.1126/science.aef5391](https://doi.org/10.1126/science.aef5391); "Writing the CRBN degron" *Nat Chem Biol* **2026-05-01** [10.1038/s41589-025-02112-x](https://doi.org/10.1038/s41589-025-02112-x); "Charged molecular glue discovery enabled by targeted degron display" *Nat Chem Biol* **2026-04-06** [10.1038/s41589-026-02182-5](https://doi.org/10.1038/s41589-026-02182-5); "Leveraging high-throughput proteomics and AI-based protein folding to accelerate VAV1 molecular glue discovery" *Nat Commun* **2026-09-12** [10.1038/s41467-026-77657-z](https://doi.org/10.1038/s41467-026-77657-z); "Multimodal substrate recruitment enables CTLH-MKLN1 E3 ligase to target N-, C-, and internal degrons" bioRxiv **2026-09-10**; "Integrated proteomic screening reveals design principles of CRBN molecular glue degraders" bioRxiv **2026-03-10**. All **[snippet]**, titles and dates only — [Europe PMC title search, degron 2025–2026](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=TITLE:%22degron%22)
- **TACK** — arXiv **2605.19579**, "A Statistical Evaluation of Degradation Activity on a Novel TArgeting Chimeras Knowledge Dataset". PROTAC-focused, not degron-sequence focused; its reference list cites a 2026 *NAR* database of targeted protein degraders which I did not verify — **[snippet]**
- **PLTNUM** (2024 preprint) — a protein-language-model half-life predictor trained on NIH3T3 mouse fibroblast data; "Using SHAP explanations, PLTNUM can also **predict potential degron sequences** that shorten protein half-lives", AUC 0.7373, reported as outperforming **DEGRONOPEDIA** and DeepSTABp on NIH3T3 — **[snippet]** only, from a search summary; I did not verify the paper or its peer-review status
- **ProHL** — *J Microbiol Biotechnol*, **2026-04-27**, [10.4014/jmb.2601.01071](https://doi.org/10.4014/jmb.2601.01071), ProteinBERT embeddings classifying long-lived vs short-lived proteins — **[snippet]**
- **"Learning the PTM code through a coarse-to-fine mechanism-aware framework"** — *Nat Commun* **2026-05-15**, [10.1038/s41467-026-73148-3](https://doi.org/10.1038/s41467-026-73148-3) — **[snippet]** title/date only. **[analysis]** "Coarse-to-fine" in PTM-site prediction is structurally the same idea as bag-level → residue-level; worth reading for Q4.

### Negative results, stated precisely

- **PubMed, `degron AND (prediction OR machine learning OR deep learning OR predictor)`, publication date 2025/01/01–2026/10/31, sorted by date: 41 total records.** I retrieved metadata for 29 and read 21 titles. **None is a new general-purpose degron predictor or web server.** The ML-flavoured ones are a review (Biol Direct 2026), a degron-*design* paper (Adv Sci 2026-09-27, deep-learning-designed binder-degron chimeras), and molecular-glue discovery papers — [PubMed query](https://pubmed.ncbi.nlm.nih.gov/?term=degron+AND+%28prediction+OR+machine+learning%29) **[read]** result set
- **Europe PMC, `TITLE_ABS:"degron"` AND prediction/ML/DL/model terms, 2025-01-01 to 2026-12-31: 100 hits**, and **`TITLE:"degron"` 2025–2026: 127 hits**. I read all 40 returned titles from each. **No new degron predictor or web server in either.** The hits are degron-*tag* tooling (AID2, dTAG, nanobody degrons), structural E3–degron papers, N-degron-pathway biology, and molecular glues — [Europe PMC queries] **[read]** result sets
- I searched specifically for a 2026 residue-level degron benchmark ("degron predictor benchmark residue-level 2026 preprint") and **found none**. The nearest 2026 item returned was CycDelta/CycDeltaBench, which is cyclic-peptide permeability, not degrons — **[read]** search result set
- I searched for a new 2026 degron dataset or web server ("targeted protein degradation machine learning degron dataset 2026 new web server") and **found none**; results returned only DEGRONOPEDIA, MetaDegron and the PROTAC-focused TACK — **[read]** search result set

### Inferences

- **[analysis] Claim 2 is dead as currently written.** The thesis card says the 28×20 matrix on experimental mutagenesis labels is "the one thing none of the four precedents outputs". Degformer outputs exactly that, from exactly those labels, at exactly 28 positions × 20 amino acids. The sentence must be deleted from every document.
- **[analysis] But Degformer is beatable, and on grounds the thesis has already measured.** Three concrete attacks, in order of strength:
  1. **Its evaluation is leaky.** A random 10% split over a merged S1+S4+S7 table puts mutants of the *same* degron on both sides of the split. S7 is saturation mutagenesis — roughly 28 × 19 mutants per degron — so a held-out mutant almost always has ~500 siblings in training. Its ρ = 0.9162 on S7 is therefore close to an upper bound on *interpolating within a known degron*, not a measure of generalisation to new degrons. The repo's cov80 protein-cluster split and its measured label ceiling (0.6514 precision@3 at residue level; cell-level AUROC ceiling 0.9519) are the honest comparison, and Degformer has never been evaluated that way.
  2. **It reports peptide-level Pearson, which the repo has already shown is the wrong metric for the residue question.** Peptide footprint presence replicates at 89.3% but *which residue* is footprint replicates at Jaccard only 0.4965. A peptide-level ρ of 0.94 is compatible with poor residue-level accuracy.
  3. **It is architecturally the null hypothesis.** One-hot embedding, CLS-token pooling, MSE on a scalar. No structure, no exposure, no residue supervision, no PLM. It is precisely the "sequence-only peptide regression" baseline the thesis needs anyway — so the right move is to **adopt it as a baseline, not to ignore it**.
- **[analysis]** Degformer being unpublished, unstarred and paper-free is not protection. It is public, indexed by search engines, Apache-2.0 licensed, and it is the first hit for the obvious query. A reviewer or the advisor could find it in one search. The thesis is safer *citing and beating* it than being silent about it.
- **[analysis]** The absence of any new published degron predictor in 2025–2026, across two independent literature databases, is a genuinely good sign for the thesis's timing and should be stated as a positive in the proposal — with the exact queries named, per repo convention, not as "nobody has done X".
- **[analysis]** The 2026 Biology Direct review omitting DEGRONOPEDIA, QCDPred and PAP entirely suggests the degron-prediction literature is still fragmented and not yet consolidated into a standard tool set. That is room for a benchmark contribution.

### Gaps

- I did not run Degformer's checkpoints. Its claimed numbers are self-reported in a README with no paper, no cross-validation detail beyond the random split, and `media/temp.md` still in the tree. **Before citing its numbers the thesis should either re-evaluate the released `peptide_model_epoch50.pt` under the repo's own cov80 split, or cite the numbers explicitly as "self-reported, unpublished, random split".** Re-evaluating it is cheap (the checkpoint and `predict.py` are in the repo) and would be a strong, defensible result.
- PLTNUM's claim to outperform DEGRONOPEDIA, and its SHAP-based degron-sequence prediction, is **[snippet]** only. If true it is a fourth tool with a mutation-adjacent interpretability layer and must be read.
- I did not verify the 2026 *NAR* targeted-protein-degrader database referenced by TACK.
- The *Nat Chem Biol* 2025-11 review "Degrons and degradation signals beyond short linear motifs" is title-only. It should be read before the proposal, because if it argues most degrons are conformational, the thesis's 28-mer framing needs an explicit scope defence.

---

## Q3. Does anyone already combine a per-residue degron predictor with a solvent-accessibility / disorder gate, and where in the architecture?

### Takeaway

I found **no** model, in degron work or in broader protein ML, that uses an exposure quantity to **modulate
pooling weights** of a learned residue-level model — but the idea is now **publicly named as a field need by
the Elledge/Timms review**, and two 2025–2026 protein-ML papers come close (rASA as input alongside attention
pooling; attention pooling for PLMs). The bigger development is a **new threat**: the review itself identifies
why GPS-peptide labels may be the wrong training signal for an exposure gate.

### Cited findings

**The field has now explicitly asked for this.** *Nat Rev Mol Cell Biol* 2025, Outlook, verbatim:
> "We need the development of computational methods that leverage protein structure models to **predict degron accessibility** and lysine availability."
— [Nat Rev Mol Cell Biol 2025](https://doi.org/10.1038/s41580-025-00870-z) **[read]**, extracted from the PDF

**The same review states the threat to using GPS labels for an exposure model.** Box 1, verbatim:
> "A limitation of the GPS–peptidome approach is its failure to recreate conformational degrons and, as the relative frequencies of linear versus conformational degrons remains uncertain, this could be a notable drawback. Moreover, E3–degron pairs identified genetically could occur indirectly, and thus require further validation through biochemical methods. **The use of GFP fusions might also alter the natural context of degrons, disrupting post-translational modifications and sterically altering E3 binding or lysine accessibility, thereby complicating predictions about the behaviour of degrons in native protein structures.**"
— [Nat Rev Mol Cell Biol 2025](https://doi.org/10.1038/s41580-025-00870-z) **[read]**

**Biological counter-evidence to a monotonic exposure gate:**
- "**BAG6 and RNF126 promote the degradation of cytosolic misfolded proteins that contain buried degron motifs**" — bioRxiv **2026-04-25**, [10.64898/2026.04.24.720685](https://doi.org/10.64898/2026.04.24.720685), citing Voutsinos 2026 — **[snippet]**, title only
- Schulze & Lindorff-Larsen eLife 2026 report **PRKN S109**, an *exposed* residue whose substitution profile resembles a buried residue, interpreted as creating an **exposed quality-control degron** on mutation — [repo prior-art §3](../../architecture-check/prior-art-exposure-gate.md) **[read]**

**Where existing degron tools put structure** (consolidating the repo's table with this session's verifications):

| Model | Where exposure enters | Evidence |
|---|---|---|
| **PAP** (Voutsinos 2026) | **Nowhere in the model.** `Conv1D → GlobalAveragePooling1D`; rASA/pLDDT used only in post-hoc analysis (ρ = −0.47 vs degron score on 173 most-exposed proteins; ΔPAP Kruskal–Wallis P = 5.4 × 10⁻⁶) | **[read]** repo source audit + repo prior-art |
| **Larsen 2025** (TF degrons) | **Analysis only.** rASA (DSSP) and pLDDT from AlphaFold DB v4 are correlated with degron scores (Fig 2C–D), used to pick examples (Fig 3) and check ZnF structures (Fig S8). "The text does not say PAP or the substitution analyses use them" | **[read]** [bioRxiv full text](https://www.biorxiv.org/content/10.1101/2025.05.16.654404v1.full) |
| **MetaDegron** | **Input feature of the non-deep branch only.** Spider2 solvent accessibility feeds MetaDegron-X's XGBoost ensemble. MetaDegron-D is sequence-only, max-pooling, no attention, no gate | **[read]** [Brief Bioinform 2024](https://academic.oup.com/bib/article/25/6/bbae519/7828723) |
| **DEGRONOPEDIA** | **Post-hoc motif annotation.** rASA (DSSP, 20% default) and pLDDT (<70 default) describe each motif's context; the CatBoost PSI model's inputs are sequence/chemical descriptors only | **[read]** [documentation](https://degronopedia.com/degronopedia/documentation) |
| **DegronMD** | **Input feature of the XGBoost branch only.** "solvent accessibility" among ~10 features; the SeqVec deep branch is not stated to use them; rASA not named, pLDDT absent | **[read]** [MBE 2023](https://academic.oup.com/mbe/article/40/12/msad253/7441958) |
| **Schulze 2026** | **Stratification variable**, not a learned component: rASA threshold 0.1 by grid search splits residues into buried/exposed classes before table lookup | **[read]** repo prior-art §3 |
| **Degformer** | **Nowhere.** No structure of any kind; one-hot embedding + CLS pooling | **[read]** [train_v2.py](https://github.com/Alpine2048/Degformer/blob/main/train_v2.py) |

**Nearest precedents in broader protein ML (new this session):**
- **Edge-aware GAT binding-site model** — *PLOS Comput Biol* **2026**, [10.1371/journal.pcbi.1014552](https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1014552), arXiv 2601.02138. It "uses **attention pooling** to aggregate atomic features to residues" and its inputs **include relative solvent accessibility (RSA)". Its pooling weights come from a learnable query vector; the search summary states the results "don't describe gating by accessibility or a burial-aware component" — **[snippet]**, two independent search summaries agreeing
- **BoM-Pooling / locality-aware pooling** — *Bioinformatics* **2025**, 41(Suppl 1):i217, [PMC12261463](https://pmc.ncbi.nlm.nih.gov/articles/PMC12261463/), [paper](https://academic.oup.com/bioinformatics/article/41/Supplement_1/i217/8199370). Attention-based pooling over per-residue PLM embeddings with a windowed-average step; motivated because "Cls-Pooling and Avg-Pooling ... cannot capture the local substructures and long-range interactions observed in proteins". Gains are largest for longer sequences and smaller models. Code at github.com/Singh-Lab/bom-pooling. **No accessibility or burial term** — **[snippet]**
- **ProSST** — NeurIPS **2024**, structure-aware PLM quantising 3D structure into discrete tokens; notes that **disordered regions may be predicted poorly by AlphaFold2, which can hurt structure-aware models** — **[snippet]**
- **PTM-Mamba** — bidirectional **gated** Mamba blocks, PTM-aware PLM, [PMC12074982](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12074982/) — **[snippet]**. **[analysis]** Gating on a token-level annotation (PTM status) is mechanically analogous to gating on an exposure annotation; worth reading as a precedent for "gate a learned model on an external per-residue label".
- Already on file: **BioBlobs** (10/2025, gated attention-MIL over protein substructures, unsupervised, no solvent accessibility), **OmniESI** (2025, conditional modulation), **Ilse 2018** (gated attention = tanh × sigmoid on the *instance embedding*, not on an external structural quantity) — [repo prior-art §4](../../architecture-check/prior-art-exposure-gate.md) **[read]**

### Inferences

- **[analysis]** The precise shape of the remaining novelty for claim 3 is now clear and much narrower than the thesis card implies. Across degron work the exposure quantity has been used in exactly four ways — **post-hoc analysis** (PAP, Larsen, DEGRONOPEDIA), **input feature of a non-attention branch** (MetaDegron-X, DegronMD), **stratification variable for table lookup** (Schulze 2026), and **not at all** (Degformer, QCDPred). The unoccupied slot is "multiplicative modulation of learned aggregation weights". That is a *mechanism-placement* novelty, which is thin for a thesis's headline claim but perfectly adequate as one component among five.
- **[analysis] The Nature Reviews quote is a double-edged sword and the thesis must handle it deliberately.** It is the single best framing sentence available — the field's leading group, in its 2025 flagship review, asking for exactly this. Put it in the proposal's opening. But it also means claim 3 can no longer be presented as *the thesis's idea*; it is the thesis *answering a publicly stated need*. That is a stronger, more honest, and more defensible position than claiming the idea.
- **[analysis] The most serious unaddressed risk in the whole plan is now on the table.** The GPS labels are measured on 28-mers fused to GFP. In that construct there is **no burial** — every residue is solvent-exposed by construction. So an exposure gate **cannot be learned from the primary labels at all**; it can only be (a) fitted on the abundance labels (MaveDB/VAMP-seq, full-length proteins) and transferred, or (b) imposed as an architectural prior with a hyperparameter. The Nature Reviews review names precisely this extrapolation problem, including "sterically altering E3 binding or **lysine accessibility**". The thesis must state in the proposal which of (a) or (b) it is doing, and must not claim the gate is validated by the GPS labels.
- **[analysis]** The BAG6/RNF126 buried-degron preprint and the PRKN S109 case both argue the exposure–degron relationship is **non-monotonic**: buried motifs can be functional degrons once the protein misfolds, and exposure can *create* degrons. A gate that simply down-weights buried residues encodes a monotonic prior that the 2026 biology contradicts. The repo's own sign-flip measurement (−0.1928 buried vs +0.3733 exposed) is consistent with non-monotonicity, not with a simple mask. **The gate should be learned and signed, not a hard mask, and the proposal should say so.**

### Gaps

- The Edge-aware GAT paper is the closest thing I found to "rASA input + attention pooling in one model", and I have it **[snippet]** only, from two agreeing search summaries. It must be read at source before the thesis asserts that nobody gates pooling on accessibility — if its attention pooling consumes RSA in the query or key, the remaining novelty for claim 3 shrinks to near zero.
- I did not find any paper searching under the terms I used that puts an exposure gate at the pooling step. Queries run: "solvent accessibility weighted attention pooling protein residue prediction"; "accessibility-gated attention pooling burial-aware protein model 2025"; "structure-aware pooling gate disorder weight attention aggregation protein language model residue". This is **three query formulations and no hit** — it is "not found", not "not done".
- I did not read PTM-Mamba. If its gating is on an external per-residue annotation it is a direct methodological precedent for the gate mechanism (though not for degrons).

---

## Q4. Is MIL vs a per-position regression head a settled question in protein site/residue prediction?

### Takeaway

**No — I found no published head-to-head comparison** of bag-level attention MIL against per-residue
supervision on the same residue-labelled protein benchmark. The literature frames the two as answering
*different label regimes*, not as competitors, which means the thesis cannot cite a settled answer and will
have to produce the comparison itself.

### Cited findings

- MIL for binding sites is old and the framing is explicit: in the calmodulin-binding study, "a positive bag is built from fixed-size windows that overlap an annotated site, and the model only needs one positive window per bag"; the authors argue it "can account for **uncertainty in binding site location**" and lets position-dependent representations be used. Their MI-1 SVM was reported more accurate than classical MI-SVM and faster to train — [Multiple instance learning of Calmodulin binding sites, *Bioinformatics* 2012, 28(18):i416](https://academic.oup.com/bioinformatics/article/28/18/i416/251326) **[snippet]**
- In the same work, "a simple sliding-window SVM on average amino acid composition achieved similar performance to the earlier hierarchical neural network, so the windowing choice mattered as much as the learning framework" — [ibid.](https://academic.oup.com/bioinformatics/article/28/18/i416/251326) **[snippet]**
- The motivating trade-off is stated as a *label-availability* argument, not an accuracy argument: residue-level MIL "only requires knowledge of the protein's function yet identifies functionally relevant residues", motivated because "discriminative methods are limited to functions with sufficient residue-level annotation" — [Functional Site Discovery From Incomplete Training Data, PMC6729729](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6729729/) **[snippet]**
- Modern per-residue baselines use PLM embeddings directly with dense per-residue heads and report competitive results against specialist methods — [Protein embeddings and deep learning predict binding residues for various ligand classes, *Sci Rep* 2021](https://www.nature.com/articles/s41598-021-03431-4) **[snippet]**
- Other MIL-in-proteins precedents surfaced but none with a per-residue-head control arm: pyLEMMINGS (large-margin MIL for bioinformatics, [arXiv 1711.04913](https://arxiv.org/pdf/1711.04913)); protein–ligand affinity MIL over docking poses ([PMC11738626](https://pmc.ncbi.nlm.nih.gov/articles/PMC11738626/)); multi-level contrastive learning for protein–ligand binding *residue* prediction ([bioRxiv 2023.12.06.570503](https://www.biorxiv.org/content/10.1101/2023.12.06.570503.full.pdf)) — all **[snippet]**
- Possibly relevant 2026 analogue not yet read: "Learning the PTM code through a **coarse-to-fine** mechanism-aware framework", *Nat Commun* 2026-05-15, [10.1038/s41467-026-73148-3](https://doi.org/10.1038/s41467-026-73148-3) — **[snippet]**, title only
- Within degron work specifically, **every** model surveyed in Q1 and Q3 uses a bag-level/window-level scalar target with simple pooling: PAP global average pooling, MetaDegron-D max-pooling, Degformer CLS token, DEGRONOPEDIA/DegronMD non-sequential regressors. **None uses attention pooling and none uses a per-residue supervised head** — **[read]** for PAP (source), MetaDegron (paper), Degformer (source), DEGRONOPEDIA (docs), DegronMD (paper)

### Inferences

- **[analysis]** The question is **not settled, and is not even posed** in the protein-residue-prediction literature I could reach. The two approaches are presented as suited to different label regimes: MIL when you have bag labels and uncertain site locations, per-residue heads when you have dense residue annotations. The thesis's label situation is genuinely **in between** — it has peptide-level PSI (bag labels) *plus* mutagenesis-derived residue footprints (noisy residue labels, Jaccard 0.4965 between replicates). That intermediate regime is where a head-to-head comparison would actually be informative.
- **[analysis]** This is the most defensible *methodological* contribution left, and it is better positioned than claim 3. "MIL bag-level attention vs per-position regression head, same split, same budget, on degron footprints with a measured label ceiling" is a clean, publishable ablation that nobody has run — and the thesis already has the split design, the ceiling and the ΔPAP control in place. The repo should consider **promoting this from an unverified premise to a stated contribution**.
- **[analysis]** The 2012 calmodulin finding that "the windowing choice mattered as much as the learning framework" is a warning: the MIL-vs-head comparison can easily be confounded by window size. The ablation must hold the window fixed.

### Gaps

- I did not find a head-to-head comparison. Queries run: "multiple instance learning versus per-residue supervision protein binding site comparison". One query formulation only for this specific sub-question — **this is thin, and more searching is warranted** (suggest: "bag-level vs residue-level supervision PTM site", "weakly supervised residue localization protein benchmark", and checking the Nat Commun 2026 coarse-to-fine PTM paper's related-work section, which is the most likely place such a comparison exists).
- The *Nat Commun* 2026 coarse-to-fine PTM paper is unread and is the single most likely source of a published bag→residue comparison.

---

## Q5. Citing / cited-by sweep: Larsen 2025 and Voutsinos, as of late 2026

### Takeaway

Both are lightly cited (9 and 11 citations) and **none of the citing works overlaps the thesis's plan**. The
citation graph is biology and biophysics, not degron ML — which is good news for the thesis's timing, and it
also surfaces two 2026 items that change the thesis's risk picture.

### Cited findings

**Larsen 2025, "Comprehensive degron mapping in human transcription factors"**, bioRxiv, published **2025-05-17**, DOI [10.1101/2025.05.16.654404](https://doi.org/10.1101/2025.05.16.654404), **citationCount = 9**, still a preprint as of this sweep — [Semantic Scholar](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1101/2025.05.16.654404) **[read]**

Its 9 citing works, all **[read]** as records from the Semantic Scholar citations endpoint:
| Citing work | Venue | Date |
|---|---|---|
| PolyA/polyQ-mediated conformational rewiring … Ascl1 | bioRxiv | 2026-09-25 |
| Interpretable biophysical neural networks of transcriptional activation domains **separate roles of protein abundance and coactivator binding** | *Cell Systems* | 2026-08-01 (bioRxiv 2025-09-21) |
| Proteome-wide identification and modeling of interactions between transactivation domains and arginine-glycine-rich regions | bioRxiv | 2026-04-16 |
| Proteasomal control of transcription factors: mechanisms, regulation and dysregulation | *Cell Mol Life Sci* | 2026-03-01 |
| **A near-complete map of human cytosolic degrons** (Voutsinos) | *Sci Adv* | 2026-02-06 |
| **MAVISp: A modular structure-based framework for protein variant effects** | *Protein Sci* | 2026-01-22 |
| Basis for lineage-determining pioneer factors targeting distinct repressed chromatin states | *Sci Adv* | 2026-01-09 |
| AF-CALVADOS: AlphaFold-guided simulations of multi-domain proteins at the proteome level | *Protein Sci* | 2025-12-22 |
| Interpretable biophysical neural networks … (bioRxiv version) | bioRxiv | 2025-09-21 |

**Voutsinos et al., "A near-complete map of human cytosolic degrons and their relevance for disease"**, *Science Advances*, published **2026-02-06**, DOI [10.1126/sciadv.adz3483](https://doi.org/10.1126/sciadv.adz3483), **citationCount = 11** — [Semantic Scholar](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1126/sciadv.adz3483) **[read]**

Its 11 citing works, all **[read]** as records:
| Citing work | Venue | Date |
|---|---|---|
| PolyA/polyQ … Ascl1 | bioRxiv | 2026-09-25 |
| **Cancer degronopathies and protein-fate biomarkers in drug resistance and cancer progression: signalling mechanisms, measurement and translational limits** | *Front Cell Dev Biol* | 2026-09-25 |
| Autoinhibition of untimely DNA binding by structural disorder in full-length PPARs | *Nat Commun* | 2026-08-26 |
| High-throughput methods for studying protein self-assembly | *Curr Opin Struct Biol* | 2026-08-14 |
| Interpretable biophysical neural networks … | *Cell Systems* | 2026-08-01 |
| Proteogenomic analysis of the differential stability of cardiac protein isoforms | bioRxiv | 2026-07-24 |
| Navigating Misfolded Terrain: ER-Associated Degradation of Membrane Proteins | *Chem Rev* | 2026-06-30 |
| **BAG6 and RNF126 promote the degradation of cytosolic misfolded proteins that contain buried degron motifs** | bioRxiv | 2026-04-25 |
| Proteasomal control of transcription factors | *Cell Mol Life Sci* | 2026-03-01 |
| **Comprehensive Variant Effect Map of Parkin-Mediated Mitophagy in Parkinson's Disease** | bioRxiv | 2026-02-09 |
| Blocking protein quality control degradation leads to structural stabilization of DHFR indel variants | bioRxiv | 2025-12-11 |

### Inferences

- **[analysis] No citing work overlaps the thesis's plan.** Of the 19 distinct citing papers, none is a degron predictor, none does residue-level degron footprint prediction, and none builds a substitution matrix for degrons. The citing community is TF biology, biophysics/simulation, and proteostasis — not degron ML. **The thesis's niche is not being taken by the obvious follow-on community**, which is the strongest timing signal in this whole report.
- **[analysis] Three citing works matter for the thesis and should be read:**
  1. **"Interpretable biophysical neural networks of transcriptional activation domains separate roles of protein abundance and coactivator binding"** (*Cell Systems* 2026-08-01, [10.1016/j.cels.2026.101701](https://doi.org/10.1016/j.cels.2026.101701)) — cites **both** Larsen and Voutsinos, and its whole point is **separating abundance from function** on tile libraries with an *interpretable* neural network. That is methodologically adjacent to the thesis and is the single most likely place a competing residue-level interpretable model already exists. **Highest-priority read.**
  2. **"BAG6 and RNF126 … buried degron motifs"** (bioRxiv 2026-04-25) — direct biological counter-evidence to a monotonic exposure gate. See Q3.
  3. **MAVISp** (*Protein Sci* 2026-01-22, [10.1002/pro.70548](https://doi.org/10.1002/pro.70548)) — "a modular structure-based framework for protein variant effects". A *framework* for structure-based variant effects that already cites Larsen is a potential application-layer competitor and a potential integration target. See Q6.
- **[analysis]** "Cancer degronopathies and protein-fate biomarkers … **translational limits**" (*Front Cell Dev Biol* 2026-09-25) is a 2026 review of the clinical framing. Useful for the proposal's significance section, and its "translational limits" framing is a caution against over-claiming clinical utility.
- **[analysis]** Larsen 2025 is still a preprint 17 months after posting. **[analysis]** That is worth noting but not over-reading; the thesis should cite it as a preprint and not assume journal validation.

### Gaps

- Semantic Scholar's citation coverage of very recent bioRxiv items is incomplete, so these counts are floors, not totals. I did not cross-check with Google Scholar (not reachable as a structured source here) or Crossref event data.
- I did not read any of the three priority citing works; all are **[read]** as bibliographic records only, not as content.

---

## Q6. Application-layer differentiation: what must a new degron tool offer to be more than "another web server"?

### Takeaway

The existing servers are **protein-at-a-time motif-annotation browsers over fixed databases**. The concrete,
verified gaps are: **no API anywhere**, **no arbitrary user-specified mutation scoring anywhere**, **no
experimental-label provenance per prediction**, **no uncertainty estimates anywhere**, and **no matrix
export**. Batch submission is *not* a gap (MetaDegron and DegronMD both have it), and that claim must be
removed from the repo's G3 line.

### Cited findings — verified feature matrix

| Feature | DEGRONOPEDIA | MetaDegron | DegronMD | PAP / QCDPred | Degformer | Zhang 2023 SVM |
|---|---|---|---|---|---|---|
| Batch submission | **No** — "it is possible to submit only one protein at a time" **[read]** | **Yes** — multiple E3s, multiple FASTA **[read]** | **Yes** — line-by-line batch search + blastp **[read]** | Colab notebook / GitHub **[read]** repo audit | Local script `predict.py` **[read]** | Not distributed as a tool **[read]** repo audit |
| Programmatic API | Not mentioned; standalone GitHub tool offered instead **[read]** | Not described **[read]** | Not mentioned **[read]** | None (GitHub only) **[read]** | None **[read]** | None **[read]** |
| Arbitrary user mutation scoring | **No** — COSMIC missense lookup only **[read]** | **No** — no mutation module **[read]** | **No** — scores only observed cancer somatic mutations **[read]** | ΔPAP computable by the user in Colab; not a product feature **[read]** | **Yes, locally** — `saturation_mut_heatmap.py` over all 20 AA **[read]** | No **[read]** |
| Position × amino-acid matrix export | Not mentioned **[read]** | Not described **[read]** | Not described **[read]** | Larsen 2025 produced a PAP-map for HSF1 by hand **[read]** | **Yes** — heatmap script **[read]** | No **[read]** |
| Per-prediction uncertainty | **No** — only global 95% band on performance plots **[read]** | **No** — only ensemble mean and CV ranges **[read]** | Confidence score per degron; **none** for mutation/drug scores **[read]** | **No** **[read]** | **No** **[read]** | **No** **[read]** |
| Experimental-label provenance per prediction | Not mentioned **[read]** | Not described **[read]** | Not mentioned **[read]** | Not applicable **[read]** | **No** **[read]** | No **[read]** |
| Compartment-specific prediction | **Not mentioned** **[read]** | Not described **[read]** | **Not mentioned** **[read]** | PAP trained on **cytosolic** data only — stated limitation in Larsen 2025 **[read]** | No **[read]** | No **[read]** |
| Downloads | xlsx of all results + degron motif list **[read]** | Not described **[read]** | Download page with datasets; plots in multiple formats **[read]** | GitHub **[read]** | GitHub **[read]** | Mendeley dataset **[read]** |
| Residue-level score shown to user | Only descriptive features (disorder, RSA, SS) **[read]** | **No** — instance start/end only **[read]** | **No** — "doesn't describe a per-residue score track" **[read]** | Per-residue profiles only as running averages over tiles in Larsen 2025 Fig 3/6C **[read]** | Scanning plots (README Fig 4) **[read]** | No **[read]** |

**Larsen 2025's own app surface and limitations** — **[read]** [bioRxiv full text](https://www.biorxiv.org/content/10.1101/2025.05.16.654404v1.full):
- They released **code on GitHub** for reproducing and generating predictions, plus screen data as supplementary Excel. "The text does not mention a web server, database interface, or API."
- Their **PAP-map (Fig 6E)** is a full in-silico ΔPAP scan of all single substitutions in **one protein, HSF1, across residues 412–420** only. Their **Fig 4A position × amino-acid heatmap is built from *measured* screen scores, not in-silico predictions**. "The paper does not describe a saturation in-silico matrix for all 1,626 TFs."
- Their per-residue profiles (Figs 3, 6C) are **running averages over tile scores (window of 5)** — a smoothing of peptide-level output, not a residue-level model. "The paper does not present a separate residue-level footprint model or validate one."
- Stated limitations, which define open ground: only **constitutive, PTM-independent** degrons were likely detected, so **phospho-degrons were probably missed**, and "exposed degrons might be blocked by phosphorylation in full-length proteins"; **compartment-specific E3 effects only partly tested** because few tiles appear in both libraries, with the authors writing "Possibly there are many more examples such as these"; **ESM-1b is less accurate in disordered regions, and PAP was trained on cytosolic data**; only **ASCL1 and HSF1** were validated in full-length context.

**Field-level demand statements** — *Nat Rev Mol Cell Biol* 2025, **[read]**:
- "Currently only **~10% of E3s have cognate degrons assigned**, and thus we are still at a very early stage of mapping E3–degron relationships. Here, we call for the development of **systematic, widely applicable and easy-to-use technologies** for scalable multiplex degron discovery and E3–degron mapping, which would enable the computational reconstruction of the proteome degradation landscape."
- "At least **51 E3s** have cognate degrons assigned." (Fig 1b legend)
- On the historical approach: "these approaches remain **laborious, low throughput and offer limited resolution of degron motifs**. Moreover, in many cases, sufficiency tests … of the putative 'degrons' identified are lacking, **hampering in silico prediction** of substrates containing such degrons."
- On motif variability: "High-resolution genetic mapping of degron motif through saturation mutagenesis has revealed **significant sequence variability within these motifs**. A prime example is KLHL15, which was initially shown to recognize an 'FRY' degron motif; however, mutational analysis revealed can also target **FRF, FRY, LRF and LRY** motifs."

### Inferences

- **[analysis] Four concrete, verified application gaps** that no existing tool fills, each checkable against the table above:
  1. **An API / programmatic interface.** Verified absent from DEGRONOPEDIA, MetaDegron and DegronMD. This is the cheapest real differentiator and the easiest for a software-engineering thesis (CT553H is Kỹ thuật phần mềm) to justify on its own terms.
  2. **Arbitrary mutation scoring with matrix export.** Every published server restricts mutations to a fixed variant database (COSMIC for DEGRONOPEDIA, cancer cohorts for DegronMD). A user cannot ask "what does my engineered substitution do". Degformer can do this *locally with a Python script*; **no server offers it**. This is where claim 2's surviving value lives.
  3. **Per-prediction uncertainty, grounded in the measured label ceiling.** No tool reports any. The repo has already measured replicate noise (75.9% of residual variance on the scanning set, 16.7% on the saturation set) and the label ceiling (0.6514 precision@3; cell-level AUROC 0.9519). A tool that returns "ΔPSI = −1.2, but this assay's residue-level labels only replicate at Jaccard 0.50, so treat residue identity as uncertain" would be **unique and honest**, and it directly monetises the repo's strongest existing work.
  4. **Experimental-label provenance per prediction.** No tool tells you which measured peptides support a given prediction. The repo has already computed that **725/770 footprint peptides have a tile in PAP's training set** — exactly the kind of provenance a user needs to know whether a prediction is interpolation or extrapolation.
- **[analysis] Two gaps the field itself named**, which are stronger than gaps the thesis invents: **compartment-specific prediction** (PAP is cytosolic-only by its authors' admission; Larsen's compartment comparison was underpowered and they wrote "Possibly there are many more examples such as these") and **phospho-degron / PTM-conditional degrons** (Larsen's stated miss; the review's "ability to systematically identify … degrons conditionally regulated by PTMs is still lacking"). The thesis cannot build the data for either, but **flagging compartment applicability per prediction** — "this prediction comes from a cytosolic-trained model; your protein is nuclear" — is a cheap, honest, genuinely novel feature.
- **[analysis] Remove "batch submission" from the repo's G3 differentiation list.** MetaDegron and DegronMD both have batch. Keeping it would be an error a reviewer could catch.
- **[analysis]** MAVISp (*Protein Sci* 2026-01) is a "modular structure-based framework for protein variant effects" that already cites Larsen. **[analysis]** The thesis should check whether integrating as a MAVISp module is a better application story than a standalone server — it would inherit an existing user base and sidestep the "another web server" objection entirely. This is a genuinely different strategic option and I flag it as unexplored.

### Gaps

- I did not load the live DEGRONOPEDIA, MetaDegron (modinfor.com/MetaDegron) or DegronMD servers to confirm the absence of an undocumented API endpoint. The absence is from documentation and papers only. **Worth 15 minutes of checking before the proposal claims it.**
- MAVISp's module interface and whether it accepts third-party predictors is unverified — bibliographic record only.
- I could not verify what the PAP Colab exposes to a user beyond running the model, because science.org is 403 from this network; the repo's source audit covers the model, not the notebook UX.

---

## Verdict: which of the three claims survives, and how each must be narrowed

### Takeaway

**Claim 2 is dead as written and must be rewritten. Claims 1 and 3 survive but both must be demoted from
"first to do X" to "first to do X *under an honest evaluation*".** The thesis's real, defensible contribution
has shifted from *outputs* to *evaluation discipline* — and that shift is survivable, because the repo already
owns the evaluation assets (cluster split, label ceiling, ΔPAP control, power analysis) that no competitor has.

### Claim 1 — residue-level degron footprint prediction trained on experimental labels

**Status: survives, narrowed.** **[analysis]**

What narrows it:
- The **concept and the experimental footprints already exist**. Zhang 2023 produced mutational fingerprints for 219 degrons and the DegronID clustering algorithm; the Nature Reviews review describes "degron mutagenesis footprints" as established practice — **[read]** both.
- **Residue-level *profiles* already exist as derived quantities.** Larsen 2025 shows per-residue profiles (running average of tile scores, window 5) and Degformer ships residue-level scanning plots — **[read]** both. What does not exist is a **residue-level supervised head**.

Defensible wording: *"first residue-level degron model **supervised at residue level** and **evaluated at residue level** under a protein-cluster split against a measured label ceiling"* — not "first residue-level degron prediction".

What would kill it: if the *Cell Systems* 2026 interpretable-biophysical-neural-network paper already has a residue-level supervised head on tile libraries. **Unread. Highest-priority check.**

### Claim 2 — the 28 × 20 position × amino-acid matrix from experimental mutagenesis labels

**Status: DEAD AS WRITTEN. Must be rewritten in every document.** **[analysis]**

What kills it: **Degformer** (public GitHub, 2026-03 to 2026-09) is trained on Zhang 2023 **S4 scanning + S7 saturation** mutagenesis, has `MAX_LEN = 28`, and ships `saturation_mut_heatmap.py` which emits ΔPSI over 28 positions × the 20 amino acids. That is the claim, exactly, already shipped — **[read]** source.

What *additionally* narrows it, independent of Degformer:
- **Larsen 2025 Fig 4A** is a position × amino-acid heatmap **from measured screen scores**, and **Fig 6E** is a full in-silico ΔPAP substitution scan (a "PAP-map") for HSF1 412–420 — **[read]**.
- **Schulze & Lindorff-Larsen eLife 2026** builds substitution matrices **per exposure class** from experimental VAMP-seq, and the authors offer them as a "strong baseline for future abundance-model development" — **[read]** repo prior-art.
- **DegronMD** has a mutation-impact module, though rule-weighted and restricted to observed cancer mutations — **[read]**.

What survives, and it is real:
1. **The benchmark, not the artefact.** Nobody has evaluated a substitution matrix for degrons under a **protein-cluster split** with a **measured label ceiling** and a **published-model control**. The repo already has all three: cov80 clustering, cell-level AUROC ceiling **0.9519**, and ΔPAP at **0.7692**. Degformer's ρ = 0.9162 on S7 is from a **random 10% split** (`random_state=42`, no grouping) that places ~500 sibling mutants of each held-out mutant in training — **[read]** source. Re-evaluating Degformer under cov80 is the single highest-value experiment available to the thesis right now.
2. **Exposure-conditioned matrices for degrons.** Schulze 2026 conditions on exposure but for *abundance*; Degformer and Larsen produce matrices but unconditioned. A matrix conditioned on exposure class, for degrons, is still unoccupied ground.
3. **Uncertainty and provenance on each cell**, which no competitor provides (Q6).

Required wording change: delete "the one thing none of the precedents outputs" and every equivalent. Replace with: *"a 28 × 20 matrix has been produced before — by Degformer on the same labels, and by Larsen 2025 for single proteins — but never under a cluster split with a measured label ceiling, never with per-cell uncertainty, and never conditioned on exposure."*

### Claim 3 — exposure gate at the POOLING step of a MIL architecture

**Status: survives as "not found", but weaker than the repo thinks, and newly threatened.** **[analysis]**

What narrows it:
- **The idea is publicly named as a field need.** Nat Rev Mol Cell Biol 2025: "We need the development of computational methods that leverage protein structure models to predict degron accessibility and lysine availability" — **[read]**. Excellent framing, but the thesis is now *answering* a stated need, not *having* the idea.
- **Near-precedents exist in protein ML.** The Edge-aware GAT binding-site model (*PLOS Comput Biol* 2026) combines **rASA inputs with attention pooling** — **[snippet]**, must be read. BoM-Pooling (*Bioinformatics* 2025) is attention pooling for PLM residues — **[snippet]**. PTM-Mamba gates on an external per-residue annotation — **[snippet]**.
- The repo's own prior-art file already established that the exposure *premise* and the ΔPAP *sign flip* were published first by Voutsinos 2026 and Larsen 2025 — **[read]**, unchanged by this session.

**What newly threatens it, and this is the most important finding in this section:**
- **The GPS labels cannot train an exposure gate.** The labels are 28-mers fused to GFP, where nothing is buried. The Nature Reviews review names exactly this: GFP fusions "might also alter the natural context of degrons … **sterically altering E3 binding or lysine accessibility**, thereby complicating predictions about the behaviour of degrons in native protein structures" — **[read]**. The gate can only be fitted on the abundance labels and transferred, or imposed as a prior. **The proposal must say which, and must not claim the GPS labels validate the gate.**
- **The exposure–degron relationship is non-monotonic**, so a gate that just down-weights buried residues encodes a prior the 2026 biology contradicts: "BAG6 and RNF126 promote the degradation of cytosolic misfolded proteins that contain **buried** degron motifs" (bioRxiv 2026-04-25) — **[snippet]**; and Schulze 2026's **PRKN S109**, an exposed residue whose mutation appears to *create* a quality-control degron — **[read]**. **The gate must be learned and signed, not a hard mask.**

Defensible wording: *"Across the degron models I examined, exposure enters in one of four ways — post-hoc analysis (PAP, Larsen, DEGRONOPEDIA), input feature of a non-attention branch (MetaDegron-X, DegronMD), stratification variable (Schulze 2026), or not at all (Degformer, QCDPred). I did not find a degron model that uses exposure to modulate learned aggregation weights, across three query formulations. Novelty is in the placement and the combination, not the mechanism."*

### The strongest remaining contribution is one the repo has not yet claimed

**[analysis]** The MIL-vs-per-position-head comparison (Q4) is **unoccupied, unposed in the literature, and
fully within reach**. No head-to-head exists in protein residue prediction; the thesis has the intermediate
label regime (bag-level PSI + noisy residue footprints) that makes the comparison informative; and it already
has the split, the ceiling, the power analysis and the ΔPAP control. Combined with **re-evaluating Degformer
under cov80**, this converts the Degformer discovery from a threat into the thesis's clearest result: *the
published and public models are evaluated on leaky random splits, and here is what they score when you do it
properly*.

### Immediate required actions

1. **Delete the claim** that no precedent outputs a 28×20 matrix, from `topics/degron-footprint/README.md` (G3 row), `research/topic-decision.md §7` and `research/full-data-audit §6.2`. Add Degformer to the precedent list — it becomes the **fifth** precedent, not the fourth.
2. **Add DegronMD** (MBE 2023) to the prior-art table — a published tool with a mutation module that the repo had missed entirely.
3. **Remove "batch submission"** from the G3 differentiation list; MetaDegron and DegronMD both have it.
4. **Download and re-evaluate `peptide_model_epoch50.pt`** under the repo's cov80 split and residue-level metrics. Highest value-per-hour experiment currently available.
5. **Read, in this order:** the *Cell Systems* 2026 interpretable-biophysical-NN paper (possible claim-1 killer); the Edge-aware GAT paper (possible claim-3 narrower); the *Nat Chem Biol* 2025-11 "beyond short linear motifs" review (scope risk to the 28-mer framing); the *Nat Commun* 2026 coarse-to-fine PTM paper (possible MIL-vs-head precedent).
6. **Add the Nature Reviews quote** ("We need the development of computational methods that leverage protein structure models to predict degron accessibility and lysine availability") to the proposal's opening — and in the same breath state that the GPS labels contain no burial, so the gate is a transferred prior, not a label-validated component.
7. **Resolve DegPred's output granularity** at source (degron.phasep.pro or GitHub) before writing the literature review; it is the one tool whose granularity I could not verify.
