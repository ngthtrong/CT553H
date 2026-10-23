# Software Requirements Specification — Degron Footprint Tool

Structure follows ISO/IEC/IEEE 29148. Status: **draft v0.1, 22 Oct 2026**, author's review pending. Requirement thresholds marked *(to be measured)* are proposals; they become binding only after a measurement on the target environment is recorded in [test-plan.md](test-plan.md). Companion documents: [db-design.md](db-design.md), [api-spec.md](api-spec.md), [ui-design.md](ui-design.md).

## 1. Introduction

### 1.1 Purpose

This document states what the web tool must do and the constraints it must respect. It is the source of the thesis chapters on the problem (Chapter 1) and the design (Chapter 3), and the basis of the test plan (Chapter 4, §4.3–4.6).

### 1.2 Scope

The tool lets a researcher enter a 28-residue peptide (or pick a tile of a human protein), obtain the predicted effect of every one of its 532 single-residue substitutions on the degron signal (the assay quantity ΔPSI), rank the substitutions, compare with measured data and ClinVar annotations where they exist, and export the result together with the information needed to reuse and trace it.

The tool wraps **one frozen research model** (v1: ridge regression on 180 sequence features, fitted on the 176 peptides / 92,337 cells of the saturation mutagenesis data of Zhang et al. 2023, with Platt calibration; model id `m3-ext4.0-platt-v1`). It is a screening aid for choosing substitutions to test, not a diagnostic instrument.

### 1.3 Out of scope

* User accounts, login, saved histories, or any personal data.
* Batch jobs over many proteins or upload of files.
* Assays other than the GPS stability assay of Zhang et al. 2023 (for example N-degron libraries, other stability assays), non-human proteins, peptides of other lengths.
* Any statement about disease causation, pathogenicity of a variant, or treatment.
* A native mobile application.
* Training or re-training models inside the tool. Training happens offline in notebooks; the tool loads frozen weights.

### 1.4 Definitions

| Term | Meaning |
|---|---|
| PSI | Protein Stability Index of the GPS assay: expected bin (1–6) of a peptide fused to GFP; lower is less stable |
| ΔPSI | PSI(mutant) − PSI(wild type) |
| Tile | A 28-residue window of a UniProt sequence, step 23; tile *n* starts at residue (n−1)·23+1 |
| Cell | One (position, substituted amino acid) of a tile; 532 per tile |
| Calibrated probability | Platt-scaled estimate of P(ΔPSI ≥ 1.0) **for the assay and domain of the model**; not a probability of disease |
| Domain status | Whether the tile is within the wild-type PSI range (≤ 4.0) on which the model was trained (see [db-design.md](db-design.md) §3.3) |
| OOF | Out-of-fold: evaluation on clusters of proteins never seen in training |
| Provenance | Model id, weights hash, data sources with licences, domain, evidence label, generation time |

### 1.5 References

Chapter 1 and Chapter 3 of the thesis (`report/chapters/`); research report [calibration-p6](../research/calibration-p6-2026-10-22/README.md) (model, calibration, prototype, verification); [next-phase plan](../research/next-phase-plan-2026-10-22/README.md); source ledger `data/README.md`.

## 2. Overall description

### 2.1 Product perspective

A three-tier web application (browser SPA, REST API, relational database) around a numpy-only inference package. It reads reference data (UniProt, the GPS peptidome screen, the saturation labels, ClinVar) that an ETL job loads from the research repository; it never writes research data.

### 2.2 Stakeholders and users

| Stakeholder | Interest |
|---|---|
| Researcher choosing mutations for follow-up experiments (primary user) | Quick ranked list of substitutions, with honest caveats |
| Student exploring sequence–degradation relations | Clear visualisation; explanations of what a score means |
| Thesis supervisor and examiners | Traceable provenance; claims that match the evidence; tests |
| Author (developer, tester, maintainer) | Reproducible build and deployment |
| Data providers | Attribution and licence compliance |

### 2.3 Assumptions and dependencies

1. **Model domain.** The model was trained only on peptides with intrinsic wild-type PSI ≤ 4.0 and is valid only for 28-residue internal tiles of the GPS assay. It cannot detect a stable tile by itself.
2. **Evidence level.** All reported performance (AUROC about 0.82, Brier 0.0925 against 0.1272 for the raw score) comes from a development OOF benchmark on data that have been examined many times. It is **not** an external validation, and the tool never says it is.
3. **Probability meaning.** The calibration is somewhat low (about 13 % relative) on peptides of the original benchmark domain; ranking is unaffected. The model card states this.
4. **Gate model.** Experiment R3 delivered a gate model for arbitrary tiles (22 Oct 2026; tier 2 AUROC 0.815, see its report). Until it is integrated, domain status for typed sequences is `unknown`. R3 also requires a third state `borderline` and replaces the raw `psi <= 4.0` rule on screen PSI by two logistic cuts (tier 1: 2.687 / 3.110).
5. The UniProt snapshot is release 2026_03 (file of 12 Oct 2026); the tile numbering of the GPS screen is assumed to follow it, which is checked by the ETL for the 176 training peptides only.
6. The research repository is available to the ETL; the hosted service does not read it at run time.

### 2.4 Constraints

| ID | Constraint |
|---|---|
| CON-1 | **Data licences.** Only sources with `redistribution_ok = true` may be served. Koren et al. 2018 (internal use only), MetaDegron/ELM-derived tables (no licence on file), and Larsen et al. 2025 (data licence unconfirmed) must not be loaded into the database or the model. |
| CON-2 | **ClinVar.** Wherever ClinVar annotations are shown, the ClinVar attribution and the sentence that the data are not intended for direct diagnostic use must appear next to them. |
| CON-3 | **No claims beyond evidence.** The interface and exports must carry the evidence label of the model. |
| CON-4 | **One developer, thesis schedule.** No new wet-lab work; the tool is built and tested by the author. |
| CON-5 | **CPU inference.** The running service needs no GPU. |
| CON-6 | **Privacy.** Input sequences are not stored beyond the request unless the user asks for a share link. |
| CON-7 | **Stack.** FastAPI (Python 3.11), React with TypeScript, PostgreSQL 16 (SQLite for development and unit tests), Docker Compose. |

## 3. Use cases

UC-01 to UC-03 are those of Chapter 1; UC-04 to UC-07 are proposed additions (see [chapter-sync.md](chapter-sync.md)). Actor for all: **User** (researcher or student, anonymous).

### UC-01 Predict the effect matrix
* **Preconditions:** the service is reachable and a default model is loaded.
* **Main flow:** 1. The user enters a 28-residue sequence, or chooses a protein and a tile (UC-04). 2. The system validates length, alphabet and tile range. 3. The system determines the domain status. 4. The system scores the 532 substitutions with the default model and calibrates them. 5. The system shows the domain status and warnings first, then the heatmap with the evidence label and model id.
* **Alternative flows:** A1 invalid input → specific message naming the field and fix, no scores. A2 `measured_out_of_domain` → refusal with the reason; the user may choose to override, which re-runs with `override_domain` and shows the strongest warning. A3 `unknown` → scores with a prominent warning. A4 model not loaded → "service unavailable" message.
* **Postconditions:** nothing is stored.
* **Requirements:** FR-01 to FR-06, FR-09 to FR-11, FR-14, FR-22.

### UC-02 Rank substitutions
* **Preconditions:** a prediction is on screen.
* **Main flow:** 1. The user opens the ranking table. 2. The system lists the 532 substitutions by raw score (rank 1 is highest). 3. The user filters by position or amino acid and sorts by any column. 4. The top 10 % are marked.
* **Alternative flows:** A1 no prediction yet → the page asks the user to run UC-01 first. A2 a filter leaves no rows → "no substitution matches the filter".
* **Requirements:** FR-07, FR-08.

### UC-03 Export results with provenance
* **Preconditions:** a prediction is on screen.
* **Main flow:** 1. The user selects CSV or JSON. 2. The system generates the file with provenance (model id, weights hash, event definition, evidence label, domain status, data sources, generation time, disclaimer). 3. The browser downloads it.
* **Alternative flows:** A1 generation or download fails → error message, the result stays on screen. A2 the user chooses a share link instead → UC-03b: the system stores the run for up to 30 days and shows a link whose token is in the URL fragment.
* **Requirements:** FR-12, FR-13, FR-14, FR-20, FR-23.

### UC-04 Select a tile from a UniProt protein (proposed)
* **Main flow:** 1. The user types a gene symbol or accession. 2. The system lists matching proteins. 3. The user picks one. 4. The system shows the tiles along the protein coloured by domain status. 5. The user picks a tile and continues with UC-01.
* **Alternative flows:** A1 no match → message and the hint that only reviewed human proteins are included. A2 the protein has no full 28-residue tile (shorter than 28) → message. A3 non-scorable tile (non-standard residue) is shown disabled with the reason.
* **Requirements:** FR-15, FR-16.

### UC-05 Compare with measured data (proposed; the *Extend* of UC-01)
* **Preconditions:** the tile is one of the 176 training peptides.
* **Main flow:** 1. The user switches on the "measured ΔPSI" layer. 2. The system overlays measured values on the heatmap and lists predicted against measured for each cell.
* **Rule:** the layer is labelled "included in the training of this model"; it is never described as validation.
* **Alternative flows:** A1 the tile has no measured data → the layer is disabled with the reason.
* **Requirements:** FR-17.

### UC-06 View ClinVar variants (proposed)
* **Main flow:** 1. The user switches on the ClinVar layer. 2. The system marks cells that correspond to ClinVar missense variants, with significance, review status and ClinVar file date. 3. The ClinVar attribution and disclaimer appear next to the layer.
* **Alternative flows:** A1 no variants in the tile → "no ClinVar missense variant in this tile".
* **Requirements:** FR-18; constraint CON-2.

### UC-07 View the model card (proposed)
* **Main flow:** the user opens the model card and reads model id, hash, event definition, domain, metrics with confidence intervals and their source files, limitations, data sources and licences, and version history.
* **Requirements:** FR-19, FR-21, FR-22.

## 4. Functional requirements

Priority: **M** must, **S** should, **C** could. "Verify" names the test group of [test-plan.md](test-plan.md).

| ID | Requirement | UC | Pri | Verify |
|---|---|---|---|---|
| FR-01 | The system shall accept a tile as a sequence of exactly 28 standard amino acids, ignoring case and surrounding whitespace. | 01 | M | UT-07, API, E2E |
| FR-02 | The system shall accept a tile as a UniProt accession and a 1-based tile index. | 01, 04 | M | API, E2E |
| FR-03 | The system shall reject invalid input with a specific coded error that names the field and states what is wrong (length, character, accession, tile range, non-scorable tile) and shall return no scores. | 01 | M | PB-02, API, E2E-08 |
| FR-04 | The system shall compute the raw score of all 532 substitutions of a valid tile with the selected frozen model. | 01 | M | RG, UT-01 |
| FR-05 | The system shall report for each substitution the calibrated probability of the event ΔPSI ≥ 1.0 and shall state the event wherever a probability is shown. | 01 | M | RG, UT-03, E2E-12 |
| FR-06 | The system shall display the 28 × 19 effect matrix as a heatmap, with the wild-type residue marked, and a switch between raw score and calibrated probability. | 01 | M | E2E-01 |
| FR-07 | The system shall show a ranking table with all substitutions that can be sorted by any column and filtered by position and by substituted amino acid. | 02 | M | E2E-02 |
| FR-08 | The system shall flag the top 10 % of substitutions by rank within the tile. | 02 | S | UT-04, E2E-02 |
| FR-09 | The system shall assign every tile and prediction a domain status (`measured_in_domain`, `measured_out_of_domain`, `measured_unreliable`, `predicted_*`, `unknown`) from measured data, and from a gate model when one is registered. | 01 | M | UT-06, ETL-05 |
| FR-10 | The system shall refuse to score a tile whose domain status is `measured_out_of_domain` or `predicted_out_of_domain`, with an explanation, unless the user explicitly overrides; an overridden result shall carry the warning `OUT_OF_DOMAIN_OVERRIDDEN`. | 01 | M | API, E2E-09 |
| FR-11 | The system shall show a prominent warning whenever the domain status is `unknown`, `measured_unreliable` or predicted, and always before the scores. | 01 | M | E2E-12 |
| FR-12 | The system shall export the result as CSV with the nine columns of the research prototype, preceded by provenance comment lines. | 03 | M | API, RG-02 |
| FR-13 | The system shall export the result as JSON containing the full prediction object and provenance. | 03 | M | API |
| FR-14 | The system shall show, and write into every export, the provenance: model id, weights SHA-256, event definition, evidence label, domain description, domain status, data sources with licences, code version, generation time and the disclaimer that scores are not probabilities of disease. | 01, 03 | M | API, E2E-12 |
| FR-15 | The system shall let the user find a protein by gene symbol or accession (reviewed human proteins of the loaded UniProt release). | 04 | M | API, E2E-04 |
| FR-16 | The system shall list the tiles of a protein with their domain status and let the user choose one. | 04 | M | API, E2E-04 |
| FR-17 | The system shall offer, for tiles with measured data, an overlay of measured ΔPSI labelled as part of the training data. | 05 | S | API, E2E-05 |
| FR-18 | The system shall offer an overlay of ClinVar missense variants with the ClinVar attribution and diagnostic disclaimer shown beside it. | 06 | S | API, E2E-06 |
| FR-19 | The system shall provide a model card page with metrics and their confidence intervals, limitations and the evidence label. | 07 | M | API, E2E-07 |
| FR-20 | The system shall let the user, on request only, store a result behind a share link that expires after at most 30 days and shall delete expired runs. | 03 | C | UT-10, API, E2E-11 |
| FR-21 | The system shall provide a page listing every data source with version, licence and required attribution. | 07 | M | API, E2E-07 |
| FR-22 | The system shall keep a registry of model versions, shall use the default frozen model unless another frozen model is requested, and shall record the model id in every result. | 01, 07 | M | API |
| FR-23 | If generating or downloading an export fails, the system shall report the error and keep the result on screen. | 03 | M | E2E-10 |

## 5. Non-functional requirements

Thresholds are proposals *(to be measured)* on a reference host of 2 vCPU and 2 GB RAM, as recorded in the test report. They replace the `[PENDING]` of Chapter 1 once measured.

| ID | Category | Requirement | Proposed threshold | Verify |
|---|---|---|---|---|
| NFR-01 | Performance | Server time for one tile prediction (532 cells), p95 | ≤ 300 ms *(to be measured)* | NF-01 |
| NFR-02 | Performance | Server time for listing the tiles of a protein of 1,000 residues (about 44 tiles), p95 | ≤ 200 ms *(to be measured)* | NF-02 |
| NFR-03 | Performance | Time from request to rendered heatmap in the browser on a standard laptop, p95 | ≤ 1.5 s *(to be measured)* | NF-06 |
| NFR-04 | Reliability / correctness | Scores and probabilities from the API equal those of the research runner and of `predict.py`; maximum absolute difference | < 1e-9 (JSON); < 5e-9 in CSV because of 10-digit rounding | RG-01, RG-02 |
| NFR-05 | Reliability | The same input and model version give identical output | exact | PB-03 |
| NFR-06 | Reliability | The service refuses to start serving if the hash of the loaded weights differs from the registered one | always | UT-09, DEP-01 |
| NFR-07 | Security / abuse | Maximum request body; rate limit on prediction endpoints | 4 KiB; 60 per minute per client *(to be fixed)* | NF-04, NF-05 |
| NFR-08 | Security | Input is never executed, evaluated or interpolated into queries or file names | always | SEC-02 |
| NFR-09 | Privacy | Sequences, accessions and share tokens do not appear in logs; sequences are not stored unless a share link is requested | always | SEC-01, SEC-04 |
| NFR-10 | Privacy | Shared runs expire; maximum lifetime; purge interval | ≤ 30 days; ≤ 1 h | UT-10, API |
| NFR-11 | Accessibility | Conformance level of all pages; keyboard-only use of every function; colour never the only carrier of information | WCAG 2.1 AA | A11Y-01 to A11Y-04 |
| NFR-12 | Compatibility | Supported browsers; minimum viewport | latest two releases of Chrome, Firefox, Safari, Edge; 360 px wide | E2E (matrix) |
| NFR-13 | Legal | No data from a source with `redistribution_ok = false` in the database, model or UI | always | ETL-03 |
| NFR-14 | Legal | ClinVar attribution and disclaimer present on every view showing ClinVar data | always | E2E-06 |
| NFR-15 | Honesty | The evidence label appears on the result page, the model card and in every export | always | E2E-12, API |
| NFR-16 | Maintainability | Database changes through versioned migrations; one command builds and starts all services | `docker compose up` | DEP-01 |
| NFR-17 | Maintainability | Automated test suites run in CI; backend line coverage | ≥ 85 % *(to be fixed)* | CI report |
| NFR-18 | Portability | API container memory with the model loaded | ≤ 512 MB *(to be measured)* | NF-03 |
| NFR-19 | Observability | Every response carries a request id; structured logs contain route template, status and duration only | always | SEC-01 |
| NFR-20 | Documentation | Installation guide (local Docker, free hosting, VPS) tested from a clean checkout | complete | DEP-01, DEP-02 |

## 6. Data and interface requirements

* **Data:** the schema, sources and ETL rules of [db-design.md](db-design.md) are part of this specification (DR-1 licence flags enforced in the ETL; DR-2 every reference row points to a `data_source` with SHA-256; DR-3 the ETL is idempotent and fails on any hash mismatch).
* **External interface:** the REST contract of [openapi.yaml](openapi.yaml) (IR-1). There are no other external systems; the service does not call third-party APIs with user input (IR-2).
* **User interface:** [ui-design.md](ui-design.md) (IR-3).

## 7. Verification approach

The method per requirement is test, inspection or demonstration; the plan, environments and criteria are in [test-plan.md](test-plan.md). A requirement is "verified" only when its test id is in the test report with a passing result and the environment recorded. Back-to-back agreement with the research code shows consistency, not scientific correctness (risk R-1 below).

## 8. Risks tied to requirements

| ID | Risk | Mitigation |
|---|---|---|
| R-1 | Back-to-back tests pass although both paths share an error (for example the label definition) | The 180 features are rebuilt independently in the tool; the evidence label stays on screen; scientific validity is addressed in Chapter 4 experiments, not in software tests |
| R-2 | Users read the calibrated probability as a probability of disease | Event definition next to every probability, disclaimer in every export (FR-05, FR-14) |
| R-3 | A stable tile receives a good-looking score | Domain status and warnings before scores (FR-09 to FR-11); typed sequences are `unknown` until the R3 gate model is integrated |
| R-4 | Free hosting limits storage or CPU | ETL `--clinvar-scope` option; SQLite fallback ([db-design.md](db-design.md) §10) |
| R-5 | Licence breach through an import shortcut | Hard block in the ETL (NFR-13) and a test (ETL-03) |

## 9. Traceability matrix

Requirement → use case → tests. Test ids are defined in [test-plan.md](test-plan.md); a group name stands for all its members relevant to the requirement.

| Requirement | UC | Tests |
|---|---|---|
| FR-01 | 01 | UT-07, PB-01, API-01, E2E-01 |
| FR-02 | 01, 04 | API-02, E2E-04 |
| FR-03 | 01 | PB-02, API-10…API-17, E2E-08 |
| FR-04 | 01 | UT-01, UT-02, RG-01, RG-04 |
| FR-05 | 01 | UT-03, RG-01, E2E-12 |
| FR-06 | 01 | E2E-01 |
| FR-07 | 02 | E2E-02 |
| FR-08 | 02 | UT-04, E2E-02 |
| FR-09 | 01 | UT-06, ETL-05, API-18 |
| FR-10 | 01 | API-19, E2E-09 |
| FR-11 | 01 | E2E-12 |
| FR-12 | 03 | UT-08, RG-02, API-30, E2E-03 |
| FR-13 | 03 | API-31, E2E-03 |
| FR-14 | 01, 03 | API-01, API-30, API-31, E2E-12 |
| FR-15 | 04 | API-20, E2E-04 |
| FR-16 | 04 | UT-05, API-21, E2E-04 |
| FR-17 | 05 | API-22, E2E-05 |
| FR-18 | 06 | API-23, E2E-06 |
| FR-19 | 07 | API-24, E2E-07 |
| FR-20 | 03 | UT-10, API-40…API-44, E2E-11 |
| FR-21 | 07 | API-25, E2E-07 |
| FR-22 | 01, 07 | API-24, UT-09 |
| FR-23 | 03 | E2E-10 |
| NFR-01 | — | NF-01 |
| NFR-02 | — | NF-02 |
| NFR-03 | — | NF-06 |
| NFR-04 | — | RG-01, RG-02 |
| NFR-05 | — | PB-03 |
| NFR-06 | — | UT-09, DEP-01 |
| NFR-07 | — | NF-04, NF-05 |
| NFR-08 | — | SEC-02 |
| NFR-09 | — | SEC-01, SEC-04 |
| NFR-10 | — | UT-10, API-43 |
| NFR-11 | — | A11Y-01…A11Y-04 |
| NFR-12 | — | E2E browser matrix |
| NFR-13 | — | ETL-03 |
| NFR-14 | — | E2E-06, API-23 |
| NFR-15 | — | E2E-12, API-01 |
| NFR-16 | — | DEP-01 |
| NFR-17 | — | CI coverage report |
| NFR-18 | — | NF-03 |
| NFR-19 | — | SEC-01 |
| NFR-20 | — | DEP-01, DEP-02 |
