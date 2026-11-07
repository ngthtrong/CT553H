# system/app

> Scope update 29 Oct 2026: this file documents the **baseline implementation/historical checks**. The accepted first local release now includes projects/history, peptide/protein jobs, ClinVar/reference annotations and experimental import/comparison; those extensions are not implemented by this documentation change. See [current scope](../README.md). The expanded OpenAPI design contains planned operations; old contract/type-check results apply to the baseline only. Public sharing and hosting examples below are legacy, outside current acceptance.


Code of the degron-footprint tool. Read [../README.md](../README.md) for the design first.

**Status reconciled 3 Nov 2026:** serving still uses the frozen baseline model; [v3 research](../../research/README.md) has not promoted a replacement. The current [Workspace UI v2 review](../design/workspace-ui-v2/README.md) is a separate fixture prototype. Projects/history, durable batch/protein jobs, experimental comparison, PostgreSQL acceptance and correct R3 integration remain open.

| Part | State (22 Oct 2026) |
|---|---|
| [backend/](backend/README.md) | Written and tested on SQLite: API, ETL, migration, tests. PostgreSQL and Docker not run |
| `frontend/` | Written by the frontend task; `docker-compose.yml` expects `./frontend/Dockerfile` |
| [DEVIATIONS.md](DEVIATIONS.md) | Where the code departs from, or must choose beyond, the design documents; open items |

The Makefile uses Bash and `.venv/bin/` paths: run its targets under Linux/WSL, using the app's own environment. The root Windows `.venv` and `.cmd` launchers belong to research training. Node/npm commands for the frontend are documented in [frontend/README.md](frontend/README.md).

Backend checks are `make test`, `make test-fast`, `make lint`, `make typecheck` and `make contract` from this directory. Frontend scripts include `npm test`, `npm run typecheck`, `npm run lint`, `npm run build` and `npm run e2e`. Historical pass counts in the subdirectory READMEs do not validate planned v0.2 routes or establish that the current expanded contract/types are in sync.

Common tasks: `make -C system/app help`. Development API for the frontend:
`make -C system/app dev-api` (http://127.0.0.1:8000, CORS for http://localhost:5173).
