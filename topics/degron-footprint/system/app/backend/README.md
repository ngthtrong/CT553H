# Backend of the degron-footprint tool

FastAPI service, inference package, SQLAlchemy models with Alembic migrations, and the ETL. Contract:
[../../openapi.yaml](../../openapi.yaml). Differences from the design documents: [../DEVIATIONS.md](../DEVIATIONS.md).

```
backend/degron_footprint/   inference: features (180), ridge + Platt/isotonic, tiles, domain gate, provenance, export
backend/api/                FastAPI app: routers, errors, middleware (request id, rate limit, headers, safe log), service
backend/db/                 SQLAlchemy 2 models, session factory
backend/migrations/         Alembic (revision 0001)
backend/models/             frozen weights, m3-ext4.0-platt-v1.npz (SHA-256 8bec0b04…cd9c3, 5.5 kB)
etl/                        sources.yaml (pinned inputs and licences), params.yaml, load.py
tests/                      pytest: unit, property, ETL, API, security, contract (schemathesis), regression, latency script
```

## Run it (development, SQLite)

```bash
make -C topics/degron-footprint/system/app venv         # once: .venv with pinned requirements
make -C topics/degron-footprint/system/app dev-api      # http://127.0.0.1:8000, CORS for http://localhost:5173
```

`dev-api` builds `.data/dev.db` on its first run from the research data (about 20 s without ClinVar, about 2 minutes
more with it; the first run uses ClinVar scope `degron-only`). To fill it differently:
`make -C … etl SCOPE=in-tiles` (`in-tiles`, `degron-only`, `all`, `none`). Interactive documentation, which is the
contract itself, is at `/docs` in `dev-api`. A reload on code change is on.

| Task | Command (from `topics/degron-footprint/system/app`) |
|---|---|
| All tests with coverage | `make test` (about 90 s; 148 tests) |
| Without the research data and the slow suites | `make test-fast` |
| Lint, types | `make lint`, `make typecheck` |
| Contract file valid | `make contract` |
| Latency and memory over HTTP | `make latency` (needs `.data/dev.db`) |

## Settings (environment, prefix `DF_`; see `api/config.py`)

| Variable | Default | Meaning |
|---|---|---|
| `DF_DATABASE_URL` | `sqlite:///./degron.db` | SQLAlchemy URL; PostgreSQL: `postgresql+psycopg://user:pw@host/db` |
| `DF_MODEL_DIR` | `backend/models` | Where the weights files named in `model_version.weights_path` are |
| `DF_GATE_WEIGHTS`, `DF_GATE_CARD` | unset | `gate-weights.npz` / `gate-card.json` of experiment R3 (ignored until a loader for its `kind` is registered in `degron_footprint/domain.py`) |
| `DF_ALLOWED_ORIGINS` | `["http://localhost:5173"]` | CORS allow-list, JSON list; no wildcard |
| `DF_RATE_LIMIT_PREDICT` / `DF_RATE_LIMIT_REFERENCE` | 60 / 120 | Requests per client and `DF_RATE_WINDOW_SECONDS` (60) |
| `DF_MAX_BODY_BYTES` | 4096 | Request body limit |
| `DF_SHARE_TTL_DEFAULT_DAYS`, `DF_SHARE_TTL_MAX_DAYS` | 7, 30 | Shared-run lifetime |
| `DF_TRUST_PROXY` | false | Take the client address from `X-Forwarded-For` (only behind your own proxy) |
| `DF_ENABLE_DOCS` | false | Serve `/docs` and `/openapi.json` |
| `DF_OPENAPI_CONTRACT` | `../openapi.yaml` | The file served as the API description |
| `DF_BACKGROUND_JOBS` | true | Hourly purge of expired runs, minute flush of usage counters |

## Docker (not run on the machine where it was written)

```bash
cd topics/degron-footprint/system/app
cp .env.example .env && $EDITOR .env           # at least POSTGRES_PASSWORD
docker compose up -d --build                   # db, api, web (the web image comes from ./frontend)
docker compose --profile tools run --rm etl    # once: fills the database from the research checkout (TOPIC_DIR)
```

VPS: `docker compose --profile vps up -d` adds Caddy with automatic TLS for `SITE_ADDRESS`; set `DF_TRUST_PROXY=true`.
Free host without a hosted PostgreSQL: run the API image with `DF_DATABASE_URL=sqlite:////data/degron.db` and a volume,
loading it with `CLINVAR_SCOPE=degron-only`. Untested; see DEVIATIONS §5.

## ETL in one paragraph

`etl/load.py` hashes every input file and compares it with `etl/sources.yaml` (mismatch: aborts, the evidence is kept in
`etl_input`), refuses any file of a source that may not be redistributed (Koren, MetaDegron/ELM and Larsen are registered
but never loadable), then loads proteins, tiles with the measured domain status, the 92,337 training cells (checked
against the UniProt-derived tile), ClinVar missense variants and the model registry. A second run with unchanged inputs
reports zero inserted and zero updated rows. The report is stored in `etl_run.report` and printed as JSON.
