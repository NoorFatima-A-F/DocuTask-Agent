"""
Platform Global Error Framework Package.
"""

from .error_codes import ErrorCategory, ErrorSeverity, RecoveryPolicy
from .problem_details import ProblemDetails
from .exceptions import (
    PlatformException,
    DatabasePlatformException,
    NetworkPlatformException,
    AIPlatformException,
    AgentPlatformException,
    WorkflowPlatformException,
    ConnectorPlatformException,
    SecurityPlatformException,
    ValidationPlatformException,
    TimeoutPlatformException,
)

__all__ = [
    "ErrorCategory",
    "ErrorSeverity",
    "RecoveryPolicy",
    "ProblemDetails",
    "PlatformException",
    "DatabasePlatformException",
    "NetworkPlatformException",
    "AIPlatformException",
    "AgentPlatformException",
    "WorkflowPlatformException",
    "ConnectorPlatformException",
    "SecurityPlatformException",
    "ValidationPlatformException",
    "TimeoutPlatformException",
]
