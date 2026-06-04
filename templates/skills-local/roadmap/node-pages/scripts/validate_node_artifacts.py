#!/usr/bin/env python3
"""Validate required mechanical artifacts for a tri-level roadmap node."""

from __future__ import annotations

import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from check_html_shape import collect_failures as collect_html_shape_failures
from extract_visible_text import extract_visible_text, render_markdown


LEVELS = ("basico", "intermediario", "avancado")
NODE_SLUG_RE = re.compile(r"^\d{2}-[a-z0-9][a-z0-9-]*$")


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        attrs_map = {name.lower(): value or "" for name, value in attrs if name}
        href = attrs_map.get("href")
        if href:
            self.hrefs.append(href)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Valida a estrutura mecânica obrigatória de um node tri-level."
    )
    parser.add_argument(
        "--roadmap-dir",
        required=True,
        help="Diretório do roadmap que contém roadmap.html.",
    )
    parser.add_argument(
        "--level",
        help="Nível do node: basico, intermediario ou avancado. Pode ser inferido se o node for único.",
    )
    parser.add_argument("--node", required=True, help="Slug do node no formato NN-slug ou node_id level/NN-slug.")
    return parser.parse_args()


def is_non_empty_file(path: Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


def load_contract(roadmap_dir: Path) -> tuple[dict[str, Any] | None, list[str]]:
    contract_path = roadmap_dir / ".roadmap" / "roadmap-contract.json"
    if not is_non_empty_file(contract_path):
        return None, [f"roadmap-contract.json ausente ou vazio: {contract_path}"]
    try:
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, [f"roadmap-contract.json inválido: {exc}"]
    if not isinstance(contract, dict):
        return None, ["roadmap-contract.json deve ser objeto"]
    failures: list[str] = []
    if contract.get("schema_version") != "2.0":
        failures.append("roadmap-contract.json deve usar schema_version 2.0")
    if contract.get("roadmap_slug") != roadmap_dir.name:
        failures.append("roadmap-contract.json não corresponde ao diretório do roadmap")
    return contract, failures


def nodes_by_level(contract: dict[str, Any] | None) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {level: [] for level in LEVELS}
    if not contract:
        return result
    levels = contract.get("levels")
    if not isinstance(levels, list):
        return result
    for level_entry in levels:
        if not isinstance(level_entry, dict):
            continue
        level = level_entry.get("level")
        nodes = level_entry.get("nodes")
        if level not in LEVELS or not isinstance(nodes, list):
            continue
        typed_nodes = [node for node in nodes if isinstance(node, dict)]
        result[str(level)] = sorted(
            typed_nodes,
            key=lambda node: node.get("order") if type(node.get("order")) is int else 9999,
        )
    return result


def split_node_target(raw_level: str | None, raw_node: str) -> tuple[str | None, str, list[str]]:
    failures: list[str] = []
    level = raw_level
    node_slug = raw_node

    if "/" in raw_node:
        parts = raw_node.split("/")
        if len(parts) != 2:
            failures.append("node_id deve seguir <level>/<node-slug>")
        else:
            embedded_level, embedded_slug = parts
            if level and level != embedded_level:
                failures.append("level informado não corresponde ao level embutido em --node")
            level = level or embedded_level
            node_slug = embedded_slug

    if level is not None and level not in LEVELS:
        failures.append("level deve ser basico, intermediario ou avancado")
    if ".." in Path(node_slug).parts or "/" in node_slug or "\\" in node_slug:
        failures.append("node slug contém caminho ou travessia")
    if not NODE_SLUG_RE.fullmatch(node_slug):
        failures.append("node slug deve seguir o formato NN-slug")

    return level, node_slug, failures


def resolve_contract_node(
    contract: dict[str, Any] | None,
    requested_level: str | None,
    node_slug: str,
) -> tuple[str | None, dict[str, Any] | None, list[str]]:
    by_level = nodes_by_level(contract)
    matches: list[tuple[str, dict[str, Any]]] = []

    for level, nodes in by_level.items():
        if requested_level and level != requested_level:
            continue
        for node in nodes:
            if node.get("slug") == node_slug or node.get("node_id") == f"{level}/{node_slug}":
                matches.append((level, node))

    if len(matches) == 1:
        return matches[0][0], matches[0][1], []
    if not matches:
        if requested_level:
            return requested_level, None, [f"node {requested_level}/{node_slug} não existe em roadmap-contract.json"]
        return None, None, ["node slug não existe em roadmap-contract.json"]
    levels = ", ".join(f"{level}/{node_slug}" for level, _ in matches)
    return None, None, [f"node slug ambíguo; informe --level. Candidatos: {levels}"]


def ordered_contract_slugs(contract: dict[str, Any] | None, level: str) -> list[str]:
    return [
        str(node.get("slug"))
        for node in nodes_by_level(contract).get(level, [])
        if isinstance(node.get("slug"), str)
    ]


def validate_inside(child: Path, parent: Path, label: str) -> list[str]:
    try:
        child.resolve().relative_to(parent.resolve())
    except ValueError:
        return [f"{label} fora do diretório permitido: {child}"]
    return []


def previous_node_dir(roadmap_dir: Path, level: str, node_slug: str, contract_slugs: list[str]) -> Path | None:
    if not contract_slugs or node_slug not in contract_slugs:
        return None
    index = contract_slugs.index(node_slug)
    if index == 0:
        return None
    return roadmap_dir / level / contract_slugs[index - 1]


def file_contains_any(path: Path, needles: tuple[str, ...]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8").lower()
    return any(needle.lower() in text for needle in needles)


def collect_hrefs(html_text: str) -> list[str]:
    parser = LinkParser()
    parser.feed(html_text)
    parser.close()
    return parser.hrefs


def validate_parent_roadmap_link(
    roadmap_html: Path,
    level: str,
    node_slug: str,
    failures: list[str],
) -> None:
    if not is_non_empty_file(roadmap_html):
        return
    expected_href = f"{level}/{node_slug}/node.html"
    hrefs = collect_hrefs(roadmap_html.read_text(encoding="utf-8"))
    if expected_href not in hrefs:
        failures.append(f"roadmap.html não linka o node atual: {expected_href}")


def file_indicates_required_rewrite(path: Path) -> bool:
    if not path.exists():
        return True
    text = path.read_text(encoding="utf-8").lower()
    blocking_patterns = (
        "reescrita obrigatória",
        "reescrita obrigatoria",
        "alteração obrigatória",
        "alteracao obrigatoria",
        "ação obrigatória",
        "acao obrigatoria",
        "falha visual pendente",
        "html precisa reescrita: sim",
    )
    no_rewrite_patterns = (
        "nenhuma reescrita é obrigatória",
        "nenhuma reescrita e obrigatoria",
        "não há reescrita obrigatória",
        "nao ha reescrita obrigatoria",
        "sem reescrita obrigatória",
        "sem reescrita obrigatoria",
        "html precisa reescrita: não",
        "html precisa reescrita: nao",
    )
    if any(pattern in text for pattern in no_rewrite_patterns):
        return False
    return any(pattern in text for pattern in blocking_patterns)


def require_audit_pass(path: Path, label: str, failures: list[str]) -> None:
    if not is_non_empty_file(path):
        failures.append(f"{label} ausente ou vazio: {path}")
        return
    if not file_contains_any(path, ("status geral: passa", "status: passa")):
        failures.append(f"{label} não registra status de passagem")


def require_revision_plan_clear(path: Path, label: str, failures: list[str]) -> None:
    if not is_non_empty_file(path):
        failures.append(f"{label} ausente ou vazio: {path}")
        return
    if file_indicates_required_rewrite(path):
        failures.append(f"{label} ainda indica reescrita obrigatória")


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
    requested_level, node_slug, target_failures = split_node_target(args.level, args.node)
    failures.extend(target_failures)

    if not roadmap_dir.exists() or not roadmap_dir.is_dir():
        failures.append(f"roadmap dir não existe: {roadmap_dir}")
        return failures

    roadmap_html = roadmap_dir / "roadmap.html"
    if not roadmap_html.exists():
        failures.append(f"roadmap.html ausente: {roadmap_html}")

    contract, contract_failures = load_contract(roadmap_dir)
    failures.extend(contract_failures)
    resolved_level, contract_node, resolve_failures = resolve_contract_node(contract, requested_level, node_slug)
    failures.extend(resolve_failures)
    if not resolved_level or not contract_node:
        return failures

    expected_node_id = f"{resolved_level}/{node_slug}"
    if contract_node.get("node_id") != expected_node_id:
        failures.append(f"node_id do contrato não corresponde ao alvo: esperado {expected_node_id}")
    if contract_node.get("level") != resolved_level:
        failures.append(f"level do contrato não corresponde ao alvo: esperado {resolved_level}")

    level_dir = roadmap_dir / resolved_level
    node_dir = level_dir / node_slug
    failures.extend(validate_inside(level_dir, roadmap_dir, "level dir"))
    failures.extend(validate_inside(node_dir, level_dir, "node dir"))

    if not node_dir.exists() or not node_dir.is_dir():
        failures.append(f"node dir não existe: {node_dir}")
        return failures

    contract_slugs = ordered_contract_slugs(contract, resolved_level)
    previous_dir = previous_node_dir(roadmap_dir, resolved_level, node_slug, contract_slugs)
    if previous_dir is not None:
        failures.extend(validate_inside(previous_dir, level_dir, "node anterior"))
        if not previous_dir.exists() or not previous_dir.is_dir():
            failures.append(f"node anterior ausente: {previous_dir}")
        else:
            for name in ("research-dump.md", "node.html"):
                path = previous_dir / name
                if not is_non_empty_file(path):
                    failures.append(f"node anterior sem {name} não vazio: {path}")

    for name in ("research-dump.md", "node.html"):
        path = node_dir / name
        if not is_non_empty_file(path):
            failures.append(f"node atual sem {name} não vazio: {path}")

    editorial_dir = node_dir / ".editorial"
    failures.extend(validate_inside(editorial_dir, node_dir, ".editorial"))
    if not editorial_dir.exists() or not editorial_dir.is_dir():
        failures.append(f".editorial ausente: {editorial_dir}")
        return failures

    concept_ledger = editorial_dir / "concept-ledger.md"
    if not is_non_empty_file(concept_ledger):
        failures.append(f"concept-ledger.md ausente ou vazio: {concept_ledger}")

    node_html = node_dir / "node.html"
    pipeline_dir = editorial_dir / "pipeline"
    visible_text = pipeline_dir / "01-visible-text" / "visible-text.md"
    if is_non_empty_file(node_html) and is_non_empty_file(visible_text):
        expected = render_markdown(
            extract_visible_text(node_html.read_text(encoding="utf-8"))
        )
        actual = visible_text.read_text(encoding="utf-8")
        if actual != expected:
            failures.append("visible-text.md não corresponde à extração atual de node.html")
    elif not is_non_empty_file(visible_text):
        failures.append(f"visible-text.md ausente ou vazio: {visible_text}")

    concept_pipe = pipeline_dir / "02-concept-introduction"
    example_pipe = pipeline_dir / "03-example-sufficiency"
    primitive_pipe = pipeline_dir / "04-visual-primitive-choice"
    visual_pipe = pipeline_dir / "05-visual-render"

    require_audit_pass(concept_pipe / "concept-audit.md", "concept-audit.md", failures)
    require_revision_plan_clear(concept_pipe / "revision-plan.md", "revision-plan.md do pipe conceitual", failures)
    require_audit_pass(example_pipe / "example-audit.md", "example-audit.md", failures)
    require_revision_plan_clear(example_pipe / "revision-plan.md", "revision-plan.md do pipe de exemplos", failures)
    require_audit_pass(primitive_pipe / "primitive-audit.md", "primitive-audit.md", failures)
    require_revision_plan_clear(primitive_pipe / "revision-plan.md", "revision-plan.md do pipe de primitiva visual", failures)
    require_audit_pass(visual_pipe / "visual-audit.md", "visual-audit.md", failures)
    require_revision_plan_clear(visual_pipe / "revision-plan.md", "revision-plan.md do pipe visual", failures)
    validate_render_checks(visual_pipe / "render-checks.json", failures)

    playwright_dir = visual_pipe / "playwright"
    if not playwright_dir.exists():
        failures.append(f"playwright do pipe visual ausente: {playwright_dir}")
    else:
        failures.extend(validate_inside(playwright_dir, visual_pipe, "playwright do pipe visual"))
        if not playwright_dir.is_dir():
            failures.append(f"playwright do pipe visual não é diretório: {playwright_dir}")
        else:
            for name in ("desktop.png", "mobile.png"):
                path = playwright_dir / name
                if not is_non_empty_file(path):
                    failures.append(f"evidência visual ausente ou vazia: {path}")

    if is_non_empty_file(node_html):
        html_failures = collect_html_shape_failures(node_html.read_text(encoding="utf-8"))
        failures.extend(f"HTML: {failure}" for failure in html_failures)
        validate_parent_roadmap_link(roadmap_html, resolved_level, node_slug, failures)

    return failures


def main() -> int:
    args = parse_args()
    failures = validate(args)

    if failures:
        print("falha: artefatos do node inválidos")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("passa: artefatos mecânicos do node válidos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
