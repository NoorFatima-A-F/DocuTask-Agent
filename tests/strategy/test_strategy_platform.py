"""
Comprehensive Unit & Integration Test Suite for Phase 13.11:
Autonomous Strategic Cognition, Goal Evolution & Executive Intelligence Platform (ASC-GEEIP).
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.runtime.strategy.events.strategy_events import (
    GoalPriority,
    GoalStatus,
    StrategicHorizon,
    DecisionImportance,
    MissionValue,
    PortfolioStatus,
    NegotiationStatus,
)
from app.runtime.strategy.goal_engine.goal_engine import (
    GoalEvolutionEngine,
    StrategicGoal,
    GoalDependency,
)
from app.runtime.strategy.portfolio.portfolio_engine import (
    MissionPortfolioEngine,
    MissionValueScore,
)
from app.runtime.strategy.roadmap.roadmap_engine import (
    RoadmapEngine,
    RoadmapMilestone,
)
from app.runtime.strategy.executive.executive_engine import (
    ExecutiveReasoningEngine,
    ExecutiveDecision,
)
from app.runtime.strategy.resource_negotiation.resource_negotiation import (
    ResourceNegotiationEngine,
    NegotiationProposal,
)
from app.runtime.strategy.organizational_memory.organization_memory import (
    OrganizationLearningEngine,
    OrganizationKnowledge,
)
from app.runtime.strategy.strategy_simulation.strategy_simulation import (
    StrategicSimulationEngine,
    StrategicScenario,
)
from app.runtime.strategy.decision_engine.decision_engine import (
    DecisionEngine,
    DecisionCandidate,
)
from app.runtime.strategy.runtime.executive_runtime import ExecutiveRuntime


@pytest.fixture
def client():
    return TestClient(app)


def test_goal_hierarchy_and_htn_decomposition():
    engine = GoalEvolutionEngine()
    root = engine.create_goal(
        title="Scale Enterprise Document Pipeline to 500k/day",
        description="Expand multi-swarm architecture with high availability.",
        priority=GoalPriority.CRITICAL,
        horizon=StrategicHorizon.DAYS_90,
        value_type=MissionValue.TRANSFORMATIVE,
        estimated_cost_usd=8000.0,
    )
    assert root.goal_id in engine.tree.all_goals
    assert root.priority == GoalPriority.CRITICAL

    # HTN decomposition
    subtasks = [
        {"title": "Implement Zero-Copy Ring Buffers", "estimated_cost_usd": 2000.0, "expected_latency_reduction_pct": 14.0},
        {"title": "Pre-Warm GPU Tensor Cache", "estimated_cost_usd": 3000.0, "expected_latency_reduction_pct": 20.0},
    ]
    subgoals = engine.decompose_goal(root.goal_id, subtasks)
    assert len(subgoals) == 2
    assert len(root.decomposed_subgoal_ids) == 2
    assert root.status == GoalStatus.REFINING


def test_goal_evolution_reprioritization_and_conflicts():
    engine = GoalEvolutionEngine()
    # Create conflicting goals
    g1 = engine.create_goal(title="Goal 1 Lock Pipeline", description="Hold global lock")
    g2 = engine.create_goal(title="Goal 2 Lock Pipeline", description="Hold global lock")
    g1.dependencies.append(GoalDependency(source_goal_id=g1.goal_id, target_goal_id=g2.goal_id, dependency_type="BLOCKING"))
    g2.dependencies.append(GoalDependency(source_goal_id=g2.goal_id, target_goal_id=g1.goal_id, dependency_type="BLOCKING"))

    conflicts = engine.detect_conflicts()
    assert len(conflicts) >= 1
    assert conflicts[0]["severity"] == "CRITICAL"

    # Run evolution cycle
    result = engine.evolve_generation()
    assert result["total_goals"] >= 2
    assert "active_goals" in result


def test_mission_portfolio_pareto_ranking():
    engine = MissionPortfolioEngine(budget_limit_usd=40000.0)
    m = engine.add_mission(
        cluster_id="cluster-perf",
        name="Speculative Header Cache Expansion",
        category="Performance",
        value_type=MissionValue.EFFICIENCY_GAIN,
        allocated_budget_usd=3000.0,
        expected_gain_usd=9000.0,
        expected_roi=3.0,
        latency_impact_pct=25.0,
        risk_score=0.08,
    )
    assert m.mission_id is not None

    portfolio_dict = engine.optimize_portfolio()
    assert portfolio_dict["status"] in ["BALANCED", "OPTIMAL", "OVERALLOCATED"]
    assert portfolio_dict["total_missions"] >= 3
    assert portfolio_dict["total_allocated_usd"] > 0


def test_strategic_roadmap_generation_all_horizons():
    engine = RoadmapEngine()
    for horizon in [StrategicHorizon.DAYS_30, StrategicHorizon.DAYS_90, StrategicHorizon.DAYS_180, StrategicHorizon.DAYS_365]:
        r = engine.get_roadmap(horizon)
        assert r is not None
        assert r["milestone_count"] >= 1
        assert len(r["critical_path_ids"]) >= 1

    # Custom roadmap generation
    custom = engine.generate_roadmap(
        horizon=StrategicHorizon.DAYS_90,
        title="Custom 90-Day Automation Push",
        theme="Multi-Region Swarm Federation",
        milestones_spec=[
            {"title": "Deploy EU Cluster", "target_day_offset": 30, "duration_days": 10},
            {"title": "Federate Memory Ledgers", "target_day_offset": 60, "duration_days": 15, "dependency_ids": ["ms-1"]},
        ],
    )
    assert custom.roadmap_id is not None
    assert len(custom.milestones) == 2


def test_executive_reasoning_decisions_and_approvals():
    engine = ExecutiveReasoningEngine()
    dec = engine.create_decision(
        title="Approve GPU Node Expansion for Q3 Peak",
        importance=DecisionImportance.TIER_1_EXECUTIVE,
        organizational_impact="Increases peak concurrency 4x.",
        tradeoffs="Incurs $4.5k/mo extra compute cost.",
        expected_roi=3.5,
        utility_score=0.96,
        confidence=0.99,
    )
    assert dec.status == "PENDING"
    assert len(dec.supporting_evidence_hashes) >= 1

    approved = engine.approve_decision(dec.decision_id, approver_key="cso_oracle_node_alpha")
    assert approved.status == "APPROVED"
    assert approved.approver_signature.startswith("secp256k1:")

    # Recommendations
    rec = engine.generate_recommendation(
        target_area="Vector Index Optimization",
        allocated_budget_usd=3500.0,
        expected_gain_pct=22.0,
        strategic_rationale="Quantization reduces latency by 22%.",
    )
    assert rec.recommendation_id is not None
    assert len(engine.list_recommendations()) >= 3


def test_multi_swarm_resource_negotiation_nash_equilibrium():
    engine = ResourceNegotiationEngine()
    proposals = [
        {"swarm_id": "swarm-extraction", "quantity_requested": 30.0, "bid_utility": 0.95, "disagreement_point": 0.2},
        {"swarm_id": "swarm-classification", "quantity_requested": 25.0, "bid_utility": 0.90, "disagreement_point": 0.2},
        {"swarm_id": "swarm-governance", "quantity_requested": 15.0, "bid_utility": 0.92, "disagreement_point": 0.3},
    ]
    session = engine.negotiate_resources(
        resource_type="GPU_VRAM_GB",
        total_capacity=48.0,
        proposals_data=proposals,
    )
    assert session.converged is True
    assert session.nash_product > 0.0
    assert sum(p.quantity_allocated for p in session.proposals) <= 48.01


def test_organizational_memory_playbooks_and_querying():
    engine = OrganizationLearningEngine()
    entries = engine.query_knowledge()
    assert len(entries) >= 5

    # Filter by category
    playbooks = engine.query_knowledge(category="PLAYBOOK")
    assert len(playbooks) >= 1

    # Record new lesson
    new_k = engine.record_knowledge(
        category="LESSON_LEARNED",
        title="Zero-Lock Buffer Migration",
        description="Atomic circular buffers eliminate 98% of telemetry lock stalls.",
        context_tags=["memory", "locks", "telemetry"],
        confidence=0.992,
    )
    assert new_k.entry_id is not None
    fetched = engine.get_knowledge(new_k.entry_id)
    assert fetched is not None
    assert fetched["usage_count"] >= 2


def test_strategy_simulation_multi_horizon():
    engine = StrategicSimulationEngine()
    sims = engine.list_simulations()
    assert len(sims) >= 2

    # Run new simulation
    sim = engine.run_simulation(
        name="Q1 Multi-Datacenter Scaling",
        horizon=StrategicHorizon.DAYS_180,
        budget_delta_usd=8000.0,
        worker_scale_delta=8,
        cache_hit_rate_pct=90.0,
        traffic_growth_pct=200.0,
    )
    assert sim.simulation_id is not None
    assert sim.expected_p95_latency_ms < 280.0
    assert sim.expected_throughput_qps > 1000.0
    assert len(sim.recommended_actions) >= 3


def test_decision_engine_mcda_ranking():
    engine = DecisionEngine()
    rankings = engine.list_rankings()
    assert len(rankings) >= 1

    candidates = [
        {
            "name": "Candidate A: Distributed Speculative Caching",
            "criteria_scores": {"roi_multiplier": 4.0, "latency_reduction_pct": 30.0, "governance_compliance": 0.99, "cost_efficiency": 0.90, "risk_safety": 0.95},
        },
        {
            "name": "Candidate B: Over-Provision Compute Nodes",
            "criteria_scores": {"roi_multiplier": 2.0, "latency_reduction_pct": 18.0, "governance_compliance": 0.90, "cost_efficiency": 0.50, "risk_safety": 0.85},
        },
    ]
    ranking = engine.rank_candidates(
        decision_context="Latency Optimization Strategy",
        candidates_data=candidates,
    )
    assert len(ranking.candidates) == 2
    assert ranking.candidates[0].pareto_rank == 1
    assert ranking.candidates[0].is_recommended is True
    assert ranking.candidates[0].composite_utility > ranking.candidates[1].composite_utility


def test_master_executive_runtime_strategic_cycle():
    runtime = ExecutiveRuntime.get_instance()
    overview = runtime.get_overview()
    assert overview["status"] == "OPERATIONAL"
    assert overview["runtime_type"] == "ASC-GEEIP (Phase 13.11)"
    assert overview["active_goals_count"] >= 2

    cycle_result = runtime.execute_strategic_cycle()
    assert cycle_result["execution_id"].startswith("strat-exec-")
    assert "goal_evolution" in cycle_result
    assert "portfolio_optimization" in cycle_result


def test_rest_api_strategy_endpoints(client):
    # 1. Overview
    res = client.get("/api/v1/strategy/overview")
    assert res.status_code == 200
    data = res.json()
    assert data["runtime_type"] == "ASC-GEEIP (Phase 13.11)"

    # 2. Goals
    res = client.get("/api/v1/strategy/goals")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

    # 3. Create Goal
    res = client.post("/api/v1/strategy/create-goal", json={
        "title": "API Test Strategic Goal",
        "description": "Created via automated test",
        "priority": "HIGH",
        "horizon": "DAYS_90",
        "value_type": "EFFICIENCY_GAIN",
        "estimated_cost_usd": 1500.0,
        "expected_latency_reduction_pct": 15.0,
        "tags": ["test", "api"],
    })
    assert res.status_code == 200
    created_goal = res.json()
    assert created_goal["title"] == "API Test Strategic Goal"

    # 4. Decompose Goal
    res = client.post("/api/v1/strategy/decompose-goal", json={
        "goal_id": created_goal["goal_id"],
        "subtasks": [{"title": "Subtask 1", "estimated_cost_usd": 750.0}],
    })
    assert res.status_code == 200
    assert len(res.json()) == 1

    # 5. Portfolio
    res = client.get("/api/v1/strategy/portfolio")
    assert res.status_code == 200
    assert "portfolio_id" in res.json()

    # 6. Roadmaps
    res = client.get("/api/v1/strategy/roadmaps")
    assert res.status_code == 200
    assert len(res.json()) >= 4

    # 7. Executive
    res = client.get("/api/v1/strategy/executive")
    assert res.status_code == 200
    exec_data = res.json()
    assert "decisions" in exec_data
    assert "recommendations" in exec_data

    # 8. Organization
    res = client.get("/api/v1/strategy/organization")
    assert res.status_code == 200
    assert len(res.json()) >= 5

    # 9. Negotiations
    res = client.get("/api/v1/strategy/negotiations")
    assert res.status_code == 200
    assert len(res.json()) >= 2

    # 10. Simulations
    res = client.get("/api/v1/strategy/simulations")
    assert res.status_code == 200
    assert len(res.json()) >= 2

    # 11. Decisions (Rankings)
    res = client.get("/api/v1/strategy/decisions")
    assert res.status_code == 200
    assert len(res.json()) >= 1

    # 12. Evolve Goals
    res = client.post("/api/v1/strategy/evolve-goals")
    assert res.status_code == 200
    assert "total_goals" in res.json()

    # 13. Prioritize Goals
    res = client.post("/api/v1/strategy/prioritize")
    assert res.status_code == 200

    # 14. Simulate
    res = client.post("/api/v1/strategy/simulate", json={
        "name": "API Test Scenario",
        "horizon": "DAYS_90",
        "budget_delta_usd": 2000.0,
        "worker_scale_delta": 4,
        "cache_hit_rate_pct": 85.0,
        "traffic_growth_pct": 100.0,
    })
    assert res.status_code == 200
    assert "expected_roi_multiplier" in res.json()

    # 15. Negotiate
    res = client.post("/api/v1/strategy/negotiate", json={
        "resource_type": "GPU_VRAM_GB",
        "total_capacity": 48.0,
        "proposals": [
            {"swarm_id": "swarm-a", "quantity_requested": 24.0, "bid_utility": 0.9},
            {"swarm_id": "swarm-b", "quantity_requested": 24.0, "bid_utility": 0.85},
        ],
    })
    assert res.status_code == 200
    assert res.json()["converged"] is True

    # 16. Approve Decision
    dec_id = exec_data["decisions"][0]["decision_id"]
    res = client.post("/api/v1/strategy/approve", json={
        "decision_id": dec_id,
        "approver_key": "cso_test_key",
    })
    assert res.status_code == 200
    assert res.json()["status"] == "APPROVED"

    # 17. Execute Cycle
    res = client.post("/api/v1/strategy/execute-cycle")
    assert res.status_code == 200
    assert "execution_id" in res.json()

    # 18. Archive Goal
    res = client.post("/api/v1/strategy/archive-goal", json={
        "goal_id": created_goal["goal_id"],
        "reason": "Test completion",
    })
    assert res.status_code == 200
    assert res.json()["status"] == "ARCHIVED"


def test_strategy_error_handling_and_not_found(client):
    res = client.post("/api/v1/strategy/archive-goal", json={
        "goal_id": "goal-non-existent-999",
        "reason": "Invalid",
    })
    assert res.status_code == 404

    res = client.post("/api/v1/strategy/approve", json={
        "decision_id": "dec-non-existent-999",
        "approver_key": "test",
    })
    assert res.status_code == 404
