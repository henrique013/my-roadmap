from __future__ import annotations

from collections.abc import Iterable

from .slugs import validate_slug


def build_node_id(level: str, node_slug: str) -> str:
    validate_slug(node_slug)
    if level not in {"basico", "intermediario", "avancado"}:
        raise ValueError(f"invalid level: {level!r}")
    return f"{level}/{node_slug}"


def validate_unique_node_ids(node_ids: Iterable[str]) -> None:
    seen: set[str] = set()
    for node_id in node_ids:
        if node_id in seen:
            raise ValueError(f"duplicate node_id: {node_id}")
        seen.add(node_id)
