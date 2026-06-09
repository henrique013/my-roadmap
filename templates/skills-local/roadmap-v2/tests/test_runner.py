from __future__ import annotations

import json
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from runner.llm import parse_llm_json
from runner.manifest import load_pipe_manifest
from runner.pipeline import PipelineRunner
from runner.artifacts import ArtifactStore
from runner.result import PipeContext
from scripts.pipe_actions import build_node_page_spec


FIXTURES = SKILL_DIR / "tests" / "fixtures"


class RunnerTests(unittest.TestCase):
    def context(self, root: Path) -> PipeContext:
        return PipeContext(
            mode="roadmap-v2-node-page",
            skill_dir=SKILL_DIR,
            output_root=root,
            pipeline_dir=root / ".pipeline",
            artifact_store=ArtifactStore(root),
        )

    def test_pipe_manifest_loads(self) -> None:
        manifest = load_pipe_manifest(SKILL_DIR / "pipes" / "roadmap-page" / "01-route-request")
        self.assertEqual(manifest.id, "01-route-request")
        self.assertEqual(manifest.kind, "deterministic")

    def test_llm_parser_rejects_html(self) -> None:
        raw = (FIXTURES / "invalid" / "llm-html-output.json").read_text(encoding="utf-8")
        with self.assertRaises(Exception):
            parse_llm_json(raw)

    def test_pipeline_records_failed_llm_pipe_without_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            runner = PipelineRunner(
                skill_dir=SKILL_DIR,
                mode="roadmap-v2-page",
                output_root=Path(tmp) / "replicacao-no-postgres",
                skip_runtime_preflight=True,
            )
            request = json.loads((FIXTURES / "request-page.json").read_text(encoding="utf-8"))
            run = runner.run({"mode": "roadmap-v2-page", **request})
            self.assertEqual(run.status, "failed")
            self.assertEqual(run.pipe_results[-1].pipe_id, "04-research-plan")
            output_root = Path(tmp) / "replicacao-no-postgres"
            self.assertTrue((output_root / ".pipeline" / "run.json").exists())
            request_path = output_root / ".pipeline" / "llm-requests" / "04-research-plan.json"
            self.assertTrue(request_path.exists())
            request = json.loads(request_path.read_text(encoding="utf-8"))
            self.assertEqual(request["pipe_id"], "04-research-plan")
            self.assertEqual(
                request["expected_output_path"],
                str(output_root / ".pipeline" / "llm-outputs" / "04-research-plan.json"),
            )

    def test_node_page_spec_uses_real_previous_next_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            roadmap = json.loads((FIXTURES / "valid" / "roadmap-spec.json").read_text(encoding="utf-8"))
            first = roadmap["levels"][0]["nodes"][0]
            second = deepcopy(first)
            second.update(
                {
                    "node_id": "basico/02-replica-fisica",
                    "order": 2,
                    "slug": "02-replica-fisica",
                    "title": "Réplica física",
                }
            )
            roadmap["levels"][0]["nodes"].append(second)

            node = json.loads((FIXTURES / "valid" / "node-spec.json").read_text(encoding="utf-8"))
            node["next_node_id"] = "basico/02-replica-fisica"

            output = build_node_page_spec(
                {"roadmap_spec": roadmap, "node_spec": node},
                self.context(root),
            )
            navigation = next(block for block in output["page_spec"]["blocks"] if block["id"] == "navigation")
            next_link = next(item for item in navigation["items"] if item["rel"] == "next")
            self.assertEqual(next_link["href"], "../02-replica-fisica/node.html")


if __name__ == "__main__":
    unittest.main()
