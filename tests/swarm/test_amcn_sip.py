"""
AMCN-SIP Phase 13.8 - Comprehensive Pytest Test Suite
Verifies all 10 core subsystems:
1. Agent Profiles & Lifecycle State Machine
2. Dynamic Discovery & Semantic Routing
3. Swarm Communication Bus (5 messaging topologies)
4. Multi-Objective Negotiation & Conflict Resolution
5. Consensus Voting Engine (4 consensus strategies)
6. Dynamic Coalition Formation & Team Optimization
7. Task Auction Marketplace & Bid Evaluation
8. Multi-Dimensional Reputation & Pairwise Trust
9. Swarm Collective Learning & Pattern Mining
10. Swarm Governance, Replay Integrity & REST APIs
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.runtime.swarm import (
    AgentRole,
    AgentState,
    SwarmAgentProfile,
    AgentRegistry,
    AgentLifecycleManager,
    AgentDirectory,
    MessageType,
    SwarmMessage,
    CommunicationBus,
    NegotiationOffer,
    NegotiationEngine,
    ConsensusVotingMode,
    SwarmVote,
    ConsensusEngine,
    CoalitionManager,
    AuctionType,
    MarketplaceTask,
    AgentBid,
    TaskMarketplace,
    ReputationEngine,
    CollectiveLearningEngine,
    SwarmGovernanceEngine,
    CoordinationReplayEngine,
)


@pytest.fixture
def client():
    return TestClient(app)


def test_agent_registry_and_lifecycle():
    registry = AgentRegistry()
    lifecycle = AgentLifecycleManager()

    # Initial seeding verification
    agents = registry.list_agents()
    assert len(agents) >= 6

    # Test registration of new agent
    new_agent = SwarmAgentProfile(
        agent_id="test-agent-99",
        name="Test Reviewer",
        role=AgentRole.REVIEWER,
        capabilities=["code_review", "audit"],
        tools=["diff_viewer"],
        max_concurrency=2,
        compute_cost_per_sec=0.03,
    )
    registry.register_agent(new_agent)
    assert registry.get_agent("test-agent-99") is not None
    assert new_agent.state == AgentState.REGISTERED

    # Test valid state transition: REGISTERED -> AVAILABLE
    ok, msg = lifecycle.transition(registry, "test-agent-99", AgentState.AVAILABLE, "Activated by orchestrator")
    assert ok is True
    assert registry.get_agent("test-agent-99").state == AgentState.AVAILABLE

    # Test valid state transition: AVAILABLE -> NEGOTIATING
    ok, msg = lifecycle.transition(registry, "test-agent-99", AgentState.NEGOTIATING, "Entering SLA bargaining")
    assert ok is True
    assert registry.get_agent("test-agent-99").state == AgentState.NEGOTIATING

    # Test invalid state transition: NEGOTIATING -> REGISTERED (not allowed)
    ok, msg = lifecycle.transition(registry, "test-agent-99", AgentState.REGISTERED, "Invalid reverse step")
    assert ok is False


def test_agent_directory_and_discovery():
    registry = AgentRegistry()
    directory = AgentDirectory(registry)

    # Discover OCR specialist
    ocr_agent = directory.discover_agent("ocr_extraction")
    assert ocr_agent is not None
    assert ocr_agent.role == AgentRole.SPECIALIST

    # Fallback discovery
    fallback = directory.fallback_discovery()
    assert fallback is not None


def test_swarm_communication_bus():
    bus = CommunicationBus()

    # Direct message
    msg = SwarmMessage(
        message_id="msg_test_01",
        sender_id="agent-exec-01",
        recipient_id="agent-plan-01",
        message_type=MessageType.DIRECT,
        payload={"command": "DECOMPOSE_MISSION", "mission_id": "m_100"},
        conversation_id="conv_m100",
    )
    ok, err = bus.send_message(msg)
    assert ok is True

    # Broadcast message
    b_msg = SwarmMessage(
        message_id="msg_test_02",
        sender_id="agent-exec-01",
        message_type=MessageType.BROADCAST,
        payload={"notice": "GLOBAL_QUOTA_RESET"},
    )
    ok, err = bus.send_message(b_msg)
    assert ok is True

    # Context sharing
    bus.context_exchange.publish_context("conv_m100", "task_budget", 500.0)
    assert bus.context_exchange.get_context("conv_m100", "task_budget") == 500.0


def test_multi_objective_negotiation():
    engine = NegotiationEngine()

    offer = NegotiationOffer(
        offer_id="off_test_1",
        proposer_id="agent-coord-01",
        receiver_id="agent-spec-ocr",
        topic="SLA_ALLOCATION",
        demands={"max_latency_ms": 150.0, "max_cost": 50.0},
        concessions={"sla_leniency": 0.05, "bonus_reputation": 0.02},
        priority=2,
    )
    agreement = engine.propose_offer(offer)
    assert agreement is not None
    assert agreement.proposer_id == "agent-coord-01"
    assert agreement.receiver_id == "agent-spec-ocr"
    assert agreement.agreement_hash != ""
    assert agreement.settled_terms["conceded"] is True

    # Test agreement retrieval
    agreements = engine.get_all_agreements()
    assert len(agreements) >= 1


def test_consensus_voting_engine():
    engine = ConsensusEngine()

    voters = ["agent-exec-01", "agent-plan-01", "agent-val-sec"]
    decision = engine.initiate_voting(
        decision_id="dec_test_01",
        proposal="UPGRADE_EXTRACTION_MODEL_V2",
        voting_mode=ConsensusVotingMode.WEIGHTED_REPUTATION,
        eligible_voters=voters,
        quorum_threshold=0.5,
    )
    assert decision.status == "IN_PROGRESS"

    # Cast votes
    ok, msg = engine.cast_vote("dec_test_01", SwarmVote("agent-exec-01", "dec_test_01", "APPROVE", 1.0, "Approved"))
    assert ok is True
    ok, msg = engine.cast_vote("dec_test_01", SwarmVote("agent-plan-01", "dec_test_01", "APPROVE", 1.0, "Optimal path"))
    assert ok is True

    final = engine.finalize_decision("dec_test_01")
    assert final.verdict == "APPROVED"
    assert final.tally_score >= 0.5


def test_coalition_manager_and_optimization():
    manager = CoalitionManager()
    registry = AgentRegistry()

    # Create coalition
    coalition = manager.create_coalition(
        coalition_id="coal_test_01",
        name="Strike Team Alpha",
        mission_id="m_9001",
        lead_agent_id="agent-exec-01",
        member_agent_ids=["agent-plan-01", "agent-spec-ocr"],
        objective="High throughput document pipeline",
    )
    assert coalition.coalition_id == "coal_test_01"
    assert len(coalition.member_agent_ids) == 2

    # Team optimization
    all_agents = registry.list_agents()
    team = manager.optimizer.optimize_team(all_agents, ["ocr_extraction", "security_verification"])
    assert len(team) >= 2


def test_task_auction_marketplace():
    marketplace = TaskMarketplace()

    task = MarketplaceTask(
        task_id="task_mkt_01",
        name="High Speed Tokenization",
        description="Tokenize 50,000 legal contracts",
        required_skills=["tokenization"],
        max_budget=100.0,
        deadline_sec=30.0,
    )
    auction = marketplace.publish_task(task, AuctionType.FIRST_PRICE_SEALED)
    assert auction.status == "OPEN"

    # Submit bids
    bid1 = AgentBid("bid_1", auction.auction_id, "agent-spec-ocr", 80.0, 150.0, 0.98)
    bid2 = AgentBid("bid_2", auction.auction_id, "agent-res-opt", 60.0, 180.0, 0.95)

    marketplace.submit_bid(auction.auction_id, bid1)
    marketplace.submit_bid(auction.auction_id, bid2)

    winning = marketplace.evaluate_and_award(auction.auction_id)
    assert winning is not None
    assert winning.bidder_agent_id in ("agent-spec-ocr", "agent-res-opt")
    assert auction.status == "AWARDED"


def test_reputation_and_trust_graph():
    rep_engine = ReputationEngine()

    initial = rep_engine.get_reputation("agent-spec-ocr")
    assert initial is not None
    init_acc = initial.accuracy_score

    # Record success
    rep_engine.record_performance("agent-spec-ocr", task_success=True, sla_met=True, governance_clean=True)
    updated = rep_engine.get_reputation("agent-spec-ocr")
    assert updated.accuracy_score >= init_acc

    # Trust matrix
    rep_engine.trust_engine.update_pairwise_trust("agent-spec-ocr", "agent-val-sec", 0.05)
    score = rep_engine.trust_engine.get_trust_score("agent-spec-ocr", "agent-val-sec")
    assert score > 0.85


def test_swarm_collective_learning():
    learning = CollectiveLearningEngine()

    summary = learning.get_collective_learning_summary()
    assert summary["knowledge_graph"]["total_nodes"] >= 6
    assert len(summary["patterns"]) >= 3
    assert summary["total_insights_mined"] >= 2


def test_swarm_governance_and_replay():
    gov = SwarmGovernanceEngine()
    replay = CoordinationReplayEngine()

    # Valid delegation
    ok, grant, msg = gov.grant_delegation(
        delegator_id="agent-exec-01",
        delegator_role="EXECUTIVE",
        delegatee_id="agent-coord-01",
        delegatee_role="COORDINATOR",
        scope="TASK_DELEGATION",
        depth=1,
    )
    assert ok is True
    assert grant.grant_signature != ""

    # Usurpation prevention: operator cannot delegate to executive
    ok, grant, msg = gov.grant_delegation(
        delegator_id="agent-spec-ocr",
        delegator_role="SPECIALIST",
        delegatee_id="agent-exec-01",
        delegatee_role="EXECUTIVE",
        scope="MISSION_COMMAND",
        depth=1,
    )
    assert ok is False

    # Replay trace verification
    trace = replay.reconstruct_trace()
    assert trace["total_frames"] >= 5
    assert trace["integrity_merkle_root"] != ""


def test_swarm_rest_endpoints(client):
    # Overview
    res = client.get("/api/v1/swarm/overview")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "SWARM_SOCIETY_HEALTHY"
    assert data["total_agents"] >= 6

    # List agents
    res = client.get("/api/v1/swarm/agents")
    assert res.status_code == 200
    agents = res.json()
    assert len(agents) >= 6

    # Discover agent
    res = client.post("/api/v1/swarm/agents/discover", json={"capability": "ocr_extraction"})
    assert res.status_code == 200
    assert "agent" in res.json()

    # Marketplace list
    res = client.get("/api/v1/swarm/marketplace/auctions")
    assert res.status_code == 200

    # Reputation list
    res = client.get("/api/v1/swarm/reputation/scores")
    assert res.status_code == 200

    # Trust graph
    res = client.get("/api/v1/swarm/reputation/trust-graph")
    assert res.status_code == 200
    assert "edges" in res.json()

    # Governance summary
    res = client.get("/api/v1/swarm/governance/summary")
    assert res.status_code == 200
    assert "policy" in res.json()

    # Replay timeline
    res = client.get("/api/v1/swarm/replay/timeline")
    assert res.status_code == 200
    assert len(res.json()) >= 1
