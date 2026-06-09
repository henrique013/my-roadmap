from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from rules.accentuation import find_accentuation_issues
from rules.ids import build_node_id, validate_unique_node_ids
from rules.navigation import validate_navigation_links
from rules.paths import safe_child_path
from rules.slugs import normalize_slug, validate_slug


class RuleTests(unittest.TestCase):
    def test_slug_normalization_and_validation(self) -> None:
        self.assertEqual(normalize_slug("Replicação no Postgres"), "replicacao-no-postgres")
        self.assertEqual(validate_slug("01-modelo-mental"), "01-modelo-mental")
        with self.assertRaises(ValueError):
            validate_slug("../bad")

    def test_node_ids_are_stable_and_unique(self) -> None:
        self.assertEqual(build_node_id("basico", "01-modelo"), "basico/01-modelo")
        validate_unique_node_ids(["basico/01-a", "basico/02-b"])
        with self.assertRaises(ValueError):
            validate_unique_node_ids(["basico/01-a", "basico/01-a"])

    def test_paths_cannot_escape_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(safe_child_path(root, "a", "b").parent, root / "a")
            with self.assertRaises(ValueError):
                safe_child_path(root, "..", "escape")

    def test_navigation_rejects_absolute_links(self) -> None:
        validate_navigation_links([{"href": "nodes/basico/01-a/node.html"}])
        with self.assertRaises(ValueError):
            validate_navigation_links([{"href": "https://example.com"}])

    def test_accentuation_flags_plain_portuguese_words(self) -> None:
        issues = find_accentuation_issues("nivel basico nao tecnico")
        self.assertTrue(any("básico" in issue for issue in issues))
        self.assertTrue(any("não" in issue for issue in issues))


if __name__ == "__main__":
    unittest.main()
