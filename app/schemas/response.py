"""
Standard Unified API Response Envelope Schema.
Mandated by the AI Document Processing Platform API guidelines.
"""

from typing import Generic, Optional, TypeVar, Any
from pydantic import BaseModel, Field

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Standardized top-level response envelope for all API endpoints."""

    success: bool = Field(..., description="Indicates whether the request was successful")
    message: str = Field(..., description="Human-readable response summary")
    data: Optional[T] = Field(None, description="Payload data returned on success")
    errors: Optional[Any] = Field(None, description="Detailed error information or list of errors on failure")

    @classmethod
    def success_response(cls, data: Optional[T] = None, message: str = "Request processed successfully") -> "APIResponse[T]":
        """Factory method for successful API responses."""
        return cls(
            success=True,
            message=message,
            data=data,
            errors=None
        )

    @classmethod
    def error_response(cls, message: str, errors: Optional[Any] = None) -> "APIResponse[Any]":
        """Factory method for error API responses."""
        return cls(
            success=False,
            message=message,
            data=None,
            errors=errors
        )
