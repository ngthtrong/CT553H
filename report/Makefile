PYTHON ?= python3
BIBLIOGRAPHY ?= auto
TARGETS := content smoke
.PHONY: all $(TARGETS) content-twoside check doctor clean
all: content content-twoside
$(TARGETS):
	$(PYTHON) scripts/build.py $@ --bibliography $(BIBLIOGRAPHY)
content-twoside:
	$(PYTHON) scripts/build.py content --twoside --bibliography $(BIBLIOGRAPHY)
check:
	$(PYTHON) scripts/check_template.py
doctor:
	$(PYTHON) scripts/doctor.py
clean:
	$(PYTHON) -c 'import shutil; shutil.rmtree("build", ignore_errors=True)'
