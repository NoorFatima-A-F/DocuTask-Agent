"""
Plan Checkpoint and State Capture Models.
"""

from typing import Any, Dict, List
from pydantic import BaseModel, Field


class PlanCheckpoint(BaseModel):
    """Execution state checkpoint enabling deterministic rollback or replay."""
    checkpoint_id: str
    node_id: str
    captured_state: Dict[str, Any] = Field(default_factory=dict)
    completed_task_ids: List[str] = Field(default_factory=list)
    model_config = {"frozen": True}
