# Degron mutation effects — English research briefing

Open **[index.html](index.html)** directly in Chrome or Edge. The deck runs offline and contains **34 main slides and 16 appendices**. It introduces the topic, reports available research findings and explains the next steps for a faculty discussion.

[Vietnamese edition](../deck-research-overview-2026-11-02/index.html).

## Controls

| Action | Key / button |
|---|---|
| Previous / next slide | Arrow keys, Space, Page Up/Down, or swipe |
| Overview and slide selection | O / Overview |
| Speaker notes and sources | N / Notes |
| Pause or resume animation | M / Pause motion |
| Fullscreen | F / Fullscreen |
| First slide / discussion | Home / End |

The deck respects reduced-motion settings. GIFs have static posters, and process animations pause when slides are hidden. Browser printing produces a static view. The interactive metric comparison is in the appendix.

## Translation and numerical fidelity

Slide text, diagrams, chart labels, tooltips, interface controls and speaker notes are translated into English. Figures are regenerated from the same research JSON values. No training or held-source T evaluation is performed. The [localization report](localization-validation.json) records numerical-source identities and preservation of the Vietnamese source files.

The HIF1A matrix contains measured labels. The application screenshot shows a design prototype with synthetic data and no backend connection. See [asset notices](asset-notices.md), [design research](design-research.md), [slide-level sources](slide-sources.json), and [evidence.json](evidence.json).

## Rebuild

Run from the repository root, using the same Python plotting dependencies as the Vietnamese edition:

```powershell
python -I -X utf8 presentation/deck-research-overview-2026-11-02-en/localize-and-build.py
```

The localizer copies assets and runtime files from the Vietnamese edition, translates source literals before layout, regenerates figures and injects reviewed English notes. It checks that the original files were not modified. The generated English `prepare-assets.py` and `build-deck.py` can also be run directly after assets have been copied.

`validate-deck.cjs` uses Playwright and Chrome headless; set `PLAYWRIGHT_MODULE` to an available Playwright package if needed. Render and interaction results are stored in [validation.json](validation.json), with slide images in [previews/](previews/). Run `validate-language.py` after rendering to audit displayed copy, chart labels and controls, and to verify exact numerical agreement with the original edition.
