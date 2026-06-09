from __future__ import annotations

from collections import Counter


def validate_content_boundaries(nodes: list[dict[str, object]]) -> None:
    titles = [str(node.get("title", "")).strip().lower() for node in nodes]
    repeated_titles = [title for title, count in Counter(titles).items() if title and count > 1]
    if repeated_titles:
        raise ValueError(f"repeated node titles: {', '.join(repeated_titles)}")

    scopes = [str(node.get("scope", "")).strip().lower() for node in nodes]
    repeated_scopes = [scope for scope, count in Counter(scopes).items() if scope and count > 1]
    if repeated_scopes:
        raise ValueError(f"repeated node scopes: {', '.join(repeated_scopes)}")

    for node in nodes:
        objectives = [str(item).strip().lower() for item in node.get("learning_objectives", [])]
        if len(objectives) != len(set(objectives)):
            raise ValueError(f"repeated objectives in node {node.get('node_id')}")
