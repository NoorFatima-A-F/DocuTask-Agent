"""
Workflow Lifecycle State Machine.
Defines explicit, deterministic states across 15 workflow lifecycle phases.
"""

from enum import Enum


class WorkflowLifecycleState(str, Enum):
    """15-state deterministic lifecycle for long-running workflows."""
    CREATED = "CREATED"
    REGISTERED = "REGISTERED"
    READY = "READY"
    SCHEDULED = "SCHEDULED"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    BLOCKED = "BLOCKED"
    PAUSED = "PAUSED"
    MIGRATING = "MIGRATING"
    COMPENSATING = "COMPENSATING"
    RECOVERING = "RECOVERING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    ARCHIVED = "ARCHIVED"

    def is_active(self) -> bool:
        """Checks if the workflow is currently progressing or waiting to progress."""
        return self in (
            WorkflowLifecycleState.READY,
            WorkflowLifecycleState.SCHEDULED,
            WorkflowLifecycleState.RUNNING,
            WorkflowLifecycleState.WAITING,
            WorkflowLifecycleState.BLOCKED,
            WorkflowLifecycleState.PAUSED,
            WorkflowLifecycleState.MIGRATING,
            WorkflowLifecycleState.COMPENSATING,
            WorkflowLifecycleState.RECOVERING,
        )

    def is_terminal(self) -> bool:
        """Checks if the workflow instance has terminated."""
        return self in (
            WorkflowLifecycleState.COMPLETED,
            WorkflowLifecycleState.FAILED,
            WorkflowLifecycleState.CANCELLED,
            WorkflowLifecycleState.ARCHIVED,
        )
