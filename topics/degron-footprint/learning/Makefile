PYTHON ?= python3
.PHONY: all assets check previews
all:
	$(PYTHON) scripts/build.py
	$(PYTHON) scripts/validate.py
assets:
	$(PYTHON) scripts/collect_evidence.py
	$(PYTHON) scripts/generate_figures.py
	$(PYTHON) scripts/generate_diagrams.py
check:
	$(PYTHON) scripts/validate.py
previews:
	$(PYTHON) scripts/render_previews.py
