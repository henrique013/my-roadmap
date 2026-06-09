from __future__ import annotations


def validate_source_traceability(source_ids: set[str], used_source_ids: list[str]) -> None:
    missing = sorted({source_id for source_id in used_source_ids if source_id not in source_ids})
    if missing:
        raise ValueError(f"unknown source_ids: {', '.join(missing)}")


def require_sources_for_current_topic(sources: list[dict[str, object]], topic: str) -> None:
    if not sources:
        raise ValueError(f"research for {topic!r} has no traceable sources")
    for source in sources:
        if not source.get("url") or not source.get("reason"):
            raise ValueError("source must include url and reason")
