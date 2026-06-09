#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

SKILL_DIR = Path(__file__).resolve().parents[1]
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from runner.paths import RuntimePaths, resolve_runtime_paths  # noqa: E402

PYTHON_MODULES = [
    ("pydantic", "pydantic"),
    ("jsonschema", "jsonschema"),
    ("yaml", "PyYAML"),
    ("bs4", "beautifulsoup4"),
]

RENDERER_PACKAGES = [
    ("astro", Path("node_modules/astro/package.json")),
    ("@awesome.me/webawesome", Path("node_modules/@awesome.me/webawesome/package.json")),
    ("typescript", Path("node_modules/typescript/package.json")),
    ("playwright", Path("node_modules/playwright/package.json")),
]

RENDERER_ASSETS = [
    ("Web Awesome assets", Path("node_modules/@awesome.me/webawesome/dist-cdn/webawesome.loader.js")),
]


def runtime_python_has_modules(paths: RuntimePaths) -> list[str]:
    if not paths.python_executable.exists():
        return [package for _, package in PYTHON_MODULES]
    script = "\n".join(
        [
            "import importlib.util, sys",
            "missing = []",
            *[
                f"missing.append({package!r}) if importlib.util.find_spec({module!r}) is None else None"
                for module, package in PYTHON_MODULES
            ],
            "print('\\n'.join(missing))",
            "raise SystemExit(1 if missing else 0)",
        ]
    )
    result = subprocess.run(
        [str(paths.python_executable), "-c", script],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()] or [
        package for _, package in PYTHON_MODULES
    ]


def playwright_chromium_is_installed(paths: RuntimePaths) -> bool:
    executable = os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH")
    if executable and Path(executable).expanduser().is_file():
        return True
    resolved_chromium = shutil.which("chromium") or shutil.which("chromium-browser")
    if resolved_chromium:
        return True

    browser_path = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    candidates: list[Path] = [paths.browsers_dir]
    if browser_path and browser_path != "0":
        candidates.append(Path(browser_path).expanduser())

    for candidate in candidates:
        if not candidate.exists():
            continue
        if any(candidate.glob("chromium-*")) or any(candidate.glob("chromium_headless_shell-*")):
            return True
    return False


def collect_errors(skill_dir: Path) -> list[str]:
    paths = resolve_runtime_paths(skill_dir)
    errors: list[str] = []

    if not (paths.skill_dir / "requirements.txt").is_file():
        errors.append(f"Arquivo de dependências Python da skill ausente: {paths.skill_dir / 'requirements.txt'}")
    if not paths.python_executable.exists():
        errors.append(f"Runtime Python da skill ausente: {paths.python_executable}")

    missing_python = runtime_python_has_modules(paths)
    if missing_python:
        errors.append("Dependências Python ausentes no runtime roadmap-v2: " + ", ".join(missing_python))

    for binary in ["node"]:
        if shutil.which(binary) is None:
            errors.append(f"Binário ausente no PATH: {binary}")

    missing_renderer = [name for name, package_path in RENDERER_PACKAGES if not (paths.node_root / package_path).exists()]
    if missing_renderer:
        errors.append("Dependências Node do runtime renderer ausentes: " + ", ".join(missing_renderer))

    missing_assets = [name for name, asset_path in RENDERER_ASSETS if not (paths.node_root / asset_path).exists()]
    if missing_assets:
        errors.append("Assets Web Awesome ausentes no runtime renderer: " + ", ".join(missing_assets))

    if not playwright_chromium_is_installed(paths):
        errors.append("Browser Chromium do Playwright não encontrado")

    return errors


def print_failure(errors: list[str], skill_dir: Path) -> None:
    paths = resolve_runtime_paths(skill_dir)
    print("Preflight roadmap-v2 falhou.", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    print("", file=sys.stderr)
    print("O runtime normal da roadmap-v2 deve vir da imagem Docker `roadmap-v2-runner`.", file=sys.stderr)
    print("Reconstrua a imagem se dependências, browser ou assets estiverem ausentes.", file=sys.stderr)
    print("", file=sys.stderr)
    print(f"Runtime esperado: {paths.runtime_home}", file=sys.stderr)
    print("", file=sys.stderr)
    print("A execução da skill não instala pacotes, não baixa browsers e não altera lockfiles.", file=sys.stderr)


def run_preflight(skill_dir: Path) -> int:
    errors = collect_errors(skill_dir)
    if errors:
        print_failure(errors, skill_dir)
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Check roadmap-v2 runtime dependencies without installing them.")
    parser.add_argument(
        "--skill-dir",
        default=str(Path(__file__).resolve().parents[1]),
        help="roadmap-v2 skill package root. Defaults to this script parent package.",
    )
    args = parser.parse_args()
    return run_preflight(Path(args.skill_dir).resolve())


if __name__ == "__main__":
    raise SystemExit(main())
