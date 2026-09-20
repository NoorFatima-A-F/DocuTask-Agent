"""
Planning Scheduling Models.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ScheduleWindow(BaseModel):
    """Execution time window specification."""
    earliest_start: Optional[datetime] = Field(default=None)
    deadline: Optional[datetime] = Field(default=None)
    max_duration_seconds: float = Field(default=3600.0, gt=0.0)
    model_config = {"frozen": True}


class SchedulingPolicy(BaseModel):
    """Scheduling strategy configuration."""
    priority_weight: float = Field(default=1.0, ge=0.0)
    allow_preemption: bool = Field(default=False)
    model_config = {"frozen": True}
