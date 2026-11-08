"""Typed failures and statuses for the document extraction path (OCR -> LLM -> validation).

Every failure on the document path is raised as an :class:`ExtractionError` carrying a
specific :class:`ErrorCode`. The HTTP status is derived from the code, so callers never
pick a status ad hoc, and the global ``BaseAppException`` handler renders it.

Messages on these exceptions are safe to show to clients: they never contain upstream
response bodies, API keys, or document content.
"""

from __future__ import annotations

from enum import StrEnum

from app.core.exceptions import BaseAppException


class ExtractionStatus(StrEnum):
    """Lifecycle status of an extraction record or job."""

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    FAILED = "FAILED"


TERMINAL_STATUSES = frozenset({ExtractionStatus.COMPLETED, ExtractionStatus.NEEDS_REVIEW, ExtractionStatus.FAILED})


class ErrorCode(StrEnum):
    """Machine-readable failure codes for the extraction path."""

    # LLM provider
    LLM_NOT_CONFIGURED = "LLM_NOT_CONFIGURED"
    LLM_AUTH_FAILED = "LLM_AUTH_FAILED"
    LLM_MODEL_NOT_FOUND = "LLM_MODEL_NOT_FOUND"
    LLM_BAD_REQUEST = "LLM_BAD_REQUEST"
    LLM_RATE_LIMITED = "LLM_RATE_LIMITED"
    LLM_UNAVAILABLE = "LLM_UNAVAILABLE"
    LLM_TIMEOUT = "LLM_TIMEOUT"
    LLM_INVALID_OUTPUT = "LLM_INVALID_OUTPUT"
    LLM_EMPTY_OUTPUT = "LLM_EMPTY_OUTPUT"
    # OCR
    OCR_ENGINE_UNAVAILABLE = "OCR_ENGINE_UNAVAILABLE"
    OCR_FAILED = "OCR_FAILED"
    OCR_NO_TEXT = "OCR_NO_TEXT"
    # Human review
    REJECTED_BY_REVIEWER = "REJECTED_BY_REVIEWER"
    # Background jobs
    QUEUE_UNAVAILABLE = "QUEUE_UNAVAILABLE"
    JOB_INTERNAL_ERROR = "JOB_INTERNAL_ERROR"


HTTP_STATUS_BY_CODE: dict[ErrorCode, int] = {
    ErrorCode.LLM_NOT_CONFIGURED: 503,
    ErrorCode.LLM_AUTH_FAILED: 502,
    ErrorCode.LLM_MODEL_NOT_FOUND: 502,
    ErrorCode.LLM_BAD_REQUEST: 502,
    ErrorCode.LLM_RATE_LIMITED: 503,
    ErrorCode.LLM_UNAVAILABLE: 503,
    ErrorCode.LLM_TIMEOUT: 504,
    ErrorCode.LLM_INVALID_OUTPUT: 502,
    ErrorCode.LLM_EMPTY_OUTPUT: 502,
    ErrorCode.OCR_ENGINE_UNAVAILABLE: 503,
    ErrorCode.OCR_FAILED: 500,
    ErrorCode.OCR_NO_TEXT: 422,
    ErrorCode.REJECTED_BY_REVIEWER: 422,
    ErrorCode.QUEUE_UNAVAILABLE: 503,
    ErrorCode.JOB_INTERNAL_ERROR: 500,
}

DEFAULT_MESSAGES: dict[ErrorCode, str] = {
    ErrorCode.LLM_NOT_CONFIGURED: "No LLM API key is configured; extraction is unavailable.",
    ErrorCode.LLM_AUTH_FAILED: "The LLM provider rejected the configured credentials.",
    ErrorCode.LLM_MODEL_NOT_FOUND: "The configured LLM model was not found by the provider.",
    ErrorCode.LLM_BAD_REQUEST: "The LLM provider rejected the request.",
    ErrorCode.LLM_RATE_LIMITED: "The LLM provider is rate limiting requests; retry later.",
    ErrorCode.LLM_UNAVAILABLE: "The LLM provider is temporarily unavailable.",
    ErrorCode.LLM_TIMEOUT: "The LLM provider did not respond in time.",
    ErrorCode.LLM_INVALID_OUTPUT: "The LLM returned output that is not valid for the requested schema.",
    ErrorCode.LLM_EMPTY_OUTPUT: "The LLM returned an empty response.",
    ErrorCode.OCR_ENGINE_UNAVAILABLE: "The OCR engine (tesseract) is not installed or not reachable.",
    ErrorCode.OCR_FAILED: "OCR processing failed for this document.",
    ErrorCode.OCR_NO_TEXT: "No readable text was found in this document.",
    ErrorCode.REJECTED_BY_REVIEWER: "The extraction was rejected by a reviewer.",
    ErrorCode.QUEUE_UNAVAILABLE: "The job queue (Redis) is not configured or not reachable.",
    ErrorCode.JOB_INTERNAL_ERROR: "The background job failed with an unexpected error.",
}

#: Codes worth retrying automatically (with backoff).
TRANSIENT_CODES = frozenset({ErrorCode.LLM_RATE_LIMITED, ErrorCode.LLM_UNAVAILABLE, ErrorCode.LLM_TIMEOUT})


class ExtractionError(BaseAppException):
    """A typed, client-safe failure on the document extraction path."""

    def __init__(self, code: ErrorCode, message: str | None = None, *, retry_after: float | None = None):
        self.code = code
        self.error_code = code.value
        self.retry_after = retry_after
        super().__init__(
            message=message or DEFAULT_MESSAGES[code],
            status_code=HTTP_STATUS_BY_CODE[code],
            errors={"error_code": code.value},
        )

    @property
    def transient(self) -> bool:
        return self.code in TRANSIENT_CODES


class LLMError(ExtractionError):
    """Failure raised by an LLM provider."""


class OCRError(ExtractionError):
    """Failure raised by the OCR pipeline."""
