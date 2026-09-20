"""
Unit Tests for Snapshot Manager and Incremental State Restoration.
"""

import pytest
from app.runtime.observability.schemas import RuntimeEvent, EventCategory, EventType, EventSeverity
from app.runtime.replay.replay_state_machine import ReplayStateMachine
from app.runtime.snapshot.snapshot_manager import SnapshotManager
from app.runtime.snapshot.snapshot_restorer import SnapshotRestorer


def _build_events(mission_id: str, count: int = 50) -> list[RuntimeEvent]:
    events = []
    prev_hash = "0" * 64
    for i in range(count):
        ev = RuntimeEvent(
            event_id=f"ev_{mission_id}_{i+1:03d}",
            mission_id=mission_id,
            sequence_number=i + 1,
            category=EventCategory.EXECUTION,
            event_type=EventType.EXECUTION_TASK_STARTED if i % 2 == 0 else EventType.EXECUTION_TASK_COMPLETED,
            severity=EventSeverity.INFO,
            stage="PROCESSING",
            payload={"task_id": f"task_{i//2}", "duration_ms": 120.0, "cost_usd": 0.0002},
            previous_hash=prev_hash,
        )
        from app.runtime.observability.event_serializer import EventSerializer
        ev.hash = EventSerializer.compute_event_hash(ev, prev_hash)
        prev_hash = ev.hash
        events.append(ev)
    return events


def test_snapshot_creation_and_compression():
    mgr = SnapshotManager(snapshot_interval=20)
    events = _build_events("mission_snap_01", 30)

    state = ReplayStateMachine.create_initial_state("mission_snap_01")
    for idx, e in enumerate(events[:20]):
        state = ReplayStateMachine.apply_event(state, e)

    rec = mgr.create_snapshot(state, event_index=19, last_event_id=events[19].event_id)

    assert rec.metadata.snapshot_id.startswith("snap_mission_snap_01_19")
    assert rec.metadata.compressed_size_bytes < rec.metadata.uncompressed_size_bytes
    assert rec.metadata.compression_ratio > 0.0
    assert len(mgr.list_snapshots("mission_snap_01")) == 1


def test_snapshot_equivalence_mathematical_proof():
    """Proves that Replay(Snapshot_k + DeltaEvents) == Replay(Full Event Log)."""
    events = _build_events("mission_equiv_01", 40)

    # 1. Compute state via full replay
    full_state = ReplayStateMachine.create_initial_state("mission_equiv_01")
    for e in events:
        full_state = ReplayStateMachine.apply_event(full_state, e)

    # 2. Compute state up to index 20 and snapshot
    mgr = SnapshotManager()
    snap_state = ReplayStateMachine.create_initial_state("mission_equiv_01")
    for e in events[:20]:
        snap_state = ReplayStateMachine.apply_event(snap_state, e)
    snapshot_rec = mgr.create_snapshot(snap_state, event_index=19, last_event_id=events[19].event_id)

    # 3. Restore snapshot and apply remaining 20 delta events
    restored_state = SnapshotRestorer.restore_and_catchup(snapshot_rec, events[20:])

    # 4. Bitwise model equality verification
    assert restored_state.model_dump_json() == full_state.model_dump_json()
    assert restored_state.total_events_applied == 40
    assert restored_state.completed_tasks == full_state.completed_tasks
