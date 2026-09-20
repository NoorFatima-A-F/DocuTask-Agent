"""
Unit Tests for Replay Runtime, Determinism Validation, and Speed Controls.
"""

import pytest
import asyncio
from app.runtime.observability.schemas import RuntimeEvent, EventCategory, EventType, EventSeverity
from app.runtime.replay.replay_runtime import ReplayRuntimeSession
from app.runtime.replay.replay_speed import ReplaySpeed


def _create_events(mission_id: str, count: int = 10) -> list[RuntimeEvent]:
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
            stage="EXTRACTION",
            payload={"task_id": f"node_{i//2}", "duration_ms": 100.0, "cost_usd": 0.0005},
            previous_hash=prev_hash,
        )
        from app.runtime.observability.event_serializer import EventSerializer
        ev.hash = EventSerializer.compute_event_hash(ev, prev_hash)
        prev_hash = ev.hash
        events.append(ev)
    return events


def test_replay_runtime_determinism_proof():
    events = _create_events("mission_det_01", 12)
    session = ReplayRuntimeSession("mission_det_01", events)

    report = session.validate_determinism(repetitions=4)
    assert report.is_deterministic is True
    assert report.runs_evaluated == 4
    assert report.state_diffs_found == 0
    assert report.verification_hash is not None


@pytest.mark.asyncio
async def test_replay_runtime_continuous_playback():
    events = _create_events("mission_play_01", 6)
    session = ReplayRuntimeSession("mission_play_01", events)
    session.set_speed(ReplaySpeed.INSTANT)

    assert session.player.cursor.current_index == 0
    await session.play(reverse=False)
    assert session.player.cursor.current_index == 5
    assert session.player.cursor.is_at_end is True


@pytest.mark.asyncio
async def test_replay_runtime_reverse_playback():
    events = _create_events("mission_rev_01", 6)
    session = ReplayRuntimeSession("mission_rev_01", events)
    session.set_speed(ReplaySpeed.INSTANT)

    session.seek(5)
    assert session.player.cursor.current_index == 5
    await session.play(reverse=True)
    assert session.player.cursor.current_index == 0
    assert session.player.cursor.is_at_start is True
