#!/usr/bin/env python3
"""Valida artefatos mecânicos do modo roadmap-page."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from check_roadmap_html_shape import collect_failures as collect_html_failures


NODE_SLUG_RE = re.compile(r"^\d{2}-[a-z0-9][a-z0-9-]*$")
HTML_SLUG_RE = re.compile(
    r"<strong>\s*Slug:\s*</strong>\s*<code>(?P<slug>\d{2}-[a-z0-9-]+)</code>",
    re.IGNORECASE | re.DOTALL,
)
SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schema" / "roadmap-contract.schema.json"


def schema_type_matches(value: Any, expected_type: str) -> bool:
    if expected_type == "object":
        return isinstance(value, dict)
    if expected_type == "array":
        return isinstance(value, list)
    if expected_type == "string":
        return isinstance(value, str)
    if expected_type == "integer":
        return type(value) is int
    if expected_type == "number":
        return type(value) in (int, float)
    if expected_type == "boolean":
        return isinstance(value, bool)
    if expected_type == "null":
        return value is None
    return True


def validate_schema(value: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    failures: list[str] = []

    if "const" in schema and value != schema["const"]:
        failures.append(f"{path} deve ser {schema['const']!r}")
        return failures

    expected_type = schema.get("type")
    if isinstance(expected_type, str) and not schema_type_matches(value, expected_type):
        failures.append(f"{path} deve ser {expected_type}")
        return failures

    if "enum" in schema and value not in schema["enum"]:
        failures.append(f"{path} deve estar em {schema['enum']!r}")

    if isinstance(value, str):
        min_length = schema.get("minLength")
        if isinstance(min_length, int) and len(value) < min_length:
            failures.append(f"{path} deve ter ao menos {min_length} caractere(s)")
        pattern = schema.get("pattern")
        if isinstance(pattern, str) and not re.fullmatch(pattern, value):
            failures.append(f"{path} não corresponde ao padrão {pattern}")

    if isinstance(value, list):
        min_items = schema.get("minItems")
        if isinstance(min_items, int) and len(value) < min_items:
            failures.append(f"{path} deve ter ao menos {min_items} item(ns)")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                failures.extend(validate_schema(item, item_schema, f"{path}[{index}]"))

    if isinstance(value, dict):
        required = schema.get("required", [])
        if isinstance(required, list):
            for field in required:
                if field not in value:
                    failures.append(f"{path}.{field} é obrigatório")
        properties = schema.get("properties", {})
        if isinstance(properties, dict):
            for field, field_schema in properties.items():
                if field in value and isinstance(field_schema, dict):
                    failures.extend(validate_schema(value[field], field_schema, f"{path}.{field}"))

    return failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Valida roadmap.html e roadmap-contract.json.")
    parser.add_argument("--roadmap-dir", required=True, help="Diretório do roadmap.")
    return parser.parse_args()


def is_non_empty_file(path: Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


def file_contains_any(path: Path, needles: tuple[str, ...]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8").lower()
    return any(needle.lower() in text for needle in needles)


def require_audit_pass(path: Path, label: str, failures: list[str]) -> None:
    if not is_non_empty_file(path):
        failures.append(f"{label} ausente ou vazio: {path}")
        return
    if not file_contains_any(path, ("status geral: passa", "status: passa")):
        failures.append(f"{label} não registra status de passagem")


def validate_render_checks(path: Path, failures: list[str]) -> None:
    if not is_non_empty_file(path):
        failures.append(f"render-checks.json ausente ou vazio: {path}")
        return
    try:
        render_checks = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        failures.append(f"render-checks.json inválido: {exc}")
        return
    if render_checks.get("status") != "passa":
        failures.append("render-checks.json não registra status passa")


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

    if not is_non_empty_file(SCHEMA_PATH):
        failures.append(f"schema do roadmap-contract ausente ou vazio: {SCHEMA_PATH}")
    else:
        try:
            schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"schema do roadmap-contract inválido: {exc}")
        else:
            failures.extend(f"schema: {failure}" for failure in validate_schema(contract, schema))

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

    pipeline_dir = roadmap_dir / ".roadmap" / "pipeline"
    expected_audits = (
        ("01-html-shape/html-shape-audit.md", "html-shape-audit.md"),
        ("02-contract-schema/contract-schema-audit.md", "contract-schema-audit.md"),
        ("03-contract-consistency/contract-consistency-audit.md", "contract-consistency-audit.md"),
        ("04-source-coverage/source-audit.md", "source-audit.md"),
        ("05-visual-render/visual-audit.md", "visual-audit.md"),
    )
    for relative_path, label in expected_audits:
        require_audit_pass(pipeline_dir / relative_path, label, failures)

    visual_pipe_dir = pipeline_dir / "05-visual-render"
    validate_render_checks(visual_pipe_dir / "render-checks.json", failures)
    playwright_dir = visual_pipe_dir / "playwright"
    if not playwright_dir.is_dir():
        failures.append(f"playwright do pipe visual ausente: {playwright_dir}")
    else:
        for name in ("desktop.png", "mobile.png"):
            path = playwright_dir / name
            if not is_non_empty_file(path):
                failures.append(f"evidência visual ausente ou vazia: {path}")

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
