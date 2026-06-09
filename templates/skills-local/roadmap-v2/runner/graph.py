from __future__ import annotations

from graphlib import TopologicalSorter


class PipelineGraph:
    def __init__(self, pipe_ids: list[str]) -> None:
        self.pipe_ids = pipe_ids

    def ordered(self) -> list[str]:
        return list(self.pipe_ids)

    @classmethod
    def from_linear(cls, pipe_ids: list[str]) -> "PipelineGraph":
        return cls(pipe_ids)

    @classmethod
    def from_dependencies(cls, dependencies: dict[str, set[str]]) -> "PipelineGraph":
        sorter = TopologicalSorter(dependencies)
        return cls(list(sorter.static_order()))
