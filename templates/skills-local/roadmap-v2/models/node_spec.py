from __future__ import annotations

from pydantic import Field

from .base import SCHEMA_VERSION, StrictModel
from .research_pack import Source
from .roadmap_spec import LevelId


class NodeConcept(StrictModel):
    id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    body: str = Field(min_length=1)
    examples: list[str] = Field(default_factory=list)
    source_ids: list[str] = Field(default_factory=list)


class NodeSpec(StrictModel):
    schema_version: str = SCHEMA_VERSION
    node_id: str = Field(min_length=1)
    roadmap_slug: str = Field(min_length=1)
    level: LevelId
    node_slug: str = Field(min_length=1)
    title: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    concepts: list[NodeConcept] = Field(min_length=1)
    exercises: list[str] = Field(default_factory=list)
    source_ids: list[str] = Field(default_factory=list)
    sources: list[Source] = Field(default_factory=list)
    previous_node_id: str | None = None
    next_node_id: str | None = None
