# Proposed changes to thesis Chapters 1 and 3

**Nothing in this file has been applied.** `report/` was not edited. Each item names the place, quotes or summarises the current text, gives the proposed change and the reason. Items marked **APPROVAL** change the meaning of something the author wrote or decided; the rest only fill `[PENDING]` or bring text in line with measured facts. Source documents: [srs.md](srs.md), [db-design.md](db-design.md), [api-spec.md](api-spec.md), [ui-design.md](ui-design.md), [test-plan.md](test-plan.md).

## Chapter 1 — `report/chapters/01-problem-description.tex`

| # | Place | Current | Proposed | Reason / flag |
|---|---|---|---|---|
| C1-1 | §Functions of the System | UC-01, UC-02, UC-03 | Add UC-04 *Select a tile from a UniProt protein*, UC-05 *Compare with measured data* (promoted from the *Extend* relation of UC-01), UC-06 *View ClinVar variants*, UC-07 *View the model card*. LaTeX in §A below | The tool needs a way to choose a tile and to show provenance/limits; they are traced in the SRS. **APPROVAL** (scope) |
| C1-2 | UC-01 *Event handling* | 1 enter, 2 validate length/alphabet/domain, 3 score, 4 display | Insert "the system determines the domain status of the tile" between 2 and 3; step 4 "displays domain status and warnings before the matrix" | Matches FR-09 to FR-11 |
| C1-3 | UC-01 *Alternative / exceptional flows* | "Invalid or out-of-domain input: the system shows an explicit message and does not return scores." | Split: (a) invalid input → message, no scores; (b) tile **measured** to be outside the domain → refusal with the reason, and the user may explicitly choose to score anyway (result then carries a prominent override warning in screen and exports); (c) domain **unknown** (typed sequence, or tile not in the screen) → scores with a prominent warning | **APPROVAL.** The override and the `unknown` case relax the present wording. Needed because the model cannot see whether a typed sequence is in its domain until the gate model (R3) exists. If the author prefers to keep the strict wording, `unknown` would have to be refused too, which would block every typed sequence |
| C1-4 | §Non-Functional Requirements (heading) | "These are targets for the prototype; [PENDING: concrete thresholds …]" | Replace the pending note with the table in §B and the sentence "Thresholds marked * are proposals and are replaced by measured values in Chapter 4" | Fills `[PENDING]` |
| C1-5 | §Performance | "should finish in interactive time … (target to be measured)" | NFR-01 to NFR-03 with the proposed figures | Fills `[PENDING]` |
| C1-6 | §Information Safety | "Only public data are used; terms of use … recorded before redistribution." | Add: sources without a licence permitting redistribution (Koren et al. 2018, MetaDegron/ELM tables, Larsen et al. 2025) are not loaded into the service; ClinVar data are shown only with attribution and the ClinVar diagnostic disclaimer | Matches CON-1, CON-2, NFR-13, NFR-14 |
| C1-7 | §Security | "user-supplied sequences are not executed or stored beyond the session unless stated" | Add "unless the user requests a share link, in which case the result is stored for at most 30 days and then deleted"; add rate limiting and request-size limit | Matches FR-20, NFR-07, NFR-09, NFR-10 |
| C1-8 | §Reliability | "scores shown in the interface must match the research runner within numerical tolerance" | State the tolerance: below 1e-9 (JSON), 5e-9 (CSV) | NFR-04; value already measured for the CLI prototype |
| C1-9 | §Implementation Constraints | "computation runs on CPU-class hardware" | Say: the service runs on CPU hardware; exploratory model training (planned experiments R1, R2, R3) runs offline in hosted notebooks and is not part of the service | The next-phase plan uses notebook GPUs for training, which the present sentence contradicts. **APPROVAL** |
| C1-10 | §Accessibility (new subsection under Non-Functional) | absent | Add "Usability and accessibility Requirements": WCAG 2.1 AA, keyboard-only use, colour not the only carrier (NFR-11, NFR-12) | Template has no such heading; add if the Faculty template allows extra subsections |
| C1-11 | Intro of §Functions | Already updated to say a minimal CLI prototype exists | After the web tool is built, replace by "the prototype is a web application (Chapter 3)" | Keep in step with progress |

### A. LaTeX for UC-04 to UC-07 (same macros as UC-01)

```latex
\subsection{Select a Tile from a UniProt Protein}
\begin{usecasespec}{Select a tile from a UniProt protein}{tab:uc-tile}
  \ucname{Select tile}{UC-04}
  \ucactor{User}{Important}{Simple}
  \ucfull{Stakeholders and interests:}{Researcher: wants to score a region of a known protein without copying its sequence.}
  \ucfull{Summary description:}{The user searches a protein by gene symbol or accession and chooses one of its 28-residue tiles, shown with their domain status.}
  \ucfull{Relationships:}{Association: User \newline Include: --- \newline Extend: --- \newline Generalization: ---}
  \ucfull{Event handling:}{1.~The user enters a gene symbol or accession. \newline 2.~The system lists matching proteins. \newline 3.~The user chooses a protein. \newline 4.~The system shows its tiles with domain status. \newline 5.~The user chooses a tile and continues with UC-01.}
  \ucfull{Alternative / exceptional flows:}{No match, protein shorter than 28 residues, or tile with a non-standard residue: the system states the reason and does not offer scoring.}
  \ucfull{Expected outcome:}{A tile selected for UC-01.}
\end{usecasespec}

\subsection{Compare with Measured Data}
\begin{usecasespec}{Compare with measured data}{tab:uc-measured}
  \ucname{Compare with measured data}{UC-05}
  \ucactor{User}{Medium}{Simple}
  \ucfull{Stakeholders and interests:}{Researcher: wants to see measured effects beside predicted ones.}
  \ucfull{Summary description:}{For tiles with measured saturation data, the system overlays measured $\Delta$PSI on the matrix and states that these data were used to train the model.}
  \ucfull{Relationships:}{Association: User \newline Include: Predict effect matrix \newline Extend: --- \newline Generalization: ---}
  \ucfull{Event handling:}{1.~The user switches on the measured layer. \newline 2.~The system overlays the measured values and the caption on training use.}
  \ucfull{Alternative / exceptional flows:}{No measured data for the tile: the layer is disabled with the reason.}
  \ucfull{Expected outcome:}{Measured values beside predictions, never presented as validation.}
\end{usecasespec}

\subsection{View ClinVar Variants}
\begin{usecasespec}{View ClinVar variants}{tab:uc-clinvar}
  \ucname{View ClinVar variants}{UC-06}
  \ucactor{User}{Medium}{Simple}
  \ucfull{Stakeholders and interests:}{Researcher: wants to know which substitutions of the tile have been reported in clinical submissions.}
  \ucfull{Summary description:}{The system marks cells that correspond to ClinVar missense variants, with significance and review status, together with the ClinVar attribution and diagnostic disclaimer.}
  \ucfull{Relationships:}{Association: User \newline Include: Predict effect matrix \newline Extend: --- \newline Generalization: ---}
  \ucfull{Event handling:}{1.~The user switches on the ClinVar layer. \newline 2.~The system marks the cells and shows the attribution and disclaimer beside the layer.}
  \ucfull{Alternative / exceptional flows:}{No variant in the tile: the system says so.}
  \ucfull{Expected outcome:}{Variant annotations that are not read as a diagnosis.}
\end{usecasespec}

\subsection{View the Model Card}
\begin{usecasespec}{View the model card}{tab:uc-card}
  \ucname{View model card}{UC-07}
  \ucactor{User}{Medium}{Simple}
  \ucfull{Stakeholders and interests:}{Researcher and examiner: want to know what the numbers mean and how far they can be trusted.}
  \ucfull{Summary description:}{The system shows model version and hash, predicted event, supported domain, metrics with confidence intervals, limitations, data sources and licences.}
  \ucfull{Relationships:}{Association: User \newline Include: --- \newline Extend: --- \newline Generalization: ---}
  \ucfull{Event handling:}{1.~The user opens the model card. \newline 2.~The system displays it.}
  \ucfull{Alternative / exceptional flows:}{Model information unavailable: the system reports the error.}
  \ucfull{Expected outcome:}{The user knows the evidence level (development benchmark, not external validation).}
\end{usecasespec}
```

### B. Non-functional requirement table for Chapter 1 (proposed)

| Requirement | Proposed value | Status |
|---|---|---|
| Server time, one tile (532 cells), p95 | ≤ 300 ms on 2 vCPU / 2 GB | to be measured |
| Server time, tile list of a 1,000-residue protein, p95 | ≤ 200 ms | to be measured |
| Time to rendered heatmap, p95 | ≤ 1.5 s | to be measured |
| Agreement with the research runner | < 1e-9 (JSON), < 5e-9 (CSV) | measured for the CLI prototype (largest difference below 1e-9) |
| Request body; rate | 4 KiB; 60 per minute per client | to be fixed |
| Retention of shared results | ≤ 30 days, purge at most hourly | design |
| Accessibility | WCAG 2.1 AA, keyboard-only | to be tested |
| Browsers | Latest two releases of Chrome, Firefox, Safari, Edge; width ≥ 360 px | to be tested |
| API container memory | ≤ 512 MB | to be measured |

## Chapter 3 — `report/chapters/03-solution-design.tex`

| # | Place | Current | Proposed | Reason / flag |
|---|---|---|---|---|
| C3-1 | §System Overview → Product Context | Two parts: research pipeline and prototype tool | Add that the tool is a web application (browser, API, database) around the frozen model; training happens offline in notebooks | Makes C1-9 consistent |
| C3-2 | §Functional Overview | "predict, rank, export" | Extend to UC-01…UC-07 | Follows C1-1 |
| C3-3 | §Architectural Components | `[PENDING: architecture diagram and component roles.]` | Diagram of browser SPA – REST API (inference package) – PostgreSQL, plus ETL and offline notebooks; role table. Source: [README.md](README.md) §1 and `ui-design.md` §8 for the frontend components. Draw as a figure (TikZ or an image generated from a diagram file kept in `report/assets/`) | Fills `[PENDING]` |
| C3-4 | §Interaction Between Components | `[PENDING]` | Sequence diagrams for UC-01 (typed sequence; stored tile), the domain-refusal flow, and the share-link flow, from `api-spec.md` §3–4 and `ui-design.md` §9 | Fills `[PENDING]` |
| C3-5 | §Design Rationale | `[PENDING: advantages and drawbacks …]` | Text from [README.md](README.md) §2 (D-1…D-12): stateless design, numpy-only inference, two-tier domain gate, licence enforcement in the ETL, generated frontend types; drawbacks: single developer, no external validation, gate model absent, hosted limits | Fills `[PENDING]` |
| C3-6 | Table `tab:sources` (Planned data sources) | Zhang Mendeley, GEO, Voutsinos, Larsen, UniProt | Add ClinVar (attribution and disclaimer); state that Larsen and Voutsinos are **not** loaded in the service v1, and that Koren et al. 2018 was audited and rejected as a training source (5 new clusters against a gate of 20) and kept for offline use only; replace "planned" by "used" where applicable | Matches the data ledger; **APPROVAL** because the table is currently a plan |
| C3-7 | §Data Model | `[PENDING]` | ER diagram and condensed DDL from [db-design.md](db-design.md) §2, §4 (generate the table from the DDL file to avoid transcription errors) | Fills `[PENDING]` |
| C3-8 | §Data Dictionary | `[PENDING: table of fields.]` | Tables of [db-design.md](db-design.md) §5 (long; consider moving the full dictionary to Appendix B and keeping a summary in the chapter) | Fills `[PENDING]` |
| C3-9 | §Relationships Between Entities | `[PENDING]` | Prose from `db-design.md` §1, §3, §6 (provenance, two-tier gate, licence per table) | Fills `[PENDING]` |
| C3-10 | §Method and Model Design | "The baseline is ridge … reference models … Transfer learning … examined … **[PENDING: final architecture, objective function and training configuration.]**" | State the final model of the service: 180 features (wild-type and substituted residue one-hot, tile composition, one-hot context at offsets ±1…±3), ridge regression (regularisation 10, selected on a cluster-aware inner validation), trained on 176 peptides / 92,337 cells with the relaxed threshold 4.0, Platt calibration for P(ΔPSI ≥ 1.0). Cite the experiment files (`learning-curve-2026-10-22`, `calibration-p6-2026-10-22`). Say that the designs with larger capacity and the transfer-learning design tested so far did not meet their pre-registered criteria | Fills `[PENDING]`; numbers from `results.json`, generated by script as in Chapter 4 |
| C3-11 | §Method — domain gate | absent | Add the two-tier domain gate (measured tile PSI now; predicted wild-type PSI from the R3 gate model, which passed its criteria on 22 Oct 2026, with the third state `borderline`) | Needed to explain FR-09 to FR-11 |
| C3-12 | §Functional Design | `[PENDING: processing flow and interface for each function.]` | For each UC: processing flow (reference `api-spec.md`), screen (reference `ui-design.md`), and the endpoint table of `api-spec.md` §2 | Fills `[PENDING]` |
| C3-13 | New §Deployment View (optional) | absent | Containers, configuration, local / free-hosting / VPS options from [README.md](README.md) §5; move installation steps to Appendix A | The template has an installation appendix |
| C3-14 | Appendix A (`a-installation-user-guide.tex`) | pending | Installation from the deployment guidance once the tool exists; user guide from `ui-design.md` | Later |

## Chapter 4 (note only)

Chapter 4 §4.3–4.6 currently describes the CLI prototype and back-to-back testing. When the web tool and tests exist, replace with the groups of [test-plan.md](test-plan.md) and report the results of all groups, including NF measurements with host and date. No edit is proposed now.

## What the author should decide

1. C1-1 (add UC-04…UC-07) and the relaxed wording of C1-3 (override; `unknown` case).
2. C1-9 (notebook training stated as outside the service).
3. C3-6 (change "planned sources" to "used / rejected / not loaded").
