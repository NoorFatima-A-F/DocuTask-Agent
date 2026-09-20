"""
Unit & Integration Tests for AROL Core Subsystems (TraceContext, EventSerializer, EventStore, EventBus).
"""

import asyncio
import pytest
from app.runtime.observability.schemas import (
    BaseRuntimeEvent,
    EventCategory,
    EventPriority,
    EventSeverity,
    MissionEvent,
    ExecutionEvent,
)
from app.runtime.observability.trace_context import (
    async_trace_span,
    get_current_trace_context,
    trace_span,
)
from app.runtime.observability.event_serializer import EventSerializer
from app.runtime.observability.event_store import EventStore
from app.runtime.observability.event_stream import EventBus


@pytest.mark.asyncio
async def test_trace_context_nesting_and_propagation():
    """Verifies that TraceContext properly increments execution depth and retains trace_id."""
    root_ctx = get_current_trace_context()
    assert root_ctx.execution_depth == 0

    with trace_span("parent_op", component="planner", baggage={"env": "prod"}) as parent:
        assert parent.execution_depth == 1
        assert parent.component == "planner"
        assert parent.baggage["env"] == "prod"

        async with async_trace_span("child_op", component="worker", baggage={"worker": "w1"}) as child:
            assert child.execution_depth == 2
            assert child.parent_span_id == parent.span_id
            assert child.trace_id == parent.trace_id
            assert child.baggage["env"] == "prod"
            assert child.baggage["worker"] == "w1"


def test_event_serializer_and_hash_chain():
    """Verifies deterministic SHA-256 hash chaining and tamper detection."""
    e1 = MissionEvent(
        category=EventCategory.MISSION,
        event_type="MISSION_CREATED",
        mission_id="m-001",
        stage="init",
    )
    e1_signed = EventSerializer.sign_and_chain_event(e1, "GENESIS")
    assert e1_signed.event_hash is not None
    assert e1_signed.prev_event_hash == "GENESIS"
    assert EventSerializer.verify_event_integrity(e1_signed) is True

    e2 = ExecutionEvent(
        category=EventCategory.EXECUTION,
        event_type="TASK_STARTED",
        mission_id="m-001",
        stage="ocr",
    )
    e2_signed = EventSerializer.sign_and_chain_event(e2, e1_signed.event_hash)
    assert e2_signed.prev_event_hash == e1_signed.event_hash
    assert EventSerializer.verify_event_integrity(e2_signed) is True

    # Verify stream
    is_valid, idx, reason = EventSerializer.verify_stream_integrity([e1_signed, e2_signed])
    assert is_valid is True
    assert idx == -1

    # Tamper test: modify payload of e1 without re-signing
    e1_signed.payload = {"tampered": True}
    is_valid_tampered, bad_idx, reason = EventSerializer.verify_stream_integrity([e1_signed, e2_signed])
    assert is_valid_tampered is False
    assert bad_idx == 0


@pytest.mark.asyncio
async def test_event_store_append_and_query():
    """Verifies EventStore async appends, queries, and cryptographic integrity verification."""
    store = EventStore()
    m_id = "mission-alpha"

    e1 = MissionEvent(category=EventCategory.MISSION, event_type="MISSION_STARTED", mission_id=m_id)
    e2 = ExecutionEvent(category=EventCategory.EXECUTION, event_type="NODE_RUN", mission_id=m_id, node_id="n1")
    e3 = ExecutionEvent(category=EventCategory.EXECUTION, event_type="NODE_RUN", mission_id=m_id, node_id="n2")

    await store.append(e1)
    await store.append(e2)
    await store.append(e3)

    assert store.total_count() == 3

    # Query mission
    m_events = store.get_events_for_mission(m_id)
    assert len(m_events) == 3

    # Verify chain
    is_valid, _, msg = store.verify_mission_integrity(m_id)
    assert is_valid is True

    # Filtered query
    exec_events = store.query(mission_id=m_id, category=EventCategory.EXECUTION)
    assert len(exec_events) == 2


@pytest.mark.asyncio
async def test_event_bus_priority_and_dlq():
    """Verifies EventBus priority delivery order and isolated DLQ exception handling."""
    bus = EventBus(max_queue_size=100)
    received = []

    async def test_sub(event: BaseRuntimeEvent):
        received.append(event.event_type)

    def failing_sub(event: BaseRuntimeEvent):
        raise ValueError("Simulated subscriber crash")

    bus.subscribe(test_sub)
    bus.subscribe_sync(failing_sub)
    await bus.start()

    try:
        e_low = ExecutionEvent(
            category=EventCategory.EXECUTION,
            event_type="LOW_TASK",
            mission_id="m1",
            priority=EventPriority.LOW,
        )
        e_crit = ExecutionEvent(
            category=EventCategory.EXECUTION,
            event_type="CRITICAL_ALARM",
            mission_id="m1",
            priority=EventPriority.CRITICAL,
        )

        await bus.publish(e_low)
        await bus.publish(e_crit)

        await asyncio.sleep(0.08)

        # Critical should be dispatched before low
        assert "CRITICAL_ALARM" in received
        assert "LOW_TASK" in received
        assert len(bus.get_dlq()) > 0  # Failing sub went to DLQ
    finally:
        await bus.stop()
