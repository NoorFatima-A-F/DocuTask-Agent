"""
Planning Resource & Execution Estimation Models.
"""

from pydantic import BaseModel, Field


class ExecutionEstimate(BaseModel):
    """Aggregate execution estimates for plan candidate evaluation."""
    estimated_duration_seconds: float = Field(default=1.0, ge=0.0)
    estimated_tokens: int = Field(default=0, ge=0)
    estimated_cost_usd: float = Field(default=0.0, ge=0.0)
    estimated_memory_mb: float = Field(default=128.0, ge=0.0)
    model_config = {"frozen": True}
