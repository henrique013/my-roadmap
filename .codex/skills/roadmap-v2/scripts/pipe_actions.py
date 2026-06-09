from __future__ import annotations

import json
import os
import posixpath
import shutil
import subprocess
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup

from models.node_spec import NodeSpec
from models.page_spec import PageBlock, PageSpec
from models.research_pack import ResearchPack
from models.roadmap_spec import LevelSpec, RoadmapNode, RoadmapSpec
from rules.accentuation import validate_visible_text_accentuation
from rules.content_boundaries import validate_content_boundaries
from rules.ids import build_node_id, validate_unique_node_ids
from rules.navigation import validate_navigation_links, validate_previous_next
from rules.paths import safe_child_path
from rules.slugs import normalize_slug, validate_slug
from rules.sources import require_sources_for_current_topic, validate_source_traceability
from runner.errors import DomValidationError, InputAmbiguityError, ResearchInsufficientError, VisualRegressionError
from runner.paths import resolve_runtime_paths
from runner.result import PipeContext


def route_request(data: dict[str, Any], context: PipeContext) -> dict[str, Any]:
    mode = data.get("mode") or context.mode
    if mode != context.mode:
        raise InputAmbiguityError(f"request mode {mode!r} conflicts with pipeline mode {context.mode!r}")
    return {**data, "mode": mode}


def normalize_input(data: dict[str, Any], context: PipeContext) -> dict[str, Any]:
    request = data.get("request", data)
    topic = str(request.get("topic", "")).strip()
    if not topic:
        raise InputAmbiguityError("roadmap topic is required")
    return {
        **data,
        "topic": topic,
        "audience": str(request.get("audience") or data.get("audience") or "general").strip() or "general",
        "assumptions": list(request.get("assumptions", data.get("assumptions", [])) or []),
        "limits": list(request.get("limits", data.get("limits", [])) or []),
    }


def resolve_output_path(data: dict[str, Any], context: PipeContext) -> dict[str, Any]:
    slug = validate_slug(data.get("roadmap_slug") or normalize_slug(data["topic"]))
    expected_root = Path(".tmp") / "roadmaps-v2" / slug
    return {
        **data,
        "roadmap_slug": slug,
        "roadmap_id": slug,
        "output_root_contract": str(expected_root),
    }


def validate_research_pack(data: dict[str, Any], context: PipeContext) -> None:
    pack_data = data.get("research_pack", data)
    pack = ResearchPack.model_validate(pack_data)
    if not pack.sources:
        raise ResearchInsufficientError(f"research for {pack.topic!r} has no sources")
    source_ids = {source.id for source in pack.sources}
    for fact in pack.facts:
        validate_source_traceability(source_ids, fact.source_ids)


def build_roadmap_spec(data: dict[str, Any], context: PipeContext) -> dict[str, Any]:
    spec_data = data.get("roadmap_spec") or data.get("roadmap_draft") or data
    spec = RoadmapSpec.model_validate(spec_data)
    _validate_roadmap_rules(spec)
    context.artifact_store.write_json("roadmap-spec.json", spec.model_dump(mode="json", exclude_none=True))
    return {**data, "roadmap_spec": spec.model_dump(mode="json", exclude_none=True), "roadmap_spec_path": "roadmap-spec.json"}


def validate_roadmap_spec(data: dict[str, Any], context: PipeContext) -> dict[str, Any]:
    spec = RoadmapSpec.model_validate(data["roadmap_spec"])
    _validate_roadmap_rules(spec)
    return data


def build_page_spec(data: dict[str, Any], context: PipeContext) -> dict[str, Any]:
    spec = RoadmapSpec.model_validate(data["roadmap_spec"])
    blocks = [
        PageBlock(
            id="hero",
            type="hero",
            title=spec.title,
            text=f"Roadmap para {spec.topic}",
            props={"audience": spec.audience},
        ),
        PageBlock(
            id="level-tabs",
            type="level_tabs",
            title="Níveis",
            items=[
                {"id": level.id, "title": level.title, "summary": level.summary}
                for level in spec.levels
            ],
        ),
        PageBlock(
            id="node-grid",
            type="node_grid",
            title="Nodes",
            items=[
                {
                    "node_id": node.node_id,
                    "level": node.level,
                    "level_title": level.title,
                    "order": node.order,
                    "slug": node.slug,
                    "title": node.title,
                    "summary": node.summary,
                    "href": f"nodes/{node.level}/{node.slug}/node.html",
                }
                for level in spec.levels
                for node in level.nodes
            ],
        ),
        PageBlock(
            id="references",
            type="references",
            title="Referências",
            items=[source.model_dump(mode="json") for source in spec.sources],
        ),
    ]
    page = PageSpec(
        page_type="roadmap",
        title=spec.title,
        slug=spec.slug,
        description=f"Roadmap estruturado para {spec.topic}.",
        blocks=blocks,
        sources=spec.sources,
    )
    context.artifact_store.write_json("page-spec.json", page.model_dump(mode="json", exclude_none=True))
    return {
        **data,
        "page_spec": page.model_dump(mode="json", exclude_none=True),
        "page_spec_path": "page-spec.json",
        "final_output_path": "roadmap.html",
    }


def load_roadmap_spec(data: dict[str, Any], context: PipeContext) -> dict[str, Any]:
    path = data.get("roadmap_spec_path", "roadmap-spec.json")
    spec = RoadmapSpec.model_validate(context.artifact_store.read_json(path))
    return {**data, "roadmap_spec": spec.model_dump(mode="json", exclude_none=True), "roadmap_slug": spec.slug}


def resolve_node_target(data: dict[str, Any], context: PipeContext) -> dict[str, Any]:
    spec = RoadmapSpec.model_validate(data["roadmap_spec"])
    target = str(data.get("node_id") or data.get("node_slug") or "").strip()
    level = data.get("level")
    candidates: list[RoadmapNode] = []
    for roadmap_level in spec.levels:
        for node in roadmap_level.nodes:
            if data.get("node_id") and node.node_id == target:
                candidates.append(node)
            elif level and data.get("node_slug") and node.level == level and node.slug == target:
                candidates.append(node)
            elif data.get("node_slug") and node.slug == target:
                candidates.append(node)
    if len(candidates) != 1:
        raise InputAmbiguityError(f"node target must resolve to exactly one node, got {len(candidates)}")
    node = candidates[0]
    return {
        **data,
        "node_id": node.node_id,
        "level": node.level,
        "node_slug": node.slug,
        "target_node": node.model_dump(mode="json"),
    }


def validate_node_order(data: dict[str, Any], context: PipeContext) -> dict[str, Any]:
    spec = RoadmapSpec.model_validate(data["roadmap_spec"])
    nodes = [node.model_dump(mode="json") for level in spec.levels for node in level.nodes]
    ordered_ids = [node["node_id"] for node in nodes]
    for index, node in enumerate(nodes):
        node["previous_node_id"] = ordered_ids[index - 1] if index > 0 else None
        node["next_node_id"] = ordered_ids[index + 1] if index + 1 < len(ordered_ids) else None
    validate_previous_next(nodes)
    current_index = ordered_ids.index(data["node_id"])
    return {
        **data,
        "previous_node_id": ordered_ids[current_index - 1] if current_index > 0 else None,
        "next_node_id": ordered_ids[current_index + 1] if current_index + 1 < len(ordered_ids) else None,
    }


def build_node_spec(data: dict[str, Any], context: PipeContext) -> dict[str, Any]:
    spec_data = data.get("node_spec") or data
    spec = NodeSpec.model_validate(spec_data)
    validate_slug(spec.node_slug)
    if spec.node_id != build_node_id(spec.level, spec.node_slug):
        raise ValueError("node_id must match level/node_slug")
    source_ids = {source.id for source in spec.sources}
    validate_source_traceability(source_ids, spec.source_ids)
    rel = f"nodes/{spec.level}/{spec.node_slug}/node-spec.json"
    context.artifact_store.write_json(rel, spec.model_dump(mode="json", exclude_none=True))
    return {**data, "node_spec": spec.model_dump(mode="json", exclude_none=True), "node_spec_path": rel}


def validate_node_spec(data: dict[str, Any], context: PipeContext) -> dict[str, Any]:
    spec = NodeSpec.model_validate(data["node_spec"])
    validate_slug(spec.node_slug)
    source_ids = {source.id for source in spec.sources}
    validate_source_traceability(source_ids, spec.source_ids)
    return data


def build_node_page_spec(data: dict[str, Any], context: PipeContext) -> dict[str, Any]:
    node = NodeSpec.model_validate(data["node_spec"])
    roadmap = RoadmapSpec.model_validate(data["roadmap_spec"])
    nodes_by_id = {
        roadmap_node.node_id: roadmap_node
        for level in roadmap.levels
        for roadmap_node in level.nodes
    }
    current_dir = f"nodes/{node.level}/{node.node_slug}"

    def relative_node_href(node_id: str | None) -> str | None:
        if node_id is None:
            return None
        target = nodes_by_id[node_id]
        return posixpath.relpath(
            f"nodes/{target.level}/{target.slug}/node.html",
            start=current_dir,
        )

    previous_href = relative_node_href(node.previous_node_id)
    next_href = relative_node_href(node.next_node_id)
    blocks = [
        PageBlock(id="hero", type="hero", title=node.title, text=node.summary),
        PageBlock(
            id="navigation",
            type="navigation_trail",
            title="Navegação",
            items=[
                {"rel": "parent", "href": "../../../roadmap.html", "label": "Roadmap"},
                *(
                    [{"rel": "previous", "href": previous_href, "label": "Anterior"}]
                    if previous_href
                    else []
                ),
                *(
                    [{"rel": "next", "href": next_href, "label": "Próximo"}]
                    if next_href
                    else []
                ),
            ],
        ),
        *[
            PageBlock(
                id=f"concept-{concept.id}",
                type="concept_section",
                title=concept.title,
                text=concept.body,
                items=[{"example": example} for example in concept.examples],
            )
            for concept in node.concepts
        ],
        PageBlock(
            id="references",
            type="references",
            title="Referências",
            items=[source.model_dump(mode="json") for source in node.sources],
        ),
    ]
    page = PageSpec(
        page_type="node",
        title=node.title,
        slug=node.node_slug,
        description=node.summary,
        blocks=blocks,
        sources=node.sources,
    )
    rel = f"nodes/{node.level}/{node.node_slug}/page-spec.json"
    context.artifact_store.write_json(rel, page.model_dump(mode="json", exclude_none=True))
    return {
        **data,
        "page_spec": page.model_dump(mode="json", exclude_none=True),
        "page_spec_path": rel,
        "final_output_path": f"nodes/{node.level}/{node.node_slug}/node.html",
    }


def update_navigation_index(data: dict[str, Any], context: PipeContext) -> dict[str, Any]:
    index_path = ".pipeline/navigation-index.json"
    try:
        index = context.artifact_store.read_json(index_path)
    except FileNotFoundError:
        index = {"nodes": {}}
    index["nodes"][data["node_id"]] = {
        "level": data["level"],
        "node_slug": data["node_slug"],
        "node_html": data.get("final_output_path"),
        "previous_node_id": data.get("previous_node_id"),
        "next_node_id": data.get("next_node_id"),
    }
    context.artifact_store.write_json(index_path, index)
    return {**data, "navigation_index_path": index_path}


def validate_dom(data: dict[str, Any], context: PipeContext) -> dict[str, Any]:
    html_path = context.output_root / data["rendered_html_path"]
    html = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    allowed_wa = {
        "wa-badge",
        "wa-breadcrumb",
        "wa-breadcrumb-item",
        "wa-button",
        "wa-card",
        "wa-callout",
        "wa-divider",
        "wa-tab",
        "wa-tab-group",
        "wa-tab-panel",
        "wa-tag",
    }
    for tag in soup.find_all(True):
        if tag.name.startswith("wa-") and tag.name not in allowed_wa:
            raise DomValidationError(f"unsupported Web Awesome component: {tag.name}")
        src = tag.get("src")
        if isinstance(src, str) and src.startswith(("http://", "https://")):
            raise DomValidationError(f"external asset reference is not allowed: {src}")
        href = tag.get("href")
        if tag.name in {"link", "script"} and isinstance(href, str) and href.startswith(("http://", "https://")):
            raise DomValidationError(f"external asset reference is not allowed: {href}")
    text = soup.get_text(" ")
    validate_visible_text_accentuation([text])
    return data


def validate_visual(data: dict[str, Any], context: PipeContext) -> dict[str, Any]:
    checks_path = context.pipeline_dir / "visual" / "checks.json"
    if checks_path.exists():
        checks = json.loads(checks_path.read_text(encoding="utf-8"))
        allowed_statuses = {"ok"}
        if os.environ.get("ROADMAP_V2_VISUAL_STRICT") == "0":
            allowed_statuses.add("skipped")
        failures = [
            item
            for item in checks.get("checks", [])
            if item.get("status") not in allowed_statuses
        ]
        if failures:
            raise VisualRegressionError(json.dumps(failures, ensure_ascii=False))
    return data


def run_visual_check(data: dict[str, Any], context: PipeContext) -> dict[str, Any]:
    html_path = context.output_root / data["rendered_html_path"]
    visual_dir = context.pipeline_dir / "visual"
    visual_dir.mkdir(parents=True, exist_ok=True)
    script = context.skill_dir / "web" / "scripts" / "check-visual.mjs"
    paths = resolve_runtime_paths(context.skill_dir)
    env = {
        **os.environ,
        "PLAYWRIGHT_BROWSERS_PATH": str(paths.browsers_dir),
        "ROADMAP_V2_NODE_MODULES": str(paths.node_modules),
    }
    result = subprocess.run(
        ["node", str(script), str(html_path), str(visual_dir)],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
    (visual_dir / "visual.stdout.log").write_text(result.stdout, encoding="utf-8")
    (visual_dir / "visual.stderr.log").write_text(result.stderr, encoding="utf-8")
    if result.returncode != 0:
        raise VisualRegressionError(result.stderr.strip() or "visual validation failed")
    return validate_visual(data, context)


def finalize_output(data: dict[str, Any], context: PipeContext) -> dict[str, Any]:
    rendered = context.output_root / data["rendered_html_path"]
    final = safe_child_path(context.output_root, data["final_output_path"])
    final.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(rendered, final)
    copy_render_assets(rendered.parent, final.parent)
    return {**data, "visible_output_path": data["final_output_path"]}


def copy_render_assets(render_dir: Path, final_dir: Path) -> None:
    ignored = {"index.html", "astro.stdout.log", "astro.stderr.log"}
    for child in render_dir.iterdir():
        if child.name in ignored:
            continue
        target = final_dir / child.name
        if child.is_dir():
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(child, target)
        elif child.is_file():
            shutil.copyfile(child, target)


def _validate_roadmap_rules(spec: RoadmapSpec) -> None:
    validate_slug(spec.slug)
    nodes = [node for level in spec.levels for node in level.nodes]
    validate_unique_node_ids(node.node_id for node in nodes)
    source_ids = {source.id for source in spec.sources}
    for node in nodes:
        if node.node_id != build_node_id(node.level, node.slug):
            raise ValueError(f"node_id does not match level/slug: {node.node_id}")
        validate_source_traceability(source_ids, node.source_ids)
    require_sources_for_current_topic([source.model_dump(mode="json") for source in spec.sources], spec.topic)
    validate_content_boundaries([node.model_dump(mode="json") for node in nodes])
    validate_navigation_links(
        [
            {"href": f"nodes/{node.level}/{node.slug}/node.html"}
            for node in nodes
        ]
    )


def validate_page_spec(data: dict[str, Any], context: PipeContext) -> None:
    page = PageSpec.model_validate(data.get("page_spec", data))
    validate_navigation_links([link.model_dump(mode="json") for link in page.navigation])
