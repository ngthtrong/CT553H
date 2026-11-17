# Run from anywhere:  make -C system/app <target>
SHELL := /bin/bash
APP   := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
PY    := $(APP).venv/bin/python
DB    ?= sqlite:///$(APP).data/dev.db
SCOPE ?= in-tiles
export DF_DATABASE_URL := $(DB)
export PYTHONPATH := $(APP)backend

.PHONY: help venv dev-api dev-worker pg-up pg-down test-pg db-migrate etl etl-docker seed-dev test test-fast lint typecheck contract latency up down clean-dev

help:
	@echo "venv        create .venv and install pinned requirements"
	@echo "db-migrate  alembic upgrade head on DB (default: .data/dev.db)"
	@echo "etl         load the reference database (SCOPE=in-tiles|all|degron-only|none)"
	@echo "dev-api     migrate + load if the dev database is missing, then serve http://127.0.0.1:8000"
	@echo "dev-worker  local job worker for peptide/protein jobs (run next to dev-api; Ctrl-C stops it)"
	@echo "test        full pytest suite with coverage;   test-fast: without slow/realdata tests"
	@echo "lint        ruff;   typecheck: mypy;   contract: validate ../openapi.yaml"
	@echo "up / down   docker compose (Docker is required; not available on every machine)"
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
	cd $(APP) && $(APP).venv/bin/ruff check backend etl tests

typecheck:
	cd $(APP) && $(APP).venv/bin/mypy backend/degron_footprint backend/api backend/db etl --explicit-package-bases

contract:
	$(PY) -c "import yaml,sys; from openapi_spec_validator import validate; validate(yaml.safe_load(open('$(APP)../openapi.yaml'))); print('openapi.yaml valid')"

latency:
	cd $(APP) && $(PY) tests/measure_latency.py

up:
	cd $(APP) && docker compose up -d --build

down:
	cd $(APP) && docker compose down

etl-docker:
	cd $(APP) && docker compose --profile tools run --rm etl

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
