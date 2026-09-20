"""
Planning Risk Evaluation Models.
"""

from typing import List
from pydantic import BaseModel, Field


class PlanRiskScore(BaseModel):
    """Calculated risk score value object for a plan."""
    score: float = Field(default=0.1, ge=0.0, le=1.0)
    risk_level: str = Field(default="LOW")  # LOW, MEDIUM, HIGH, CRITICAL
    model_config = {"frozen": True}


class PlanRiskAssessment(BaseModel):
    """Comprehensive risk assessment for plan validation."""
    risk_score: PlanRiskScore = Field(default_factory=PlanRiskScore)
    risk_factors: List[str] = Field(default_factory=list)
    mitigation_strategies: List[str] = Field(default_factory=list)
    model_config = {"frozen": True}
