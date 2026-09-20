"""
Snapshot Manager for Phase 13.4.
Manages periodic mission state checkpoints for instant time travel and fast replay seeks.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import hashlib
import json


class ReplayCheckpoint(BaseModel):
    checkpoint_id: str
    mission_id: str
    event_cursor: int
    state_hash: str
    state_payload: Dict[str, Any]
    created_at: str


class SnapshotManager:
    """
    Captures and indexes incremental mission checkpoints.
    """

    def __init__(self, checkpoint_interval: int = 25):
        self.interval = checkpoint_interval
        self._checkpoints: Dict[str, List[ReplayCheckpoint]] = {}

    def capture_checkpoint(
        self,
        mission_id: str,
        cursor: int,
        state_payload: Dict[str, Any],
    ) -> ReplayCheckpoint:
        from datetime import datetime, timezone

        hasher = hashlib.sha256(json.dumps(state_payload, sort_keys=True).encode("utf-8"))
        state_hash = f"sha256:{hasher.hexdigest()}"

        cp = ReplayCheckpoint(
            checkpoint_id=f"chk_{mission_id}_{cursor}",
            mission_id=mission_id,
            event_cursor=cursor,
            state_hash=state_hash,
            state_payload=state_payload,
            created_at=datetime.now(timezone.utc).isoformat(),
        )

        mission_cps = self._checkpoints.setdefault(mission_id, [])
        mission_cps.append(cp)
        return cp

    def get_nearest_checkpoint(
        self,
        mission_id: str,
        target_cursor: int,
    ) -> Optional[ReplayCheckpoint]:
        cps = self._checkpoints.get(mission_id, [])
        valid = [cp for cp in cps if cp.event_cursor <= target_cursor]
        if not valid:
            return None
        return max(valid, key=lambda c: c.event_cursor)

    def list_checkpoints(self, mission_id: str) -> List[ReplayCheckpoint]:
        return self._checkpoints.get(mission_id, [])
