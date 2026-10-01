# Advisor research landscape (Prof. Yu-Yen Ou, Dr. Quang-Thai Ho) and 2024–2026 PLM methodological trends

Scope note: the group's publication list was read from the local files
`/home/ngthtrong/CT553H/docs/common/advisor/Prof Ou/research.md` and
`/home/ngthtrong/CT553H/docs/common/advisor/Prof Ho/research.md` (scraped Google Scholar
tables, profiles [user=SdzxC9AAAAAJ](https://scholar.google.com/citations?user=SdzxC9AAAAAJ&hl=en&sortby=pubdate)
and [user=n21zhvkAAAAJ](https://scholar.google.com/citations?hl=vi&user=n21zhvkAAAAJ&view_op=list_works&sortby=pubdate)),
and the Scholar profile for Prof. Ou was re-fetched to confirm. Methodological detail
(datasets, CD-HIT thresholds, metrics, RAG mechanics) was extracted directly from the 9 PDFs
in those two folders using PyMuPDF.

## Q1. Full 2023–2026 paper list, recurring tasks/datasets, typical evaluation protocol

### Takeaway
The group publishes a highly repeatable template at a rate of ~8–10 papers/year: PLM embeddings
(almost always ProtT5-XL-U50 from ProtTrans, with ESM-2 and TAPE as the two standard baselines)
→ multi-window CNN (mCNN) or multi-scale separable CNN (msCNN) → binary/multiclass head, evaluated
with 5-fold CV plus an independent test, reported as sensitivity/specificity/accuracy/MCC/AUC,
with CD-HIT (or BLAST) redundancy removal at 30–40% identity. Since 2025 the only recurring
"novelty slot" has been the add-on module: RAG retrieval over embeddings, ProtGPT2 generation,
knowledge-graph RAG, or (Ho, 2026) a structure-gated GNN.

### Cited Findings — paper list

2026 (Ou profile, confirmed by re-fetch of the Scholar profile):
- NeoGen-BC — generative PLM + multi-window DL for shared breast-cancer neoantigens, *Biochem. Biophys. Res. Commun.* 836:154567 — [doi 10.1016/j.bbrc.2026.154567](https://doi.org/10.1016/j.bbrc.2026.154567)
- DeepCR — cytokine receptor proteins, PLM + DL, *J. Biomol. Struct. Dyn.* 44(10):4821–4838 — [Scholar entry](https://scholar.google.com/citations?view_op=view_citation&hl=en&user=SdzxC9AAAAAJ&citation_for_view=SdzxC9AAAAAJ:8AbLer7MMksC)
- Metal-binding residue classification with RAG + PLM + DL, *Engineering Applications of AI* 171:114330 — [Scholar entry](https://scholar.google.com/citations?view_op=view_citation&hl=en&user=SdzxC9AAAAAJ&citation_for_view=SdzxC9AAAAAJ:V3AGJWp-ZtQC)
- RAG-msCNN — protein-DNA binding sites, *Biomed. Signal Process. Control* 115:109407 — [doi 10.1016/j.bspc.2025.109407](https://doi.org/10.1016/j.bspc.2025.109407)
- msCNN-PLM-FAD — FAD binding sites, *Analytical Biochemistry* 116092 — [doi 10.1016/j.ab.2026.116092](https://doi.org/10.1016/j.ab.2026.116092)
- MCNN-AAPT — amino-acid/peptide transporters within secondary active transporters, *J. Biomol. Struct. Dyn.* 44(2):657–666 — [Scholar entry](https://scholar.google.com/citations?view_op=view_citation&hl=en&user=SdzxC9AAAAAJ&citation_for_view=SdzxC9AAAAAJ:738O_yMBCRsC)
- IFNg_DeepKG — IFN-γ-inducing epitopes via knowledge-graph RAG, *J. Chem. Inf. Model.* 66(1):770–784 — [Scholar entry](https://scholar.google.com/citations?view_op=view_citation&hl=en&user=SdzxC9AAAAAJ&citation_for_view=SdzxC9AAAAAJ:BrmTIyaxlBUC)
- SirtSAGE — sirtuin classification + evolutionary mapping, structural-gated graph attention, *J. Comput. Biophys. Chem.* (Ho profile, Ou not an author) — [Scholar entry](https://scholar.google.com/citations?view_op=view_citation&hl=vi&user=n21zhvkAAAAJ&citation_for_view=n21zhvkAAAAJ:mVmsd5A6BfQC)

2025:
- CFTR_TL — transfer learning for CFTR ATP binding sites + mCNN, *ACS Omega* 10(47):56964–56972
- DEEPTRANS — primary active transporters, RAG-augmented PLM + multi-scale DL, *Chemical Physics Letters* 142495
- mCNN-GenEfflux — efflux proteins/superfamilies, ProtGPT2-generated sequences + mCNN, *Comput. Biol. Chem.* 108595 — [doi 10.1016/j.compbiolchem.2025.108595](https://doi.org/10.1016/j.compbiolchem.2025.108595)
- RTK_RAG — ATP binding sites in receptor tyrosine kinases, RAG + mCNN, *J. Chem. Inf. Model.* 65(13):7277 — [doi 10.1021/acs.jcim.5c00766](https://doi.org/10.1021/acs.jcim.5c00766)
- NA_mCNN — sodium transporters, ProtTrans + multi-window DL, *J. Proteome Res.* 24(5):2324–2335
- NAD_MCNN — deacetylase NAD+ binding sites, *Chem. Biol. Drug Des.* 105(4):e70085
- mCNN-glucose — glucose transporter families, *Int. J. Biol. Macromol.* 294:139522
- DeepEpiIL13 — IL-13-inducing epitopes, ProtT5 + mCNN, *ACS Omega* 10:9675–9683 — [doi 10.1021/acsomega.4c10960](https://doi.org/10.1021/acsomega.4c10960)
- RAG_MCNNIL6 — IL-6-inducing epitopes, retrieval-augmented mCNN, *J. Chem. Inf. Model.* 65(5):2685
- CaBind_MCNN — calcium-binding sites in ion channels/transporters, *J. Chem. Inf. Model.* 65(4):2145
- ATP_mCNN — ATP binding sites, *Computers in Biology and Medicine* 185:109541
- (non-bioinformatics) real-world Taiwanese hypertension cohort, *J. Hypertension* 44(1):130

2024:
- "Deciphering the language of protein-DNA interactions" — contextual embeddings + multi-scale sequence modeling, *J. Mol. Biol.* 436(22):168769
- DeepNeoAG — melanoma neoantigen epitopes, PLM + multi-window scanning, *Int. J. Biol. Macromol.* 281:136252
- VesiMCNN — vesicular transport proteins, *Int. J. Biol. Macromol.* 136048
- MCNN_MC — mitochondrial carriers + bongkrekic acid toxicity, *J. Chem. Inf. Model.* 64(24):9125
- ProtTrans + multi-window scanning CNN for protein-peptide interaction sites, *J. Mol. Graph. Model.* 130:108777
- DeepPLM_mCNN — ion channels and ion transporters, *Comput. Biol. Chem.* 110:108055
- MFPS_CNN (ion transporters, PSSM + multi-filter CNN) appears as a 2024 thesis-type entry on the Ho profile; the journal version is *Molecular Informatics* 41(9):2100271 (2022)

2023:
- Review: "Recent advances in features generation for membrane protein sequences: from MSA to pre-trained language models", Ou, Ho, Chang, *Proteomics* 23(23-24):2200494
- "Integrating pre-trained PLM and multiple window scanning deep learning networks ... secondary active transporters", Malik & Ou, *Methods* 220:11–20
- Disto-TRP — TRP channel identification using AlphaFold-generated structural information, *Gene* (Ou profile; the one clear pre-2024 use of predicted structure in the group)
- "Anti-drugs chatbot: Chinese BERT-based cognitive intent analysis", *IEEE Trans. Comput. Soc. Syst.* (off-topic)

Ho's earlier line (2021–2022, mostly with N.Q.K. Le) is DNA-sequence BERT work: BERT-Promoter
(*Comput. Biol. Chem.* 99:107732, [doi 10.1016/j.compbiolchem.2022.107732](https://doi.org/10.1016/j.compbiolchem.2022.107732)),
6mA cross-species with deep transformers (*Methods* 204:199–206, [doi 10.1016/j.ymeth.2021.12.004](https://doi.org/10.1016/j.ymeth.2021.12.004)),
BERT+2D-CNN DNA enhancers (*Brief. Bioinform.* 22(5):bbab005), SNARE proteins with multiscan CNN + PSSM
(*J. Chem. Inf. Model.* 62(19):4820), mCNN-ETC electron transporters (*Brief. Bioinform.* 23(1):bbab352),
and GT-Finder glucose transporter families with BERT ([doi 10.1016/j.compbiomed.2021.104259](https://doi.org/10.1016/j.compbiomed.2021.104259)).

### Cited Findings — evaluation protocol (from the PDFs)
- Redundancy filtering is CD-HIT at **40%** identity for protein-family / peptide tasks: GT-Finder used CD-HIT 40% on GLUT/SGLT/SWEET, reducing 9616/4107/2026 proteins to **510/225/190** ([GT-Finder](https://doi.org/10.1016/j.compbiomed.2021.104259)); RTK_RAG ran CD-HIT at 40% between ATP-549 and a new RTK(313) set, leaving 69 RTK proteins for validation and 244 for the RAG database ([RTK_RAG](https://doi.org/10.1021/acs.jcim.5c00766)); NeoGen-BC used CD-HIT at 40% leaving 561 neoantigen and 2823 self-antigen peptides ([NeoGen-BC](https://doi.org/10.1016/j.bbrc.2026.154567)).
- Residue-level binding-site tasks use **30%**: RAG-msCNN applied CD-HIT so that no training/test proteins share >30% similarity, and used the same 30% cutoff for the RNA datasets ([RAG-msCNN](https://doi.org/10.1016/j.bspc.2025.109407)); msCNN-PLM-FAD used BLAST to drop >30% identity, cutting 22,506 collected samples to **12,850** ([msCNN-PLM-FAD](https://doi.org/10.1016/j.ab.2026.116092)).
- Metrics are always sensitivity, specificity, accuracy, MCC, AUC; MCC is treated as the headline "class-balance" metric. NeoGen-BC additionally reports **AUPRC**, which is new for the group ([NeoGen-BC](https://doi.org/10.1016/j.bbrc.2026.154567)).
- Protocol is 5-fold CV on the training split plus a held-out independent test; mCNN-GenEfflux used an 80/20 split with 5-fold CV inside the 80% ([mCNN-GenEfflux](https://doi.org/10.1016/j.compbiolchem.2025.108595)). The Ho-line DNA papers used 10-fold CV instead ([BERT-Promoter](https://doi.org/10.1016/j.compbiolchem.2022.107732)).
- Window-size sweeps are a standard experiment: msCNN-PLM-FAD compared window lengths 13/15/17/19 with 5-fold CV and reported Welch's t-test (p = 0.0466) for msCNN vs. single-window CNN, best mean CV MCC 0.6559 ± 0.0754 ([msCNN-PLM-FAD](https://doi.org/10.1016/j.ab.2026.116092)); RTK_RAG settled on windows 10/12/8 ([RTK_RAG](https://doi.org/10.1021/acs.jcim.5c00766)).
- Embedding comparison is a fixed table. RTK_RAG without RAG: ProtTrans AUC 0.9497 / MCC 0.3181; ESM-2 1280-dim AUC 0.9403 / MCC 0.2293; ESM-2 2560-dim AUC 0.9378 / MCC 0.4235; TAPE AUC 0.8300 / MCC 0.1100 — and they note ESM-2 2560 "demanded roughly twice the computational resources" so ProtTrans was chosen ([RTK_RAG](https://doi.org/10.1021/acs.jcim.5c00766)). DeepEpiIL13 likewise reports ProtT5-XL-U50 beating ESM-2 and ESM-1b ([DeepEpiIL13](https://doi.org/10.1021/acsomega.4c10960)).
- Interpretability is **post-hoc and standard**: t-SNE/UMAP cluster plots plus SHAP in msCNN-PLM-FAD (with per-residue SHAP mapped onto the B-factor column of PDB 1O97) and RAG-msCNN; Grad-CAM heatmaps in mCNN-GenEfflux; t-SNE/UMAP/SHAP in the 6mA paper.
- Code/data are released on GitHub per paper (e.g. github.com/mhb1717/RAG_DNA_RNA, github.com/mhb1717/efflux, github.com/B1607/RTK_RAG, github.com/s1101404/DeepEpiIL13, github.com/s1129108/NeoGenBC).
- Funding is NSTC Taiwan (e.g. NSTC 112-2221-E-155-020-MY3, in RAG-msCNN).

### Cited Findings — what the "RAG" module actually is
- RAG-msCNN builds the retrieval DB from a separate curated set, CD-HIT-clustered at 30% so retrieval sequences do not overlap train/test; retrieval is applied **only to positive residues**, finds top k = 5 nearest neighbours by Euclidean (L2) distance, averages them, and fuses with α = 0.7 original / 0.3 retrieved — explicitly "within the convex hull of the original and retrieved embeddings" ([RAG-msCNN](https://doi.org/10.1016/j.bspc.2025.109407)). So it is a k-NN embedding-smoothing trick, not generative retrieval.
- RTK_RAG's RAG database is 244 RTK sequences (2676 ATP-binding and 261,088 non-binding residues); the paper's Figure 4 narrates the generic LLM-RAG story (retrieved sequences form an "enriched prompt ... passed into an LLM") even though the model has no LLM ([RTK_RAG](https://doi.org/10.1021/acs.jcim.5c00766)).
- msCNN replaces standard Conv2D with SeparableConv2D to decouple spatial and channel-wise extraction and cut parameters; the stated motivation is that mCNN "did not exploit channel-wise independence across feature dimensions" ([RAG-msCNN](https://doi.org/10.1016/j.bspc.2025.109407)).
- mCNN-GenEfflux fine-tunes ProtGPT2 on efflux families to generate sequences as augmentation for severely imbalanced classes (SMR had 18 sequences vs ABC 2394), filters generated sequences by perplexity, and validates folding confidence with AlphaFold2 pLDDT/pTM; reported gains are large (Class B sensitivity 0.5385→0.9999, MCC 0.4397→0.9327) ([mCNN-GenEfflux](https://doi.org/10.1016/j.compbiolchem.2025.108595)).
- NeoGen-BC is the group's most elaborate pipeline: CEDAR-curated epitopes → MCNN-BiLSTM classifier → RAG module → ProtGPT2 de novo generation → convex-hull biophysical filtering → ESMFold pLDDT screening → NetMHCIIpan 4.3 cross-check across 14 HLA-II alleles; independent-test AUC 0.9053 ([NeoGen-BC](https://doi.org/10.1016/j.bbrc.2026.154567)).
- SirtSAGE (Ho, 2026) is the group's first graph model: ESM-2 embeddings into GATv2 with AlphaFold **pLDDT scores used as spatial confidence gates** ([Scholar entry](https://scholar.google.com/citations?view_op=view_citation&hl=vi&user=n21zhvkAAAAJ&citation_for_view=n21zhvkAAAAJ:mVmsd5A6BfQC)); I could not open the full text (publisher page [worldscientific.com/toc/jcbc](https://www.worldscientific.com/toc/jcbc/0/0)) so the dataset size and metrics are unverified.

### Inferences
- The group's unit of novelty is **task × add-on module**, not architecture or training regime. Every 2024–2026 paper keeps frozen PLM embeddings + window-scanning CNN fixed, and varies either the biological target or one bolt-on (RAG / ProtGPT2 / KG / GNN).
- Two intentional efficiency constraints are visible and will shape what an advisor accepts: they pick ProtTrans over ESM-2 2560 explicitly on compute grounds, and they moved to separable convolutions to cut parameters. A proposal that needs large-scale training will meet resistance; one that *saves* compute is on-brand.
- Reported numbers are at the ceiling (AUC up to 99.9% in RAG-msCNN on highly imbalanced residue data). That is a methodological opening, not just bragging: AUC on 5–11% positive data is close to uninformative, and the group has only just started reporting AUPRC (NeoGen-BC). A thesis that re-evaluates their own published tasks under AUPRC + proper splits has built-in novelty with zero new biology.

### Gaps
- Citation/impact-factor data per venue not collected. Several 2025–2026 titles (DeepCR, MCNN-AAPT, metal-binding EAAI, DEEPTRANS, CFTR_TL, NA_mCNN, NAD_MCNN, mCNN-glucose, CaBind_MCNN, ATP_mCNN, IFNg_DeepKG) were only available as Scholar entries — their internal protocol details (exact CD-HIT thresholds, dataset sizes) are inferred from the sibling papers, not verified.
- SirtSAGE and IFNg_DeepKG full texts were not obtained, so how far the group has already gone with GNNs and knowledge graphs is only partly known.

## Q2. Which wider-field 2024–2026 trends are absent from the group's work

### Takeaway
Six trends are clearly adopted by the wider field but absent from the group's 2024–2026 output:
(1) parameter-efficient fine-tuning (LoRA) of the PLM instead of frozen embeddings; (2) structure-aware
PLMs (SaProt, ProstT5, ESM3/ESM-C); (3) predicted-structure + GNN inputs (only just entering via
SirtSAGE); (4) multi-task heads shared across ligand types; (5) calibration / conformal uncertainty;
(6) contrastive or zero-shot/text-conditioned classification for rare families. Explainability is
partially adopted (SHAP, Grad-CAM) but never validated against known motifs, and leakage-aware
splitting beyond CD-HIT is absent.

### Cited Findings — the trends and their prior work
- **PEFT/LoRA is now the recommended default.** Schmirler et al., "Fine-tuning protein language models boosts predictions across diverse tasks", *Nature Communications* 15:7407 (28 Aug 2024): parameter-efficient fine-tuning "can reach similar improvements consuming substantially fewer resources at up to 4.5-fold acceleration of training over fine-tuning full models", they used the LoRA implementation of PEFT, and they conclude one should "always try fine-tuning, in particular for problems with small datasets" — [Nature Communications](https://www.nature.com/articles/s41467-024-51844-2). (Note: I could not open the full text past the publisher login/CAPTCHA, so these are the publisher-indexed abstract/summary claims, not verified against the tables.)
- PEFT-SP applies LoRA to ESM2-3B for signal-peptide prediction and surpasses the prior state of the art and fully fine-tuned ESM-2 across all five signal-peptide types — [PMC11529868](https://pmc.ncbi.nlm.nih.gov/articles/PMC11529868/).
- LoRA on ESM-2 for **binding-residue** prediction specifically exists already: ESMBind/QBind predicts binding residues from single sequences with no MSA or structure and is reported comparable to structural models — [ESMBind write-up](https://huggingface.co/blog/AmelieSchreiber/esmbind), [ESMBind/QBind preprint](https://www.biorxiv.org/content/10.1101/2023.11.13.566930.full.pdf). This is a 2023-origin result, so "LoRA on a binding-site task" alone is no longer novel.
- SI-Tuning combines an injection mechanism with LoRA, keeps the ESM-2 backbone frozen, tunes <2% of parameters, and improves metal-ion binding by 4.49% and 1.99% on two settings — [Boost Protein Language Model with Injected Structure Information Through PEFT, *Comput. Biol. Med.*](https://www.sciencedirect.com/science/article/abs/pii/S0010482525009588).
- A 2025 study finds "fine-tuned embeddings consistently outperform static embeddings despite dataset-specific variations", framing frozen-embedding pipelines as "a critical shortcoming of existing methods" — [Enhancing Structure-aware PLMs, bioRxiv](https://www.biorxiv.org/content/10.1101/2025.04.23.650337v1.full.pdf).
- **Structure-aware PLMs.** SaProt uses a structure-aware vocabulary pairing residue tokens with Foldseek 3Di structure tokens, trained on ~40M sequence+structure pairs, and surpasses baselines on 10 downstream tasks — [SaProt, ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/file/1c42513b8895ab11fbbb5b7e8e6b6b02-Paper-Conference.pdf). ProstT5 is bilingual over amino-acid and 3Di sequences and was benchmarked on per-residue tasks including **binding residues** — [ProstT5, bioRxiv](https://www.biorxiv.org/content/10.1101/2023.07.23.550085v1.full.pdf). S-PLM aligns sequence and structure by contrastive learning — [*Advanced Science* 2025](https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/advs.202404212).
- **ESM-C** (ESM Cambrian, released at 300M/600M/6B) reports that the 300M model "delivers similar performance to ESM2 650M with dramatically reduced memory requirements and faster inference" — [EvolutionaryScale blog](https://www.evolutionaryscale.ai/blog/esm-cambrian), [model card](https://multimolecule.danling.org/models/esmc/). The group's standard baseline table (ProtTrans / ESM-2 / TAPE) contains nothing from 2024 onwards.
- **Predicted structure + GNN, multi-task over ligands.** GPSite is a single multi-task GNN over ESMFold-predicted structures and PLM embeddings predicting binding residues for DNA, RNA, peptide, protein, ATP, HEM and metal ions, with a shared GNN plus 10 ligand-specific MLPs; it "substantially surpasses state-of-the-art sequence-based and structure-based approaches ... even when the structures are not well-predicted" — [eLife 2024](https://elifesciences.org/articles/93695/peer-reviews), [PMC11023698](https://pmc.ncbi.nlm.nih.gov/articles/PMC11023698/), [code](https://github.com/biomed-AI/GPSite).
- MPBind (Bioinformatics 41(11), Nov 2025) is multi-task over proteins, DNA/RNA, ligands, ions and lipids using **both ProtTrans and ProstT5** plus an equivariant GNN; trained on ~376K PDB chains clustered at 30% identity, tested on Test1 (40,651 chains) and a post-2022 Test2 (1,452 chains); Test2 AUROC 0.84 / AUPRC 0.62 for protein-protein and AUROC 0.81 / AUPRC 0.44 for DNA/RNA; outperforms ScanNet, CLAPE and GraphBind and works with AlphaFold structures — [Bioinformatics](https://academic.oup.com/bioinformatics/article/41/11/btaf589/8300842).
- LABind predicts ligand-aware binding sites by learning ligand-protein interactions, i.e. generalises across ligand types rather than one model per ligand — [*Nature Communications* 2025](https://www.nature.com/articles/s41467-025-62899-0).
- Note the contrast: the group ships **one paper per ligand** (ATP, FAD, NAD, Ca, metal), while the field's 2024–2025 state of the art is one multi-task model for all of them.
- **Contrastive learning for protein-DNA binding already exists** in exactly the group's task: "Protein–DNA binding sites prediction based on pre-trained protein language model and contrastive learning", *Briefings in Bioinformatics* 25(1):bbad488 — [BIB](https://academic.oup.com/bib/article/25/1/bbad488/7505238). An attention-map-guided GCN with PLM embeddings + physicochemical features for nucleic-acid binding sites appeared in *Briefings in Bioinformatics* 26(5):bbaf457 (2025) — [BIB](https://academic.oup.com/bib/article/26/5/bbaf457/8249066).
- **Calibration / conformal prediction.** CPEC couples a deep model with conformal prediction to give FDR-controlled enzyme function predictions with a user-specified risk level — [*PLOS Comput. Biol.* 2024](https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1012135), [PMC11164347](https://pmc.ncbi.nlm.nih.gov/articles/PMC11164347/). "Functional protein mining with conformal guarantees" extends this to search/homology/EC classification — [*Nature Communications* 2024/2025](https://www.nature.com/articles/s41467-024-55676-y). Nothing comparable appears in the group's work; their uncertainty handling is limited to reporting MCC.
- **Zero-shot / text-conditioned classification.** ProtNote couples protein embeddings with LLM text embeddings to predict unseen GO terms and EC numbers in a zero-shot setting — [bioRxiv](https://www.biorxiv.org/content/10.1101/2024.10.17.618952v1.full), [PubMed 40233101](https://pubmed.ncbi.nlm.nih.gov/40233101/). For transporters specifically, TooTranslator does zero-shot substrate classification by aligning protein and chemical language embeddings — [bioRxiv Nov 2025](https://www.biorxiv.org/content/10.1101/2025.11.13.688294.full.pdf).
- **Transporter-task competitors the group does not cite.** TooT-SC predicts 11 substrate classes (82.5% accuracy on independent test) and TooT-SS (ICBBB 2025) uses ProtBERT-BFD transfer learning to predict 83 of 96 specific-substrate classes with F1 0.92 / MCC 0.91 — [TooT-SS PDF](https://www.bio-conferences.org/articles/bioconf/pdf/2025/14/bioconf_icbbb2025_01001.pdf). SPOT (PLOS Biology, Sept 2024) uses fine-tuned ESM-1b vectors for transporter-substrate prediction — [PLOS Biology](https://journals.plos.org/plosbiology/article?id=10.1371%2Fjournal.pbio.3002807). A 2025 paper compares structure encodings vs sequence embeddings for transporter substrate prediction — [*Molecules* 30:3226](https://doi.org/10.3390/molecules30153226).
- **Leakage-aware evaluation.** Random splitting of biological sequence databases produces "dubious assessments of generalization because of similarity between training and test samples"; SpanSeq offers similarity-based splitting — [arXiv 2402.14482](https://arxiv.org/pdf/2402.14482). "Beware of Data Leakage from Protein LLM Pretraining" shows leakage from *pretraining* data distorts measured performance and compares pretraining-aware vs naive clustering splits — [bioRxiv](https://www.biorxiv.org/content/10.1101/2024.07.23.604678v1.full). For interaction benchmarks, strict sequence-identity thresholds alone "fail to prevent substantial leakage, leading to overoptimistic performance metrics"; iDist detects redundancy via 3D interface geometry — [Revealing Data Leakage in Protein Interaction Benchmarks, ICLR workshop 2024](https://mlanthology.org/iclrw/2024/bushuiev2024iclrw-revealing/). A 2026 preprint reports a residue-level leakage artifact inflating metrics by 27–39% and able to reverse representation rankings — [arXiv 2606.04228](https://arxiv.org/pdf/2606.04228).
- **Structure is not always worth it** — useful ammunition for a sequence-only thesis. The same 2026 analysis finds ESM-2 beats AlphaFold2 representations on binding affinity (0.449 vs 0.307 correlation) and conformational flexibility (AUROC 0.824 vs 0.764), while AlphaFold2 wins only on allosteric-site classification (AUROC 0.548 vs 0.485), concluding the benefit "depends entirely on the biological mechanism" — [arXiv 2606.04228](https://arxiv.org/pdf/2606.04228).
- **Motif-validated explainability** is an active 2025 area the group has not touched: MotifAE uses sparse autoencoders over PLM embeddings and shows the discovered sparse features align with known functional motifs — [bioRxiv / PMC12637460](https://pmc.ncbi.nlm.nih.gov/articles/PMC12637460/); InterPLM discovers interpretable features via sparse autoencoders including binding sites and structural motifs — [InterPLM](https://www.researchgate.net/publication/395958458_InterPLM_discovering_interpretable_features_in_protein_language_models_via_sparse_autoencoders); concept activation vectors have been used to localize protein motifs in PLM embedding space — [arXiv 2511.21614](https://arxiv.org/pdf/2511.21614). A 2025 review stresses that interpretability claims remain "a mathematical explanation until a human researcher recognizes it", i.e. attribution must be checked against known motifs — [Toward the Explainability of Protein Language Models, arXiv 2506.19532](https://arxiv.org/pdf/2506.19532).

### Inferences
- The single biggest methodological gap is **frozen embeddings**. Everything in the group's 2024–2026 pipeline treats the PLM as a fixed feature extractor; the field's 2024 consensus paper says fine-tuning should be the default, especially for small datasets — which describes nearly every dataset the group works on (190–561 sequences after CD-HIT in several cases).
- Their second-biggest gap is **evaluation rigour rather than architecture**. They already do CD-HIT splits, but not pretraining-aware splits, not AUPRC as standard, not calibration, and not time-based (post-cutoff) test sets like MPBind's Test2. These are all cheap on Colab and directly attack the ceiling-effect numbers in their own papers.
- "RAG" in their papers is k-NN embedding fusion with a hand-set α = 0.7. That is a parameter nobody in the group has justified or learned — a legitimate small-scale methodological target.

### Gaps
- I could not verify Schmirler et al.'s per-task numbers (how much LoRA gains on per-residue binding tasks specifically) because the Nature Communications full text was behind a redirect/login and the PMC mirror returned a CAPTCHA. The report writer should treat the "up to 4.5-fold acceleration" and "always try fine-tuning" claims as abstract-level.
- No reliable source found on whether anyone has applied LoRA-tuned PLMs to the group's *specific* transporter-family tasks (glucose/sodium/vesicular/mitochondrial carriers). Absence of evidence here is weak evidence of absence — the transporter-family literature is thin and partly in low-visibility venues.
- SaProt/ProstT5 performance on transporter *family* classification (as opposed to binding residues) was not found.

## Q3. Candidate thesis directions: prior work and remaining gap

### Takeaway
The directions with the best novelty-per-effort ratio for a 4–6 month undergraduate thesis on Colab
Pro + Kaggle are (a) LoRA fine-tuning replacing frozen embeddings on one of the group's own tasks
with a rigorous re-evaluation, (b) a single multi-task model across the ligand types the group
published separately, and (c) a calibration/leakage audit of the group's own benchmark suite. Pure
structure-based GNN work and new structure-aware-PLM pretraining are poor fits on compute and on
the student's biology background.

### Cited Findings and gap analysis, direction by direction

**D1. LoRA/PEFT a PLM on a group task, vs their frozen-embedding mCNN baseline.**
Prior work: LoRA on ESM-2 for binding residues exists ([ESMBind/QBind](https://www.biorxiv.org/content/10.1101/2023.11.13.566930.full.pdf)); PEFT shown broadly beneficial ([Nature Comms 15:7407](https://www.nature.com/articles/s41467-024-51844-2)); SI-Tuning improves metal-ion binding with <2% tunable parameters ([Comput. Biol. Med.](https://www.sciencedirect.com/science/article/abs/pii/S0010482525009588)).
Remaining gap: nobody has asked whether PEFT makes the group's **window-scanning CNN head unnecessary** — i.e. is mCNN's gain just a cheap substitute for adapting the backbone? That is a clean, falsifiable research question ("does multi-window convolution still add anything once the PLM is LoRA-adapted?"), uses their published datasets and GitHub baselines, and needs only one small-to-mid PLM (ESM-2 150M/650M or ESM-C 300M fits Colab; [ESM-C 300M ≈ ESM2-650M at lower memory](https://www.evolutionaryscale.ai/blog/esm-cambrian)). Risk: LoRA itself is not novel, so the novelty must sit in the ablation and in a task where it has not been tried (e.g. FAD, NAD, vesicular/mitochondrial transporters).

**D2. One multi-task model across the ligands the group published one-by-one (ATP, FAD, NAD, Ca, metal).**
Prior work: GPSite already multi-tasks DNA/RNA/peptide/protein/ATP/HEM/metal with a shared GNN + per-ligand MLPs ([eLife 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11023698/)); MPBind multi-tasks five molecular classes with ProtTrans+ProstT5+EGNN ([Bioinformatics 2025](https://academic.oup.com/bioinformatics/article/41/11/btaf589/8300842)); LABind generalises by conditioning on the ligand ([Nat. Commun. 2025](https://www.nature.com/articles/s41467-025-62899-0)).
Remaining gap: the published multi-task models are **structure-based**. A sequence-only multi-task head over the group's own cofactor set (ATP/FAD/NAD — chemically related nucleotide cofactors, plus Ca/metal as a contrast) has not been done, and the cross-ligand transfer question ("does FAD data help NAD prediction?") is directly answerable with their public datasets. Strong fit: it unifies five of their papers, which flatters the advisor rather than threatening him.

**D3. Calibration / conformal prediction + leakage-aware re-evaluation of the group's benchmark suite.**
Prior work: conformal prediction for FDR-controlled enzyme annotation ([PLOS Comput. Biol. 2024](https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1012135)) and protein search ([Nat. Commun.](https://www.nature.com/articles/s41467-024-55676-y)); leakage critiques ([SpanSeq](https://arxiv.org/pdf/2402.14482); [pretraining leakage](https://www.biorxiv.org/content/10.1101/2024.07.23.604678v1.full); [interaction benchmarks](https://mlanthology.org/iclrw/2024/bushuiev2024iclrw-revealing/); [27–39% residue-level inflation](https://arxiv.org/pdf/2606.04228)).
Remaining gap: no one has applied conformal risk control to **transporter-family or cofactor-binding-site** prediction, and the group's own results (AUC up to 99.9% on 5–11%-positive residue data, [RAG-msCNN](https://doi.org/10.1016/j.bspc.2025.109407)) are exactly the kind of number a calibration study should interrogate. Cheapest direction on compute (reuses frozen embeddings; no backbone training). Risk: reads as a critique of the advisor's own papers — must be framed as "adding a reliability layer to our pipeline", with the group's models as the base predictors, not as debunking.

**D4. Learned / principled retrieval instead of the fixed α = 0.7 top-5 k-NN "RAG".**
Prior work: their own four RAG papers (RTK_RAG, RAG_MCNNIL6, RAG-msCNN, DEEPTRANS, plus the metal-binding EAAI paper) all use the same fixed-fusion recipe; the clearest documented mechanics are in [RAG-msCNN](https://doi.org/10.1016/j.bspc.2025.109407). Retrieval-augmented *classification* in the wider field normally learns the fusion (attention over retrieved neighbours) rather than fixing a scalar.
Remaining gap: (i) α and k are unablated across tasks; (ii) retrieval is applied **only to positive residues**, which is a train-time asymmetry that deserves scrutiny because at inference time the label is unknown — this is worth checking directly in their released code (github.com/mhb1717/RAG_DNA_RNA) as a possible evaluation flaw; (iii) replacing the fixed average with learned attention is a self-contained contribution. Highest "extends their pipeline" score of any direction; lowest biology requirement. Risk: if (ii) turns out to be a genuine leak, the thesis becomes awkward politically — handle as an ablation, not an accusation.

**D5. Structure-aware PLM embeddings (SaProt / ProstT5) as a drop-in for ProtTrans on transporter families.**
Prior work: [SaProt (ICLR 2024)](https://proceedings.iclr.cc/paper_files/paper/2024/file/1c42513b8895ab11fbbb5b7e8e6b6b02-Paper-Conference.pdf), [ProstT5](https://www.biorxiv.org/content/10.1101/2023.07.23.550085v1.full.pdf), [S-PLM](https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/advs.202404212); MPBind already uses ProstT5 with structure ([Bioinformatics 2025](https://academic.oup.com/bioinformatics/article/41/11/btaf589/8300842)); a 2025 paper already compares structure encodings vs sequence embeddings for transporter substrates ([*Molecules* 30:3226](https://doi.org/10.3390/molecules30153226)).
Remaining gap: the group's 2026 embedding baseline tables still stop at ProtTrans/ESM-2/TAPE, so "update the baseline" is real but is an incremental benchmarking contribution. Membrane transporters are a fair test case because AlphaFold/ESMFold confidence is uneven in transmembrane regions — and SirtSAGE already shows the group is interested in pLDDT as a gate. Compute risk: SaProt needs Foldseek 3Di tokens from structures, so the thesis depends on downloading AlphaFold DB entries rather than folding proteins itself; folding thousands of transporters on Colab is not feasible.

**D6. Motif-validated explainability (does the model find the Walker A / P-loop and the Rossmann-fold motifs?).**
Prior work: the group does SHAP/Grad-CAM/t-SNE but never checks attribution against annotated motifs ([msCNN-PLM-FAD](https://doi.org/10.1016/j.ab.2026.116092) maps SHAP onto a single structure, PDB 1O97, visually). The field now has sparse-autoencoder feature discovery aligned to known motifs ([MotifAE](https://pmc.ncbi.nlm.nih.gov/articles/PMC12637460/), [InterPLM](https://www.researchgate.net/publication/395958458_InterPLM_discovering_interpretable_features_in_protein_language_models_via_sparse_autoencoders)), concept activation vectors for motif localization ([arXiv 2511.21614](https://arxiv.org/pdf/2511.21614)), and the explicit warning that attribution without human/wet-lab grounding is not interpretability ([arXiv 2506.19532](https://arxiv.org/pdf/2506.19532)). The Walker A / P-loop motif GxxGxGK[T/S] is a well-defined, machine-checkable string for ATP tasks — [Walker motifs](https://en.wikipedia.org/wiki/Walker_motifs), [ATP-binding motif](https://en.wikipedia.org/wiki/ATP-binding_motif).
Remaining gap: a quantitative, motif-level audit of the group's own ATP/FAD/NAD models — "what fraction of top-attributed residues fall in annotated Walker A / Rossmann motifs, and is attribution better than a PROSITE-regex baseline?" — does not exist. Very low compute, moderate biology requirement (needs reading motif annotations from UniProt/PROSITE), and it converts their decorative SHAP figures into a measurable claim.

**D7. Few-shot / zero-shot family classification for rare transporter families.**
Prior work: [ProtNote](https://www.biorxiv.org/content/10.1101/2024.10.17.618952v1.full) (zero-shot GO/EC from text), [TooTranslator](https://www.biorxiv.org/content/10.1101/2025.11.13.688294.full.pdf) (zero-shot transporter substrates via protein-chemical embedding alignment), [TooT-SS](https://www.bio-conferences.org/articles/bioconf/pdf/2025/14/bioconf_icbbb2025_01001.pdf) (83/96 substrate classes, F1 0.92), [SPOT](https://journals.plos.org/plosbiology/article?id=10.1371%2Fjournal.pbio.3002807).
Remaining gap: the group's own answer to rare classes is ProtGPT2 augmentation (SMR with 18 sequences, [mCNN-GenEfflux](https://doi.org/10.1016/j.compbiolchem.2025.108595)). A head-to-head of **generative augmentation vs metric/contrastive few-shot learning** on their rare transporter families is unaddressed and is a genuinely interesting question (does synthesising sequences beat changing the loss?). Contrastive learning for protein-DNA binding already exists ([BIB 25:bbad488](https://academic.oup.com/bib/article/25/1/bbad488/7505238)), so the novelty must stay on the rare-family comparison, not on "we used contrastive loss".

### Inferences
- D1, D2, D4 and D6 all reuse the group's public datasets and GitHub code, which is what makes them 4–6-month feasible for a student with basic biology: the biology is already encoded in the benchmark.
- D3, D4 and D6 need essentially no GPU beyond one pass of embedding extraction, so they are the safest under a 45 GPU-hour/week budget. D1 needs LoRA training of a mid-size PLM, which fits; D5's dependence on structure files is the main logistical risk.
- A defensible combination for one thesis: pick one task family (ATP/FAD/NAD cofactor binding sites, where the group has three papers and public data), then do D1 (LoRA vs frozen) + D3 (AUPRC, calibration, leakage-aware split) + D6 (motif-level attribution audit). That is one coherent story — "what actually drives performance in PLM+mCNN binding-site prediction, and how reliable are the reported numbers" — rather than three disconnected tricks.

### Gaps
- Whether the group's released RAG code applies positive-only retrieval at inference time (the potential flaw behind D4) can only be settled by reading github.com/mhb1717/RAG_DNA_RNA; I did not fetch that repository.
- No source found quantifying how much LoRA helps specifically on *transporter family* classification, so D1's expected effect size on that subtask is unknown.

## Q4. Which directions an advisor in this group would likely welcome vs find risky

### Takeaway
This is an inference section: I found no public statement of either advisor's supervision preferences. The judgement below is read off their publication behaviour and the explicit design justifications in their papers.

### Cited Findings (behavioural evidence)
- They explicitly trade accuracy for compute: ESM-2 2560-dim had the best MCC in the RTK_RAG feature table (0.4235 vs ProtTrans 0.3181) but was rejected because it "demanded roughly twice the computational resources and time investment", and ProtTrans was called "the more balanced choice" — [RTK_RAG](https://doi.org/10.1021/acs.jcim.5c00766).
- They explicitly value parameter reduction: msCNN was introduced because separable convolutions "reduce the number of trainable parameters and improve model" efficiency — [RAG-msCNN](https://doi.org/10.1016/j.bspc.2025.109407).
- They do adopt new modules fast when they bolt onto the existing pipeline: RAG (2025, 5 papers), ProtGPT2 generation (2025–2026), KG-RAG (2026), GATv2 with pLDDT gating (SirtSAGE 2026) — all within two years, all keeping PLM embeddings as the input layer.
- They do use predicted structure when it is cheap context rather than the model's backbone: AlphaFold2 pLDDT/pTM to validate generated sequences ([mCNN-GenEfflux](https://doi.org/10.1016/j.compbiolchem.2025.108595)), ESMFold pLDDT to screen peptides ([NeoGen-BC](https://doi.org/10.1016/j.bbrc.2026.154567)), AlphaFold structural information for TRP channels (Disto-TRP 2023), pLDDT as a gate (SirtSAGE 2026).
- Publication venue pattern (JCIM, ACS Omega, Int. J. Biol. Macromol., Comput. Biol. Chem., Analytical Biochemistry, Biomed. Signal Process. Control) favours applied, benchmark-beating, biologically framed papers over methodological-critique papers.

### Inferences — likely welcomed
- **D2 (multi-task over their own ligand set)** and **D4 (better retrieval fusion)**: pure extensions of their pipelines, reuse their data, produce a new named model with a table of wins. Highest acceptance probability.
- **D1 (LoRA/PEFT)**: should land well *if* pitched as "same accuracy or better at a fraction of the memory", which matches their documented compute-consciousness. Pitched as "your frozen-embedding approach is outdated", it will not.
- **D6 (motif-validated attribution)**: they already invest in interpretability figures in every paper, so making them quantitative is an easy sell and gives a biology-flavoured results section, which their venues like.
- **D5 (SaProt/ProstT5 baseline refresh)**: plausible, and SirtSAGE shows appetite for structure-adjacent signals; but it is the kind of contribution a reviewer calls incremental unless paired with a real question.

### Inferences — likely seen as risky
- **D3 (calibration/leakage audit)** is methodologically the strongest and politically the weakest: its natural conclusion is that published AUCs in this literature — including theirs — are inflated. Mitigation: scope it as a new reliability layer on one task with the group's model as the base predictor, report AUPRC alongside (not instead of) AUC, and cite the group's own NeoGen-BC adoption of AUPRC as the precedent.
- **Full structure-based GNN work** (own ESMFold/AlphaFold folding at scale, equivariant GNNs à la MPBind) is risky on two counts: 45 GPU-hours/week does not cover folding plus training, and the group has only one in-house precedent (SirtSAGE), so supervision depth is thin.
- **New PLM pretraining or large-scale fine-tuning (ESM-2 3B, ESM3)** is out of budget; PEFT on ≤650M-parameter models is the ceiling.
- **Zero-shot/text-multimodal (D7 ProtNote-style)** requires an LLM text pipeline the group has only touched via KG-RAG; novelty is high but so is the chance of a null result within 4–6 months.

### Gaps
- No interview, lab page, or student-handbook source on either advisor's stated supervision preferences, thesis expectations for CT553H-scale work, or whether they require a publishable result. Everything in this section is inferred from publication behaviour and should be presented as inference, not fact.
- Dr. Ho's independent preferences (as distinct from Prof. Ou's) are hard to separate: his 2025–2026 bioinformatics output is co-authored with Ou except SirtSAGE, which is the one signal that his own line is moving toward graph/structure-gated models with Can Tho University students (Nguyen, Nguyen, Ly are CTU-affiliated co-authors on SirtSAGE and msCNN-PLM-FAD).
