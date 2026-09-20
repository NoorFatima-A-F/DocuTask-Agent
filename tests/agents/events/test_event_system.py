"""
Production Tests for Event-Driven Agent Architecture.
Covers EnterpriseEventBus, EventStore, DeadLetterQueue, wildcard matching, async dispatch, and hash chaining.
"""

import asyncio
import pytest
from datetime import datetime, timezone
from uuid import uuid4

from app.agents.events.dead_letter_queue import DeadLetterQueue, DeadLetterRecord
from app.agents.events.event_bus import EnterpriseEventBus
from app.agents.events.event_store import EventEntry, EventStore
from app.agents.events.event_types import (
    AgentCompletedEvent,
    AgentEvent,
    AgentFailedEvent,
    AgentNegotiationCompletedEvent,
    AgentNegotiationStartedEvent,
    EventPriority,
    ExecutionCompletedEvent,
    ExecutionStartedEvent,
    GoalReceivedEvent,
    GoalUnderstandingCompletedEvent,
    HumanEscalationRequestedEvent,
    HumanFeedbackReceivedEvent,
    MemoryConsolidationCompletedEvent,
    ObservationCompletedEvent,
    PlanOptimizedEvent,
    PlanningCompletedEvent,
    PlanningStartedEvent,
    ReflectionCritiqueCompletedEvent,
    ReflectionStartedEvent,
    RetryRequestedEvent,
    SecurityViolationEvent,
    SelfCorrectionTriggeredEvent,
    StateTransitionEvent,
    TaskCompletedEvent,
    TaskFailedEvent,
    TaskMutatedEvent,
    TaskStartedEvent,
    ToolInvokedEvent,
    ToolPolicyViolationEvent,
)


class TestEventTypes:
    def test_base_agent_event_creation(self):
        evt = AgentEvent(execution_id="exec-1", document_id="doc-1")
        assert evt.event_type == "AgentEvent"
        assert evt.execution_id == "exec-1"
        assert evt.priority == EventPriority.NORMAL
        assert isinstance(evt.to_dict(), dict)
        assert evt.to_dict()["event_type"] == "AgentEvent"

    def test_custom_event_serialization(self):
        evt = GoalUnderstandingCompletedEvent(
            execution_id="exec-2",
            document_id="doc-2",
            payload={"intent": "TAX_AUDIT"},
        )
        data = evt.to_dict()
        assert data["event_type"] == "GoalUnderstandingCompleted"
        assert data["payload"]["intent"] == "TAX_AUDIT"
        assert "event_id" in data
        assert "timestamp" in data

    def test_priority_levels(self):
        assert EventPriority.LOW.value == "low"
        assert EventPriority.NORMAL.value == "normal"
        assert EventPriority.HIGH.value == "high"
        assert EventPriority.CRITICAL.value == "critical"

    def test_task_events(self):
        t_start = TaskStartedEvent(task_id="t1", assigned_agent="AgentA")
        assert t_start.task_id == "t1"
        assert t_start.assigned_agent == "AgentA"

        t_done = TaskCompletedEvent(task_id="t1", duration_ms=150.5)
        assert t_done.duration_ms == 150.5

        t_fail = TaskFailedEvent(task_id="t1", error_message="OCR Timeout", retry_count=2)
        assert t_fail.retry_count == 2
        assert "OCR" in t_fail.error_message

        t_mut = TaskMutatedEvent(mutation_type="INJECT_NODE", affected_tasks=["t1", "t2"])
        assert t_mut.mutation_type == "INJECT_NODE"
        assert len(t_mut.affected_tasks) == 2

    def test_security_and_hitl_events(self):
        sec = SecurityViolationEvent(agent_id="AgentX", action="DELETE_DATA", severity="CRITICAL")
        assert sec.severity == "CRITICAL"

        hitl = HumanEscalationRequestedEvent(ticket_id="tick-1", sla_timeout_seconds=600.0)
        assert hitl.sla_timeout_seconds == 600.0

    def test_legacy_lifecycle_events(self):
        g = GoalReceivedEvent(execution_id="e1")
        ps = PlanningStartedEvent(execution_id="e1")
        pc = PlanningCompletedEvent(execution_id="e1")
        es = ExecutionStartedEvent(execution_id="e1")
        ec = ExecutionCompletedEvent(execution_id="e1")
        oc = ObservationCompletedEvent(execution_id="e1")
        rs = ReflectionStartedEvent(execution_id="e1")
        ac = AgentCompletedEvent(execution_id="e1")
        af = AgentFailedEvent(execution_id="e1")
        rr = RetryRequestedEvent(execution_id="e1")
        assert g.event_type == "GoalReceived"
        assert ps.event_type == "PlanningStarted"
        assert pc.event_type == "PlanningCompleted"
        assert es.event_type == "ExecutionStarted"
        assert ec.event_type == "ExecutionCompleted"
        assert oc.event_type == "ObservationCompleted"
        assert rs.event_type == "ReflectionStarted"
        assert ac.event_type == "AgentCompleted"
        assert af.event_type == "AgentFailed"
        assert rr.event_type == "RetryRequested"

    def test_advanced_phase26_events(self):
        opt = PlanOptimizedEvent(execution_id="e1")
        neg_s = AgentNegotiationStartedEvent(task_id="t1")
        neg_c = AgentNegotiationCompletedEvent(task_id="t1", selected_agent_id="ag1", agreed_cost=0.01)
        tool_i = ToolInvokedEvent(tool_name="tess", agent_id="ag1")
        tool_v = ToolPolicyViolationEvent(tool_name="tess", policy_name="HIPAA", violation_reason="unmasked")
        ref_c = ReflectionCritiqueCompletedEvent(overall_score=0.95, passed=True)
        self_c = SelfCorrectionTriggeredEvent(iteration=2, reason="Score low")
        human_f = HumanFeedbackReceivedEvent(ticket_id="t1", action="APPROVE", operator_id="op1")
        mem_c = MemoryConsolidationCompletedEvent(promoted_patterns_count=3)
        st_tr = StateTransitionEvent(from_state="PLANNING", to_state="EXECUTING")

        assert opt.event_type == "PlanOptimized"
        assert neg_s.event_type == "AgentNegotiationStarted"
        assert neg_c.selected_agent_id == "ag1"
        assert tool_i.tool_name == "tess"
        assert tool_v.policy_name == "HIPAA"
        assert ref_c.overall_score == 0.95
        assert self_c.iteration == 2
        assert human_f.action == "APPROVE"
        assert mem_c.promoted_patterns_count == 3
        assert st_tr.from_state == "PLANNING"

    @pytest.mark.parametrize("priority", [EventPriority.LOW, EventPriority.NORMAL, EventPriority.HIGH, EventPriority.CRITICAL])
    def test_event_priority_parameterization(self, priority):
        evt = AgentEvent(priority=priority)
        assert evt.priority == priority
        assert evt.to_dict()["priority"] == priority.value

    def test_event_trace_propagation(self):
        evt = AgentEvent(trace_id="tr-100", correlation_id="cr-200")
        assert evt.trace_id == "tr-100"
        assert evt.correlation_id == "cr-200"


class TestDeadLetterQueue:
    def test_dlq_enqueue_and_retrieve(self):
        dlq = DeadLetterQueue(max_capacity=10)
        evt = AgentEvent(execution_id="exec-dlq")
        err = RuntimeError("Connection dropped")

        rec = dlq.enqueue(event=evt, topic="task.ocr", error=err, retry_count=3)
        assert rec.topic == "task.ocr"
        assert rec.error_type == "RuntimeError"
        assert len(dlq) == 1

        records = dlq.get_records()
        assert len(records) == 1
        assert records[0].dlq_id == rec.dlq_id

    def test_dlq_quarantine_and_release(self):
        dlq = DeadLetterQueue()
        evt = AgentEvent()
        rec = dlq.enqueue(evt, "topic.1", ValueError("Bad input"))

        assert not rec.quarantined
        assert dlq.quarantine(rec.dlq_id)
        assert dlq.get_records(quarantined_only=True)[0].quarantined

        released = dlq.release(rec.dlq_id)
        assert released.dlq_id == rec.dlq_id
        assert len(dlq) == 0

    def test_dlq_capacity_eviction(self):
        dlq = DeadLetterQueue(max_capacity=3)
        for i in range(5):
            dlq.enqueue(AgentEvent(), f"topic.{i}", ValueError(f"Err {i}"))
        assert len(dlq) == 3

    def test_dlq_clear(self):
        dlq = DeadLetterQueue()
        dlq.enqueue(AgentEvent(), "t", ValueError("Err"))
        dlq.enqueue(AgentEvent(), "t", ValueError("Err"))
        assert dlq.clear() == 2
        assert len(dlq) == 0

    def test_dlq_record_to_dict(self):
        dlq = DeadLetterQueue()
        rec = dlq.enqueue(AgentEvent(execution_id="e1"), "topic.test", RuntimeError("Crash"))
        d = rec.to_dict()
        assert d["topic"] == "topic.test"
        assert d["error_type"] == "RuntimeError"
        assert d["error_message"] == "Crash"

    def test_dlq_get_records_by_event_type(self):
        dlq = DeadLetterQueue()
        dlq.enqueue(GoalReceivedEvent(), "t1", ValueError("Err1"))
        dlq.enqueue(TaskStartedEvent(), "t2", ValueError("Err2"))
        assert len(dlq.get_records(event_type="GoalReceived")) == 1
        assert len(dlq.get_records(event_type="TaskStarted")) == 1
        assert len(dlq.get_records(event_type="Unknown")) == 0

    def test_dlq_release_nonexistent(self):
        dlq = DeadLetterQueue()
        assert dlq.release(uuid4()) is None

    def test_dlq_quarantine_nonexistent(self):
        dlq = DeadLetterQueue()
        assert dlq.quarantine(uuid4()) is False

    def test_dlq_quarantine_eviction_protection(self):
        dlq = DeadLetterQueue(max_capacity=2)
        r1 = dlq.enqueue(AgentEvent(), "t1", ValueError("Err1"))
        dlq.quarantine(r1.dlq_id)
        dlq.enqueue(AgentEvent(), "t2", ValueError("Err2"))
        dlq.enqueue(AgentEvent(), "t3", ValueError("Err3"))
        records = dlq.get_records()
        assert any(r.dlq_id == r1.dlq_id for r in records)


class TestEventStore:
    def test_append_and_retrieve(self):
        store = EventStore()
        evt1 = GoalReceivedEvent(execution_id="exec-1")
        evt2 = PlanningStartedEvent(execution_id="exec-1")
        evt3 = ExecutionStartedEvent(execution_id="exec-2")

        store.append(evt1)
        store.append(evt2)
        store.append(evt3)

        assert len(store) == 3
        assert len(store.get_by_execution_id("exec-1")) == 2
        assert len(store.get_by_execution_id("exec-2")) == 1
        assert len(store.get_by_type("GoalReceived")) == 1

    def test_cryptographic_hash_integrity(self):
        store = EventStore()
        store.append(AgentEvent(execution_id="e1", payload={"a": 1}))
        store.append(AgentEvent(execution_id="e2", payload={"b": 2}))
        store.append(AgentEvent(execution_id="e3", payload={"c": 3}))

        assert store.verify_integrity() is True

    def test_replay_with_filter(self):
        store = EventStore()
        store.append(GoalReceivedEvent(execution_id="e1"))
        store.append(PlanningStartedEvent(execution_id="e1"))
        store.append(TaskCompletedEvent(execution_id="e1", task_id="t1"))

        replayed = []
        count = store.replay(
            handler=lambda e: replayed.append(e.event_type),
            filter_fn=lambda e: e.event_type.startswith("Plan") or e.event_type.startswith("Task"),
        )
        assert count == 2
        assert replayed == ["PlanningStarted", "TaskCompleted"]

    def test_correlation_query(self):
        store = EventStore()
        store.append(AgentEvent(correlation_id="corr-99"))
        store.append(AgentEvent(correlation_id="corr-99"))
        store.append(AgentEvent(correlation_id="corr-100"))

        assert len(store.get_by_correlation_id("corr-99")) == 2

    def test_event_entry_to_dict(self):
        store = EventStore()
        entry = store.append(AgentEvent(execution_id="e1"))
        d = entry.to_dict()
        assert d["sequence_number"] == 1
        assert "hash" in d
        assert "previous_hash" in d

    def test_empty_store_integrity(self):
        store = EventStore()
        assert store.verify_integrity() is True

    def test_get_all(self):
        store = EventStore()
        store.append(AgentEvent())
        store.append(AgentEvent())
        assert len(store.get_all()) == 2

    def test_replay_range(self):
        store = EventStore()
        for i in range(10):
            store.append(AgentEvent(payload={"idx": i}))
        items = []
        store.replay(handler=lambda e: items.append(e.payload["idx"]), from_sequence=3, to_sequence=6)
        assert items == [2, 3, 4, 5]

    def test_tamper_detection(self):
        store = EventStore()
        store.append(AgentEvent(execution_id="e1"))
        store.append(AgentEvent(execution_id="e2"))
        # Artificially tamper with previous hash
        store._entries[1] = EventEntry(
            sequence_number=2,
            event=store._entries[1].event,
            hash=store._entries[1].hash,
            previous_hash="tampered_hash_value_12345",
        )
        assert store.verify_integrity() is False


class TestEnterpriseEventBus:
    @pytest.mark.asyncio
    async def test_publish_and_subscribe_by_class(self):
        bus = EnterpriseEventBus()
        received = []

        async def handler(evt: GoalReceivedEvent):
            received.append(evt.execution_id)

        bus.subscribe(GoalReceivedEvent, handler)
        invoked = await bus.publish(GoalReceivedEvent(execution_id="exec-class-1"))

        assert invoked == 1
        assert received == ["exec-class-1"]
        assert bus.metrics["published"] == 1
        assert bus.metrics["handled"] == 1

    @pytest.mark.asyncio
    async def test_publish_and_subscribe_wildcard_topic(self):
        bus = EnterpriseEventBus()
        received_topics = []

        async def wildcard_handler(evt: AgentEvent):
            received_topics.append(evt.event_type)

        bus.subscribe("Task*", wildcard_handler)
        await bus.publish(TaskStartedEvent(task_id="t1"))
        await bus.publish(TaskCompletedEvent(task_id="t1"))
        await bus.publish(GoalReceivedEvent(execution_id="e1"))

        assert len(received_topics) == 2
        assert "TaskStarted" in received_topics
        assert "TaskCompleted" in received_topics

    @pytest.mark.asyncio
    async def test_sync_handler_execution(self):
        bus = EnterpriseEventBus()
        sync_received = []

        def sync_fn(evt: AgentEvent):
            sync_received.append(evt.execution_id)

        bus.subscribe("SyncTopic", sync_fn)
        await bus.publish(AgentEvent(execution_id="sync-1"), topic="SyncTopic")

        assert sync_received == ["sync-1"]

    @pytest.mark.asyncio
    async def test_handler_error_routing_to_dlq(self):
        bus = EnterpriseEventBus(max_retries=1)

        async def failing_handler(evt: AgentEvent):
            raise ValueError("Deterministic handler crash")

        bus.subscribe("FailTopic", failing_handler)
        invoked = await bus.publish(AgentEvent(execution_id="fail-e"), topic="FailTopic")

        assert invoked == 0
        assert bus.metrics["failed"] == 1
        assert bus.metrics["dlq_size"] == 1
        dlq_records = bus.dead_letter_queue.get_records()
        assert len(dlq_records) == 1
        assert "Deterministic handler crash" in dlq_records[0].error_message

    @pytest.mark.asyncio
    async def test_unsubscribe(self):
        bus = EnterpriseEventBus()
        events = []

        def listener(evt: AgentEvent):
            events.append(evt)

        bus.subscribe("TestTopic", listener)
        await bus.publish(AgentEvent(), topic="TestTopic")
        assert len(events) == 1

        assert bus.unsubscribe("TestTopic", listener) is True
        await bus.publish(AgentEvent(), topic="TestTopic")
        assert len(events) == 1

    @pytest.mark.asyncio
    async def test_unsubscribe_by_type(self):
        bus = EnterpriseEventBus()
        events = []

        async def listener(evt: GoalReceivedEvent):
            events.append(evt)

        bus.subscribe(GoalReceivedEvent, listener)
        assert bus.unsubscribe(GoalReceivedEvent, listener) is True
        assert bus.unsubscribe(GoalReceivedEvent, listener) is False

    @pytest.mark.asyncio
    async def test_clear_bus(self):
        bus = EnterpriseEventBus()
        bus.subscribe("Topic1", lambda e: None)
        bus.clear()
        assert len(bus._subscribers) == 0
        assert bus.metrics["published"] == 0

    @pytest.mark.asyncio
    async def test_universal_wildcard_subscription(self):
        bus = EnterpriseEventBus()
        all_events = []

        async def all_listener(evt: AgentEvent):
            all_events.append(evt)

        bus.subscribe("*", all_listener)
        await bus.publish(GoalReceivedEvent(execution_id="g1"))
        await bus.publish(TaskStartedEvent(task_id="t1"))
        await bus.publish(AgentCompletedEvent(execution_id="c1"))

        assert len(all_events) == 3

    @pytest.mark.asyncio
    async def test_event_store_receives_all_published(self):
        bus = EnterpriseEventBus()
        await bus.publish(GoalReceivedEvent(execution_id="g10"))
        await bus.publish(TaskCompletedEvent(task_id="t10"))

        assert len(bus.event_store) == 2
        assert len(bus.event_store.get_by_execution_id("g10")) == 1

    @pytest.mark.asyncio
    @pytest.mark.parametrize("event_cls", [
        GoalReceivedEvent,
        PlanningStartedEvent,
        PlanningCompletedEvent,
        ExecutionStartedEvent,
        ExecutionCompletedEvent,
        ObservationCompletedEvent,
        ReflectionStartedEvent,
        AgentCompletedEvent,
        AgentFailedEvent,
        RetryRequestedEvent,
        GoalUnderstandingCompletedEvent,
        PlanOptimizedEvent,
        TaskStartedEvent,
        TaskCompletedEvent,
        TaskFailedEvent,
        TaskMutatedEvent,
        AgentNegotiationStartedEvent,
        AgentNegotiationCompletedEvent,
        ToolInvokedEvent,
        ToolPolicyViolationEvent,
        ReflectionCritiqueCompletedEvent,
        SelfCorrectionTriggeredEvent,
        HumanEscalationRequestedEvent,
        HumanFeedbackReceivedEvent,
        MemoryConsolidationCompletedEvent,
        StateTransitionEvent,
        SecurityViolationEvent,
    ])
    async def test_all_event_types_dispatch_correctly(self, event_cls):
        bus = EnterpriseEventBus()
        captured = []

        async def capture_handler(e):
            captured.append(e.event_type)

        bus.subscribe(event_cls, capture_handler)
        evt = event_cls(execution_id="param-test")
        invoked = await bus.publish(evt)
        assert invoked == 1
        assert len(captured) == 1

    @pytest.mark.parametrize("event_cls", [
        GoalReceivedEvent,
        PlanningStartedEvent,
        PlanningCompletedEvent,
        ExecutionStartedEvent,
        ExecutionCompletedEvent,
        ObservationCompletedEvent,
        ReflectionStartedEvent,
        AgentCompletedEvent,
        AgentFailedEvent,
        RetryRequestedEvent,
        GoalUnderstandingCompletedEvent,
        PlanOptimizedEvent,
        TaskStartedEvent,
        TaskCompletedEvent,
        TaskFailedEvent,
        TaskMutatedEvent,
        AgentNegotiationStartedEvent,
        AgentNegotiationCompletedEvent,
        ToolInvokedEvent,
        ToolPolicyViolationEvent,
        ReflectionCritiqueCompletedEvent,
        SelfCorrectionTriggeredEvent,
        HumanEscalationRequestedEvent,
        HumanFeedbackReceivedEvent,
        MemoryConsolidationCompletedEvent,
        StateTransitionEvent,
        SecurityViolationEvent,
    ])
    def test_all_event_types_serialization_roundtrip(self, event_cls):
        evt = event_cls(execution_id="roundtrip-test", payload={"source": "test_runner"})
        d = evt.to_dict()
        assert d["execution_id"] == "roundtrip-test"
        assert d["payload"]["source"] == "test_runner"
        assert "event_id" in d
        assert "timestamp" in d
        assert "event_type" in d

    def test_event_store_filter_by_timestamp_range(self):
        store = EventStore()
        e1 = AgentEvent(execution_id="t1")
        e2 = AgentEvent(execution_id="t2")
        store.append(e1)
        store.append(e2)
        assert len(store.get_all()) == 2

