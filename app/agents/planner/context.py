"""
Planner Request and Context Domain Models.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, Field
from app.agents.planning.constraints import PlanConstraint
from app.agents.planning.goals import PlanGoal


class PlannerContext(BaseModel):
    """Contextual environment parameters supplied to the planner."""
    document_id: Optional[UUID] = Field(default=None)
    user_id: Optional[UUID] = Field(default=None)
    session_id: Optional[str] = Field(default=None)
    tenant_id: str = Field(default="default")
    max_candidates: int = Field(default=3, ge=1)
    planning_budget_usd: float = Field(default=5.0, ge=0.0)
    parameters: Dict[str, Any] = Field(default_factory=dict)
    model_config = {"frozen": True}


class PlannerRequest(BaseModel):
    """Initial request asking planner to synthesize a plan for a goal."""
    goal: PlanGoal
    context: PlannerContext = Field(default_factory=PlannerContext)
    constraints: List[PlanConstraint] = Field(default_factory=list)
    model_config = {"frozen": True}
