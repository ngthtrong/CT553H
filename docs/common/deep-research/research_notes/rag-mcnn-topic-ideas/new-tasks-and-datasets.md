# New prediction tasks and public benchmarks for a "PLM + mCNN + bolt-on module" thesis (Ou / Ho group, 2023–2026)

Scope note: every row below was checked against the group's own publication list in
`docs/common/advisor/Prof Ho/research.md` and `docs/common/advisor/Prof Ou/research.md`, and against the
four topic proposals already in `docs/common/deep-research/reports/bioinformatics-topic-survey.md`
(label-independent retrieval for DNA/RNA sites, generative augmentation for efflux, ATP/FAD/NAD multitask,
ATP explanation/conformal). Those four are treated as **already proposed** and are excluded from the picks.

**Tasks the group has already published on (VERIFIED from the two research.md lists, so do not re-use):**
ATP sites (ATP_mCNN, RTK_RAG, CFTR_TL), FAD (msCNN-PLM-FAD), NAD+ (NAD_MCNN), Ca²⁺ (CaBind_MCNN),
metal-binding residues with RAG (EAAI 2026), protein–DNA sites (JMB 2024 + RAG-msCNN 2026),
**protein–peptide interaction sites (JMGM 2024 — already done, exclude)**, ion channels/transporters
(DeepPLM_mCNN, MFPS_CNN), secondary active transporters, amino-acid/peptide transporters (MCNN-AAPT),
sodium (NA_mCNN), glucose (mCNN-glucose), vesicular (VesiMCNN), mitochondrial carriers (MCNN_MC),
efflux (mCNN-GenEfflux), electron transport chain (mCNN-ETC), SNARE, primary active transport (DEEPTRANS),
cytokine **receptor** proteins (DeepCR), IL-6 (RAG_MCNNIL6), IL-13 (DeepEpiIL13), IFN-γ (IFNg_DeepKG),
neoantigens (DeepNeoAG, NeoGen-BC), sirtuins (SirtSAGE), plus DNA-level work (BERT-Promoter, enhancers, 6mA).

---

## Objective: table of candidate tasks not yet done by the group

### Takeaway
Three families of task are both untouched by the group and backed by clean public benchmarks: (a) **single-ligand
binding residues other than ATP/FAD/NAD/Ca/metal/DNA — heme, GTP, and the "unseen ligand" setting** (LABind /
BioLiP2, with a real temporal split and Zenodo data); (b) **the remaining cytokine-inducing epitope panel — IL-4,
IL-10, TNF-α** (tiny datasets, exact clones of the group's IL-6/IL-13/IFN-γ template); and (c) **cross-species PTM
sites, above all lysine lactylation**, where a published mini-review documents a collapse from AUC 0.97 to 0.56
when models move off their home dataset — a ready-made, citable failure mode to fix.

### Cited Findings — candidate table

Columns: dataset/size/positives · split + identity cutoff · current SOTA · retrieval likely to help? (leakage risk) ·
compute fit (Colab Pro + Kaggle) · biology knowledge · fit with group style (one task / ProtT5 + mCNN + module).
"V" = VERIFIED from the cited source; "I" = INFERRED by me.

| # | Task | Benchmark + URL | Size / positive rate | Split & identity cutoff | SOTA (source) | Retrieval helps? / leakage | Compute | Biology | Group-style fit |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **Heme (HEM) binding residues** | LABind DS1/DS2, data on Zenodo `10.5281/zenodo.15875006`; structures from [BioLiP2](https://academic.oup.com/nar/article/52/D1/D404/7233921) — [LABind, Nat Commun 2025](https://www.nature.com/articles/s41467-025-62899-0) | DS1 = 2,626 chains over 19 ligands (V); per-residue positive rate not stated per ligand (gap) | CD-HIT **30%** for DS1/DS2; **temporal** split by PDB release date before/after **Jan 2017** (V) | MCC **0.730** LABind (DS2); DELIA 0.596, GraphBind 0.633 (V, [PMC12365077](https://pmc.ncbi.nlm.nih.gov/articles/PMC12365077)) | Yes — heme-binding motifs are strongly homologous (I); leakage already controlled by 30% + date split | Low: few thousand chains, ProtT5 once, store fp16 per-residue (I) | Medium (what a cofactor/porphyrin is) | **Very high** — exactly "one ligand, one paper" |
| 2 | **GTP binding residues** | same LABind DS1 / LigBind lineage — [LABind](https://www.nature.com/articles/s41467-025-62899-0) | part of the 2,626-chain DS1 (V) | CD-HIT 30% + pre/post-2017 temporal (V) | MCC **0.667** LABind vs **0.554** LigBind (V) | Yes (P-loop/Walker-like motifs) (I); same control as #1 | Low | Medium | Very high; natural sequel to ATP (nucleotide cousin) |
| 3 | **Unseen-ligand generalisation (ligand-aware binding sites)** | LABind **DS3** — [LABind](https://www.nature.com/articles/s41467-025-62899-0) | 21,651 train proteins / 3,651 ligands; **1,049 test proteins / 474 unseen ligands** (V) | MMseqs2 **<30% identity, coverage >0.3**; train = released before **1 Jan 2021**, test later (V) | ATP MCC 0.663 on DS3 (V); all SOTA here is **structure-based** | Retrieval is the natural sequence-only substitute for ligand geometry (I); honest by construction | Medium-high (21k proteins ≈ the largest embedding job here; ~6 GB-class storage, see survey §4) | Medium-high | High novelty, medium fit (one model, many ligands — against the group's one-task-per-paper habit) |
| 4 | **Zn²⁺ binding residues** | LABind DS2 | 6 ligands incl. Zn²⁺ (V) | as #1 | MCC **0.837** (V) | Yes (I) | Low | Low-medium | Medium — **overlaps** the group's 2026 metal-binding RAG paper |
| 5 | **Lysine lactylation (Kla) sites, cross-species** | HybridKla set 23,984 pos / 23,984 neg over **14 species**; DeepKla 1,720/1,767; Auto-Kla 1,912/19,562; ABFF-Kla 9,560/9,560 — [mini-review, PMC13256538](https://pmc.ncbi.nlm.nih.gov/articles/PMC13256538/); [CLEAR-Lactyl 16,604 human sites](https://www.biorxiv.org/content/10.64898/2026.07.28.741267v1) | see left; early sets ~**1:20** imbalance (V) | CD-HIT **30%** (DeepKla), **70%** (Auto-Kla, ABFF-Kla), peptide-level only (FSL-Kla, HybridKla) (V) | PCBert-Kla AUC **0.9728** / MCC 0.8999; DeepKla 0.9722/0.8671; HybridKla (ESM2+LSTM) AUC 0.8460 (V) | **Strongest case in this table**: published cross-species collapse — DeepKla AUC → **0.5563**, Auto-Kla → **0.6563** on the multi-species benchmark (V) | Very low (31–51 aa windows, ~50k peptides) | Low-medium | High — PTM sites are residue-level windows, i.e. mCNN's home turf |
| 6 | **Other PTM sites (succinylation, glycosylation, ubiquitination, phosphorylation)** | [dbPTM 2025](https://biomics.lab.nycu.edu.tw/dbPTM/) — [NAR 2025 D377–D386](https://academic.oup.com/nar/advance-article-pdf/doi/10.1093/nar/gkae1005/60586513/gkae1005.pdf) | **>2.79 M PTM sites, 2.243 M experimentally validated**, from 48 databases + >80,000 articles (V) | dbPTM is a database, **not** a split benchmark — each sub-task has its own ad-hoc set (V) | task-specific; no single leaderboard (V) | Likely yes; leakage risk **high** because peptide windows recur across databases (I) | Low per task | Low-medium | High fit, but you must build the split yourself |
| 7 | **IL-4-inducing epitopes** | [IL4pred](https://pmc.ncbi.nlm.nih.gov/articles/PMC3893860/); [IL4Pred2 (2025)](https://www.biorxiv.org/content/10.1101/2025.04.23.650150.full.pdf); source IEDB | IL4pred: **904 inducing / 742 non-inducing** MHC-II peptides; IL4Pred2: 845 human + 560 mouse positives with equal-size negatives (V) | peptide-level; identity handling not clearly reported (gap) | Meta-IL4 ensemble published 2023 ([Methods](https://www.sciencedirect.com/science/article/abs/pii/S1046202323001135)); no PLM+mCNN entry found (I) | Retrieval already shown useful by the group on IL-6; small corpus limits the neighbour pool (I) | Trivial (<2,000 peptides) | Low | **Highest** — literally the next cytokine in the group's own series |
| 8 | **TNF-α-inducing epitopes** | [TNFepitope](https://www.sciencedirect.com/science/article/abs/pii/S0010482523003943); standalone + data on [Zenodo](https://zenodo.org/records/20150935) | **3,177 of 3,635** IEDB TNF-α-inducing peptides are human/mouse (V) | separate human and mouse independent test sets (V) | AUROC **0.83** (human) / **0.77** (mouse) (V) | Yes; the modest SOTA leaves real head-room, unlike saturated tasks (I) | Trivial | Low | Highest, same reason as #7 |
| 9 | **IL-10-inducing epitopes** | [IL-10Pred](https://webs.iiitd.edu.in/raghava/il10pred/algo.php); [PMC5314457](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5314457/) | **394 positives / 848 negatives** (MHC-II binders) (V) | peptide-level (V) | IL-10Pred (first method for the task) (V) | Too few sequences for a useful retrieval database (I) | Trivial | Low | High fit but **dataset probably too small** for a thesis-grade claim |
| 10 | **AMP potency / spectrum / safety under homology control** | [AMPBench-MT (arXiv 2607.25518)](https://arxiv.org/pdf/2607.25518); sources DBAASP + APD | sizes not extractable from the PDF (gap) | **homology-controlled**: clustering at ~30% identity, each cluster in exactly one partition (V) | baselines in paper, numbers not extractable (gap) | Retrieval risky: [negative-set bias](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9487607/) and k-mer leakage are documented for AMP benchmarks (V) | Trivial | Low | Medium — multi-task, so less "one task per paper" |
| 11 | **Anticancer peptides (ACP)** | ACP740 (**374 ACP / 366 non-ACP**), ACPmain, ACPAlter, AntiCP2.0 main/alternate — [PLMACPred, Sci Rep 2024](https://www.nature.com/articles/s41598-024-67433-8) | see left (V) | legacy splits; cross-dataset overlap reported in the field (V) | **Metrics already saturated**: ACP-ESM 88.51% acc on ACP740; PLMACPred up to 94.76 / 96.39 / **98.65%** accuracy (V) | Leakage is the known problem here ("many test samples already exist in training sets") (V) | Trivial | Low | Medium — hard to beat, easy to criticise |
| 12 | **Hemolysis / peptide toxicity screening** | HemoPI line; reliability critique in [arXiv 2012.06470](https://arxiv.org/pdf/2012.06470); safety tasks also inside AMPBench-MT (V) | not verified (gap) | critique paper exists precisely because standard splits are unreliable (V) | Retrieval plausible; leakage high (near-duplicate designed peptides) (I) | Trivial | Low | Medium |
| 13 | **Intrinsic disorder + disordered binding regions** | [CAID 3 (PMC12750029)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12750029/); DisProt | **43 methods on 646 DisProt proteins**; CAID3 ran in 2025 and assessed 24 new methods (V) | **blind community assessment** on newly curated DisProt entries = honest held-out by design (V) | Best Fmax **0.483** full set, **0.792** after filtering structured regions; +31% AP on linkers and +15% on disorder vs CAID2; **top methods are pLM-based** (V); new binding sub-challenge "remains challenging" (V) | Retrieval dubious — disorder is poorly conserved (I) | Low-medium | Medium | Medium — CAID is a known yardstick but far from the group's ligand/transporter identity |
| 14 | **Bacterial secreted effectors (T1/T3/T4/T6SE) — family classification** | [PLM-T3SE](https://onlinelibrary.wiley.com/doi/10.1002/jcb.30642); [PLM-effector, Brief Bioinform 2026](https://academic.oup.com/bib/article/27/2/bbag143/8607031); [MoCETSE, PLOS CB](https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1013397); review: [challenges in T3SE prediction](https://royalsocietypublishing.org/rsob/article/16/8/250485/483063/Challenges-and-opportunities-in-type-III-secretion) | not verified per set (gap) | not verified (gap) | PLM-T3SE accuracy **98.1%** (1.8–42.4 pp above prior tools); PLM-effector macro-F1 **0.9899** for T3SE (V) | Homology is the classical signal here, so retrieval should help — but metrics are already ~0.99, leaving only honest-split work (I) | Low-medium | Medium | High structurally (same shape as the transporter-family papers) but **crowded in 2024–2026** |
| 15 | **ARG class / resistance-mechanism classification** | [CARD 2023](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9825576/); [Trans-ARG (ESM-2)](https://dl.acm.org/doi/10.1145/3703412.3703425); [ProtAlign-ARG, Sci Rep 2025](https://www.nature.com/articles/s41598-025-14545-4); [PLM-based ARG + phenotype, 2025](https://pubmed.ncbi.nlm.nih.gov/40988849/) | not verified (gap) | not verified; CARD supports ML workflows (V) | Trans-ARG sens **0.8879** / spec **0.9211** / AUC **0.9672** vs CARD AUC **0.7382**; ProtAlign-ARG F1 **0.83** vs alignment-only 0.71 (V) | Retrieval = exactly what alignment-based ARG tools already do, so a RAG module is well motivated **and** the leakage question is live (I) | Low-medium | Medium | High — multi-class family task, same shape as transporter super-families |
| 16 | **Phage protein function / virion protein classification; phage lifestyle** | [PhageScope, NAR 2024](https://academic.oup.com/nar/article/52/D1/D756/7334092); [ProteoKnight (arXiv 2508.07345)](https://arxiv.org/pdf/2508.07345); [ProkBERT PhaStyle](https://academic.oup.com/bioinformaticsadvances/article/5/1/vbaf188/8317429) | PhageScope: **553,688 virulent / 320,030 temperate** phages; proteins in **10 functional classes** (lysis, integration, replication, tRNA, regulation, packaging, assembly, infection, immune, hypothetical) (V) | virion-protein benchmark built from RefSeq viral proteins up to **Dec 2022** (V) | ProkBERT PhaStyle benchmarked vs BACPHLIP/DeePhage/PhaTYP (V); exact numbers not extracted (gap) | Retrieval plausible; large hypothetical-protein fraction is a label-noise risk (I) | Medium (big corpus; subsample) | Medium | Medium — lifestyle prediction is a *nucleotide* LM task, only the protein-function part fits mCNN |
| 17 | **MHC class II binding (peptide–MHC)** | [IEDB weekly automated benchmark](https://tools.iedb.org/auto_bench/mhcii/weekly/); [platform paper, Bioinformatics 2018](https://academic.oup.com/bioinformatics/article/34/9/1522/4769495) | weekly datasets; e.g. an entry of **n = 1,372** on 30 Aug 2024 (V) | **prospective**: tools are evaluated on data newly entered into IEDB *before it is public* (V) | NetMHCIIpan **4.1 BA** is the top-ranked binding predictor (V) | Allele-aware retrieval plausible; this is the most honest evaluation available (V) | Low | Medium-high (alleles, HLA nomenclature) | Low-medium — beating NetMHCIIpan is a hard target for a first paper (I) |

### Inferences
- The cheapest *and* least duplicated slot in the group's own taxonomy is **one more single-ligand residue task (heme or GTP)**, because LABind/BioLiP2 hands over 30%-identity-filtered data *plus* a date-based temporal split, and because every published competitor on those ligands is structure-based — a sequence-only ProtT5 + mCNN (+ retrieval) entry therefore has a defensible reason to exist rather than being a re-run.
- The cytokine-epitope series (IL-6 → IL-13 → IFN-γ) has an obvious next element (IL-4, TNF-α). That maximises advisor fit and minimises risk, but the novelty is procedural, not conceptual, so the thesis contribution has to come from the evaluation (honest split + retrieval ablation on α and k), not from the task choice.
- Tasks whose SOTA already sits at 0.98–0.99 accuracy (ACP, T3SE) are poor targets: there is no measurable head-room, and the only defensible contribution left is showing that the numbers fall under a controlled split — which is the sensitive framing the earlier survey already flagged.

### Gaps
- Per-ligand residue counts and positive rates for heme/GTP/Zn in LABind DS1/DS2 are not in the article body; they are inside the Zenodo archive, which I did not download.
- Carbohydrate-binding residues: I found no dedicated 2023–2026 sequence-only benchmark with published sizes; they appear only inside the 3,651/474-ligand DS3 pool.
- AMPBench-MT and PepBenchmark dataset sizes, positive rates and baseline numbers could not be extracted (the arXiv PDF exceeded the fetch limit; the GitHub README does not enumerate per-dataset sizes). PepBenchmark is only described as **35 datasets (29 canonical + 6 non-canonical) in 7 groups**, data auto-downloaded from HuggingFace `jiahuizhang/PepBenchData`, with a `hybrid_split` and five `fold_seeds` — and its own docs warn that negative sampling "may introduce UniRef sequences (unverified)" and that `fold_seed` significantly affects results — [PepBenchmark repo](https://github.com/ZGCI-AI4S-Pep/PepBenchmark), [arXiv 2604.10531](https://arxiv.org/abs/2604.10531). No license stated in the README excerpt.
- Signal peptides (SignalP-style) and B-cell epitopes were not searched in this pass; treat them as unknown rather than absent.

---

## Q1: Peptide-level tasks with clean benchmarks that the group has not touched

### Takeaway
The remaining cytokine panel (IL-4, TNF-α, IL-10) is untouched, tiny, and a direct continuation of the group's own
IL-6/IL-13/IFN-γ line; AMP/ACP/hemolysis benchmarks are larger but carry documented leakage and negative-set bias,
and ACP metrics are already near-saturated.

### Cited Findings
- IL4pred's benchmark: **904 IL-4-inducing and 742 non-inducing MHC class II binding peptides**, built from experimentally validated IEDB T-helper epitopes — [Prediction of IL4 Inducing Peptides, PMC3893860](https://pmc.ncbi.nlm.nih.gov/articles/PMC3893860/). IL4Pred2 (2025) extends this to **845 human and 560 mouse** IL-4-inducing MHC-II binders with equal-sized negative sets — [IL4Pred2 preprint](https://www.biorxiv.org/content/10.1101/2025.04.23.650150.full.pdf).
- A 2023 ensemble method (Meta-IL4) already exists for IL-4 — [Methods 2023](https://www.sciencedirect.com/science/article/abs/pii/S1046202323001135).
- TNFepitope was built from IEDB TNF-α-inducing peptides, **3,177 of 3,635 belonging to human or mouse**, and its best models reach **AUROC 0.83 (human)** and **0.77 (mouse)** on independent data; a standalone package and web server exist — [Comput Biol Med 2023](https://www.sciencedirect.com/science/article/abs/pii/S0010482523003943), data at [Zenodo](https://zenodo.org/records/20150935).
- IL-10Pred was the first method for IL-10-inducing epitopes; its data comprise **394 MHC-II binders that cause IL-10 release and 848 that do not** — [IL-10Pred algorithm page](https://webs.iiitd.edu.in/raghava/il10pred/algo.php), [PMC5314457](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5314457/).
- ACP benchmarks in current use: ACPmain, ACPAlter, **ACP740 (374 ACP / 366 non-ACP)**, ACPred-Fuse, ACPred-FL, ACP240, AntiCP2.0 main/alternate; PLMACPred (ProtT5 + ESM-2 embeddings) reports accuracies of **94.76 / 96.39 / 98.65%** on the three independent sets — [PLMACPred, Sci Rep 2024](https://www.nature.com/articles/s41598-024-67433-8); ACP-ESM reports **88.51%** accuracy, MCC 0.72 on ACP740 — [arXiv 2401.02124](https://arxiv.org/pdf/2401.02124).
- AMP benchmark hygiene is a documented problem: benchmarks are **biased by negative-data selection** — [Sidorczuk et al., PMC9487607](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9487607/); and homology-controlled AMP evaluation (clustering at 30% identity, each cluster in exactly one partition; k-mer leakage flagged) is only now being formalised — [AMPBench-MT, arXiv 2607.25518](https://arxiv.org/pdf/2607.25518), with a cross-species variant in [PathoMIC, arXiv 2608.26228](https://arxiv.org/pdf/2608.26228).
- Hemolysis prediction has its own reliability critique — [arXiv 2012.06470](https://arxiv.org/pdf/2012.06470).
- For peptide–MHC, the IEDB runs a **weekly, fully automated, prospective benchmark** on data entered into IEDB before release; NetMHCIIpan 4.1 BA currently tops the MHC-II binding ranking — [platform paper](https://academic.oup.com/bioinformatics/article/34/9/1522/4769495), [live table](https://tools.iedb.org/auto_bench/mhcii/weekly/).

### Inferences
- IL-4 and TNF-α are the two best peptide-level candidates: untouched by the group, same data provenance (IEDB) and same window sizes as DeepEpiIL13/RAG_MCNNIL6, and TNF-α's 0.83/0.77 AUROC leaves genuine head-room, which ACP's 0.98 accuracy does not.
- IL-10 (394 positives) is probably below the size at which an embedding-retrieval database is meaningful — the neighbour pool is the dataset itself.
- A credible "two-task" variant exists: IL-4 **and** TNF-α in one paper, with a shared retrieval module, mirroring how the group reuses one module across ligands.

### Gaps
- None of the cytokine-epitope papers I read state a sequence-identity cutoff (CD-HIT) between their train and independent peptide sets; this must be checked in the supplementary material before claiming an honest split.
- B-cell epitope benchmarks (BepiPred-class) were not examined in this pass.

---

## Q2: Residue-level tasks — benchmark availability and positive rates

### Takeaway
Heme, GTP and the "unseen ligand" setting are the cleanest untouched residue-level targets, all delivered by the
LABind/BioLiP2 line with 30% identity filtering and a genuine date-based split; among PTMs, lactylation has the
best-documented benchmark *and* the best-documented failure mode.

### Cited Findings
- LABind's three datasets: **DS1** = 2,626 chains, 19 ligands (9 metal ions + ATP/ADP/AMP/GDP/GTP/HEM/CO₃²⁻/NO₂⁻/SO₄²⁻/PO₄³⁻) from BioLiP (Feb 2021); **DS2** = 6 ligands (ATP, HEM, Zn²⁺, Ca²⁺, Mg²⁺, Mn²⁺); **DS3** = 21,651 training proteins with 3,651 ligands and 1,049 test proteins with **474 unseen ligands** from BioLiP2 (3 Apr 2024) — [LABind, PMC12365077](https://pmc.ncbi.nlm.nih.gov/articles/PMC12365077).
- Redundancy and split control: CD-HIT removal of chains above **30% identity** for DS1/DS2 and MMseqs2 at **<30% identity with >0.3 coverage** for DS3; DS1/DS2 split by PDB release date around **January 2017**, DS3 trained on pre-**1 Jan 2021** data and tested on later entries — [LABind, PMC12365077](https://pmc.ncbi.nlm.nih.gov/articles/PMC12365077).
- Per-ligand results: Zn²⁺ MCC **0.837**, HEM **0.730** (vs DELIA 0.596, GraphBind 0.633), GTP **0.667** (vs LigBind 0.554), ATP on DS3 **0.663**; LABind's average MCC is **4.7% above GPSite** on DS2 — [LABind](https://www.nature.com/articles/s41467-025-62899-0), [PMC12365077](https://pmc.ncbi.nlm.nih.gov/articles/PMC12365077).
- Sites are derived from **BioLiP2**, which covers 463 ligands (353 from BioLiP v1 plus 110 added later) — [BioLiP2, NAR 2024](https://academic.oup.com/nar/article/52/D1/D404/7233921).
- Lactylation datasets and their cutoffs: FSL-Kla 343 pos / ~6,860 neg (3 species, peptide-level, 2021); DeepKla 1,720/1,767 (CD-HIT **30%**, 2022); Auto-Kla 1,912/19,562 (CD-HIT **70%**, 2023); ABFF/EBFF-Kla 9,560/9,560 (CD-HIT 70%, 2024); HybridKla **23,984/23,984 across 14 species** (peptide-level, 2025) — [mini-review, PMC13256538](https://pmc.ncbi.nlm.nih.gov/articles/PMC13256538/).
- Reported lactylation performance: PCBert-Kla AUC **0.9728** / MCC **0.8999**; DeepKla **0.9722 / 0.8671**; ABFF-Kla 0.9399 / 0.6829; Auto-Kla 0.9234 / 0.554; HybridKla (ESM2 + LSTM) 0.8460 — [PMC13256538](https://pmc.ncbi.nlm.nih.gov/articles/PMC13256538/); PBertKla reports AUC >0.880 on independent validation — [BMC Biol 2025](https://bmcbiol.biomedcentral.com/articles/10.1186/s12915-025-02202-1).
- The review's central negative result: on the comprehensive multi-species benchmark, **DeepKla's AUC fell to 0.5563 and Auto-Kla's to 0.6563**; early datasets carry ~**1:20** imbalance; "unlabeled lysines cannot be assumed to be true negatives" — [PMC13256538](https://pmc.ncbi.nlm.nih.gov/articles/PMC13256538/).
- dbPTM 2025 holds **>2.79 million PTM sites, 2.243 million experimentally validated**, from 48 databases and >80,000 articles, with cross-species search and bulk download — [NAR 2025, D377–D386](https://academic.oup.com/nar/advance-article-pdf/doi/10.1093/nar/gkae1005/60586513/gkae1005.pdf), [dbPTM site](https://biomics.lab.nycu.edu.tw/dbPTM/index.php).
- Disorder: CAID3 (run in **2025**) assessed 43 methods on **646 DisProt proteins**, with best **Fmax 0.483** overall and **0.792** after filtering bona fide structured regions, gains of **+31% AP on linkers** and **+15% on disorder** over CAID2, and "mostly new" top methods built on pLM embeddings; the new sub-challenge of finding binding regions inside known IDRs "remains challenging" — [CAID3, PMC12750029](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12750029/).
- Protein–peptide binding residues are **already done by the group** (ProtTrans + multi-window CNN, JMGM 2024, 130:108777) — group list, `Prof Ou/research.md`.

### Inferences
- Lactylation is the one residue-level task where the published literature itself names the research question for you: "does a PLM + mCNN model, with or without retrieval, survive a cross-species split?" The expected answer is initially *no*, which is a publishable, falsifiable result rather than a 0.99 table.
- The mixed identity cutoffs across Kla datasets (30% vs 70% vs peptide-level only) mean the first contribution of such a thesis would be a re-split, which is cheap and defensible.
- Heme and GTP let you keep the group's exact paper template while competing against structure-based methods — the fairest kind of comparison to lose, and a strong one to win.

### Gaps
- Per-ligand positive rates (residue-level) for heme/GTP are not in the LABind text; they are in the Zenodo archive.
- No verified benchmark found this pass for carbohydrate-binding residues or for signal peptides.

---

## Q3: Protein-family tasks analogous to the transporter series

### Takeaway
The closest structural analogues to the group's transporter papers are ARG resistance-class/mechanism
classification and bacterial secreted-effector typing; both are multi-class, sequence-only, homology-driven family
problems — but effector prediction is already at ~0.99 and therefore saturated, while ARG still shows a visible
gap between alignment-based and PLM-based tools.

### Cited Findings
- Trans-ARG (ESM-2 embeddings + transformer) reports sensitivity **0.8879**, specificity **0.9211**, AUC **0.9672**, against CARD's AUC **0.7382** — [Trans-ARG, ACM 2024](https://dl.acm.org/doi/10.1145/3703412.3703425).
- ProtAlign-ARG combines PLM embeddings with alignment scoring and reaches **F1 0.83** vs **0.71** for the alignment-only model — [Sci Rep 2025](https://www.nature.com/articles/s41598-025-14545-4).
- A 2025 study predicts ARGs **and bacterial phenotypes** from PLMs, reporting that CARD has slightly higher precision but is worst on the other three metrics — [PubMed 40988849](https://pubmed.ncbi.nlm.nih.gov/40988849/). Resistance **mechanism** prediction from a PLM is also published — [PMC11464418](https://pmc.ncbi.nlm.nih.gov/articles/PMC11464418/). CARD 2023 explicitly added ML support and resistome prediction — [PMC9825576](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9825576/).
- Secreted effectors: PLM-T3SE reaches **98.1% accuracy, 1.8–42.4 pp above prior predictors** on the same independent set — [J Cell Biochem 2024](https://onlinelibrary.wiley.com/doi/10.1002/jcb.30642); PLM-effector reaches **macro-F1 0.9899** for T3SEs via a stacking ensemble of terminal PLM embeddings — [Brief Bioinform 2026](https://academic.oup.com/bib/article/27/2/bbag143/8607031); MoCETSE is best on T1SE/T6SE — [PLOS Comput Biol](https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1013397); a 2026 review catalogues the field's open problems — [Open Biology 2026](https://royalsocietypublishing.org/rsob/article/16/8/250485/483063/Challenges-and-opportunities-in-type-III-secretion) and [PMC13139186](https://pmc.ncbi.nlm.nih.gov/articles/PMC13139186/).
- Phage resources: PhageScope holds **553,688 virulent and 320,030 temperate** phages and annotates proteins into **10 functional classes**; lifestyle labels come partly from the Graphage predictor rather than from experiment — [NAR 2024](https://academic.oup.com/nar/article/52/D1/D756/7334092). Phage lifestyle prediction is currently a *genomic* LM task (Nucleotide Transformer, DNABERT-2, ProkBERT vs BACPHLIP/DeePhage/PhaTYP) — [ProkBERT PhaStyle](https://academic.oup.com/bioinformaticsadvances/article/5/1/vbaf188/8317429); a protein-level virion-protein benchmark was built from RefSeq viral proteins up to **Dec 2022** — [ProteoKnight, arXiv 2508.07345](https://arxiv.org/pdf/2508.07345).

### Inferences
- ARG classification is the best family-level fit: it is multi-class like the efflux super-family paper, it is sequence-only, and because the incumbent tools (CARD/RGI, DeepARG) are explicitly alignment-based, a retrieval module is not a bolt-on gimmick but the natural hypothesis — "is embedding retrieval just a soft BLAST?" is a question the data can answer.
- Effector typing would be a well-fitting but crowded choice: four 2024–2026 methods already use PLMs, and at macro-F1 0.99 the only remaining contribution is an honest-split re-evaluation.
- Phage lifestyle is a poor fit for a protein-level mCNN pipeline (it is nucleotide-level), and PhageScope's lifestyle labels are themselves partly predicted — a label-noise trap.

### Gaps
- I did not verify dataset sizes, positive rates or identity cutoffs for any ARG or effector benchmark; this is required before a proposal.
- GPCR subfamily and enzyme EC-class benchmarks were not searched in this pass.

---

## Q4: Which tasks offer temporal / held-out test sets for honest evaluation

### Takeaway
Four settings give a genuinely honest evaluation without you having to invent a protocol: LABind DS1/DS2
(release-date split), LABind DS3 (pre-2021 training, unseen ligands after), CAID3 (blind community assessment on
newly curated DisProt entries), and the IEDB weekly automated benchmark (prospective, on data not yet public).

### Cited Findings
- LABind DS1/DS2 are divided by **PDB release date before/after January 2017**; DS3 trains on entries released before **1 January 2021** and tests on later entries carrying **474 unseen ligands** — [LABind, PMC12365077](https://pmc.ncbi.nlm.nih.gov/articles/PMC12365077).
- The DNA/RNA benchmark line adds a structural de-duplication step beyond CD-HIT 0.3: removal of proteins with **TM-score > 0.5** by US-align — [MegSite, PMC12496013](https://pmc.ncbi.nlm.nih.gov/articles/PMC12496013/) (already summarised in the earlier survey's dataset notes).
- CAID3 is a blind assessment: 43 methods, 646 DisProt proteins, run in 2025 — [PMC12750029](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12750029/).
- The IEDB automated benchmark evaluates tools "on data newly entered into the IEDB before they are made public", weekly and fully automated — [Bioinformatics 2018](https://academic.oup.com/bioinformatics/article/34/9/1522/4769495); the live MHC-II table shows dated rounds such as **30 Aug 2024 (n = 1,372)** — [weekly table](https://tools.iedb.org/auto_bench/mhcii/weekly/).
- The virion-protein benchmark is time-bounded by construction (RefSeq annotations **up to December 2022**) — [ProteoKnight](https://arxiv.org/pdf/2508.07345).
- Among PTM tasks, the multi-species Kla benchmark functions as a *de facto* held-out set, and that is exactly where published models collapse (AUC 0.9722 → 0.5563) — [PMC13256538](https://pmc.ncbi.nlm.nih.gov/articles/PMC13256538/).

### Inferences
- A thesis built on LABind DS2/DS3 inherits both the identity filter and the time split, so the evaluation-quality contribution the earlier survey recommended comes for free — you spend your months on the model and the ablation, not on re-splitting.
- Cross-species (Kla) and unseen-ligand (DS3) splits are the two cheapest proxies for a temporal split when no date metadata exists.

### Gaps
- Whether CAID3 or the IEDB benchmark accepts new submissions on a timetable compatible with a 4–6 month thesis is not established; both may be usable only as *published* yardsticks, not as live entries.

---

## Q5: Vietnam-relevant angles with real public data

### Takeaway
No curated, protein-level, split-ready benchmark exists for the obvious Mekong-region targets (shrimp AHPND
*Vibrio*, aquaculture pathogens): what is public is genome assemblies and pangenome studies, not a labelled
prediction benchmark. The realistic Vietnam-relevant angle is **antimicrobial-resistance classification**, where
curated labels (CARD) and PLM baselines already exist; aquaculture framing can then be narrative rather than data-dependent.

### Cited Findings
- Public AHPND-related data are genome assemblies and comparative-genomics studies, not prediction benchmarks: complete genomes of *V. parahaemolyticus* L2171/L2181 from *Penaeus vannamei* postlarvae — [PMC12269462](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12269462/); a draft genome from Bangladesh — [Microbiol Resour Announc 2026](https://journals.asm.org/doi/abs/10.1128/mra.00495-26); a Thailand outbreak isolate — [PMC9933731](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9933731/); a Malaysian shrimp-pathogen genome — [PMC6256671](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6256671/); WGS-based delineation of Asian AHPND outbreak origins — [PMC5712426](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5712426/).
- The one ML study found in this area works at the **pangenome/gene-cluster** level (random forest over gene clusters separating environmental, seafood and clinical isolates), not at the protein-sequence-classification level — [PMC11961994](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11961994/).
- The AHPND virulence determinant itself is well defined (pVA plasmid carrying **pirA/pirB** binary toxin genes) — [PMC12269462](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12269462/), [BMC Microbiol 2019](https://bmcmicrobiol.biomedcentral.com/articles/10.1186/s12866-019-1655-8).
- By contrast, AMR has curated labels and published PLM baselines usable immediately: [CARD 2023](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9825576/), [Trans-ARG](https://dl.acm.org/doi/10.1145/3703412.3703425), [ProtAlign-ARG](https://www.nature.com/articles/s41598-025-14545-4), [ARG + phenotype prediction, 2025](https://pubmed.ncbi.nlm.nih.gov/40988849/).

### Inferences
- A "Vietnam-relevant" thesis should therefore be **AMR-framed, not pathogen-framed**: train and evaluate on CARD-derived labels (global, curated, public), and use the aquaculture/Mekong context only in the motivation section. Building a shrimp-pathogen benchmark from scratch would consume the whole 4–6 months on data curation with no guaranteed labels — the classic way a thesis runs out of time.
- A second, lighter Vietnam angle exists in principle via IEDB epitope data for regionally endemic pathogens (dengue), which would reuse the group's epitope pipeline, but I did not verify that a split-ready dengue epitope benchmark exists.

### Gaps
- No verified public benchmark with labelled positives/negatives for aquaculture-pathogen protein classification.
- Dengue/regional-pathogen epitope benchmark availability unverified.

---

## The 3–5 most promising picks, with the argument

### Takeaway
Rank: (1) cross-species lactylation under an honest split, (2) heme or GTP binding residues, sequence-only with
retrieval, (3) IL-4 + TNF-α inducing epitopes, (4) ARG class/mechanism with a "retrieval vs alignment" ablation,
(5) unseen-ligand generalisation on LABind DS3. The first three are the safe-but-publishable core; (4) adds the
Vietnam framing; (5) is the highest-novelty, highest-risk option.

### Cited Findings
- **Pick 1 — Lysine lactylation, cross-species.** Benchmarks ready at several scales (23,984/23,984 over 14 species down to 1,720/1,767 at CD-HIT 30%) and a documented collapse of published models off-dataset (**AUC 0.9722 → 0.5563** for DeepKla; 0.9234 → 0.6563 for Auto-Kla); the review names class imbalance (~1:20), inferred-negative label noise and black-box interpretability as the open problems — [PMC13256538](https://pmc.ncbi.nlm.nih.gov/articles/PMC13256538/). Several ProtBert/ESM-2-based predictors already exist to serve as baselines — [PCBert-Kla, Brief Bioinform 2025](https://academic.oup.com/bib/article/26/6/bbaf615/8328239), [PBertKla, BMC Biol 2025](https://bmcbiol.biomedcentral.com/articles/10.1186/s12915-025-02202-1).
- **Pick 2 — Heme (or GTP) binding residues, sequence-only.** 30%-identity-filtered data with a release-date split; every strong competitor is structure-based (DELIA 0.596, GraphBind 0.633, LABind 0.730 for HEM; LigBind 0.554 vs LABind 0.667 for GTP); data on Zenodo `10.5281/zenodo.15875006` — [LABind](https://www.nature.com/articles/s41467-025-62899-0), [PMC12365077](https://pmc.ncbi.nlm.nih.gov/articles/PMC12365077).
- **Pick 3 — IL-4 and/or TNF-α inducing epitopes.** Tiny, IEDB-derived, same shape as the group's IL-6/IL-13/IFN-γ papers; TNF-α SOTA is only **AUROC 0.83 / 0.77** — [TNFepitope](https://www.sciencedirect.com/science/article/abs/pii/S0010482523003943); IL-4 sets are 904/742 and 845+560 — [PMC3893860](https://pmc.ncbi.nlm.nih.gov/articles/PMC3893860/), [IL4Pred2](https://www.biorxiv.org/content/10.1101/2025.04.23.650150.full.pdf).
- **Pick 4 — ARG class / resistance mechanism.** PLM methods beat alignment baselines by a visible margin (AUC 0.9672 vs 0.7382; F1 0.83 vs 0.71), and curated labels exist in CARD 2023 — [Trans-ARG](https://dl.acm.org/doi/10.1145/3703412.3703425), [ProtAlign-ARG](https://www.nature.com/articles/s41598-025-14545-4), [CARD 2023](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9825576/).
- **Pick 5 — Unseen-ligand generalisation.** 21,651 train / 1,049 test proteins, **474 unseen ligands**, MMseqs2 <30% identity, pre-2021 training cut-off — [LABind, PMC12365077](https://pmc.ncbi.nlm.nih.gov/articles/PMC12365077).
- Compute context (from the earlier survey, for reference): Kaggle gives ~**30 GPU-hours/week** (P100 or T4×2, 12 h/session, 16 GB) and Colab Pro's 100 compute units buy roughly **84 T4-hours or ~18.5 A100-hours per month**; the real bottleneck is embedding **storage** (~6 GB for one window-expanded residue dataset at 1024 dims), so store per-residue embeddings once and slice windows in the dataloader — `docs/common/deep-research/reports/bioinformatics-topic-survey.md` §4, citing [Kaggle docs](https://www.kaggle.com/docs/efficient-gpu-usage) and [Colab FAQ](https://research.google.com/colaboratory/faq.html).

### Inferences
- **Why Pick 1 ranks first.** It satisfies all four of the student's constraints at once: biology load is low (a single modified residue type in a sequence window), compute is trivial (tens of thousands of short peptides, no 6 GB embedding store), the group's pipeline transfers unchanged (ProtT5 + mCNN over a window, plus retrieval as the bolt-on module), and — crucially — the research question is already stated in the published literature rather than being a critique of the advisors' own work. That last point matters given the relationship risk flagged in the earlier survey: the target of the criticism is DeepKla/Auto-Kla, not RAG-msCNN.
- **Why Pick 2 ranks second.** It is the least risky way to get a conventional paper out of the group's template: a new ligand, a dataset that already enforces 30% identity and a time split, and a built-in reason for a sequence-only model to exist (competitors need structures). Risk: the group's 2026 metal-binding RAG paper is adjacent, so heme/GTP must be framed as *organic cofactor / nucleotide*, not as "another metal".
- **Why Pick 3 ranks third despite being the easiest.** Advisor fit is maximal and the data fit on a laptop, but the novelty is procedural — it is the fourth cytokine in a series. It is the right choice if the priority is a smooth defence and a likely co-authored paper; it is the wrong choice if the thesis needs an identifiable idea. Mitigation: make the contribution the **ablation the group has never published** (α and k in the retrieval mixer, plus an honest peptide-level split), with IL-4/TNF-α as the vehicle.
- **Why Pick 4 is the only defensible "Vietnam angle".** The AMR framing has real curated data; the aquaculture framing does not. It also sets up the sharpest version of the retrieval question — against ARG tools that are *explicitly* alignment-based, "does embedding retrieval add anything beyond nearest-neighbour homology?" is directly measurable.
- **Why Pick 5 is last.** Highest novelty (ligand-aware, sequence-only, unseen ligands) but it breaks the group's one-task-per-paper habit, needs the largest embedding job (21k proteins), and risks an empty result if a sequence-only model simply cannot generalise to unseen ligands without ligand geometry.
- Tasks I would actively advise against: ACP and T3SE (metrics at 0.98–0.99, documented train/test overlap), IL-10 (394 positives), phage lifestyle (nucleotide-level, partly predicted labels), MHC-II binding (NetMHCIIpan is too strong a baseline for a first paper).

### Gaps
- For every pick, the per-class positive rates and the exact train/test identity handling still need to be read out of the primary data archives (Zenodo for LABind, GitHub/web servers for the Kla and cytokine sets) before a proposal is written; this pass verified sizes and metrics, not the fold files.
- No source was found that states either advisor's willingness to supervise PTM or AMR topics; all "fit with group style" judgements here are INFERRED from the publication record only.
