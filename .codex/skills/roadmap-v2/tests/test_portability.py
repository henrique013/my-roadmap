from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from runner.paths import resolve_runtime_paths


def file_state(root: Path) -> dict[str, str]:
    state: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        state[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return state


class PortabilityTests(unittest.TestCase):
    def test_skill_package_does_not_reference_source_tree(self) -> None:
        forbidden = "/".join(["templates", "skills-local"])
        offenders: list[str] = []
        for path in sorted(SKILL_DIR.rglob("*")):
            if not path.is_file() or path.suffix in {".pyc", ".png"}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if forbidden in text:
                offenders.append(path.relative_to(SKILL_DIR).as_posix())
        self.assertEqual(offenders, [])

    def test_skill_package_has_no_generated_renderer_dependencies(self) -> None:
        self.assertFalse((SKILL_DIR / "web" / "node_modules").exists())
        self.assertFalse((SKILL_DIR / "web" / ".astro").exists())
        self.assertFalse((SKILL_DIR / "web" / "dist").exists())
        self.assertFalse((SKILL_DIR / "web" / "dist.work").exists())

    def test_webawesome_assets_are_not_generated_under_skill_public_dir(self) -> None:
        self.assertFalse((SKILL_DIR / "web" / "public" / "vendor" / "webawesome" / "dist-cdn").exists())

    def test_fixture_pipeline_does_not_write_under_installed_skill_package(self) -> None:
        paths = resolve_runtime_paths(SKILL_DIR)
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            installed_skill = tmp_path / "consumer" / ".codex" / "skills" / "roadmap-v2"
            shutil.copytree(
                SKILL_DIR,
                installed_skill,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "node_modules", ".astro", "dist", "dist.work"),
            )
            before = file_state(installed_skill)
            output_root = tmp_path / "outputs" / "replicacao-no-postgres"
            command = [
                str(paths.python_executable),
                "-B",
                str(installed_skill / "scripts" / "run_pipeline.py"),
                "--mode",
                "roadmap-v2-page",
                "--input",
                str(installed_skill / "tests" / "fixtures" / "request-page.json"),
                "--output-root",
                str(output_root),
                "--llm-fixtures-dir",
                str(installed_skill / "tests" / "fixtures" / "llm-page"),
            ]
            env = {
                **os.environ,
                "ROADMAP_V2_RUNTIME_HOME": str(paths.runtime_home),
                "ROADMAP_V2_NO_PYTHON_REEXEC": "1",
            }
            result = subprocess.run(command, check=False, env=env, capture_output=True, text=True)
            if result.returncode != 0:
                self.fail(result.stderr or result.stdout)
            self.assertEqual(json.loads((output_root / ".pipeline" / "run.json").read_text(encoding="utf-8"))["status"], "success")
            self.assertEqual(file_state(installed_skill), before)


if __name__ == "__main__":
    unittest.main()
