"""
Policy Constraints Evaluator.
"""

from pydantic import BaseModel, Field


class PolicyConstraints(BaseModel):
    max_cost: float = Field(default=5.0, ge=0.0)
    model_config = {"frozen": True}
