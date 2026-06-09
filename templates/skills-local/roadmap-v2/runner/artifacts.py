from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from rules.paths import safe_child_path


class ArtifactStore:
    def __init__(self, output_root: Path) -> None:
        self.output_root = output_root.resolve()

    def path(self, relative_path: str) -> Path:
        return safe_child_path(self.output_root, relative_path)

    def read_json(self, relative_path: str) -> Any:
        return json.loads(self.path(relative_path).read_text(encoding="utf-8"))

    def write_json(self, relative_path: str, data: Any) -> Path:
        path = self.path(relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return path

    def read_text(self, relative_path: str) -> str:
        return self.path(relative_path).read_text(encoding="utf-8")

    def write_text(self, relative_path: str, data: str) -> Path:
        path = self.path(relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(data, encoding="utf-8")
        return path
