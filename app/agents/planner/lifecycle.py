"""
Planner Lifecycle States.
Defines PlannerLifecycleState enum.
"""

from enum import Enum


class PlannerLifecycleState(str, Enum):
    """Cognitive planning lifecycle state transitions."""
    INITIALIZING = "INITIALIZING"
    ANALYZING_GOAL = "ANALYZING_GOAL"
    DECOMPOSING = "DECOMPOSING"
    GENERATING_CANDIDATES = "GENERATING_CANDIDATES"
    OPTIMIZING = "OPTIMIZING"
    REFLECTING = "REFLECTING"
    REPAIRING = "REPAIRING"
    FINALIZING = "FINALIZING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
