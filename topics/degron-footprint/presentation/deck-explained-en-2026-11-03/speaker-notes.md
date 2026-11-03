# Speaker notes

## 1. RESIDUE-LEVEL DEGRON MUTATION EFFECT PREDICTION AND ANALYSIS TOOL

This presentation explains the project from biological foundations to machine learning research and software. The opening matrix illustrates the experimental design; it is not an inference result. The target is the effect of a single amino acid substitution on reporter stability.

Sources: https://pubmed.ncbi.nlm.nih.gov/37738965/, research/README.md

## 2. A protein is built from an amino acid sequence

The GIF is a predicted Fam188a structure model by Nikolakhs, licensed CC BY-SA 3.0. It is not HIF1A or a structure of the assayed degron. The eight-amino-acid sequence is hypothetical. The core prediction task uses 28-residue peptides.

Sources: https://commons.wikimedia.org/wiki/File:I-TASSER_predicted_protein_fold_of_Fam188a.gif

## 3. Degrons help direct protein degradation

The schematic simplifies the ubiquitin–proteasome system and does not cover all degradation mechanisms. E3 ligases and the appropriate machinery contribute to substrate recognition. NIGMS movie 3764 by Andreas Martin/HHMI simulates a ubiquitin-tagged substrate being unfolded by the AAA+ motor; ubiquitin is removed before substrate cleavage. This is a molecular simulation, not an observation from the Zhang dataset. Molecular colors in the movie follow its authors' conventions.

Sources: https://www.nigms.nih.gov/image-gallery/3764, https://www.nigms.nih.gov/image-gallery, https://pubmed.ncbi.nlm.nih.gov/37738965/

## 4. One substitution can change the signal

Hypothetical example: MAGLSKVT becomes MAGPSKVT through L4P. A substitution may alter degron activity, act through another mechanism, or have little effect. This particular L-to-P example is not attributed to a measured degron.

Sources: https://pubmed.ncbi.nlm.nih.gov/37738965/

## 5. 532 substitutions motivate experimental prioritization

28 positions multiplied by 19 non-WT amino acids gives at most 532 single substitutions. The matrix has 20 amino acid rows, with WT-to-WT cells masked. A peptide can have at most 532 valid measured cells after QC. The figure illustrates the design, not experimental labels or model predictions.

Sources: research/kaggle-roadmap-2026-10-31/dataset-build.json

## 6. GPS converts fluorescence signals into PSI

GFP is fused to the peptide and DsRed provides a reference signal. Cells are sorted into six bins by GFP/DsRed ratio, followed by sequencing to count constructs. PSI is a weighted average of bin scores after normalization. The Zhang assay uses a scale from 1 to 6. The illustrated histogram heights are not experimental measurements.

Sources: https://pubmed.ncbi.nlm.nih.gov/37738965/, research/full-data-audit/psi-build.json

## 7. ΔPSI is the effect the model aims to predict

ΔPSI = PSI(mutant) − PSI(WT). A positive value means that the mutant reporter is more stable in this assay. This can be consistent with a weakened degron, but it does not establish the mechanism. It does not directly quantify half-life, whole-protein effects or pathogenicity. The values 2.5 and 3.8 are hypothetical.

Sources: https://pubmed.ncbi.nlm.nih.gov/37738965/

## 8. Saturation and scanning provide complementary coverage

The scanning replacement depends on the WT amino acid and follows the R/A/S design. Across the alphabet this yields 20 directed WT-to-mutant types among 380 nonsynonymous types. Saturation can assay 19 replacements per position when coverage is complete. Assayed cells do not necessarily all pass QC.

Sources: https://pubmed.ncbi.nlm.nih.gov/37738965/, research/scan-sat-merge-2026-10-23/README.md

## 9. Each mutation cell becomes a labeled data record

A mutation cell is identified by peptide, position, WT and mutant amino acids; it is not an independent protein. Scanning uses mut0 from the corresponding replicate. Saturation has no mut0: its intrinsic WT reference is the median of valid synonymous cells within each experimental half. BAG6 WT must not be treated as a saturation reference or an extra replicate.

Sources: research/kaggle-roadmap-2026-10-31/dataset-build.json, research/full-data-audit/saturation-matrix.json

## 10. The QC-filtered data retain the full PSI range

Counts are read from dataset-build.json: 122,412 saturation cells, 235 saturation peptides, 221 saturation groups and 224,470 scanning cells. The scanning count covers all QC-filtered cells, not only pretraining data. scan_dev, scan_T and sat_overlap serve distinct roles. The presentation reports the data directly without a version-by-version comparison.

Sources: research/kaggle-roadmap-2026-10-31/dataset-build.json

## 11. The pipeline connects data, models and the analysis tool

This diagram provides a roadmap for the presentation. Models and comparisons from the development benchmark do not automatically become serving models. Recipe locking, calibration, evaluation on T and external validation remain unfinished in the documented snapshot.

Sources: research/kaggle-roadmap-2026-10-31/dataset-build.json, research/README.md

## 12. Sequences are inputs; PSI measurements define the labels

The main inputs are the WT sequence, mutation position and replacement amino acid. WT/mutant PSI, read counts, group/fold IDs and strata are excluded from the main feature set. Computing ΔPSI from measurements constructs the training label; those measurements are not supplied at inference.

Sources: research/kaggle-roadmap-2026-10-31/degron_v3/features.py, research/kaggle-roadmap-2026-10-31/dataset-build.json

## 13. Keep protein groups intact when splitting the data

Splits keep similarity groups intact and block duplicate sequences across scanning and saturation. Within each outer fold, tuning and preprocessing use only inner training/validation data. The selected setup is then refitted on outer training data and evaluated on outer test groups. Seeds are 17, 29 and 43. Confidence intervals resample the 221 protein groups. Heuristic grouping does not establish absolute biological independence.

Sources: research/kaggle-roadmap-2026-10-31/dataset-build.json, research/kaggle-roadmap-2026-10-31/EXECUTION-PROTOCOL.md

## 14. Ridge tests the predictive value of sequence context

An ordered context radius of 5 produces 40 WT/mutant one-hot features, 20 composition features and 200 ordered-neighbor features: 260 in total. Mutation position is used to extract context rather than supplied as a separate numeric column. Ridge regularization constrains large weights. Deep learning is not assumed to outperform Ridge.

Sources: research/kaggle-roadmap-2026-10-31/degron_v3/features.py, research/kaggle-roadmap-2026-10-31/output-analysis.json

## 15. A one-hot CNN learns local sequence patterns

The implemented head uses a 15-position crop, 20 one-hot channels, a center indicator and 60 substitution/composition features. The CNN kernel size is 5. This provides a control from the same head family without ESM differences. The drawing is a simplified conceptual illustration.

Sources: research/kaggle-roadmap-2026-10-31/degron_v3/neural.py, research/kaggle-roadmap-2026-10-31/degron_v3/features.py

## 16. ESM2 converts sequences into numeric representations

WT and mutant pass through the same pretrained ESM2 encoder; ΔH = H_mutant − H_WT. The CNN head uses a site-centered crop and projection together with WT one-hot features, a center indicator and 60 auxiliary features. Embedding dimensions are not directly measured biological quantities. The benchmark shown here covers ESM2-35M only.

Sources: research/kaggle-roadmap-2026-10-31/degron_v3/neural.py, research/kaggle-roadmap-2026-10-31/output-analysis.json

## 17. Pointwise and CNN heads differ in position mixing

The pointwise head uses Conv1D with kernel size 1; the CNN uses kernel size 5. Both also use max pooling and center pooling, so pointwise does not mean that the complete model ignores every other position. Head parameter counts differ. The comparison therefore does not fully isolate position mixing from model capacity. Auxiliary inputs are consistent across heads.

Sources: research/kaggle-roadmap-2026-10-31/degron_v3/neural.py, research/kaggle-roadmap-2026-10-31/output-analysis.json

## 18. mCNN explores multiple context widths

Each branch applies convolution, activation, max pooling and center pooling. Branch features are concatenated with auxiliary features before the regression head. This architecture is being compared experimentally; the design itself is not evidence that multiple kernels outperform a single kernel.

Sources: research/kaggle-roadmap-2026-10-31/degron_v3/neural.py

## 19. Frozen and LoRA update different parameters

Frozen training updates only the head. LoRA retains the base backbone weights and trains low-rank adapters together with the head. This fine-tuning branch is separate from CNN training on cached representations. In the Kaggle snapshot, only frozen seed 17 was complete; LoRA OOF results were incomplete. A complete matched LoRA-versus-frozen comparison is not available.

Sources: research/kaggle-roadmap-2026-10-31/output-analysis.json, research/README.md

## 20. Error, ranking and confidence intervals answer different questions

MAE is macro-averaged over 235 peptides. Positive-event AUROC/AP use 184 peptides with at least three cells in each class. These are not accuracy scores, and AP depends on event prevalence. The 5,000 bootstrap resamples are drawn by protein group, not by treating all 122,412 cells as independent. MAE addresses the main regression task; AUROC addresses a supplementary event-ranking task. Confidence intervals describe metric differences, not per-mutation probabilities.

Sources: research/kaggle-roadmap-2026-10-31/output-analysis.json

## 21. Experiment A: which PSI range should be used for training?

The protocol names the configurations A/B/C/D/E; the slides use readable training-scope labels. The W evaluation set contains 235 peptides in 221 groups. PSI thresholds of 3, 4 or 5 are training-scope choices, not definitive degron/non-degron labels. Balancing changes training weights without changing the test population.

Sources: research/kaggle-roadmap-2026-10-31/output-analysis.json, research/kaggle-roadmap-2026-10-31/dataset-build.json

## 22. Full-range training reduces Ridge regression error

Both English plots use the same saved data as the Vietnamese figures. Full-range minus PSI≤4 training has a 97.5% confidence interval adjusted for the two main comparisons. It supports improvement but does not establish a reduction of at least 0.02 PSI across the full interval. Balancing helps high-PSI strata but involves trade-offs at low PSI. The PSI>5 stratum has no eligible positive events with ΔPSI≥1, so positive-event AUROC is undefined.

Sources: research/kaggle-roadmap-2026-10-31/output-analysis.json

## 23. Experiment B: what do ESM2 and CNN add?

The main MAE values are 0.4078 for Ridge, 0.3897 for pointwise, 0.3844 for CNN, 0.3850 for mCNN and 0.3838 for balanced mCNN. The first four rows use full-range training; the last changes weighting. Positive-event AUROC values are approximately 0.8319, 0.8375, 0.8488, 0.8463 and 0.8470. Buttons change the metric. The PDF shows the static MAE chart. These are development results, not locked-T results or serving-model acceptance.

Sources: research/kaggle-roadmap-2026-10-31/output-analysis.json

## 24. Small differences need confidence intervals

Direct comparison of balanced mCNN with full-range CNN: MAE difference −0.0005076313196522603; descriptive 95% CI [−0.003157472974124294, +0.0022234273088492414], using 5,000 protein-group bootstrap resamples. Both architecture and training weights differ. With the same full-range training, the mCNN–CNN difference is also unresolved. Intervals outside the primary training-range contrasts are descriptive and do not adjust for the full recipe-selection process.

Sources: research/kaggle-roadmap-2026-10-31/output-analysis-details.json, research/kaggle-roadmap-2026-10-31/output-analysis.json

## 25. Experiment C: open questions about transfer learning

Scanning-replicate-1 pretraining reduces one-hot CNN MAE by about 0.006385 relative to scratch training; descriptive 95% CI [−0.009929, −0.003013]. These are saturation OOF results, not ESM-plus-scanning or locked-T validation. Averaging replicates has not clearly beaten replicate 1, and the current quality-weighting recipe has a negative result. LoRA remains incomplete. Local runtime or ongoing local results are not pooled into the Kaggle benchmark.

Sources: research/kaggle-roadmap-2026-10-31/output-analysis.json, research/kaggle-roadmap-2026-10-31/output-analysis-details.json

## 26. The effect map supports experimental prioritization

The cells and bars illustrate the workflow rather than actual inference scores. The tool needs model/source versions and applicability information. ΔPSI should not be interpreted as disease probability or proof of an E3 mechanism. Event probabilities, if provided, require model-specific calibration and evaluation.

Sources: system/README.md

## 27. The serving baseline and UI prototype have different roles

The screenshot is reused from the Workspace UI prototype with synthetic fixtures. It is not the React baseline or real inference. PostgreSQL, persistent projects/history, durable batch jobs, whole-protein web tiling and experimental import/comparison remain to be implemented or validated. The serving model remains m3-ext4.0-platt-v1. Baseline test records are historical and were not rerun for this presentation.

Sources: system/README.md, system/design/workspace-ui-v2/README.md

## 28. What is available and what remains unfinished

The Kaggle snapshot was updated on 1 Nov at 11:18:07 UTC and analyzed on 2 Nov. The local record from 3 Nov at 12:38 UTC+8 lists 456 inherited completed work units, 178 pending units and one paused LoRA checkpoint. These are progress records, not proof of a live worker or 635 independent experiments. Job status is not a benchmark result. G2/G3 remain open.

Sources: research/README.md, system/README.md

## 29. Contributions should be grounded in inspectable evidence

These are contribution areas under development. Data/benchmarks and development results exist, while final validation and the extended software remain unfinished. The project does not claim a new architecture, generalization to all proteins or exclusive novelty from building a website.

Sources: research/kaggle-roadmap-2026-10-31/output-analysis.json, system/README.md

## 30. Lock and validate the model before integration

The final-promotion stage currently supports context Ridge; CNN needs its own final refit and export. Lock the recipe and calibration before evaluating T. T partitions have different exposure histories across designs and should be described accurately as held-source evaluation. External sources require endpoint and provenance checks. Model research and software work can progress in parallel.

Sources: research/kaggle-roadmap-2026-10-31/EXECUTION-PROTOCOL.md, system/README.md

## 31. From a sequence to a testable hypothesis

Connect biology, experimental labels, sequence-only inputs, group-based evaluation and the analysis tool. Available evidence supports further study of ESM2 with CNN, but does not establish independent validation across all sources or a completed product.

Sources: research/kaggle-roadmap-2026-10-31/output-analysis.json, system/README.md

## 32. Key terms used in this presentation

These definitions explain the presentation. A confidence interval for an aggregate metric is not a prediction interval for each mutation. PSI is not half-life, and ΔPSI is not disease probability.

Sources: https://pubmed.ncbi.nlm.nih.gov/37738965/, research/kaggle-roadmap-2026-10-31/output-analysis.json

## 33. From read counts to ΔPSI: use the correct WT reference

Do not substitute unnormalized raw bin counts into the PSI formula. The source pipeline normalizes by bin/condition; the stored audit reconstructed 261,865 values within 5×10^-7 of the authors' values. Saturation QC requires at least 10 reads, at least 10 valid synonymous cells per half and valid mutation measurements in both halves. WT references differ between saturation and scanning; BAG6 WT is a different condition. This presentation describes the existing audit without rerunning raw-data processing.

Sources: research/full-data-audit/psi-build.json, research/full-data-audit/saturation-matrix.json, research/kaggle-roadmap-2026-10-31/dataset-build.json

## 34. HIF1A example: reading an experimental effect map

Peptide Q16665_HIF1A_25 spans protein positions 553–580 and has intrinsic WT PSI 2.1865. It has 529 measured substitution cells, including 186 with ΔPSI≥1. The example was selected among peptides with at least 500 cells by the largest positive-cell count, with ID as a tie-breaker. The figure shows experimental labels, not new inference or a newly discovered HIF1A/VHL mechanism. WT and missing cells are masked; missing values are not filled with zero.

Sources: research/slide-figures-2026-10-15/example-matrix.json

## 35. Results and units of evaluation

Metrics are macro-averaged by peptide. The positive event is ΔPSI≥1; eligible peptides need at least three cells in each class. These are development OOF results. AUROC values from different cohorts are not directly comparable. The balanced-mCNN minus full-range-CNN MAE CI is [−0.003157, +0.002223]. CNN minus pointwise has CI [−0.010173, −0.000899], but head capacities differ.

Sources: research/kaggle-roadmap-2026-10-31/output-analysis.json, research/kaggle-roadmap-2026-10-31/output-analysis-details.json

## 36. Sources and evidence can be explored by topic

Author-reported evidence, measured labels, illustrations, fixtures and proposals are distinguished. Assets and data sources have hashes in evidence.json. PAP/Degformer audits and R0–R6 are historical and use different populations or protocols; their AUROCs should not be joined into a progress curve or compared directly with W. The paper has a Figure 2A erratum, DOI 10.1016/j.molcel.2023.10.021; that figure is not used here. Data versions are not part of the on-slide narrative.

Sources: https://pubmed.ncbi.nlm.nih.gov/37738965/, research/README.md, asset-notices.md
