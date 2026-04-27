# Resume

This repository now treats LaTeX as the source of truth for the resume and generates the published HTML from it.

## Layout

- `src/resume.tex`: canonical resume content
- `src/resume.css`: stylesheet for generated HTML
- `index.html`: generated HTML published by GitHub Pages
- `resume.css`: generated copy of the publish stylesheet
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

`index.html` and `resume.css` are generated artifacts and should not be edited by hand.
