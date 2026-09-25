"""
Recovery Lifecycle State Domain Models.
Defines the state machine governing recovery sessions and diagnostic pipelines.
"""

from enum import Enum


class RecoveryLifecycleState(str, Enum):
    """Lifecycle states of an autonomous recovery session."""
    INITIALIZING = "INITIALIZING"
    DETECTING = "DETECTING"
    CLASSIFYING = "CLASSIFYING"
    ANALYZING = "ANALYZING"
    STRATEGY_SELECTING = "STRATEGY_SELECTING"
    PLANNING = "PLANNING"
    EXECUTING = "EXECUTING"
    RECONCILING = "RECONCILING"
    COMPLETED = "COMPLETED"
    ESCALATED = "ESCALATED"
    FAILED = "FAILED"
