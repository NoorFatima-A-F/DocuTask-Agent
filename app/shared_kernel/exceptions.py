"""
Platform Exception Taxonomy and Base Hierarchy.
Provides traceable, structured exceptions for catastrophic or unhandled platform states.
"""
from typing import Optional, Dict, Any

class PlatformException(Exception):
    """Root platform exception for all non-recoverable system failures."""
    def __init__(
        self,
        message: str,
        error_code: str = "ERR_PLATFORM_GENERAL",
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.cause = cause

class PlatformVerificationError(PlatformException):
    """Verification platform base exception."""
    pass

class DomainException(PlatformVerificationError):
    """Raised when pure domain invariants are breached."""
    def __init__(self, message: str, code: str = "ERR_DOMAIN_INVARIANT", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code, details)

class InvariantViolationError(DomainException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "ERR_INVARIANT_VIOLATION", details)

class ApplicationException(PlatformException):
    """Raised during use case or workflow orchestration failure."""
    def __init__(self, message: str, code: str = "ERR_APPLICATION_WORKFLOW", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code, details)

class InfrastructureException(PlatformException):
    """Raised during storage, database, network, or external IO failure."""
    def __init__(self, message: str, code: str = "ERR_INFRASTRUCTURE", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code, details)

class ValidationException(PlatformException):
    """Raised on critical validation failures."""
    def __init__(self, message: str, code: str = "ERR_VALIDATION_FAILED", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code, details)

class ConfigurationException(PlatformException):
    """Raised on invalid, missing, or corrupt configuration."""
    def __init__(self, message: str, code: str = "ERR_CONFIGURATION", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code, details)

class SecurityException(PlatformException):
    """Raised on security, authentication, or tamper violations."""
    def __init__(self, message: str, code: str = "ERR_SECURITY_VIOLATION", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code, details)

class TamperDetectionError(SecurityException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "ERR_TAMPER_DETECTED", details)

class TimeoutException(PlatformException):
    """Raised when execution exceeds hard timeout deadlines."""
    def __init__(self, message: str, code: str = "ERR_EXECUTION_TIMEOUT", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code, details)

class DependencyException(PlatformException):
    """Raised when external systems or plugins are missing or unresponsive."""
    def __init__(self, message: str, code: str = "ERR_DEPENDENCY_FAILURE", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code, details)

class EnvironmentNotReadyError(DependencyException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "ERR_ENV_NOT_READY", details)

class QualityGateFailedError(DomainException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "ERR_QUALITY_GATE_FAILED", details)

class ConcurrencyException(PlatformException):
    """Raised on optimistic locking or concurrency conflicts."""
    def __init__(self, message: str, code: str = "ERR_CONCURRENCY_CONFLICT", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code, details)

class SerializationException(PlatformException):
    """Raised on serialization or schema deserialization failure."""
    def __init__(self, message: str, code: str = "ERR_SERIALIZATION", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code, details)
