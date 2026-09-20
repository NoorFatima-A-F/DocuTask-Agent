"""
Message Lifecycle States.
Defines MessageLifecycleState enum.
"""

from enum import Enum


class MessageLifecycleState(str, Enum):
    """Message processing lifecycle states."""
    CREATED = "CREATED"
    PUBLISHED = "PUBLISHED"
    ROUTED = "ROUTED"
    DISPATCHED = "DISPATCHED"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"
    DEAD_LETTERED = "DEAD_LETTERED"
