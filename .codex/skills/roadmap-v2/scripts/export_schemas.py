#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

SKILL_DIR = Path(__file__).resolve().parents[1]
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from models.node_spec import NodeSpec  # noqa: E402
from models.page_spec import PageSpec  # noqa: E402
from models.pipeline import PipelineRun  # noqa: E402
from models.research_pack import ResearchPack  # noqa: E402
from models.roadmap_spec import RoadmapSpec  # noqa: E402


SCHEMAS = {
    "research-pack.schema.json": ResearchPack,
    "roadmap-spec.schema.json": RoadmapSpec,
    "node-spec.schema.json": NodeSpec,
    "page-spec.schema.json": PageSpec,
    "pipeline-run.schema.json": PipelineRun,
}


def normalized_schema(model: type) -> str:
    schema = model.model_json_schema(mode="validation")
    return json.dumps(schema, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Export or check roadmap-v2 JSON Schemas.")
    parser.add_argument("--check", action="store_true", help="Fail if committed schemas drift from models.")
    args = parser.parse_args()

    contracts_dir = SKILL_DIR / "contracts"
    contracts_dir.mkdir(parents=True, exist_ok=True)
    drift: list[str] = []
    for filename, model in SCHEMAS.items():
        path = contracts_dir / filename
        expected = normalized_schema(model)
        if args.check:
            current = path.read_text(encoding="utf-8") if path.exists() else ""
            if current != expected:
                drift.append(filename)
        else:
            path.write_text(expected, encoding="utf-8")

    if drift:
        print("Schema drift detected: " + ", ".join(drift), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
