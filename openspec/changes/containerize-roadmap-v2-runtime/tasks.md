## 1. Runtime Boundary

- [x] 1.1 Confirm the final container contract for `roadmap-v2-runner`, including entry command, supported environment variables, output mounts, and non-root execution behavior.
- [x] 1.2 Decide whether the image builds from `.codex/skills/roadmap-v2` or from `templates/skills-local/roadmap-v2` with an internal publication step.

## 2. Minimal Image Build

- [x] 2.1 Add a minimal Docker build definition for `roadmap-v2-runner`.
- [x] 2.2 Add a `.dockerignore` that excludes `.git`, `.tmp`, `.codex-runtime`, `.codex/runtime`, package manager caches, render outputs, and non-runtime artifacts.
- [x] 2.3 Move Python dependency preparation into image build-time using the pinned `requirements.txt`.
- [x] 2.4 Move Node/Astro/Web Awesome/Playwright dependency preparation into image build-time using `web/package.json` and `web/package-lock.json`.
- [x] 2.5 Install only the OS packages required for Python, Node, Playwright, Chromium, fonts, certificates, and runtime validation.
- [x] 2.6 Remove package manager caches and temporary build artifacts from the final image layer.

## 3. Skill Backend Integration

- [x] 3.1 Add the Docker backend invocation path while preserving `$roadmap-v2`, `$roadmap-v2-page`, and `$roadmap-v2-node-page` as the public interface.
- [x] 3.2 Preserve `run_pipeline.py --mode --input --output-root` as the execution contract.
- [x] 3.3 Ensure `.pipeline/llm-requests` and `.pipeline/llm-outputs` continue to work through bind-mounted outputs.
- [x] 3.4 Configure runtime environment variables so writable caches use `/tmp`, `.pipeline/work`, or mounted output paths instead of `/root`.
- [x] 3.5 Run the containerized pipeline as the host UID/GID or an equivalent non-root runtime user.

## 4. Legacy Runtime Decommission

- [x] 4.1 Replace the old `make setup`/`setup.py` host-runtime setup with a simple `make setup` that builds the Docker image and cleans the scoped legacy runtime directories.
- [x] 4.2 Remove or reclassify host setup/preflight code so public execution no longer depends on `.codex-runtime/roadmap-v2/` or `.codex/runtime/roadmap-v2/`.
- [x] 4.3 Add a scoped cleanup step for generated legacy runtime directories `.codex-runtime/roadmap-v2/` and `.codex/runtime/roadmap-v2/`.
- [x] 4.4 Verify cleanup does not remove source files, OpenSpec changes, or generated roadmap outputs outside the confirmed cleanup scope.

## 5. Validation

- [x] 5.1 Validate unit checks for contracts, rules, runner behavior, and schema export.
- [x] 5.2 Validate integration checks for Astro rendering and fixture-backed pipeline execution inside the container.
- [x] 5.3 Validate portability checks to ensure runtime execution does not write under the skill package.
- [x] 5.4 Validate fixture-backed `roadmap-v2-page` and `roadmap-v2-node-page` runs.
- [x] 5.5 Validate strict Playwright visual checks with `ROADMAP_V2_VISUAL_STRICT` enabled.
- [x] 5.6 Validate runtime execution with network disabled after the image is built.
- [x] 5.7 Validate bind-mounted output ownership so generated files are writable by the host user without post-run `chown`.
- [x] 5.8 Record image base, OS packages, dependency versions, validation evidence, and rollback notes.

## 6. Publication

- [x] 6.1 Update the skill source under `templates/skills-local/roadmap-v2`.
- [x] 6.2 Publish/sync the generated skill package through the repository's public publication flow.
- [x] 6.3 Re-check the published package under `.codex/skills/roadmap-v2` for drift, generated dependency trash, and stale setup instructions.
- [x] 6.4 Run final OpenSpec status validation for `containerize-roadmap-v2-runtime`.
