## ADDED Requirements

### Requirement: Containerized runtime is the normal execution backend

The `roadmap-v2` skill SHALL use a containerized runner as the normal backend for executing the `roadmap-v2` pipeline. The public skill interface SHALL remain `$roadmap-v2` plus exactly one of `$roadmap-v2-page` or `$roadmap-v2-node-page`.

#### Scenario: User runs roadmap page generation

- **WHEN** the user invokes `$roadmap-v2 $roadmap-v2-page` with enough topic context
- **THEN** the skill resolves the mode and request JSON and runs the pipeline through the containerized backend without requiring `python3 <skill-dir>/scripts/setup.py`

#### Scenario: User runs node page generation

- **WHEN** the user invokes `$roadmap-v2 $roadmap-v2-node-page` with an existing roadmap and exactly one node target
- **THEN** the skill resolves the mode and request JSON and runs the pipeline through the containerized backend without requiring `.codex-runtime/roadmap-v2/`

### Requirement: Runner image excludes non-runtime artifacts

The `roadmap-v2-runner` image SHALL contain the runtime components required for `run_pipeline.py`, deterministic Python pipes, Astro rendering, Web Awesome assets, DOM validation, Playwright, Chromium, and strict visual validation. It SHALL exclude generated dependency trash and files not needed by normal runtime execution.

#### Scenario: Non-runtime artifacts are excluded

- **WHEN** the final container image is inspected or built through its `.dockerignore`
- **THEN** the image excludes `.git`, generated host runtime directories, package manager caches, render outputs, and other files not required for normal `roadmap-v2` execution

### Requirement: Runtime execution performs no dependency installation

The containerized runtime SHALL perform no package installation, no browser download, and no lockfile mutation during normal pipeline execution. Dependency installation SHALL happen only during image build-time or an explicitly documented image preparation phase.

#### Scenario: Runtime runs offline

- **WHEN** the image has already been built and the pipeline is executed with runtime network access disabled
- **THEN** `run_pipeline.py` can complete fixture-backed page and node executions without fetching packages, downloading browsers, or changing lockfiles

#### Scenario: Runtime install attempt is rejected

- **WHEN** normal pipeline execution reaches preflight, render, DOM validation, or visual validation
- **THEN** missing dependencies cause a clear failure instead of invoking `pip install`, `npm ci`, `playwright install`, or equivalent install commands

### Requirement: Pipeline input and output contracts are preserved

The containerized backend SHALL preserve the existing runner contract for `--mode`, `--input`, `--output-root`, `.pipeline/llm-requests`, `.pipeline/llm-outputs`, and outputs under `.tmp/roadmaps-v2/<roadmap-slug>/`.

#### Scenario: LLM handoff remains file-based

- **WHEN** the runner reaches an LLM pipe without a ready output
- **THEN** it writes `.pipeline/llm-requests/<pipe-id>.json` and expects structured JSON in `.pipeline/llm-outputs/<pipe-id>.json`

#### Scenario: Final roadmap output remains stable

- **WHEN** a `roadmap-v2-page` run succeeds
- **THEN** the visible output remains `.tmp/roadmaps-v2/<roadmap-slug>/roadmap.html` with required structured artifacts in the same roadmap output root

#### Scenario: Final node output remains stable

- **WHEN** a `roadmap-v2-node-page` run succeeds
- **THEN** the visible output remains `.tmp/roadmaps-v2/<roadmap-slug>/nodes/<level>/<node-slug>/node.html` with required structured artifacts in the same roadmap output root

### Requirement: Bind-mounted outputs are not root-owned

The containerized backend SHALL create files in bind-mounted output paths with host-writable ownership. The default local execution path SHALL run the pipeline as the host UID/GID or use an equivalent non-root privilege drop before writing outputs.

#### Scenario: Local output ownership matches host user

- **WHEN** a local user runs the containerized backend with a bind-mounted `.tmp/roadmaps-v2` output directory
- **THEN** generated `.pipeline` files, logs, screenshots, assets, and final HTML are writable by the host user without requiring a post-run `chown`

#### Scenario: Container does not depend on `/root`

- **WHEN** the pipeline runs as a non-root user inside the container
- **THEN** runtime temporary files and caches are written to mounted output paths, `.pipeline/work`, or `/tmp`, not to `/root`

### Requirement: Legacy host runtime model is decommissioned

The normal `roadmap-v2` workflow SHALL no longer require or document `.codex-runtime/roadmap-v2/`, `.codex/runtime/roadmap-v2/`, or `python3 <skill-dir>/scripts/setup.py` as public setup requirements. Existing generated runtime artifacts from the old model SHALL have a scoped cleanup path.

#### Scenario: Documentation no longer instructs host dependency setup

- **WHEN** a user follows the documented `roadmap-v2` installation and execution path
- **THEN** `make setup` prepares the container runtime instead of running `python3 <skill-dir>/scripts/setup.py`

#### Scenario: Legacy runtime directories are cleaned explicitly

- **WHEN** the implementation applies the cleanup phase for the old runtime model
- **THEN** it removes or documents removal of `.codex-runtime/roadmap-v2/` and `.codex/runtime/roadmap-v2/` without touching unrelated OpenSpec changes, source files, or user outputs outside the confirmed cleanup scope

### Requirement: Validation covers runtime, permissions, and portability

The implementation SHALL validate the containerized runtime with unit, integration, portability, fixture-backed page and node runs, strict visual validation, offline runtime execution, and output ownership checks.

#### Scenario: Apply validation is complete

- **WHEN** the change is considered ready for review
- **THEN** validation evidence includes command results or documented non-execution for unit tests, integration tests, portability tests, page fixtures, node fixtures, strict visual checks, offline runtime, and file ownership
