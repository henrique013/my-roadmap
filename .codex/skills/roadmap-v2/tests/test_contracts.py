from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from models.node_spec import NodeSpec
from models.page_spec import PageSpec
from models.pipeline import PipelineRun
from models.research_pack import ResearchPack
from models.roadmap_spec import RoadmapSpec


FIXTURES = SKILL_DIR / "tests" / "fixtures"


class ContractTests(unittest.TestCase):
    def load(self, relative: str) -> dict:
        return json.loads((FIXTURES / relative).read_text(encoding="utf-8"))

    def test_valid_contract_fixtures(self) -> None:
        ResearchPack.model_validate(self.load("valid/research-pack.json"))
        RoadmapSpec.model_validate(self.load("valid/roadmap-spec.json"))
        NodeSpec.model_validate(self.load("valid/node-spec.json"))
        PageSpec.model_validate(self.load("valid/page-spec-roadmap.json"))
        PageSpec.model_validate(self.load("valid/page-spec-node.json"))
        PipelineRun.model_validate(self.load("valid/pipeline-run.json"))

    def test_invalid_roadmap_duplicate_node_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            RoadmapSpec.model_validate(self.load("invalid/roadmap-spec-duplicate-node.json"))

    def test_extra_fields_are_rejected(self) -> None:
        data = self.load("valid/page-spec-roadmap.json")
        data["unexpected"] = True
        with self.assertRaises(ValueError):
            PageSpec.model_validate(data)


if __name__ == "__main__":
    unittest.main()
