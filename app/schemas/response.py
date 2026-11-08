"""
Standard Unified API Response Envelope Schema.
Mandated by the AI Document Processing Platform API guidelines.
"""

from typing import Any

from pydantic import BaseModel, Field


class APIResponse[T](BaseModel):
    """Standardized top-level response envelope for all API endpoints."""

    success: bool = Field(..., description="Indicates whether the request was successful")
    message: str = Field(..., description="Human-readable response summary")
    data: T | None = Field(None, description="Payload data returned on success")
    errors: Any | None = Field(None, description="Detailed error information or list of errors on failure")

    @classmethod
    def success_response(
        cls, data: T | None = None, message: str = "Request processed successfully"
    ) -> "APIResponse[T]":
        """Factory method for successful API responses."""
        return cls(success=True, message=message, data=data, errors=None)

    @classmethod
    def error_response(cls, message: str, errors: Any | None = None) -> "APIResponse[Any]":
        """Factory method for error API responses."""
        return cls(success=False, message=message, data=None, errors=errors)
