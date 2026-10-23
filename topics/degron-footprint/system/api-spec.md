# API Specification

Machine-readable contract: [openapi.yaml](openapi.yaml) (OpenAPI 3.1, checked with `openapi-spec-validator`: valid, 13 paths, 26 schemas). This file explains the rules the schema cannot express. Status: **draft v0.1 (22 Oct 2026)**; backend and frontend are both written against it. Where this text and `openapi.yaml` disagree, fix both in the same change.

## 1. Conventions

| Topic | Rule |
|---|---|
| Base path | `/v1`; a breaking change creates `/v2`. `/healthz` is unversioned |
| Format | JSON in and out (`application/json`), UTF-8. Exports may be `text/csv` |
| Naming | `snake_case` fields. Column names of the cells (`score_dpsi_raw`, `p_dpsi_ge_1_calibrated`, `rank_in_tile`, `top10pct_in_tile`) are identical to the command-line prototype and to its CSV, so a golden file serves both |
| Positions | `position` is 1-based **inside the tile** (1…28). `start_pos`/`end_pos` are protein coordinates |
| Cell count | Always exactly **532** cells per prediction (28 × 19), in the order position ascending, then amino acid in the alphabet `ACDEFGHIKLMNPQRSTVWY` without the wild-type letter |
| Time | RFC 3339 UTC |
| Headers | Every response has `X-Request-Id`. Predictions have `Cache-Control: no-store`. No cookies are set |
| Auth | None. Share links use a bearer-style token in the `X-Share-Token` header |
| CORS | Allow-list of the web origin set by configuration; no wildcard in production |

## 2. Endpoints

| Method | Path | Use case | Stores data? |
|---|---|---|---|
| `POST` | `/v1/predict` | UC-01, UC-02 | No |
| `POST` | `/v1/export` | UC-03 | No |
| `GET` | `/v1/proteins?query=` | UC-04 | No |
| `GET` | `/v1/proteins/{uniprot_id}/tiles` | UC-04 | No |
| `GET` | `/v1/proteins/{uniprot_id}/tiles/{tile_index}/measured` | UC-05 | No |
| `GET` | `/v1/proteins/{uniprot_id}/tiles/{tile_index}/clinvar` | UC-06 | No |
| `GET` | `/v1/models`, `/v1/models/{model_id}` | UC-07 | No |
| `GET` | `/v1/sources` | About / licences | No |
| `POST` | `/v1/runs` | optional share (UC-03 variant) | **Yes**, ≤ 30 days |
| `GET` | `/v1/runs/{run_id}`, `/v1/runs/{run_id}/export?format=` | share | reads |
| `GET` | `/healthz` | operations | No |

**Differences from the first plan** (`next-phase-plan §4.6`), made because the UI needs them: added `GET /v1/proteins?query=` (search by gene or accession), added `GET /v1/sources` (About page) and stateless `POST /v1/export` (so that exporting does not force the server to store the sequence), and the overlay endpoints use `(uniprot_id, tile_index)` instead of a surrogate `tile_id`, which clients cannot know.

## 3. Request validation (`POST /v1/predict`, `/v1/export`, `/v1/runs`)

Validation runs in this order and stops at the first failure.

1. Body is JSON, at most **4 KiB** ⇒ else `400 INVALID_REQUEST` / `413 PAYLOAD_TOO_LARGE`.
2. Unknown fields are rejected ⇒ `422 INVALID_REQUEST` (`field` is `null`: the unknown name is not echoed). The three request schemas (`PredictRequest`, `ExportRequest`, `RunRequest`) are closed and written out in full in `openapi.yaml`; they share only the rule of rule 3 (`RequestTarget`). `POST /v1/export` needs `format` (`csv`|`json`): missing is `422 INVALID_REQUEST` with `field: format`, a wrong value is `400 INVALID_FORMAT`.
3. **Exactly one** of `sequence` or (`uniprot_id` + `tile_index`) ⇒ else `422 INVALID_REQUEST`.
4. `sequence`: trim whitespace, upper-case. Length must be exactly 28 ⇒ else `422 INVALID_LENGTH` (message states the actual length). Every character must be one of the 20 standard letters ⇒ else `422 INVALID_CHARACTER` (message names the first offending character and its position; `B`, `J`, `O`, `U`, `X`, `Z`, digits, gaps and `*` are rejected).
5. `uniprot_id`: must match the accession pattern ⇒ else `422 INVALID_REQUEST`; must exist ⇒ else `404 UNKNOWN_ACCESSION`.
6. `tile_index`: integer ≥ 1 and ≤ `n_max` of the protein ⇒ else `422 TILE_OUT_OF_RANGE` (message gives `n_max`). The tile must be scorable ⇒ else `422 TILE_NOT_SCORABLE`.
7. `model_id`, if given, must exist and be `frozen` and have role `effect` ⇒ else `404 MODEL_NOT_FOUND`.
8. Domain gate (§4).

## 4. Domain handling: the rule that protects the user

| `domain.status` | Source of the status | Behaviour of `predict` | Warning code in response |
|---|---|---|---|
| `measured_in_domain` | tile measured, PSI ≤ 4.0 | Scores returned | none (or `TRAINING_PEPTIDE`) |
| `measured_unreliable` | in the screen, too few reads | Scores returned | `DOMAIN_UNRELIABLE` |
| `unknown` | user sequence, or tile not in the screen, no gate model | Scores returned | `DOMAIN_UNKNOWN` |
| `predicted_in_domain` | gate model (R3), when it exists | Scores returned | `PREDICTED_DOMAIN` |
| `predicted_out_of_domain` | gate model | **Refused** (`422 OUT_OF_DOMAIN`) unless `override_domain = true` | `PREDICTED_DOMAIN`, plus `OUT_OF_DOMAIN_OVERRIDDEN` if overridden |
| `measured_out_of_domain` | tile measured, PSI > 4.0 | **Refused** (`422 OUT_OF_DOMAIN`) unless `override_domain = true` | `OUT_OF_DOMAIN_OVERRIDDEN` if overridden |

`TRAINING_PEPTIDE` is added whenever the tile is one of the 176 training peptides, in any status.

A user-typed `sequence` that happens to equal a stored tile is **not** looked up: the status stays `unknown`. Sequence matching would let the server infer and keep information about the input, and the gate for typed sequences is the job of the future gate model.

Chapter 1 (UC-01 alternative flow) says an out-of-domain input gets an explicit message and no scores. The refusal above implements that for the *measured* case; the `override_domain` escape hatch and the `unknown` case are additions that need the author's approval (see `chapter-sync.md`, item C1-3).

## 5. Error model

Every non-2xx response has this body, with a stable `code`:

```json
{ "code": "INVALID_LENGTH", "message": "The sequence must have exactly 28 amino acids; it has 27.", "field": "sequence" }
```

| HTTP | `code` | When |
|---:|---|---|
| 400 | `INVALID_REQUEST` | Body is not valid JSON; missing required query parameter (`GET /v1/proteins` without `query`; `GET /v1/runs/{id}/export` without `format`) |
| 400 | `INVALID_FORMAT` | `format` is neither `csv` nor `json` |
| 401 | `TOKEN_REQUIRED` | Share link read without a valid `X-Share-Token` |
| 404 | `UNKNOWN_ACCESSION` · `MODEL_NOT_FOUND` · `RUN_NOT_FOUND` · `TILE_OUT_OF_RANGE` (overlay endpoints only) | Unknown resource. A wrong token on an existing run also returns `RUN_NOT_FOUND`, so that run ids cannot be probed. A `model_id` that does not match the id pattern is `MODEL_NOT_FOUND`, not 422 |
| 404 / 405 | `INVALID_REQUEST` | Unknown route or wrong method. Not listed per operation in `openapi.yaml` (no operation exists to attach it to); the body is the usual `Error` |
| 410 | `RUN_EXPIRED` | Shared run past `expires_at` |
| 413 | `PAYLOAD_TOO_LARGE` | Body above 4 KiB |
| 422 | `INVALID_REQUEST` · `INVALID_LENGTH` · `INVALID_CHARACTER` · `TILE_OUT_OF_RANGE` · `TILE_NOT_SCORABLE` · `OUT_OF_DOMAIN` | Validation and domain gate (§3, §4), and malformed path or query parameters of the GET endpoints (accession pattern, non-integer `tile_index`, `query` shorter than 2 characters, `limit` out of range, run id that is not a UUID). A field that the contract does not know is a 422 with `field: null`: the name is attacker-controlled text and is not echoed |
| 429 | `RATE_LIMITED` | Over the rate limit; `Retry-After` header set |
| 500 | `INTERNAL_ERROR` | Unexpected; the message never contains input or stack traces |
| 503 | `SERVICE_UNAVAILABLE` | Model file missing or hash mismatch; database unavailable; no model serving (reference endpoints); no ClinVar rows loaded (ClinVar overlay) |

The messages are written for the person who typed the input and name the problem and the fix.

## 6. Provenance (mandatory)

Every 200 response that carries scores or overlays has a `provenance` object, and every export contains the same information (UC-03):

| Field | Source |
|---|---|
| `model_id`, `model_kind`, `weights_sha256`, `feature_spec` | `model_version` |
| `event_definition` | `model_version` — what the probability is of (`P(ΔPSI ≥ 1.0)`) |
| `evidence_label` | `model_version` — "development OOF benchmark, not external validation" |
| `domain_description` | `model_version` |
| `data_sources[]` | `data_source` rows for the model's training sources and for any overlay used |
| `code_version`, `generated_at` | Build and request time |
| `disclaimers[]` | At least: scores are not probabilities of disease. Adds the ClinVar diagnostic disclaimer when `data_sources` contains ClinVar |

The server refuses to start (`SERVICE_UNAVAILABLE` on `/healthz`) if `weights_sha256` of the loaded file differs from the registered value.

## 7. Export formats

**JSON.** The `PredictionResult` object plus `exported_at`.

**CSV.** UTF-8, `\n` line ends. Provenance first as comment lines starting with `# key=value`, one per line, then a header row and 532 data rows with the same nine columns as the command-line prototype:

```
# model_id=m3-ext4.0-platt-v1
# weights_sha256=8bec0b04…cd9c3
# event_definition=P(DeltaPSI >= 1.0)
# evidence_label=development OOF benchmark, not external validation
# domain_status=measured_in_domain
# data_sources=zhang2023-mendeley-v2,uniprot-2026_03,zhang2023-geo-gse240610
# generated_at=2026-10-22T12:00:00Z
# disclaimer=Not a probability of disease; not for diagnostic use.
peptide,tile,position,wt_aa,mut_aa,score_dpsi_raw,p_dpsi_ge_1_calibrated,rank_in_tile,top10pct_in_tile
A6NMZ7_28,28,1,D,A,-0.04768813161,0.02801670181,410,0
```

Readers that understand a comment prefix (`pandas.read_csv(..., comment='#')`) ignore the provenance lines. Numbers are written with ten significant digits (`%.10g`), as the prototype does, so a client can compare to the runner at 5e-9. For a typed sequence `peptide` is `user_seq` and `tile` is `0`. File names: `degron-footprint_<model_id>_<uniprot_id>-t<n>_<date>.csv` or `…_user-seq_<date>.csv`; the sequence itself is never part of a file name.

## 8. Limits (proposed, *to be measured and fixed with the NFRs*)

| Limit | Proposed value |
|---|---|
| Request body | 4 KiB |
| Rate limit | 60 requests per minute per client address on prediction endpoints; 120 on reference endpoints |
| `ttl_days` | 1–30, default 7 |
| `GET /v1/proteins` | `query` 2–32 characters; `limit` ≤ 50 |
| Response size | one prediction ≈ 70 KB uncompressed; gzip enabled |
| Latency target | in SRS NFR-01 / NFR-02 |

## 9. Privacy rules for implementers

* Do not log request bodies, the `sequence`, `uniprot_id`, `tile_index` or share tokens. Log method, route template (`/v1/proteins/{uniprot_id}/tiles`), status, duration and `X-Request-Id`.
* `usage_daily` counters are keyed by endpoint and model only.
* A share token is returned once; the database stores its SHA-256. The web client puts it in the URL **fragment** and sends it in `X-Share-Token`, so it does not reach access logs.
* The frontend must not call third-party services with user input (no analytics that receive sequences).

## 9a. Model card and sources not used

`GET /v1/models/{model_id}` returns, besides metrics and `trained_on_sources`, the array `not_used_sources` (`source_id`, `name`, `reason`): the sources that were examined and are deliberately neither served nor used for training (Koren 2018 Table S4, MetaDegron/ELM, Larsen 2025). The list is generated by the server from the same constant as the ETL's blocked-source list, so the page cannot disagree with what the code enforces; the model card page of the web client shows it (E2E-07). `GET /v1/sources` lists only the sources that are served.

## 10. Contract tests derived from this file

`schemathesis` runs against `openapi.yaml` for every endpoint and error code (test ids in [test-plan.md](test-plan.md), group API). Since the contract was reconciled with the implementation (22 Oct 2026) the status check is the one documented **per operation** in `openapi.yaml`. The `firstCells` example in `openapi.yaml` is an excerpt (three of 532 cells) and is therefore excluded from response validation.
