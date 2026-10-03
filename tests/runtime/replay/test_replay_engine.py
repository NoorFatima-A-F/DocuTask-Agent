"""
Unit Tests for Replay Engine and Playback Controller.
"""

from app.runtime.observability.schemas import RuntimeEvent, EventCategory, EventType, EventSeverity
from app.runtime.replay.replay_engine import MasterReplayEngine
from app.runtime.replay.replay_bookmarks import BookmarkType


def _create_sample_events(mission_id: str, count: int = 20) -> list[RuntimeEvent]:
    events = []
    prev_hash = "0" * 64
    for i in range(count):
        ev = RuntimeEvent(
            event_id=f"ev_{mission_id}_{i+1:03d}",
            mission_id=mission_id,
            sequence_number=i + 1,
            category=EventCategory.EXECUTION if i % 2 == 0 else EventCategory.PLANNER,
            event_type=EventType.EXECUTION_TASK_STARTED if i % 2 == 0 else EventType.PLANNER_STRATEGY_SELECTED,
            severity=EventSeverity.INFO,
            stage="TEST_STAGE",
            payload={"task_id": f"task_{i}", "step": i, "duration_ms": 50.0},
            previous_hash=prev_hash,
        )
        from app.runtime.observability.event_serializer import EventSerializer
        ev.hash = EventSerializer.compute_event_hash(ev, prev_hash)
        prev_hash = ev.hash
        events.append(ev)
    return events


def test_master_replay_engine_in_memory_session():
    engine = MasterReplayEngine()
    events = _create_sample_events("mission_test_01", 10)
    session = engine.create_in_memory_session("mission_test_01", events)

    assert session.mission_id == "mission_test_01"
    assert len(session.events) == 10
    assert session.player.cursor.total_events == 10
    assert session.player.cursor.current_index == 0


def test_replay_seek_and_step():
    engine = MasterReplayEngine()
    events = _create_sample_events("mission_test_02", 15)
    session = engine.create_in_memory_session("mission_test_02", events)

    # Seek to middle
    state = session.seek(7)
    assert session.player.cursor.current_index == 7
    assert session.player.cursor.progress_percentage == 50.0
    assert state.total_events_applied == 8

    # Step forward
    state = session.step_forward()
    assert session.player.cursor.current_index == 8
    assert state.total_events_applied == 9

    # Step backward
    state = session.step_backward()
    assert session.player.cursor.current_index == 7
    assert state.total_events_applied == 8


def test_replay_bookmarks_and_navigation():
    engine = MasterReplayEngine()
    events = _create_sample_events("mission_test_03", 10)
    session = engine.create_in_memory_session("mission_test_03", events)

    bm = session.bookmark_manager.add_bookmark(
        event_index=5,
        event_id=events[5].event_id,
        bookmark_type=BookmarkType.CUSTOM,
        label="Midpoint Check",
    )

    assert session.bookmark_manager.get_bookmark(bm.bookmark_id) is not None
    state = session.seek_to_bookmark(bm.bookmark_id)
    assert state is not None
    assert session.player.cursor.current_index == 5
