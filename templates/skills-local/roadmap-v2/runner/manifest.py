from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import Field, model_validator

from models.base import StrictModel


class RetryPolicy(StrictModel):
    max_attempts: int = Field(default=1, ge=1)
    on_fail: Literal["fail", "repair_same_scope"] = "fail"


class ArtifactPolicy(StrictModel):
    reads: list[str] = Field(default_factory=list)
    writes: list[str] = Field(default_factory=list)


class PipeManifest(StrictModel):
    id: str = Field(min_length=1)
    kind: Literal["deterministic", "llm", "external-tool", "human-checkpoint"]
    input: str = Field(min_length=1)
    action: str = Field(min_length=1)
    validation: str = Field(min_length=1)
    output: str = Field(min_length=1)
    retry: RetryPolicy = Field(default_factory=RetryPolicy)
    artifacts: ArtifactPolicy = Field(default_factory=ArtifactPolicy)
    blocks_pipeline_on_fail: bool = True

    @model_validator(mode="after")
    def manifest_paths_are_relative(self) -> "PipeManifest":
        for value in [self.input, self.output]:
            if value.startswith("/") or ".." in Path(value).parts:
                raise ValueError(f"manifest path must be relative and local: {value}")
        for value in [self.action, self.validation]:
            if value in {"none", "astro-render"} or value.startswith("python:"):
                continue
            if value.startswith("/") or ".." in Path(value).parts:
                raise ValueError(f"manifest path must be relative and local: {value}")
        return self


def load_pipe_manifest(pipe_dir: Path) -> PipeManifest:
    manifest_path = pipe_dir / "pipe.yaml"
    if not manifest_path.exists():
        raise FileNotFoundError(f"missing pipe manifest: {manifest_path}")
    data = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    return PipeManifest.model_validate(data)
