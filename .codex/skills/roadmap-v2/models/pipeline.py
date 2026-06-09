from __future__ import annotations

from typing import Literal

from pydantic import Field

from .base import SCHEMA_VERSION, StrictModel


PipeStatus = Literal["pending", "success", "failed", "skipped"]


class ArtifactRef(StrictModel):
    path: str = Field(min_length=1)
    sha256: str | None = None


class PipeResult(StrictModel):
    pipe_id: str = Field(min_length=1)
    status: PipeStatus
    attempts: int = Field(default=1, ge=0)
    duration_ms: int = Field(default=0, ge=0)
    input_hash: str | None = None
    output_hash: str | None = None
    read_artifacts: list[ArtifactRef] = Field(default_factory=list)
    written_artifacts: list[ArtifactRef] = Field(default_factory=list)
    error_type: str | None = None
    error_message: str | None = None


class PipelineRun(StrictModel):
    schema_version: str = SCHEMA_VERSION
    run_id: str = Field(min_length=1)
    mode: Literal["roadmap-v2-page", "roadmap-v2-node-page"]
    status: Literal["success", "failed"]
    output_root: str = Field(min_length=1)
    started_at: str = Field(min_length=1)
    finished_at: str | None = None
    pipe_results: list[PipeResult] = Field(default_factory=list)
