#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

SKILL_DIR = Path(__file__).resolve().parents[1]
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from runner.paths import resolve_runtime_paths  # noqa: E402
from scripts.preflight import PYTHON_MODULES, collect_errors  # noqa: E402


UNIT_TESTS = [
    "test_contracts.py",
    "test_dom_gate.py",
    "test_rules.py",
    "test_runner.py",
]

INTEGRATION_TESTS = [
    "test_renderer_contract.py",
    "test_pipeline_fixtures.py",
]

PORTABILITY_TESTS = [
    "test_portability.py",
]


def reexec_with_runtime_python_if_available() -> None:
    if os.environ.get("ROADMAP_V2_NO_PYTHON_REEXEC") == "1":
        return
    paths = resolve_runtime_paths(SKILL_DIR)
    if not paths.python_executable.exists():
        return
    if Path(sys.prefix).resolve() == paths.python_venv.resolve():
        return
    os.environ["ROADMAP_V2_NO_PYTHON_REEXEC"] = "1"
    os.execv(str(paths.python_executable), [str(paths.python_executable), "-B", *sys.argv])


def run_unittest_file(filename: str) -> int:
    return subprocess.run(
        [sys.executable, "-B", "-m", "unittest", str(SKILL_DIR / "tests" / filename)],
        cwd=SKILL_DIR,
        check=False,
    ).returncode


def run_commands(commands: list[list[str]]) -> int:
    for command in commands:
        result = subprocess.run(command, cwd=SKILL_DIR, check=False)
        if result.returncode != 0:
            return result.returncode
    return 0


def require_python_test_dependencies() -> int:
    missing = [package for module, package in PYTHON_MODULES if importlib.util.find_spec(module) is None]
    if not missing:
        return 0
    print("roadmap-v2 Python test dependencies are missing: " + ", ".join(missing), file=sys.stderr)
    print(f"Run: python3 {SKILL_DIR / 'scripts' / 'setup.py'}", file=sys.stderr)
    return 1


def require_runtime_ready() -> int:
    errors = collect_errors(SKILL_DIR)
    if not errors:
        return 0
    print("roadmap-v2 integration runtime is not ready:", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    print(f"Run: python3 {SKILL_DIR / 'scripts' / 'setup.py'}", file=sys.stderr)
    return 1


def run_unit() -> int:
    status = require_python_test_dependencies()
    if status != 0:
        return status
    commands = [[sys.executable, "-B", str(SKILL_DIR / "scripts" / "export_schemas.py"), "--check"]]
    for filename in UNIT_TESTS:
        status = run_unittest_file(filename)
        if status != 0:
            return status
    return run_commands(commands)


def run_integration() -> int:
    status = require_runtime_ready()
    if status != 0:
        return status
    for filename in INTEGRATION_TESTS:
        status = run_unittest_file(filename)
        if status != 0:
            return status
    return 0


def run_portability() -> int:
    status = require_runtime_ready()
    if status != 0:
        return status
    for filename in PORTABILITY_TESTS:
        status = run_unittest_file(filename)
        if status != 0:
            return status
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run roadmap-v2 tests.")
    parser.add_argument(
        "--mode",
        choices=["unit", "integration", "portability", "all"],
        default="unit",
        help="Test mode to run. Integration and portability require the roadmap-v2 setup runtime.",
    )
    args = parser.parse_args()

    reexec_with_runtime_python_if_available()

    if args.mode == "unit":
        return run_unit()
    if args.mode == "integration":
        return run_integration()
    if args.mode == "portability":
        return run_portability()

    for runner in [run_unit, run_integration, run_portability]:
        status = runner()
        if status != 0:
            return status
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
