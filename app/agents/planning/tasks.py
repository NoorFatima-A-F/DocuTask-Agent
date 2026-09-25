"""
Planning Task Domain Models.
Defines PlanningTask aggregate for plan execution graphs.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class PlanningTask(BaseModel):
    """Atomic executable task unit within a plan graph."""
    task_id: str
    name: str
    task_type: str = Field(default="STANDARD")
    capability_requirement: Optional[str] = Field(default=None)
    parameters: Dict[str, Any] = Field(default_factory=dict)
    estimated_duration_seconds: float = Field(default=1.0, ge=0.0)
    estimated_cost_usd: float = Field(default=0.0, ge=0.0)
    dependencies: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    model_config = {"frozen": True}
