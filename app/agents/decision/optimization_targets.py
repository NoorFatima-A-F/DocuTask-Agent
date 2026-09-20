"""
Optimization Target Models.
Cost, Latency, Accuracy, and Reliability targets.
"""

from enum import Enum
from pydantic import BaseModel, Field


class OptimizationMetric(str, Enum):
    COST = "COST"
    LATENCY = "LATENCY"
    ACCURACY = "ACCURACY"
    RELIABILITY = "RELIABILITY"


class OptimizationTarget(BaseModel):
    metric: OptimizationMetric = Field(default=OptimizationMetric.COST)
    target_value: float = Field(default=1.0)
    weight: float = Field(default=1.0, ge=0.0)
    model_config = {"frozen": True}
