from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


RUNTIME_HOME_ENV = "ROADMAP_V2_RUNTIME_HOME"


@dataclass(frozen=True)
class RuntimePaths:
    skill_dir: Path
    repo_root: Path
    runtime_home: Path
    python_venv: Path
    python_executable: Path
    node_root: Path
    node_modules: Path
    browsers_dir: Path
    cache_dir: Path
    renderer_dir: Path

    def pipeline_work_dir(self, output_root: Path, pipe_id: str) -> Path:
        return output_root.resolve() / ".pipeline" / "work" / pipe_id

    def pipeline_render_dir(self, output_root: Path, pipe_id: str) -> Path:
        return output_root.resolve() / ".pipeline" / "render" / pipe_id


def resolve_repo_root(skill_dir: Path) -> Path:
    resolved = skill_dir.resolve()
    parts = resolved.parts
    for index, part in enumerate(parts):
        if part == ".codex" and index + 1 < len(parts) and parts[index + 1] == "skills":
            return Path(*parts[:index]).resolve()
        if part == "templates" and index + 1 < len(parts) and parts[index + 1] in {"skills", "skills-local"}:
            return Path(*parts[:index]).resolve()
    for candidate in [resolved, *resolved.parents]:
        if (candidate / ".git").exists() or (candidate / "agents-compose.yml").exists():
            return candidate.resolve()
    return resolved.parents[2].resolve() if len(resolved.parents) >= 3 else resolved


def resolve_runtime_home(skill_dir: Path, repo_root: Path | None = None) -> Path:
    root = repo_root or resolve_repo_root(skill_dir)
    configured = os.environ.get(RUNTIME_HOME_ENV)
    if configured:
        path = Path(configured).expanduser()
        return (root / path).resolve() if not path.is_absolute() else path.resolve()
    return (root / ".codex-runtime" / "roadmap-v2").resolve()


def resolve_runtime_paths(skill_dir: Path) -> RuntimePaths:
    resolved_skill_dir = skill_dir.resolve()
    repo_root = resolve_repo_root(resolved_skill_dir)
    runtime_home = resolve_runtime_home(resolved_skill_dir, repo_root)
    python_venv = runtime_home / "python"
    python_executable = python_venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    node_root = runtime_home / "node"
    return RuntimePaths(
        skill_dir=resolved_skill_dir,
        repo_root=repo_root,
        runtime_home=runtime_home,
        python_venv=python_venv,
        python_executable=python_executable,
        node_root=node_root,
        node_modules=node_root / "node_modules",
        browsers_dir=runtime_home / "browsers",
        cache_dir=runtime_home / "cache",
        renderer_dir=resolved_skill_dir / "web",
    )


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False
