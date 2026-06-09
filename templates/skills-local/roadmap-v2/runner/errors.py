from __future__ import annotations


class PipelineError(RuntimeError):
    code = "PipelineError"


class InputAmbiguityError(PipelineError):
    code = "InputAmbiguityError"


class ContractValidationError(PipelineError):
    code = "ContractValidationError"


class LlmOutputInvalidError(PipelineError):
    code = "LlmOutputInvalidError"


class ResearchInsufficientError(PipelineError):
    code = "ResearchInsufficientError"


class RenderFailedError(PipelineError):
    code = "RenderFailedError"


class DomValidationError(PipelineError):
    code = "DomValidationError"


class VisualRegressionError(PipelineError):
    code = "VisualRegressionError"
