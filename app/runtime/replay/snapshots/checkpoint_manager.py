"""
Checkpoint Manager for Phase 13.4.
Coordinates point-in-time state restoration for time-travel inspection.
"""

from typing import Dict, Any, Optional
from app.runtime.replay.snapshots.snapshot_manager import SnapshotManager, ReplayCheckpoint


class CheckpointManager:
    """
    Coordinates checkpoint generation and fast restoration during replay.
    """

    def __init__(self, snapshot_manager: Optional[SnapshotManager] = None):
        self.snapshot_manager = snapshot_manager or SnapshotManager()

    def create_checkpoint_if_due(
        self,
        mission_id: str,
        cursor: int,
        state: Dict[str, Any],
        interval: int = 20,
    ) -> Optional[ReplayCheckpoint]:
        if cursor % interval == 0:
            return self.snapshot_manager.capture_checkpoint(mission_id, cursor, state)
        return None

    def restore_checkpoint(
        self,
        mission_id: str,
        target_cursor: int,
    ) -> Optional[ReplayCheckpoint]:
        return self.snapshot_manager.get_nearest_checkpoint(mission_id, target_cursor)
