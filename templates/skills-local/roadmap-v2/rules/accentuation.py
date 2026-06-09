from __future__ import annotations

import re


EXPECTED_ACCENTS = {
    "basico": "básico",
    "intermediario": "intermediário",
    "avancado": "avançado",
    "nao": "não",
    "voce": "você",
    "conteudo": "conteúdo",
    "pratica": "prática",
    "tecnico": "técnico",
    "codigo": "código",
}


def find_accentuation_issues(text: str) -> list[str]:
    issues: list[str] = []
    lowered = text.lower()
    for plain, accented in EXPECTED_ACCENTS.items():
        if re.search(rf"\b{re.escape(plain)}\b", lowered):
            issues.append(f"use {accented!r} instead of {plain!r} in visible text")
    return issues


def validate_visible_text_accentuation(texts: list[str]) -> None:
    issues: list[str] = []
    for text in texts:
        issues.extend(find_accentuation_issues(text))
    if issues:
        raise ValueError("; ".join(issues))
