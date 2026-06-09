#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

sys.dont_write_bytecode = True

SKILL_DIR = Path(__file__).resolve().parents[1]
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from runner.paths import RUNTIME_HOME_ENV, RuntimePaths, resolve_runtime_paths  # noqa: E402


def run(command: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> None:
    result = subprocess.run(command, cwd=cwd, env=env, check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def require_file(path: Path, label: str) -> None:
    if not path.is_file():
        raise SystemExit(f"Missing {label}: {path}")


def require_binary(name: str) -> str:
    resolved = shutil.which(name)
    if resolved is None:
        raise SystemExit(f"Missing required binary on PATH: {name}")
    return resolved


def prepare_python(paths: RuntimePaths) -> None:
    requirements = paths.skill_dir / "requirements.txt"
    require_file(requirements, "Python requirements")

    paths.runtime_home.mkdir(parents=True, exist_ok=True)
    if not paths.python_executable.exists():
        print(f"Creating roadmap-v2 Python runtime at {paths.python_venv}")
        run([sys.executable, "-m", "venv", "--without-pip", str(paths.python_venv)])

    prepare_pip(paths)

    print(f"Installing roadmap-v2 Python dependencies from {requirements}")
    run([str(paths.python_executable), "-m", "pip", "install", "-r", str(requirements)])


def pip_is_ready(paths: RuntimePaths) -> bool:
    result = subprocess.run(
        [str(paths.python_executable), "-m", "pip", "--version"],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def prepare_pip(paths: RuntimePaths) -> None:
    if pip_is_ready(paths):
        return

    ensurepip = subprocess.run(
        [str(paths.python_executable), "-m", "ensurepip", "--upgrade"],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if ensurepip.returncode == 0 and pip_is_ready(paths):
        return

    get_pip = paths.cache_dir / "get-pip.py"
    get_pip.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading pip bootstrap into {get_pip}")
    try:
        urllib.request.urlretrieve("https://bootstrap.pypa.io/get-pip.py", get_pip)
    except Exception as exc:  # noqa: BLE001 - setup should report the precise blocked prerequisite.
        raise SystemExit(
            "Could not prepare pip in the roadmap-v2 Python runtime. "
            "Install python3-venv/ensurepip support or allow network access to bootstrap.pypa.io."
        ) from exc
    run([str(paths.python_executable), str(get_pip)])


def prepare_node(paths: RuntimePaths) -> None:
    require_binary("node")
    require_binary("npm")

    package_json = paths.renderer_dir / "package.json"
    package_lock = paths.renderer_dir / "package-lock.json"
    require_file(package_json, "renderer package.json")
    require_file(package_lock, "renderer package-lock.json")

    paths.node_root.mkdir(parents=True, exist_ok=True)
    shutil.copy2(package_json, paths.node_root / "package.json")
    shutil.copy2(package_lock, paths.node_root / "package-lock.json")

    env = {
        **os.environ,
        "PLAYWRIGHT_BROWSERS_PATH": str(paths.browsers_dir),
        "ASTRO_TELEMETRY_DISABLED": "1",
    }
    print(f"Installing roadmap-v2 renderer dependencies with npm ci at {paths.node_root}")
    run(["npm", "ci"], cwd=paths.node_root, env=env)

    playwright_cli = paths.node_modules / "playwright" / "cli.js"
    require_file(playwright_cli, "Playwright CLI")
    paths.browsers_dir.mkdir(parents=True, exist_ok=True)
    print(f"Installing roadmap-v2 Playwright Chromium browser at {paths.browsers_dir}")
    run(["node", str(playwright_cli), "install", "chromium"], cwd=paths.node_root, env=env)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Internal/legacy helper for preparing a roadmap-v2 runtime. "
            "Normal roadmap-v2 execution uses the roadmap-v2-runner Docker image."
        )
    )
    parser.add_argument(
        "--skill-dir",
        default=str(SKILL_DIR),
        help="Installed roadmap-v2 skill package root. Defaults to this script parent package.",
    )
    parser.add_argument(
        "--runtime-home",
        help=f"Override {RUNTIME_HOME_ENV} for this setup run.",
    )
    args = parser.parse_args()

    if sys.version_info < (3, 10):
        raise SystemExit("Python 3.10+ is required to set up roadmap-v2.")

    if args.runtime_home:
        os.environ[RUNTIME_HOME_ENV] = args.runtime_home

    paths = resolve_runtime_paths(Path(args.skill_dir))
    prepare_python(paths)
    prepare_node(paths)
    print(f"roadmap-v2 internal runtime preparation complete. Runtime home: {paths.runtime_home}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
