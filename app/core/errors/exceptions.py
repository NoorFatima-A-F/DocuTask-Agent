"""
Enterprise Platform Exception Hierarchy.
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional
import uuid
from .error_codes import ErrorCategory, ErrorSeverity, RecoveryPolicy
from .problem_details import ProblemDetails


class PlatformException(Exception):
    """
    Standard Enterprise Platform Exception.
    Encapsulates category, severity, recovery policy, retryability, and RFC 9457 mapping.
    """

    def __init__(
        self,
        message: str,
        category: ErrorCategory = ErrorCategory.PLATFORM,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        recovery_policy: RecoveryPolicy = RecoveryPolicy.RETRY,
        retryable: bool = False,
        error_code: str = "PLATFORM_ERROR",
        correlation_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        root_cause: Optional[str] = None,
        action: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        http_status: int = 500,
    ):
        super().__init__(message)
        self.error_id = str(uuid.uuid4())
        self.message = message
        self.category = category
        self.severity = severity
        self.recovery_policy = recovery_policy
        self.retryable = retryable
        self.error_code = error_code
        self.correlation_id = correlation_id or str(uuid.uuid4())
        self.tenant_id = tenant_id
        self.root_cause = root_cause
        self.action = action
        self.details = details or {}
        self.http_status = http_status
        self.timestamp = datetime.now(timezone.utc)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to structured JSON dictionary."""
        return {
            "id": self.error_id,
            "category": self.category.value,
            "severity": self.severity.value,
            "recovery_policy": self.recovery_policy.value,
            "retryable": self.retryable,
            "error_code": self.error_code,
            "correlation_id": self.correlation_id,
            "tenant": self.tenant_id,
            "root_cause": self.root_cause,
            "action": self.action,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
        }

    def to_problem_details(self) -> ProblemDetails:
        """Convert to RFC 9457 Problem Details object."""
        return ProblemDetails(
            type=f"https://api.docutask.ai/errors/{self.error_code.lower()}",
            title=self.error_code.replace("_", " ").title(),
            status=self.http_status,
            detail=self.message,
            error_id=self.error_id,
            timestamp=self.timestamp,
            extensions={
                "category": self.category.value,
                "severity": self.severity.value,
                "retryable": self.retryable,
                "correlation_id": self.correlation_id,
                "tenant": self.tenant_id,
                "action": self.action,
            },
        )


class DatabasePlatformException(PlatformException):
    def __init__(self, message: str, **kwargs):
        super().__init__(message, category=ErrorCategory.DATABASE, error_code="DATABASE_ERROR", http_status=500, **kwargs)


class NetworkPlatformException(PlatformException):
    def __init__(self, message: str, **kwargs):
        super().__init__(message, category=ErrorCategory.NETWORK, retryable=True, error_code="NETWORK_ERROR", http_status=502, **kwargs)


class AIPlatformException(PlatformException):
    def __init__(self, message: str, **kwargs):
        super().__init__(message, category=ErrorCategory.AI, error_code="AI_PROVIDER_ERROR", http_status=502, **kwargs)


class AgentPlatformException(PlatformException):
    def __init__(self, message: str, **kwargs):
        super().__init__(message, category=ErrorCategory.AGENT, error_code="AGENT_EXECUTION_ERROR", http_status=500, **kwargs)


class WorkflowPlatformException(PlatformException):
    def __init__(self, message: str, **kwargs):
        super().__init__(message, category=ErrorCategory.WORKFLOW, error_code="WORKFLOW_ERROR", http_status=500, **kwargs)


class ConnectorPlatformException(PlatformException):
    def __init__(self, message: str, **kwargs):
        super().__init__(message, category=ErrorCategory.CONNECTOR, error_code="CONNECTOR_ERROR", http_status=502, **kwargs)


class SecurityPlatformException(PlatformException):
    def __init__(self, message: str, **kwargs):
        super().__init__(message, category=ErrorCategory.SECURITY, severity=ErrorSeverity.HIGH, error_code="SECURITY_VIOLATION", http_status=403, **kwargs)


class ValidationPlatformException(PlatformException):
    def __init__(self, message: str, **kwargs):
        super().__init__(message, category=ErrorCategory.VALIDATION, error_code="VALIDATION_FAILED", http_status=422, **kwargs)


class TimeoutPlatformException(PlatformException):
    def __init__(self, message: str, **kwargs):
        super().__init__(message, category=ErrorCategory.TIMEOUT, retryable=True, error_code="EXECUTION_TIMEOUT", http_status=504, **kwargs)
