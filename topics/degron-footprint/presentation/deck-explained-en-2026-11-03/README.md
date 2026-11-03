# RESIDUE-LEVEL DEGRON MUTATION EFFECT PREDICTION AND ANALYSIS TOOL

Open [index.html](index.html) directly in Chrome or Edge. This English edition contains **31 main slides and 5 appendices**, matching the Vietnamese deck. It includes the same GIF, proteasome video, step-by-step diagrams and interactive metric chart, with English text, labels, controls and speaker notes.

- [Static PDF: 36 pages](slides.pdf)
- [Main-slide overview](previews/contact-main.png)
- [Speaker notes and sources](speaker-notes.md)
- [Vietnamese edition](../deck-explained-2026-11-03/index.html)

All presentation assets are local. No network connection, backend or Node installation is required for playback.

## Controls

| Action | Key / control |
| --- | --- |
| Reveal the next step, then advance | → / Space / Page Down |
| Previous step | ← / Page Up |
| Skip directly between slides | Shift + ← / → |
| Overview / notes and sources | O / N |
| Pause / resume motion | M |
| Fullscreen | F |
| Opening / closing slide | Home / End |

Swipe horizontally on touch devices. Slide 23 switches between MAE, positive-event AUROC and positive-event AP. The video has a separate play/pause button. Reduced-motion preferences use still images, and hidden slides pause their media. The PDF shows all diagram steps and static figures.

## Translation and scientific scope

Slide order, diagrams, data, uncertainty and evidence boundaries follow the Vietnamese source. The learning-roadmap slide remains omitted. Data are presented directly, without a version-by-version narrative. Personal names and immutable model identifiers retain their original spelling.

English labels for five research figures are rendered from the same saved JSON values. Development results remain distinct from independent validation. The UI screenshot uses synthetic fixtures. Hypothetical examples remain labeled, and the incomplete LoRA comparison remains incomplete.

`translation.json` contains the UI/diagram translations; `notes-en.json` contains the 36 English speaker notes. `build-deck.py` localizes the approved Vietnamese HTML and preserves its structure and interactions. It requires the sibling Vietnamese source folder when rebuilding, while the resulting HTML is self-contained within this folder. `reuse-manifest.json` records hashes of every Vietnamese source file before this work.

## Rebuild and validate

From the repository root, using a separate preview environment:

```bash
python3 -m venv /tmp/degron-deck-tools
/tmp/degron-deck-tools/bin/pip install -r topics/degron-footprint/presentation/deck-explained-en-2026-11-03/requirements-preview.txt
/tmp/degron-deck-tools/bin/python -m playwright install chromium
/tmp/degron-deck-tools/bin/python topics/degron-footprint/presentation/deck-explained-en-2026-11-03/prepare-figures.py
python3 -I topics/degron-footprint/presentation/deck-explained-en-2026-11-03/build-deck.py
/tmp/degron-deck-tools/bin/python topics/degron-footprint/presentation/deck-explained-en-2026-11-03/validate-deck.py
```

The validator checks layout, local resources, video playback, step navigation, notes, metric switching, reduced motion, viewport sizes, the 36-page PDF, unchanged source files, numeric parity and translation completeness. See `validation.json` and `VALIDATION.md` for the recorded results. No models are trained or promoted during this workflow.
