"""
AI Subsystem Domain Exception Classes.
"""

from app.core.exceptions import BaseAppException


class AIException(BaseAppException):
    """Base exception class for all AI subsystem failures."""

    def __init__(self, message: str = "AI processing error", errors=None):
        super().__init__(message=message, status_code=500, errors=errors)


class AIProviderException(AIException):
    """Raised when LLM provider API invocation fails or times out."""

    def __init__(self, message: str = "AI provider API error", errors=None):
        super().__init__(message=message, errors=errors)


class AIPromptException(AIException):
    """Raised when prompt construction or document type configuration fails."""

    def __init__(self, message: str = "Invalid prompt configuration", errors=None):
        super().__init__(message=message, errors=errors)


class AIValidationException(AIException):
    """Raised when LLM generated JSON fails target schema validation."""

    def __init__(self, message: str = "Structured JSON validation failed", errors=None):
        super().__init__(message=message, errors=errors)


class AIRetryLimitExceededException(AIException):
    """Raised when max retry attempts to obtain valid JSON from LLM are exhausted."""

    def __init__(self, message: str = "Maximum AI retry attempts exhausted", errors=None):
        super().__init__(message=message, errors=errors)
