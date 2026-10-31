# User Interface Design

Status: **v0.2 local design, 29 Oct 2026.** Baseline single-tile screens below are retained; workspace/job/import additions in §12 are planned. Public sharing is retired.  Wireframes are ASCII and show structure, not final styling. Values inside the wireframes (ranks, scores, probabilities, the out-of-domain PSI of 4.8) are **placeholders**, not model output; only the A6NMZ7 tile sequence and tile PSI come from the repository data. They realise the baseline UC-01 to UC-07 of [srs.md](srs.md) against the endpoints of [api-spec.md](api-spec.md). Stack: React + TypeScript (Vite); the baseline uses custom SVG with D3 colour scales, as recorded in app/frontend/README.md. New screens remain planned.

## 1. Principles

1. **Say what the number is, always next to it.** A score or probability is never shown without (a) the domain status, (b) the model id, and (c) for probabilities, the event they predict (`P(ΔPSI ≥ 1.0)`).
2. **Warnings come before scores** in reading order and in the DOM, so that screen-reader users hear them first.
3. **Do not decorate uncertainty away.** The evidence label ("development OOF benchmark, not external validation") is visible on the result page without scrolling or clicking.
4. **Colour is never the only carrier** of information (text, pattern or position repeats it).
5. **Saved results use IDs, never sequences in URLs.** Reopen immutable project snapshots; unsaved previews remain in memory. The browser is a local client of one trusted workspace.

Direction of the quantity, to be written in the interface wherever needed: ΔPSI ≥ 1.0 means the substitution **raises the stability index by at least one bin of the assay**, i.e. it is predicted to **weaken the degron signal** of the tile in this assay. Higher is therefore "more disrupting".

## 2. Site map

```
/                      Input         (UC-01, UC-04)
/protein/:acc          Tile picker   (UC-04)
/result                Result        (UC-01, UC-02, UC-05, UC-06, UC-03)   state in memory, not in the URL for typed sequences
/result/uniprot/:acc/:n   Reference-tile preview (no sequence in URL)
/projects               Project list (UC-10)
/projects/:project_id   Workspace and history (UC-10)
/jobs/:job_id           Batch/protein progress and outcomes (UC-08)
/datasets/:dataset_id   Import preview and dataset details (UC-09)
/analyses/:analysis_id  Saved analysis and comparison (UC-05, UC-10)
/model                 Model card    (UC-07)
/about                 About, data sources and licences (UC-07)
```

## 3. Pages

### 3.1 Input (`/`)

Two tabs. The default tab is the one the user used last in the session.

```
+--------------------------------------------------------------------------------+
|  Degron Footprint     [Input] [Model card] [About & data]                      |
+--------------------------------------------------------------------------------+
|  Predict the effect of every substitution in a 28-residue degron tile          |
|  Assay: GPS (Zhang et al. 2023). Model m3-ext4.0-platt-v1. Development benchmark.|
|                                                                                |
|  ( Paste a sequence )   ( Choose a protein )                                   |
|  +---------------------------------------------------------------------+       |
|  | Tile sequence (exactly 28 amino acids)                               |       |
|  | [ DIMFLVDSSGSIGPENFSKMKTFMKNLV                                  ]    |       |
|  | 28 / 28 characters                                                   |       |
|  +---------------------------------------------------------------------+       |
|  ! Domain of a typed sequence is unknown. The model was trained only on tiles   |
|    that behave as degrons (wild-type PSI <= 4.0) and cannot check yours.       |
|                                                                                |
|  [ Predict ]                                                                   |
+--------------------------------------------------------------------------------+
```

*Protein tab*: an autocomplete field (`GET /v1/proteins?query=`, debounce 250 ms) lists `GENE — name — accession — n tiles`. Choosing a protein goes to the tile picker.

* **Live validation** (no round trip for what the client can check): count of characters `n / 28`; characters outside the 20 letters are underlined and named: "Position 7: 'B' is not a standard amino acid." Submit is disabled only while the sequence is empty; an invalid sequence is submitted-blocked with the message focused.
* **Privacy:** a typed sequence is sent in a POST body and the unsaved preview stays in memory, never in the URL, `localStorage` or analytics. Explicit Save to project persists it in the local workspace. A stored tile is addressed by accession and index, so its URL contains no user input.

### 3.2 Tile picker (`/protein/:acc`)

```
+--------------------------------------------------------------------------------+
|  COL6A6 (A6NMZ7) - 2,263 residues - 98 tiles                                   |
|  Tile map (one box per tile, left to right = N to C terminus):                 |
|  [##][##][..][##][??][..][##]...   legend: ## in domain  .. outside  ?? unreliable|
|                                           -- unknown: no marker, grey dotted   |
|  Selected: tile 28  (residues 622-649)  DIMFLVDSSGSIGPENFSKMKTFMKNLV          |
|  Status: in domain (measured tile PSI 1.88, replicate 1; gate status requires R3 integration) |
|                                                                                |
|  [ Predict this tile ]                                                         |
+--------------------------------------------------------------------------------+
```

* Each tile box has a text label on focus and in the tooltip ("tile 28, residues 622–649, in domain"), and a pattern in addition to colour: solid fill = in domain, hatched = outside, dotted outline = unreliable, empty = unknown.
* Non-scorable tiles are disabled with `aria-disabled` and the reason.
* For long proteins the map scrolls horizontally; a list view with the same data is available (table of tiles, sortable by status) for keyboard and screen-reader users.

### 3.3 Result (`/result…`)

```
+--------------------------------------------------------------------------------+
|  A6NMZ7 tile 28 (622-649) - model m3-ext4.0-platt-v1 - [ Model card ]          |
+--------------------------------------------------------------------------------+
|  DOMAIN: in domain - measured tile PSI 1.88 (replicate 1)                      |
|  ! This tile is among the peptides the model was trained on; scores are not    |
|    an out-of-sample estimate.                                                  |
|  Evidence: development OOF benchmark, not external validation.                 |
+--------------------------------------------------------------------------------+
|  View: (o) probability P(DeltaPSI >= 1.0)  ( ) raw score     Layers: [ ] measured|
|                                                                      [ ] ClinVar |
|        A C D E F G H I K L M N P Q R S T V W Y        colour bar 0 ----- 1      |
|   1 D  . . - . . . . . . . . . . . . . . . . .                                |
|   2 I  . . . . . . - . . . . . . . . . . . . .                                |
|   ...                                                                          |
|  28 V  . . . . . . . . . . . . . . . . . - . .       (- = wild type, no cell) |
|                                                                                |
|  Ranking (532 substitutions)  Filter: position [ all v ] amino acid [ all v ]  |
|  +------+-----+----+-----+------------+---------------+--------------+        |
|  | rank | pos | wt | mut | raw score  | P(dPSI>=1)    | top 10 %     |        |
|  | 1    | 14  | D  | W   | 1.42       | 0.58          | yes          |        |
|  +------+-----+----+-----+------------+---------------+--------------+        |
|  [ Export CSV ] [ Export JSON ] [ Save to project ]                          |
+--------------------------------------------------------------------------------+
|  Provenance: model m3-ext4.0-platt-v1 | weights 8bec0b04... | data: Zhang 2023  |
|  (CC BY 4.0) | generated 2026-10-22T12:00Z | Not a probability of disease.     |
+--------------------------------------------------------------------------------+
```

* **Block order (DOM order = reading order):** header, domain banner, warnings, evidence label, controls, heatmap, ranking, actions, provenance footer.
* **Heatmap:** rows = positions 1–28 labelled `position + wild-type letter`; columns = the 20 amino acids; the wild-type cell is shown as a hatched cell with the label "wild type". Each cell exposes a tooltip and a keyboard-focusable description: "position 14, D to W, probability 0.58, raw score 1.42, rank 1 of 532".
* **Scale toggle:** probability (sequential, 0–1) or raw score (diverging around 0). The legend states the event in words: "Probability that the substitution raises PSI by at least one bin (weakens the degron signal) in this assay."
* **Overlay layers** are off by default and appear only when data exist (otherwise a disabled control with the reason, not a hidden control):
  * *Measured ΔPSI* — outlined cell with measured value on hover; a persistent caption: "Measured values are part of the training data of this model; they are not a validation."
  * *ClinVar* — a marker glyph (diamond) on the cell, different shape per significance class in addition to colour; the ClinVar attribution and the diagnostic disclaimer sit directly under the layer toggle and in the hover card.
* **Ranking table:** all 532 rows (baseline native table; paginate job-level results), sortable columns, filters for position and amino acid; the top-10 % flag is text ("yes"), not only colour; row focus syncs with the heatmap cell.
* **Actions:** CSV/JSON download (FR-12, FR-13); *Save to project* selects a local project and explains that input/results persist until deletion; no share token or 7/30-day project expiry.

### 3.4 States of the result page

| State | What the user sees | Behaviour |
|---|---|---|
| Loading | Skeleton of the heatmap, text "Scoring 532 substitutions…" (`aria-live=polite`) | Cancel button; request aborted on navigation |
| Success | §3.3 | — |
| Success with warning (`unknown`, `unreliable`, predicted, training peptide) | Warning block (amber, icon, text) above the heatmap | Cannot be dismissed; reappears on every view |
| **Refused: out of domain** (`OUT_OF_DOMAIN`) | Page replaced by a notice: "This tile is outside the domain of the model. The frozen domain gate classifies this tile outside the supported range; inspect its source and estimator before overriding." Buttons: *Choose another tile*, *Score anyway* | *Score anyway* re-sends with `override_domain=true`; the result then shows a red banner "Out-of-domain override" and the warning stays in every export |
| Validation error (`INVALID_*`) | Inline on the input, message from the API (never a generic "error") | Focus moves to the field |
| Not found (`UNKNOWN_ACCESSION`, `TILE_OUT_OF_RANGE`) | Message with the valid range, link back to search | — |
| Empty overlay | "No ClinVar missense variant in this tile." / "No measured data for this tile." | — |
| Export error | Inline message "The file could not be created. Your result is still here." | Result unchanged (FR-23) |
| Rate limited (`RATE_LIMITED`) | "Too many requests. Try again in N seconds." using `Retry-After` | Button disabled with countdown |
| Service unavailable (503) | "The service is not ready (model or database unavailable)." with a retry link | `/healthz` polled every 10 s |

### 3.5 Local save and reopen

Choose a project and explicitly save the current analysis. Show that input, output and provenance will persist locally until deletion. Saved URLs contain only an analysis ID; there is no public sharing/token screen. Reopening reads the frozen snapshot; “Run again” creates a new history entry.

## 4. Mandatory warning rules

| ID | Rule |
|---|---|
| W-1 | Domain banner is present on every result view, with the status in words. |
| W-2 | For `unknown`, `measured_unreliable`, `borderline`, `predicted_*`: an amber warning block above the heatmap, not dismissible. |
| W-3 | For an overridden out-of-domain result: a red banner on the page and the warning in every export. |
| W-4 | Every probability is accompanied by the event `P(ΔPSI ≥ 1.0)` in the column header, legend or tooltip. |
| W-5 | The evidence label appears on the result page and in exports. |
| W-6 | ClinVar layer: attribution and diagnostic disclaimer directly beside the toggle and in the hover card. |
| W-7 | Training peptide: warning "scores are not an out-of-sample estimate". |
| W-8 | No text in the interface may describe a score as risk of disease, pathogenicity, or diagnosis. |

## 5. Colour, contrast and non-colour cues

| Use | Palette | Cue besides colour |
|---|---|---|
| Probability 0–1 (sequential) | Viridis, light (low) to dark (high) reversed so that high probability is darkest | Numeric value on focus/hover; legend with ticks |
| Raw score (diverging, centre at 0) | ColorBrewer PuOr 11-class: `#7f3b08 #b35806 #e08214 #fdb863 #fee0b6 #f7f7f7 #d8daeb #b2abd2 #8073ac #542788 #2d004b` (orange = negative, purple = positive); blue–orange/purple family chosen for colour-vision deficiency | Sign shown in tooltip |
| Domain status | Distinct fills targeted for colour-vision simulation (verification pending) | Pattern (solid / hatched / dotted / empty) and text |
| Warning levels | Amber (notice), red (override) | Icon and the word "Warning"/"Override" |
| ClinVar classes | Marker shapes per class | Shape and text in hover card |

Text contrast ≥ 4.5 : 1, large text and UI components ≥ 3 : 1 (WCAG 2.1 AA). Light and dark themes target these levels; theme follows the system preference with a manual switch.

## 6. Keyboard and ARIA

* Skip link to main content; landmarks `header`, `nav`, `main`, `footer`.
* Tab order follows the DOM order of §3.3. The heatmap is one composite widget (`role="grid"`) with roving `tabindex`; arrow keys move between cells, `Enter` selects and syncs the ranking row; `Esc` leaves the grid. A "table view" toggle presents the same data as a plain accessible table.
* The warning block has `role="alert"` when it appears after a request, otherwise `role="note"`.
* Live regions: loading and result summary (`aria-live="polite"`), errors (`assertive`).
* Every form control has a visible label; error messages are linked with `aria-describedby`.
* Respect `prefers-reduced-motion`; no auto-playing animation.
* Language attribute `en`; amino-acid sequences have `translate="no"` and a monospace font, and are announced letter by letter only on request (an "Read sequence" button), to avoid noisy output.

## 7. Heatmap requirement (library-independent)

Render 532 cells + 28 wild-type cells in one SVG or canvas; cell size ≥ 24 × 24 CSS px at 1280 px width (≥ 16 px on 360 px width with horizontal scroll); on small screens the table view is the default; selection and hover must not re-render the whole grid; initial render within NFR-03.

## 8. Components (React)

| Component | Props (TypeScript) | Responsibility |
|---|---|---|
| `AppShell` | `children` | Header, nav, footer, theme switch, skip link |
| `InputPage` | — | Tabs, owns the form state |
| `SequenceInput` | `value: string; onChange; error?: ApiError` | Live validation and messages (§3.1) |
| `ProteinSearch` | `onSelect(p: ProteinSummary)` | Debounced autocomplete |
| `TileMap` | `tiles: TileSummary[]; selected?: number; onSelect(i: number)` | Tile boxes with patterns and keyboard support |
| `ResultPage` | route state | Orchestrates the query, layers and actions |
| `DomainBanner` | `domain: DomainInfo` | Status text and measured evidence |
| `WarningList` | `warnings: Warning[]; overridden: boolean` | Rules W-2, W-3, W-7 |
| `EvidenceLabel` | `provenance: Provenance` | Rule W-5 |
| `Heatmap` | `cells: Cell[]; tile: TileInfo; mode: 'prob' \| 'raw'; measured?: MeasuredCell[]; clinvar?: ClinvarVariant[]; onSelect(c: Cell)` | Grid, legend, tooltips, ARIA grid |
| `ScaleToggle` | `mode; onChange` | Probability / raw score |
| `LayerToggles` | `measuredAvailable: boolean; clinvarAvailable: boolean; state; onChange` | Overlay controls; disabled with reason |
| `ClinvarNotice` | `disclaimer: string; attribution: string` | Rule W-6 |
| `RankTable` | `cells: Cell[]; filter; onFilter; selected?; onSelect` | Sort/filter tile rows; job tables paginate |
| `ExportMenu` | `request: PredictRequest; onError(e)` | CSV/JSON download; explicit Save to project action |
| `ProvenanceFooter` | `provenance: Provenance` | Always visible provenance line |
| `RefusalNotice` | `error: ApiError; onOverride(); onBack()` | Out-of-domain flow |
| `ModelCardPage` | — | Reads `/v1/models/{id}` |
| `AboutPage` | — | Reads `/v1/sources` |
| `ErrorBanner` | `error: ApiError` | Maps error codes to messages (§3.4) |

The baseline uses generated OpenAPI types. Regenerate and reconcile the client when implementing the planned v0.2 operations; this documentation update does not claim that baseline types already cover them.

## 9. State and data flow

```
idle --submit--> validating(client) --ok--> loading(POST /v1/predict)
   ^                  | invalid                   |-- 200 --> success(result) --> [layers fetched lazily on toggle]
   |                  v                           |-- 422 OUT_OF_DOMAIN --> refused --override--> loading(override_domain=true)
   +---- edit ---- inputError                     |-- 4xx/5xx --> error(code)
```

* Server state with TanStack Query (cache key = request without sequence for stored tiles; for typed sequences, no cache persistence and `gcTime = 0`).
* UI state (mode, filters, layers, selected cell) in component state; layer data are fetched on first toggle.
* Selected cell, filter and mode may be mirrored in the URL for stored tiles (`?mode=raw&pos=14`), never for typed sequences.
* Types for errors come from `Error.code`; the message shown is the server `message` plus a client-side hint per code.

## 10. Responsive behaviour

360 px minimum width; below 768 px the heatmap becomes horizontally scrollable with the position labels sticky, and the ranking table is shown first with the heatmap behind a toggle. Touch targets ≥ 44 px for controls.

## 11. Open points

* Baseline heatmap uses custom SVG/D3 scales; recheck rendering/accessibility under expanded job views.
* Whether a mock-up in HTML or Figma is wanted for the thesis figures; not part of this design.
* Wording review of the direction note ("weaken the degron signal") with the supervisor before release.

## 12. First-release workspace, batch and import screens (planned)

These screens and state changes are mandatory release-1 scope, not implemented by this document change. Use the same React application and loopback FastAPI service.

### 12.1 Project list and history — UC-10

Navigation: Projects, New analysis, Model, About/data. Project cards show name, updated time, analysis/job/dataset counts. Create/rename acts on the local workspace; no login/account menu. A project has Analysis history, Jobs and Experimental datasets tabs. History rows show immutable run ID, input label, tile/protein context, model/version, date, status and warning badges. Reopen reads saved data; “Run again” visibly creates a new entry. Delete first displays a dependency summary and asks for confirmation; show cleanup errors and retry states. No automatic 30-day expiry for project data.

### 12.2 New analysis and job progress — UC-08

Input modes: Single peptide, Peptide batch, Whole protein. Batch accepts pasted peptide records or multi-record FASTA parsed into stable IDs. Whole protein accepts a loaded human accession or one FASTA record, with optional verified mapping metadata. Select a project before batch submission; clearly state that job inputs/results are persisted locally.

Before submit: preview item count, expected full windows, supported-domain warning, invalid entries, estimated work and configured limits. Do not replace the 28-residue model by a whole-protein prediction. Job page shows terminal/pending/running counts, progress, cancellation, per-item errors/refusals and partial completion. After application restart the same page resumes from durable state. Table pagination avoids rendering every substitution at once; open one tile's matrix on demand.

Protein view: show covered/uncovered intervals including termini, unscorable windows and per-tile domain. Repeated protein positions in overlapping windows keep their tile/context; no silent averaging or global disease ranking. Export all outcomes, not only the current page.

### 12.3 Import validation — UC-09

Choose CSV/TSV, dataset name, assay/endpoint/units, source/reference and replicate metadata. Display a validation preview with file hash and counts for valid, missing, duplicate/conflicting, unmatched and rejected rows. List row-specific corrections. Blocking errors disable Commit; warnings require acknowledgement. State “comparison only; not used to retrain the model”. Staged and committed states are visually distinct. Committing stores a new immutable dataset revision in the selected project.

### 12.4 Comparison and annotations — UC-05/06

Saved-analysis view selects a committed dataset and replicate or explicit aggregation. Show prediction, measurement, residual and units only for comparable endpoints. Display matched/missing/unmatched counts, n and undefined-metric reasons. Different assays appear in separate labelled views. Training-reference observations carry the training caption; imported observations carry their dataset revision and no automatic independent-validation label.

ClinVar and approved supplementary evidence are release-1 layers. Show classification, review/conflict state, accession/release/reference-residue mapping and snapshot date; retain source links, attribution and diagnostic disclaimer. Distinguish no matching variant, mapping unavailable, source unavailable and mapping conflict. Custom unmapped sequences do not acquire guessed annotations.

### 12.5 Component/state additions

`ProjectList`, `ProjectWorkspace`, `HistoryTable`, `SaveAnalysisDialog`, `BatchInput`, `ProteinCoverage`, `JobProgress`, `JobItemTable`, `ImportWizard`, `ValidationReport`, `DatasetList`, `ComparisonPanel`, `AnnotationStatus` and `DeleteConfirmation` extend the baseline components. New server state is keyed by project/job/analysis/dataset ID; no biological payload is persisted in browser URLs or localStorage.

Job: pending → running → completed/partial/failed/cancelled. Import: staged → validation errors or committable → committed; expired preview is explicit. Save/delete/restart have pending/success/error states. Keyboard focus, accessible tables, status text and polite progress announcements apply to all new screens. Figures/wireframes for these additions remain pending until implementation.
