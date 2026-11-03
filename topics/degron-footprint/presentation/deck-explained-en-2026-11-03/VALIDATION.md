# English-edition validation — 3 November 2026

**PASS:** 31 main slides, 5 appendices and a 36-page static PDF. Full results are recorded in `validation.json`.

## Translation and evidence parity

- Slide text, diagram labels, accessibility labels, controls, chart labels and all 36 speaker notes are in English. Vietnamese personal names retain their original spelling.
- Automated scans found no remaining Vietnamese presentation text outside those names, including the JavaScript controls and regenerated SVG figures.
- Recipe IDs, numeric chart values, research references, slide order and appendix flags match the Vietnamese source.
- Five research figures were regenerated with English labels. Their training-range values, test-stratum values, transfer values, CI and HIF1A measured-cell count match the saved research data.
- Video, GIF, posters, UI screenshot and graphical abstract hashes match the source edition. Every Vietnamese source file remains unchanged according to `reuse-manifest.json`.
- Research-source, asset and localization hashes match `evidence.json`. No training, locked-T evaluation, campaign operation or serving-model change was performed.

## Browser behavior and layout

- All 36 slides rendered offline without JavaScript errors, unresolved local links, broken images or failed resource loads.
- Step navigation, direct slide skipping, the 36-item overview, notes and MAE/AUROC/AP switching passed.
- The proteasome movie decoded at 1820×1080 and advanced during actual playback. Its duration is 12.32 seconds. Motion pause and reduced-motion still-image fallback passed.
- A video range request canceled by Chromium during navigation is recorded separately; successful decoding and playback distinguish it from a resource failure.
- No detected text/image overflow after shortening the substitution-count label and fitting the synonymous-WT caption.
- Viewport checks passed at 1280×720, 1920×1080, 390×844 and 844×390. Mobile playback retains the slide's 16:9 aspect ratio.

## PDF and visual inspection

- Exactly 36 pages, all 16:9, with no blank pages. The shortest page contains 205 extractable characters.
- All fonts are embedded and have Unicode mappings, as checked by `pdffonts`.
- Print output shows all reveal steps, replaces media with still images and uses a static MAE figure instead of the interactive canvas.
- Contact sheets of all main slides and appendices were inspected. PDF pages 5, 20, 22, 23, 30, 33, 34 and 36 were also rasterized and visually reviewed for translated labels, chart readability, formula layout, the heatmap and source captions.
- `git diff --check` and whitespace checks on all new text files passed. The pre-existing Vietnamese edition was preserved; no commit was created.

See `previews/`, `figure-data.json`, `slide-sources.json`, `speaker-notes.md` and `asset-notices.md` for the rendered artifacts and supporting records.

## Thesis-title update

The opening slide, browser/PDF title, overview entry and speaker-note heading now use “Residue-Level Degron Mutation Effect Prediction and Analysis Tool”, matching the thesis title in `report/config/metadata.tex`. The Vietnamese source received the corresponding authorized title update. The previous source-hash manifest is retained as `reuse-manifest-before-title-update.json`; `reuse-manifest.json` records the refreshed Vietnamese source after that update. Both editions were rebuilt and validated, with the remaining slides, scientific values and assets checked against their pre-update snapshots.
