#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

SKILL_DIR = Path(__file__).resolve().parents[1]
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from runner.paths import resolve_runtime_paths  # noqa: E402
from scripts.preflight import run_preflight  # noqa: E402


def reexec_with_runtime_python_if_available(skill_dir: Path) -> None:
    if os.environ.get("ROADMAP_V2_NO_PYTHON_REEXEC") == "1":
        return
    paths = resolve_runtime_paths(skill_dir)
    if not paths.python_executable.exists():
        return
    if Path(sys.prefix).resolve() == paths.python_venv.resolve():
        return
    os.environ["ROADMAP_V2_NO_PYTHON_REEXEC"] = "1"
    os.execv(str(paths.python_executable), [str(paths.python_executable), "-B", *sys.argv])


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a roadmap-v2 pipeline.")
    parser.add_argument("--mode", required=True, choices=["roadmap-v2-page", "roadmap-v2-node-page"])
    parser.add_argument("--input", required=True, help="Path to request JSON.")
    parser.add_argument("--output-root", required=True, help="Resolved .tmp/roadmaps-v2/<slug> output root.")
    parser.add_argument("--llm-fixtures-dir", help="Directory with <pipe-id>.json fixture outputs for LLM pipes.")
    parser.add_argument("--llm-outputs-dir", help="Directory with agent-produced <pipe-id>.json outputs for LLM pipes.")
    parser.add_argument("--skip-preflight", action="store_true", help="Skip dependency preflight for controlled tests.")
    args = parser.parse_args()

    if not args.skip_preflight:
        reexec_with_runtime_python_if_available(SKILL_DIR)

    if not args.skip_preflight:
        preflight_status = run_preflight(SKILL_DIR)
        if preflight_status != 0:
            return preflight_status

    from runner.pipeline import PipelineRunner  # noqa: PLC0415

    request = json.loads(Path(args.input).read_text(encoding="utf-8"))
    runner = PipelineRunner(
        skill_dir=SKILL_DIR,
        mode=args.mode,
        output_root=Path(args.output_root),
        llm_fixtures_dir=Path(args.llm_fixtures_dir) if args.llm_fixtures_dir else None,
        llm_outputs_dir=Path(args.llm_outputs_dir) if args.llm_outputs_dir else None,
        skip_runtime_preflight=args.skip_preflight,
    )
    run = runner.run({"mode": args.mode, **request})
    print(run.model_dump_json(indent=2, exclude_none=True))
    return 0 if run.status == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
