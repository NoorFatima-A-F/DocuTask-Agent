"""
Unit and Integration Test Suite for Enterprise Multi-Agent Coordination Framework.
Targeting >=95% meaningful coverage across agent lifecycle, capability matching,
delegation, team formation, protocols, consensus, swarms, work stealing, and adapters.
"""

import pytest
from uuid import uuid4

from app.agents.coordination.agent import Agent
from app.agents.coordination.agent_builder import AgentBuilder
from app.agents.coordination.agent_directory import AgentDirectory
from app.agents.coordination.agent_factory import AgentFactory
from app.agents.coordination.agent_registry import AgentRegistry
from app.agents.coordination.agent_selector import AgentSelector
from app.agents.coordination.auction import AuctionEngine
from app.agents.coordination.builders import DelegationRequestBuilder
from app.agents.coordination.capability_graph import CapabilityGraph
from app.agents.coordination.capability_matcher import (
    CapabilityMatcher,
    CapabilityRequirement,
)
from app.agents.coordination.communication import (
    AgentMessage,
    CommunicationPattern,
)
from app.agents.coordination.consensus import ConsensusEngine, ConsensusOutcome
from app.agents.coordination.context import CoordinationRequest, CoordinationResult
from app.agents.coordination.contract_net import ContractNetEngine
from app.agents.coordination.delegation import (
    DelegationMode,
    DelegationResult,
    DelegationStatus,
)
from app.agents.coordination.delegation_executor import DelegationExecutor
from app.agents.coordination.delegation_planner import DelegationPlanner
from app.agents.coordination.delegation_policy import DelegationPolicy
from app.agents.coordination.distributed_state import DistributedStateStore
from app.agents.coordination.exceptions import (
    CircularDelegationError,
    ConsensusNotReachedError,
    DuplicateAgentIdError,
    InconsistentSharedStateError,
    MissingCapabilityError,
    OrphanedTeamError,
    StaleLeaseError,
)
from app.agents.coordination.factory import CoordinationFactory
from app.agents.coordination.formation import TeamFormationEngine
from app.agents.coordination.leader_election import LeaderElectionEngine
from app.agents.coordination.lease_manager import LeaseManager
from app.agents.coordination.lifecycle import AgentLifecycleState, CoordinationLifecycleState
from app.agents.coordination.message_router import MessageRouter
from app.agents.coordination.metrics import CoordinationMetricsCollector
from app.agents.coordination.negotiation import Bid, NegotiationSession
from app.agents.coordination.serialization import CoordinationSerializer
from app.agents.coordination.shared_context import SharedContext
from app.agents.coordination.swarm import SwarmEngine
from app.agents.coordination.team import Team, TeamType
from app.agents.coordination.telemetry import CoordinationTelemetry
from app.agents.coordination.validators import CoordinationValidator
from app.agents.coordination.voting import AgentVote
from app.agents.coordination.work_stealing import WorkStealingPool


@pytest.fixture
def sample_agents():
    """Provides standard worker and specialist agent instances."""
    a1 = (
        AgentBuilder("ExtractorAlpha")
        .with_role("worker")
        .add_skill("pdf_parsing", domain="document")
        .add_skill("table_extraction", domain="document")
        .add_tool("pdf_parser")
        .with_confidence(0.95)
        .build()
    )
    a2 = (
        AgentBuilder("AnalyzerBeta")
        .with_role("specialist")
        .add_skill("financial_analysis", domain="financial")
        .add_tool("financial_calculator")
        .with_confidence(0.98)
        .build()
    )
    sup = AgentFactory.create_supervisor("MasterSupervisor")
    return [a1, a2, sup]


# ---------------------------------------------------------------------------
# Part 1: Agent Registry & Lifecycle Tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_agent_registry_lifecycle_and_duplicates(sample_agents):
    """Tests agent registration, duplicate rejection, and state transitions."""
    registry = AgentRegistry()
    a1 = sample_agents[0]

    await registry.register(a1)
    assert registry.size() == 1

    # Verify agent state transitioned to AVAILABLE upon registration
    retrieved = await registry.get_by_id(a1.agent_id)
    assert retrieved is not None
    assert retrieved.state == AgentLifecycleState.AVAILABLE

    # Duplicate registration must fail fast
    with pytest.raises(DuplicateAgentIdError):
        await registry.register(a1)

    # Retire agent
    await registry.unregister(a1.agent_id)
    retired = await registry.get_by_id(a1.agent_id)
    assert retired.state == AgentLifecycleState.RETIRED


@pytest.mark.asyncio
async def test_agent_directory_queries(sample_agents):
    """Tests multi-index queries in AgentDirectory."""
    registry = AgentRegistry()
    for a in sample_agents:
        await registry.register(a)

    directory = AgentDirectory(registry)
    workers = await directory.find_by_role("worker")
    assert len(workers) == 1
    assert workers[0].name == "ExtractorAlpha"

    financial_agents = await directory.find_by_skill("financial_analysis")
    assert len(financial_agents) == 1
    assert financial_agents[0].name == "AnalyzerBeta"


# ---------------------------------------------------------------------------
# Part 2: Capability Matching & Discovery Tests
# ---------------------------------------------------------------------------

def test_capability_matcher_and_selector(sample_agents):
    """Tests multi-criteria scoring and selection."""
    matcher = CapabilityMatcher()
    req = CapabilityRequirement(
        required_skills=["pdf_parsing"],
        required_tools=["pdf_parser"]
    )
    results = matcher.match_capabilities(req, sample_agents)
    assert len(results) == 3
    # Top result should be fully qualified ExtractorAlpha
    assert results[0].agent_id == str(sample_agents[0].agent_id)
    assert results[0].is_fully_qualified is True

    selector = AgentSelector()
    best_agent = selector.select_agent(req, sample_agents)
    assert best_agent.name == "ExtractorAlpha"

    # Missing capability exception check
    impossible_req = CapabilityRequirement(required_skills=["quantum_teleportation"])
    with pytest.raises(MissingCapabilityError):
        selector.select_agent(impossible_req, sample_agents)


def test_capability_graph():
    """Tests prerequisite DAG resolution in CapabilityGraph."""
    graph = CapabilityGraph()
    graph.add_capability("financial_analysis", prerequisites=["table_extraction"])
    graph.add_capability("table_extraction", prerequisites=["pdf_parsing"])

    prereqs = graph.get_prerequisites("financial_analysis")
    assert "table_extraction" in prereqs


# ---------------------------------------------------------------------------
# Part 3: Delegation Subsystem Tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_delegation_planner_and_executor(sample_agents):
    """Tests delegation planning, execution, and chain tracking."""
    registry = AgentRegistry()
    for a in sample_agents:
        await registry.register(a)

    planner = DelegationPlanner()
    executor = DelegationExecutor(registry=registry)

    req = (
        DelegationRequestBuilder(delegator_agent_id=sample_agents[2].agent_id)
        .with_mode(DelegationMode.SINGLE)
        .add_task("task_parse", "Parse Document", skills=["pdf_parsing"])
        .build()
    )

    available = await registry.list_available()
    planned_tasks = planner.plan_delegation(req, available)
    assert len(planned_tasks) == 1
    assert planned_tasks[0].assigned_agent_id == sample_agents[0].agent_id

    planned_req = req.model_copy(update={"tasks": planned_tasks})
    result: DelegationResult = await executor.delegate_task(planned_req)

    assert result.status == DelegationStatus.COMPLETED
    assert "task_parse" in result.results
    assert len(result.delegation_chain) >= 2


def test_delegation_policy_circular_detection():
    """Tests detection and rejection of circular delegation chains."""
    policy = DelegationPolicy(max_depth=3)
    id1 = uuid4()
    id2 = uuid4()
    chain = [id1, id2]

    # Re-delegating to id1 creates a cycle
    with pytest.raises(CircularDelegationError):
        policy.validate_delegation_chain(chain, id1)

    # Exceeding depth limit
    id3 = uuid4()
    id4 = uuid4()
    with pytest.raises(CircularDelegationError):
        policy.validate_delegation_chain([id1, id2, id3], id4)


# ---------------------------------------------------------------------------
# Part 4: Team Formation & Swarms Tests
# ---------------------------------------------------------------------------

def test_team_formation_and_integrity(sample_agents):
    """Tests supervisor-led, peer, and dynamic team formation."""
    engine = TeamFormationEngine()
    sup = sample_agents[2]
    workers = sample_agents[:2]

    team = engine.form_supervisor_team("DocProcessingTeam", sup, workers)
    assert team.team_type == TeamType.SUPERVISOR_LED
    assert team.leader_id == sup.agent_id
    assert len(team.members) == 3

    # Integrity validator
    CoordinationValidator.validate_team_integrity(team)

    # Orphaned team failure
    orphaned_team = Team(name="EmptyTeam", members=[])
    with pytest.raises(OrphanedTeamError):
        CoordinationValidator.validate_team_integrity(orphaned_team)


def test_swarm_fan_out_fan_in(sample_agents):
    """Tests swarm fan-out partitioning and fan-in aggregation."""
    engine = SwarmEngine()
    items = ["chunk_1", "chunk_2", "chunk_3", "chunk_4"]
    swarm_workers = sample_agents[:2]

    tasks = engine.fan_out(items, swarm_workers)
    assert len(tasks) == 4
    assert tasks[0].assigned_agent_id == swarm_workers[0].agent_id
    assert tasks[1].assigned_agent_id == swarm_workers[1].agent_id

    # Fan-in reduction
    results = {"t0": 10, "t1": 20, "t2": 30}
    summed = engine.fan_in_aggregate(results, reducer=sum)
    assert summed == 60

    # Ensemble decision
    ensemble_votes = [{"decision": "APPROVE"}, {"decision": "APPROVE"}, {"decision": "REJECT"}]
    winning = engine.ensemble_decision(ensemble_votes)
    assert winning == "APPROVE"


# ---------------------------------------------------------------------------
# Part 5: Communication & Routing Tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_message_router_point_to_point_and_broadcast():
    """Tests point-to-point and broadcast message delivery."""
    router = MessageRouter()
    a1_id = uuid4()
    a2_id = uuid4()
    a3_id = uuid4()

    router.register_endpoint(a1_id)
    router.register_endpoint(a2_id)
    router.register_endpoint(a3_id)

    # Point-to-point
    msg1 = AgentMessage(sender_id=a1_id, recipient_id=a2_id, content={"text": "hello a2"})
    await router.send_message(msg1)

    inbox_a2 = router.receive_messages(a2_id)
    assert len(inbox_a2) == 1
    assert inbox_a2[0].content["text"] == "hello a2"
    assert len(router.receive_messages(a2_id)) == 0  # Inbox drained

    # Broadcast
    b_msg = AgentMessage(
        sender_id=a1_id,
        recipient_id=None,
        pattern=CommunicationPattern.BROADCAST,
        content={"alert": "system update"}
    )
    await router.send_message(b_msg)

    assert len(router.receive_messages(a2_id)) == 1
    assert len(router.receive_messages(a3_id)) == 1
    assert len(router.receive_messages(a1_id)) == 0  # Sender does not receive own broadcast


# ---------------------------------------------------------------------------
# Part 6: Protocols, Auctions, Voting & Consensus Tests
# ---------------------------------------------------------------------------

def test_contract_net_protocol():
    """Tests Call for Proposals, bidding, and proposal scoring."""
    cnp = ContractNetEngine()
    initiator_id = uuid4()
    session = cnp.issue_call_for_proposals(initiator_id, "task_101")

    b1 = Bid(bidder_agent_id=uuid4(), task_id="task_101", proposed_cost_usd=0.05, estimated_duration_ms=500.0)
    b2 = Bid(bidder_agent_id=uuid4(), task_id="task_101", proposed_cost_usd=0.01, estimated_duration_ms=300.0)

    session = session.submit_bid(b1).submit_bid(b2)
    winning_bid = cnp.evaluate_proposals(session)

    assert winning_bid is not None
    assert winning_bid.proposed_cost_usd == 0.01  # Lower cost & duration won


def test_auction_engine():
    """Tests first-price and Vickrey reverse auctions."""
    engine = AuctionEngine()
    session = NegotiationSession(task_id="task_202", initiator_id=uuid4())
    b1 = Bid(bidder_agent_id=uuid4(), task_id="task_202", proposed_cost_usd=10.0, estimated_duration_ms=100.0)
    b2 = Bid(bidder_agent_id=uuid4(), task_id="task_202", proposed_cost_usd=5.0, estimated_duration_ms=100.0)
    session = session.submit_bid(b1).submit_bid(b2)

    winner_first = engine.run_first_price_reverse_auction(session)
    assert winner_first.proposed_cost_usd == 5.0

    winner_vickrey = engine.run_vickrey_reverse_auction(session)
    assert winner_vickrey.proposed_cost_usd == 5.0


@pytest.mark.asyncio
async def test_consensus_and_leader_election(sample_agents):
    """Tests quorum checking, majority voting, and leader election."""
    consensus_engine = ConsensusEngine()
    votes = [
        AgentVote(voter_agent_id=uuid4(), choice="OPTION_A"),
        AgentVote(voter_agent_id=uuid4(), choice="OPTION_A"),
        AgentVote(voter_agent_id=uuid4(), choice="OPTION_B"),
    ]

    outcome: ConsensusOutcome = await consensus_engine.reach_consensus(
        topic="migration_target",
        votes=votes,
        total_cluster_size=3
    )
    assert outcome.agreed_decision == "OPTION_A"
    assert outcome.quorum_met is True

    # Quorum failure check
    with pytest.raises(ConsensusNotReachedError):
        await consensus_engine.reach_consensus(
            topic="upgrade",
            votes=[votes[0]],
            total_cluster_size=5,
            quorum_fraction=0.6
        )

    # Leader election
    election_engine = LeaderElectionEngine()
    leader = await election_engine.elect_leader(sample_agents)
    assert leader is not None


# ---------------------------------------------------------------------------
# Part 7: Shared State, Work Stealing & Leases
# ---------------------------------------------------------------------------

def test_shared_context_and_optimistic_locking():
    """Tests shared context synchronization and distributed state optimistic locking."""
    ctx = SharedContext()
    p_id = uuid4()
    ctx.put("extracted_revenue", 500000.0, producer_id=p_id)
    assert ctx.get("extracted_revenue") == 500000.0

    # Distributed state with optimistic locking
    store = DistributedStateStore()
    entry = store.set_with_optimistic_lock("config", "v1", expected_version=0, agent_id=p_id)
    assert entry.version == 1

    # Conflict on outdated expected version
    with pytest.raises(InconsistentSharedStateError):
        store.set_with_optimistic_lock("config", "v2", expected_version=0, agent_id=p_id)


def test_work_stealing_pool():
    """Tests task work stealing between agent queues."""
    pool = WorkStealingPool()
    a1_id = uuid4()
    a2_id = uuid4()

    pool.enqueue_task(a1_id, "task_1")
    pool.enqueue_task(a1_id, "task_2")
    pool.enqueue_task(a1_id, "task_3")

    assert pool.queue_depth(a1_id) == 3
    # a2 steals task from a1
    stolen = pool.steal_task(thief_agent_id=a2_id)
    assert stolen == "task_3"
    assert pool.queue_depth(a1_id) == 2


def test_lease_manager_concurrency():
    """Tests task lease acquisition, conflict rejection, and release."""
    lm = LeaseManager(default_lease_ttl_seconds=60.0)
    a1_id = uuid4()
    a2_id = uuid4()

    lease = lm.acquire_lease("task_999", a1_id)
    assert lease.holder_agent_id == a1_id

    # a2 cannot acquire while active
    with pytest.raises(StaleLeaseError):
        lm.acquire_lease("task_999", a2_id)

    # Release and reacquire
    lm.release_lease("task_999", a1_id)
    lease_2 = lm.acquire_lease("task_999", a2_id)
    assert lease_2.holder_agent_id == a2_id


# ---------------------------------------------------------------------------
# Part 8: End-to-End Coordination Engine & Runtime
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_coordination_engine_end_to_end(sample_agents):
    """Verifies end-to-end multi-agent coordination workflow."""
    engine = CoordinationFactory.create_engine()
    for a in sample_agents:
        await engine.manager.registry.register(a)

    req = CoordinationRequest(
        goal="Parse financial document tables",
        initiator_agent_id=sample_agents[2].agent_id,
        required_capabilities=["pdf_parsing"]
    )

    result: CoordinationResult = await engine.coordinate(req)

    assert result.lifecycle_state == CoordinationLifecycleState.COMPLETED
    assert len(result.outputs) >= 1
    assert result.statistics.agents_allocated >= 1
    assert not result.errors


@pytest.mark.asyncio
async def test_coordination_runtime_lifecycle(sample_agents):
    """Tests CoordinationRuntime container start and stop."""
    runtime = CoordinationFactory.create_runtime()
    await runtime.start()
    assert runtime.is_running is True

    for a in sample_agents:
        await runtime.engine.manager.registry.register(a)

    req = CoordinationRequest(
        goal="Extract document",
        initiator_agent_id=sample_agents[2].agent_id,
        required_capabilities=["pdf_parsing"]
    )
    res = await runtime.coordinate_goal(req)
    assert res.lifecycle_state == CoordinationLifecycleState.COMPLETED

    await runtime.stop()
    assert runtime.is_running is False


# ---------------------------------------------------------------------------
# Part 9: Serialization & Telemetry Tests
# ---------------------------------------------------------------------------

def test_coordination_serialization_roundtrip(sample_agents):
    """Tests versioned JSON and Pub/Sub serialization."""
    agent = sample_agents[0]
    json_str = CoordinationSerializer.serialize_to_json(agent)
    assert "schema_version" in json_str
    assert "21.0" in json_str

    deserialized: Agent = CoordinationSerializer.deserialize_from_json(json_str, Agent)
    assert deserialized.agent_id == agent.agent_id

    pubsub_msg = CoordinationSerializer.to_pubsub_message(agent)
    assert "data" in pubsub_msg
    assert pubsub_msg["attributes"]["schema_version"] == "21.0"


def test_telemetry_and_metrics():
    """Tests W3C tracecontext generation and Cloud Monitoring export."""
    headers = CoordinationTelemetry.generate_trace_context("corr_123")
    assert "traceparent" in headers
    assert headers["correlation-id"] == "corr_123"

    metrics = CoordinationMetricsCollector()
    metrics.record_delegation_started()
    metrics.record_delegation_completed(150.0)
    metrics.record_message_routed()
    metrics.set_active_teams(2)

    snap = metrics.get_snapshot()
    assert snap.total_delegations_completed == 1
    assert snap.average_delegation_latency_ms == 150.0

    cloud_export = metrics.export_cloud_monitoring()
    assert "custom.googleapis.com/agent/coordination/delegations_completed" in cloud_export
