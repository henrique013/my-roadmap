#!/usr/bin/env python3
"""Validate required mechanical artifacts for a roadmap node."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from check_html_shape import collect_failures as collect_html_shape_failures
from extract_visible_text import extract_visible_text, render_markdown


NODE_SLUG_RE = re.compile(r"^\d{2}-[a-z0-9][a-z0-9-]*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Valida a estrutura mecânica obrigatória de um node."
    )
    parser.add_argument(
        "--roadmap-dir",
        required=True,
        help="Diretório do roadmap que contém roadmap.html.",
    )
    parser.add_argument("--node", required=True, help="Slug do node no formato NN-slug.")
    return parser.parse_args()


def is_non_empty_file(path: Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


def validate_inside(child: Path, parent: Path, label: str) -> list[str]:
    try:
        child.resolve().relative_to(parent.resolve())
    except ValueError:
        return [f"{label} fora do diretório permitido: {child}"]
    return []


def previous_node_dir(roadmap_dir: Path, node_slug: str) -> Path | None:
    number_text, suffix = node_slug.split("-", 1)
    number = int(number_text)
    if number <= 1:
        return None

    prefix = f"{number - 1:02d}-"
    candidates = sorted(
        path for path in roadmap_dir.iterdir() if path.is_dir() and path.name.startswith(prefix)
    )
    if not candidates:
        return roadmap_dir / f"{number - 1:02d}-{suffix}"
    if len(candidates) == 1:
        return candidates[0]
    return candidates[0]


def file_contains_any(path: Path, needles: tuple[str, ...]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8").lower()
    return any(needle.lower() in text for needle in needles)


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


def validate(args: argparse.Namespace) -> list[str]:
    failures: list[str] = []
    roadmap_dir = Path(args.roadmap_dir)
    node_slug = args.node

    if ".." in Path(node_slug).parts or "/" in node_slug or "\\" in node_slug:
        failures.append("node slug contém caminho ou travessia")
    if not NODE_SLUG_RE.fullmatch(node_slug):
        failures.append("node slug deve seguir o formato NN-slug")

    if not roadmap_dir.exists() or not roadmap_dir.is_dir():
        failures.append(f"roadmap dir não existe: {roadmap_dir}")
        return failures

    roadmap_html = roadmap_dir / "roadmap.html"
    if not roadmap_html.exists():
        failures.append(f"roadmap.html ausente: {roadmap_html}")

    node_dir = roadmap_dir / node_slug
    failures.extend(validate_inside(node_dir, roadmap_dir, "node dir"))

    if not node_dir.exists() or not node_dir.is_dir():
        failures.append(f"node dir não existe: {node_dir}")
        return failures

    previous_dir = previous_node_dir(roadmap_dir, node_slug)
    if previous_dir is not None:
        failures.extend(validate_inside(previous_dir, roadmap_dir, "node anterior"))
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

    required_editorial_files = (
        "concept-ledger.md",
        "visible-text.md",
        "concept-audit.md",
        "example-audit.md",
        "visual-audit.md",
        "revision-plan.md",
    )
    for name in required_editorial_files:
        path = editorial_dir / name
        if not is_non_empty_file(path):
            failures.append(f"arquivo editorial ausente ou vazio: {path}")

    node_html = node_dir / "node.html"
    visible_text = editorial_dir / "visible-text.md"
    if is_non_empty_file(node_html) and is_non_empty_file(visible_text):
        expected = render_markdown(
            extract_visible_text(node_html.read_text(encoding="utf-8"))
        )
        actual = visible_text.read_text(encoding="utf-8")
        if actual != expected:
            failures.append("visible-text.md não corresponde à extração atual de node.html")

    concept_audit = editorial_dir / "concept-audit.md"
    if is_non_empty_file(concept_audit) and not file_contains_any(
        concept_audit,
        (
            "status geral: passa",
            "status: passa",
            "passa",
        ),
    ):
        failures.append("concept-audit.md não registra status de passagem")

    example_audit = editorial_dir / "example-audit.md"
    if is_non_empty_file(example_audit) and not file_contains_any(
        example_audit,
        (
            "status geral: passa",
            "status: passa",
        ),
    ):
        failures.append("example-audit.md não registra status de passagem")

    visual_audit = editorial_dir / "visual-audit.md"
    if is_non_empty_file(visual_audit) and not file_contains_any(
        visual_audit,
        (
            "status geral: passa",
            "status: passa",
        ),
    ):
        failures.append("visual-audit.md não registra status de passagem")

    playwright_dir = editorial_dir / "playwright"
    if not playwright_dir.exists():
        failures.append(f".editorial/playwright ausente: {playwright_dir}")
    else:
        failures.extend(validate_inside(playwright_dir, editorial_dir, ".editorial/playwright"))
        if not playwright_dir.is_dir():
            failures.append(f".editorial/playwright não é diretório: {playwright_dir}")
        else:
            for name in ("desktop.png", "mobile.png"):
                path = playwright_dir / name
                if not is_non_empty_file(path):
                    failures.append(f"evidência visual ausente ou vazia: {path}")

    revision_plan = editorial_dir / "revision-plan.md"
    if is_non_empty_file(revision_plan) and file_indicates_required_rewrite(revision_plan):
        failures.append("revision-plan.md ainda indica reescrita obrigatória")

    if is_non_empty_file(node_html):
        html_failures = collect_html_shape_failures(node_html.read_text(encoding="utf-8"))
        failures.extend(f"HTML: {failure}" for failure in html_failures)

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
