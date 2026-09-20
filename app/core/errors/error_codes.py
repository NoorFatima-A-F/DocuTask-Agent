"""
Global Error Categories, Severity Levels, and Recovery Policies.
"""

from enum import Enum


class ErrorCategory(str, Enum):
    """12 standard platform error categories."""
    PLATFORM = "PLATFORM"
    DATABASE = "DATABASE"
    NETWORK = "NETWORK"
    AI = "AI"
    AGENT = "AGENT"
    WORKFLOW = "WORKFLOW"
    CONNECTOR = "CONNECTOR"
    SECURITY = "SECURITY"
    VALIDATION = "VALIDATION"
    STORAGE = "STORAGE"
    QUEUE = "QUEUE"
    TIMEOUT = "TIMEOUT"


class ErrorSeverity(str, Enum):
    """Severity classification for error handling and alerting."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    FATAL = "FATAL"


class RecoveryPolicy(str, Enum):
    """Policy-driven recovery strategy."""
    RETRY = "RETRY"
    ROLLBACK = "ROLLBACK"
    COMPENSATION = "COMPENSATION"
    ESCALATION = "ESCALATION"
    DEAD_LETTER_QUEUE = "DEAD_LETTER_QUEUE"
    RESTART_SERVICE = "RESTART_SERVICE"
    HUMAN_APPROVAL = "HUMAN_APPROVAL"
    ABORT = "ABORT"
