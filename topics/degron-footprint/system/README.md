# System: Degron Footprint Tool

Design documents of the web tool that wraps the frozen research model (v1: `m3-ext4.0-platt-v1`, ridge M3 trained with the relaxed threshold 4.0, Platt calibration). Written in English because they feed Chapters 1, 3 and 4 of the thesis directly. Status: **design draft v0.1, 22 Oct 2026. Nothing here is implemented**, no requirement is verified, and every threshold marked *(to be measured)* is a proposal. Origin: [next-phase plan §4](../research/next-phase-plan-2026-10-22/README.md).

## 1. Contents

| File | What it is | Read it for |
|---|---|---|
| [srs.md](srs.md) | Software requirements (ISO/IEC/IEEE 29148): scope, use cases UC-01…07, FR-01…23, NFR-01…20, constraints, traceability | What the tool must do and may not do |
| [db-design.md](db-design.md) | ER diagram, PostgreSQL DDL, data dictionary, licence per table, idempotent ETL, retention, sizes | Data model and loading |
| [openapi.yaml](openapi.yaml) | OpenAPI 3.1 contract (validated) | What backend and frontend both code against |
| [api-spec.md](api-spec.md) | Rules the schema cannot express: validation order, domain gate, errors, provenance, exports, privacy | Behaviour of each endpoint |
| [ui-design.md](ui-design.md) | Site map, wireframes, states, mandatory warnings, colours, ARIA, React components, state flow | Frontend |
| [test-plan.md](test-plan.md) | Test levels and ids (UT, PB, RG, API, ETL, E2E, NF, SEC, A11Y, DEP), environments, mapping to Chapter 4 | Verification |
| [chapter-sync.md](chapter-sync.md) | **Proposed** edits to thesis Chapters 1 and 3 — not applied | What the author must approve |

Planned, not yet created: `app/` (code), see §4.

**Reading order:** this file → `srs.md` §1–3 → `db-design.md` §3–4 → `openapi.yaml` + `api-spec.md` → `ui-design.md` → `test-plan.md`. Implementers of the backend need `db-design`, `openapi.yaml`, `api-spec`; of the frontend, `openapi.yaml`, `api-spec`, `ui-design`.

## 2. Decisions taken and why

| # | Decision | Reason |
|---|---|---|
| D-1 | Stack: FastAPI (Python 3.11) · React + TypeScript (Vite) · PostgreSQL 16 (SQLite for dev and unit tests) · Docker Compose | Chosen by the author (22 Oct). OpenAPI comes free from FastAPI; Playwright and axe fit React; inference needs only numpy |
| D-2 | Predictions are **stateless**; a row is stored only on an explicit share request, ≤ 30 days | Chapter 1 forbids keeping sequences beyond the session unless stated; no accounts, so no personal data |
| D-3 | Nothing is precomputed; scores are computed per request | 116,702 degron tiles × 532 cells ≈ 62 million rows would add nothing, since a score is one dot product |
| D-4 | A tile is 28 residues, step 23, numbered from 1 | Taken from `predict.py` and the GPS screen id convention |
| D-5 | Domain gate in two tiers: *measured* tile PSI from the GPS screen now; *predicted* from a gate model (R3) later. `measured_out_of_domain` is **refused unless the user overrides**; `unknown` is scored with a prominent warning | The model cannot tell by itself that a tile is stable. Chapter 1 asks for a refusal. The override and the `unknown` case are additions that need approval (chapter-sync C1-3) |
| D-6 | Typed sequences are never matched to stored tiles | Avoids the server inferring and retaining information about input; gate for typed sequences waits for R3 |
| D-7 | Share token is returned once, stored only as SHA-256, and carried in the URL **fragment** and the `X-Share-Token` header | Keeps it out of access logs and the database |
| D-8 | Measured ΔPSI overlay is labelled "included in the training data" | The 176 peptides are the training set; presenting them as validation would be false |
| D-9 | The service package and `predict.py` stay two independent implementations of the features; the API test compares them | Keeps back-to-back testing meaningful |
| D-10 | The ClinVar table is loaded with `--clinvar-scope` = `all`, `in-tiles` or `degron-only` | Free hosted databases have small storage caps |
| D-11 | Blocked sources (Koren, MetaDegron/ELM, Larsen) are enforced in the ETL and tested | A licence breach must be impossible by shortcut, not just discouraged |
| D-12 | Frontend types are generated from `openapi.yaml` | The contract cannot drift silently |

## 3. Status of the implementation (22 Oct 2026) and what is not yet verified

### 3.1 Built and run on the development machine

| Part | Evidence (command, result) |
|---|---|
| Contract | `openapi.yaml` validates with `openapi-spec-validator`; reconciled with the implementation (D-1…D-6 of `app/DEVIATIONS.md` closed); the three request schemas are closed and written out in full |
| Backend (`app/backend`) | 149 pytest tests passed, including agreement with the research runner (< 1e-9 on 92,337 cells) and schemathesis over all 13 endpoints with the statuses documented **per operation**; `ruff` and `mypy` clean; SQLite only |
| ETL | Ran on the real data into SQLite: 20,431 proteins, 482,216 tiles, 92,337 training cells, 2,338,863 ClinVar variants; second run changes 0 rows |
| Frontend (`app/frontend`) | `tsc`, `eslint`, `check:api` clean; vitest 131 tests passed; build 380 kB; Playwright (Chromium 156): 12 tests on the mock, 12 on the production build under the CSP, 11 against the real backend (`make -C app dev-api`) |
| Model card "sources not used" (E2E-07) | Served by the API (`ModelCard.not_used_sources`, generated from the same constant as the ETL's blocked-source list); rendered by the web client; tested on both sides |

### 3.2 Not verified (do not rely on these)

| Item | Why open | How to settle |
|---|---|---|
| **PostgreSQL** | Migration, ETL and API ran on SQLite only; the 30-day `CHECK` and `psycopg` binding are untested | Run `docker compose up` (or a local PostgreSQL) and the same suite with `DF_DATABASE_URL` set |
| **Docker Compose and the images** | No Docker on the development machine | `docker compose build && up`; then `nginx -t` in the `web` image |
| **nginx** (`frontend/nginx.conf`) and the proxy path (`DF_TRUST_PROXY`) | Never executed | Same run; check the CSP header and `/v1` proxying |
| **Reference host (2 vCPU / 2 GB)** | Latency and memory were measured on a shared laptop over loopback | NF-01…NF-06 on the chosen host, over TLS |
| **Browsers other than Chromium**, colour-blind simulation (A11Y-03) | Only Chromium 156 and axe were run | Firefox and WebKit in Playwright; a simulation tool |
| Tile numbering of the GPS screen vs UniProt 2026_03 | ETL-04 proves it for the 176 training peptides only; 16,266 screen rows sit just after the last full window (C-terminal tile, not served) | Decide whether to serve end-aligned tiles |
| Gate threshold: tile PSI (one replicate) ≤ 4.0 vs *intrinsic* PSI(WT) (two replicates) ≤ 4.0 | Different estimators | Experiment R3; until then the UI shows "measured tile PSI (replicate 1)" |
| GEO Table S1 terms | Recorded as "GEO terms (public)" only | Read the GEO policy and write it into `data/README.md` before any public release |
| Free-tier and VPS limits | Provider terms change | Read the provider's current limits when choosing |
| Wording "weakens the degron signal" | Interpretation of ΔPSI ≥ 1 for the interface | Supervisor review |
| Chapter 1 amendments | Not approved | `chapter-sync.md` |

## 4. Planned layout of `app/`

```
app/
  backend/
    degron_footprint/      # inference package: features, model, calibration, tiles, domain, provenance, export
    api/                   # FastAPI routers, schemas, error mapping, rate limit
    migrations/            # Alembic
    models/                # frozen weights (.npz) with SHA-256 files; not in git if large
  etl/                     # sources.yaml, params.yaml, load.py
  frontend/                # Vite + React + TypeScript
  tests/                   # unit, property, regression, api, etl, e2e, nf, a11y
  docker-compose.yml       # api, db, web (nginx); optional caddy for VPS
  Makefile                 # make test | etl | up
```

## 5. Deployment guidance (both targets are in scope; the choice is the author's)

**Common.** One `docker compose up` starts `api`, `db` and `web`. Configuration by environment variables only: database URL, allowed web origin (CORS), rate limit, share-link maximum lifetime, model directory. The image never contains `data/`; the ETL runs once against the database. Health: `/healthz`; the container restart policy is `unless-stopped`.

**Local Docker (development, demonstration, defence).** `docker compose up -d`, `make etl`, open `http://localhost:8080`. Needs about 2 GB of free RAM and the research repository checkout for the ETL. This is the baseline all tests must pass on.

**Free hosting service.**
* Run the database as the host's managed PostgreSQL if its storage cap fits the ETL size report (`db-design.md` §10), otherwise use the SQLite fallback inside the API container and `--clinvar-scope degron-only`.
* Expect cold starts and small CPU/RAM; measure NF-01…NF-06 on it and record the plan name and date. Provider limits are not assumed here; read the current terms when choosing.
* Load the database from a laptop through the provider's connection string (ETL needs the research data), never ship `data/` to the host.
* HTTPS and a domain are normally provided; set the allowed CORS origin to it.

**Rented VPS.**
* Reference size 2 vCPU / 2 GB RAM; Docker Engine and the compose plugin; firewall opens 80/443 only.
* Add a reverse proxy container (for example Caddy) in front of `web` for automatic TLS on a domain name; the API and database stay on the internal network.
* Run the ETL on the VPS from a copy of the needed files, or load locally and restore a dump; backups are optional because everything is rebuildable by the ETL; if wanted, schedule `pg_dump`.
* Keep the OS and images updated; rerun `pip-audit`/`npm audit` before each release.

Deployment tests: DEP-01 (clean checkout) and DEP-02 (the target actually used).

## 6. Rules for anyone editing these documents

* Keep the five sources of truth in agreement: `srs.md` (what), `db-design.md` (data), `openapi.yaml` (interface), `ui-design.md` (screens), `test-plan.md` (checks). A change to a requirement id, an error code or a domain status must be made in all that mention it in the same change.
* Every number taken from research must name its source file; do not retype results from memory.
* Do not edit `report/` from here; propose changes in `chapter-sync.md`.
