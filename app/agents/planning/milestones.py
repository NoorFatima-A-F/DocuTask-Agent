"""
Planning Milestone Models.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class PlanMilestone(BaseModel):
    """Execution progress milestone requiring verification of prerequisite task completions."""
    milestone_id: str
    name: str
    required_task_ids: List[str] = Field(default_factory=list)
    target_completion: Optional[datetime] = Field(default=None)
    is_reached: bool = Field(default=False)
    model_config = {"frozen": True}
