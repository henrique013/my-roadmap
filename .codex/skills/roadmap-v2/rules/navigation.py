from __future__ import annotations

from urllib.parse import urlparse


def validate_navigation_links(links: list[dict[str, str]]) -> None:
    for link in links:
        href = link.get("href", "")
        parsed = urlparse(href)
        if parsed.scheme or parsed.netloc or href.startswith("/"):
            raise ValueError(f"navigation href must be relative: {href!r}")
        if "\\" in href or ".." in href.split("/"):
            raise ValueError(f"navigation href is unsafe: {href!r}")


def validate_previous_next(nodes: list[dict[str, str]]) -> None:
    ordered = [node["node_id"] for node in nodes]
    by_id = {node["node_id"]: node for node in nodes}
    for index, node_id in enumerate(ordered):
        node = by_id[node_id]
        expected_previous = ordered[index - 1] if index > 0 else None
        expected_next = ordered[index + 1] if index + 1 < len(ordered) else None
        if node.get("previous_node_id") != expected_previous:
            raise ValueError(f"invalid previous pointer for {node_id}")
        if node.get("next_node_id") != expected_next:
            raise ValueError(f"invalid next pointer for {node_id}")
