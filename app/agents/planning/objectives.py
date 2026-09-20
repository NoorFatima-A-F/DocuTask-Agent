"""
Planning Objective Models.
"""

from typing import Any, Dict
from pydantic import BaseModel, Field


class PlanObjective(BaseModel):
    """Specific measurable target associated with a plan goal."""
    objective_id: str
    target_metric: str
    target_value: float
    unit: str = Field(default="")
    is_mandatory: bool = Field(default=True)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    model_config = {"frozen": True}
