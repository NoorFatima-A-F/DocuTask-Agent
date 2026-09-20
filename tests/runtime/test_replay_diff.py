"""
Replay Step Diff and State Comparison Test Suite.
Verifies engineering replay comparison between step A and step B.
"""

import pytest
from datetime import datetime, timezone
from app.runtime.events.base import RuntimeEvent
from app.runtime.events.persistence import EventStore
from app.runtime.events.replay import EventReplayEngine


@pytest.mark.asyncio
async def test_replay_step_diff():
    store = EventStore()
    m_id = "mission_replay_diff_test"

    # Sequence of events
    ev1 = RuntimeEvent(event_id="e1", mission_id=m_id, sequence_number=1, event_type="MissionCreated", payload={"goal": "Audit Invoices"})
    ev2 = RuntimeEvent(event_id="e2", mission_id=m_id, sequence_number=2, event_type="WorkerStarted", agent_id="PLANNER", payload={"task_id": "task_plan_1"})
    ev3 = RuntimeEvent(event_id="e3", mission_id=m_id, sequence_number=3, event_type="WorkerCompleted", agent_id="PLANNER", payload={"task_id": "task_plan_1", "tokens_processed": 500})
    ev4 = RuntimeEvent(event_id="e4", mission_id=m_id, sequence_number=4, event_type="WorkerStarted", agent_id="EXTRACTOR", payload={"task_id": "task_extract_2"})
    ev5 = RuntimeEvent(event_id="e5", mission_id=m_id, sequence_number=5, event_type="ValidationPassed", payload={"confidence": 0.95})

    for e in [ev1, ev2, ev3, ev4, ev5]:
        await store.append(e)

    engine = EventReplayEngine(store)
    diff = await engine.compare_replay_steps(m_id, step_a=2, step_b=5)

    assert diff.step_a == 2
    assert diff.step_b == 5
    assert "task_plan_1" in diff.delta_completed_tasks
    assert diff.delta_confidence > 0.0
    assert len(diff.intermediate_events) == 3
    assert diff.delta_tokens >= 500
    assert diff.delta_cost_usd > 0.0
