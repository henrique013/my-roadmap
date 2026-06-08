#!/usr/bin/env python3
"""Smoke tests for node position context validation."""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path
from types import SimpleNamespace

from extract_visible_text import extract_visible_text, render_markdown
from validate_node_artifacts import validate


LEVEL = "basico"
NODES = [
    {
        "node_id": "basico/01-first-node",
        "level": LEVEL,
        "order": 1,
        "slug": "01-first-node",
        "label": "First Node",
    },
    {
        "node_id": "basico/02-middle-node",
        "level": LEVEL,
        "order": 2,
        "slug": "02-middle-node",
        "label": "Middle Node",
    },
    {
        "node_id": "basico/03-last-node",
        "level": LEVEL,
        "order": 3,
        "slug": "03-last-node",
        "label": "Last Node",
    },
]


def contract() -> dict[str, object]:
    return {
        "schema_version": "2.0",
        "roadmap_slug": "position-fixture",
        "theme": "Position Fixture Roadmap",
        "levels": [
            {
                "level": LEVEL,
                "nodes": NODES,
            },
            {
                "level": "intermediario",
                "nodes": [],
            },
            {
                "level": "avancado",
                "nodes": [],
            },
        ],
    }


def node_html(node: dict[str, object], previous_markup: str, next_markup: str) -> str:
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{node["label"]}</title>
  <style>
    body {{ font-family: Arial, sans-serif; }}
    .node-context {{ border: 1px solid #ccc; padding: 8px; }}
  </style>
</head>
<body>
  <main>
    <a href="../../roadmap.html">Voltar ao roadmap</a>
    <div
      class="node-context"
      data-node-position="true"
      data-level="{node["level"]}"
      data-node-order="{node["order"]}"
      data-node-count="3"
      data-roadmap-slug="position-fixture">
      <p><strong>Básico · {int(node["order"]):02d} de 03</strong></p>
      <p>Roadmap: Position Fixture Roadmap</p>
      <p>Node atual: {node["label"]}</p>
      <p>Anterior: {previous_markup} · Próximo: {next_markup}</p>
    </div>
    <h1>{node["label"]}</h1>
    <p class="lead">A short narrative opening.</p>
    <section>
      <h2>Readable Section</h2>
      <p>Body text.</p>
    </section>
  </main>
  <!-- Referências: fixture -->
</body>
</html>
"""


def html_without_position(node: dict[str, object]) -> str:
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{node["label"]}</title>
  <style>body {{ font-family: Arial, sans-serif; }}</style>
</head>
<body>
  <main>
    <a href="../../roadmap.html">Voltar ao roadmap</a>
    <h1>{node["label"]}</h1>
    <p class="lead">Only technical metadata would not be enough.</p>
  </main>
  <!-- Referências: fixture -->
</body>
</html>
"""


def write_pipeline(node_dir: Path, html_text: str) -> None:
    editorial = node_dir / ".editorial"
    pipeline = editorial / "pipeline"
    visual = pipeline / "05-visual-render"
    (pipeline / "01-visible-text").mkdir(parents=True)
    (pipeline / "02-concept-introduction").mkdir(parents=True)
    (pipeline / "03-example-sufficiency").mkdir(parents=True)
    (pipeline / "04-visual-primitive-choice").mkdir(parents=True)
    (visual / "playwright").mkdir(parents=True)

    (editorial / "concept-ledger.md").write_text("# Concept ledger\n", encoding="utf-8")
    visible = render_markdown(extract_visible_text(html_text))
    (pipeline / "01-visible-text" / "visible-text.md").write_text(visible, encoding="utf-8")

    audit_files = [
        pipeline / "02-concept-introduction" / "concept-audit.md",
        pipeline / "03-example-sufficiency" / "example-audit.md",
        pipeline / "04-visual-primitive-choice" / "primitive-audit.md",
        visual / "visual-audit.md",
    ]
    for path in audit_files:
        path.write_text("# Audit\n\nStatus geral: passa\n", encoding="utf-8")

    revision_files = [
        pipeline / "02-concept-introduction" / "revision-plan.md",
        pipeline / "03-example-sufficiency" / "revision-plan.md",
        pipeline / "04-visual-primitive-choice" / "revision-plan.md",
        visual / "revision-plan.md",
    ]
    for path in revision_files:
        path.write_text("# Revision plan\n\nNenhuma reescrita é obrigatória.\n", encoding="utf-8")

    (visual / "render-checks.json").write_text('{"status": "passa"}\n', encoding="utf-8")
    (visual / "playwright" / "desktop.png").write_bytes(b"png")
    (visual / "playwright" / "mobile.png").write_bytes(b"png")


def write_node(roadmap_dir: Path, node: dict[str, object], html_text: str) -> None:
    node_dir = roadmap_dir / str(node["level"]) / str(node["slug"])
    node_dir.mkdir(parents=True)
    (node_dir / "research-dump.md").write_text("# Research dump\n", encoding="utf-8")
    (node_dir / "node.html").write_text(html_text, encoding="utf-8")
    write_pipeline(node_dir, html_text)


def neighbor_markup(
    node: dict[str, object],
    generated_slugs: set[str],
    force_plain: set[tuple[str, str]],
    direction: str,
) -> str:
    slug = str(node["slug"])
    label = str(node["label"])
    if slug in generated_slugs and (slug, direction) not in force_plain:
        return f'<a href="../{slug}/node.html">{label}</a>'
    return label


def build_fixture(
    root: Path,
    omit_position_for: str | None = None,
    skip_generated: set[str] | None = None,
    force_plain: set[tuple[str, str]] | None = None,
) -> Path:
    roadmap_dir = root / "position-fixture"
    skipped = skip_generated or set()
    plain = force_plain or set()
    generated_slugs = {str(node["slug"]) for node in NODES if str(node["slug"]) not in skipped}
    (roadmap_dir / ".roadmap").mkdir(parents=True)
    (roadmap_dir / ".roadmap" / "roadmap-contract.json").write_text(
        json.dumps(contract(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    links = [
        f'<a href="{LEVEL}/{node["slug"]}/node.html">{node["label"]}</a>'
        for node in NODES
    ]
    roadmap_html = "<!doctype html><html><body>{}</body></html>".format("".join(links))
    (roadmap_dir / "roadmap.html").write_text(roadmap_html, encoding="utf-8")

    for index, node in enumerate(NODES):
        if str(node["slug"]) in skipped:
            continue
        previous_markup = (
            "primeiro node do nível"
            if index == 0
            else neighbor_markup(NODES[index - 1], generated_slugs, plain, "previous")
        )
        next_markup = (
            "último node do nível"
            if index == len(NODES) - 1
            else neighbor_markup(NODES[index + 1], generated_slugs, plain, "next")
        )
        if node["slug"] == omit_position_for:
            html_text = html_without_position(node)
        else:
            html_text = node_html(node, previous_markup, next_markup)
        write_node(roadmap_dir, node, html_text)

    return roadmap_dir


def validate_node(roadmap_dir: Path, node_slug: str) -> list[str]:
    args = SimpleNamespace(roadmap_dir=str(roadmap_dir), level=LEVEL, node=node_slug)
    return validate(args)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="node-position-context-") as tmp:
        roadmap_dir = build_fixture(Path(tmp))
        for node in NODES:
            failures = validate_node(roadmap_dir, str(node["slug"]))
            if failures:
                print(f"falha: {node['slug']} deveria passar")
                for failure in failures:
                    print(f"- {failure}")
                return 1

    with tempfile.TemporaryDirectory(prefix="node-position-context-missing-") as tmp:
        roadmap_dir = build_fixture(Path(tmp), omit_position_for="02-middle-node")
        failures = validate_node(roadmap_dir, "02-middle-node")
        if not any("contexto de posição" in failure for failure in failures):
            print("falha: node sem contexto de posição deveria falhar")
            for failure in failures:
                print(f"- {failure}")
            return 1

    with tempfile.TemporaryDirectory(prefix="node-position-context-next-missing-") as tmp:
        roadmap_dir = build_fixture(Path(tmp), skip_generated={"03-last-node"})
        failures = validate_node(roadmap_dir, "02-middle-node")
        if failures:
            print("falha: próximo node não gerado deveria passar sem link")
            for failure in failures:
                print(f"- {failure}")
            return 1

    with tempfile.TemporaryDirectory(prefix="node-position-context-prev-plain-") as tmp:
        roadmap_dir = build_fixture(Path(tmp), force_plain={("01-first-node", "previous")})
        failures = validate_node(roadmap_dir, "02-middle-node")
        if not any("deve linkar node anterior" in failure for failure in failures):
            print("falha: anterior gerado sem link deveria falhar")
            for failure in failures:
                print(f"- {failure}")
            return 1

    with tempfile.TemporaryDirectory(prefix="node-position-context-next-plain-") as tmp:
        roadmap_dir = build_fixture(Path(tmp), force_plain={("03-last-node", "next")})
        failures = validate_node(roadmap_dir, "02-middle-node")
        if not any("deve linkar node próximo" in failure for failure in failures):
            print("falha: próximo gerado sem link deveria falhar")
            for failure in failures:
                print(f"- {failure}")
            return 1

    print("passa: contexto de posição valida links de vizinhos gerados, ausência e casos negativos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
