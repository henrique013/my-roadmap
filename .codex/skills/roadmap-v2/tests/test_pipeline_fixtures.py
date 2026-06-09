from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from runner.pipeline import PipelineRunner


FIXTURES = SKILL_DIR / "tests" / "fixtures"


class PipelineFixtureTests(unittest.TestCase):
    def test_overview_pipeline_fixture_completes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp) / "replicacao-no-postgres"
            request = json.loads((FIXTURES / "request-page.json").read_text(encoding="utf-8"))
            runner = PipelineRunner(
                skill_dir=SKILL_DIR,
                mode="roadmap-v2-page",
                output_root=output_root,
                llm_fixtures_dir=FIXTURES / "llm-page",
            )
            run = runner.run({"mode": "roadmap-v2-page", **request})
            self.assertEqual(run.status, "success")
            self.assertTrue((output_root / "roadmap.html").exists())
            self.assertFalse((output_root.parent.parent / "roadmaps").exists())

    def test_node_pipeline_fixture_completes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp) / "replicacao-no-postgres"
            output_root.mkdir(parents=True)
            shutil.copyfile(FIXTURES / "valid" / "roadmap-spec.json", output_root / "roadmap-spec.json")
            request = json.loads((FIXTURES / "request-node.json").read_text(encoding="utf-8"))
            runner = PipelineRunner(
                skill_dir=SKILL_DIR,
                mode="roadmap-v2-node-page",
                output_root=output_root,
                llm_fixtures_dir=FIXTURES / "llm-node",
            )
            run = runner.run({"mode": "roadmap-v2-node-page", **request})
            self.assertEqual(run.status, "success")
            self.assertTrue((output_root / "nodes" / "basico" / "01-modelo-mental-da-replicacao" / "node.html").exists())


if __name__ == "__main__":
    unittest.main()
