#!/usr/bin/env python3
"""Detecta max-width estreito em seletores de texto comum."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


TEXT_SELECTORS = {
    "p",
    ".lead",
    ".callout",
    "section > p",
    "article > p",
}
ALLOWED_SELECTORS = {
    ".card p",
    ".tag",
    ".small",
    "figcaption",
}
MAIN_SELECTOR_RE = re.compile(r"(^|,)\s*main\s*(,|$)")
BLOCK_RE = re.compile(r"(?P<selectors>[^{}]+)\{(?P<body>[^{}]+)\}", re.MULTILINE)
MAX_WIDTH_RE = re.compile(r"max-width\s*:\s*(?P<value>[^;]+);?", re.IGNORECASE)
STYLE_RE = re.compile(r"<style\b[^>]*>(?P<style>.*?)</style>", re.IGNORECASE | re.DOTALL)
PX_RE = re.compile(r"(?P<number>\d+(?:\.\d+)?)px")


@dataclass(frozen=True)
class CssRule:
    selectors: tuple[str, ...]
    body: str
    max_width: float | None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Falha quando texto comum cria coluna menor que a largura útil."
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--html", help="HTML com CSS embutido.")
    source.add_argument("--css", help="Arquivo CSS.")
    parser.add_argument(
        "--ratio",
        type=float,
        default=0.9,
        help="Percentual mínimo da largura de main para texto comum.",
    )
    return parser.parse_args()


def extract_css(path: Path, is_html: bool) -> str:
    text = path.read_text(encoding="utf-8")
    if not is_html:
        return text
    return "\n".join(match.group("style") for match in STYLE_RE.finditer(text))


def parse_px(value: str) -> float | None:
    value = value.strip().lower()
    if value == "none":
        return None
    match = PX_RE.search(value)
    if not match:
        return None
    return float(match.group("number"))


def parse_rules(css_text: str) -> list[CssRule]:
    rules: list[CssRule] = []
    css_without_comments = re.sub(r"/\*.*?\*/", "", css_text, flags=re.DOTALL)

    for match in BLOCK_RE.finditer(css_without_comments):
        selectors = tuple(
            selector.strip()
            for selector in match.group("selectors").split(",")
            if selector.strip()
        )
        body = match.group("body")
        max_match = MAX_WIDTH_RE.search(body)
        rules.append(
            CssRule(
                selectors=selectors,
                body=body,
                max_width=parse_px(max_match.group("value")) if max_match else None,
            )
        )

    return rules


def main_width(rules: list[CssRule]) -> float | None:
    width: float | None = None
    for rule in rules:
        if any(MAIN_SELECTOR_RE.search(selector) for selector in rule.selectors):
            if rule.max_width is not None:
                width = rule.max_width
    return width


def selector_is_text(selector: str) -> bool:
    normalized = re.sub(r"\s+", " ", selector.strip())
    if normalized in ALLOWED_SELECTORS:
        return False
    return normalized in TEXT_SELECTORS


def collect_failures(rules: list[CssRule], ratio: float) -> list[str]:
    main = main_width(rules)
    failures: list[str] = []

    if main is None:
        failures.append("não foi possível encontrar `main { max-width: ...px }`")
        return failures

    minimum = main * ratio
    for rule in rules:
        if rule.max_width is None:
            continue
        for selector in rule.selectors:
            if selector_is_text(selector) and rule.max_width < minimum:
                failures.append(
                    f"{selector} usa max-width {rule.max_width:g}px com main {main:g}px"
                )

    return failures


def main() -> int:
    args = parse_args()
    path = Path(args.html or args.css)
    if not path.exists():
        print(f"falha: arquivo não encontrado: {path}")
        return 1

    css_text = extract_css(path, is_html=bool(args.html))
    failures = collect_failures(parse_rules(css_text), args.ratio)
    if failures:
        print("falha: largura de conteúdo inválida")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("passa: largura de conteúdo sem max-width estreito em texto comum")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
