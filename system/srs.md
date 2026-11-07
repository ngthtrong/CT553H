# Software Requirements Specification — Degron Footprint Tool

**v0.2, 29 Oct 2026.** First-release scope confirmed by the author; implementation and acceptance of the additions remain pending. Structure follows the requirements categories of the existing SRS. Thresholds marked *proposed* need local measurement. See [README.md](README.md) for the decision and evidence record.

## 1. Introduction

### 1.1 Purpose

Specify the local software delivered to researchers choosing mutations for follow-up experiments. This document supplies Chapter 1 requirements, Chapter 3 design and Chapter 4 acceptance scenarios of the [working thesis](../report/README.md).

### 1.2 Scope

One React + TypeScript / FastAPI web application running on the researcher's computer. Release 1 supports single-peptide prediction, peptide batches, whole-protein tiling, substitution ranking, ClinVar and approved reference annotations, project-specific experimental-data import/comparison, CSV/JSON export, and persistent projects and analysis history.

The prediction unit stays `(WT peptide, position, mutant amino acid)`, with 28-residue peptides and 532 substitutions. Whole-protein mode applies the same model to full windows (step 23), retaining each window's domain and context. It does not predict a validated whole-protein phenotype. The baseline model is frozen `m3-ext4.0-platt-v1`; the software scope does not assert that model selection or scientific validation is complete.

### 1.3 Out of scope

Public/remote deployment, hosting/VPS/TLS and availability SLAs; public sharing; accounts, multi-user collaboration and tenant isolation; wet-lab execution or sample management; automatic training or incorporation of imported observations into the research benchmark; specific E3 identification, disease/therapy inference, multi-mutant effects and new validated assay/species domains; native mobile/desktop editions. Non-human or unverified custom sequences cannot be represented as validated human-domain predictions.

### 1.4 Definitions

| Term | Meaning |
|---|---|
| PSI / ΔPSI | GPS stability index / PSI(mutant) − PSI(WT); positive ΔPSI means greater reporter stability in this assay |
| Tile / cell | Full 28-residue window, step 23 / one non-WT substitution (532 per tile) |
| Calibrated probability | Estimate of P(ΔPSI ≥ 1.0) in the model's assay/domain; separate from the raw regression score |
| Project | Named workspace containing saved runs, batch jobs and imported datasets |
| Run snapshot | Immutable input, model/calibrator hashes, scores, warnings, annotation/dataset versions and timestamps |
| History | Chronological saved runs in a project; reopening reads the snapshot, rerunning creates a new run |
| Batch job | Durable bounded request with per-tile outcomes and progress |
| Imported dataset | User-provided observations plus assay, units, replicate/reference metadata and file hash, kept separately from reference/training data |
| Provenance | Input and model identity, data/source versions, mapping and domain evidence, code/configuration and generation time |

## 2. Overall description

### 2.1 Product perspective

Browser SPA → local REST API → inference/reference data and project storage. A local worker executes durable jobs; PostgreSQL holds metadata and results, and a workspace directory holds committed source files. Reference ETL and research training remain separate offline processes. SQLite supports baseline development and isolated tests; there is one accepted local product configuration.

### 2.2 Stakeholders

Researchers need a ranked, traceable shortlist and comparison with their measurements. Computational researchers need structured exports. The author maintains the model/data and local software; the supervisor evaluates evidence and scope. The local workspace has one trusted operator, with no account/permission model.

### 2.3 Assumptions and dependencies

* Model evidence is the development benchmark recorded in the calibration research, not independent validation. No numerical scientific result is changed here.
* The supported effect model takes 28-residue internal peptides; processing a protein does not extend this domain.
* R3 domain-gate results exist, but baseline integration is incomplete. Do not apply intrinsic PSI(WT) ≤ 4.0 directly to screen PSI; implement the frozen gate rules and `borderline` state consistently before acceptance.
* Reference snapshots (UniProt, Zhang GPS/saturation, ClinVar) are prepared locally. Runtime prediction/import does not send user data to third-party APIs.
* ClinVar mapping requires accession/reference release, protein position and WT agreement. Custom inputs lacking a verified mapping show annotations as unavailable.
* User observations may be missing, contradictory or assay-incompatible. Import and comparison must expose these states.

### 2.4 Constraints

| ID | Constraint |
|---|---|
| CON-1 | Serve only approved reference sources with recorded licence and redistribution permission; keep blocked sources out of reference ETL/model. Private imports do not become reference sources. |
| CON-2 | ClinVar displays and exports include source version, attribution and diagnostic disclaimer. |
| CON-3 | Preserve evidence labels; imported measurements are not automatically independent validation. |
| CON-4 | One developer and thesis schedule; no new wet-lab experiments are required. |
| CON-5 | Local inference runs on CPU; model training is outside the application. |
| CON-6 | Single previews are transient unless saved. Project saves/job submissions/import commits explicitly persist data locally until deletion. No sequences or imported observations in logs. |
| CON-7 | React + TypeScript (Vite), FastAPI, local PostgreSQL; SQLite only for baseline development/tests. Docker may package this same local application. |
| CON-8 | One loopback-only instance; no public deployment or public sharing acceptance requirement. |

## 3. Use cases

All UC-01…10 are in release 1. Actor: local researcher. UC-01…07 extend the existing baseline; UC-08…10 are planned additions. FR-20 public sharing is retired rather than reused for persistence.

### UC-01 Predict the effect matrix

Enter a 28-residue sequence or choose a tile; validate syntax and domain; compute 532 effects; show domain/warnings before matrix and ranking. Invalid input produces a specific error and no scores. Known out-of-domain tiles are refused by default; explicit override is recorded. Unknown, unreliable and borderline domains are labelled prominently. A preview is transient; saving creates a project run snapshot (UC-10).

### UC-02 Rank substitutions

Sort and filter substitutions within each tile; mark top 10% and select a shortlist. Batch/protein views preserve tile identity and do not imply calibrated cross-tile biological comparability. An empty filter has an explicit empty state.

### UC-03 Export results with provenance

Export one run or job as CSV/JSON, including per-item status, tile and protein coordinates, warnings, selected annotation/dataset versions and the model identity. Failed/skipped items remain in a job manifest. Export failure preserves the saved/on-screen result. No public share link is required.

### UC-04 Select a protein and tiles

Search the loaded human UniProt release by gene/accession; show full tiles and domain status. Select one tile or submit the whole protein to UC-08. Proteins shorter than 28, non-standard residues, unverified mappings and uncovered terminal residues are reported explicitly.

### UC-05 Compare with measured data

Choose reference measurements or a committed project dataset (UC-09). Align by exact WT peptide, position and substitution, with accession/release checks when supplied. Show prediction, observation and residual side by side only when units/endpoint are comparable. Label training observations. For other assays show separately labelled values without pooled ΔPSI metrics. Missing values are not zero. Report matched/unmatched/conflicting row counts and metric sample sizes.

### UC-06 View ClinVar and approved reference annotations

Show mapped missense variants with classification, review/conflict status, source identifiers and snapshot date; retain source links and attribution. UniProt sequence mapping and GPS reference evidence provide context. Distinguish no match, mapping unavailable and source not loaded. Annotation absence does not mean benign, and classification is not inferred from ΔPSI. New external annotation integrations require a named, approved source contract.

### UC-07 View model and data provenance

Read the frozen model card, event definition, assay/domain, benchmark evidence, source versions/licences and known limitations. Historical runs retain their own snapshots even when the current model/source changes.

### UC-08 Analyse peptide batches or a whole protein

Select a project, then submit a list/multi-record FASTA of 28-residue peptides or one protein accession/single-record protein FASTA. Preview normalised inputs, tile count, coverage gaps and limits; confirm local persistence and submit. A durable job pins model/gate/source versions. Show pending/running/completed/partial/failed/cancelled states, counts and per-tile results; allow cancellation. Restart recovers unfinished work without duplicate completed runs. Invalid or refused items do not erase successful items. Each scored tile matches UC-01. Overlapping substitutions keep distinct tile-context identifiers.

### UC-09 Import experimental observations

Select a project and upload CSV/TSV. Supply dataset name, assay, units, source/reference and replicate metadata. Preview schema, coordinates, WT agreement, duplicates/conflicts and missing values. Blocking errors prevent commit; warnings and unmatched rows are shown. Explicit commit stores an immutable dataset revision and file hash. Compare via UC-05. No script execution, research-data overwrite, automatic averaging or retraining.

### UC-10 Manage projects and history

Create/rename a project; explicitly save a preview, submit a job or commit a dataset; list chronological runs and reopen snapshots after application restart. Reruns create new entries. Delete a dataset, run or project with a dependency summary and explicit confirmation. Deletion removes owned files/results and comparison dependencies; shared reference/model data remain intact. There are no accounts, cross-user sharing or automatic 30-day expiry for project history.

## 4. Functional requirements

M = mandatory first release; S = useful refinement; retired = no longer an acceptance requirement. Test IDs are defined in [test-plan.md](test-plan.md).

| ID | Requirement | UC | Priority | Verify |
|---|---|---|---|---|
| FR-01 | Accept exactly 28 standard amino acids for peptide input, normalising case and surrounding whitespace. | 01 | M | UT-07, API-01 |
| FR-02 | Accept a loaded UniProt accession and a 1-based tile index. | 01,04 | M | API-02 |
| FR-03 | Reject invalid input with a field-specific coded error, without scores for that item. | 01,08,09 | M | PB-02, BATCH-01, IMP-01 |
| FR-04 | Compute 532 non-WT substitution scores per valid scored tile. | 01,08 | M | RG-01, BATCH-02 |
| FR-05 | Distinguish raw score from calibrated P(ΔPSI ≥ 1.0); state the event next to probabilities. | 01 | M | UT-03, E2E-12 |
| FR-06 | Render a 28-position × 20-letter grid with WT cells masked and 532 scored cells. | 01 | M | E2E-01 |
| FR-07 | Provide sortable/filterable ranking and shortlist selection within each tile. | 02 | M | E2E-02 |
| FR-08 | Flag the top 10% by within-tile rank. | 02 | S | UT-04 |
| FR-09 | Attach measured/predicted/unknown/unreliable/borderline domain evidence to each tile; freeze the gate identity/rules per run. | 01,08 | M | DOM-01 |
| FR-10 | Refuse known out-of-domain scoring unless explicitly overridden, recording the warning. | 01,08 | M | E2E-09, BATCH-03 |
| FR-11 | Show uncertain/predicted/override warnings before scores and carry them into saved/exported results. | 01,08 | M | E2E-12 |
| FR-12 | Export single-tile CSV with the baseline nine score columns and provenance. | 03 | M | RG-02 |
| FR-13 | Export complete prediction/provenance JSON. | 03 | M | API-31 |
| FR-14 | Record model/hash, event, evidence, domain/gate, source/configuration/code versions and timestamps. | 01,03,07,10 | M | API-01, HIST-02 |
| FR-15 | Search loaded human proteins by gene/accession. | 04 | M | E2E-04 |
| FR-16 | List full tiles with 1-based protein coordinates and domain status. | 04,08 | M | UT-05, BATCH-04 |
| FR-17 | Compare reference and imported observations with predictions, keeping their training/assay/source labels. | 05,09 | M | E2E-05, IMP-03 |
| FR-18 | Provide ClinVar missense annotations, source versions, mapping/review/conflict states and attribution. | 06 | M | E2E-06, ANN-01 |
| FR-19 | Provide the model card and its evidence/limitations. | 07 | M | E2E-07 |
| FR-20 | Legacy expiring public share-link requirement. Retired in v0.2; legacy endpoints are not project history. | — | retired | Legacy only |
| FR-21 | List approved reference sources, versions, licences and attribution. | 07 | M | E2E-07 |
| FR-22 | Use a frozen model registry; keep historical snapshots tied to their original model. | 01,07,10 | M | UT-09, HIST-02 |
| FR-23 | Preserve results when export/download fails and allow retry. | 03 | M | E2E-10 |
| FR-24 | Accept bounded peptide batches with stable input/item identifiers and a validation preview. | 08 | M | BATCH-01 |
| FR-25 | Tile one complete reference protein; report uncovered residues, invalid windows and mapping limits, without merging overlapping contexts. | 04,08 | M | BATCH-04 |
| FR-26 | Persist job progress, per-item success/refusal/error, cancellation and restart recovery. | 08 | M | BATCH-03, BATCH-05 |
| FR-27 | Pin model/calibrator/gate/source versions on submission and save immutable completed run snapshots. | 08,10 | M | BATCH-02, HIST-02 |
| FR-28 | Preview CSV/TSV imports with assay/units/replicate/reference metadata; block malformed/conflicting records before commit. | 09 | M | IMP-01, IMP-02 |
| FR-29 | Align observations using WT sequence, position and substitution; verify supplied accession/release and WT residue. | 05,09 | M | IMP-03 |
| FR-30 | Keep incompatible endpoints separate; calculate residuals/MAE/Spearman only on comparable matched observations with n and explicit replicate selection. | 05 | M | IMP-04 |
| FR-31 | Create, rename, list and reopen local projects. | 10 | M | HIST-01 |
| FR-32 | Save/list/reopen analysis history across restart; rerun creates a new entry and never overwrites history. | 10 | M | HIST-02 |
| FR-33 | Confirm deletion with dependency summary and remove owned rows/files; retain shared reference/model data. | 09,10 | M | HIST-03 |
| FR-34 | Export batch manifest and annotated/comparison tables with item status, context coordinates and snapshot provenance. | 03,05,06,08 | M | BATCH-06, IMP-04, ANN-01 |
| FR-35 | Show UniProt mapping/GPS evidence alongside ClinVar, retaining independent source/mapping states. | 06 | M | ANN-01 |
| FR-36 | Enforce configured file/item/residue limits and paginate results without truncation disguised as completion. | 08,09,10 | M | BATCH-01, IMP-01, NF-07 |

## 5. Non-functional requirements

Local performance numbers below are **proposed targets, not measurements**. Record the actual computer, database sizes, batch/import sizes, sample counts and date. Do not substitute VPS measurements or historical single-tile tests for v0.2 acceptance.

| ID | Category | Requirement / target | Verify |
|---|---|---|---|
| NFR-01 | Performance | Single-tile server p95 ≤ 300 ms, proposed on recorded local CPU. | NF-01 |
| NFR-02 | Performance | List a 1,000-residue protein's tiles p95 ≤ 200 ms, proposed. | NF-02 |
| NFR-03 | Usability | Single-tile click-to-heatmap p95 ≤ 1.5 s; job progress remains responsive, proposed. | NF-06, NF-07 |
| NFR-04 | Correctness | API/runner difference < 1e-9 JSON, < 5e-9 ten-digit CSV. | RG-01, RG-02 |
| NFR-05 | Reproducibility | Same normalised input and frozen configuration give identical score arrays; timestamps/IDs can differ. | PB-03, BATCH-02 |
| NFR-06 | Integrity | Hash mismatch prevents scoring and marks health not ready. | UT-09, DEP-01 |
| NFR-07 | Resource bounds | Proposed defaults: 4 KiB single request; 1 MiB batch JSON, 100 peptides or one protein ≤ 10,000 residues; 10 MiB import and 100,000 rows; ≤ 200 paginated items/page. Rate/concurrency bounds are configured and tested locally. | NF-04, NF-05, NF-07 |
| NFR-08 | Input safety | Never execute imported content or interpolate input into paths/SQL; neutralise spreadsheet formula text in CSV exports. | SEC-02, IMP-01 |
| NFR-09 | Privacy | No sequences/observations in logs, URLs or telemetry; explicit persistence for saved projects/jobs/imports. | SEC-01, HIST-01 |
| NFR-10 | Retention | Saved work survives restart until user deletion; deletion cascades to owned files/results. Pending import previews expire and are never mistaken for committed datasets. | HIST-02, HIST-03, IMP-02 |
| NFR-11 | Accessibility | WCAG 2.1 AA target, keyboard paths and non-colour cues. | A11Y-01…04 |
| NFR-12 | Compatibility | Local desktop browser is primary; verify Chromium, Firefox/WebKit and responsive table fallback at 360 px. | E2E matrix |
| NFR-13 | Data rights | Reference licence gates and project-import isolation apply independently. | ETL-03, IMP-02 |
| NFR-14 | Attribution | ClinVar attribution/disclaimer on annotated views and exports. | ANN-01, E2E-06 |
| NFR-15 | Scientific limits | Every score result/export carries domain, event and development-evidence labels; comparison does not claim clinical validity. | E2E-12, IMP-04 |
| NFR-16 | Maintainability | Versioned schema migrations, documented local API/worker/frontend start; no cloud orchestration requirement. | DEP-01 |
| NFR-17 | Verification | Automated tests and recorded coverage; ≥ 85% backend line coverage is a proposed target, not a substitute for acceptance cases. | Local test report |
| NFR-18 | Resources | Record peak API/worker/browser memory and disk growth under representative jobs/imports; 512 MB API-only is a proposed baseline target, excluding DB/worker. | NF-03, NF-07 |
| NFR-19 | Observability | Request/job IDs, counts/status/duration in structured logs; no biological payload. | SEC-01, BATCH-05 |
| NFR-20 | Local installation | Clean-checkout installation, reference preparation and UC-01…10 on one local instance; no external deployment test. | DEP-01, DEP-02 |

## 6. Data and interfaces

[db-design.md](db-design.md) distinguishes baseline DDL from the planned workspace migration. [openapi.yaml](openapi.yaml) distinguishes baseline and `planned` operations; a planned contract is not an executable feature. [api-spec.md](api-spec.md) defines import schema, jobs, retention and exports. [ui-design.md](ui-design.md) defines the local screens. Reference ETL is idempotent and provenance-checked; project imports never write `data/` or alter weights.

## 7. Verification and traceability

The FR/NFR tables provide requirement → UC → test links; [test-plan.md](test-plan.md) defines each test ID and expected outcome. A requirement is verified only with a dated result and environment. Historical baseline cases are evidence for their original scope only. Back-to-back tests demonstrate consistency, not independent scientific validation.

## 8. Risks and handling

| ID | Risk | Handling |
|---|---|---|
| R-1 | Shared model/label error survives numerical agreement | Independent feature checks and separate scientific evaluation |
| R-2 | ClinVar or probability is read as a disease prediction | Event/annotation separation and diagnostic disclaimer |
| R-3 | Whole-protein display hides out-of-domain or unscored regions | Per-tile domain and coverage manifest; no silent averaging |
| R-4 | Batches/history fill local disk or block the browser | Bounded durable jobs, cancellation, paging and explicit deletion |
| R-5 | Import confuses incompatible assays or training observations with validation | Metadata/WT checks, endpoint-specific comparisons, no automatic training |
| R-6 | Old snapshots change when sources/models are updated | Immutable snapshots and explicit reruns |
