# Test Plan

Status: **draft v0.1, 22 Oct 2026.** No test listed here has been written or run except the four back-to-back checks that already exist in `research/calibration-p6-2026-10-22/verify.py` (marked ✔ existing). Headings follow the Faculty outline used in Chapter 4, §4.3–4.6 of the thesis (§9 maps them). Requirement ids are those of [srs.md](srs.md).

## 1. Functions under test

UC-01 to UC-07 and the requirements FR-01 to FR-23, NFR-01 to NFR-20 of the SRS: the inference package, the REST API, the ETL, the database migrations and the React interface. The research code itself is **not** under test here; its correctness is the subject of the experiments in Chapter 4, §4.2.

## 2. Approach

| Level | Idea | Tools |
|---|---|---|
| Unit (UT) | Small functions with known answers; the 180-feature builder is compared with a second, independent implementation (`derisk.featurize`) | pytest |
| Property (PB) | Many generated inputs, asserting invariants (532 finite cells, coded errors, determinism) | pytest + hypothesis |
| Back-to-back regression (RG) | The service path equals the research path to 1e-9 on all 92,337 cells; a golden file freezes the CSV | pytest, `verify.py` (✔ existing) |
| API contract (API) | Every endpoint and error code against `openapi.yaml`; behaviour tests per rule of [api-spec.md](api-spec.md) | pytest + httpx, schemathesis |
| ETL (ETL) | Hash gate, idempotence, licence block, tile reconstruction against the 176 training peptides | pytest on a PostgreSQL container |
| End-to-end (E2E) | Each use case through a real browser: main flow and every alternative flow of the SRS | Playwright |
| Non-functional (NF) | Latency, memory, limits, measured on the reference host | locust (light), `docker stats`, browser traces |
| Security/privacy (SEC) | Fuzzed input, log inspection, token handling, headers, dependency audit | pytest, schemathesis fuzz, `pip-audit`, `npm audit` |
| Accessibility (A11Y) | Automated rules plus manual keyboard and colour-vision checks | axe-core (via Playwright), manual checklist |
| Deployment (DEP) | Clean-checkout install on each target | shell scripts, manual log |

**What back-to-back agreement does and does not show.** It shows that the tool computes what the research code computed. It does not show that the research quantity is right (an error shared by both paths would pass). The 180 features are rebuilt independently in the tool, so a path is not checked against itself, but the label definition and the trained weights are shared. The evidence label in the interface exists because of this limit.

## 3. Pass and fail criteria

* Numerical: largest absolute difference between service and research path **< 1e-9** for JSON values; **< 5e-9** for CSV values (ten significant digits are written).
* Functional: the observed result equals the expected result column; error responses have the exact `code` and, where stated, `field`.
* Performance: a threshold is *met* only when the p95 of at least 200 requests on the reference host (§7) is below the value in the SRS; the host, the number of requests and the date are recorded.
* A11Y: zero `serious`/`critical` axe violations on every page and all manual checks passed.
* A test fails if any of its assertions fails or if it errors; a skipped test is reported as skipped, not passed.

## 4. Suspension and restart

The suite stops at the first failing **RG** or **ETL** test (everything downstream depends on them). Restart: rebuild the model file, reload the database with `make etl` from an empty schema, and run the suite from the start. Test data that mutate the database use a transaction rolled back after each test or a throw-away schema.

## 5. Test environments

| Id | Where | Used for |
|---|---|---|
| E-DEV | Linux under WSL2 on the author's computer (CPU only; Python 3.12.3, NumPy as pinned) — the environment that ran `verify.py` | UT, PB, RG, API (SQLite), ETL (PostgreSQL in Docker), E2E |
| E-CI | A CI runner or `make test` in a clean container | Everything except NF and DEP-02; coverage |
| E-REF | **Reference host: 2 vCPU, 2 GB RAM** (a small VPS or the free-tier instance chosen for the demo; the product is recorded in the report) | NF-01…NF-06, DEP-02 |
| E-BROWSER | Latest two releases of Chrome, Firefox, Safari (or WebKit via Playwright), Edge; viewport 360 × 800 and 1280 × 800 | E2E matrix, A11Y |

Everything that can be tested on a local machine is; E-REF is needed only for numbers that depend on the host.

## 6. Test cases

*Exp.* = expected result. "✔ existing" = a corresponding check exists today in `verify.py`/`verify.json`.

### 6.1 Unit (UT)

| ID | Requirement | Description | Exp. |
|---|---|---|---|
| UT-01 | FR-04 | `featurize(seq,pos,aa)` equals `derisk.featurize` for every cell of the 176 training peptides ✔ existing | max \|Δ\| < 1e-9 (measured 1.1e-16) |
| UT-02 | FR-04 | Boundary positions 1 and 28, and context offsets beyond the tile ends, give the expected zero blocks | exact |
| UT-03 | FR-05 | Platt and isotonic calibrators against precomputed sklearn outputs ✔ existing | < 1e-9 |
| UT-04 | FR-08 | Ranking is a permutation of 1…532; ties broken stably; exactly ⌈10 % · 532⌉ = 54 cells flagged | exact |
| UT-05 | FR-16 | Tile generator: `n_max = (L−28)//23+1`; tile *n* starts at (n−1)·23+1; proteins shorter than 28 have none; last window is full | exact |
| UT-06 | FR-09 | Mapping (PSI, reads) → domain status at the boundaries 4.0, 4.0+ε, reads 9/10, PSI NA | exact |
| UT-07 | FR-01 | Normalisation: case, surrounding whitespace; internal whitespace rejected | exact |
| UT-08 | FR-12 | CSV writer: provenance lines, nine columns, `%.10g` formatting, 532 rows | exact vs golden |
| UT-09 | FR-22, NFR-06 | Loading weights whose hash differs from the registry raises and marks the service not ready | raises |
| UT-10 | FR-20, NFR-10 | Expiry logic: `expires_at` ≤ 30 days; purge removes expired runs and cascades cells | exact |

### 6.2 Property (PB)

| ID | Requirement | Property |
|---|---|---|
| PB-01 | FR-01 | Any 28-string over the 20 letters: 532 cells, all finite, probabilities in [0,1] |
| PB-02 | FR-03 | Any string with a wrong length or a character outside the alphabet: coded error, no scores, no exception text |
| PB-03 | NFR-05 | Same input and model twice: identical bytes |
| PB-04 | FR-08 | Ranks form a permutation; the highest raw score has rank 1 |
| PB-05 | FR-05 | Calibrated probability is non-decreasing in the raw score |

### 6.3 Back-to-back regression (RG)

| ID | Requirement | Description | Exp. |
|---|---|---|---|
| RG-01 | NFR-04, FR-04, FR-05 | Run the eleven checks of `verify.py` against the service code path (labels, features, raw score, Platt and isotonic, UniProt → tile path, fold coefficients, CSV) ✔ existing for the CLI | all < 1e-9 |
| RG-02 | FR-12, NFR-04 | API CSV of tile `A6NMZ7_28` equals `example-output.csv` after dropping `#` lines | max \|Δ\| < 5e-9 |
| RG-03 | NFR-06 | SHA-256 of the packaged weights equals the registry and the value in the model card | equal |
| RG-04 | FR-04 | For all 176 training peptides, UniProt-derived tile → service scores equal the training-path scores ✔ existing (difference 0) | < 1e-9 |

### 6.4 API (API)

| ID | Requirement | Description | Exp. |
|---|---|---|---|
| API-01 | FR-01, FR-14 | `POST /v1/predict` with a valid sequence | 200; 532 cells; full provenance; `Cache-Control: no-store` |
| API-02 | FR-02 | Same with `uniprot_id` + `tile_index` | 200; `tile` has coordinates |
| API-10 | FR-03 | Invalid JSON; unknown field; both or neither of `sequence`/`uniprot_id` | 400/422 `INVALID_REQUEST` |
| API-11 | FR-03 | Sequence of 27 and 29 | 422 `INVALID_LENGTH`, `field=sequence`, message gives the length |
| API-12 | FR-03 | Sequence containing `B`, `X`, digit, space inside, `*` | 422 `INVALID_CHARACTER` naming character and position |
| API-13 | FR-03 | Unknown accession | 404 `UNKNOWN_ACCESSION` |
| API-14 | FR-03 | `tile_index` 0 and `n_max+1` | 422 `TILE_OUT_OF_RANGE` (message gives `n_max`) |
| API-15 | FR-03 | Tile with a non-standard residue | 422 `TILE_NOT_SCORABLE` |
| API-16 | FR-22 | Unknown `model_id`; a `candidate` model | 404 `MODEL_NOT_FOUND` |
| API-17 | NFR-07 | Body of 5 KiB | 413 `PAYLOAD_TOO_LARGE` |
| API-18 | FR-09 | Tiles of each status class (fixture rows) | `domain.status` as stored; typed sequence equal to a stored tile stays `unknown` |
| API-19 | FR-10 | `measured_out_of_domain` fixture without and with `override_domain` | 422 `OUT_OF_DOMAIN`; then 200 with `OUT_OF_DOMAIN_OVERRIDDEN` |
| API-20 | FR-15 | `GET /v1/proteins?query=COL6` and an accession prefix; 1-character query | results ranked; 422 for short query |
| API-21 | FR-16 | Tiles of a protein | all tiles, statuses, count equals `n_max` |
| API-22 | FR-17 | Measured overlay for a training tile and for a non-training tile | cells with `in_training_set=true`; empty list |
| API-23 | FR-18, NFR-14 | ClinVar overlay | ClinVar attribution and disclaimer in `provenance.disclaimers`; `clinvar_file_date` present |
| API-24 | FR-19, FR-22 | `GET /v1/models`, `/v1/models/{id}` | default listed first; metrics carry `metrics_source_file` |
| API-25 | FR-21 | `GET /v1/sources` | no source with `redistribution_ok=false` is listed |
| API-26 | NFR-06 | `/healthz` with weights present, missing, hash mismatch, database down | ok / 503 as specified |
| API-27 | NFR-07 | 61 requests in one minute from one client | 429 `RATE_LIMITED` with `Retry-After` |
| API-28 | NFR-12 | CORS preflight from an allowed and a disallowed origin | allowed / refused |
| API-30 | FR-12, FR-14 | `POST /v1/export` format `csv` | provenance lines; nine columns; 532 rows |
| API-31 | FR-13, FR-14 | Same with `json` | equals the `/predict` body plus `exported_at` |
| API-32 | FR-03 | Unknown `format` | 400 `INVALID_FORMAT` |
| API-40 | FR-20 | `POST /v1/runs` | 201; token returned once; DB stores only the hash |
| API-41 | FR-20 | `GET /v1/runs/{id}` with the token | 200; equals the original result |
| API-42 | FR-20 | Missing and wrong token | 401 `TOKEN_REQUIRED`; 404 `RUN_NOT_FOUND` for a wrong token |
| API-43 | FR-20, NFR-10 | Read after `expires_at` | 410 `RUN_EXPIRED`; row purged by the job |
| API-44 | FR-20 | Export of a shared run (csv, json) | as API-30/31 |
| API-50 | all | schemathesis over `openapi.yaml`, all endpoints, positive and negative generation | no 5xx; all responses conform to schema |

### 6.5 ETL (ETL)

| ID | Requirement | Description | Exp. |
|---|---|---|---|
| ETL-01 | DR-3 | Alter one byte of an input file | Run aborts, `etl_input` shows expected ≠ actual |
| ETL-02 | DR-3 | Run twice on unchanged input | Second run: 0 inserted, 0 updated; row counts equal |
| ETL-03 | NFR-13 | Register a source with `redistribution_ok=false` and try to load a table from it | Aborts; nothing loaded |
| ETL-04 | FR-16, DR-2 | For the 176 training peptides, UniProt-derived tile sequence equals the training sequence | 0 mismatches |
| ETL-05 | FR-09 | Counts of tiles per `domain_status`, screen ids unmatched, ClinVar reference mismatches | Report written; matches expectations in the report; no negative or missing counts |

### 6.6 End-to-end (E2E)

| ID | UC / Requirement | Scenario | Exp. |
|---|---|---|---|
| E2E-01 | UC-01, FR-06 | Paste a valid sequence, predict | Warning (`unknown`) before the heatmap; 28 rows × 19 cells + wild-type cells; model id and evidence label visible |
| E2E-02 | UC-02, FR-07, FR-08 | Sort by probability, filter position 14 and amino acid W | Only matching rows; filter with no rows shows the message; top-10 % column reads "yes" for rank ≤ 54 |
| E2E-03 | UC-03, FR-12, FR-13 | Download CSV and JSON | Files contain provenance; values equal the on-screen table |
| E2E-04 | UC-04, FR-02, FR-15, FR-16 | Search a gene, pick a tile, predict | Tile map with statuses; result page for the tile |
| E2E-05 | UC-05, FR-17 | Switch on measured layer for a training tile | Overlay and the "included in training" caption |
| E2E-06 | UC-06, FR-18, NFR-14 | Switch on ClinVar layer | Attribution and disclaimer directly beside the toggle and in hover card |
| E2E-07 | UC-07, FR-19, FR-21 | Open model card and About | Metrics from the API; excluded sources listed (`ModelCard.not_used_sources`, the ETL block list); licences table |
| E2E-08 | FR-03 | Invalid sequences (short, 'B', empty) | Inline specific message; focus on the field; no request for client-detectable errors |
| E2E-09 | FR-10 | Out-of-domain fixture; "Score anyway" | Refusal page with reason; after override a red banner and warning in the export |
| E2E-10 | FR-23 | Simulate export failure (blocked route) | Error message; result still displayed |
| E2E-11 | FR-20 | Create share link; open in a new context | Token only in URL fragment; same result; expired link shows the expiry message |
| E2E-12 | FR-05, FR-11, FR-14, NFR-15 | On every result variant (known, unknown, unreliable, training, overridden) | Domain banner first; event definition near probabilities; evidence label; disclaimer in provenance footer |

### 6.7 Non-functional (NF)

| ID | Requirement | Measurement | Threshold |
|---|---|---|---|
| NF-01 | NFR-01 | 200+ sequential and 10-way concurrent `POST /v1/predict`; p50/p95/p99 | p95 ≤ 300 ms *(to be measured)* |
| NF-02 | NFR-02 | Tiles list of a 1,000-residue protein | p95 ≤ 200 ms *(to be measured)* |
| NF-03 | NFR-18 | API container memory after warm-up and under NF-01 | ≤ 512 MB *(to be measured)* |
| NF-04 | NFR-07 | Rate limit behaviour (as API-27) under load | no 5xx; limit applied |
| NF-05 | NFR-07 | Oversized and malformed bodies at volume | 413/400 only; service healthy |
| NF-06 | NFR-03 | Browser trace: click "Predict" → heatmap painted, 20 runs, standard laptop | p95 ≤ 1.5 s *(to be measured)* |

### 6.8 Security and privacy (SEC)

| ID | Requirement | Description | Exp. |
|---|---|---|---|
| SEC-01 | NFR-09, NFR-19 | Run requests with a canary sequence, canary accession and share token; grep all logs and the database | Canary absent from logs; present in DB only for an explicit share run |
| SEC-02 | NFR-08 | Fuzz: very long strings, Unicode, control characters, SQL and path metacharacters in every field and path parameter | Coded 4xx; no 5xx; no echo of raw input in error messages beyond the validated character |
| SEC-03 | — | Security headers (CSP without `unsafe-inline`, `X-Content-Type-Options`, `Referrer-Policy: no-referrer`) | Present |
| SEC-04 | NFR-09 | Share token | DB holds only SHA-256; token in response once; not in any URL path or query |
| SEC-05 | — | `pip-audit`, `npm audit` | No known high/critical vulnerability unaddressed |

### 6.9 Accessibility (A11Y)

| ID | Requirement | Description | Exp. |
|---|---|---|---|
| A11Y-01 | NFR-11 | axe-core on Input, Tile picker, Result (each variant), Model card, About, in light and dark themes | 0 serious/critical |
| A11Y-02 | NFR-11 | Complete UC-01 to UC-03 with keyboard only | Possible; focus visible; no trap |
| A11Y-03 | NFR-11 | Simulate protanopia, deuteranopia, tritanopia on heatmap, tile map, ClinVar markers | Information still recoverable from patterns, shapes and text |
| A11Y-04 | NFR-11 | Contrast check of text and components | ≥ 4.5 : 1 text, ≥ 3 : 1 UI |

### 6.10 Deployment (DEP)

| ID | Requirement | Description | Exp. |
|---|---|---|---|
| DEP-01 | NFR-06, NFR-16, NFR-20 | From a clean checkout: `docker compose up`, run migrations and ETL, open the app | Works; a deliberately corrupted weights file prevents readiness |
| DEP-02 | NFR-20 | Follow the install guide on (a) a free-tier host and (b) a rented VPS, whichever is used for the demo; record product and plan | Reachable over HTTPS; NF suite run on it |

## 7. Test management

| Item | Plan |
|---|---|
| Activities | Write UT/PB/RG first (they gate the rest), then ETL and API, then E2E, then NF/SEC/A11Y/DEP on E-REF; re-run the full suite before each model release |
| Order of execution | RG and ETL first; failures stop the run (§4) |
| Resources | One person, the author, who is developer and tester. There is no independent tester; this is stated as a threat to validity in Chapter 4 |
| Test data | Fixtures: the 176 training tiles; a handful of synthetic rows for every `domain_status`; `example-output.csv`; a canary for SEC-01. No third-party private data |
| Defect handling | Each failing test gets a short note (what, which requirement, fix commit) in the test report |
| Risks | (1) Shared-error blind spot of RG (§2). (2) Probabilities low by about 13 % on the original domain; the tests check ranking and consistency, not truth. (3) No external validation exists; no test can supply it. (4) A free-tier host may be slower than E-REF figures; NF numbers are valid only for the recorded host. (5) A11Y automated rules find only part of the issues; the manual checks are required |

## 8. Test deliverables

Test code under `app/tests/`, the generated `verify`-style JSON for RG, coverage and results reports from CI, a measurements table for NF (host, count, percentiles, date), the A11Y checklist, and the test report whose summary feeds Chapter 4. The numbers in that chapter are generated from the result files by a script, as for the experiments.

## 9. Mapping to the thesis template (Chapter 4)

| Template heading | Content from this plan |
|---|---|
| 4.3 Software Testing Plan | §1 functions, §2 approach, §3 criteria, §4 suspension and restart, §8 deliverables |
| 4.4 Test Management | §5 environments, §7 activities, resources, risks |
| 4.5 Test Scenarios and Test Cases | §6 (scenario = a use case; case = a row) |
| 4.6 Test Evaluation | The report: pass/fail counts per group, NF measurements, A11Y results, and a statement of what the tests do **not** show (§2, last paragraph) |

The existing Chapter 4 text covers UC-01 to UC-03 through back-to-back testing only (11 checks); input validation, interface, performance and usability remain `[PENDING]` there until the groups above are executed.
