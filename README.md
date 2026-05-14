# Resume

This repository treats LaTeX as the source of truth for the resume artifacts.
The GitHub Pages site is the multi-page technical CV, and a one-page ML
platform resume PDF is published beside it for applications.

## Layout

- `src/resume-full.tex`: canonical multi-page technical CV content
- `src/resume-platform.tex`: one-page ML platform resume content
- `src/resume.css`: stylesheet for generated HTML
- `index.html`: generated technical CV HTML published by GitHub Pages
- `resume.css`: generated copy of the publish stylesheet
- `platform-resume.pdf`: generated one-page ML platform resume linked from the CV
- `scripts/build_resume.py`: PDF and HTML build entrypoint
- `scripts/validate_resume_html.py`: structural HTML validation

## Local usage

Requirements:

- `pdflatex`
- `make4ht`
- `python3`
- `pre-commit` if you want commit hooks installed

Commands:

```bash
make pdf
make html
make validate
make clean
```

Install hooks:

```bash
pre-commit install
```

`index.html`, `resume.css`, and `platform-resume.pdf` are generated artifacts
and should not be edited by hand.
