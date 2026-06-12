#!/usr/bin/env python3
import os
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
RUNTIME_DIR = SCRIPT_DIR.parent
REPO_ROOT = RUNTIME_DIR.parent.parent
RUNNER = RUNTIME_DIR / "run"
IMAGE = "my-roadmap-roadmap-runtime:playwright-1.60.0"


FAKE_DOCKER = """#!/usr/bin/env python3
import os
import sys
import time

log_path = os.environ["FAKE_DOCKER_LOG"]
mode = os.environ["ROADMAP_FAKE_DOCKER_MODE"]
args = sys.argv[1:]

with open(log_path, "a", encoding="utf-8") as log:
    log.write("cmd\\n")
    for arg in args:
        log.write(f"arg={arg}\\n")
    log.write("end\\n")

command = args[0] if args else ""

if command == "version":
    if mode == "daemon-hang":
        time.sleep(3)
    if mode == "daemon-error":
        print("permission denied fake", file=sys.stderr)
        raise SystemExit(1)
    raise SystemExit(0)

if command == "image" and len(args) >= 2 and args[1] == "inspect":
    if mode == "present":
        raise SystemExit(0)
    if mode == "inspect-error":
        print("inspect exploded fake", file=sys.stderr)
        raise SystemExit(1)
    raise SystemExit(1)

if command == "build" and mode == "build":
    raise SystemExit(0)

if command == "run" and mode == "present":
    raise SystemExit(0)

raise SystemExit(64)
"""


def fail(message: str) -> None:
    raise AssertionError(message)


def assert_contains(path: Path, expected: str) -> None:
    content = path.read_text(encoding="utf-8")
    if expected not in content:
        raise AssertionError(f"conteudo esperado ausente: {expected}\narquivo: {path}\n{content}")


def assert_not_contains(path: Path, unexpected: str) -> None:
    content = path.read_text(encoding="utf-8")
    if unexpected in content:
        raise AssertionError(f"conteudo inesperado presente: {unexpected}\narquivo: {path}\n{content}")


class Harness:
    def __init__(self, tmp_dir: Path) -> None:
        self.tmp_dir = tmp_dir
        self.fake_bin = tmp_dir / "bin"
        self.empty_bin = tmp_dir / "empty-bin"
        self.stdout = tmp_dir / "stdout"
        self.stderr = tmp_dir / "stderr"
        self.log = tmp_dir / "docker.log"
        self.fake_bin.mkdir()
        self.empty_bin.mkdir()
        self._install_fake_docker()
        self.reset()

    def _install_fake_docker(self) -> None:
        fake = self.fake_bin / "docker"
        fake.write_text(FAKE_DOCKER, encoding="utf-8")
        fake.chmod(0o755)

    def reset(self) -> None:
        self.stdout.write_text("", encoding="utf-8")
        self.stderr.write_text("", encoding="utf-8")
        self.log.write_text("", encoding="utf-8")

    def run_wrapper(
        self,
        mode: str,
        timeout_seconds: str,
        *args: str,
        build_mode: str | None = None,
        path: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["PATH"] = path if path is not None else f"{self.fake_bin}:{env.get('PATH', '')}"
        env["FAKE_DOCKER_LOG"] = str(self.log)
        env["ROADMAP_FAKE_DOCKER_MODE"] = mode
        env["ROADMAP_RUNTIME_DOCKER_TIMEOUT"] = timeout_seconds
        if build_mode is not None:
            env["ROADMAP_RUNTIME_BUILD"] = build_mode
        else:
            env.pop("ROADMAP_RUNTIME_BUILD", None)

        completed = subprocess.run(
            [sys.executable, str(RUNNER), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
            check=False,
        )
        self.stdout.write_text(completed.stdout, encoding="utf-8")
        self.stderr.write_text(completed.stderr, encoding="utf-8")
        return completed


def test_docker_cli_missing(harness: Harness) -> None:
    harness.reset()
    completed = harness.run_wrapper("present", "2", "--preflight", path=str(harness.empty_bin))
    if completed.returncode != 127:
        fail("preflight deveria retornar 127 quando Docker CLI esta ausente")
    assert_contains(harness.stderr, "falha: Docker CLI nao encontrado no PATH")


def test_daemon_timeout(harness: Harness) -> None:
    harness.reset()
    completed = harness.run_wrapper("daemon-hang", "1", "--preflight")
    if completed.returncode != 1:
        fail("preflight deveria falhar quando o daemon trava")
    assert_contains(harness.stderr, "falha: Docker daemon nao respondeu em 1s")


def test_daemon_immediate_error(harness: Harness) -> None:
    harness.reset()
    completed = harness.run_wrapper("daemon-error", "2", "--preflight")
    if completed.returncode != 1:
        fail("preflight deveria falhar quando o daemon esta inacessivel")
    assert_contains(harness.stderr, "falha: Docker daemon inacessivel pelo contexto atual")
    assert_contains(harness.stderr, "permission denied fake")


def test_missing_image_fails_fast(harness: Harness) -> None:
    harness.reset()
    completed = harness.run_wrapper("missing", "2", "true")
    if completed.returncode != 1:
        fail("execucao deveria falhar quando a imagem esta ausente")
    assert_contains(harness.stderr, f"falha: imagem runtime ausente: {IMAGE}")
    assert_contains(harness.stderr, "rode: make setup")
    assert_not_contains(harness.log, "arg=run")


def test_inspect_error_is_not_missing_image(harness: Harness) -> None:
    harness.reset()
    completed = harness.run_wrapper("inspect-error", "2", "true")
    if completed.returncode != 1:
        fail("execucao deveria falhar quando inspect tem erro inesperado")
    assert_contains(harness.stderr, f"falha: docker image inspect nao conseguiu verificar {IMAGE}")
    assert_contains(harness.stderr, "inspect exploded fake")
    assert_not_contains(harness.log, "arg=run")


def test_explicit_build(harness: Harness) -> None:
    harness.reset()
    completed = harness.run_wrapper("build", "2", "--build")
    if completed.returncode != 0:
        fail("build explicito deveria passar com docker fake")
    assert_contains(harness.log, "arg=build")
    assert_contains(harness.log, "arg=--tag")
    assert_contains(harness.log, f"arg={IMAGE}")
    assert_contains(harness.log, f"arg={REPO_ROOT}/docker/runtime")
    assert_contains(harness.stderr, f"build: construindo imagem runtime {IMAGE}")


def test_present_image_runs_docker(harness: Harness) -> None:
    harness.reset()
    completed = harness.run_wrapper("present", "2", "echo", "ok")
    if completed.returncode != 0:
        fail("docker run deveria passar com imagem presente")
    assert_contains(harness.log, "arg=image")
    assert_contains(harness.log, "arg=inspect")
    assert_contains(harness.log, "arg=run")
    assert_contains(harness.log, "arg=--rm")
    assert_contains(harness.log, "arg=--workdir")
    assert_contains(harness.log, "arg=/workspace")
    assert_contains(harness.log, "arg=--env")
    assert_contains(harness.log, "arg=PLAYWRIGHT_BROWSERS_PATH=/ms-playwright")
    assert_contains(harness.log, "arg=--mount")
    assert_contains(harness.log, f"arg=type=bind,source={REPO_ROOT},target=/workspace")
    assert_contains(harness.log, "arg=--network")
    assert_contains(harness.log, "arg=none")
    assert_contains(harness.log, "arg=--ipc")
    assert_contains(harness.log, "arg=host")
    assert_contains(harness.log, f"arg={IMAGE}")
    assert_contains(harness.log, "arg=echo")
    assert_contains(harness.log, "arg=ok")


def test_passthrough_after_double_dash(harness: Harness) -> None:
    harness.reset()
    completed = harness.run_wrapper("present", "2", "--", "--flag", "value with space")
    if completed.returncode != 0:
        fail("passthrough depois de -- deveria passar com imagem presente")
    assert_contains(harness.log, "arg=--flag")
    assert_contains(harness.log, "arg=value with space")


def test_invalid_build_mode(harness: Harness) -> None:
    harness.reset()
    completed = harness.run_wrapper("present", "2", "true", build_mode="sometimes")
    if completed.returncode != 2:
        fail("ROADMAP_RUNTIME_BUILD invalido deveria retornar 2")
    assert_contains(harness.stderr, "ROADMAP_RUNTIME_BUILD deve ser always ou never")
    assert_not_contains(harness.log, "arg=version")


def test_missing_command(harness: Harness) -> None:
    harness.reset()
    completed = harness.run_wrapper("present", "2")
    if completed.returncode != 2:
        fail("chamada sem comando deveria retornar 2")
    assert_contains(harness.stderr, "Uso:")
    assert_not_contains(harness.log, "arg=version")


def main() -> int:
    tests = [
        test_docker_cli_missing,
        test_daemon_timeout,
        test_daemon_immediate_error,
        test_missing_image_fails_fast,
        test_inspect_error_is_not_missing_image,
        test_explicit_build,
        test_present_image_runs_docker,
        test_passthrough_after_double_dash,
        test_invalid_build_mode,
        test_missing_command,
    ]

    with tempfile.TemporaryDirectory(prefix="roadmap-runtime-test-") as tmp:
        harness = Harness(Path(tmp))
        for test in tests:
            test(harness)

    print("passa: docker/runtime/run cobre preflight, imagem, build, passthrough e erros")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
