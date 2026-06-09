## Why

The current `roadmap-v2` runtime requires host preparation across Python, Node, npm, Astro, Web Awesome, Playwright, and Chromium, which makes installation and maintenance heavier than the skill contract should expose. This change makes Docker the definitive runtime boundary so the skill can stay thin, portable, reproducible, and free from the generated dependency directories created by the current setup model.

## What Changes

- Introduce a lean `roadmap-v2-runner` container image that contains the runtime needed to execute the existing deterministic pipeline, Astro renderer, DOM gate, and Playwright visual gate.
- **BREAKING**: remove the current host setup model from the normal `roadmap-v2` execution path, including the supported need for `.codex-runtime/roadmap-v2/`, `.codex/runtime/roadmap-v2/`, and `python3 <skill-dir>/scripts/setup.py` as a user-facing preparation step.
- Replace host dependency installation with image build-time dependency preparation, and require normal runtime execution to perform no package installs, no browser downloads, and no lockfile mutations.
- Keep the public skill interface as `$roadmap-v2` plus exactly one mode flag, with Docker used as an internal execution backend rather than as the user-facing workflow.
- Preserve the current pipeline input/output contract: `--mode`, `--input`, `--output-root`, `.pipeline/llm-requests`, `.pipeline/llm-outputs`, and final outputs under `.tmp/roadmaps-v2/<roadmap-slug>/`.
- Ensure files created from bind mounts are owned by the host user by running the containerized pipeline as the host UID/GID or an equivalent non-root runtime user.
- Remove generated runtime/dependency trash from the supported model and add explicit cleanup/decommission steps for existing local artifacts created by the old model.
- Keep the image lean by excluding generated/runtime trash, tests, fixtures, package-manager caches, render outputs, and duplicated browser downloads.

## Capabilities

### New Capabilities

- `roadmap-v2-container-runtime`: Defines the containerized runtime contract, minimal image requirements, host file permission behavior, legacy runtime decommissioning, and validation criteria for `roadmap-v2`.

### Modified Capabilities

- None.

## Impact

- Affected skill source and published package: `templates/skills-local/roadmap-v2/**` and `.codex/skills/roadmap-v2/**`.
- Affected user-facing setup documentation: `README.md`, `Makefile`, and the `roadmap-v2` `SKILL.md` setup/runtime sections.
- Affected runtime scripts: `scripts/setup.py`, `scripts/preflight.py`, `scripts/run_pipeline.py`, `runner/paths.py`, renderer execution, and test helpers that currently assume `.codex-runtime/roadmap-v2/`.
- New container artifacts are expected, likely including a Dockerfile, `.dockerignore`, and a thin host wrapper or skill backend switch.
- Dependency/platform evidence is required for the image base, OS packages, Python, Node, npm packages, Playwright, Chromium, and cleanup/rollback path.
