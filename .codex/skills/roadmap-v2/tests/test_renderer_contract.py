from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from runner.paths import resolve_runtime_paths

WEB_DIR = SKILL_DIR / "web"
FIXTURES = SKILL_DIR / "tests" / "fixtures"


class RendererContractTests(unittest.TestCase):
    def test_pagespec_to_html(self) -> None:
        paths = resolve_runtime_paths(SKILL_DIR)
        with tempfile.TemporaryDirectory() as tmp:
            render_dir = Path(tmp) / "render"
            work_dir = Path(tmp) / "work"
            env = {
                **__import__("os").environ,
                "ASTRO_TELEMETRY_DISABLED": "1",
                "PAGE_SPEC_PATH": str(FIXTURES / "valid" / "page-spec-roadmap.json"),
                "PLAYWRIGHT_BROWSERS_PATH": str(paths.browsers_dir),
                "ROADMAP_RENDERER_DIR": str(WEB_DIR),
                "ROADMAP_V2_NODE_MODULES": str(paths.node_modules),
                "ROADMAP_V2_PIPELINE_RENDER": "1",
                "RENDER_OUTPUT_DIR": str(render_dir),
                "RENDER_WORK_DIR": str(work_dir),
                "ASTRO_CACHE_DIR": str(work_dir / ".astro-cache"),
                "VITE_CACHE_DIR": str(work_dir / ".vite-cache"),
            }
            result = subprocess.run(["node", str(WEB_DIR / "scripts" / "build.mjs")], cwd=WEB_DIR, env=env, check=False)
            self.assertEqual(result.returncode, 0)
            self.assertTrue((render_dir / "index.html").exists())
            self.assertTrue((render_dir / "vendor" / "webawesome" / "dist-cdn" / "webawesome.loader.js").exists())


if __name__ == "__main__":
    unittest.main()
