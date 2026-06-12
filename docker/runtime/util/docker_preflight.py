#!/usr/bin/env python3
"""Checagens de preflight compartilhadas por wrappers Docker."""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from typing import Sequence


EXIT_PREFLIGHT_FAILED = 125


@dataclass(frozen=True)
class CommandResult:
    returncode: int
    output: str


def run_command(args: Sequence[str], timeout_seconds: float) -> CommandResult:
    try:
        completed = subprocess.run(
            args,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout_seconds,
        )
    except FileNotFoundError as exc:
        return CommandResult(127, str(exc))
    except subprocess.TimeoutExpired as exc:
        output = "\n".join(
            part.strip()
            for part in (exc.stdout or "", exc.stderr or "")
            if isinstance(part, str) and part.strip()
        )
        details = f"tempo limite excedido apos {timeout_seconds:g}s"
        if output:
            details = f"{details}\n{output}"
        return CommandResult(124, details)

    output = "\n".join(
        part.strip()
        for part in (completed.stdout, completed.stderr)
        if part.strip()
    )
    return CommandResult(completed.returncode, output)


def print_failure(message: str, details: str | None = None) -> None:
    print(message, file=sys.stderr)
    if details:
        print(details, file=sys.stderr)
    print("Nenhum comando foi executado na imagem runtime.", file=sys.stderr)


def check_docker_ready(docker_bin: str, timeout_seconds: float, wrapper_label: str) -> None:
    result = run_command([docker_bin, "version"], timeout_seconds)
    if result.returncode == 0:
        return

    details = [
        f"Wrapper: {wrapper_label}",
        f"Comando falhou: {docker_bin} version",
        "Verifique se o Docker CLI esta instalado e se o Docker daemon esta em execucao.",
    ]
    if result.output:
        details.extend(["Saida do Docker:", result.output])
    print_failure("falha: runtime Docker nao esta pronto.", "\n".join(details))
    raise SystemExit(EXIT_PREFLIGHT_FAILED)


def check_image_available(
    docker_bin: str,
    image: str,
    default_image: str,
    build_command: str | None,
    timeout_seconds: float,
    wrapper_label: str,
) -> None:
    result = run_command([docker_bin, "image", "inspect", image], timeout_seconds)
    if result.returncode == 0:
        return

    details = [
        f"Wrapper: {wrapper_label}",
        f"Imagem configurada: {image}",
        f"Comando falhou: {docker_bin} image inspect {image}",
    ]
    if image == default_image and build_command:
        details.extend(
            [
                "Prepare a imagem padrao com:",
                f"  {build_command}",
            ]
        )
    else:
        details.append(
            "Prepare uma imagem compativel com o contrato do wrapper e informe-a em ROADMAP_RUNTIME_IMAGE."
        )
    if result.output:
        details.extend(["Saida do Docker:", result.output])
    print_failure("falha: imagem runtime Docker nao encontrada.", "\n".join(details))
    raise SystemExit(EXIT_PREFLIGHT_FAILED)


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verifica Docker e imagem runtime antes de executar um wrapper."
    )
    parser.add_argument("--image", required=True)
    parser.add_argument("--default-image", required=True)
    parser.add_argument("--build-command")
    parser.add_argument("--wrapper-label", default="docker runtime wrapper")
    parser.add_argument("--docker-bin", default="docker")
    parser.add_argument("--timeout-seconds", default=15.0, type=float)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    check_docker_ready(args.docker_bin, args.timeout_seconds, args.wrapper_label)
    check_image_available(
        args.docker_bin,
        args.image,
        args.default_image,
        args.build_command,
        args.timeout_seconds,
        args.wrapper_label,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
