#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

sys.dont_write_bytecode = True

SKILL_DIR = Path(__file__).resolve().parents[1]
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from runner.paths import resolve_repo_root  # noqa: E402

DEFAULT_IMAGE = "roadmap-v2-runner:local"
CONTAINER_ROADMAPS_ROOT = Path("/workspace/.tmp/roadmaps-v2")
CONTAINER_OUTPUT_ROOT = Path("/workspace/output")
CONTAINER_INPUT_ROOT = Path("/workspace/input")
CONTAINER_FIXTURES_ROOT = Path("/workspace/fixtures")
CONTAINER_LLM_OUTPUTS_ROOT = Path("/workspace/llm-outputs")


@dataclass(frozen=True)
class BindMount:
    source: Path
    target: Path
    readonly: bool = False

    def docker_arg(self) -> str:
        mode = ",readonly" if self.readonly else ""
        return f"type=bind,source={self.source},target={self.target}{mode}"


def require_docker() -> str:
    docker = shutil.which("docker")
    if docker is None:
        raise SystemExit("Docker CLI not found. Build and run the roadmap-v2-runner image before using roadmap-v2.")
    return docker


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def map_path(path: Path, mounts: list[BindMount]) -> Path | None:
    resolved = path.resolve()
    candidates = sorted(
        [mount for mount in mounts if is_relative_to(resolved, mount.source)],
        key=lambda mount: len(mount.source.resolve().parts),
        reverse=True,
    )
    if not candidates:
        return None
    mount = candidates[0]
    return mount.target / resolved.relative_to(mount.source.resolve())


def add_file_mount(path: Path, mounts: list[BindMount], target_root: Path, filename: str) -> Path:
    mapped = map_path(path, mounts)
    if mapped is not None:
        return mapped
    target = target_root / filename
    mounts.append(BindMount(path.resolve(), target, readonly=True))
    return target


def add_dir_mount(path: Path, mounts: list[BindMount], target: Path, readonly: bool) -> Path:
    mapped = map_path(path, mounts)
    if mapped is not None:
        return mapped
    mounts.append(BindMount(path.resolve(), target, readonly=readonly))
    return target


def build_mounts(repo_root: Path, output_root: Path, input_path: Path) -> tuple[list[BindMount], Path, Path]:
    mounts: list[BindMount] = []
    roadmaps_root = repo_root / ".tmp" / "roadmaps-v2"
    output_root.mkdir(parents=True, exist_ok=True)

    if output_root == roadmaps_root or is_relative_to(output_root, roadmaps_root):
        roadmaps_root.mkdir(parents=True, exist_ok=True)
        mounts.append(BindMount(roadmaps_root.resolve(), CONTAINER_ROADMAPS_ROOT))
        container_output = CONTAINER_ROADMAPS_ROOT / output_root.resolve().relative_to(roadmaps_root.resolve())
    else:
        mounts.append(BindMount(output_root.resolve(), CONTAINER_OUTPUT_ROOT))
        container_output = CONTAINER_OUTPUT_ROOT

    container_input = add_file_mount(input_path, mounts, CONTAINER_INPUT_ROOT, "request.json")
    return mounts, container_input, container_output


def main() -> int:
    parser = argparse.ArgumentParser(description="Run roadmap-v2 through the roadmap-v2-runner Docker image.")
    parser.add_argument("--mode", required=True, choices=["roadmap-v2-page", "roadmap-v2-node-page"])
    parser.add_argument("--input", required=True, help="Path to request JSON.")
    parser.add_argument("--output-root", required=True, help="Resolved .tmp/roadmaps-v2/<slug> output root.")
    parser.add_argument("--llm-fixtures-dir", help="Directory with <pipe-id>.json fixture outputs for LLM pipes.")
    parser.add_argument("--llm-outputs-dir", help="Directory with agent-produced <pipe-id>.json outputs for LLM pipes.")
    parser.add_argument(
        "--image",
        default=os.environ.get("ROADMAP_V2_IMAGE", DEFAULT_IMAGE),
        help=f"Docker image to run. Defaults to ROADMAP_V2_IMAGE or {DEFAULT_IMAGE}.",
    )
    parser.add_argument(
        "--network",
        default=os.environ.get("ROADMAP_V2_DOCKER_NETWORK", "none"),
        help="Docker network mode for runtime execution. Defaults to none.",
    )
    parser.add_argument("--no-read-only", action="store_true", help="Do not run the container root filesystem read-only.")
    args = parser.parse_args()

    docker = require_docker()
    repo_root = resolve_repo_root(SKILL_DIR)
    input_path = Path(args.input).expanduser().resolve()
    output_root = Path(args.output_root).expanduser().resolve()

    if not input_path.is_file():
        raise SystemExit(f"roadmap-v2 input JSON not found: {input_path}")

    mounts, container_input, container_output = build_mounts(repo_root, output_root, input_path)

    container_llm_fixtures: Path | None = None
    if args.llm_fixtures_dir:
        fixtures_dir = Path(args.llm_fixtures_dir).expanduser().resolve()
        if not fixtures_dir.is_dir():
            raise SystemExit(f"LLM fixtures directory not found: {fixtures_dir}")
        container_llm_fixtures = add_dir_mount(fixtures_dir, mounts, CONTAINER_FIXTURES_ROOT, readonly=True)

    container_llm_outputs: Path | None = None
    if args.llm_outputs_dir:
        llm_outputs_dir = Path(args.llm_outputs_dir).expanduser().resolve()
        llm_outputs_dir.mkdir(parents=True, exist_ok=True)
        container_llm_outputs = add_dir_mount(llm_outputs_dir, mounts, CONTAINER_LLM_OUTPUTS_ROOT, readonly=False)

    uid = os.getuid()
    gid = os.getgid()
    command = [
        docker,
        "run",
        "--rm",
        "--network",
        args.network,
        "--user",
        f"{uid}:{gid}",
        "--workdir",
        "/workspace",
        "--tmpfs",
        "/tmp:rw,exec,nosuid,size=1024m,mode=1777",
        "-e",
        "HOME=/tmp",
        "-e",
        "XDG_CACHE_HOME=/tmp/.cache",
        "-e",
        "TMPDIR=/tmp",
        "-e",
        "ASTRO_TELEMETRY_DISABLED=1",
        "-e",
        "PLAYWRIGHT_BROWSERS_PATH=0",
        "-e",
        "PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium",
        "-e",
        "ROADMAP_V2_RUNTIME_HOME=/opt/roadmap-v2/runtime",
        "-e",
        f"ROADMAP_V2_VISUAL_STRICT={os.environ.get('ROADMAP_V2_VISUAL_STRICT', '1')}",
    ]
    if not args.no_read_only:
        command.append("--read-only")
    for mount in mounts:
        command.extend(["--mount", mount.docker_arg()])

    command.extend(
        [
            args.image,
            "--mode",
            args.mode,
            "--input",
            str(container_input),
            "--output-root",
            str(container_output),
        ]
    )
    if container_llm_fixtures is not None:
        command.extend(["--llm-fixtures-dir", str(container_llm_fixtures)])
    if container_llm_outputs is not None:
        command.extend(["--llm-outputs-dir", str(container_llm_outputs)])

    return subprocess.run(command, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
