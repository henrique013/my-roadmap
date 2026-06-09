from __future__ import annotations

from typing import Literal

from pydantic import AnyUrl, Field

from .base import SCHEMA_VERSION, StrictModel


class ResearchQuestion(StrictModel):
    id: str = Field(min_length=1)
    question: str = Field(min_length=1)
    reason: str = Field(min_length=1)


class Source(StrictModel):
    id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    url: AnyUrl
    source_type: Literal[
        "official-docs",
        "source-code",
        "standard",
        "article",
        "paper",
        "book",
        "other",
    ]
    reason: str = Field(min_length=1)
    supports: list[str] = Field(default_factory=list)


class ResearchFact(StrictModel):
    id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    source_ids: list[str] = Field(min_length=1)
    supports: list[str] = Field(default_factory=list)


class ResearchPack(StrictModel):
    schema_version: str = SCHEMA_VERSION
    topic: str = Field(min_length=1)
    audience: str = Field(default="general")
    questions: list[ResearchQuestion] = Field(default_factory=list)
    sources: list[Source] = Field(default_factory=list)
    facts: list[ResearchFact] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)
    discarded_sources: list[Source] = Field(default_factory=list)
