"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - Exception Hierarchy.
Provides typed, structured exceptions for connector lifecycles, authentication,
rate limiting, circuit breakers, sandboxing, and policy evaluations.
"""

from typing import Any, Dict, Optional


class ConnectorError(Exception):
    """Base exception for all connector platform errors."""

    def __init__(self, message: str, connector_id: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.connector_id = connector_id
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "connector_id": self.connector_id,
            "details": self.details,
        }


class ConnectorNotFoundError(ConnectorError):
    """Raised when a requested connector is not registered or found."""
    pass


class CapabilityNotFoundError(ConnectorError):
    """Raised when no connector satisfies the requested generic capability."""
    pass


class InvalidConnectorStateError(ConnectorError):
    """Raised when an illegal lifecycle transition is attempted on a connector."""
    pass


class AuthenticationError(ConnectorError):
    """Raised when authentication or credential validation fails."""
    pass


class CredentialNotFoundError(ConnectorError):
    """Raised when credentials for a connector/workspace are missing."""
    pass


class RateLimitExceededError(ConnectorError):
    """Raised when a connector invocation exceeds rate limit policies."""
    def __init__(self, message: str, retry_after_seconds: float = 1.0, **kwargs):
        super().__init__(message, **kwargs)
        self.retry_after_seconds = retry_after_seconds


class CircuitBreakerOpenError(ConnectorError):
    """Raised when an invocation is rejected because the circuit breaker is OPEN."""
    pass


class PolicyViolationError(ConnectorError):
    """Raised when a connector action violates organizational governance policies."""
    pass


class SandboxViolationError(ConnectorError):
    """Raised when a connector execution exceeds memory, CPU, or network boundaries."""
    pass


class ActionExecutionError(ConnectorError):
    """Raised when an action execution fails on an external provider or adapter."""
    pass


class TransformationError(ConnectorError):
    """Raised when payload transformation or serialization fails."""
    pass


class SchemaMappingError(ConnectorError):
    """Raised when schema mapping or path evaluation fails."""
    pass


class WebhookVerificationError(ConnectorError):
    """Raised when webhook signature verification or replay check fails."""
    pass


class CertificationError(ConnectorError):
    """Raised when a connector package fails certification audits."""
    pass


class MCPProtocolError(ConnectorError):
    """Raised when Model Context Protocol communication or discovery fails."""
    pass
