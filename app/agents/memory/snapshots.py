"""
Memory State Snapshots.
Defines MemorySnapshot, WorkflowSnapshot, ContextSnapshot, PlannerSnapshot, and ReflectionSnapshot for deterministic recovery.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List
from pydantic import BaseModel, Field


class BaseSnapshot(BaseModel):
    """Base snapshot specification."""
    snapshot_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    checksum: str = Field(default="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    model_config = {"frozen": True}


class MemorySnapshot(BaseSnapshot):
    """Snapshot of a memory container state."""
    item_count: int = Field(default=0, ge=0)
    state_payload: Dict[str, Any] = Field(default_factory=dict)


class ContextSnapshot(BaseSnapshot):
    """Snapshot of active context window."""
    token_count: int = Field(default=0, ge=0)
    active_memory_ids: List[str] = Field(default_factory=list)


class ReflectionSnapshot(BaseSnapshot):
    """Snapshot of reflection analysis."""
    quality_score: float = Field(default=1.0, ge=0.0, le=1.0)
    findings: List[str] = Field(default_factory=list)
