# Thesis synchronization record — local scope v0.2

**Applied on 29 Oct 2026 at the author's explicit request.** This replaces the old unapproved chapter-change proposal. The working thesis is [../report/](../report/README.md), not the former root `report/`. The proposal PDF/Markdown/Word, original template and experimental result files are unchanged.

## 1. Confirmed scope and document mapping

| Author instruction | System documents | Thesis content |
|---|---|---|
| ClinVar and supplementary annotations in release 1 | UC-06, FR-18/35, ANN-01; API/UI/data provenance | Chapter 1 UC-06; Chapter 3 sources/annotation flow; Chapter 4 ANN-01 |
| Peptide batches and whole-protein processing in release 1 | UC-08, FR-24…27/34/36; jobs, coverage, cancellation/recovery | Chapter 1 UC-08; Chapter 3 architecture/tiling; Chapter 4 BATCH cases |
| Experimental-data import/comparison in release 1 | UC-05/09, FR-17/28…30; immutable datasets and assay checks | Chapters 1/3 workflows/data; Chapter 4 IMP cases |
| Projects and history in release 1 | UC-10, FR-31…33; explicit local persistence until deletion | Chapters 1/3 lifecycle/data; Chapter 4 HIST cases |
| React + FastAPI fixed | README D-1, CON-7, API/UI design | Introduction technologies; Chapters 1/3; Appendix A |
| One local instance; no real/public deployment | CON-8, NFR-20; local-only DEP cases | Introduction scope; Chapters 1/3/4; Appendix A |
| Update system README, not proposal | README is the current scope entry point | Proposal files intentionally unchanged |

## 2. Files synchronized

* Introduction: objective, software scope, stack and local-only operation.
* Chapter 1: customer problem, UC-01…10, local/persistence/import requirements and constraints.
* Chapter 3: planned local architecture figure, component roles, job/import interactions, reference/project data and source boundaries.
* Chapter 4: expanded local test plan, historical CLI evidence separated from baseline source/historical checks and pending new acceptance.
* English/Vietnamese abstracts: matching planned software scope; no claim that added features are complete.
* Conclusion program subsection: target scope and pending status only; no invented achieved results.
* Appendix A: executable baseline guide separated from pending PostgreSQL/worker/workspace guide.

## 3. Not completed by this change

No new application functionality, data migration, model training, user study or expanded acceptance run. No G2/G3 completion claim. Existing code's screen-PSI gate is still an integration gap. `openapi.yaml` contains planned operations and deprecates sharing; generated client types and runtime routes must be reconciled in the implementation task. Final capacity limits/performance require local measurement.

Document validation/build evidence is recorded in [scope-validation-2026-10-29.md](scope-validation-2026-10-29.md), separately from application/scientific validation.
