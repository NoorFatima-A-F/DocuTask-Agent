"""
Planning SubTask Domain Models.
"""

from typing import Any, Dict
from pydantic import BaseModel, Field


class PlanningSubTask(BaseModel):
    """Sub-task component of a parent PlanningTask."""
    subtask_id: str
    parent_task_id: str
    name: str
    order_index: int = Field(default=0, ge=0)
    parameters: Dict[str, Any] = Field(default_factory=dict)
    model_config = {"frozen": True}
