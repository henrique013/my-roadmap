#!/usr/bin/env python3
"""Valida a forma mecânica mínima de roadmap.html."""

from __future__ import annotations

import argparse
import re
from html.parser import HTMLParser
from pathlib import Path


PROHIBITED_TERMS = (
    "laboratório",
    "laboratorio",
    "exercício",
    "exercicio",
    "hands-on",
    "desafio prático",
    "desafio pratico",
    "projeto final",
)
REQUIRED_TEXT_GROUPS = (
    ("visão geral", "visao geral"),
    ("mapa tri-level", "mapa dos níveis", "mapa dos niveis"),
    ("básico", "basico"),
    ("intermediário", "intermediario"),
    ("avançado", "avancado"),
    ("matriz anti-repetição", "matriz anti-repeticao"),
    ("checklist final",),
    ("referências consolidadas", "referencias consolidadas"),
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
        self.level_sections: set[str] = set()
        self.node_ids: list[str] = []
        self.node_sections: list[dict[str, str]] = []
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attrs_map = {name.lower(): value for name, value in attrs if name}
        if tag == "html" and (attrs_map.get("lang") or "").lower() == "pt-br":
            self.has_html_pt_br = True
        elif tag == "meta":
            if (attrs_map.get("charset") or "").lower() == "utf-8":
                self.has_meta_charset_utf8 = True
            if (attrs_map.get("name") or "").lower() == "viewport" and attrs_map.get("content"):
                self.has_viewport = True
        elif tag == "style":
            self.has_style = True
        elif tag == "title":
            self.has_title = True
        elif tag == "h1":
            self.has_h1 = True
        elif tag == "a":
            href = attrs_map.get("href")
            if href:
                self.hrefs.append(href)
        if tag in {"section", "article", "div"}:
            level = (attrs_map.get("data-level") or "").lower()
            node_id = attrs_map.get("data-node-id")
            if level in {"basico", "intermediario", "avancado"} and not node_id:
                self.level_sections.add(level)
            if node_id:
                self.node_ids.append(node_id)
                self.node_sections.append(
                    {
                        "id": attrs_map.get("id") or "",
                        "level": level,
                        "node_id": node_id,
                        "slug": attrs_map.get("data-node-slug") or "",
                    }
                )


def strip_tags(html_fragment: str) -> str:
    return re.sub(r"(?is)<[^>]+>", " ", html_fragment)


def numeric_only_flow_step_failures(html_text: str) -> list[str]:
    failures: list[str] = []
    flow_re = re.compile(
        r'(?is)<(?P<tag>div|section|nav)\b(?P<attrs>[^>]*)class="[^"]*\bflow-steps\b[^"]*"[^>]*>(?P<body>.*?)</(?P=tag)>'
    )
    for match in flow_re.finditer(html_text):
        text = strip_tags(match.group("body"))
        tokens = re.findall(r"\S+", text)
        if tokens and all(re.fullmatch(r"\d{1,2}", token) for token in tokens):
            failures.append("flow-steps numérico-only detectado na lista de nodes")
    return failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Valida a forma mínima de roadmap.html.")
    parser.add_argument("--html", required=True, help="Caminho para roadmap.html.")
    return parser.parse_args()


def collect_failures(html_text: str) -> list[str]:
    failures: list[str] = []
    lower_text = html_text.lower()

    if not re.search(r"(?is)^\s*<!doctype\s+html\s*>", html_text):
        failures.append("doctype HTML ausente ou não está no início do arquivo")

    parser = ShapeParser()
    try:
        parser.feed(html_text)
        parser.close()
    except Exception as exc:
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
    if "```" in html_text:
        failures.append("Markdown cru detectado: fence ```")
    missing_levels = {"basico", "intermediario", "avancado"} - parser.level_sections
    if missing_levels:
        failures.append(f"seções data-level ausentes: {', '.join(sorted(missing_levels))}")
    if not parser.node_ids:
        failures.append("nenhum data-node-id de node detectado")
    for node in parser.node_sections:
        node_id = node["node_id"]
        level = node["level"] or (node_id.split("/", 1)[0] if "/" in node_id else "")
        slug = node["slug"] or (node_id.split("/", 1)[1] if "/" in node_id else "")
        expected_id = f"{level}-{slug}" if level and slug else ""
        if not expected_id or node["id"] != expected_id:
            failures.append(f"seção de node sem id estável esperado: {node_id}")
        if expected_id and f"#{expected_id}" not in parser.hrefs:
            failures.append(f"lista resumida sem link interno para node: {node_id}")

    failures.extend(numeric_only_flow_step_failures(html_text))

    for term in PROHIBITED_TERMS:
        if term in lower_text:
            failures.append(f"termo prático proibido detectado: {term}")

    for group in REQUIRED_TEXT_GROUPS:
        if not any(term in lower_text for term in group):
            failures.append(f"seção obrigatória não detectada: {'/'.join(group)}")
    return sorted(set(failures))


def main() -> int:
    args = parse_args()
    html_path = Path(args.html)
    if not html_path.exists():
        print(f"falha: HTML não encontrado: {html_path}")
        return 1
    failures = collect_failures(html_path.read_text(encoding="utf-8"))
    if failures:
        print("falha: forma mecânica de roadmap inválida")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("passa: forma mecânica de roadmap válida")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
