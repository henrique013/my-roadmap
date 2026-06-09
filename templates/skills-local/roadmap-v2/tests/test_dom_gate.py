from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from runner.artifacts import ArtifactStore
from runner.errors import DomValidationError
from runner.result import PipeContext
from scripts.pipe_actions import copy_render_assets, validate_dom


class DomGateTests(unittest.TestCase):
    def context(self, root: Path) -> PipeContext:
        return PipeContext(
            mode="roadmap-v2-page",
            skill_dir=SKILL_DIR,
            output_root=root,
            pipeline_dir=root / ".pipeline",
            artifact_store=ArtifactStore(root),
        )

    def test_dom_gate_rejects_unsupported_webawesome_component(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            html_path = root / ".pipeline" / "render" / "index.html"
            html_path.parent.mkdir(parents=True)
            html_path.write_text("<html><body><wa-unknown>Bad</wa-unknown></body></html>", encoding="utf-8")
            with self.assertRaises(DomValidationError):
                validate_dom({"rendered_html_path": ".pipeline/render/index.html"}, self.context(root))

    def test_dom_gate_accepts_allowed_component(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            html_path = root / ".pipeline" / "render" / "index.html"
            html_path.parent.mkdir(parents=True)
            html_path.write_text(
                "<html><body><wa-card>Texto com conteúdo técnico suficiente.</wa-card></body></html>",
                encoding="utf-8",
            )
            validate_dom({"rendered_html_path": ".pipeline/render/index.html"}, self.context(root))

    def test_dom_gate_accepts_external_reference_link(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            html_path = root / ".pipeline" / "render" / "index.html"
            html_path.parent.mkdir(parents=True)
            html_path.write_text(
                '<html><body><a href="https://example.com">Referência externa confiável</a></body></html>',
                encoding="utf-8",
            )
            validate_dom({"rendered_html_path": ".pipeline/render/index.html"}, self.context(root))

    def test_dom_gate_rejects_external_stylesheet(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            html_path = root / ".pipeline" / "render" / "index.html"
            html_path.parent.mkdir(parents=True)
            html_path.write_text(
                '<html><head><link rel="stylesheet" href="https://example.com/app.css"></head><body>Texto técnico suficiente.</body></html>',
                encoding="utf-8",
            )
            with self.assertRaises(DomValidationError):
                validate_dom({"rendered_html_path": ".pipeline/render/index.html"}, self.context(root))

    def test_copy_render_assets_promotes_static_directories(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            render_dir = root / "render"
            final_dir = root / "final"
            (render_dir / "_astro").mkdir(parents=True)
            (render_dir / "vendor").mkdir()
            (render_dir / "_astro" / "style.css").write_text("body{}", encoding="utf-8")
            (render_dir / "vendor" / "webawesome.js").write_text("export {}", encoding="utf-8")
            (render_dir / "index.html").write_text("<html></html>", encoding="utf-8")
            final_dir.mkdir()

            copy_render_assets(render_dir, final_dir)

            self.assertTrue((final_dir / "_astro" / "style.css").exists())
            self.assertTrue((final_dir / "vendor" / "webawesome.js").exists())
            self.assertFalse((final_dir / "index.html").exists())


if __name__ == "__main__":
    unittest.main()
