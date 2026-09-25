"""
Incremental Snapshot Restorer.
Restores a mission state from a compressed snapshot checkpoint and replays incremental delta events.
"""

from typing import List
from app.runtime.observability.schemas import RuntimeEvent
from app.runtime.replay.replay_state_machine import ReplayStateMachine, ReconstructedMissionState
from app.runtime.snapshot.snapshot_manager import MissionSnapshotRecord
from app.runtime.snapshot.snapshot_serializer import SnapshotSerializer


class SnapshotRestorer:
    """Restores mission state by combining a snapshot with trailing delta events."""

    @staticmethod
    def restore_and_catchup(
        snapshot_record: MissionSnapshotRecord,
        delta_events: List[RuntimeEvent],
    ) -> ReconstructedMissionState:
        # 1. Deserialize base snapshot
        base_state = SnapshotSerializer.deserialize_state(
            payload=snapshot_record.payload_bytes,
            compressed=True,
            expected_checksum=snapshot_record.metadata.checksum,
        )

        # 2. Replay incremental delta events
        state = base_state
        for event in delta_events:
            state = ReplayStateMachine.apply_event(state, event)

        return state
