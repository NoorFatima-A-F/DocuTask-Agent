"""
Recommendation Engine Subsystem.
Defines Recommendation model and RecommendationEngine.
"""

from typing import List
from pydantic import BaseModel, Field
from app.agents.decision.context import DecisionContext


class Recommendation(BaseModel):
    """Specific actionable recommendation emitted by DecisionEngine."""
    action: str
    rationale: str
    confidence: float = Field(default=0.9, ge=0.0, le=1.0)
    model_config = {"frozen": True}


class RecommendationEngine:
    """Generates execution and optimization recommendations based on decision context."""

    def generate_recommendations(self, is_approved: bool, context: DecisionContext) -> List[Recommendation]:
        if is_approved:
            return [Recommendation(action="PROCEED", rationale="All policy and rule constraints satisfied", confidence=0.98)]
        return [Recommendation(action="REQUEST_HUMAN_APPROVAL", rationale="Cost or risk thresholds exceeded", confidence=0.85)]
