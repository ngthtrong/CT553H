# System: Degron Footprint Tool

**Current software scope: v0.2, 29 Oct 2026, confirmed by the author in this session.** One local web application, React + TypeScript and FastAPI, for researchers prioritising single-amino-acid substitutions for experimental follow-up. The first release includes single-peptide analysis, peptide batches, whole-protein tiling, ClinVar and approved reference annotations, experimental-data import for comparison, and persistent projects and analysis history.

This is a requirements and design update, **not an implementation or acceptance report**. The baseline service wraps the frozen `m3-ext4.0-platt-v1` model; changing the software scope does not select a new research model, retrain it or close G2/G3. The proposal files are deliberately unchanged. The working thesis is [../report/](../report/README.md).

## 1. Scope confirmed on 29 Oct 2026

| Topic | First-release scope | Boundary |
|---|---|---|
| Platform | React + TypeScript (Vite), FastAPI, local PostgreSQL 16; SQLite remains a test/baseline-development backend | One product and one local workspace; no account system or multi-tenant deployment |
| Operation | Browser and backend on the same computer, bound to loopback; CPU inference | No public website, hosting/VPS, domain, TLS or Internet availability acceptance requirement; reference downloads are a separate preparation step |
| Single peptide | 28 standard amino acids; 532 substitutions, matrix, ranking, CSV/JSON | Same mutation-level ΔPSI task and assay domain |
| Batch | A list/FASTA of 28-residue peptides; a background job with per-item outcomes | Configurable bounded input, cancellation, restart recovery and partial-failure reporting |
| Whole protein | One loaded human UniProt accession or one supplied protein FASTA; full 28-residue windows, step 23 | Report uncovered residues and unsuitable tiles; no full-protein biological-effect claim; keep overlapping tile contexts separate |
| Annotations | ClinVar missense, UniProt mapping and approved GPS reference evidence | Source version, attribution, reference-residue checks; unavailable/ambiguous mappings are explicit; no disease-probability inference |
| Experimental comparison | CSV/TSV import, validation preview, explicit commit into a project, aligned prediction/measurement comparison | Keep assay, units, replicates and provenance; no automatic relabelling, pooling or retraining |
| Projects and history | Create, rename, reopen, delete; save immutable analysis snapshots and imported datasets locally | Explicit save/submit consent; retain until deleted, no 30-day expiry for project history; no public sharing |
| Evidence | Model card, domain assessment and provenance in results and exports | Development benchmark is not independent validation; training-data overlays are labelled |

Whole-protein mode changes the number of inference tiles, not the model's 28-residue prediction unit. Imported observations are project data, not new training labels or proof of external validation.

## 2. Documents and status

| File | Current role |
|---|---|
| [srs.md](srs.md) | v0.2 scope, UC-01…10, FR-01…36 (FR-20 retired), NFR-01…20 and traceability |
| [db-design.md](db-design.md) | Baseline DDL plus explicitly planned workspace/job/import migration (§11) |
| [openapi.yaml](openapi.yaml) | Baseline contract plus planned v0.2 operations marked `x-implementation-status`; legacy sharing deprecated |
| [api-spec.md](api-spec.md) | Validation, domain, batch, import, persistence and export behaviour |
| [ui-design.md](ui-design.md) | Existing single-tile screens plus first-release workspace, job and import screens |
| [test-plan.md](test-plan.md) | Local acceptance plan, including pending v0.2 cases |
| [chapter-sync.md](chapter-sync.md) | Record of the scope changes applied to the thesis; remaining implementation work |
| [app/](app/README.md) | Baseline implementation, not changed in this documentation task |

Read this README, SRS, data design, API contract/specification, UI design, then test plan. English design documents feed the English thesis; its Vietnamese abstract states the same scope.

## 3. Design decisions

| ID | Decision | Reason |
|---|---|---|
| D-1 | React + TypeScript and FastAPI, one local instance with PostgreSQL | Confirmed stack; interactive matrix and reusable Python inference |
| D-2 | Unsaved single-tile previews are transient; project saves, batch submissions and committed imports are persisted explicitly | Reopening projects and history requires durable storage and clear retention |
| D-3 | Compute scores on demand; save completed run snapshots, not all possible reference predictions | Traceability without precomputing the reference proteome |
| D-4 | 28-residue tiles, step 23, 1-based coordinates | Preserve the baseline feature domain and coordinate convention |
| D-5 | Domain status is attached to every tile; refuse known out-of-domain tiles by default, allow explicit warned override; unknown/borderline results carry warnings | Gate evidence and implementation must agree; R3 integration remains open |
| D-6 | Custom sequences are not silently matched to a canonical protein | Protein mapping requires an explicit, validated accession/release; annotations can be unavailable |
| D-7 | Public sharing and its expiring token flow are outside the accepted release | A local project workspace replaces sharing as the persistence use case |
| D-8 | Distinguish training observations, imported observations and predictions | Comparison does not itself establish independent validation |
| D-9 | Keep independent inference/runner calculations for numerical checks | Avoid checking one implementation against itself |
| D-10 | ClinVar is mandatory in release 1; record the loaded scope and snapshot | Show empty, unavailable and mapping-conflict states separately |
| D-11 | Licence/source gates apply to reference ETL; private project imports remain segregated | Import does not grant permission to redistribute or train |
| D-12 | Generate frontend types from the contract when implementing v0.2 | Documentation alone does not make the baseline client support new routes |
| D-13 | Durable jobs, run snapshots, dataset hashes and local deletion | Batch recovery and reproducible history require more than browser state |

## 4. Baseline evidence and outstanding work

The following are **historical records from the 22–23 Oct documents, not re-executed tests for v0.2**:

| Part | Recorded baseline evidence |
|---|---|
| Backend | 149 pytest cases; runner agreement on 92,337 cells; SQLite, ruff and mypy checks |
| Reference ETL | SQLite load: 20,431 proteins, 482,216 tiles, 92,337 training cells and 2,338,863 ClinVar variants; reported idempotence |
| Frontend | 131 vitest cases; Chromium mock/build/backend runs; single-tile UI and source/model pages |
| Contract | Baseline 13-path contract was reconciled with the code; new planned paths are not part of those results |

**Pending first-release implementation/verification:** projects/history, durable batch jobs, whole-protein web flow, experimental import/comparison, expanded exports and local PostgreSQL integration. Existing single-tile/ClinVar functionality must be rechecked under the new scope. Historical counts must not be presented as passing the new requirements.

**Scientific integration gap:** R3 showed that raw screen PSI and intrinsic PSI(WT) are different estimators. The baseline app still compares screen PSI directly with 4.0 and does not load the delivered gate model or represent `borderline`. Correct integration is required; merely changing a document is insufficient. Tile/reference mapping outside the training peptides and source terms remain data-quality checks, not hosting tasks.

## 5. Local operation and acceptance

There is one local application, not separate public/internal editions. Target components are the browser frontend, FastAPI, a local job worker using the same inference package, PostgreSQL and a local workspace file directory. Bind application listeners to `127.0.0.1`; allow only the configured loopback frontend origin. No third-party API receives user sequences.

Docker Compose may package these same local components; it is not a second deployment target and is not required for public hosting. Existing VPS/Caddy configuration is legacy code outside this release's acceptance scope. Current development commands in [app/Makefile](app/Makefile) start only the baseline: they do not implement jobs or project persistence.

Acceptance is a clean local installation and execution of UC-01…10, close/reopen recovery of saved work, numerical agreement, import/annotation correctness and measured local resource use. Record the actual OS, CPU, RAM, dataset sizes and dependency versions; the old VPS sizing is not a requirement. Performance and input-limit defaults in the SRS are proposed until measured locally.

## 6. Documentation maintenance

Keep requirements, data design, API, screens and tests consistent. New routes and migrations are labelled planned until implemented and tested. The author explicitly requested the thesis update in this session; [chapter-sync.md](chapter-sync.md) records the applied changes. Do not edit the proposal or unrelated experimental results as part of this scope update.
