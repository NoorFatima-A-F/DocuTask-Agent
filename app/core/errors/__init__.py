"""
Platform Global Error Framework Package.
"""

from .error_codes import ErrorCategory, ErrorSeverity, RecoveryPolicy
from .exceptions import (
    AgentPlatformException,
    AIPlatformException,
    ConnectorPlatformException,
    DatabasePlatformException,
    NetworkPlatformException,
    PlatformException,
    SecurityPlatformException,
    TimeoutPlatformException,
    ValidationPlatformException,
    WorkflowPlatformException,
)
from .problem_details import ProblemDetails

__all__ = [
    "AIPlatformException",
    "AgentPlatformException",
    "ConnectorPlatformException",
    "DatabasePlatformException",
    "ErrorCategory",
    "ErrorSeverity",
    "NetworkPlatformException",
    "PlatformException",
    "ProblemDetails",
    "RecoveryPolicy",
    "SecurityPlatformException",
    "TimeoutPlatformException",
    "ValidationPlatformException",
    "WorkflowPlatformException",
]
