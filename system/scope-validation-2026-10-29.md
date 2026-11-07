# Scope/document synchronization validation — 29 Oct 2026

This records **documentation/build checks**, not new application or scientific acceptance. The author confirmed the revised scope and requested synchronization of system documents and the working thesis. Proposal files and experimental results were left unchanged.

## Changed scope

Release 1 includes ClinVar/approved supplementary reference annotations, peptide batches and whole-protein tiling, experimental CSV/TSV import/comparison, and local projects/history. Stack: React + TypeScript and FastAPI. One local instance; no public/hosted deployment requirement. New runtime features, migrations and corresponding acceptance tests remain pending.

## Checks executed

| Check | Result |
|---|---|
| `make -C topics/degron-footprint/report doctor` | Required build tools, Times New Roman faces and logo found |
| `make -C topics/degron-footprint/report all` | Built one-sided and two-sided PDFs, 74 pages each; references resolved |
| `make -C topics/degron-footprint/report check` | Both report PDFs pass A4, embedded fonts, required headings, final-log layout/reference checks; the pre-existing 9-page smoke PDF also checked, not rebuilt |
| `make -C topics/degron-footprint/system/app contract` | Expanded OpenAPI 3.1 document validates; planned endpoints are not treated as implemented |
| Requirement/traceability inspection | UC-01…10; FR-01…36 with FR-20 retired; NFR-01…20; all 15 added DOM/ANN/BATCH/IMP/HIST case IDs are linked to the plan |
| Local Markdown links and `git diff --check` | Rechecked after creating this record; no broken modified-document links or whitespace errors |
| Proposal checksums | PDF, Markdown and DOCX match their pre-edit hashes below |
| Source diff | No application runtime/test code or research-result files changed; app guides only carry a baseline-status notice |

The first PDF attempt found two overfull lines in the rewritten Chapter 4 scope paragraph. Rephrasing removed them; the final normal/two-sided builds and check passed. The changed English/Vietnamese abstracts, Chapter 1 scope/use-case pages, Chapter 3 architecture/data tables, Chapter 4 acceptance table and Appendix A were rendered and visually inspected (PDF pages 7, 8, 22, 27, 36, 38, 67 and 72). No clipping or overlap was observed; long use-case tables continue across page boundaries.

## Preserved proposal hashes (SHA-256)

| File | Hash |
|---|---|
| `proposal/proposal.pdf` | `21b1e6aa68bece4ae65f2023b41076b653b6b577e0f26aaeb5a618dfe3f7c40a` |
| `proposal/proposal.md` | `2c5f597e7514caa4c49fc290f2e5454390fbac0eac95e5bb394e707054d84203` |
| `proposal/proposal.docx` | `7e2fad20dad8ed3f9597892bfcf296e805ffc1324b401de11de5ba37128d80f8` |

## Limits and concurrent work

No new project/job/import code, database migration, model fit, app test run or user study was performed. Historical baseline/CLI results remain historical evidence. Generated frontend types and baseline contract-test expectations will need reconciliation when the expanded contract is implemented; prior `check:api` results do not apply to the changed design. R3 domain-gate integration remains open.

A concurrent modification to `report/config/metadata.tex` (student/advisor display names) appeared during the task. It was not made or reverted by this scope update; the PDFs include the metadata present at build time. No original-template files or proposal artefacts were edited, and no commit was created.
