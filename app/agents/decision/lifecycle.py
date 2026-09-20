"""
Decision Lifecycle States.
Defines DecisionLifecycleState enum.
"""

from enum import Enum


class DecisionLifecycleState(str, Enum):
    """Decision evaluation lifecycle states."""
    REQUESTED = "REQUESTED"
    EVALUATING = "EVALUATING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"
    FAILED = "FAILED"
