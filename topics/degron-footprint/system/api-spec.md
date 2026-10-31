# API Specification

**v0.2 design, 29 Oct 2026.** One loopback-only local application. [openapi.yaml](openapi.yaml) preserves baseline operations and adds planned project/job/import operations with `x-implementation-status: planned`. The baseline backend has not gained these operations in this documentation update. Public sharing is deprecated and outside acceptance. See [srs.md](srs.md) for the accepted scope.

## 1. Conventions and local access

* Base `/v1`, JSON UTF-8, `snake_case`, RFC 3339 UTC. Exports support CSV/JSON.
* Bind API/worker/frontend services to loopback. One trusted local workspace, no login/accounts. Require JSON content type and exact configured loopback origin for browser mutations; no permissive CORS. The absence of accounts is not permission to expose the API remotely.
* `position` is 1-based within a tile; protein coordinates are separate. A scored tile contains 532 non-WT cells, position ascending then alphabet `ACDEFGHIKLMNPQRSTVWY` excluding WT.
* `X-Request-Id` on responses. `Cache-Control: no-store` for input/results. IDs, not biological sequences, appear in project/job routes. No user data in URLs, access logs or third-party requests.
* Preview requests are transient. Saving a preview, submitting a job and committing an import are explicit local-persistence operations, shown as such in the UI.
* Proposed limits are SRS NFR-07. Single-tile limits do not apply to imports/batches. Settings and actual accepted sizes are recorded with the local test environment.

## 2. Operations and implementation boundary

| Method | Path | Role | Status |
|---|---|---|---|
| POST | `/v1/predict`, `/v1/export` | Single-tile preview/export, UC-01…03 | Baseline |
| GET | `/v1/proteins`, `/v1/proteins/{uniprot_id}/tiles` | Search and tile selection, UC-04 | Baseline |
| GET | `/v1/proteins/{uniprot_id}/tiles/{tile_index}/measured` | Reference observations, UC-05 | Baseline |
| GET | `/v1/proteins/{uniprot_id}/tiles/{tile_index}/clinvar` | ClinVar, UC-06 | Baseline; v0.2 mapping states pending |
| GET | `/v1/models`, `/v1/models/{model_id}`, `/v1/sources` | Model/source evidence, UC-07 | Baseline |
| GET | `/healthz` | Local health/readiness | Baseline |
| GET, POST | `/v1/projects` | List/create local projects, UC-10 | Planned |
| GET, PATCH, DELETE | `/v1/projects/{project_id}` | Read/rename/delete project, UC-10 | Planned |
| GET, POST | `/v1/projects/{project_id}/analyses` | Paginated history; explicitly save single-tile snapshot | Planned |
| GET, DELETE | `/v1/analyses/{analysis_id}` | Reopen/delete immutable analysis | Planned |
| GET | `/v1/analyses/{analysis_id}/export` | Export saved prediction/comparison, `format=csv|json` | Planned |
| GET, POST | `/v1/projects/{project_id}/jobs` | List/submit peptide/protein jobs, UC-08 | Planned |
| GET | `/v1/jobs/{job_id}` | Progress, coverage and outcome counts | Planned |
| GET | `/v1/jobs/{job_id}/items` | Paginated tile outcomes/results | Planned |
| POST | `/v1/jobs/{job_id}/cancel` | Request cancellation | Planned |
| GET | `/v1/jobs/{job_id}/export` | Combined CSV/JSON with per-item manifest | Planned |
| GET, POST | `/v1/projects/{project_id}/datasets` | List datasets / validate import preview, UC-09 | Planned |
| GET, POST | `/v1/datasets/{dataset_id}` | Read preview/revision / commit validated preview | Planned |
| DELETE | `/v1/datasets/{dataset_id}` | Remove project-owned dataset and dependent comparisons | Planned |
| GET, POST | `/v1/analyses/{analysis_id}/comparisons` | List/compute comparisons with a committed dataset, UC-05 | Planned |
| GET | `/v1/comparisons/{comparison_id}` | Reopen immutable comparison | Planned |
| POST/GET | `/v1/runs` and `/v1/runs/{run_id}…` | Legacy expiring share links | Deprecated; excluded |

Deletion accepts `confirm=true`; without it return `409 CONFIRMATION_REQUIRED` with dependency counts, without deleting. All list operations use `offset`/`limit` with `limit` ≤ 200; exports include all rows rather than only the current page. Endpoints below are design contracts, not claims of code availability.

## 3. Single-tile validation and domain

Normalise case and surrounding whitespace. Require exactly one of `sequence` or (`uniprot_id`, `tile_index`). Validate standard alphabet, length, accession/index, scorable window and frozen model in this order. Invalid items produce no scores.

The baseline implements `unknown`, measured/predicted in/out and unreliable states, but its direct screen-PSI threshold is stale. The v0.2 target must use the frozen R3 gate rules and include `borderline`; it must not equate screen PSI with intrinsic PSI(WT). Preserve the measured estimator and gate identity in provenance. Exact research cuts live in the R3 artefacts and [db-design.md](db-design.md) §3.3; integrate and test them before declaring this requirement met.

* In-domain: score with evidence label; add `TRAINING_PEPTIDE` when applicable.
* Unknown, unreliable, predicted or borderline: prominent warning before scores.
* Known out-of-domain: `422 OUT_OF_DOMAIN` unless explicitly overridden; record `OUT_OF_DOMAIN_OVERRIDDEN` in the snapshot/export.
* Typed sequence: no silent canonical mapping. Without verified accession/release, ClinVar is `mapping_unavailable` rather than an empty annotation set.

The legacy single-tile request/response shapes remain in `openapi.yaml`. Adding `borderline` and gate provenance is a planned compatibility extension, not evidence that the baseline server returns it.

## 4. Projects and immutable analyses

`POST /projects` creates a named project; `PATCH` changes only name/description. `POST /projects/{id}/analyses` accepts a prediction request and explicit save action, computes the result and transactionally stores its snapshot. Reading history never recomputes. A rerun uses the saved input but produces a new analysis ID linked through `parent_analysis_id`.

Snapshot: normalised input, tile/protein coordinates and mapping release, frozen model/calibrator/gate IDs and hashes, raw/calibrated arrays, rank/shortlist, domain and warning states, source/annotation versions and data or a versioned local artefact reference, code/configuration version and creation time. Imports/comparison revisions are recorded independently. Missing artefacts produce an explicit integrity error; do not silently substitute today's reference data.

Projects, runs and committed observations have no automatic expiry. Delete only after the dependency summary is confirmed. Project deletion cancels jobs, prevents late worker writes, and removes owned files/results; reference tables, shared weights and other projects remain intact. The local filesystem and database are one workspace; document copying both for recovery. Backups/OS copies are outside the application's deletion guarantee.

## 5. Peptide and whole-protein jobs

`POST /projects/{id}/jobs` accepts a mode and exactly its input:

* `peptides`: a bounded array of `{input_id, sequence}` entries. The UI may parse multi-record FASTA into this array; preserve headers as data and never file paths. Stable unique `input_id`s keep duplicates distinguishable.
* `protein`: exactly one `uniprot_id` or `{input_id, sequence}` for one protein FASTA. An optional explicit accession/release mapping must be verified before using reference annotations.

Submission pins model/calibrator/gate/source versions and persists input. `202` returns the job ID; a local worker executes it. States: `pending → running → completed|partial|failed|cancelled`; cancellation also allowed from pending. Each item is `pending|running|succeeded|refused|failed|cancelled`. Counts must reconcile with the manifest. Completed means every item succeeded; partial means terminal mixed outcomes with at least one success; no successful item means failed unless cancelled. Repeated cancellation is idempotent. The worker claims items transactionally; a lease expires after a crash and unfinished work is reclaimed. Completed snapshots are unique by `(job_id,item_id)` and never duplicated.

Generate only full windows: `start=(tile_index−1)*23+1`, `end=start+27`. Keep the reference sequence hash and uncovered residue intervals, including terminal gaps; proteins shorter than 28 have zero tiles and an explicit error. Do not pad, silently end-align or average repeated protein substitutions across tile contexts. A non-standard residue makes its window unscorable, not the entire job. Each tile keeps domain/override status; partial failures do not discard other results. Ranking stays per tile.

## 6. Experimental import schema and lifecycle

Upload CSV/TSV by multipart to `POST /projects/{id}/datasets`, with file and JSON metadata string. It creates only a staged validation preview (`201`), not a committed observation dataset. A JSON commit `{action: commit, acknowledge_warnings: true}` to `/datasets/{id}` succeeds only with no blocking errors; preview/file hash is immutable. Abandoned previews expire after a proposed 24 h; committed datasets are retained until deletion.

Metadata: dataset name, assay name/version, endpoint, units, source/citation, reference description, and declared comparison compatibility (`zhang_gps_dpsi` or `other`). Declaring compatibility does not bypass checks. Record provenance/rights supplied by the operator; no redistribution or model use is implied.

| Column | Rule |
|---|---|
| `peptide_id` | Required stable row-group identifier |
| `wt_sequence` | Required 28 standard amino acids for this import version |
| `position` | Required integer 1…28, within peptide |
| `wt_aa`, `mut_aa` | Required standard letters; WT must equal sequence[position]; mutant must differ |
| `observed_value` | Required column; finite numeric value or empty with missing reason, never silently zero |
| `replicate_id` | Required; use a declared single-replicate identifier when appropriate |
| `uniprot_id`, `reference_release`, `start_pos` | Optional together; accession/release/sequence must match before protein-coordinate alignment |
| `missing_reason` | Required when value is empty |

Validation reports row numbers and counts for valid, missing, unmatched, duplicate, conflicting and rejected records. Duplicate keys `(wt_sequence,position,mut_aa,replicate_id)` block commit; conflicting values never overwrite earlier values. Preserve replicates; any aggregation is a separate explicit comparison operation with its method recorded. Unsupported coordinate conventions, nonfinite values, incorrect WT and inconsistent PSI/ΔPSI declarations are blocking errors. File names are sanitised display metadata; storage paths are generated IDs. CSV formula text is not executed and is neutralised in exports.

## 7. Comparison and annotation semantics

Comparison selects one committed dataset, one analysis and either a named replicate or an explicit mean/median aggregation. Match exact WT sequence + position + mutant; if protein mapping is supplied also check accession/release/start. Report matched/unmatched/conflicting and missing counts. For compatible GPS ΔPSI return observed value, raw predicted ΔPSI and residual `predicted − observed`; MAE and Spearman include n, aggregation and exclusions. Spearman is unavailable for insufficient/constant pairs. Other endpoints retain separate units and get no pooled ΔPSI residual/metric. Never compare a raw ΔPSI measurement directly to the calibrated probability as if units matched.

ClinVar is mandatory in release 1. Annotation status is `available|no_match|mapping_unavailable|source_unavailable|mapping_conflict`. Source not loaded must not appear as “no variants”. Include source/release IDs, accession/residue check, clinical classification, review/conflict status and diagnostic disclaimer. UniProt sequence/coordinate mapping and approved GPS measurements are the initial supplementary sources; additional integrations require an explicit source contract. Absence of an annotation is not evidence of benignity. Save annotation snapshots/source revisions for historical runs, and copy attribution to exports.

## 8. Exports and provenance

Preserve the baseline nine single-tile score columns: `peptide,tile,position,wt_aa,mut_aa,score_dpsi_raw,p_dpsi_ge_1_calibrated,rank_in_tile,top10pct_in_tile`. Prefix single-tile CSV with provenance comments; ten significant digits gives the existing 5e-9 tolerance.

Job CSV adds `project_id,job_id,item_id,input_id,uniprot_id,reference_release,start_pos,end_pos,protein_position,status,error_code,domain_status`. Write a manifest record for unscored items (score fields empty); JSON separates manifest and successful analyses. Annotated/comparison exports add namespaced annotation/measurement columns plus source/dataset revision, replicate/aggregation and units. Do not multiply score rows silently for multiple clinical submissions: represent one-to-many annotations explicitly in JSON or in a separate named table.

Every result/export contains model and weight hash, event definition, development-evidence label, gate/domain, source versions/attribution, input/configuration/code identity, timestamps, and the disclaimer that the output is not a disease probability. Historical exports use their stored snapshots. Filenames never include input sequences. Paginated screens do not truncate exports.

## 9. Errors, limits and tests

Baseline coded errors remain documented in `openapi.yaml`. Planned operations additionally use `PROJECT_NOT_FOUND`, `ANALYSIS_NOT_FOUND`, `JOB_NOT_FOUND`, `DATASET_NOT_FOUND`, `CONFIRMATION_REQUIRED`, `IMPORT_INVALID`, `DATASET_NOT_COMMITTED`, `INCOMPATIBLE_ENDPOINT`, `JOB_STATE_CONFLICT` and `SNAPSHOT_UNAVAILABLE`. Use 404 for missing resources, 409 for confirmation/state conflicts, 413 for configured size limits, 422 for schema/coordinate/compatibility problems and 503 for unavailable dependencies. Item errors remain in a successful job-status response; they do not make the whole HTTP response a 500.

Machine schema validity, baseline implementation agreement and new-operation acceptance are separate checks. Test new operations only after implementation; planned cases are in [test-plan.md](test-plan.md). This task validates documents, not the new runtime behaviour.
