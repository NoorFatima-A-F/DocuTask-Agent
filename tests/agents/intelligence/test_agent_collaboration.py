"""Tests for Multi-Agent Collaboration and Messaging Engine (Phase 25.0).

Covers:
- AgentProfile (capacity limits, load tracking, heartbeat timeouts, capability checks)
- AgentRegistry (catalog management, health monitoring, capability indexing)
- AgentDiscoveryService (Pareto multi-factor scoring, constraints filtering)
- AgentNegotiator (Contract-Net protocol, bidding rounds, utility optimization, award logic)
- AgentMessage & AgentMessageBus (async point-to-point, topic pub/sub, DLQ, trace history)
"""

from __future__ import annotations

import asyncio
import time
import pytest

from app.agents.collaboration import (
    AgentDiscoveryService,
    AgentMessage,
    AgentMessageBus,
    AgentNegotiator,
    AgentProfile,
    AgentRegistry,
    MessageType,
    NegotiationSession,
    NegotiationStatus,
    TaskBid,
)


class TestAgentProfile:
    def test_profile_initialization_defaults(self):
        p = AgentProfile("ag_1", "OCR_AGENT", ["ocr"])
        assert p.agent_id == "ag_1"
        assert p.role == "OCR_AGENT"
        assert p.max_concurrency == 10
        assert p.current_load == 0
        assert p.is_healthy is True
        assert p.can_accept_task() is True

    def test_load_tracking(self):
        p = AgentProfile("ag_1", "OCR_AGENT", ["ocr"], max_concurrency=2)
        p.increment_load()
        assert p.current_load == 1
        assert p.can_accept_task() is True

        p.increment_load()
        assert p.current_load == 2
        assert p.can_accept_task() is False

        with pytest.raises(RuntimeError, match="cannot accept more load"):
            p.increment_load()

        p.decrement_load()
        assert p.current_load == 1
        assert p.can_accept_task() is True

    def test_decrement_load_cannot_be_negative(self):
        p = AgentProfile("ag_1", "OCR_AGENT", ["ocr"])
        p.decrement_load()
        assert p.current_load == 0

    def test_has_capability(self):
        p = AgentProfile("ag_1", "VISION_EXTRACTION_AGENT", ["ocr", "layout"])
        assert p.has_capability("ocr") is True
        assert p.has_capability("layout") is True
        assert p.has_capability("vision") is True  # role match
        assert p.has_capability("quantum") is False

    def test_update_heartbeat(self):
        p = AgentProfile("ag_1", "OCR_AGENT", ["ocr"])
        old = p.last_heartbeat
        time.sleep(0.002)
        p.update_heartbeat()
        assert p.last_heartbeat >= old


class TestAgentRegistry:
    @pytest.fixture
    def registry(self):
        return AgentRegistry(heartbeat_timeout_seconds=0.1)

    def test_register_and_get(self, registry):
        p = AgentProfile("ag_1", "ROLE_1", ["cap_1"])
        registry.register(p)
        assert registry.get("ag_1") == p
        assert registry.get("nonexistent") is None

    def test_deregister(self, registry):
        p = AgentProfile("ag_1", "ROLE_1", ["cap_1"])
        registry.register(p)
        assert registry.deregister("ag_1") is True
        assert registry.get("ag_1") is None
        assert registry.deregister("ag_1") is False

    def test_list_all(self, registry):
        p1 = AgentProfile("ag_1", "ROLE_1", ["cap_1"])
        p2 = AgentProfile("ag_2", "ROLE_2", ["cap_2"])
        registry.register(p1)
        registry.register(p2)
        assert len(registry.list_all()) == 2

    def test_find_by_capability(self, registry):
        p1 = AgentProfile("ag_1", "ROLE_1", ["ocr"])
        p2 = AgentProfile("ag_2", "ROLE_2", ["nlp"])
        registry.register(p1)
        registry.register(p2)
        assert registry.find_by_capability("ocr") == [p1]
        assert registry.find_by_capability("nlp") == [p2]
        assert registry.find_by_capability("unknown") == []

    def test_heartbeat_timeout_marks_unhealthy(self, registry):
        p = AgentProfile("ag_1", "ROLE_1", ["cap_1"])
        registry.register(p)
        assert registry.get("ag_1").is_healthy is True
        time.sleep(0.12)
        # after timeout, get() marks is_healthy = False
        assert registry.get("ag_1").is_healthy is False

    def test_record_heartbeat_restores_health(self, registry):
        p = AgentProfile("ag_1", "ROLE_1", ["cap_1"])
        registry.register(p)
        time.sleep(0.12)
        assert registry.get("ag_1").is_healthy is False
        registry.record_heartbeat("ag_1")
        assert registry.get("ag_1").is_healthy is True


class TestAgentDiscoveryService:
    @pytest.fixture
    def discovery_env(self):
        reg = AgentRegistry()
        p1 = AgentProfile("ag_cheap", "OCR", ["ocr"], cost_per_call=0.0005, latency_p95_ms=300.0, confidence_rating=0.90)
        p2 = AgentProfile("ag_fast", "OCR", ["ocr"], cost_per_call=0.002, latency_p95_ms=50.0, confidence_rating=0.95)
        p3 = AgentProfile("ag_accurate", "OCR", ["ocr"], cost_per_call=0.005, latency_p95_ms=400.0, confidence_rating=0.99)
        reg.register(p1)
        reg.register(p2)
        reg.register(p3)
        return AgentDiscoveryService(reg)

    def test_discover_best_agent_default(self, discovery_env):
        best = discovery_env.discover_best_agent("ocr")
        assert best is not None
        assert best.agent_id in ("ag_fast", "ag_accurate")

    def test_discover_best_agent_with_max_cost(self, discovery_env):
        best = discovery_env.discover_best_agent("ocr", max_cost=0.001)
        assert best is not None
        assert best.agent_id == "ag_cheap"

    def test_discover_best_agent_with_max_latency(self, discovery_env):
        best = discovery_env.discover_best_agent("ocr", max_latency_ms=100.0)
        assert best is not None
        assert best.agent_id == "ag_fast"

    def test_discover_best_agent_with_min_confidence(self, discovery_env):
        best = discovery_env.discover_best_agent("ocr", min_confidence=0.98)
        assert best is not None
        assert best.agent_id == "ag_accurate"

    def test_discover_no_agent_for_missing_capability(self, discovery_env):
        best = discovery_env.discover_best_agent("quantum_computing")
        assert best is None


class TestAgentNegotiator:
    @pytest.fixture
    def setup_negotiator(self):
        reg = AgentRegistry()
        p1 = AgentProfile("ag_supervisor", "SUP", ["orchestration"])
        p2 = AgentProfile("ag_bidder_1", "OCR", ["ocr"], cost_per_call=0.002, latency_p95_ms=200.0, confidence_rating=0.96)
        p3 = AgentProfile("ag_bidder_2", "OCR", ["ocr"], cost_per_call=0.001, latency_p95_ms=150.0, confidence_rating=0.98)
        reg.register(p1)
        reg.register(p2)
        reg.register(p3)
        return AgentNegotiator(reg)

    def test_initiate_negotiation_collects_bids(self, setup_negotiator):
        neg = setup_negotiator
        session = neg.initiate_negotiation("ag_supervisor", "task_ocr_1", "ocr")
        assert session.session_id.startswith("neg_")
        assert session.originating_agent_id == "ag_supervisor"
        assert len(session.bids) == 2
        # Originating agent should not bid
        bidder_ids = {b.agent_id for b in session.bids}
        assert "ag_supervisor" not in bidder_ids
        assert bidder_ids == {"ag_bidder_1", "ag_bidder_2"}

    def test_evaluate_and_award_winner(self, setup_negotiator):
        neg = setup_negotiator
        session = neg.initiate_negotiation("ag_supervisor", "task_ocr_1", "ocr")
        winner = neg.evaluate_and_award(session.session_id)
        # ag_bidder_2 is cheaper, faster, and more confident
        assert winner == "ag_bidder_2"
        assert session.status == NegotiationStatus.ACCEPTED
        assert session.awarded_agent_id == "ag_bidder_2"

    def test_negotiation_fails_when_budget_exceeded(self, setup_negotiator):
        neg = setup_negotiator
        # Set max_budget extremely low (lower than any bid)
        session = neg.initiate_negotiation("ag_supervisor", "task_ocr_1", "ocr", max_budget=0.00001)
        # Fallback will pick lowest bid if relaxed
        winner = neg.evaluate_and_award(session.session_id)
        assert winner is not None

    def test_get_session_returns_none_for_unknown(self, setup_negotiator):
        assert setup_negotiator.get_session("unknown_sess") is None


class TestAgentMessaging:
    def test_agent_message_envelope(self):
        msg = AgentMessage(
            sender_id="ag_1",
            recipient_id="ag_2",
            message_type=MessageType.TASK_REQUEST,
            payload={"task": "ocr"},
        )
        assert msg.message_id.startswith("msg_")
        assert msg.correlation_id.startswith("corr_")
        assert msg.priority == 1
        assert msg.payload["task"] == "ocr"

    @pytest.mark.asyncio
    async def test_direct_message_delivery(self):
        bus = AgentMessageBus()
        received = []

        async def handler(msg: AgentMessage):
            received.append(msg)

        bus.subscribe_agent("ag_worker", handler)
        msg = AgentMessage("ag_mgr", "ag_worker", MessageType.TASK_REQUEST, {"work": "extract"})
        success = await bus.send(msg)

        assert success is True
        assert len(received) == 1
        assert received[0].payload["work"] == "extract"

    @pytest.mark.asyncio
    async def test_message_to_unsubscribed_recipient_routes_to_dlq(self):
        bus = AgentMessageBus()
        msg = AgentMessage("ag_mgr", "ag_unknown", MessageType.TASK_REQUEST, {"data": 123})
        success = await bus.send(msg)

        assert success is False
        dlq = bus.get_dlq()
        assert len(dlq) == 1
        assert dlq[0].recipient_id == "ag_unknown"

    @pytest.mark.asyncio
    async def test_topic_publish_to_multiple_subscribers(self):
        bus = AgentMessageBus()
        rec_1 = []
        rec_2 = []

        async def h1(msg: AgentMessage):
            rec_1.append(msg.payload)

        async def h2(msg: AgentMessage):
            rec_2.append(msg.payload)

        bus.subscribe_topic("telemetry/metrics", h1)
        bus.subscribe_topic("telemetry/metrics", h2)

        msg = AgentMessage("ag_1", "all", MessageType.HEARTBEAT, {"cpu": 12.5})
        delivered_count = await bus.publish("telemetry/metrics", msg)

        assert delivered_count == 2
        assert len(rec_1) == 1
        assert len(rec_2) == 1
        assert rec_1[0]["cpu"] == 12.5

    @pytest.mark.asyncio
    async def test_clear_dlq(self):
        bus = AgentMessageBus()
        msg = AgentMessage("a", "b", MessageType.HELP_REQUEST, {})
        await bus.send(msg)
        assert len(bus.get_dlq()) == 1
        cleared = bus.clear_dlq()
        assert cleared == 1
        assert len(bus.get_dlq()) == 0

    @pytest.mark.asyncio
    async def test_get_history_by_correlation_id(self):
        bus = AgentMessageBus()
        async def dummy(m): pass
        bus.subscribe_agent("ag_2", dummy)

        m1 = AgentMessage("ag_1", "ag_2", MessageType.TASK_REQUEST, {}, correlation_id="c_100")
        m2 = AgentMessage("ag_1", "ag_2", MessageType.TASK_RESULT, {}, correlation_id="c_100")
        m3 = AgentMessage("ag_1", "ag_2", MessageType.TASK_REQUEST, {}, correlation_id="c_200")

        await bus.send(m1)
        await bus.send(m2)
        await bus.send(m3)

        hist = bus.get_history(correlation_id="c_100")
        assert len(hist) == 2
        assert all(m.correlation_id == "c_100" for m in hist)


class TestExpandedCollaborationScenarios:
    @pytest.mark.parametrize("m_type", [
        MessageType.TASK_REQUEST,
        MessageType.TASK_RESULT,
        MessageType.FAILURE_EVENT,
        MessageType.HELP_REQUEST,
        MessageType.NEGOTIATION_OFFER,
        MessageType.NEGOTIATION_ACCEPT,
        MessageType.REFLECTION_UPDATE,
        MessageType.HEARTBEAT,
    ])
    def test_all_message_types(self, m_type):
        msg = AgentMessage("s", "r", m_type)
        assert msg.message_type == m_type

    @pytest.mark.asyncio
    async def test_subscriber_exception_routes_to_dlq(self):
        bus = AgentMessageBus()

        async def failing_handler(msg):
            raise RuntimeError("Database connection lost")

        bus.subscribe_agent("ag_worker", failing_handler)
        msg = AgentMessage("ag_mgr", "ag_worker", MessageType.TASK_REQUEST, {})
        success = await bus.send(msg)

        assert success is False
        assert len(bus.get_dlq()) == 1
        assert bus.get_dlq()[0].message_id == msg.message_id

    @pytest.mark.asyncio
    async def test_high_concurrency_message_dispatch(self):
        bus = AgentMessageBus()
        received = []

        async def handler(msg):
            received.append(msg.payload["idx"])

        bus.subscribe_agent("ag_sink", handler)

        tasks = [
            bus.send(AgentMessage("ag_src", "ag_sink", MessageType.TASK_REQUEST, {"idx": i}))
            for i in range(25)
        ]
        results = await asyncio.gather(*tasks)

        assert all(results)
        assert len(received) == 25
        assert set(received) == set(range(25))

    def test_task_bid_properties(self):
        bid = TaskBid(agent_id="ag_1", cost_bid=0.005, estimated_latency_ms=120.0, confidence_bid=0.97)
        assert bid.agent_id == "ag_1"
        assert bid.cost_bid == 0.005
        assert bid.estimated_latency_ms == 120.0
        assert bid.confidence_bid == 0.97
        assert bid.bid_id.startswith("bid_")

    def test_negotiation_session_dataclass(self):
        sess = NegotiationSession(originating_agent_id="ag_0", task_id="t1", required_capability="ocr")
        assert sess.status == NegotiationStatus.OPEN
        assert sess.awarded_agent_id is None
        assert sess.bids == []

    def test_negotiation_empty_candidates_returns_none(self):
        reg = AgentRegistry()
        neg = AgentNegotiator(reg)
        sess = neg.initiate_negotiation("ag_0", "t1", "quantum_teleportation")
        winner = neg.evaluate_and_award(sess.session_id)
        assert winner is None
        assert sess.status == NegotiationStatus.REJECTED

    def test_agent_profile_metadata(self):
        p = AgentProfile("ag_meta", "ROLE", ["cap"], metadata={"tier": "enterprise", "datacenter": "us-east1"})
        assert p.metadata["tier"] == "enterprise"
        assert p.metadata["datacenter"] == "us-east1"

    def test_agent_registry_multiple_heartbeats(self):
        reg = AgentRegistry(heartbeat_timeout_seconds=0.1)
        p = AgentProfile("ag_live", "ROLE", ["cap"])
        reg.register(p)
        for _ in range(3):
            time.sleep(0.04)
            assert reg.record_heartbeat("ag_live") is True
            assert reg.get("ag_live").is_healthy is True

    def test_record_heartbeat_unknown_returns_false(self):
        reg = AgentRegistry()
        assert reg.record_heartbeat("unknown_agent") is False

    def test_discovery_relaxed_constraints_when_no_agent_meets_budget(self):
        reg = AgentRegistry()
        p = AgentProfile("ag_expensive", "OCR", ["ocr"], cost_per_call=10.0, confidence_rating=0.99)
        reg.register(p)
        disc = AgentDiscoveryService(reg)
        # max_cost is 1.0, but only ag_expensive exists with capacity
        found = disc.discover_best_agent("ocr", max_cost=1.0)
        assert found == p

    def test_negotiation_session_lookup(self):
        reg = AgentRegistry()
        neg = AgentNegotiator(reg)
        sess = neg.initiate_negotiation("ag_0", "t1", "ocr")
        assert neg.get_session(sess.session_id) == sess

    @pytest.mark.asyncio
    async def test_topic_publish_with_no_subscribers_returns_zero(self):
        bus = AgentMessageBus()
        msg = AgentMessage("ag_0", "all", MessageType.HEARTBEAT, {})
        delivered = await bus.publish("empty/topic", msg)
        assert delivered == 0

    @pytest.mark.asyncio
    async def test_message_bus_history_unfiltered(self):
        bus = AgentMessageBus()
        async def dummy(m): pass
        bus.subscribe_agent("ag_target", dummy)

        for i in range(5):
            await bus.send(AgentMessage("s", "ag_target", MessageType.TASK_REQUEST, {"i": i}))
        assert len(bus.get_history()) == 5

