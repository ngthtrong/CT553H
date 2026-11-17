# Deviations from the design documents

> Scope update 29 Oct 2026: this file documents the **baseline implementation/historical checks**. The accepted first local release now includes projects/history, peptide/protein jobs, ClinVar/reference annotations and experimental import/comparison; those extensions are not implemented by this documentation change. See [current scope](../README.md). The expanded OpenAPI design contains planned operations; old contract/type-check results apply to the baseline only. Public sharing and hosting examples below are legacy, outside current acceptance.


Where the backend differs from, or had to choose beyond, `../openapi.yaml`, `../api-spec.md`, `../db-design.md`,
`../srs.md` and `../test-plan.md`. Nothing in `../` was edited. Written 22 Oct 2026 with the backend.

## 1. Defects and gaps in `openapi.yaml` — **all closed on 22 Oct 2026** (contract and `api-spec.md` edited; see §6)

The table keeps the original findings. The column "Suggested fix" is what was done.

| # | Gap | What the backend does | Suggested fix of the contract |
|---|---|---|---|
| D-1 | `POST /v1/predict` and `POST /v1/runs` list no `400`, but api-spec §5 says a body that is not JSON is `400 INVALID_REQUEST` | Returns 400 | Add `'400'` to both operations |
| D-2 | `GET` endpoints list no `422`, but a malformed accession, a non-integer `tile_index`, a too-short `query` or a bad `limit` are `422 INVALID_REQUEST`; `GET /v1/proteins` without `query` is `400` | Returns 422 / 400 | Add `'422'` (and `'400'` for `/v1/proteins`) |
| D-3 | `PredictRequest` has `additionalProperties: false` and is extended with `allOf` by `/v1/export` (`format`) and `/v1/runs` (`ttl_days`). No instance can satisfy both branches, so a generator such as schemathesis cannot build a request | The server accepts the extra field. `tests/test_contract.py` removes `additionalProperties` from an in-memory copy of the contract | Replace by `unevaluatedProperties: false` on the composed schemas, or write `ExportRequest` and `RunRequest` out in full |
| D-4 | `TILE_OUT_OF_RANGE` is `422` in api-spec §5 (for `predict`) but the overlay endpoints list only `404` | `predict`, `export`, `runs`: 422. `…/measured` and `…/clinvar`: **404** `TILE_OUT_OF_RANGE` | State both in api-spec |
| D-5 | No error code for an unknown route or a wrong method | `404`/`405` with code `INVALID_REQUEST` and the standard body | Add `NOT_FOUND`, `METHOD_NOT_ALLOWED` to the enum, or keep as is |
| D-6 | The `firstCells` example lists only the Zhang source in `data_sources`, although the tile comes from UniProt and the status from the GEO screen | `data_sources` holds the model's training sources **plus** every source used for the request: UniProt for a UniProt tile, the GEO screen for a measured status, ClinVar for the ClinVar overlay (api-spec §6 says "and for any overlay used") | Update the example |

The API test `API-50` (schemathesis over the whole contract, positive and negative generation) now checks the
statuses **listed per operation** (`status_code_conformance`) and that every error body conforms to `Error`; the
in-memory patch of the contract is gone.

## 2. Choices where the documents leave room

* **Unknown request field**: `422 INVALID_REQUEST` with `field: null`. The name is attacker-controlled text and is not echoed (SEC-02).
* **`format` missing** in `POST /v1/export` is `422 INVALID_REQUEST` (field `format`); a wrong value is `400 INVALID_FORMAT`. In `GET /v1/runs/{id}/export` a missing `format` is `400 INVALID_REQUEST`, checked before the token, so nothing about the run is revealed.
* **Share token**: missing or empty ⇒ `401 TOKEN_REQUIRED`; any other wrong token ⇒ `404 RUN_NOT_FOUND` with the same message as an unknown run id; constant-time comparison of SHA-256 hashes.
* **Expired run**: the first read with the right token gives `410 RUN_EXPIRED` and deletes the row (db-design §9, "opportunistic delete"); later reads give `404`. The hourly job removes the rest.
* **`model_id`** that does not match the id pattern is `404 MODEL_NOT_FOUND` (the contract lists no 422 for it). Only `frozen` models with role `effect` serve predictions; `GET /v1/models` lists all registered models, default first.
* **Reference endpoints** (`tiles`, overlays) carry a `provenance` object, which the contract requires to hold `model_id` etc.; it is filled from the default model and the sources of the overlay. If no model is serving they answer 503.
* **ClinVar overlay** answers `503 SERVICE_UNAVAILABLE` when no ClinVar rows are loaded (a deployment may skip ClinVar).
* **Protein search** accepts `[A-Za-z0-9._-]{2,32}`; anything else is 422. Ranking: exact gene, exact accession, gene prefix, accession prefix, then gene symbol and accession.
* **Typed sequences** never look up a stored tile (api-spec §4); a gate model, when one is registered, may still classify them.
* **`usage_daily.endpoint`** holds `METHOD route-template`, the model id is filled only for prediction routes.
* **Access log**: uvicorn's own access log is switched off (`--no-access-log`) because it prints concrete paths, i.e. accessions and tokens; the application logs `METHOD template status ms request-id` only.
* **Rate limiter** and usage counters are in process memory, so the container runs **one** worker. Two workers would each allow the full rate.

## 3. Database (`db/models.py`, migration `0001`) against the DDL of db-design §4

| DDL | Implemented | Reason |
|---|---|---|
| `jsonb` | SQLAlchemy `JSON` (PostgreSQL `json`) | One type for SQLite and PostgreSQL; nothing queries inside the documents |
| `uuid` | `varchar(36)` | Same; the UUID is generated by the application |
| `char(28)` etc. | `CHAR(n)` | Equal. All values have exactly that length, so padding does not occur |
| `CHECK (expires_at <= created_at + interval '30 days')` | Added by the migration **only on PostgreSQL**; SQLite relies on the application (`ttl_days` ≤ 30) | `interval` arithmetic is not portable |
| `CHECK (length = char_length(sequence))` | `length(sequence)` | `length()` exists in both |
| Constraint names | Named by the naming convention `ck_<table>_<name>` | Alembic needs names |
| `bigserial` | `BIGINT` that becomes `INTEGER PRIMARY KEY` on SQLite | Auto-increment on both |

The migration was generated by Alembic and checked against the models: `alembic upgrade head` on SQLite followed by
`compare_metadata` reports no difference, and `downgrade base` works (`tests/test_etl.py` migrates a fresh database for each case).

## 4. ETL

* **Inputs are the derived caches** named in `etl/sources.yaml` (`interim/gps-peptidome-rep1.tsv`, `processed/learning-curve-sat-ext4.0.npz`), pinned by SHA-256 *taken from the local copy*; they detect later change, not original provenance. The FASTA and ClinVar hashes are the ones recorded in `data/README.md` and the manifests.
* **ETL-04** is done on features, not on strings: each of the 92,337 training rows must equal the 180 features rebuilt from the UniProt-derived tile at some (position, mutant) in order. Zero mismatches means tile sequence and numbering agree for all 176 training peptides. It says nothing about the other tiles.
* **New finding for the open question in db-design §3.3** (tile numbering of the screen against UniProt 2026_03): of 19,687 screen rows without a tile, **16,266 have index exactly one above the last full window** of their protein (so the library very probably also holds an end-aligned C-terminal tile), 2,055 are two above, 295 more, and 1,071 belong to accessions that are not in the snapshot. The 482,216 tiles of the product use only full 28-residue windows with step 23 (decision D-4); the C-terminal tile is not served. See the ETL report (`tiles`, `screen_rows_unmatched_reasons`).

## 5. Not verified

* **PostgreSQL**: the migration, the ETL and the API ran only on SQLite. `docker-compose.yml` has not been run (no Docker on the development machine). The PostgreSQL path is therefore untested, including the 30-day check and `psycopg` binding of `executemany`.
* The `web` service builds `./frontend`, which belongs to the frontend task; compose cannot start without it.
* Behind a reverse proxy: `DF_TRUST_PROXY` reads the first `X-Forwarded-For` entry; not exercised.
* NF numbers (`tests/results/latency.json`) are for the development laptop over loopback, not for the reference host (2 vCPU / 2 GB) and not over TLS.
* Free-tier hosting limits, and the database size with ClinVar scope `in-tiles` on a hosted PostgreSQL (the SQLite file is about 450 MB).

## 6. Reconciliation of 22 Oct 2026 (contract brought in line with the implementation)

| Item | Closed by |
|---|---|
| D-1 | `400` added to `POST /v1/predict` and `POST /v1/runs` (and `413`, which the body-size limit returns, to `/v1/runs` and `/v1/export`) |
| D-2 | `422` added to every GET with path or query parameters; `400` and `422` to `GET /v1/proteins`; `503` to the ClinVar overlay (no ClinVar rows loaded) |
| D-3 | `PredictRequest`, `ExportRequest` and `RunRequest` are separate closed schemas (`additionalProperties: false`) that share the property schemas (`Request*`) and the rule `RequestTarget`; no `allOf` extension of a closed schema, so schemathesis builds valid requests and the patch in `test_contract.py` was deleted |
| D-4 | The 404 of both overlay endpoints is described: `UNKNOWN_ACCESSION` or `TILE_OUT_OF_RANGE` (404 there, 422 for `predict`/`export`/`runs`); api-spec §5 lists both |
| D-5 | Kept as is and documented in api-spec §5: unknown route or wrong method is 404/405 `INVALID_REQUEST`, not attached to an operation |
| D-6 | The `firstCells` example and the CSV example list the three sources of the request (Zhang saturation, UniProt, GEO screen) |
| E2E-07 (frontend README) | **Decision: the list comes from the backend.** `ModelCard.not_used_sources` (`source_id`, `name`, `reason`) is generated from `degron_footprint.sources.NOT_USED_SOURCES`, which a test requires to have exactly the ids of `BLOCKED_SOURCE_IDS` (what the ETL refuses to load), so the page cannot disagree with the enforcement. The frontend renders it in a "Sources not used" section; the card Markdown no longer carries it. Tests: `test_api24_models` (backend), `E2E-07` in `flows.test.tsx` (mock) and `real.spec.ts` (real backend) |
| Frontend config | `playwright.config.ts`: the desktop project now ignores `narrow.spec.ts`, which asserts the 360 px table-first layout and failed when run at 1280 px |

## 7. Open item added on 23 Oct 2026: integrate the R3 domain gate

> **Closed on 16 Nov 2026 (branch 2, WP7).** Implemented as below; the table that follows is the original open item.
>
> * `degron_footprint/gate_r3.py` loads the frozen R3 weights (`gate-weights.npz`, SHA-256 `13be4bf1…`) through an
>   application card `models/gate.json` written by the ETL; the R3 files are not edited. Registered as
>   `model_version` `gate-r3-v1` (role `gate`). A card/weights mismatch disables the gate (NullGate), never the service.
> * Tier 1 replaces `psi <= 4.0`: `P = σ(10.187 − 3.275·x)`, in ≥ 0.8 (x ≤ 2.687), out < 0.5 (x ≥ 3.110), else
>   `measured_borderline`. Without a gate a reliable measurement stays `unknown`; there is no 4.0 fallback.
> * Tier 2: `x̂ = counts·coef + intercept` on **raw** counts (run_r3 `fit` returns `b = ȳ − x̄·coef`), `P = σ(8.457 −
>   1.911·x̂)`; the ETL stores it for unscreened scorable tiles, the service applies it to typed sequences.
>   Golden tests (`tests/test_gate.py`) compare features and x̂ with `run_r3.feats` on 503 sequences (max |Δ| < 1e-12)
>   and the cut points with `gate-card.json`.
> * D-5 behaviour as proposed: borderline is scored with `DOMAIN_BORDERLINE`; out-of-domain is refused unless
>   `override_domain`. Jobs pin `gate_model_id` and `gate_sha256`.
> * Measured on the real reference (ETL of 16 Nov, `.data/etl-report.json`): 347,780 reliable screen tiles →
>   88,147 in (25.35 %) / 30,347 borderline (8.73 %) / 229,286 out (65.93 %), matching R3's 26 / 9 / 65 %; the 26,397
>   unscreened scorable tiles → 12,707 / 6,604 / 7,086 (predicted). Of the 176 training tiles, 143 are in, 22
>   borderline and **11 out**: those 11 are refused by default when picked by accession, which follows from the gate
>   (R3 tier-1 precision 0.934), not from a defect.
> * `.data/dev.db` was migrated to `0003` and its reference reloaded with `make etl SCOPE=none` (ClinVar rows kept:
>   2,338,863); the pre-change copy is `.data/backup/dev-2026-11-16.db`.

Experiment R3 ([report](../../research/r3-domain-gate-2026-10-22/README.md), files in `run-kaggle-20261022/`) delivered the gate. What the code must change (not done):

| Item | Today | Needed |
|---|---|---|
| Tier-1 rule `status_from_measurement` (`domain.py`), `etl/load.py` | `psi <= DOMAIN_PSI_MAX (4.0)` on the **screen** PSI | R3 measured specificity 0.20 for that rule. Map through `P = σ(10.187 − 3.275·x)`: in if x <= 2.687, out if x >= 3.110, else borderline |
| `STATUSES`, DB `CHECK`, `openapi.yaml`, `schema.d.ts`, `domain.ts`, mock, tests | no `borderline` | add `measured_borderline` and `predicted_borderline`; new Alembic migration (0001 holds the constraint) |
| Gate loader (`GATE_LOADERS`) | none registered; `gate-card.json` has no `kind` | register a loader and wrap the card in the app's own file (do not edit the R3 files). `x̂ = counts(20 aa + 400 adjacent pairs) · tier2_coef + tier2_intercept`; `P = σ(8.457 − 1.911·x̂)`; cuts x̂ <= 3.700 / >= 4.426. `psi_wt_predicted` is on the **screen** scale, not comparable with 4.0. A golden test against `run_r3.py` is required (the intercept's centring was not checked end to end) |
| Behaviour for `borderline` | undefined | the author's decision (D-5): proposed "score with a warning, refuse only out-of-domain" |
| UX consequence | — | about 26% of screen tiles are in, 9% borderline, 65% out ([proteome-domain-share.json](../../research/r3-domain-gate-2026-10-22/run-kaggle-20261022/proteome-domain-share.json)): with refusal by default, about two thirds of arbitrary UniProt tiles would be refused |


## 8. Workspace schema (migrations `0002`, `0003`) against db-design §11 — 16 Nov 2026

Branch 2, WP2 of [implementation-plan-2026-11-16.md](../implementation-plan-2026-11-16.md). §11 gives entities and
invariants but no DDL; these are the choices made, all checked by `tests/test_workspace_schema.py`.

| §11 / contract | Implemented | Reason |
|---|---|---|
| Cross-project associations must be impossible | Composite FKs `(project_id, job_id)` → `analysis_job`, `(project_id, analysis_id)` → `analysis_run`, `(project_id, dataset_id)` → `import_dataset`; `comparison` therefore carries its own `project_id` | A single-column FK cannot express "same project" |
| `analysis_run.parent_analysis_id` | Plain column, **no FK** | An FK would either block deleting a parent or force rewriting an immutable child; the API reports a missing parent explicitly |
| `job_item` key `(job_id, item_id)` | Adds `ordinal` (unique per job) | Stable manifest order and pagination tie-breaker independent of the item ID format |
| `import_dataset` "new file = new revision" | Unique `(project_id, name, revision)` | Revisions are grouped by display name inside a project |
| Saved runs must not depend on mutable reference rows | `analysis_run`/`job_item` store accession + tile index as data, **no FK** to `tile`/`protein` | A new reference load must not break or alter history (A-6) |
| `analysis_run` immutable | Enforced by the application (no update path); no trigger | Triggers differ between SQLite and PostgreSQL; covered by HIST tests in WP4 |
| `DomainStatus` in `openapi.yaml` has one `borderline` | Two states, `measured_borderline` and `predicted_borderline` (as §7 and plan.md 2.10) | Keeps the measured/predicted origin like every other state; the contract is aligned in WP3 |
| Borderline states in the `tile` CHECK | `0003` rebuilds `tile` on SQLite (in-place `ALTER` on PostgreSQL); downgrade refuses while a borderline tile exists; refuses to run with `PRAGMA foreign_keys=ON` | On SQLite, dropping the old table with foreign keys on would cascade into `measured_cell` |
| Workspace files | `.data/workspace/<project_uuid>/<dataset_uuid>.{csv,tsv}`, path stored relative; `api/workspace.py` accepts only canonical UUIDs and refuses paths (or symlinks) that leave the root | NFR-08; no user text in paths |

Measured on 16 Nov 2026 (SQLite copy of the 453 MB `dev.db`, then PostgreSQL 16.16 in Docker): `upgrade head` then
`downgrade 0001` leaves `protein` 20,431 / `tile` 482,216 / `measured_cell` 92,337 / `clinvar_variant` 2,338,863 rows
unchanged, `PRAGMA foreign_key_check` empty, `integrity_check` ok; on PostgreSQL `upgrade head` → `compare_metadata`
empty → `downgrade base` → `upgrade head`. The original `dev.db` was not migrated.

## 9. Contract changes to `../openapi.yaml` — 16 Nov 2026 (WP3)

Unlike the 22 Oct baseline, branch 2 edits the contract first (A-1 of the implementation plan) and regenerates
`frontend/src/api/schema.d.ts`. Changes on 16 Nov, all still `x-implementation-status: planned` until their WP lands:

| Change | Why |
|---|---|
| `DomainStatus`: `borderline` → `measured_borderline`, `predicted_borderline`; `Warning.code` gains `DOMAIN_BORDERLINE` | §7/§8; the frontend gives both a dotted pattern and an amber warning (ui-design W-2) |
| `Error.code` gains `COMPARISON_NOT_FOUND`, `IMPORT_EXPIRED` | `getComparison` 404 had no code; IMP-02 requires an expired preview to be reported as such |
| `422` on `listProjectJobs`, `listComparisons`, `getComparison` | Invalid `offset`/`limit`/UUID had no declared response |
| `Project.counts {analyses, jobs, datasets}` (required) | The project card of the Projects screen shows them |
| `Job.cancel_requested` | The UI can show "cancelling" before the last running item stops |
| `SavedAnalysis.parent_available` | `parent_analysis_id` has no FK (§8); a deleted parent is reported, not hidden |
| `SavedAnalysisPage.items` → new `SavedAnalysisSummary` (no cells) | `PredictionResult.cells` requires 532 cells; a 50-row history page would carry ~3 MB. The full result is read with `getAnalysis` |
| `Project.deletion_pending` | HIST-03: a confirmed deletion whose file cleanup failed stays visible for a retry instead of being reported as done |
| `400` declared on all 24 workspace operations | Non-JSON bodies (`INVALID_REQUEST`) and bad `format` (`INVALID_FORMAT`) answer 400 as on the baseline operations; schemathesis (API-50) found the gap |

The mock of the 24 operations is `frontend/mock/workspace.ts` (synthetic numbers, in-memory state), tested by
`frontend/tests/workspace-mock.test.ts`.

## 10. Workspace API behaviour chosen in WP4–WP5 — 16 Nov 2026

| Topic | Implemented | Reason |
|---|---|---|
| Malformed path id (`/v1/projects/abc`) | `422 INVALID_REQUEST` with the parameter name, never a lookup | Same rule as `tile_index`; a 404 would hide a client bug |
| Project deletion order | (1) mark `deleting` and cancel jobs in one transaction, (2) remove `.data/workspace/<id>/`, (3) delete owned rows | A file failure is reported (503) and retried; rows are never removed before files, so nothing is orphaned |
| History timestamps | Stored with microseconds, shown to the second | "Most recent first" must hold for two saves within one second |
| Item refused at submission | Inputs that can never be scored (length, letter, unscorable window) become `refused` items immediately | The manifest accounts for every input; a job with only refused items is `failed` without a worker |
| Job state `running` | Only after a worker first claims an item | Refused-at-submission items must not make an untouched job look started |
| Claim | Compare-and-set `UPDATE … WHERE state='pending' OR lease expired`, `rowcount == 1`; PostgreSQL adds `FOR UPDATE SKIP LOCKED` to the candidate select | Correct on both back-ends without `BEGIN IMMEDIATE`; A-4 |
| In-flight item when a job is cancelled or its project deleted | The worker's commit sees the flag and records `cancelled` (or `lost` if the rows are gone); no analysis is written | FR-26, HIST-03: no late writes |
| Pinned model/gate no longer serving | The item fails with `MODEL_NOT_FOUND` / `SNAPSHOT_UNAVAILABLE`; it is never scored with other weights | FR-27 |
| Worker process | `python -m api.worker` (`make dev-worker`); `DF_EMBEDDED_WORKER=1` runs the same loop in a thread of the API for a one-command start | A-2 keeps the process separate by default |
| Body limit | 4 KiB for single predictions as before; 256 KiB for workspace JSON (100 peptides or a 10,000-residue protein) | FR-36 |
