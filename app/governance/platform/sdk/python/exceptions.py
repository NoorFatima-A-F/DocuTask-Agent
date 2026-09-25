"""Exceptions for the Enterprise Governance Python SDK."""

from typing import Any, Dict, Optional


class GovernanceSDKError(Exception):
    """Base class for all Governance SDK exceptions."""

    def __init__(self, message: str, code: str = "SDK_ERROR", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}


class AuthenticationError(GovernanceSDKError):
    """Raised when authentication credentials (API key or Bearer token) are missing, invalid, or expired."""

    def __init__(self, message: str = "Invalid or expired credentials", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, code="AUTHENTICATION_FAILED", details=details)


class PermissionDeniedError(GovernanceSDKError):
    """Raised when the client lacks required scopes or attempts cross-tenant access."""

    def __init__(self, message: str = "Permission denied", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, code="PERMISSION_DENIED", details=details)


class PolicyDeniedError(GovernanceSDKError):
    """Raised when an evaluation fails active governance policy rules."""

    def __init__(self, message: str = "Action blocked by governance policy", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, code="POLICY_DENIED", details=details)


class RateLimitExceededError(GovernanceSDKError):
    """Raised when client exceeds rate limits."""

    def __init__(self, message: str = "Rate limit exceeded", retry_after: float = 1.0, details: Optional[Dict[str, Any]] = None) -> None:
        det = details or {}
        det["retry_after"] = retry_after
        super().__init__(message, code="RATE_LIMIT_EXCEEDED", details=det)
        self.retry_after = retry_after


class ResourceNotFoundError(GovernanceSDKError):
    """Raised when requested policy, decision, or audit record is not found."""

    def __init__(self, message: str = "Resource not found", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, code="NOT_FOUND", details=details)
