from __future__ import annotations

from pathlib import Path
from typing import Any
import json

from pydantic import BaseModel, ConfigDict


SCHEMA_VERSION = "roadmap-v2.0"


class StrictModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
    )


def read_json_model(path: Path, model_type: type[StrictModel]) -> StrictModel:
    return model_type.model_validate_json(path.read_text(encoding="utf-8"))


def dump_json(data: StrictModel | dict[str, Any]) -> str:
    if isinstance(data, StrictModel):
        return data.model_dump_json(indent=2, exclude_none=True)
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)
