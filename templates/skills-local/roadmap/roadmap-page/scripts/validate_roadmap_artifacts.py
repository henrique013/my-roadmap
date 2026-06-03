#!/usr/bin/env python3
"""Valida artefatos mecânicos do modo roadmap-page."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from check_roadmap_html_shape import collect_failures as collect_html_failures


NODE_SLUG_RE = re.compile(r"^\d{2}-[a-z0-9][a-z0-9-]*$")
HTML_SLUG_RE = re.compile(
    r"<strong>\s*Slug:\s*</strong>\s*<code>(?P<slug>\d{2}-[a-z0-9-]+)</code>",
    re.IGNORECASE | re.DOTALL,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Valida roadmap.html e roadmap-contract.json.")
    parser.add_argument("--roadmap-dir", required=True, help="Diretório do roadmap.")
    return parser.parse_args()


def is_non_empty_file(path: Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


def validate(args: argparse.Namespace) -> list[str]:
    failures: list[str] = []
    roadmap_dir = Path(args.roadmap_dir)
    html_path = roadmap_dir / "roadmap.html"
    contract_path = roadmap_dir / ".roadmap" / "roadmap-contract.json"

    if not roadmap_dir.exists() or not roadmap_dir.is_dir():
        return [f"roadmap dir não existe: {roadmap_dir}"]
    if not is_non_empty_file(html_path):
        failures.append(f"roadmap.html ausente ou vazio: {html_path}")
    if not is_non_empty_file(contract_path):
        failures.append(f"roadmap-contract.json ausente ou vazio: {contract_path}")
        return failures

    html_text = html_path.read_text(encoding="utf-8") if html_path.exists() else ""
    if html_text:
        failures.extend(f"HTML: {failure}" for failure in collect_html_failures(html_text))

    try:
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return failures + [f"roadmap-contract.json inválido: {exc}"]

    if contract.get("schema_version") != "1.0":
        failures.append("schema_version deve ser 1.0")
    if contract.get("roadmap_slug") != roadmap_dir.name:
        failures.append("roadmap_slug não corresponde ao nome da pasta")

    sources = contract.get("sources")
    if not isinstance(sources, list) or not sources:
        failures.append("sources ausente ou vazio")
        source_ids: set[str] = set()
    else:
        source_ids = {source.get("id") for source in sources if isinstance(source, dict)}
        for source in sources:
            if not isinstance(source, dict):
                failures.append("source deve ser objeto")
                continue
            if not source.get("id") or not source.get("url") or not source.get("reason"):
                failures.append(f"source incompleta: {source}")

    anti_repetition = contract.get("anti_repetition")
    if not isinstance(anti_repetition, list) or not anti_repetition:
        failures.append("anti_repetition ausente ou vazio")

    nodes = contract.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        failures.append("nodes ausente ou vazio")
        return failures

    json_slugs: list[str] = []
    for index, node in enumerate(nodes, start=1):
        if not isinstance(node, dict):
            failures.append("node deve ser objeto")
            continue
        slug = str(node.get("slug") or "")
        json_slugs.append(slug)
        if not NODE_SLUG_RE.fullmatch(slug):
            failures.append(f"slug inválido: {slug}")
        if node.get("order") != index:
            failures.append(f"ordem inválida para {slug}: esperado {index}")
        if slug and not slug.startswith(f"{index:02d}-"):
            failures.append(f"slug fora da ordem numérica: {slug}")
        for field in ("label", "role_in_chain", "must_cover", "must_not_cover", "questions"):
            value = node.get(field)
            if value in ("", [], None):
                failures.append(f"node {slug} sem campo obrigatório útil: {field}")
        references = node.get("references")
        if not isinstance(references, list) or not references:
            failures.append(f"node {slug} sem referências")
        else:
            for reference in references:
                if not isinstance(reference, dict):
                    failures.append(f"referência inválida em {slug}")
                    continue
                source_id = reference.get("source_id")
                if source_id and source_ids and source_id not in source_ids:
                    failures.append(f"referência de {slug} aponta para source_id não declarado: {source_id}")

    if len(json_slugs) != len(set(json_slugs)):
        failures.append("slugs duplicados no contrato JSON")

    html_slugs = HTML_SLUG_RE.findall(html_text)
    if html_slugs:
        if html_slugs != json_slugs:
            failures.append("slugs do HTML e do JSON não têm a mesma ordem")
    else:
        failures.append("nenhum slug de node encontrado no HTML")

    visual_audit = roadmap_dir / ".roadmap" / "visual-audit.md"
    if visual_audit.exists():
        text = visual_audit.read_text(encoding="utf-8").lower()
        if "status geral: passa" not in text and "status: passa" not in text:
            failures.append("visual-audit.md existe, mas não registra passagem")

    return failures


def main() -> int:
    failures = validate(parse_args())
    if failures:
        print("falha: artefatos do roadmap inválidos")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("passa: artefatos mecânicos do roadmap válidos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
