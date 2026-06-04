#!/usr/bin/env python3
"""Extrai contrato JSON tri-level de roadmap.html para bootstrap mecânico."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path


COMMON_SCRIPTS = Path(__file__).resolve().parents[2] / "common" / "scripts"
sys.path.insert(0, str(COMMON_SCRIPTS))

from normalize_slug import normalize_slug  # noqa: E402


LEVELS = ("basico", "intermediario", "avancado")
LEVEL_LABELS = {
    "basico": "Básico",
    "intermediario": "Intermediário",
    "avancado": "Avançado",
}
LEVEL_SEMANTICS = {
    "basico": "fundamentos, vocabulário indispensável e modelos mentais",
    "intermediario": "arquitetura, relações, decisões e trade-offs",
    "avancado": "limites, casos de borda, falhas, comportamento avançado e critérios de especialista",
}

NODE_ID_RE = re.compile(r"(basico|intermediario|avancado)/\d{2}-[a-z0-9][a-z0-9-]*")
NODE_SECTION_RE = re.compile(
    r"<(?P<tag>section|article)\b(?P<attrs>[^>]*)\bdata-node-id=\"(?P<node_id>[^\"]+)\"[^>]*>"
    r"(?P<body>.*?)(?=</(?P=tag)>)",
    re.IGNORECASE | re.DOTALL,
)
H2_RE = re.compile(r"<h2[^>]*>(?P<text>.*?)</h2>", re.IGNORECASE | re.DOTALL)
H1_RE = re.compile(r"<h1[^>]*>(?P<text>.*?)</h1>", re.IGNORECASE | re.DOTALL)
LINK_RE = re.compile(r'<a\b[^>]*href="(?P<url>[^"]+)"[^>]*>(?P<label>.*?)</a>', re.IGNORECASE | re.DOTALL)
H3_BLOCK_RE = re.compile(
    r"<h3[^>]*>(?P<title>.*?)</h3>(?P<body>.*?)(?=<h3\b|<h2\b|</section>|</article>|$)",
    re.IGNORECASE | re.DOTALL,
)
LI_RE = re.compile(r"<li[^>]*>(?P<text>.*?)</li>", re.IGNORECASE | re.DOTALL)
ROW_RE = re.compile(r"<tr[^>]*>(?P<row>.*?)</tr>", re.IGNORECASE | re.DOTALL)
CELL_RE = re.compile(r"<t[dh][^>]*>(?P<cell>.*?)</t[dh]>", re.IGNORECASE | re.DOTALL)


def strip_tags(value: str) -> str:
    without_tags = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(without_tags)).strip()


def list_after_heading(block: str, heading_keywords: tuple[str, ...]) -> list[str]:
    for match in H3_BLOCK_RE.finditer(block):
        title = strip_tags(match.group("title")).lower()
        if any(keyword in title for keyword in heading_keywords):
            items = [strip_tags(item.group("text")) for item in LI_RE.finditer(match.group("body"))]
            if items:
                return items
            text = strip_tags(match.group("body"))
            return [text] if text else []
    return []


def paragraph_after_heading(block: str, heading_keywords: tuple[str, ...]) -> str:
    values = list_after_heading(block, heading_keywords)
    return " ".join(values)


def node_ids_from_text(value: str) -> list[str]:
    return [match.group(0) for match in NODE_ID_RE.finditer(value)]


def extract_sources(html_text: str) -> tuple[list[dict[str, object]], dict[str, str]]:
    seen: dict[str, str] = {}
    sources: list[dict[str, object]] = []
    for link in LINK_RE.finditer(html_text):
        url = html.unescape(link.group("url"))
        if not url or url == "#" or url in seen:
            continue
        source_id = f"F{len(sources) + 1}"
        seen[url] = source_id
        sources.append(
            {
                "id": source_id,
                "url": url,
                "type": "fonte extraída do HTML",
                "reason": strip_tags(link.group("label")) or "Referência do roadmap",
                "supports_nodes": [],
                "limits": "Contrato extraído mecanicamente; revise antes de liberar node-pages.",
            }
        )
    return sources, seen


def reuse_entries(cell_text: str, field: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for node_id in node_ids_from_text(cell_text):
        key = "reuse" if field == "allowed_reuses" else "reason"
        entries.append({"node_id": node_id, key: cell_text, "reason": cell_text})
    return entries


def extract_anti_repetition(html_text: str) -> list[dict[str, object]]:
    matrix_match = re.search(
        r"<h2[^>]*>[^<]*(Matriz Anti-Repeti(?:ç|c)[aã]o)[^<]*</h2>(?P<body>.*?)(?=<h2\b)",
        html_text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not matrix_match:
        return []

    entries: list[dict[str, object]] = []
    for row in ROW_RE.finditer(matrix_match.group("body")):
        cells = [strip_tags(cell.group("cell")) for cell in CELL_RE.finditer(row.group("row"))]
        if len(cells) < 3 or cells[0].lower() == "conceito":
            continue
        first_ids = node_ids_from_text(cells[1])
        entries.append(
            {
                "concept": cells[0],
                "first_introduction_node": first_ids[0] if first_ids else cells[1],
                "allowed_reuses": reuse_entries(cells[2], "allowed_reuses"),
                "blocked_reuses": reuse_entries(cells[3], "blocked_reuses") if len(cells) > 3 else [],
                "boundary_reason": cells[4] if len(cells) > 4 else "",
            }
        )
    return entries


def node_blocks(html_text: str) -> list[tuple[str, str]]:
    return [(match.group("node_id"), match.group("body")) for match in NODE_SECTION_RE.finditer(html_text)]


def extract_nodes_by_level(html_text: str, source_ids_by_url: dict[str, str]) -> dict[str, list[dict[str, object]]]:
    nodes_by_level: dict[str, list[dict[str, object]]] = {level: [] for level in LEVELS}
    for node_id, block in node_blocks(html_text):
        if "/" not in node_id:
            continue
        level, slug = node_id.split("/", 1)
        if level not in LEVELS:
            continue
        heading = H2_RE.search(block)
        label = strip_tags(heading.group("text")) if heading else slug
        label = re.sub(r"^\s*Node\s+\d{2}\s*-\s*", "", label, flags=re.IGNORECASE).strip()
        if not slug:
            slug = normalize_slug(label, "node")
        order_match = re.match(r"^(\d{2})-", slug)
        order = int(order_match.group(1)) if order_match else len(nodes_by_level[level]) + 1

        references = []
        for link in LINK_RE.finditer(block):
            url = html.unescape(link.group("url"))
            source_id = source_ids_by_url.get(url)
            if source_id:
                references.append(
                    {
                        "source_id": source_id,
                        "url": url,
                        "reason": strip_tags(link.group("label")) or "Referência específica",
                    }
                )
        nodes_by_level[level].append(
            {
                "node_id": node_id,
                "level": level,
                "order": order,
                "slug": slug,
                "label": label,
                "role_in_chain": paragraph_after_heading(block, ("papel", "corrente")),
                "inherited_prerequisites": list_after_heading(block, ("pré-requisitos", "pre-requisitos")),
                "first_introduces": list_after_heading(block, ("introduz",)),
                "must_cover": list_after_heading(block, ("deve cobrir", "cobrir")),
                "must_not_cover": list_after_heading(block, ("não deve cobrir", "nao deve cobrir")),
                "questions": list_after_heading(block, ("perguntas",)),
                "conceptual_vocabulary": list_after_heading(block, ("vocabulário", "vocabulario")),
                "allowed_examples_or_diagrams": list_after_heading(block, ("exemplos", "diagramas")),
                "pitfalls": list_after_heading(block, ("armadilhas", "erros comuns")),
                "mastery_criterion": paragraph_after_heading(block, ("critério", "criterio")),
                "handoff_to_next": paragraph_after_heading(block, ("handoff",)),
                "references": references,
            }
        )
    return nodes_by_level


def build_contract(html_path: Path) -> dict[str, object]:
    html_text = html_path.read_text(encoding="utf-8")
    h1_match = H1_RE.search(html_text)
    title = strip_tags(h1_match.group("text")) if h1_match else html_path.parent.name
    theme = re.sub(r"^\s*Roadmap\s*-\s*", "", title, flags=re.IGNORECASE).strip()
    sources, source_ids_by_url = extract_sources(html_text)
    nodes_by_level = extract_nodes_by_level(html_text, source_ids_by_url)
    return {
        "schema_version": "2.0",
        "roadmap_slug": html_path.parent.name,
        "theme": theme,
        "background": "",
        "research_date": "",
        "assumptions": [],
        "limits": ["Contrato extraído mecanicamente de roadmap.html; revise antes de liberar node-pages."],
        "expected_understanding": "",
        "sources": sources,
        "anti_repetition": extract_anti_repetition(html_text),
        "levels": [
            {
                "level": level,
                "label": LEVEL_LABELS[level],
                "semantics": LEVEL_SEMANTICS[level],
                "nodes": nodes_by_level[level],
            }
            for level in LEVELS
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extrai roadmap-contract.json tri-level de roadmap.html.")
    parser.add_argument("--html", required=True, help="Caminho para roadmap.html.")
    parser.add_argument("--out", required=True, help="Caminho de saída para roadmap-contract.json.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    html_path = Path(args.html)
    out_path = Path(args.out)
    if not html_path.exists():
        print(f"falha: HTML não encontrado: {html_path}")
        return 1
    contract = build_contract(html_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"passa: contrato tri-level extraído em {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
