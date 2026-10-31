# system/app

> Scope update 29 Oct 2026: this file documents the **baseline implementation/historical checks**. The accepted first local release now includes projects/history, peptide/protein jobs, ClinVar/reference annotations and experimental import/comparison; those extensions are not implemented by this documentation change. See [current scope](../README.md). The expanded OpenAPI design contains planned operations; old contract/type-check results apply to the baseline only. Public sharing and hosting examples below are legacy, outside current acceptance.


Code of the degron-footprint tool. Read [../README.md](../README.md) for the design first.

| Part | State (22 Oct 2026) |
|---|---|
| [backend/](backend/README.md) | Written and tested on SQLite: API, ETL, migration, tests. PostgreSQL and Docker not run |
| `frontend/` | Written by the frontend task; `docker-compose.yml` expects `./frontend/Dockerfile` |
| [DEVIATIONS.md](DEVIATIONS.md) | Where the code departs from, or must choose beyond, the design documents; open items |

Common tasks: `make -C topics/degron-footprint/system/app help`. Development API for the frontend:
`make -C topics/degron-footprint/system/app dev-api` (http://127.0.0.1:8000, CORS for http://localhost:5173).
