"""
Planning Constraints Models.
Defines PlanConstraint and ConstraintType.
"""

from enum import Enum
from typing import Any, Dict
from pydantic import BaseModel, Field


class ConstraintType(str, Enum):
    BUDGET = "BUDGET"
    TIMEOUT = "TIMEOUT"
    SECURITY = "SECURITY"
    DATA_RESIDENCY = "DATA_RESIDENCY"
    DEPENDENCY = "DEPENDENCY"


class PlanConstraint(BaseModel):
    """Execution constraint applied to a plan or plan node."""
    constraint_id: str
    constraint_type: ConstraintType = Field(default=ConstraintType.TIMEOUT)
    limit_value: float = Field(default=0.0)
    parameters: Dict[str, Any] = Field(default_factory=dict)
    model_config = {"frozen": True}
