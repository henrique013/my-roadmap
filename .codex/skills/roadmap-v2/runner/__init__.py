from .errors import (
    ContractValidationError,
    DomValidationError,
    InputAmbiguityError,
    LlmOutputInvalidError,
    PipelineError,
    RenderFailedError,
    ResearchInsufficientError,
    VisualRegressionError,
)

__all__ = [
    "ContractValidationError",
    "DomValidationError",
    "InputAmbiguityError",
    "LlmOutputInvalidError",
    "PipeManifest",
    "PipelineError",
    "PipelineRunner",
    "RenderFailedError",
    "ResearchInsufficientError",
    "VisualRegressionError",
    "load_pipe_manifest",
]


def __getattr__(name: str):
    if name in {"PipeManifest", "load_pipe_manifest"}:
        from .manifest import PipeManifest, load_pipe_manifest

        values = {
            "PipeManifest": PipeManifest,
            "load_pipe_manifest": load_pipe_manifest,
        }
        return values[name]
    if name == "PipelineRunner":
        from .pipeline import PipelineRunner

        return PipelineRunner
    raise AttributeError(name)
