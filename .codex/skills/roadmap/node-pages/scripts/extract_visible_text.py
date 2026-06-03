#!/usr/bin/env python3
"""Extract visible and semi-visible text from a roadmap node HTML file."""

from __future__ import annotations

import argparse
import html
import re
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path


CAPTURE_TAGS = {
    "title",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "p",
    "a",
    "th",
    "td",
    "strong",
    "span",
    "code",
    "figcaption",
    "caption",
    "summary",
    "button",
    "li",
    "dt",
    "dd",
    "blockquote",
}
SKIP_TAGS = {"script", "style"}
ATTRIBUTES_TO_CAPTURE = ("aria-label", "alt", "title")


@dataclass
class Capture:
    tag: str
    label: str
    order: int
    text_parts: list[str] = field(default_factory=list)


@dataclass
class ExtractedText:
    order: int
    location: str
    text: str


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def markdown_table_cell(value: str) -> str:
    return value.replace("\\", "\\\\").replace("|", "\\|")


class VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.items: list[ExtractedText] = []
        self.capture_stack: list[Capture] = []
        self.skip_depth = 0
        self._next_order = 1

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attrs_map = {name.lower(): value for name, value in attrs if name}

        if tag in SKIP_TAGS:
            self.skip_depth += 1
            return

        if self.skip_depth:
            return

        label = self._label_for(tag, attrs_map)

        for attr_name in ATTRIBUTES_TO_CAPTURE:
            value = attrs_map.get(attr_name)
            text = normalize_text(value or "")
            if text:
                self.items.append(
                    ExtractedText(
                        order=self._consume_order(),
                        location=f"{label}@{attr_name}",
                        text=text,
                    )
                )

        if tag in CAPTURE_TAGS:
            self.capture_stack.append(
                Capture(tag=tag, label=label, order=self._consume_order())
            )

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()

        if tag in SKIP_TAGS and self.skip_depth:
            self.skip_depth -= 1
            return

        if self.skip_depth:
            return

        for index in range(len(self.capture_stack) - 1, -1, -1):
            capture = self.capture_stack[index]
            if capture.tag != tag:
                continue

            self.capture_stack.pop(index)
            text = normalize_text(" ".join(capture.text_parts))
            if text:
                self.items.append(
                    ExtractedText(
                        order=capture.order,
                        location=capture.label,
                        text=text,
                    )
                )
            break

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return

        if not data.strip():
            return

        for capture in self.capture_stack:
            capture.text_parts.append(data)

    def handle_entityref(self, name: str) -> None:
        self.handle_data(f"&{name};")

    def handle_charref(self, name: str) -> None:
        self.handle_data(f"&#{name};")

    def _consume_order(self) -> int:
        order = self._next_order
        self._next_order += 1
        return order

    @staticmethod
    def _label_for(tag: str, attrs_map: dict[str, str | None]) -> str:
        class_value = normalize_text(attrs_map.get("class") or "")
        if class_value:
            classes = ".".join(
                part for part in re.split(r"\s+", class_value) if part
            )
            if classes:
                return f"{tag}.{classes}"

        element_id = normalize_text(attrs_map.get("id") or "")
        if element_id:
            return f"{tag}#{element_id}"

        return tag


def extract_visible_text(html_text: str) -> list[ExtractedText]:
    parser = VisibleTextParser()
    parser.feed(html_text)
    parser.close()
    return sorted(parser.items, key=lambda item: item.order)


def render_markdown(items: list[ExtractedText]) -> str:
    lines = [
        "# Visible text extraction",
        "",
        "## Ordem de aparição",
        "",
        "| Ordem | Local | Texto |",
        "|---:|---|---|",
    ]

    for display_order, item in enumerate(items, start=1):
        lines.append(
            "| {order} | {location} | {text} |".format(
                order=display_order,
                location=markdown_table_cell(item.location),
                text=markdown_table_cell(item.text),
            )
        )

    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extrai texto visível e semivisível de node.html."
    )
    parser.add_argument("--html", required=True, help="Caminho para node.html.")
    parser.add_argument(
        "--out",
        required=True,
        help="Caminho de saída para .editorial/pipeline/01-visible-text/visible-text.md.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    html_path = Path(args.html)
    out_path = Path(args.out)

    if not html_path.exists():
        raise SystemExit(f"falha: HTML não encontrado: {html_path}")

    html_text = html_path.read_text(encoding="utf-8")
    items = extract_visible_text(html_text)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_markdown(items), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
