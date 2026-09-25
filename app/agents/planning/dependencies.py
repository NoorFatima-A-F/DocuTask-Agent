"""
Planning Dependency Domain Models.
Defines Dependency and DependencyType (HARD, SOFT, DATA, TEMPORAL).
"""

from enum import Enum
from pydantic import BaseModel, Field


class DependencyType(str, Enum):
    HARD = "HARD"
    SOFT = "SOFT"
    DATA = "DATA"
    TEMPORAL = "TEMPORAL"


class Dependency(BaseModel):
    """Dependency relationship between two tasks or graph nodes."""
    source_id: str
    target_id: str
    dependency_type: DependencyType = Field(default=DependencyType.HARD)
    model_config = {"frozen": True}
