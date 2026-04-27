#!/usr/bin/env python3
from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
HTML_PATH = ROOT / "index.html"


class Validator(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.seen_html = False
        self.seen_head = False
        self.seen_title = False
        self.seen_body = False
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "html":
            self.seen_html = True
        elif tag == "head":
            self.seen_head = True
        elif tag == "title":
            self.seen_title = True
        elif tag == "body":
            self.seen_body = True

        if tag == "a":
            attr_map = dict(attrs)
            href = attr_map.get("href")
            if href:
                self.links.append(href)


def main() -> int:
    html = HTML_PATH.read_text(encoding="utf-8")
    parser = Validator()
    parser.feed(html)
    parser.close()

    failures: list[str] = []
    if "<!DOCTYPE html>" not in html and "<!DOCTYPE HTML>" not in html:
        failures.append("Missing HTML doctype.")
    if not parser.seen_html:
        failures.append("Missing <html> element.")
    if not parser.seen_head:
        failures.append("Missing <head> element.")
    if not parser.seen_title:
        failures.append("Missing <title> element.")
    if not parser.seen_body:
        failures.append("Missing <body> element.")
    if "resume.css" not in html:
        failures.append("Generated HTML is not linked to resume.css.")
    if not any(link.startswith("https://github.com/Chr1sC0de") for link in parser.links):
        failures.append("Expected GitHub profile link is missing.")
    if "Chris Mamon" not in html:
        failures.append("Expected resume owner name is missing.")

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
