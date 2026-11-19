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

* ~~**PostgreSQL**: the migration, the ETL and the API ran only on SQLite. `docker-compose.yml` has not been run.~~ Closed: PostgreSQL suite since 16 Nov (WP8); the whole compose stack ran on 17 Nov 2026 (§12).
* ~~The `web` service builds `./frontend` …~~ Closed 17 Nov 2026 (§12).
* Behind a reverse proxy: `DF_TRUST_PROXY` reads the first `X-Forwarded-For` entry. In compose the `web` container overwrites the header and `DF_TRUST_PROXY=true` (§12); the `vps` profile with Caddy in front is still not exercised.
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

## 11. Found and decided during WP9–WP11 — 17 Nov 2026

| Topic | Implemented | Why / evidence |
|---|---|---|
| Cross-site writes (SEC-03, CON-8) | `POST`/`PUT`/`PATCH`/`DELETE` under `/v1/` with an `Origin` that is neither in `DF_ALLOWED_ORIGINS` nor this host, or with `Sec-Fetch-Site: cross-site`, answer `403 INVALID_REQUEST`; JSON bodies must be declared `application/json` (`415`). `403`/`415` added to the contract for those operations | CORS stops a foreign page from *reading* the answer, not from *sending* a write to `127.0.0.1`; a `text/plain` or form post needs no preflight. Clients without these headers (curl, worker, tests) are unaffected. `tests/test_workspace_api.py` SEC-03 cases |
| Migration `0004` | Index on `clinvar_variant.clinvar_file_date` | NF-07 run: `max(clinvar_file_date)` scanned 2,338,863 rows (~290 ms) for every annotated tile; whole-protein jobs took 324 ms/tile, now 54 ms/tile (`tests/results/workspace-performance.json`) |
| Worker commit on SQLite | The commit starts with a compare-and-set `UPDATE` of the owned item, then re-reads the job | A cancellation committed while the worker finished an item could be overwritten (job `partial` instead of `cancelled`); reproduced by `test_cancel_racing_a_live_worker_always_ends_cancelled` (fails 3/3 on the old code, passes on the fix) |
| Model page at 360 px | Tables wrapped in scroll regions; `code` wraps | Found by the new browser × width matrix (`e2e/matrix.spec.ts`), a baseline defect |
| `/` and `/new` | Both render New analysis; the sidebar links `/` | Keeps the baseline routes and e2e flows; `/new?mode=batch|protein&project=` carries ids only |
| Footprint track | Mean of the 19 substitutions per position beside the matrix, same scale as the matrix | Proposed addition (G-4), recorded in `ui-design.md` §12.4b; equals the recomputation within 1e-9 |
| Priority panel (plan 2.11) | Top 5/10/20 by rank within the tile; the "retrospective, development benchmark" label precedes the numbers in the DOM | `plan.md` 2.11 |
| Vitest import test | jsdom gives MSW an empty `File` inside `FormData`; the Vitest case checks the report and the blocking path only | The acknowledge-then-commit path is checked in Chromium (`e2e/workspace.spec.ts`) and against the real backend (`e2e/real.spec.ts`) |

## 12. Docker for every component and the optional LoRA-D model — 17 Nov 2026

| Topic | Implemented | Why / evidence |
|---|---|---|
| Whole stack in Docker | `docker-compose.yml`: `db` (PostgreSQL 16), `api`, `worker` (separate process, A-2), `web` (nginx), `etl` (profile `tools`); `compose.dev.yml`: bind-mounted source, Vite `:5173`, API `--reload` `:8000`, `test` service. Every published port on `127.0.0.1` | User request of 17 Nov 2026 ("move all FE and BE to Docker"). Record: `docker-validation-2026-11-17.md` |
| Defects found when the compose file first ran | `web` published container port 80 but nginx-unprivileged listens on 8080; nginx sent `Host` without the port (`$host`), so the API's same-origin check would refuse writes from `:8080`; `client_max_body_size 8k` for every `/v1/` path blocked saved analyses (256 KiB) and imports (10 MiB); no `worker` service, so jobs never ran; no volume for imported files | Fixed: `127.0.0.1:8080:8080`, `$http_host`, 320 KiB for `/v1/` and 11 MiB for `POST /v1/projects/{id}/datasets`, `worker` service, `workspace` volume. `frontend/tests/security-headers.test.ts` checks the nginx rules |
| `Settings` no longer reads `.env` | `env_file=None` | `system/app/.env` is now the Compose file with container values (`DF_TRUST_PROXY=true`, origins `:8080`); read implicitly it broke `test_sec03_allowed_and_same_origin_writes_pass` on the host and would have trusted `X-Forwarded-For` in a host process. `tests/test_lora.py::test_settings_ignore_the_compose_dotenv_in_the_working_directory` |
| LoRA-D model kind `torch_lora` (WP10) | Frozen, **non-default** effect model; serving code `degron_footprint/lora.py` written from the recipe (not importing `degron_v3`); optional dependencies `requirements-lora.txt`; Docker build argument `WITH_LORA=1` | `plan.md` 2.12. `backend/LORA.md` |
| Calibrator values for LoRA-D | The contract keeps `platt`/`iso`. For LoRA-D `platt` means its three-class logistic calibrator (logistic regression on the raw score); `iso` → `422 INVALID_REQUEST`, field `calibrator` (predict and job submission) | No contract change; the calibrator the research fitted is logistic, there is no isotonic one |
| `DF_DEFAULT_MODEL_ID` | Chooses the model used when a request names none; not serving → registry default kept, reason in `registry.errors`. `/v1/models` and `/v1/models/{id}` report the effective default in `is_default` | Promotion is a serving decision separate from research (`serving_promotion: not_authorized_by_research_execution`) |
| `TRAINING_PEPTIDE` per model | A model may carry its own training set; LoRA-D's bundle lists the 235 W tiles and the warning follows it for typed and stored tiles. The npz model keeps the previous rule (stored tiles among its 176 training peptides) | Without this, a W tile outside the 176 would have been served by LoRA-D without the warning |
| Domain gate | R3 applies to LoRA-D as to the npz model, although LoRA-D was trained on every wild-type PSI (arm D) | Conservative; changing the gate per model would be a scientific decision |
| Latency | LoRA-D p95 39.1 s per tile in Docker (4 CPU threads), npz p95 20 ms; nginx `proxy_read_timeout 300s` for `/v1/` | NFR-01 (300 ms) not met by LoRA-D; recorded, not hidden: `tests/results/latency-lora.json` |
| Fonts blocked by the CSP in the nginx build | `build.assetsInlineLimit: 0` in `frontend/vite.config.ts`: small Fira subsets are files under `/assets`, not `data:` URIs | Found 17 Nov 2026 in the Docker UI check with LoRA-D as default (4 console CSP errors, now 0); the CSP stays strict (no `font-src data:`) |
| Typography and UI pass (17 Nov 2026) | Roboto / Roboto Mono (variable, self-hosted) replace Fira Sans / Fira Code; type-scale and weight tokens; domain banner coloured by status, evidence label in the info tone; grouped matrix toolbar; key–value alignment fix | User request; `../design/ui-ux-pro-max-2026-11-17/README.md`. Scientific colour scales and DOM order unchanged |

## 13. System completion, wave 1 (`plan-system.md`) — 18 Nov 2026

| Topic | Implemented | Why / evidence |
|---|---|---|
| `TRAINING_PEPTIDE` for typed input with the npz model (1.5) | The registry fills the npz model's `training_sequences` from the reference DB (tiles with a measured cell flagged `in_training_set`, 176 in `dev.db`); every model answers from its own set, typed or stored. **Behaviour change:** a typed copy of a training tile is now warned (before: only the stored tile) | plan-system 1.5. `tests/test_lora.py::test_training_peptide_warned_for_typed_input_with_each_model`; `test_api18` expectation updated |
| Default model provenance (4.3) | `Registry.default_source` (`registry`/`setting`/`fallback`); one start-up log line in API and worker; `/healthz` adds `default_model_source`, `default_model_sha256` (contract: optional fields of `Health`) | `system/serving-policy.md`. A default must match a serving decision record; the current `.env` (LoRA-D) has none yet (policy §4) |
| `/v1/models` serving fields (1.1) | `serving`, `not_serving_reason`, `expected_tile_seconds` added to `ModelSummary` (required; `ModelCard` inherits them). Gate rows serve when they are the gate loaded by this process | `tests/test_api.py::test_msel01_*`, `test_api16_models` |
| `expected_tile_seconds` source (1.1) | Plan says "moving average measured in the process". Implemented: mean of the last 20 real model computations in the answering process (cache hits and DB time excluded); **when the process has none, the median `duration_ms` of the last 20 succeeded job items of that model** (worker is another process). The fallback includes the item's DB work, so it slightly overstates | Without it the first LoRA-D request after a restart (≈ 40 s) had no warning. `tests/test_jobs.py::test_batch08_*` |
| Slow-model confirmation threshold (1.1) | 20 s total (`SLOW_SECONDS`); no dialog when the model has no measurement yet | A threshold was not fixed by the plan; 20 s is above any npz job of ≤ 100 peptides and below one LoRA-D tile |
| Prediction cache (1.2) | `degron_footprint/cache.py`: key `sha256(seq · model_id · weights_sha256 · calibrator · CODE_VERSION)` with the **effective** calibrator (omitted = model default); memory LRU (default, 512 entries) / disk (opt-in, `.npz` per key, 0700, atomic replace) / off. Cached arrays are read-only. Stats logged as counts on the usage-flush tick | plan-system 1.2; disk mode stores sequences implicitly — INSTALL.md §6, NFR-09/10. `tests/test_cache.py` |
| Seed spread (1.3) | `Cell.score_seed_sd/min/max` (optional, nullable): always present (null) in new results of the npz model, absent in older snapshots. Plan names `score_seed_sd` only; min/max added because the inspector shows the seed range. Stored in `analysis_cell` **and** `prediction_cell` (share links rebuild identically). CSV exports: three columns after the nine FR-12 columns, empty without seeds | Migration `0005`; `tests/test_seed_spread.py`; export header tests updated |
| Job ETA (1.7) | `Job.eta_seconds` (required, nullable): mean `duration_ms` of the job's last ≤ 20 measured items × (pending + running), **assuming one worker**; null below 3 measured items or when terminal. `job_item.duration_ms` written by the worker at commit (not for cancelled items) | With several workers (plan 4.5) the estimate is pessimistic; revisit then |
| Notification (1.7) | Local `Notification` API only, permission requested on the user's tick, one notification per terminal transition, text = short job id + counts | NFR-09: no sequence or input id in the notification |
| Vitest dialogs | `tests/setup.ts` polyfills `HTMLDialogElement.showModal/close` (jsdom lacks them) by toggling `open` | The real modal behaviour (focus, Escape) is checked in Playwright (`MSEL-02 (mock)`) |
| Real-backend e2e and the rate limit | `real.spec.ts` confirms the slow-model dialog when it appears (not inside the NF-06 timing loop) and MSEL-04 waits for `Retry-After` on 429 | With the npz default the suite is fast enough to hit the service's own reference limit (120/min) after NF-06; the limit is correct behaviour, not relaxed |
| Test on a copy of `dev.db` | `test_whole_protein_windows_match_the_reference_tiles` upgrades its copy to head first | Found in the container run (slow tests are skipped by `test-fast`): the copy was at 0004 |
| Not done in this pass | 2.1, 2.3, 3.5, 4.1, 4.6 not started; serving decision of 4.3 awaits Trọng's confirmation of `serving-decision-2026-11-18.md` | `acceptance-system-2026-11-18.md`, `plan-system.md` §11 |

## 14. System completion, wave 1 continued (2.1, 2.3, 3.5, 4.1) — 18 Nov 2026

| Topic | Implemented | Why / evidence |
|---|---|---|
| Protein footprint (2.1) | `GET /v1/jobs/{id}/footprint` (`JobFootprint`): per tile, the SQL mean of `analysis_cell` per position (probability and raw), protein coordinates, domain status, `training_peptide` from the snapshot's warning codes; **409** while the job is not terminal and for peptide jobs | Plan: "job protein đã xong". Values are means of stored cells, never a cross-tile average (VIZ-01/02) |
| Footprint chart keyboard path (2.1) | The SVG is `role="img"` with mouse click to open a tile; keyboard and screen-reader users use the table view, which has a link per tile | Focusable links inside SVG behave inconsistently across browsers; the table carries the same content (VIZ-03 axe passes) |
| Comparison charts (2.3) | Pure frontend from the comparison rows plus the saved analysis cells (probability of the same substitution); the existing sentence "the calibrated probability is never compared with a ΔPSI measurement" is reworded: it is compared only with the observed **event** ΔPSI ≥ 1 in the calibration chart | Calibration needs the probability; the event matches the model's definition P(ΔPSI ≥ 1). Mock comparison rows now null `predicted_dpsi_raw` for incompatible endpoints, as the backend does |
| Report (3.5) | `GET /v1/analyses/{id}/report?format=html[&download=true]`, `api/report.py`; Viridis by 11 fixed stops (shades may differ slightly from the d3 ramp; values are printed). PDF by the browser's print dialog; **no server-side PDF renderer** | Plan 3.5 keeps the installation small. The route sets its own CSP (`style-src 'unsafe-inline'`, no script, `img-src data:`); the middleware now adds its default API CSP only when a route has not set one |
| Backup/restore (4.1) | `ops/backup.py` (stdlib + docker CLI), `make backup`, `make restore BACKUP=`; Docker workspace volume read/written through a throw-away `postgres:16-alpine` container (already pulled), not through `api` | Works while `api` is stopped. A volume created this way has no Compose labels: `docker compose down -v` does not remove it (found in the round trip; `docker volume rm` needed) |
| Backup round trip on Docker | Done against a separate Compose project `df-ops01` restored from a backup of the live stack, then with both scratch volumes deleted; the live database was never overwritten | Avoids destroying the user's data for a test; content checksums and file hashes identical (`tests/results/backup-roundtrip.json`) |

## 15. Wave 1 closing and wave 2 start — 18 Nov 2026

| Topic | Implemented | Why / evidence |
|---|---|---|
| Visual regression (4.6, UX-01) | `frontend/e2e/visual.spec.ts`: 6 screens × light/dark × 1440/360 px, full page, Chromium, `maxDiffPixelRatio 0.002`, mock API; 24 baselines in `e2e/visual.spec.ts-snapshots/` | Pages without timestamps or random ids; a sticky header overlaps the top of a full-page capture (Playwright artefact, stable between runs). Baselines are rebuilt with `--update-snapshots` after an intended UI change |
| Screenshots (4.6) | `docs/screenshots/` retaken on a scratch copy of `dev.db` with the npz model; new 06b protein footprint, 07b report, 08b comparison charts. `report/assets/screenshots/` not changed | Report figures belong to branch 3. Seed-spread view not photographed: the host API has no PyTorch |
| Found by looking at the new screenshots | Comparison charts printed the same tick label several times on a narrow range and the Bland–Altman y label overlapped its ticks → d3 `tickFormat` and a wider left margin; test "a narrow residual range never repeats a tick label" | 2.3 follow-up |
| Manual accessibility (4.6) | Template `a11y-manual-2026-11-18.md` (keyboard K1–K12, screen reader S1–S6, colour C1–C4) for a person to fill | UX-02 cannot be automated |
| Model comparison (2.2) | `POST /v1/analyses/compare` (save=false → 200, nothing stored; save=true → 201, both analyses in one active project), `GET /v1/model-comparisons/{id}`, `.../export`, `GET /v1/projects/{id}/model-comparisons`; table `model_comparison` (migration 0006). Disagreement = \|P_B − P_A\| (common scale of two models); raw-score agreement by rank first | Plan 2.2. The plan says "danh sách ô bất đồng lớn nhất" without a measure; probability is the only scale two models share. Error code reuses `INVALID_REQUEST` (422, field `analysis_b`) for different sequences instead of a new code |
| "Compare with another model" | Scores the same saved input with the other model as a **new linked analysis** (A-5), then saves the comparison | Comparisons are between stored, immutable analyses, so the second side has provenance too |
| Comparison page at 360 px | Flex items of the figure row may shrink (`min-width: 0`); the heatmap scrolls in its box | Found by the new CMP mock e2e (60 px overflow) |

## 16. Wave 2 — 18 Nov 2026 (2.6, 3.3, 3.4, 4.2, 4.5, 5.1, 5.4)

| Topic | Implemented | Why / evidence |
|---|---|---|
| Candidates (2.6) | `GET /v1/analyses/{id}/suggestions[?compare_with=&format=csv]` (`api/suggestions.py`); thresholds fixed in code: \|ΔP\| ≥ 0.2, seed SD ≥ 75th percentile of the tile within the top 10 %, ClinVar variants of the snapshot with matching reference residue | The plan names the criteria, not their thresholds; they are returned in `criteria` and printed in the CSV |
| Several proteins (3.3) | `JobRequest.proteins` (1–20) in protein mode; item ids `p<k>t<tile>`; coverage version 2 lists one coverage per protein; footprint takes `input_id` | Unknown accession, letters, a too-short protein or another release refuse **that protein** (one item `p<k>t00000`); request-shape errors and the total residue limit refuse the job |
| CLI and client (3.4) | `python -m api.cli`, `api/client.py` (urllib, no new dependency); `--offline` calls the service's own functions in-process | The runtime has no httpx; the notebook is tested by executing its code cells against a live app (no Jupyter in the image) |
| Admin page (4.2) | `GET /v1/admin/status`, `POST /v1/admin/registry/reload`; new error code `LOCAL_ONLY` (403); setting `DF_ADMIN_ALLOWED_NETWORKS` (loopback; compose adds private ranges because the API sees the Docker bridge address of `web`, whose port is bound to 127.0.0.1) | A request is admitted on its client address (X-Forwarded-For when `DF_TRUST_PROXY`); the address check is not authentication |
| Worker heartbeat (4.2/4.5) | Migration 0007 `worker_heartbeat`, written at most every 5 s, stamped on stop; alive = reported within 30 s | Without it the admin page could not tell a stopped worker from an idle one (OPS-04) |
| Priority and running limit (4.5) | Migration 0008 `analysis_job.priority`; claim orders by priority then age and skips jobs with ≥ `DF_JOB_MAX_RUNNING_ITEMS` (2) live items; `JobRequest.priority` "high" can only raise | The running limit is checked in the claim query: two workers claiming at the same instant could exceed it by one (soft limit). The job ETA (1.7) now divides by min(alive workers, 2) |
| Glossary (5.1) | `src/lib/glossary.ts`; "domain gate", "raw score" and "top 10 %" are not in `srs.md` §1.4 and follow the interface texts | Terms are explanations; the limitation labels next to the numbers are unchanged (R-1) |
| Tests and the first-visit guide | Vitest marks the guide as seen in `beforeEach`; Playwright sets the flag in `storageState`; the guide and glossary tests start from an empty storage | Otherwise every test would see the guide |
| Glossary buttons | 44 px hit area with negative margins | The 360 px test requires 44 px targets (NFR-12) |
| Presentation mode (5.4) | Alt+Shift+P; sessionStorage flag only | No conflict with NVDA/Orca default keys (they use Insert/CapsLock modifiers) |

## 17. Wave 3 start — 18 Nov 2026 (1.6 preparation, 4.4, 5.2) and 1.4

| Topic | Implemented | Why / evidence |
|---|---|---|
| Gate policy per model (1.6) | Proposal only: `research/lora-refit-transfer-2026-11-16/gate-policy-proposal-2026-11-18.md` (strata of T, options A/B/C, recommendation A, decision fields empty). **No code change**; R3 stays for every model | Plan 1.6: "không triển khai khi chưa có biên bản" |
| Agreement over time (4.4) | `GET /v1/projects/{id}/agreement` built from the stored `comparison` rows (no new table); flag rule n ≥ 5, ≥ 2 earlier comparable points, MAE > 1.25 × their mean or Spearman more than 0.2 below their mean | The plan leaves "xấu đi đáng kể" open; the rule is returned in `rules` and printed under the chart |
| Shortcuts (5.2) | Single keys v, t, /, ? with an off switch (WCAG 2.1.4); ignored in fields, with modifiers and inside dialogs | Screen readers in browse mode consume single keys first; the off switch covers dictation and focus mode |
| Shortlist (5.2) | Pins in the ranking table (☆/★) and a "Pinned" list; the plan's "shortlist" had no separate UI before (2.11 is the priority panel) | Remembered with filter and sort under `df-view:analysis:<id>` or `df-view:tile:<acc>:<n>`; typed previews never |
| LoRA-D speed (1.4) | `DF_LORA_BATCH`, `DF_LORA_MERGE` (merge W + α/r·BA at load) in `lora.py`, default unchanged; `tests/measure_lora_speed.py` → `tests/results/lora-speed.json` | Step a: the backbone forward is ≈ all of the time; batch size changes nothing measurable; 6 threads ≈ −16 %; merging ≈ −2–3 % with max \|Δ\| 5.0e-6 vs the fixture (≤ 1e-5: same model id allowed). "Compute WT once for all seeds" is not possible: each seed's LoRA changes the backbone. ONNX/GPU (c, d) not done. Target p95 ≤ 15 s/tile **not met** |
| Compose and LoRA knobs (1.4) | `DF_LORA_MERGE` and `DF_LORA_BATCH` passed to the backend containers (defaults: no merge, built-in batch) | Needed for the PERF-01 run in Docker; `.env` unchanged |
| `measure_latency_lora.py` with the cache (1.4) | Each model measured once even when LoRA-D is the default; warm-up on a tile outside the measured ones | Found 18 Nov: with LoRA-D as default the second pass hit the prediction cache (1.2) and overwrote the first (p50 23.5 ms, void); re-measured |
| Several worker containers (4.5) | `docker compose up -d --scale worker=3`: 3 jobs × 12 items finished in 3.1 s (npz), 15/13/8 items per worker, all attempts 1, 36 analyses, no duplicate (`tests/results/workers-scale.json`); scaled back to 1 | Plan 4.5 asks for a run with several real worker containers besides the in-process threads of BATCH-11 |
