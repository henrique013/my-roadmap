#!/usr/bin/env python3
"""Valida artefatos mecânicos do modo roadmap-page."""

from __future__ import annotations

import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from check_roadmap_html_shape import collect_failures as collect_html_failures


LEVELS = ("basico", "intermediario", "avancado")
LEVEL_LABELS = {
    "basico": "Básico",
    "intermediario": "Intermediário",
    "avancado": "Avançado",
}
NODE_SLUG_RE = re.compile(r"^\d{2}-[a-z0-9][a-z0-9-]*$")
NODE_ID_RE = re.compile(r"^(basico|intermediario|avancado)/\d{2}-[a-z0-9][a-z0-9-]*$")
SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schema" / "roadmap-contract.schema.json"


class RoadmapHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.level_sections: set[str] = set()
        self.node_ids: list[str] = []
        self.node_attrs: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag not in {"section", "article", "div"}:
            return
        attrs_map = {name.lower(): value or "" for name, value in attrs if name}
        level = attrs_map.get("data-level")
        node_id = attrs_map.get("data-node-id")
        if node_id:
            self.node_ids.append(node_id)
            self.node_attrs.append(
                {
                    "node_id": node_id,
                    "level": level or "",
                    "slug": attrs_map.get("data-node-slug", ""),
                }
            )
        elif level in LEVELS:
            self.level_sections.add(level)


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


def resolve_ref(root_schema: dict[str, Any], ref: str) -> dict[str, Any] | None:
    if not ref.startswith("#/"):
        return None
    current: Any = root_schema
    for part in ref[2:].split("/"):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current if isinstance(current, dict) else None


def validate_schema(
    value: Any,
    schema: dict[str, Any],
    path: str = "$",
    root_schema: dict[str, Any] | None = None,
) -> list[str]:
    root = root_schema or schema
    failures: list[str] = []

    ref = schema.get("$ref")
    if isinstance(ref, str):
        resolved = resolve_ref(root, ref)
        if resolved is None:
            return [f"{path} usa $ref não resolvido: {ref}"]
        return validate_schema(value, resolved, path, root)

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
        max_items = schema.get("maxItems")
        if isinstance(max_items, int) and len(value) > max_items:
            failures.append(f"{path} deve ter no máximo {max_items} item(ns)")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                failures.extend(validate_schema(item, item_schema, f"{path}[{index}]", root))

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
                    failures.extend(validate_schema(value[field], field_schema, f"{path}.{field}", root))

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


def parse_html_contract(html_text: str) -> RoadmapHTMLParser:
    parser = RoadmapHTMLParser()
    parser.feed(html_text)
    parser.close()
    return parser


def level_entries(contract: dict[str, Any]) -> list[dict[str, Any]]:
    levels = contract.get("levels")
    return levels if isinstance(levels, list) else []


def flatten_nodes(contract: dict[str, Any]) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    levels_by_name = {
        level.get("level"): level
        for level in level_entries(contract)
        if isinstance(level, dict)
    }
    for level_name in LEVELS:
        level = levels_by_name.get(level_name)
        if not isinstance(level, dict):
            continue
        level_nodes = level.get("nodes")
        if isinstance(level_nodes, list):
            nodes.extend(node for node in level_nodes if isinstance(node, dict))
    return nodes


def node_id_from(level: str, slug: str) -> str:
    return f"{level}/{slug}"


def validate_levels_and_nodes(contract: dict[str, Any], source_ids: set[str]) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    levels = level_entries(contract)
    if not levels:
        return ["levels ausente ou vazio"], []

    seen_levels: set[str] = set()
    seen_node_ids: set[str] = set()
    ordered_node_ids: list[str] = []

    for level in levels:
        if not isinstance(level, dict):
            failures.append("level deve ser objeto")
            continue
        level_name = str(level.get("level") or "")
        if level_name not in LEVELS:
            failures.append(f"level inválido: {level_name}")
            continue
        if level_name in seen_levels:
            failures.append(f"level duplicado: {level_name}")
        seen_levels.add(level_name)

        nodes = level.get("nodes")
        if not isinstance(nodes, list) or not nodes:
            failures.append(f"level {level_name} sem nodes")
            continue
        if len(nodes) > 20:
            failures.append(f"level {level_name} tem {len(nodes)} nodes; máximo permitido é 20")

        seen_slugs: set[str] = set()
        for index, node in enumerate(nodes, start=1):
            if not isinstance(node, dict):
                failures.append(f"node em {level_name} deve ser objeto")
                continue
            slug = str(node.get("slug") or "")
            node_level = str(node.get("level") or "")
            node_id = str(node.get("node_id") or "")
            ordered_node_ids.append(node_id)

            if node_level != level_name:
                failures.append(f"node {node_id or slug} tem level {node_level!r}, esperado {level_name!r}")
            if not NODE_SLUG_RE.fullmatch(slug):
                failures.append(f"slug inválido em {level_name}: {slug}")
            if slug in seen_slugs:
                failures.append(f"slug duplicado em {level_name}: {slug}")
            seen_slugs.add(slug)
            if node_id != node_id_from(level_name, slug):
                failures.append(f"node_id inválido para {level_name}/{slug}: {node_id}")
            if not NODE_ID_RE.fullmatch(node_id):
                failures.append(f"node_id fora do formato esperado: {node_id}")
            if node_id in seen_node_ids:
                failures.append(f"node_id duplicado: {node_id}")
            seen_node_ids.add(node_id)
            if node.get("order") != index:
                failures.append(f"ordem inválida para {node_id}: esperado {index}")
            if slug and not slug.startswith(f"{index:02d}-"):
                failures.append(f"slug fora da ordem numérica local: {node_id}")

            for field in ("label", "role_in_chain", "must_cover", "must_not_cover", "questions"):
                value = node.get(field)
                if value in ("", [], None):
                    failures.append(f"node {node_id} sem campo obrigatório útil: {field}")

            references = node.get("references")
            if not isinstance(references, list) or not references:
                failures.append(f"node {node_id} sem referências")
            else:
                for reference in references:
                    if not isinstance(reference, dict):
                        failures.append(f"referência inválida em {node_id}")
                        continue
                    source_id = reference.get("source_id")
                    if source_id and source_ids and source_id not in source_ids:
                        failures.append(f"referência de {node_id} aponta para source_id não declarado: {source_id}")

    missing_levels = set(LEVELS) - seen_levels
    extra_levels = seen_levels - set(LEVELS)
    if missing_levels:
        failures.append(f"levels ausentes: {', '.join(sorted(missing_levels))}")
    if extra_levels:
        failures.append(f"levels não permitidos: {', '.join(sorted(extra_levels))}")

    return failures, ordered_node_ids


def validate_level_aware_references(contract: dict[str, Any], node_ids: set[str]) -> list[str]:
    failures: list[str] = []

    sources = contract.get("sources")
    if isinstance(sources, list):
        for source in sources:
            if not isinstance(source, dict):
                continue
            source_id = source.get("id", "<sem id>")
            supports_nodes = source.get("supports_nodes", [])
            if supports_nodes in ("", None):
                continue
            if not isinstance(supports_nodes, list):
                failures.append(f"source {source_id} tem supports_nodes não-lista")
                continue
            for node_id in supports_nodes:
                if node_id not in node_ids:
                    failures.append(f"source {source_id} aponta para node_id inexistente: {node_id}")

    anti_repetition = contract.get("anti_repetition")
    if not isinstance(anti_repetition, list) or not anti_repetition:
        failures.append("anti_repetition ausente ou vazio")
        return failures

    for entry in anti_repetition:
        if not isinstance(entry, dict):
            failures.append("anti_repetition deve conter objetos")
            continue
        concept = entry.get("concept", "<sem conceito>")
        first_node = entry.get("first_introduction_node")
        if first_node not in node_ids:
            failures.append(f"anti_repetition {concept!r} aponta primeira introdução inexistente: {first_node}")
        for field in ("allowed_reuses", "blocked_reuses"):
            values = entry.get(field, [])
            if not isinstance(values, list):
                failures.append(f"anti_repetition {concept!r}.{field} deve ser lista")
                continue
            for value in values:
                if not isinstance(value, dict):
                    failures.append(f"anti_repetition {concept!r}.{field} deve usar objetos com node_id")
                    continue
                node_id = value.get("node_id")
                if node_id not in node_ids:
                    failures.append(f"anti_repetition {concept!r}.{field} aponta node_id inexistente: {node_id}")

    return failures


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
    html_contract = parse_html_contract(html_text) if html_text else RoadmapHTMLParser()
    if html_text:
        failures.extend(f"HTML: {failure}" for failure in collect_html_failures(html_text))

    try:
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return failures + [f"roadmap-contract.json inválido: {exc}"]

    if not isinstance(contract, dict):
        return failures + ["roadmap-contract.json deve ser objeto"]

    if not is_non_empty_file(SCHEMA_PATH):
        failures.append(f"schema do roadmap-contract ausente ou vazio: {SCHEMA_PATH}")
    else:
        try:
            schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"schema do roadmap-contract inválido: {exc}")
        else:
            failures.extend(f"schema: {failure}" for failure in validate_schema(contract, schema))

    if contract.get("schema_version") != "2.0":
        failures.append("schema_version deve ser 2.0")
    if contract.get("roadmap_slug") != roadmap_dir.name:
        failures.append("roadmap_slug não corresponde ao nome da pasta")

    sources = contract.get("sources")
    if not isinstance(sources, list) or not sources:
        failures.append("sources ausente ou vazio")
        source_ids: set[str] = set()
    else:
        source_ids = set()
        for source in sources:
            if not isinstance(source, dict):
                failures.append("source deve ser objeto")
                continue
            source_id = source.get("id")
            if isinstance(source_id, str):
                if source_id in source_ids:
                    failures.append(f"source_id duplicado: {source_id}")
                source_ids.add(source_id)
            if not source.get("id") or not source.get("url") or not source.get("reason"):
                failures.append(f"source incompleta: {source}")

    node_failures, ordered_node_ids = validate_levels_and_nodes(contract, source_ids)
    failures.extend(node_failures)
    node_ids = set(ordered_node_ids)
    failures.extend(validate_level_aware_references(contract, node_ids))

    if html_text:
        if set(html_contract.level_sections) != set(LEVELS):
            missing = set(LEVELS) - html_contract.level_sections
            if missing:
                failures.append(f"HTML sem seção data-level para: {', '.join(sorted(missing))}")
        if html_contract.node_ids:
            if html_contract.node_ids != ordered_node_ids:
                failures.append("node_id do HTML e do JSON não têm a mesma ordem tri-level")
            for attrs in html_contract.node_attrs:
                node_id = attrs["node_id"]
                level = attrs["level"]
                if node_id in node_ids and "/" in node_id and level and level != node_id.split("/", 1)[0]:
                    failures.append(f"HTML tem data-level incompatível com data-node-id: {node_id}")
        else:
            failures.append("nenhum data-node-id de node encontrado no HTML")

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
