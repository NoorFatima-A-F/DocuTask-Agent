"""
Planning Goal Domain Models.
Defines PlanGoal, StrategicGoal, and GoalStatus.
"""

from enum import Enum
from typing import Any, Dict, List
from pydantic import BaseModel, Field


class GoalStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    SATISFIED = "SATISFIED"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"


class PlanGoal(BaseModel):
    """Goal definition within a planning hierarchy."""
    goal_id: str
    name: str
    description: str = Field(default="")
    status: GoalStatus = Field(default=GoalStatus.PENDING)
    priority: int = Field(default=100, ge=1)
    success_criteria: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    model_config = {"frozen": True}


class StrategicGoal(PlanGoal):
    """High-level strategic goal decomposing into operational subgoals."""
    subgoal_ids: List[str] = Field(default_factory=list)
