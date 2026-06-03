#!/usr/bin/env python3
"""Validate the mechanical shape of a roadmap node HTML file."""

from __future__ import annotations

import argparse
import re
from html.parser import HTMLParser
from pathlib import Path


PROHIBITED_SECTIONS = (
    "Objetivo do node",
    "Ao final você vai saber",
    "Pré-requisitos herdados",
    "Critério de domínio",
    "Checklist final",
)

COMMAND_PATTERNS = (
    re.compile(r"(?m)^\s*(?:sudo|apt|dnf|yum|brew|docker|kubectl|psql|npm|pip|python3?)\s+\S+"),
    re.compile(r"(?m)^\s*(?:\$|#)\s+\S+"),
)


class ShapeParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.has_html_pt_br = False
        self.has_meta_charset_utf8 = False
        self.has_viewport = False
        self.has_style = False
        self.has_title = False
        self.has_h1 = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attrs_map = {name.lower(): value for name, value in attrs if name}

        if tag == "html" and (attrs_map.get("lang") or "").lower() == "pt-br":
            self.has_html_pt_br = True
        elif tag == "meta":
            charset = (attrs_map.get("charset") or "").lower()
            name = (attrs_map.get("name") or "").lower()
            if charset == "utf-8":
                self.has_meta_charset_utf8 = True
            if name == "viewport" and attrs_map.get("content"):
                self.has_viewport = True
        elif tag == "style":
            self.has_style = True
        elif tag == "title":
            self.has_title = True
        elif tag == "h1":
            self.has_h1 = True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Valida a forma mecânica mínima de node.html."
    )
    parser.add_argument("--html", required=True, help="Caminho para node.html.")
    return parser.parse_args()


def collect_failures(html_text: str) -> list[str]:
    lower_text = html_text.lower()
    failures: list[str] = []

    if not re.search(r"(?is)^\s*<!doctype\s+html\s*>", html_text):
        failures.append("doctype HTML ausente ou não está no início do arquivo")

    parser = ShapeParser()
    try:
        parser.feed(html_text)
        parser.close()
    except Exception as exc:  # HTMLParser is permissive, but keep the contract explicit.
        failures.append(f"HTML não parseável: {exc}")

    if not parser.has_html_pt_br:
        failures.append('tag <html lang="pt-BR"> ausente')
    if not parser.has_meta_charset_utf8:
        failures.append('<meta charset="utf-8"> ausente')
    if not parser.has_viewport:
        failures.append("meta viewport ausente")
    if not parser.has_style:
        failures.append("<style> ausente")
    if not parser.has_title:
        failures.append("<title> ausente")
    if not parser.has_h1:
        failures.append("<h1> ausente")
    if "<!--" not in html_text or "refer" not in lower_text:
        failures.append("seção de referências comentadas ausente")
    if "```" in html_text:
        failures.append("Markdown cru detectado: fence ```")

    for section in PROHIBITED_SECTIONS:
        if section.lower() in lower_text:
            failures.append(f"seção proibida detectada: {section}")

    for pattern in COMMAND_PATTERNS:
        if pattern.search(html_text):
            failures.append("possível sequência de comandos como corpo operacional")
            break

    return failures


def main() -> int:
    args = parse_args()
    html_path = Path(args.html)

    if not html_path.exists():
        print(f"falha: HTML não encontrado: {html_path}")
        return 1

    html_text = html_path.read_text(encoding="utf-8")
    failures = collect_failures(html_text)

    if failures:
        print("falha: forma mecânica inválida")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("passa: forma mecânica mínima válida")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
