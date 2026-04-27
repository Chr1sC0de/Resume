PYTHON ?= python3

.PHONY: pdf html all validate clean

pdf:
	$(PYTHON) scripts/build_resume.py pdf

html:
	$(PYTHON) scripts/build_resume.py html

all:
	$(PYTHON) scripts/build_resume.py all

validate: html
	$(PYTHON) scripts/validate_resume_html.py

clean:
	$(PYTHON) scripts/build_resume.py clean
