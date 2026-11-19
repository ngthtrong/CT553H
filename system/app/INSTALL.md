# Installing and running Degron Footprint locally

Source for Appendix A of the thesis (`report/appendices/a-installation-user-guide.tex`). Everything runs on one
computer: a FastAPI service and a job worker, a React interface, and a PostgreSQL 16 (Docker) or SQLite database.
Nothing is sent to another server. Two ways to run it: **Docker** (§0, every component in a container) or a
**local install** (§1–§5, Python virtual environment and Node.js on the host). Tested on 17 Nov 2026 by a clean install into an empty directory
([tests/results/dep01-clean-install.json](tests/results/dep01-clean-install.json): 179 s in total on the author's
laptop, WSL2 Ubuntu 24.04).

## 0. Docker: the whole application in containers

Needs Docker Engine with Compose v2 (Docker Desktop with WSL integration on Windows) and this repository's `data/`
directory (the ETL reads it read-only). No Python or Node.js on the host.

```bash
cd system/app
make docker-env                             # .env with a random POSTGRES_PASSWORD (once; edit .env for other settings)
docker compose up -d --build db             # PostgreSQL 16 (volume dbdata)
make docker-etl                             # fills the database and the model volume (CLINVAR_SCOPE=degron-only: faster)
make docker-up                              # api, worker, web  ->  http://127.0.0.1:8080
```

| Container | Image | Role |
| --- | --- | --- |
| `db` | `postgres:16-alpine` | database, volume `dbdata`; not published to the host |
| `api` | `degron-footprint/backend` (target `runtime`) | FastAPI on port 8000 inside the network; runs the migrations at start |
| `worker` | same image, `python -m api.worker` | durable job queue (peptide batches, whole-protein scans) |
| `web` | `degron-footprint/web` (nginx, non-root) | the built interface on `127.0.0.1:8080`; proxies `/v1` and `/healthz` to `api` |
| `etl` (profile `tools`) | backend image | loads reference data and models from the checkout mounted read-only at `/topic` |

Uploaded import files live in the volume `workspace`, model weights in `models`. Back up `dbdata` **and** `workspace`
together. `make docker-down` stops the containers and keeps the volumes; `docker compose down -v` deletes them.
`make docker-logs` follows the logs; `make docker-ps` shows the health of each container.

**Development in Docker.** `make docker-dev` starts the same services with the source bind-mounted: Vite with hot reload
on `http://127.0.0.1:5173`, the API with `--reload` and `/docs` on `http://127.0.0.1:8000`, PostgreSQL on
`127.0.0.1:55433`. `make docker-test` runs the backend suite in the dev image against that PostgreSQL
(`DF_TEST_BACKEND=sqlite` for SQLite plus the real-data tests); `make docker-e2e` runs the real-backend Playwright specs
against `http://127.0.0.1:8080`.

**Optional LoRA-D model.** `WITH_LORA=1` in `.env` builds the backend image with PyTorch (CPU) and Transformers; the ETL
registers LoRA-D when its exported bundle is present (`backend/LORA.md`). The npz model stays the default unless
`DF_DEFAULT_MODEL_ID` names LoRA-D.

## 1. Requirements

| Item | Version used | Notes |
| --- | --- | --- |
| Python | 3.12 (3.11 works) | with `venv` (`sudo apt install python3.12-venv` on Ubuntu) |
| Node.js | 24.22 or later 24.x | e.g. `nvm install 24`; only needed to build or develop the interface |
| Research data | this repository's `data/` directory | not in git; the ETL reads it read-only and checks every file's SHA-256 |
| Docker (optional) | Docker Engine 29 / Compose v2 | the whole stack (§0) or only PostgreSQL 16 (`make pg-up`) |
| Browser | recent Chromium, Firefox or Safari/WebKit | checked at 360, 768, 1280 and 1440 px |

## 2. Install

```bash
cd system/app
make venv                                   # .venv with the pinned backend requirements
cd frontend && npm ci && npm run build && cd ..
```

## 3. Prepare the reference database

```bash
make etl SCOPE=in-tiles                     # .data/dev.db: proteins, tiles, R3 domain labels, ClinVar in tiles (~2–3 min)
```

`SCOPE=degron-only` loads a smaller ClinVar subset (about 2 minutes), `SCOPE=none` keeps the ClinVar rows already
loaded. The ETL also copies the frozen model (`m3-ext4.0-platt-v1`) and the R3 domain gate (`gate-r3-v1`) into
`backend/models/` after checking their hashes. A second run changes nothing when the inputs are unchanged.

## 4. Start

Two terminals:

```bash
make dev-api                                # API on http://127.0.0.1:8000 (migrates the database first)
make dev-worker                             # job worker for peptide batches and whole-protein scans
```

Or one process: `DF_EMBEDDED_WORKER=1 make dev-api`. Then the interface:

```bash
cd frontend && npm run dev                  # http://localhost:5173 (proxies /v1 to the API)
```

Check `http://127.0.0.1:8000/healthz`: `"model_loaded": true` and `"database": "ok"`. If the model weights do not match
their registered hash the service reports `degraded` and refuses to score (NFR-06).

## 5. Optional: PostgreSQL 16

```bash
make pg-up                                  # postgres:16-alpine on 127.0.0.1:55432; password in .data/pg-dev.env
source .data/pg-dev.env
make etl DB="postgresql+psycopg://degron:$POSTGRES_PASSWORD@127.0.0.1:55432/degron"
DF_DATABASE_URL="postgresql+psycopg://degron:$POSTGRES_PASSWORD@127.0.0.1:55432/degron" make dev-api
```

## 6. Where the data lives, backup and deletion

| What | Where |
| --- | --- |
| Reference data, saved analyses, jobs, imported observations | the database (`.data/dev.db` by default) |
| Uploaded import files | `.data/workspace/<project id>/` (generated names only) |
| Model and gate weights | `backend/models/` (rebuilt by the ETL) |

**Prediction cache (plan-system 1.2).** Scores of recently scored tiles are kept in memory per process
(`DF_PREDICTION_CACHE=memory`, the default; at most `DF_PREDICTION_CACHE_MAX_ENTRIES`, 512). Reopening or exporting
the same tile with the same model, weights and calibrator then takes milliseconds instead of a new computation (LoRA-D:
tens of seconds). `DF_PREDICTION_CACHE=off` disables it. `DF_PREDICTION_CACHE=disk` also writes one file per tile to
`DF_PREDICTION_CACHE_DIR` (default `.data/prediction-cache/`, mode 0700) so the cache survives a restart. **The disk
cache keeps the scored sequences on disk although nobody pressed Save** (the file names are hashes, but the stored
wild-type letters spell the sequence): enable it only on a computer where that is acceptable, and delete the directory
to forget them. It is off by default for that reason (NFR-09/10).

**Backup and restore (plan-system 4.1).** `make backup` writes `.data/backups/backup-<time>/` with the database
dump, the project files and `manifest.json` (SHA-256 of each file, schema revision, model ids and weights hashes,
row counts); it reads the running Docker stack and changes nothing. `make restore BACKUP=<dir>` checks every hash and
the schema revision first, shows what it will overwrite with the current and backed-up row counts, asks you to type
`restore`, stops `api` and `worker`, replaces the database and the project files, and starts them again
(`YES=1` skips the question). For a host install use `SQLITE=.data/dev.db` (and `WORKSPACE=` if needed). Model weights
are not in the backup: the ETL rebuilds them. **A backup contains your sequences, saved analyses and imported
observations**: keep it as private as the installation.

Copy the database **and** `.data/workspace/` together to back up a workspace. Deleting a project in the interface
removes its rows and files after showing what depends on it; copies made outside the application are not affected.
The reference data can always be rebuilt with `make etl`; saved work and imports cannot.

## 6b. Command line, Python client, admin page and several workers (plan-system 3.4, 4.2, 4.5)

```bash
cd system/app/backend
python -m api.cli predict --sequence DIMFLVDSSGSIGPENFSKMKTFMKNLV             # JSON on stdout, log on stderr
python -m api.cli predict --uniprot P60484 --tile 3 --format csv --out tile.csv
python -m api.cli job --project <project id> --fasta proteins.fa --wait --export csv --out manifest.csv
python -m api.cli compare <analysis a> <analysis b> --save
python -m api.cli --offline predict --sequence ...       # same service code in-process on DF_DATABASE_URL
```

`--api` defaults to `$DF_API_URL` or `http://127.0.0.1:8080`. The Python client is `api.client.Client` (standard
library only); `docs/notebooks/degron-footprint-client.ipynb` shows a full round (score, save, job, export).

The **Admin** page (`/admin`) shows models and why one is not serving, workers and queue, the prediction cache,
database and project-file sizes and the last ETL run; its only action reloads the models and re-checks their hashes.
It answers only on this computer (`DF_ADMIN_ALLOWED_NETWORKS`).

LoRA-D speed (plan-system 1.4): `DF_LORA_THREADS` (CPU threads, default 4) and `DF_LORA_MERGE=1` (merge the LoRA
update into the weights at load; scores differ from the unmerged model by at most 1e-5) are read from `.env`; on the
author's laptop 6 threads with merging scored a tile about 1.2× faster (`tests/results/lora-speed.json`).

More workers: `docker compose up -d --scale worker=3`. Each worker with LoRA-D needs about 500 MiB of RAM; at most 2
items of one job run at once (`DF_JOB_MAX_RUNNING_ITEMS`) and jobs of ≤ 10 items go first.

## 7. Checking an installation

```bash
make test                                   # backend (≈ 4 min); make test-pg for PostgreSQL
cd frontend && npm test && npm run e2e      # interface unit tests and browser flows (mock API)
```

## 8. Limits

Scores describe one assay (GPS, Zhang et al. 2023) and a development benchmark, not external validation; they are not
probabilities of disease. The R3 gate labels tiles in, borderline or out of the training domain; out-of-domain tiles
are refused unless explicitly overridden. Imported measurements are used for comparison only and never retrain the
model.
