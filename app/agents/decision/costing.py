"""
Cost Estimation Subsystem.
"""

from pydantic import BaseModel, Field


class CostEstimate(BaseModel):
    estimated_cost_usd: float = Field(default=0.0, ge=0.0)
    currency: str = Field(default="USD")
    model_config = {"frozen": True}
