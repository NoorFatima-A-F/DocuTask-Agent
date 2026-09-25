"""
Reflection Lifecycle State Machine.
Defines explicit, deterministic states for reflection processing.
"""

from enum import Enum


class ReflectionLifecycleState(str, Enum):
    """Lifecycle states for a reflection session."""
    PENDING = "PENDING"
    EVALUATING = "EVALUATING"
    CRITIQUING = "CRITIQUING"
    EXTRACTING = "EXTRACTING"
    RECOMMENDING = "RECOMMENDING"
    ADAPTING = "ADAPTING"
    FEEDBACK_GENERATION = "FEEDBACK_GENERATION"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

    def is_terminal(self) -> bool:
        """Checks if the state is terminal."""
        return self in (ReflectionLifecycleState.COMPLETED, ReflectionLifecycleState.FAILED)

    def is_active(self) -> bool:
        """Checks if reflection is currently progressing."""
        return not self.is_terminal() and self != ReflectionLifecycleState.PENDING
