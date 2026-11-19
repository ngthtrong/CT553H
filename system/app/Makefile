# Run from anywhere:  make -C system/app <target>
SHELL := /bin/bash
APP   := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
PY    := $(APP).venv/bin/python
DB    ?= sqlite:///$(APP).data/dev.db
SCOPE ?= in-tiles
export DF_DATABASE_URL := $(DB)
export PYTHONPATH := $(APP)backend

.PHONY: help venv dev-api dev-worker pg-up pg-down test-pg db-migrate etl etl-docker seed-dev test test-fast lint typecheck contract latency up down clean-dev \
        docker-env docker-up docker-down docker-etl docker-logs docker-ps docker-dev docker-dev-down docker-test docker-e2e lora-bundle \
        backup restore

help:
	@echo "venv        create .venv and install pinned requirements"
	@echo "db-migrate  alembic upgrade head on DB (default: .data/dev.db)"
	@echo "etl         load the reference database (SCOPE=in-tiles|all|degron-only|none)"
	@echo "dev-api     migrate + load if the dev database is missing, then serve http://127.0.0.1:8000"
	@echo "dev-worker  local job worker for peptide/protein jobs (run next to dev-api; Ctrl-C stops it)"
	@echo "test        full pytest suite with coverage;   test-fast: without slow/realdata tests"
	@echo "lint        ruff;   typecheck: mypy;   contract: validate ../openapi.yaml"
	@echo "docker-env  write .env with a random POSTGRES_PASSWORD (once)"
	@echo "docker-up   whole app in Docker: db, api, worker, web -> http://127.0.0.1:8080 (WITH_LORA=1 adds PyTorch)"
	@echo "docker-etl  fill the Docker database and model volume from the checkout (CLINVAR_SCOPE=in-tiles|degron-only)"
	@echo "docker-dev  the same with bind-mounted source: Vite :5173, API --reload :8000, PostgreSQL :55433"
	@echo "docker-test backend pytest inside the dev image on the compose PostgreSQL (DF_TEST_BACKEND=sqlite for SQLite)"
	@echo "docker-e2e  Playwright real-backend specs against the Docker web container (E2E_BASE_URL)"
	@echo "backup      one-command backup of the Docker stack: DB dump + project files + manifest (OUT=dir optional)"
	@echo "restore     BACKUP=dir: check the manifest and schema, show what is overwritten, ask, then restore"
	@echo "lora-bundle export the LoRA-D serving bundle from branch-1 artifacts into data/processed (needs .venv-lora)"
	@echo "pg-up       local PostgreSQL 16 in Docker on 127.0.0.1:55432 (password in .data/pg-dev.env)"
	@echo "test-pg     the backend suite on PostgreSQL (needs pg-up)"

venv:
	python3 -m venv $(APP).venv
	$(APP).venv/bin/pip install -r $(APP)backend/requirements-dev.txt

db-migrate:
	@mkdir -p $(APP).data
	$(APP).venv/bin/alembic -c $(APP)backend/alembic.ini upgrade head

etl: db-migrate
	cd $(APP) && $(PY) -m etl.load --db $(DB) --clinvar-scope $(SCOPE) --report $(APP).data/etl-report.json

# The development server for the frontend: http://127.0.0.1:8000 with CORS for http://localhost:5173.
# The first run builds the database from the research data (about 20 s without ClinVar; ClinVar adds minutes).
dev-api:
	@mkdir -p $(APP).data
	@if [ ! -s $(APP).data/dev.db ]; then \
	  echo "[dev-api] building .data/dev.db (first run)"; \
	  $(MAKE) -s etl SCOPE=$${SCOPE:-degron-only}; \
	fi
	cd $(APP)backend && DF_ENABLE_DOCS=1 DF_ALLOWED_ORIGINS='["http://localhost:5173","http://127.0.0.1:5173"]' \
	  DF_RATE_LIMIT_PREDICT=600 DF_RATE_LIMIT_REFERENCE=1200 \
	  $(PY) -m uvicorn api.main:create_app --factory --host 127.0.0.1 --port 8000 --no-access-log --reload

# The job worker is a separate process (implementation plan A-2). DF_EMBEDDED_WORKER=1 runs it inside dev-api instead.
dev-worker:
	cd $(APP)backend && $(PY) -m api.worker

test:
	cd $(APP) && $(PY) -m pytest --cov=degron_footprint --cov=api --cov=db --cov=etl --cov-report=term-missing:skip-covered

test-fast:
	cd $(APP) && $(PY) -m pytest -m "not slow and not realdata"

lint:
	cd $(APP) && $(APP).venv/bin/ruff check backend etl tests ops

typecheck:
	cd $(APP) && $(APP).venv/bin/mypy backend/degron_footprint backend/api backend/db etl ops --explicit-package-bases

contract:
	$(PY) -c "import yaml,sys; from openapi_spec_validator import validate; validate(yaml.safe_load(open('$(APP)../openapi.yaml'))); print('openapi.yaml valid')"

latency:
	cd $(APP) && $(PY) tests/measure_latency.py

# ---- Whole application in Docker (docker-compose.yml) and the development override (compose.dev.yml)
DC     := cd $(APP) && docker compose
DC_DEV := cd $(APP) && HOST_UID=$$(id -u) HOST_GID=$$(id -g) docker compose -f docker-compose.yml -f compose.dev.yml

docker-env:
	@if [ -f $(APP).env ]; then echo ".env exists; not overwritten"; else \
	  (umask 077; python3 -c "import re,secrets,sys; s=open(sys.argv[1]).read(); \
	  open(sys.argv[2],'w').write(re.sub(r'(?m)^POSTGRES_PASSWORD=.*$$', 'POSTGRES_PASSWORD='+secrets.token_urlsafe(24), s))" \
	  $(APP).env.example $(APP).env); echo "wrote .env with a random POSTGRES_PASSWORD"; fi

docker-up up: docker-env
	$(DC) up -d --build --wait db api worker web
	@$(DC) ps

docker-down down:
	$(DC) down

docker-etl etl-docker: docker-env
	$(DC) --profile tools run --rm etl
	$(DC) restart api worker

docker-logs:
	$(DC) logs -f --tail=100

docker-ps:
	$(DC) ps

docker-dev: docker-env
	$(DC_DEV) up -d --build --wait db api worker web web-dev
	@$(DC_DEV) ps

docker-dev-down:
	$(DC_DEV) down

docker-test: docker-env
	$(DC_DEV) --profile tools run --rm test $(PYTEST_ARGS)

E2E_BASE_URL ?= http://127.0.0.1:8080
docker-e2e:
	cd $(APP)frontend && E2E_REAL=1 E2E_BASE_URL=$(E2E_BASE_URL) npx playwright test --project=chromium-desktop e2e/real.spec.ts

# LoRA-D serving bundle (plan 2.12). Reads the branch-1 artifacts read-only; writes data/processed/lora-d-serving-v1/.
LORA_PY ?= $(APP).venv-lora/bin/python
lora-bundle:
	$(LORA_PY) $(APP)etl/export_lora.py

# ---- PostgreSQL 16 for development and the parity suite (WP8). Loopback only; the password stays in .data/.
PG_ENV  := $(APP).data/pg-dev.env
PG_PORT ?= 55432

pg-up:
	@mkdir -p $(APP).data
	@test -f $(PG_ENV) || (umask 077; printf 'POSTGRES_PASSWORD=%s\n' "$$(python3 -c 'import secrets; print(secrets.token_urlsafe(24))')" > $(PG_ENV))
	@if docker container inspect df-pg-dev >/dev/null 2>&1; then docker start df-pg-dev >/dev/null; else \
	  . $(PG_ENV); docker run -d --name df-pg-dev --restart unless-stopped -e POSTGRES_DB=degron -e POSTGRES_USER=degron \
	    -e POSTGRES_PASSWORD="$$POSTGRES_PASSWORD" -v df-pg-dev-data:/var/lib/postgresql/data \
	    -p 127.0.0.1:$(PG_PORT):5432 postgres:16-alpine >/dev/null; fi
	@for i in $$(seq 1 30); do docker exec df-pg-dev pg_isready -U degron -d degron >/dev/null 2>&1 && break; sleep 1; done
	@echo "PostgreSQL 16 ready on 127.0.0.1:$(PG_PORT); password in .data/pg-dev.env"

pg-down:
	docker stop df-pg-dev

test-pg:
	@. $(PG_ENV); cd $(APP) && DF_TEST_BACKEND=postgresql \
	  DF_TEST_PG_URL="postgresql+psycopg://degron:$$POSTGRES_PASSWORD@127.0.0.1:$(PG_PORT)/degron" $(PY) -m pytest

# ---- Backup and restore (plan-system 4.1). Docker stack by default; SQLITE=.data/dev.db for a host install.
BACKUP_ARGS = $(if $(SQLITE),--sqlite $(SQLITE) --workspace $(or $(WORKSPACE),$(APP).data/workspace),)
backup:
	python3 $(APP)ops/backup.py backup $(BACKUP_ARGS) $(if $(OUT),--out $(OUT),)

restore:
	@test -n "$(BACKUP)" || (echo "usage: make restore BACKUP=<backup directory> [YES=1]"; exit 2)
	python3 $(APP)ops/backup.py restore $(BACKUP) $(BACKUP_ARGS) $(if $(YES),--yes,)
