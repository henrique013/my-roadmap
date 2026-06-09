from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .artifacts import ArtifactStore


def stable_hash(data: Any) -> str:
    encoded = json.dumps(data, ensure_ascii=False, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass
class PipeContext:
    mode: str
    skill_dir: Path
    output_root: Path
    pipeline_dir: Path
    artifact_store: ArtifactStore
    llm_fixtures_dir: Path | None = None
    llm_outputs_dir: Path | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PipeExecution:
    pipe_id: str
    input_data: dict[str, Any]
    output_data: dict[str, Any] | None = None
    attempts: int = 0
    duration_ms: int = 0
    read_artifacts: list[Path] = field(default_factory=list)
    written_artifacts: list[Path] = field(default_factory=list)
