# Deviations from the design documents

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
