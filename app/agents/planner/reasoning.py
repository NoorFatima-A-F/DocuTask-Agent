"""
Planning Reasoning Trace Models.
"""

from typing import List
from pydantic import BaseModel, Field


class PlanningReasoningStep(BaseModel):
    """Step in the planner's internal chain of thought reasoning."""
    step_number: int
    stage: str  # GOAL_ANALYSIS, DECOMPOSITION, RANKING, REFLECTION, REPAIR
    decision: str
    rationale: str
    model_config = {"frozen": True}


class PlanningReasoningLog(BaseModel):
    """Aggregated reasoning trace of planning decisions."""
    steps: List[PlanningReasoningStep] = Field(default_factory=list)
    model_config = {"frozen": True}
