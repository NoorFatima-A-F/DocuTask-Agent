"""
Planning Graph Edge Models.
Defines PlanEdge and EdgeType (SEQUENTIAL, CONDITIONAL, DEPENDENCY, FALLBACK, ROLLBACK).
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class EdgeType(str, Enum):
    SEQUENTIAL = "SEQUENTIAL"
    CONDITIONAL = "CONDITIONAL"
    DEPENDENCY = "DEPENDENCY"
    FALLBACK = "FALLBACK"
    ROLLBACK = "ROLLBACK"


class PlanEdge(BaseModel):
    """Directed connection between two PlanNodes."""
    edge_id: str
    source_node_id: str
    target_node_id: str
    edge_type: EdgeType = Field(default=EdgeType.SEQUENTIAL)
    condition_expression: Optional[str] = Field(default=None)
    weight: float = Field(default=1.0, ge=0.0)
    model_config = {"frozen": True}
