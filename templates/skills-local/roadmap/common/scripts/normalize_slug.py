#!/usr/bin/env python3
"""Normaliza texto livre para slug estável de roadmap ou node."""

from __future__ import annotations

import argparse
import re
import unicodedata


def normalize_slug(value: str, fallback: str = "roadmap") -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_text.lower())
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or fallback


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normaliza texto para slug.")
    parser.add_argument("text", help="Texto de origem.")
    parser.add_argument("--fallback", default="roadmap", help="Slug se o texto ficar vazio.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print(normalize_slug(args.text, args.fallback))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
