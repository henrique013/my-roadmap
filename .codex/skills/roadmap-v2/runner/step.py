from __future__ import annotations

import importlib.util
import importlib
import json
import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator

from .errors import ContractValidationError, RenderFailedError
from .llm import load_fixture_output, load_handoff_output, write_llm_request
from .manifest import PipeManifest, load_pipe_manifest
from .paths import resolve_runtime_paths
from .result import PipeContext, PipeExecution


def load_json_schema(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_schema(schema_path: Path, data: dict[str, Any]) -> None:
    schema = load_json_schema(schema_path)
    errors = sorted(Draft202012Validator(schema).iter_errors(data), key=lambda err: err.path)
    if errors:
        message = "; ".join(f"{list(err.path)}: {err.message}" for err in errors)
        raise ContractValidationError(message)


def load_python_callable(path: Path, function_name: str) -> Callable[[dict[str, Any], PipeContext], dict[str, Any]]:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot import pipe action: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    action = getattr(module, function_name)
    return action


def load_dotted_callable(reference: str) -> Callable[..., Any]:
    _, module_name, function_name = reference.split(":", 2)
    module = importlib.import_module(module_name)
    return getattr(module, function_name)


class PipeExecutor:
    def __init__(self, pipe_dir: Path) -> None:
        self.pipe_dir = pipe_dir
        self.manifest: PipeManifest = load_pipe_manifest(pipe_dir)

    def execute(self, input_data: dict[str, Any], context: PipeContext) -> PipeExecution:
        execution = PipeExecution(pipe_id=self.manifest.id, input_data=input_data)
        validate_schema(self.pipe_dir / self.manifest.input, input_data)
        started = time.monotonic()
        last_error: Exception | None = None

        for attempt in range(1, self.manifest.retry.max_attempts + 1):
            execution.attempts = attempt
            try:
                output_data = self._run_action(input_data, context)
                validate_schema(self.pipe_dir / self.manifest.output, output_data)
                validation_action = self._load_optional_validation()
                if validation_action is not None:
                    validation_action(output_data, context)
                execution.output_data = output_data
                execution.duration_ms = int((time.monotonic() - started) * 1000)
                return execution
            except Exception as exc:  # noqa: BLE001 - mapped by runner into structured result.
                last_error = exc
                if self.manifest.retry.on_fail != "repair_same_scope":
                    break

        execution.duration_ms = int((time.monotonic() - started) * 1000)
        if last_error is not None:
            raise last_error
        raise ContractValidationError(f"pipe {self.manifest.id} failed without error")

    def _run_action(self, input_data: dict[str, Any], context: PipeContext) -> dict[str, Any]:
        if self.manifest.kind == "llm":
            if context.llm_fixtures_dir is not None:
                return {**input_data, **load_fixture_output(context.llm_fixtures_dir, self.manifest.id)}
            output_path = (context.llm_outputs_dir or context.pipeline_dir / "llm-outputs") / f"{self.manifest.id}.json"
            write_llm_request(
                context.pipeline_dir / "llm-requests",
                self.manifest.id,
                self.pipe_dir / self.manifest.action,
                self.pipe_dir / self.manifest.input,
                self.pipe_dir / self.manifest.output,
                input_data,
                output_path,
            )
            return {**input_data, **load_handoff_output(context.llm_outputs_dir, self.manifest.id)}
        if self.manifest.kind == "external-tool":
            return self._run_external(input_data, context)
        if self.manifest.action.startswith("python:"):
            action = load_dotted_callable(self.manifest.action)
            return action(input_data, context)
        action_path, function_name = self._parse_python_action()
        action = load_python_callable(action_path, function_name)
        return action(input_data, context)

    def _parse_python_action(self) -> tuple[Path, str]:
        if ":" in self.manifest.action:
            path_text, function_name = self.manifest.action.split(":", 1)
        else:
            path_text, function_name = self.manifest.action, "run"
        return self.pipe_dir / path_text, function_name

    def _load_optional_validation(self) -> Callable[[dict[str, Any], PipeContext], None] | None:
        if self.manifest.validation == "none":
            return None
        if self.manifest.validation.startswith("python:"):
            return load_dotted_callable(self.manifest.validation)
        path_text, function_name = (
            self.manifest.validation.split(":", 1)
            if ":" in self.manifest.validation
            else (self.manifest.validation, "validate")
        )
        validation_path = self.pipe_dir / path_text
        if not validation_path.exists():
            return None
        return load_python_callable(validation_path, function_name)

    def _run_external(self, input_data: dict[str, Any], context: PipeContext) -> dict[str, Any]:
        if self.manifest.action != "astro-render":
            raise RenderFailedError(f"unsupported external action: {self.manifest.action}")
        page_spec_path = context.output_root / input_data["page_spec_path"]
        paths = resolve_runtime_paths(context.skill_dir)
        render_dir = paths.pipeline_render_dir(context.output_root, self.manifest.id)
        work_dir = paths.pipeline_work_dir(context.output_root, self.manifest.id)
        render_dir.mkdir(parents=True, exist_ok=True)
        web_dir = context.skill_dir / "web"
        env = {
            **os.environ,
            "ASTRO_TELEMETRY_DISABLED": "1",
            "PAGE_SPEC_PATH": str(page_spec_path),
            "PLAYWRIGHT_BROWSERS_PATH": str(paths.browsers_dir),
            "ROADMAP_V2_NODE_MODULES": str(paths.node_modules),
            "ROADMAP_V2_PIPELINE_RENDER": "1",
            "ROADMAP_RENDERER_DIR": str(web_dir),
            "RENDER_OUTPUT_DIR": str(render_dir),
            "RENDER_WORK_DIR": str(work_dir),
            "ASTRO_CACHE_DIR": str(work_dir / ".astro-cache"),
            "VITE_CACHE_DIR": str(work_dir / ".vite-cache"),
        }
        node_bin = shutil.which("node") or "node"
        result = subprocess.run(
            [node_bin, str(web_dir / "scripts" / "build.mjs")],
            cwd=paths.node_root,
            env=env,
            check=False,
            capture_output=True,
            text=True,
        )
        (render_dir / "astro.stdout.log").write_text(result.stdout, encoding="utf-8")
        (render_dir / "astro.stderr.log").write_text(result.stderr, encoding="utf-8")
        if result.returncode != 0:
            raise RenderFailedError(result.stderr.strip() or "Astro render failed")
        html_path = render_dir / "index.html"
        rewrite_root_relative_asset_paths(html_path)
        return {
            **input_data,
            "rendered_html_path": str(html_path.relative_to(context.output_root)),
            "renderer": "astro",
        }


def rewrite_root_relative_asset_paths(html_path: Path) -> None:
    html = html_path.read_text(encoding="utf-8")
    html = html.replace('href="/_astro/', 'href="_astro/')
    html = html.replace('src="/_astro/', 'src="_astro/')
    html = html.replace('href="/vendor/', 'href="vendor/')
    html = html.replace('src="/vendor/', 'src="vendor/')
    html_path.write_text(html, encoding="utf-8")
