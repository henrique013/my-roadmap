from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .errors import LlmOutputInvalidError


def parse_llm_json(raw: str) -> dict[str, Any]:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise LlmOutputInvalidError(f"LLM output is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise LlmOutputInvalidError("LLM output must be a JSON object")
    reject_free_form_html(data)
    return data


def reject_free_form_html(data: Any) -> None:
    if isinstance(data, str):
        lowered = data.lower()
        if "<html" in lowered or "<body" in lowered or "<script" in lowered:
            raise LlmOutputInvalidError("LLM output contains free-form final HTML")
    elif isinstance(data, dict):
        for value in data.values():
            reject_free_form_html(value)
    elif isinstance(data, list):
        for value in data:
            reject_free_form_html(value)


def load_fixture_output(fixtures_dir: Path | None, pipe_id: str) -> dict[str, Any]:
    if fixtures_dir is None:
        raise LlmOutputInvalidError(f"LLM output required for pipe {pipe_id}")
    path = fixtures_dir / f"{pipe_id}.json"
    if not path.exists():
        raise LlmOutputInvalidError(f"missing LLM fixture output for pipe {pipe_id}: {path}")
    return parse_llm_json(path.read_text(encoding="utf-8"))


def write_llm_request(
    requests_dir: Path,
    pipe_id: str,
    prompt_path: Path,
    input_schema_path: Path,
    output_schema_path: Path,
    input_data: dict[str, Any],
    expected_output_path: Path,
) -> Path:
    requests_dir.mkdir(parents=True, exist_ok=True)
    request_path = requests_dir / f"{pipe_id}.json"
    request = {
        "pipe_id": pipe_id,
        "prompt": prompt_path.read_text(encoding="utf-8"),
        "input_schema": json.loads(input_schema_path.read_text(encoding="utf-8")),
        "output_schema": json.loads(output_schema_path.read_text(encoding="utf-8")),
        "input": input_data,
        "expected_output_path": str(expected_output_path),
    }
    request_path.write_text(json.dumps(request, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return request_path


def load_handoff_output(outputs_dir: Path | None, pipe_id: str) -> dict[str, Any]:
    if outputs_dir is None:
        raise LlmOutputInvalidError(f"LLM output required for pipe {pipe_id}")
    path = outputs_dir / f"{pipe_id}.json"
    if not path.exists():
        raise LlmOutputInvalidError(
            f"missing LLM handoff output for pipe {pipe_id}: write structured JSON to {path}"
        )
    return parse_llm_json(path.read_text(encoding="utf-8"))
