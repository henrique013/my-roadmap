from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator

from .base import SCHEMA_VERSION, StrictModel
from .research_pack import Source


LevelId = Literal["basico", "intermediario", "avancado"]


class RoadmapNode(StrictModel):
    node_id: str = Field(min_length=1)
    level: LevelId
    order: int = Field(ge=1)
    slug: str = Field(min_length=1)
    title: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    scope: str = Field(min_length=1)
    learning_objectives: list[str] = Field(min_length=1)
    prerequisites: list[str] = Field(default_factory=list)
    source_ids: list[str] = Field(default_factory=list)


class LevelSpec(StrictModel):
    id: LevelId
    title: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    nodes: list[RoadmapNode] = Field(min_length=1, max_length=10)


class RoadmapSpec(StrictModel):
    schema_version: str = SCHEMA_VERSION
    roadmap_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    slug: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    audience: str = Field(default="general")
    assumptions: list[str] = Field(default_factory=list)
    levels: list[LevelSpec] = Field(min_length=1)
    sources: list[Source] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_node_identity(self) -> "RoadmapSpec":
        seen_ids: set[str] = set()
        seen_level_slugs: set[tuple[str, str]] = set()
        for level in self.levels:
            for node in level.nodes:
                if node.level != level.id:
                    raise ValueError(f"node {node.node_id} level does not match container")
                if node.node_id in seen_ids:
                    raise ValueError(f"duplicate node_id: {node.node_id}")
                seen_ids.add(node.node_id)
                key = (node.level, node.slug)
                if key in seen_level_slugs:
                    raise ValueError(f"duplicate node slug in level: {node.level}/{node.slug}")
                seen_level_slugs.add(key)
        return self
