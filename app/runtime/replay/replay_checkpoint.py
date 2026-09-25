"""
Replay Checkpoint Subsystem.
Stores fast in-memory snapshots of reconstructed mission state at defined event boundaries
enabling O(1) jump and fast reverse seeking without full replay overhead.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class ReplayCheckpoint(BaseModel):
    checkpoint_id: str = Field(..., description="Unique checkpoint ID")
    mission_id: str = Field(..., description="Mission identifier")
    event_index: int = Field(..., description="Event index of checkpoint")
    event_id: str = Field(..., description="Associated event ID")
    state_payload: Dict = Field(..., description="Serialized reconstructed state dictionary")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ReplayCheckpointManager:
    """Maintains indexed checkpoints for fast seeks."""

    def __init__(self, interval: int = 50):
        self.interval = interval
        self._checkpoints: Dict[int, ReplayCheckpoint] = {}  # event_index -> Checkpoint

    def add_checkpoint(self, checkpoint: ReplayCheckpoint) -> None:
        self._checkpoints[checkpoint.event_index] = checkpoint

    def get_nearest_preceding_checkpoint(self, target_index: int) -> Optional[ReplayCheckpoint]:
        """Finds the latest checkpoint where checkpoint.event_index <= target_index."""
        valid_indices = [idx for idx in self._checkpoints.keys() if idx <= target_index]
        if not valid_indices:
            return None
        best_index = max(valid_indices)
        return self._checkpoints[best_index]

    def clear(self) -> None:
        self._checkpoints.clear()

    def list_checkpoints(self) -> List[ReplayCheckpoint]:
        return [self._checkpoints[k] for k in sorted(self._checkpoints.keys())]
