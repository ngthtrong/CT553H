# Repository Guidelines

## Project Structure & Module Organization

This is a research and thesis-planning repository with multiple candidate topics. Read [CLAUDE.md](CLAUDE.md), [the topic index](docs/topics/README.md), and recent entries in [the work log](docs/common/work-log.md) before changing research direction.

- `docs/topics/<slug>/`: topic-specific ideas, surveys, data reports, and proposals, organized by numbered stages such as `01-idea/` and `04-proposal/`.
- `docs/common/`: shared research, advisor references, resources, and session logs.
- `docs/meeting/`: meeting preparation, minutes, and presentation assets.
- `ml/<slug>/`: Python preprocessing and experiments; experiment directories contain scripts, configuration, and small `results/` files.
- `data/<slug>/{raw,interim,processed}/`: local inputs, caches, and generated datasets, excluded from Git.

Application services and a dedicated test directory do not yet exist. Create new topic directories only when needed, and register topics in `docs/topics/README.md`.

## Build, Test, and Development Commands

Run from the repository root:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r ml/requirements.txt
.venv/bin/python ml/personal-expense-management/preprocessing/clean_data.py
.venv/bin/python ml/personal-expense-management/experiments/rq1-quick-check/run.py
.venv/bin/python ml/personal-expense-management/experiments/rq2-baseline-recall/run.py
.venv/bin/python ml/rtk-atp-applicability/preprocessing/prepare_data.py
```

Expense preprocessing requires local `raw/notion-export.csv` and `raw/anonymize_names.txt`; run it before the experiments, then run RQ1 before RQ2. Embedding experiments may download models. RTK preparation verifies a pinned archive and generates audit reports; use `--archive /path/to/archive.zip` for offline input. There is no unified build command.

## Coding Style & Naming Conventions

Use four-space Python indentation, `snake_case` functions and variables, and uppercase constants. Follow existing `pathlib`-based repository paths. No formatter or linter is configured. Use lowercase English kebab-case for topic slugs and document names; retain Python-style filenames such as `clean_data.py`. Use relative Markdown links and update references when moving files.

## Testing Guidelines

No automated testing framework or coverage threshold is configured. Validate script changes by rerunning the affected pipeline and inspecting generated counts, audit reports, and metrics. Fix random seeds, save experiment configurations, and link reported numbers to result files. Document data prerequisites and known leakage limitations in experiment READMEs.

## Commit & Pull Request Guidelines

History mixes `docs:`/`feat:` prefixes with plain imperative messages. Prefer concise, scoped messages such as `docs: update RTK data report`. PRs should describe the affected topic, rationale, validation commands, and result changes; link related issues when applicable and include screenshots for presentation changes.

## Data & Configuration Safety

Never commit personal datasets, real names, secrets, model weights, or caches. Preserve raw inputs and regenerate processed data through scripts. Share only anonymized expense exports. Keep small, reviewed experiment results in Git and record substantial research changes in the shared work log.
