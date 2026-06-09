from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .result import stable_hash


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_pipe_snapshot(
    pipeline_dir: Path,
    pipe_id: str,
    input_data: dict[str, Any],
    output_data: dict[str, Any] | None,
    result: dict[str, Any],
) -> None:
    pipe_dir = pipeline_dir / "pipes" / pipe_id
    pipe_dir.mkdir(parents=True, exist_ok=True)
    (pipe_dir / "input.json").write_text(
        json.dumps(input_data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if output_data is not None:
        (pipe_dir / "output.json").write_text(
            json.dumps(output_data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    result = {
        **result,
        "recorded_at": utc_now(),
        "input_hash": stable_hash(input_data),
        "output_hash": stable_hash(output_data) if output_data is not None else None,
    }
    (pipe_dir / "result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
