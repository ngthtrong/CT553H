# Test Plan

**v0.2, 29 Oct 2026.** UC-01…10, active FR-01…36 and NFR-01…20 in [srs.md](srs.md). This is the **local acceptance plan**, not an executed test report. Historical baseline results are recorded separately in [README.md](README.md) §4. Newly added cases are pending implementation/execution. FR-20, legacy share-token tests and external-host deployment are outside current acceptance.

## 1. Functions under test

Single-tile predictions/ranking/export; protein and annotation lookup; domain and provenance; persistent projects/history; peptide/protein jobs; CSV/TSV import and assay-aware comparison. Reference ETL, migrations, worker, API and React screens are included. Scientific model evaluation remains separate in the thesis experiments; a passing software test does not establish biological or clinical validity.

## 2. Approach

| Group | Approach |
|---|---|
| UT / PB | Deterministic examples and generated invariants: cells, coordinates, calibrators, input and ranking |
| RG | Independent feature reconstruction and back-to-back agreement against frozen runner artefacts |
| API | Schema validation plus operation-specific behaviour; planned operations tested only after implementation |
| ETL | Hash/licence gate, idempotence, mapping and immutable reference-version support |
| E2E | Browser main/error flows for UC-01…10, including close/reopen |
| DOM / ANN | Gate estimator boundaries and annotation mapping/provenance |
| BATCH / IMP / HIST | Durable-job, import/comparison and project-history integration cases |
| NF / SEC / A11Y / DEP | Local responsiveness/resources, payload safety, accessible workflows and clean local installation |

The CLI's independent feature path and frozen verification artefacts remain useful numerical evidence. They share label definitions and weights, so numerical agreement does not certify scientific correctness.

## 3. Pass/fail and suspension

Numerical limits: <1e-9 for JSON, <5e-9 for ten-digit CSV. Same frozen inputs/configuration give identical score arrays; new IDs/timestamps may differ. Functional assertions include persisted state, counts, exclusions, warnings and exact error codes. Skipped/not-run cases are not passes.

Record actual OS/CPU/RAM, Python/Node/database/browser versions, reference/model hashes, job/import sizes and date. Proposed p95 targets require at least 200 single-tile/list requests and 20 browser render runs; report batch duration/progress delay/peak memory separately. No cloud-host criterion applies.

Stop downstream scoring tests on RG, reference-integrity or mapping failure. Restart after fixing/rebuilding a disposable test database. Never reset a real project workspace to rerun tests. Job restart/cancel tests use isolated data and simulate worker interruption deliberately.

## 4. Local environments

| ID | Purpose |
|---|---|
| E-DEV | Actual development computer; baseline SQLite unit/API tests and local browser |
| E-LOCAL | One local React/FastAPI/worker/PostgreSQL instance with workspace files; required integration/acceptance configuration |
| E-CLEAN | Clean local checkout, documented preparation/install, isolated database and file root |
| E-BROWSER | Chromium plus Firefox/WebKit; desktop primary, 360 px responsive table fallback |

Containers may reproduce E-LOCAL on the same computer. They are not a separate hosted product. No VPS/free-tier/HTTPS deployment test is required.

## 5. Baseline and retained cases

These IDs retain their function; listed expectations are targets, not fresh results.

| ID | Requirements | Expected outcome |
|---|---|---|
| UT-01, UT-02 | FR-04 | Independent 180-feature vectors and boundary zero-padding match known values |
| UT-03 | FR-05 | Calibrator output matches frozen reference |
| UT-04 | FR-08 | Permutation 1…532, deterministic ties, top-10% count 54 |
| UT-05 | FR-16 | Full 28-residue windows at step 23, correct n/start/end, no padded windows |
| UT-07 | FR-01 | Case/outer whitespace normalised; invalid internal characters rejected |
| UT-08 | FR-12 | Nine-column CSV and provenance, stable numeric formatting |
| UT-09 | FR-22, NFR-06 | Wrong model hash prevents readiness/scoring |
| PB-01 | FR-01, FR-04 | Valid tile gives 532 finite cells, probabilities in [0,1] |
| PB-02 | FR-03 | Invalid input yields a coded error and no scored item |
| PB-03 | NFR-05 | Same input/configuration → identical scores, ignoring request IDs/times |
| PB-04, PB-05 | FR-08, FR-05 | Stable ranks and monotone Platt calibration |
| RG-01 | FR-04, FR-05, NFR-04 | Service matches independent runner on frozen verification data |
| RG-02 | FR-12, NFR-04 | Exported score values meet the CSV tolerance |
| RG-03, RG-04 | NFR-06, FR-04 | Packaged hash and UniProt-to-tile scoring agree with frozen sources |
| API-01, API-02 | FR-01, FR-02, FR-14 | Sequence and accession/tile paths return 532 cells and provenance |
| API-10…API-19 | FR-03, FR-09, FR-10 | Malformed bodies/fields/length/alphabet/accession/index/model/domain fail explicitly; target gate tested in DOM-01 |
| API-20, API-21 | FR-15, FR-16 | Search and tile list are bounded, mapped and correctly positioned |
| API-22, API-23 | FR-17, FR-18 | Reference observations and ClinVar remain separate from predictions |
| API-24, API-25 | FR-19, FR-21, FR-22 | Model/source cards retain evidence, licences and excluded-source reasons |
| API-26, API-27 | NFR-07 | Body/concurrency/rate limits are endpoint-specific and explicit |
| API-30, API-31 | FR-12, FR-13 | CSV/JSON exports contain all scores/provenance |
| ETL-01, ETL-02 | Data requirements | Pinned hashes verified; second identical reference load changes zero rows |
| ETL-03 | NFR-13 | Blocked reference sources cannot enter served/model tables; project imports stay separate |
| ETL-04, ETL-05 | FR-16, FR-09 | Coordinate/WT agreement and correct gate estimator/source; mismatches reported |
| E2E-01…E2E-04 | UC-01…04 | Predict, rank/filter, export, search/select tile with main and invalid-input flows |
| E2E-05 | FR-17 | Training overlay labelled as training; imported layer labels dataset/revision |
| E2E-06 | FR-18, NFR-14 | ClinVar attribution/review/version/disclaimer beside annotations |
| E2E-07 | FR-19, FR-21 | Model, data and excluded-source information visible |
| E2E-08, E2E-09 | FR-03, FR-10 | Invalid input and warned out-of-domain override handled correctly |
| E2E-10 | FR-23 | Failed export leaves result available for retry |
| E2E-12 | FR-05, FR-11, FR-14 | Event/domain/evidence warnings visible before results and in exports |

UT-06's old direct screen-PSI threshold expectation is superseded by DOM-01. UT-10, API-40…44, E2E-11 and the former SEC-04 token case are legacy share tests, not v0.2 acceptance. No historic test ID is reused for a different feature.

## 6. New first-release cases — all pending

| ID | Requirements / UC | Scenario and expected result |
|---|---|---|
| DOM-01 | FR-09…11, UC-01/08 | Boundary fixtures for frozen R3 measured/predicted gates, unknown/unreliable/borderline and override; screen estimator is not compared directly with intrinsic 4.0; snapshot includes gate provenance |
| ANN-01 | FR-18, FR-35, FR-34 | Exact ClinVar/UniProt/GPS mapping; release/WT mismatch, ambiguous mapping, unavailable source and genuine no-match remain distinct; attribution/version/conflicts preserved in saved/exported results |
| BATCH-01 | FR-24, FR-36 | Empty, valid, duplicate-ID, mixed-invalid and oversized lists/FASTA; preview counts correct, limits reject explicitly, input IDs remain traceable |
| BATCH-02 | FR-04, FR-27 | Every successful batch tile matches single-tile scoring; updating current weights/sources during execution does not change pinned job configuration |
| BATCH-03 | FR-10, FR-26 | Valid, refused and invalid items coexist; terminal state/counts match outcomes; successful results survive item failure and cancellation |
| BATCH-04 | FR-16, FR-25 | Protein lengths 27/28/50/51, termini, overlapping coordinates and non-standard residues; manifest exposes uncovered intervals and distinct tile contexts; no padding/averaging |
| BATCH-05 | FR-26, NFR-19 | Interrupt/restart worker while running, repeat cancellation, cancel then delete project; recover leases with no duplicate completed run or late write to deleted project |
| BATCH-06 | FR-34 | Multi-page job export contains all inputs, tile mapping, successes/refusals/failures and pinned provenance; totals reconcile |
| IMP-01 | FR-28, FR-36, NFR-08 | CSV/TSV schema, missing/nonfinite values, WT/coordinate errors, size/count limits, path/formula text; validation safe, row-specific, no execution |
| IMP-02 | FR-28, NFR-10/13 | Blocking errors prevent commit; warnings acknowledged; expired preview explicit; committed revision immutable; no change to reference tables/weights |
| IMP-03 | FR-17, FR-29 | Match exact WT/position/mutant and supplied mapping; retain missing/unmatched rows, conflicting duplicates and replicates; no silent zero fill/averaging |
| IMP-04 | FR-30, FR-34 | Compatible GPS ΔPSI residuals/MAE/Spearman verified on hand-calculated fixtures; report n/aggregation; constant/insufficient pairs and other endpoints show no misleading metric; export units and dataset revision |
| HIST-01 | FR-31, NFR-09 | Create/rename/list project; unsaved preview absent from storage/logs; explicit save/submit/commit present in local project |
| HIST-02 | FR-14, FR-22, FR-27, FR-32, NFR-10 | Save then restart browser/API/worker; reopen exact snapshots; update active model/ClinVar and confirm old run unchanged; rerun creates new linked entry |
| HIST-03 | FR-33, NFR-10 | Dependency summary before delete, cancellation/dependent comparison and file cleanup, failed cleanup retry; reference/model data and other projects unaffected |

## 7. Non-functional and local acceptance cases

| ID | Requirements | Expected outcome |
|---|---|---|
| NF-01, NF-02 | NFR-01, NFR-02 | Measured local p95 single-tile ≤300 ms and protein-list ≤200 ms, proposed targets; record actual values |
| NF-03 | NFR-18 | Peak API memory reported (proposed API-only 512 MB); DB/worker/browser measured separately |
| NF-04, NF-05 | NFR-07 | Bounded rate/concurrency/body/file/row handling; no silent truncation |
| NF-06 | NFR-03 | Single-tile click-to-render p95 ≤1.5 s, proposed; actual browser/host recorded |
| NF-07 | NFR-03/07/18 | Representative 100-peptide, bounded-protein and import jobs: duration, progress delay, paging, cancellation, disk growth and peak memory reported; UI remains usable |
| SEC-01 | NFR-09/19 | Canary sequence/observation absent from logs/URLs/telemetry; present in workspace only after explicit persistence |
| SEC-02 | NFR-08 | Unsafe text, paths, SQL/formula payloads cannot execute or escape workspace |
| SEC-03 | CON-8 | Services bind loopback; exact origin/content-type mutation checks and browser security headers |
| SEC-05 | NFR-08 | Dependency audit recorded; material unresolved findings reported |
| A11Y-01…04 | NFR-11 | axe checks, keyboard completion of UC-01…10, non-colour cues and contrast checks; automated results do not replace manual checks |
| DEP-01 | NFR-06/16/20 | Clean local preparation/install/start, migrations/ETL, correct model health and UC main flows; no cloud/TLS test |
| DEP-02 | NFR-20, UC-08…10 | Stop/restart the same local instance; saved history/imports/jobs recover; local guide reproduces the workflow |

## 8. Management and deliverables

One author is developer/tester; no independent tester is claimed. Use isolated fixtures and hand-calculated comparison examples, record defects and fix/retest links. Deliver dated test results, coverage, contract validation, migration/job recovery logs, local resource measurements and manual accessibility notes. New cases remain pending until there is executable evidence. A usable application and a valid scientific model are distinct acceptance questions.

## 9. Thesis mapping

Chapter 4 testing plan uses §§1–3; management uses §§4/8; scenarios use §§5–7; evaluation reports executed evidence separately from pending local acceptance. Existing CLI `verify.json` remains historical numerical evidence; README's baseline test counts do not verify v0.2 additions. No public deployment result is required.
