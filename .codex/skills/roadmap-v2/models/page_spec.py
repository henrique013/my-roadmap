from __future__ import annotations

from typing import Any, Literal

from pydantic import Field

from .base import SCHEMA_VERSION, StrictModel
from .research_pack import Source


PageType = Literal["roadmap", "node"]
BlockType = Literal[
    "hero",
    "level_tabs",
    "node_grid",
    "concept_section",
    "source_list",
    "navigation_trail",
    "references",
]


class NavigationLink(StrictModel):
    label: str = Field(min_length=1)
    href: str = Field(min_length=1)
    rel: Literal["self", "parent", "previous", "next", "node", "source"] = "node"


class PageBlock(StrictModel):
    id: str = Field(min_length=1)
    type: BlockType
    title: str | None = None
    text: str | None = None
    items: list[dict[str, Any]] = Field(default_factory=list)
    props: dict[str, Any] = Field(default_factory=dict)


class PageSpec(StrictModel):
    schema_version: str = SCHEMA_VERSION
    page_type: PageType
    title: str = Field(min_length=1)
    slug: str = Field(min_length=1)
    description: str = Field(min_length=1)
    navigation: list[NavigationLink] = Field(default_factory=list)
    blocks: list[PageBlock] = Field(min_length=1)
    sources: list[Source] = Field(default_factory=list)
