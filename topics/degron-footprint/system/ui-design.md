# User Interface Design

Status: **draft v0.1, 22 Oct 2026.** Wireframes are ASCII and show structure, not final styling. Values inside the wireframes (ranks, scores, probabilities, the out-of-domain PSI of 4.8) are **placeholders**, not model output; only the A6NMZ7 tile sequence and tile PSI come from the repository data. They realise UC-01 to UC-07 of [srs.md](srs.md) against the endpoints of [api-spec.md](api-spec.md). Stack: React + TypeScript (Vite), heatmap with Plotly.js or D3 *(to be chosen on a spike; the requirement is §7, not the library)*.

## 1. Principles

1. **Say what the number is, always next to it.** A score or probability is never shown without (a) the domain status, (b) the model id, and (c) for probabilities, the event they predict (`P(ΔPSI ≥ 1.0)`).
2. **Warnings come before scores** in reading order and in the DOM, so that screen-reader users hear them first.
3. **Do not decorate uncertainty away.** The evidence label ("development OOF benchmark, not external validation") is visible on the result page without scrolling or clicking.
4. **Colour is never the only carrier** of information (text, pattern or position repeats it).
5. **One task per page, URL as state.** Every result is reproducible from its URL (tile or sequence in the query for typed sequences is **not** allowed; see §3.1 on privacy).

Direction of the quantity, to be written in the interface wherever needed: ΔPSI ≥ 1.0 means the substitution **raises the stability index by at least one bin of the assay**, i.e. it is predicted to **weaken the degron signal** of the tile in this assay. Higher is therefore "more disrupting".

## 2. Site map

```
/                      Input         (UC-01, UC-04)
/protein/:acc          Tile picker   (UC-04)
/result                Result        (UC-01, UC-02, UC-05, UC-06, UC-03)   state in memory, not in the URL for typed sequences
/result/uniprot/:acc/:n   Result for a stored tile (shareable URL, no sequence)
/shared/:run_id#t=TOKEN   Shared run (UC-03b)
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
* **Privacy:** a typed sequence is sent in a POST body and kept only in memory (React state), never in the URL, `localStorage` or analytics. A stored tile is addressed by accession and index, so its URL contains no user input.

### 3.2 Tile picker (`/protein/:acc`)

```
+--------------------------------------------------------------------------------+
|  COL6A6 (A6NMZ7) - 2,263 residues - 98 tiles                                   |
|  Tile map (one box per tile, left to right = N to C terminus):                 |
|  [##][##][..][##][??][..][##]...   legend: ## in domain  .. outside  ?? unreliable|
|                                           -- unknown: no marker, grey dotted   |
|  Selected: tile 28  (residues 622-649)  DIMFLVDSSGSIGPENFSKMKTFMKNLV          |
|  Status: in domain (measured tile PSI 1.88, replicate 1)                       |
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
|  [ Export CSV ] [ Export JSON ] [ Create share link ]                          |
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
* **Ranking table:** all 532 rows, virtualised, sortable columns, filters for position and amino acid; the top-10 % flag is text ("yes"), not only colour; row focus syncs with the heatmap cell.
* **Actions:** CSV/JSON download (FR-12, FR-13); *Create share link* is secondary and explains that the sequence will be stored for up to 7 days (selectable 1–30) before the first request.

### 3.4 States of the result page

| State | What the user sees | Behaviour |
|---|---|---|
| Loading | Skeleton of the heatmap, text "Scoring 532 substitutions…" (`aria-live=polite`) | Cancel button; request aborted on navigation |
| Success | §3.3 | — |
| Success with warning (`unknown`, `unreliable`, predicted, training peptide) | Warning block (amber, icon, text) above the heatmap | Cannot be dismissed; reappears on every view |
| **Refused: out of domain** (`OUT_OF_DOMAIN`) | Page replaced by a notice: "This tile is outside the domain of the model. Its measured wild-type PSI is 4.8; the model was trained on tiles with PSI ≤ 4.0, so a score would not be meaningful." Buttons: *Choose another tile*, *Score anyway* | *Score anyway* re-sends with `override_domain=true`; the result then shows a red banner "Out-of-domain override" and the warning stays in every export |
| Validation error (`INVALID_*`) | Inline on the input, message from the API (never a generic "error") | Focus moves to the field |
| Not found (`UNKNOWN_ACCESSION`, `TILE_OUT_OF_RANGE`) | Message with the valid range, link back to search | — |
| Empty overlay | "No ClinVar missense variant in this tile." / "No measured data for this tile." | — |
| Export error | Toast and inline message "The file could not be created. Your result is still here." | Result unchanged (FR-23) |
| Rate limited (`RATE_LIMITED`) | "Too many requests. Try again in N seconds." using `Retry-After` | Button disabled with countdown |
| Service unavailable (503) | "The service is not ready (model or database unavailable)." with a retry link | `/healthz` polled every 10 s |
| Share link expired (`RUN_EXPIRED`) | "This shared result has expired." | — |

### 3.5 Model card (`/model`)

```
+--------------------------------------------------------------------------------+
|  Model m3-ext4.0-platt-v1   status: frozen (default)   weights 8bec0b04...     |
|  What it predicts: P(DeltaPSI >= 1.0) in the GPS assay (Zhang 2023)            |
|  Domain: 28-mer internal tiles, intrinsic PSI(WT) <= 4.0                        |
|  Evidence: development OOF benchmark - NOT external validation                 |
|  Performance (with 95 % CI by protein cluster; source file shown):              |
|     AUROC 0.8208 [..]   Brier 0.0925 vs 0.1272 raw   Top-10 % enrichment 4.02x  |
|  Known limitations: probabilities about 13 % low on the original domain; ...    |
|  Trained on: Zhang 2023 saturation mutagenesis (176 peptides, 92,337 cells)     |
|  Not used: [list of excluded sources and the reason]                            |
|  Version history: (table)                                                      |
+--------------------------------------------------------------------------------+
```

Numbers are read from `metrics` of the API, never typed into the frontend. The card links the experiment reports of the research repository.

### 3.6 About, data sources and licences (`/about`)

A table from `GET /v1/sources`: name, version, licence, attribution text, disclaimer. Fixed text blocks: what the tool is not (no diagnosis, no disease-causation claim), privacy statement (sequences are not stored unless a share link is requested), how to cite, contact.

## 4. Mandatory warning rules

| ID | Rule |
|---|---|
| W-1 | Domain banner is present on every result view, with the status in words. |
| W-2 | For `unknown`, `measured_unreliable`, `predicted_*`: an amber warning block above the heatmap, not dismissible. |
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
| Domain status | Four fills tested in a deuteranopia/protanopia/tritanopia simulation | Pattern (solid / hatched / dotted / empty) and text |
| Warning levels | Amber (notice), red (override) | Icon and the word "Warning"/"Override" |
| ClinVar classes | Marker shapes per class | Shape and text in hover card |

Text contrast ≥ 4.5 : 1, large text and UI components ≥ 3 : 1 (WCAG 2.1 AA). Light and dark themes both meet these; theme follows the system preference with a manual switch.

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
| `RankTable` | `cells: Cell[]; filter; onFilter; selected?; onSelect` | Sort, filter, virtualised rows |
| `ExportMenu` | `request: PredictRequest; onError(e)` | CSV/JSON download, share link |
| `ProvenanceFooter` | `provenance: Provenance` | Always visible provenance line |
| `RefusalNotice` | `error: ApiError; onOverride(); onBack()` | Out-of-domain flow |
| `ModelCardPage` | — | Reads `/v1/models/{id}` |
| `AboutPage` | — | Reads `/v1/sources` |
| `ErrorBanner` | `error: ApiError` | Maps error codes to messages (§3.4) |

Types are generated from `openapi.yaml` (for example with `openapi-typescript`) so that the frontend cannot drift from the contract.

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

* Heatmap library (Plotly.js vs D3) — decide on a half-day spike against §7 and NFR-03.
* Whether a mock-up in HTML or Figma is wanted for the thesis figures; not part of this design.
* Wording review of the direction note ("weaken the degron signal") with the supervisor before release.
