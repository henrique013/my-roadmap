## Context

`roadmap-v2` currently publishes a skill package, then prepares a separate host runtime under `.codex-runtime/roadmap-v2/` with Python dependencies, Node dependencies, Astro, Web Awesome, Playwright, Chromium, and cache files. The public setup path is documented through `python3 <skill-dir>/scripts/setup.py` and local shortcuts such as `make setup`.

That model keeps generated dependencies outside the skill package, but it still makes each host responsible for Python, Node, npm, `venv`, package installation, browser download, runtime path configuration, and cleanup. The desired end state is a definitive container runtime where the skill remains the public interface and Docker is only the mechanical backend.

Current execution shape:

```text
$roadmap-v2 + mode flag
  |
  +-> host setup must already exist
  |     +-> .codex-runtime/roadmap-v2/python
  |     +-> .codex-runtime/roadmap-v2/node
  |     +-> .codex-runtime/roadmap-v2/browsers
  |
  +-> run_pipeline.py --mode --input --output-root
        |
        +-> deterministic Python pipes
        +-> LLM JSON handoff
        +-> Astro render
        +-> DOM + Playwright visual gates
        +-> .tmp/roadmaps-v2/<roadmap-slug>/
```

Target execution shape:

```text
$roadmap-v2 + mode flag
  |
  +-> skill resolves semantic mode and request JSON
  |
  +-> docker run roadmap-v2-runner
        |
        +-> prebuilt minimal runtime inside the image
        +-> no install, no browser download, no lockfile mutation
        +-> runs as host UID/GID or equivalent non-root user
        +-> writes only mounted output paths
        |
        +-> .tmp/roadmaps-v2/<roadmap-slug>/
```

## Goals / Non-Goals

**Goals:**

- Make Docker the definitive `roadmap-v2` runtime boundary for normal execution.
- Keep the runner image lean by excluding non-runtime files and avoiding duplicated browser downloads.
- Remove the host setup model from the normal user workflow.
- Decommission `.codex-runtime/roadmap-v2/` and `.codex/runtime/roadmap-v2/` as supported runtime homes.
- Preserve `$roadmap-v2`, `$roadmap-v2-page`, and `$roadmap-v2-node-page` as the public interface.
- Preserve existing pipeline contracts for `--mode`, `--input`, `--output-root`, `.pipeline/llm-requests`, `.pipeline/llm-outputs`, and `.tmp/roadmaps-v2/<roadmap-slug>/`.
- Ensure generated files on bind-mounted output paths are not owned by root on the host.
- Allow runtime execution without network access after the image has been built.

**Non-Goals:**

- Do not replace the LLM handoff model with a direct model API call.
- Do not change roadmap or node page content semantics.
- Do not preserve host setup as a parallel first-class runtime path.
- Do not keep `.codex-runtime/roadmap-v2/` as a cache volume by default.
- Do not optimize for running arbitrary commands inside the container.

## Decisions

### Use a single runner image

Build one `roadmap-v2-runner` image that contains the published `roadmap-v2` package and a prebuilt runtime. The image must be a command runner, not a long-running service, and it must expose no ports.

Alternatives considered:

| Alternative | Reason rejected |
|---|---|
| Keep host setup | Preserves the installation complexity this change is meant to remove. |
| Use a generic devcontainer | Optimizes for full development environments and tends to include extra tools. |
| Use `npx` or an npm package | Does not solve Python, Playwright, Chromium, and OS package requirements cleanly. |
| Build dependencies at each execution | Reintroduces setup cost and network dependency into runtime execution. |

### Keep the image lean without adding user workflow

The implementation should keep the image lean through simple build choices.
Image-size measurement can be used as implementation evidence, but it must not
become a user-facing setup step.

Size reduction tactics should include:

- Use a slim base image or multi-stage build when compatible with Playwright/Chromium.
- Install only required OS packages for Node, Python, Playwright, Chromium, fonts, and certificate handling.
- Avoid dev-only tools in the final image.
- Keep package manager caches out of the final layer.
- Avoid shipping tests, fixtures, `.git`, host runtime directories, `node_modules` outside the prepared runtime, and generated render outputs unless needed for runtime validation.
- Avoid preserving `.codex-runtime/roadmap-v2/` or `.codex/runtime/roadmap-v2/` as copied host artifacts.

### Run as a non-root writer for mounted outputs

The containerized pipeline must create bind-mounted output files with host-writable ownership. The default local command should run the process with the host UID/GID, for example with `--user "$(id -u):$(id -g)"`, or use an equivalent entrypoint that drops privileges before running the pipeline.

The image filesystem must be readable/executable by that runtime user. Writable paths must be limited to mounted output directories and internal temporary paths such as `/tmp`.

### Keep the skill as the public API

The skill continues to interpret the user request, choose exactly one mode, enforce overwrite checkpoints, prepare the input JSON, and invoke the backend. Docker commands may exist as internal implementation details or documented troubleshooting commands, but the normal public workflow remains `$roadmap-v2` plus one mode flag.

### Preserve the runner contract

The Docker backend should call the existing runner contract unless a smaller wrapper is needed:

```bash
python3 <skill-dir>/scripts/run_pipeline.py \
  --mode roadmap-v2-page|roadmap-v2-node-page \
  --input <request-json> \
  --output-root <output-root>
```

If `run_pipeline.py` is adjusted, it must remain compatible with this contract or provide a documented migration path inside the change.

### Remove the legacy runtime model

The implementation should remove or deprecate host setup scripts and docs that imply normal users must run `python3 <skill-dir>/scripts/setup.py`. If scripts remain for image build-time use, they must be marked as internal build helpers, not public setup commands.

Cleanup must include existing generated runtime directories from the supported model:

```text
.codex-runtime/roadmap-v2/
.codex/runtime/roadmap-v2/
```

Because these paths are generated and ignored, cleanup should be explicit and scoped. The Apply phase may remove local generated artifacts only after the task plan names the paths and the user has authorized that implementation scope.

## Risks / Trade-offs

- Image base drift -> Pin image base and record platform evidence, versions, validation, and rollback.
- Playwright/Chromium dependencies increase size -> Use a minimal compatible dependency set and avoid duplicated browser downloads.
- Root-owned output files -> Run with host UID/GID or drop privileges before invoking `run_pipeline.py`.
- Runtime cannot write caches -> Set `HOME` and temporary caches to `/tmp` or `.pipeline/work`, not `/root`.
- Hidden Docker complexity -> Keep Docker behind the skill interface and document only the minimum required operational knobs.
- Removing host setup is breaking -> Make the proposal explicit, update docs, and provide rollback to the last host-runtime implementation if needed.
- Offline runtime might fail due to implicit downloads -> Validate with network disabled after image build.

## Migration Plan

1. Add a minimal container build definition and `.dockerignore`.
2. Move dependency preparation into image build-time.
3. Add a thin backend invocation path for the skill that runs `roadmap-v2-runner`.
4. Make output mounts and UID/GID handling part of the default command.
5. Update docs so `make setup` builds the container runtime instead of running `python3 <skill-dir>/scripts/setup.py`.
6. Remove or reclassify old host setup/runtime code that no longer belongs to the public workflow.
7. Remove generated local runtime directories from the supported model and provide a scoped cleanup step for existing `.codex-runtime/roadmap-v2/` and `.codex/runtime/roadmap-v2/`.
8. Validate unit, integration, portability, fixture execution, visual strict mode, offline runtime, and file ownership.

Rollback is to restore the prior host setup workflow and remove the Docker backend from the public `roadmap-v2` path. Rollback must also document whether generated runtime directories need to be recreated with the old setup command.

## Apply Decisions

- The image builds from the `templates/skills-local/roadmap-v2` source package.
  The published `.codex/skills/roadmap-v2` package is synchronized afterward
  through the repository publication flow instead of becoming the source of
  truth.
- Normal validation moves into the image. Tests and fixtures are not shipped in
  the runtime image; validation mounts the source `tests/` directory read-only
  when needed so the final runner stays smaller.

## Apply Evidence

- Public setup command validated: `make setup`.
- Image base resolved during build: `node:24-bookworm-slim@sha256:242549cd46785b480c832479a730f4f2a20865d61ea2e404fdb2a5c3d3b73ecf`.
- Runtime image id after final build: `sha256:2e4e24f381ae31e24d34caf6e2b5162a0a4e5ed540762acc95e9032205bc4253`.
- Runtime OS packages installed: `ca-certificates`, `chromium`, `fonts-liberation`, `fonts-noto-core`, `fonts-noto-color-emoji`, `python3`, `python3-pip`, and `python3-venv`.
- Python dependencies are installed from `requirements.txt`: `pydantic==2.13.4`, `jsonschema==4.26.0`, `PyYAML==6.0.3`, and `beautifulsoup4==4.14.3`.
- Node dependencies are installed from `web/package-lock.json`, including `@awesome.me/webawesome@3.8.0`, `astro@6.4.4`, `playwright@1.60.0`, and `typescript@6.0.3`.
- The image uses Debian Chromium at `/usr/bin/chromium` and sets `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1`, `PLAYWRIGHT_BROWSERS_PATH=0`, and `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium` so Playwright does not download its own browser.
- The final runtime image intentionally excludes tests, fixtures, `.git`, `.tmp`, `.codex-runtime`, `.codex/runtime`, package-manager caches, render outputs, and generated renderer artifacts.
- `make setup` removed the generated legacy runtime directories `.codex-runtime/roadmap-v2/` and `.codex/runtime/roadmap-v2/`.
- `make roadmap-v2-test-container` passed with runtime network disabled and read-only container filesystem.
- Fixture execution through `.codex/skills/roadmap-v2/scripts/run_container.py` passed with `roadmap-v2-page`, bind-mounted output, `ROADMAP_V2_VISUAL_STRICT=1`, desktop visual check `ok`, and mobile visual check `ok`.
- Output ownership validation returned no files outside the host user or non-writable by the host user, and no symlinks remained in the generated output.
- Rollback is to restore the previous host-runtime implementation, rebuild `.codex/skills/roadmap-v2` through `update-docs`, and reintroduce the old setup path only if the Docker backend must be removed.
