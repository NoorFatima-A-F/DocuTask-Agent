"""
Plan Lifecycle State Models.
Defines PlanLifecycleState enum and transition rules.
"""

from enum import Enum


class PlanLifecycleState(str, Enum):
    """Plan lifecycle states throughout generation, validation, execution, and archiving."""
    DRAFT = "DRAFT"
    VALIDATED = "VALIDATED"
    OPTIMIZED = "OPTIMIZED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    ARCHIVED = "ARCHIVED"
