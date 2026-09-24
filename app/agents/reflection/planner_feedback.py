"""
Planner Feedback Contracts.
Produces structured, typed feedback for the Intelligent Planner to improve future plan generation.
"""

from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class PlannerCritiqueItem(BaseModel):
    """Specific critique item targeting planner decomposition or dependency graph."""
    code: str  # DUPLICATED_TASKS, UNNECESSARY_TASK, MISSING_DEPENDENCY, POOR_DECOMPOSITION, EXCESSIVE_BRANCHING, INVALID_ASSUMPTION
    description: str
    affected_tasks: List[str] = Field(default_factory=list)
    suggested_action: str
    confidence: float = 0.9

    model_config = {"frozen": True}


class PlannerFeedback(BaseModel):
    """
    Structured feedback delivered to the Intelligent Planner.
    The planner consumes this feedback without reflection modifying planning models directly.
    """
    feedback_id: UUID = Field(default_factory=uuid4)
    execution_id: UUID
    plan_id: Optional[UUID] = None
    critique_items: List[PlannerCritiqueItem] = Field(default_factory=list)
    recommended_heuristics: List[str] = Field(default_factory=list)
    decomposition_score: float = Field(default=1.0, ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {"frozen": True}
