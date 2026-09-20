"""
Planning Optimization Models.
Defines PlanOptimizationTarget and PlanOptimizationScore.
"""

from enum import Enum
from typing import Dict, List
from pydantic import BaseModel, Field


class OptimizationMetric(str, Enum):
    COST = "COST"
    DURATION = "DURATION"
    TOKEN_COUNT = "TOKEN_COUNT"
    RELIABILITY = "RELIABILITY"


class PlanOptimizationTarget(BaseModel):
    metric: OptimizationMetric = Field(default=OptimizationMetric.DURATION)
    target_value: float = Field(default=10.0)
    weight: float = Field(default=1.0, ge=0.0)
    model_config = {"frozen": True}


class PlanOptimizationScore(BaseModel):
    composite_score: float = Field(default=1.0, ge=0.0, le=1.0)
    metrics: Dict[str, float] = Field(default_factory=dict)
    model_config = {"frozen": True}
