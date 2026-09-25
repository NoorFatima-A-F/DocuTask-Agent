"""
Snapshot Manager for Event-Sourced Mission Replay.
Periodically persists compressed state checkpoints, avoiding full replays of large event logs.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from app.runtime.replay.replay_state_machine import ReconstructedMissionState
from app.runtime.snapshot.snapshot_serializer import SnapshotSerializer


class MissionSnapshotMetadata(BaseModel):
    snapshot_id: str
    mission_id: str
    version: int = Field(default=1, description="Snapshot schema version")
    event_index: int = Field(..., description="Event index covered by this snapshot")
    last_event_id: str = Field(..., description="ID of the last event applied to this snapshot")
    compressed_size_bytes: int
    uncompressed_size_bytes: int
    compression_ratio: float
    checksum: str = Field(..., description="SHA-256 checksum of uncompressed state")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class MissionSnapshotRecord(BaseModel):
    metadata: MissionSnapshotMetadata
    payload_bytes: bytes


class SnapshotManager:
    """Manages periodic versioned snapshots for missions."""

    def __init__(self, snapshot_interval: int = 100):
        self.snapshot_interval = snapshot_interval
        self._snapshots: Dict[str, List[MissionSnapshotRecord]] = {}  # mission_id -> List[Record]

    def create_snapshot(
        self,
        state: ReconstructedMissionState,
        event_index: int,
        last_event_id: str,
        version: int = 1,
    ) -> MissionSnapshotRecord:
        payload_bytes, checksum, uncomp_size = SnapshotSerializer.serialize_state(state, compress=True)
        comp_size = len(payload_bytes)
        ratio = round((1.0 - (comp_size / max(1, uncomp_size))) * 100.0, 2)

        meta = MissionSnapshotMetadata(
            snapshot_id=f"snap_{state.mission_id}_{event_index}_v{version}",
            mission_id=state.mission_id,
            version=version,
            event_index=event_index,
            last_event_id=last_event_id,
            compressed_size_bytes=comp_size,
            uncompressed_size_bytes=uncomp_size,
            compression_ratio=ratio,
            checksum=checksum,
        )

        record = MissionSnapshotRecord(metadata=meta, payload_bytes=payload_bytes)
        if state.mission_id not in self._snapshots:
            self._snapshots[state.mission_id] = []
        self._snapshots[state.mission_id].append(record)
        return record

    def get_latest_snapshot_before(
        self,
        mission_id: str,
        target_index: int,
    ) -> Optional[MissionSnapshotRecord]:
        records = self._snapshots.get(mission_id, [])
        valid = [r for r in records if r.metadata.event_index <= target_index]
        if not valid:
            return None
        return max(valid, key=lambda r: r.metadata.event_index)

    def list_snapshots(self, mission_id: str) -> List[MissionSnapshotMetadata]:
        return [r.metadata for r in self._snapshots.get(mission_id, [])]
