from __future__ import annotations

from pathlib import Path


def safe_child_path(root: Path, *parts: str) -> Path:
    root_resolved = root.resolve()
    candidate = root_resolved.joinpath(*parts).resolve()
    if candidate != root_resolved and root_resolved not in candidate.parents:
        raise ValueError(f"path escapes output root: {candidate}")
    return candidate


def ensure_relative_artifact(path: str) -> str:
    if path.startswith("/") or "://" in path or "\\" in path:
        raise ValueError(f"artifact path must be safe and relative: {path!r}")
    if any(part in {"", ".", ".."} for part in Path(path).parts):
        raise ValueError(f"artifact path contains unsafe segment: {path!r}")
    return path
