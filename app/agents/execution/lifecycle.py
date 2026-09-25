"""
Execution Lifecycle State Domain Models.
Defines the 14 canonical runtime task and workflow execution states.
"""

from enum import Enum


class ExecutionLifecycleState(str, Enum):
    """
    Canonical 14 runtime states representing deterministic task and execution lifecycle.
    """
    CREATED = "CREATED"
    READY = "READY"
    WAITING = "WAITING"
    SCHEDULED = "SCHEDULED"
    RUNNING = "RUNNING"
    BLOCKED = "BLOCKED"
    PAUSED = "PAUSED"
    RETRYING = "RETRYING"
    ROLLING_BACK = "ROLLING_BACK"
    ROLLED_BACK = "ROLLED_BACK"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    TIMED_OUT = "TIMED_OUT"
