# Official Degron research presentation

The presentation and speaker Notes are in **English**. Keep these two official files:

- [Degron_Research_Report.pptx](../Degron_Research_Report.pptx): editable source; save updates to this same path.
- [Degron_Research_Report.pdf](../Degron_Research_Report.pdf): exported from the official PPTX.

Evidence date: **7 November 2026**. There are **94 slides**: 57 main slides,
26 appendix slides (58–83), and 11 reference slides (84–94). The report moves
from biological foundations and the ΔPSI task through prior work, data/QC,
methods, evaluation, available results, limitations and next steps.

## Official project titles

**English:** Sequence-Based Prediction of Single-Residue Mutation Effects on PSI in Degron Assays and Development of an Analysis Tool

**Vietnamese:** Dự đoán ảnh hưởng của đột biến amino acid đơn lên chỉ số PSI trong nghiên cứu degron và xây dựng công cụ phân tích

`manage.py` reads the English title from `report/config/metadata.tex`
(`\ThesisTitle`) and the Vietnamese title from `proposal/proposal.md`
(`subtitle`). The cover uses the English title; cover Notes and PPTX metadata
retain the exact Vietnamese title. Author/supervisor names retain their spelling.
The title synchronization is recorded in
[the project validation record](../../report/title-sync-validation-2026-11-08.md).

## Design and editing

The original CTU 16:9 master, logo and footer artwork are retained. Headings
use K2D and body text uses Readex Pro. Install the bundled Regular/Bold fonts
from `../templateCTU/ctu-slides/assets/fonts/` when editing on another computer.
The original template files are unchanged.

Diagrams, the mutation matrix, tables and eight charts are editable PowerPoint
objects. Charts include embedded data workbooks. Conceptual diagrams are
identified as schematics. Short source IDs appear below subtitles; Notes and
References contain full citations, paths and locators.

Open the official PPTX, edit content/Notes, and keep its filename. For supported
data-backed revisions, edit the relevant content in `manage.py` and specify the
semantic slide IDs. Unselected slides, including manual changes, are preserved.
Do not create parallel `v2`, `final`, `updated`, or HTML decks.

Run from the repository root using the existing Python environment:

```bash
.venv/bin/python presentation/research-report/manage.py list
.venv/bin/python presentation/research-report/manage.py revise --slides lora-results,lora-ci,lora-domain
.venv/bin/python presentation/research-report/manage.py render
.venv/bin/python presentation/research-report/manage.py check
```

Select all affected methods, results, intervals, limitations and references
when changing evidence. Review source-hash failures and update the actual claims.
After export, inspect slide images as well as the automated checks.

`render --soffice /path/to/soffice` selects LibreOffice. This environment can
also use its existing relocatable copy at `/tmp/isds-lo/root`; another computer
needs its own LibreOffice installation. Required Python libraries are
`python-pptx`, `pandas`, `pyarrow`, `numpy`, `Pillow`, `matplotlib` and `PyMuPDF`.

`build` is for initial creation and refuses to overwrite an existing PPTX.
`authoring-plan.json` records generated revisions; it is not authoritative over
manual PPTX edits. `speaker-notes.md` is exported from actual PPTX Notes.
The single CLI reuses the template engine without modifying it.

## Evidence and validation

- [evidence-map.json](evidence-map.json): per-slide sources, locators and input hashes.
- [source-verification.json](source-verification.json): targeted source checks, prior audits and access gaps.
- [checks/validation.json](checks/validation.json): structure, fonts, Notes, sources, hashes and PDF page count.
- [checks/language-validation.json](checks/language-validation.json): English delivery and exact bilingual title metadata.
- [checks/text-layout.json](checks/text-layout.json): text retention, geometry and glyph checks.
- [checks/numerical-evidence.json](checks/numerical-evidence.json): delivered values compared with saved source JSON, including all 88 v3 recipes and 23 R6 rows.
- [checks/english-update.json](checks/english-update.json): translation scope and unchanged chart data.
- [checks/visual-review.json](checks/visual-review.json): current rendered-slide review.
- [checks/scoped-update.json](checks/scoped-update.json): historical selective-revision check, before the English migration.
- [VALIDATION.md](VALIDATION.md): current validation scope and limitations.

The results retain their original populations, runtime, seed/fold support,
endpoints and interval types. OOF/replay evidence is developmental. T contains
W5-D only and shares the source/lab; LoRA-T, independent external/structure
benchmarks and prospective wet-lab/resource benefits remain unmeasured.
This update runs no training, model inference or research bootstrap and makes
no serving-model or G2/G3 decision. Prior large artifact audits are cited from
saved records. Scientific data and other decks are outside this update.
