# Validation — English Degron Research Report

Completed: 8 November 2026 (UTC+8). Scientific evidence remains dated 7 November.

- Official PPTX: `presentation/Degron_Research_Report.pptx`.
- PDF exported from that PPTX: `presentation/Degron_Research_Report.pdf`.
- 94 slides/pages, 16:9: 57 main, 26 appendix and 11 reference slides.
- PPTX SHA-256: `8a40b78f37c8795afa43c69de7538b4b4bdc254404c0f23d5d5d03873c3502b7`.
- PDF SHA-256: `ee2974e00d863afdd95de89afddde6ff8c77265df2c24a891c2280a297de774a`.

## Checks passed

- 16 CTU structure checks: input hashes, canvas, fonts, Notes, sources, ZIP integrity and PDF page count.
- Text retention and layout: zero missing text, replacement glyphs, out-of-canvas text, text-box collisions or unintended text below 8.9 pt. Math fallback glyphs are checked separately.
- 16 numerical checks against saved source artifacts: all 88 v3 recipe rows with seed support, 23 R6 rows, historical G2/scanning results, summary values, replay chart and the real R1A example.
- Exact English title on the cover and core metadata; exact Vietnamese title in cover Notes and metadata. English prose/language metadata; proper names retained.
- 44 cited source IDs, all present in References; no citation orphans. Access gaps and prior online checks remain recorded in `source-verification.json`.
- Eight editable native charts with embedded data. All chart numeric caches are identical to the preceding Vietnamese deck. Slide order and semantic IDs are unchanged.
- All PDF fonts embedded. K2D and Readex Pro remain primary; DejaVu Sans supplies selected mathematical glyphs.
- `git diff --check`; original CTU and report templates have no source changes.

## Visual review

Viewed all 94 English pages in 12 contact sheets (up to 8 slides per sheet,
940 px per slide). Reviewed English wording, complete cover title, number
formats, formulas/directions, diagram padding, tensors, charts, table columns,
page numbering, branding and References. Expanded cards and shortened copy
where translation affected fit. Selected pages were inspected at 1280×720.
After final copy corrections, pages 11 and 48 were reinspected individually;
the other 92 final preview images are pixel-identical to the reviewed English
render. See `checks/visual-review.json` for current hashes.

Original CTU master/layout and artwork are retained. Visible short citations
below subtitles follow the author's report requirement. Matrix axis labels
9–10 pt are intentional figure detail; sources are 12.5 pt, references 13.5 pt,
content tables 15–19 pt and primary body text 18–24 pt.

## Scope and limitations

The official PPTX remains the editable source. No parallel English deck was
created. The English and Vietnamese project titles are read directly from
thesis/proposal metadata. Thesis and proposal outputs were rebuilt for this
explicitly authorized title synchronization; see
[the project validation record](../../report/title-sync-validation-2026-11-08.md).

PDF export/rendering used LibreOffice; Microsoft PowerPoint Slide Show and
Microsoft Word were not exercised. Artifact checks do not establish scientific
generalization, E3 mechanisms, prospective wet-lab utility or G2/G3 acceptance.
No model training/inference or research bootstrap was run. The proposal retains
its 3 November scientific snapshot; the dated progress validator replays its
preserved prior validation record rather than reading mutable live state.
Other decks and pre-existing overview-deck deletions were left untouched.
No commit or push.
