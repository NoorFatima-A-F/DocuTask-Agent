"""
Risk Assessment Subsystem.
Defines RiskScore, RiskAssessment, and RiskProfile models.
"""

from typing import Dict, List
from pydantic import BaseModel, Field


class RiskScore(BaseModel):
    """Calculated risk score value object (0.0 Low -> 1.0 Critical)."""
    score: float = Field(default=0.1, ge=0.0, le=1.0)
    risk_level: str = Field(default="LOW")  # LOW, MEDIUM, HIGH, CRITICAL
    model_config = {"frozen": True}


class RiskProfile(BaseModel):
    """Organizational risk tolerance profile."""
    profile_name: str = Field(default="STANDARD")
    max_acceptable_risk_score: float = Field(default=0.5, ge=0.0, le=1.0)
    category_weights: Dict[str, float] = Field(default_factory=lambda: {"SECURITY": 0.4, "COST": 0.3, "COMPLIANCE": 0.3})
    model_config = {"frozen": True}


class RiskAssessment(BaseModel):
    """Risk Assessment result model."""
    risk_score: RiskScore = Field(default_factory=RiskScore)
    risk_profile: RiskProfile = Field(default_factory=RiskProfile)
    risk_factors: List[str] = Field(default_factory=list)
    model_config = {"frozen": True}
