#!/usr/bin/env python3
"""Scan literal blocked aliases from a concept ledger against extracted text."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


BLOCKED_SECTION_HEADINGS = {
    "conceitos permitidos só no dump",
    "conceitos permitidos so no dump",
    "conceitos reservados a nodes futuros",
}
BLOCKED_LIST_LABELS = {
    "aliases bloqueados no html",
    "aliases bloqueados",
}


@dataclass(frozen=True)
class Match:
    term: str
    line_number: int
    context: str


def normalize_heading(value: str) -> str:
    return (
        value.strip()
        .lower()
        .replace("ó", "o")
        .replace("í", "i")
        .replace("á", "a")
        .replace("ã", "a")
        .replace("ç", "c")
        .replace("é", "e")
        .replace("ê", "e")
    )


def extract_blocked_terms(ledger_text: str) -> list[str]:
    terms: list[str] = []
    current_section: str | None = None
    in_blocked_alias_list = False

    for raw_line in ledger_text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        normalized = normalize_heading(stripped.lstrip("#").strip())

        if stripped.startswith("## "):
            current_section = normalized
            in_blocked_alias_list = False
            continue

        if stripped.startswith("### "):
            if current_section in {normalize_heading(item) for item in BLOCKED_SECTION_HEADINGS}:
                term = stripped.lstrip("#").strip()
                if term:
                    terms.append(term)
            in_blocked_alias_list = False
            continue

        label_match = re.match(r"-\s*([^:]+):\s*(.*)$", stripped)
        if label_match:
            label = normalize_heading(label_match.group(1))
            value = label_match.group(2).strip()
            in_blocked_alias_list = label in {
                normalize_heading(item) for item in BLOCKED_LIST_LABELS
            }
            if in_blocked_alias_list and value:
                terms.append(value)
            continue

        if in_blocked_alias_list:
            item_match = re.match(r"-\s+(.+)$", stripped)
            if item_match:
                value = item_match.group(1).strip()
                if value:
                    terms.append(value)
                continue

            if stripped:
                in_blocked_alias_list = False

    return sorted(set(term for term in terms if is_real_term(term)))


def is_real_term(term: str) -> bool:
    stripped = term.strip()
    if not stripped or stripped == "...":
        return False
    if stripped.startswith("<") and stripped.endswith(">"):
        return False
    return True


def scan_terms(text: str, terms: list[str]) -> list[Match]:
    matches: list[Match] = []
    lines = text.splitlines()

    for line_number, line in enumerate(lines, start=1):
        for term in terms:
            if not term:
                continue

            pattern = re.compile(re.escape(term), flags=re.IGNORECASE)
            if pattern.search(line):
                matches.append(
                    Match(
                        term=term,
                        line_number=line_number,
                        context=line.strip(),
                    )
                )

    return matches


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Procura aliases bloqueados literais no texto extraído ou HTML."
    )
    parser.add_argument("--ledger", required=True, help="Caminho para concept-ledger.md.")
    parser.add_argument(
        "--visible",
        help="Caminho para .editorial/visible-text.md. Use --html como alternativa.",
    )
    parser.add_argument("--html", help="Caminho para node.html. Alternativa a --visible.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ledger_path = Path(args.ledger)

    if not ledger_path.exists():
        print(f"falha: ledger não encontrado: {ledger_path}")
        return 1

    if bool(args.visible) == bool(args.html):
        print("falha: informe exatamente um entre --visible e --html")
        return 1

    target_path = Path(args.visible or args.html)
    if not target_path.exists():
        print(f"falha: alvo de busca não encontrado: {target_path}")
        return 1

    terms = extract_blocked_terms(ledger_path.read_text(encoding="utf-8"))
    matches = scan_terms(target_path.read_text(encoding="utf-8"), terms)

    if matches:
        print("falha: candidato de termo bloqueado encontrado")
        for match in matches:
            print(f"- termo: {match.term}")
            print(f"  linha: {match.line_number}")
            print(f"  contexto: {match.context}")
        return 1

    print("passa: nenhum termo bloqueado literal encontrado")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
