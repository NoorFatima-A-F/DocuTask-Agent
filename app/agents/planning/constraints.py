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


class ConstraintBuilder:
    """Fluent builder for PlanConstraint definitions."""

    def __init__(self, constraint_id: str = "c_default"):
        self._id = constraint_id
        self._type = ConstraintType.TIMEOUT
        self._limit = 0.0
        self._params: Dict[str, Any] = {}

    def with_id(self, constraint_id: str) -> "ConstraintBuilder":
        self._id = constraint_id
        return self

    def with_type(self, constraint_type: ConstraintType) -> "ConstraintBuilder":
        self._type = constraint_type
        return self

    def with_limit(self, limit: float) -> "ConstraintBuilder":
        self._limit = limit
        return self

    def with_param(self, key: str, value: Any) -> "ConstraintBuilder":
        self._params[key] = value
        return self

    def build(self) -> PlanConstraint:
        return PlanConstraint(
            constraint_id=self._id,
            constraint_type=self._type,
            limit_value=self._limit,
            parameters=self._params,
        )

