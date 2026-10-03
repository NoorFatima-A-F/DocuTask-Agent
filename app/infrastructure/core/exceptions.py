"""Domain exceptions for the Infrastructure Abstraction Platform."""

from typing import Any, Dict, Optional


class InfrastructureError(Exception):
    """Base exception for all infrastructure runtime errors."""

    def __init__(self, message: str, code: str = "INFRASTRUCTURE_ERROR", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}


class ResourceAllocationError(InfrastructureError):
    """Raised when compute, storage, or network resource provisioning fails."""

    def __init__(self, message: str = "Resource allocation failed", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, code="RESOURCE_ALLOCATION_FAILED", details=details)


class ProviderTimeoutError(InfrastructureError):
    """Raised when an underlying cloud provider adapter operation times out."""

    def __init__(self, message: str = "Provider operation timed out", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, code="PROVIDER_TIMEOUT", details=details)


class ConfigurationInvalidError(InfrastructureError):
    """Raised when declarative infrastructure configuration fails validation."""

    def __init__(self, message: str = "Invalid infrastructure configuration", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, code="INVALID_CONFIGURATION", details=details)


class ServiceHealthError(InfrastructureError):
    """Raised when a service health check reports critical failure."""

    def __init__(self, message: str = "Service health check failed", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, code="SERVICE_UNHEALTHY", details=details)


class InvalidStateTransitionError(InfrastructureError):
    """Raised when an invalid lifecycle state transition is attempted."""

    def __init__(self, message: str = "Invalid lifecycle state transition", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, code="INVALID_STATE_TRANSITION", details=details)
