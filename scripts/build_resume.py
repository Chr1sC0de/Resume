#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "src"
BUILD_DIR = ROOT / "build"
PDF_DIR = BUILD_DIR / "pdf"
HTML_DIR = BUILD_DIR / "html"
TEXMF_DIR = BUILD_DIR / ".texmf-var"
SOURCE_TEX = SRC_DIR / "resume.tex"
SOURCE_CSS = SRC_DIR / "resume.css"
OUTPUT_HTML = ROOT / "index.html"
OUTPUT_CSS = ROOT / "resume.css"


def run(cmd: list[str], cwd: Path | None = None) -> None:
    TEXMF_DIR.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["TEXMFVAR"] = str(TEXMF_DIR)
    result = subprocess.run(cmd, cwd=cwd or ROOT, env=env, text=True)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def ensure_commands(*commands: str) -> None:
    missing = [command for command in commands if shutil.which(command) is None]
    if missing:
        missing_list = ", ".join(missing)
        raise SystemExit(f"Missing required command(s): {missing_list}")


def build_pdf() -> None:
    ensure_commands("pdflatex")
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    command = [
        "pdflatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        f"-output-directory={PDF_DIR}",
        str(SOURCE_TEX),
    ]
    run(command)
    run(command)


def normalize_html(raw_html: str) -> str:
    normalized = raw_html.replace("<!-- l. ", "<!-- line ")
    normalized = normalized.replace(
        "<title></title>", "<title>Chris Mamon Resume</title>"
    )
    if '<meta name="viewport"' not in normalized:
        normalized = normalized.replace(
            "<head>",
            '<head>\n<meta name="viewport" content="width=device-width, initial-scale=1.0" />',
            1,
        )
    return normalized


def build_html() -> None:
    ensure_commands("make4ht")
    if HTML_DIR.exists():
        shutil.rmtree(HTML_DIR)
    HTML_DIR.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(dir=BUILD_DIR) as tmp_dir:
        tmp_path = Path(tmp_dir)
        staged_source = tmp_path / SOURCE_TEX.name
        staged_source.write_text(SOURCE_TEX.read_text(encoding="utf-8"), encoding="utf-8")
        run(
            [
                "make4ht",
                "-u",
                "-f",
                "html5",
                "-d",
                str(HTML_DIR),
                staged_source.name,
            ],
            cwd=tmp_path,
        )

    generated_html = HTML_DIR / "resume.html"
    if not generated_html.exists():
        raise SystemExit(f"Expected generated HTML at {generated_html}")

    OUTPUT_CSS.write_text(SOURCE_CSS.read_text(encoding="utf-8"), encoding="utf-8")
    normalized = normalize_html(generated_html.read_text(encoding="utf-8"))
    OUTPUT_HTML.write_text(normalized, encoding="utf-8")


def clean() -> None:
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "target",
        choices=["pdf", "html", "all", "clean"],
        help="Build target",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.target == "clean":
        clean()
        return 0
    if args.target in {"pdf", "all"}:
        build_pdf()
    if args.target in {"html", "all"}:
        build_html()
    return 0


if __name__ == "__main__":
    sys.exit(main())
