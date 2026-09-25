"""
Planning State Snapshot Models for Deterministic Recovery.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List
from pydantic import BaseModel, Field


class PlanSnapshot(BaseModel):
    """Immutable point-in-time snapshot of plan graph and execution state."""
    snapshot_id: str
    plan_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    state_payload: Dict[str, Any] = Field(default_factory=dict)
    completed_node_ids: List[str] = Field(default_factory=list)
    checksum: str = Field(default="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    model_config = {"frozen": True}
