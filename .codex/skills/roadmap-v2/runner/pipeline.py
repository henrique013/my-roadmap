from __future__ import annotations

import json
import shutil
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from models.pipeline import ArtifactRef, PipelineRun, PipeResult

from .artifacts import ArtifactStore
from .errors import PipelineError
from .graph import PipelineGraph
from .paths import resolve_runtime_paths
from .result import PipeContext, stable_hash
from .snapshots import write_pipe_snapshot
from .step import PipeExecutor


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class PipelineRunner:
    def __init__(
        self,
        skill_dir: Path,
        mode: str,
        output_root: Path,
        llm_fixtures_dir: Path | None = None,
        llm_outputs_dir: Path | None = None,
        skip_runtime_preflight: bool = False,
    ) -> None:
        self.skill_dir = skill_dir.resolve()
        if str(self.skill_dir) not in sys.path:
            sys.path.insert(0, str(self.skill_dir))
        self.mode = mode
        self.output_root = output_root.resolve()
        self.pipeline_dir = self.output_root / ".pipeline"
        self.runtime_paths = resolve_runtime_paths(self.skill_dir)
        self.skip_runtime_preflight = skip_runtime_preflight
        self.context = PipeContext(
            mode=mode,
            skill_dir=self.skill_dir,
            output_root=self.output_root,
            pipeline_dir=self.pipeline_dir,
            artifact_store=ArtifactStore(self.output_root),
            llm_fixtures_dir=llm_fixtures_dir,
            llm_outputs_dir=llm_outputs_dir or self.pipeline_dir / "llm-outputs",
            metadata={"runtime_home": str(self.runtime_paths.runtime_home)},
        )

    def run(self, input_data: dict[str, Any]) -> PipelineRun:
        manifest = self._load_pipeline_manifest()
        pipe_ids = PipelineGraph.from_linear(manifest["pipes"]).ordered()
        self.output_root.mkdir(parents=True, exist_ok=True)
        self.pipeline_dir.mkdir(parents=True, exist_ok=True)

        run = PipelineRun(
            run_id=str(uuid.uuid4()),
            mode=self.mode,  # type: ignore[arg-type]
            status="failed",
            output_root=str(self.output_root),
            started_at=utc_now(),
        )

        current = input_data
        try:
            self._ensure_runtime_ready()
            for pipe_id in pipe_ids:
                pipe_dir = self._resolve_pipe_dir(pipe_id)
                executor = PipeExecutor(pipe_dir)
                execution = executor.execute(current, self.context)
                current = execution.output_data or {}
                pipe_result = PipeResult(
                    pipe_id=pipe_id,
                    status="success",
                    attempts=execution.attempts,
                    duration_ms=execution.duration_ms,
                    input_hash=stable_hash(execution.input_data),
                    output_hash=stable_hash(current),
                    read_artifacts=[ArtifactRef(path=str(path)) for path in execution.read_artifacts],
                    written_artifacts=[ArtifactRef(path=str(path)) for path in execution.written_artifacts],
                )
                run.pipe_results.append(pipe_result)
                write_pipe_snapshot(
                    self.pipeline_dir,
                    pipe_id,
                    execution.input_data,
                    current,
                    pipe_result.model_dump(exclude_none=True),
                )
            run.status = "success"
            return self._finish(run)
        except Exception as exc:  # noqa: BLE001 - persisted as expected pipeline error.
            error_type = exc.code if isinstance(exc, PipelineError) else type(exc).__name__
            failed_pipe = pipe_ids[len(run.pipe_results)] if len(run.pipe_results) < len(pipe_ids) else "unknown"
            pipe_result = PipeResult(
                pipe_id=failed_pipe,
                status="failed",
                attempts=1,
                input_hash=stable_hash(current),
                error_type=error_type,
                error_message=str(exc),
            )
            run.pipe_results.append(pipe_result)
            write_pipe_snapshot(
                self.pipeline_dir,
                failed_pipe,
                current,
                None,
                pipe_result.model_dump(exclude_none=True),
            )
            return self._finish(run)

    def _finish(self, run: PipelineRun) -> PipelineRun:
        run.finished_at = utc_now()
        path = self.pipeline_dir / "run.json"
        path.write_text(run.model_dump_json(indent=2, exclude_none=True) + "\n", encoding="utf-8")
        return run

    def _load_pipeline_manifest(self) -> dict[str, Any]:
        manifest_path = self.skill_dir / "pipelines" / f"{self.mode}.yaml"
        data = json.loads(json.dumps(__import__("yaml").safe_load(manifest_path.read_text(encoding="utf-8"))))
        if not data.get("pipes"):
            raise ValueError(f"pipeline manifest has no pipes: {manifest_path}")
        return data

    def _ensure_runtime_ready(self) -> None:
        if self.skip_runtime_preflight:
            return
        from scripts.preflight import collect_errors  # noqa: PLC0415

        errors = collect_errors(self.skill_dir)
        if errors:
            raise RuntimeError("roadmap-v2 runtime is not ready: " + "; ".join(errors))

    def _resolve_pipe_dir(self, pipe_id: str) -> Path:
        group_by_mode = {
            "roadmap-v2-page": "roadmap-page",
            "roadmap-v2-node-page": "node-page",
        }
        group = group_by_mode.get(self.mode)
        if group is None:
            raise ValueError(f"unknown pipeline mode: {self.mode}")
        candidate = self.skill_dir / "pipes" / group / pipe_id
        if candidate.exists():
            return candidate
        raise FileNotFoundError(f"pipe not found: {group}/{pipe_id}")


def finalize_output(rendered_html_path: Path, final_path: Path) -> None:
    final_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(rendered_html_path, final_path)
