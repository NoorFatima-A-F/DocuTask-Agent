"""
Phase 13.14 - Comprehensive Pytest Test Suite
Autonomous AI Organization, Multi-Agent Enterprise Governance & Mission Execution Platform (AAO-MAGEMEP)
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

from app.runtime.organization.events.organization_events import (
    AgentRole,
    MissionPriority,
    OrganizationState,
    GovernanceVerdict,
    ConflictStatus,
    org_event_bus,
)
from app.runtime.organization.mission.mission_engine import mission_engine, Mission
from app.runtime.organization.strategy.organization_strategy_engine import organization_strategy_engine
from app.runtime.organization.organization.organization_engine import organization_engine
from app.runtime.organization.workforce.workforce_engine import workforce_engine
from app.runtime.organization.project.project_engine import project_engine
from app.runtime.organization.resource.resource_engine import resource_engine
from app.runtime.organization.performance.performance_engine import performance_engine
from app.runtime.organization.finance.finance_engine import finance_engine
from app.runtime.organization.negotiation.negotiation_engine import negotiation_engine
from app.runtime.organization.governance.governance_engine import governance_engine
from app.runtime.organization.simulation.simulation_engine import organization_simulation_engine
from app.runtime.organization.runtime.organization_runtime import organization_runtime


@pytest.fixture
def client():
    return TestClient(app)


# ---------------------------------------------------------------------------
# 1. Mission Engine Tests
# ---------------------------------------------------------------------------

def test_mission_decomposition():
    goal = "Reduce cloud document processing latency by 50% and maintain 99% accuracy"
    mission = mission_engine.decompose_goal(goal, priority=MissionPriority.HIGH, timeline_days=60)

    assert mission.mission_id.startswith("msn_")
    assert len(mission.objectives) >= 3
    assert len(mission.constraints) >= 2
    assert mission.state == OrganizationState.PLANNING
    assert mission.strategic_alignment_score >= 0.85


def test_mission_validation():
    missions = mission_engine.list_missions()
    assert len(missions) > 0

    first_id = missions[0].mission_id
    val_res = mission_engine.validate_mission(first_id)

    assert val_res["valid"] is True
    assert val_res["confidence_score"] >= 0.90
    assert "strategic_alignment" in val_res["checks"]


# ---------------------------------------------------------------------------
# 2. Strategy Engine Tests
# ---------------------------------------------------------------------------

def test_strategy_generation_and_monte_carlo():
    mission_id = "msn_reduce_cost_40pct"
    strategies = organization_strategy_engine.generate_strategies(mission_id, count=3)

    assert len(strategies) == 3
    strat = strategies[0]
    assert strat.expected_roi_multiplier > 1.0
    assert len(strat.actions) >= 1

    mc_eval = organization_strategy_engine.evaluate_strategy_monte_carlo(strat.strategy_id, iterations=100)
    assert "probability_of_success" in mc_eval
    assert mc_eval["probability_of_success"] >= 0.70
    assert mc_eval["mean_expected_roi"] > 0.0


def test_optimal_strategy_selection():
    mission_id = "msn_reduce_cost_40pct"
    best = organization_strategy_engine.select_optimal_strategy(mission_id)

    assert best is not None
    assert best.is_selected is True


# ---------------------------------------------------------------------------
# 3. Organization Designer Tests
# ---------------------------------------------------------------------------

def test_organization_designer():
    org = organization_engine.design_organization_for_mission("msn_reduce_cost_40pct", "strat_adaptive_quantization_001")

    assert org.org_id.startswith("org_")
    assert len(org.departments) >= 2
    assert org.operational_efficiency >= 0.90

    restructured = organization_engine.restructure_organization(org.org_id)
    assert restructured.operational_efficiency >= org.operational_efficiency


# ---------------------------------------------------------------------------
# 4. Workforce Manager Tests
# ---------------------------------------------------------------------------

def test_workforce_operations():
    # Listing
    agents = workforce_engine.list_agents()
    assert len(agents) >= 4

    # Hiring
    new_hire = workforce_engine.hire_agent(
        name="Security Audit Agent Specialist",
        role=AgentRole.SECURITY_AGENT,
        department_id="dept_engineering_core",
        skill_names=["vulnerability_scanning", "zero_trust_verification"],
    )
    assert new_hire.agent_id.startswith("agent_")
    assert len(new_hire.skills) == 2

    # Capability Upgrade
    upgraded = workforce_engine.upgrade_agent_capability(new_hire.agent_id, "vulnerability_scanning", boost=0.08)
    assert upgraded.skills[0].proficiency_level > 0.85

    # Rebalancing
    rebalance_res = workforce_engine.optimize_workforce_allocation()
    assert rebalance_res["rebalanced_agents"] >= len(agents)

    # Retiring
    success = workforce_engine.retire_agent(new_hire.agent_id)
    assert success is True


# ---------------------------------------------------------------------------
# 5. Project Engine Tests
# ---------------------------------------------------------------------------

def test_project_lifecycle_and_critical_path():
    proj = project_engine.create_project(
        mission_id="msn_reduce_cost_40pct",
        title="Test Dynamic Scaling Initiative",
        description="Verifies CPM and dependency graphs",
        task_specs=[
            {"title": "Core Module Setup", "estimated_days": 2.0},
            {"title": "Load Ingestion Cluster", "estimated_days": 4.0, "dependencies": []},
            {"title": "Verify Metrics", "estimated_days": 1.0, "dependencies": []},
        ],
    )

    assert proj.project_id.startswith("proj_")
    assert len(proj.tasks) == 3
    assert proj.critical_path_duration_days > 0.0

    # Update Task Status
    first_task = proj.tasks[0]
    updated_t = project_engine.update_task_status(proj.project_id, first_task.task_id, "COMPLETED", 100.0)
    assert updated_t.status == "COMPLETED"

    # Replanning
    replanned = project_engine.replan_project(proj.project_id)
    assert replanned.total_progress_percent > 0.0


# ---------------------------------------------------------------------------
# 6. Resource Intelligence Tests
# ---------------------------------------------------------------------------

def test_resource_optimization():
    pool = resource_engine.get_pool_status()
    assert pool.compute_slots_total >= 32
    assert pool.utilization_rate > 0.0

    plan = resource_engine.optimize_resources(prioritize_metric="COST_EFFICIENCY")
    assert plan.is_pareto_optimal is True
    assert len(plan.quotas) >= 3
    assert plan.overall_efficiency_score >= 0.90


# ---------------------------------------------------------------------------
# 7. Performance Scorecard Tests
# ---------------------------------------------------------------------------

def test_performance_scorecard_generation():
    scorecard = performance_engine.generate_scorecard()

    assert scorecard.overall_roi_multiplier >= 3.0
    assert scorecard.composite_health_score >= 0.90
    assert len(scorecard.agent_scorecards) >= 4
    assert len(scorecard.team_scorecards) >= 2


# ---------------------------------------------------------------------------
# 8. Finance & Economic Intelligence Tests
# ---------------------------------------------------------------------------

def test_finance_engine_forecasting():
    summary = finance_engine.get_financial_summary()
    assert summary.total_monthly_burn_usd > 0.0

    forecast = finance_engine.forecast_costs(months=12)
    assert forecast.projected_spend_usd > 0.0
    assert forecast.projected_savings_usd > 0.0

    roi = finance_engine.compute_roi_projection()
    assert roi.projected_annual_roi_multiplier >= 3.5
    assert roi.savings_percentage > 30.0


# ---------------------------------------------------------------------------
# 9. Multi-Agent Negotiation Tests
# ---------------------------------------------------------------------------

def test_multi_agent_negotiation_nash_solution():
    neg = negotiation_engine.initiate_negotiation(
        initiator=AgentRole.RESEARCH_AGENT,
        respondent=AgentRole.OPERATIONS_AGENT,
        topic="Memory Cache Allocation Conflict",
        requested_resource="MEMORY_GB",
        requested_units=64.0,
        rationale="Need expanded cache for vector indexes",
    )

    assert neg.status == ConflictStatus.IN_NEGOTIATION

    negotiation_engine.submit_counter_proposal(
        negotiation_id=neg.negotiation_id,
        respondent=AgentRole.OPERATIONS_AGENT,
        offered_units=40.0,
        conditions=["Evict cold keys every 6 hours"],
    )

    agreement = negotiation_engine.solve_nash_equilibrium(neg.negotiation_id)
    assert agreement.settled_units == 52.0  # (64 + 40) / 2
    assert agreement.is_pareto_optimal is True

    resolved_neg = negotiation_engine.get_negotiation(neg.negotiation_id)
    assert resolved_neg.status == ConflictStatus.RESOLVED


# ---------------------------------------------------------------------------
# 10. Governance & Simulation Tests
# ---------------------------------------------------------------------------

def test_governance_multi_pillar_review():
    review = governance_engine.review_decision(
        decision_title="Deploy 4-Bit Quantized Extractor",
        proposing_role=AgentRole.CTO_AGENT,
        decision_payload={"target_model": "gemini_flash_lite_distilled", "savings": "45%"},
        simulation_verified=True,
    )

    assert review.verdict == GovernanceVerdict.APPROVED
    assert len(review.cryptographic_seal_sha256) == 64
    assert review.confidence_score >= 0.90


def test_simulation_engine():
    rep = organization_simulation_engine.run_simulation(runs=50)

    assert rep.runs_completed == 50
    assert rep.success_rate >= 0.90
    assert rep.resilience_score >= 0.90


# ---------------------------------------------------------------------------
# 11. Master Organization Runtime Cycle Tests
# ---------------------------------------------------------------------------

def test_end_to_end_autonomous_organization_cycle():
    summary = organization_runtime.run_full_autonomous_cycle(
        mission_goal="Reduce total OCR infrastructure spend by 40% while preserving 99% accuracy"
    )

    assert summary.cycle_id.startswith("org_cyc_")
    assert summary.status == "COMPLETED"
    assert summary.roi_multiplier >= 3.5
    assert summary.duration_ms > 0.0

    overview = organization_runtime.get_overview()
    assert overview["composite_health_score"] >= 0.90
    assert overview["total_cycles_executed"] >= 2


# ---------------------------------------------------------------------------
# 12. REST API Integration Tests
# ---------------------------------------------------------------------------

def test_api_organization_endpoints(client):
    # Overview
    res = client.get("/api/v1/organization/overview")
    assert res.status_code == 200
    data = res.json()
    assert "composite_health_score" in data

    # Missions
    res = client.get("/api/v1/organization/missions")
    assert res.status_code == 200
    assert len(res.json()) >= 1

    post_m = client.post(
        "/api/v1/organization/missions",
        json={"goal": "Automate invoice reconciliation across 50 vendors", "priority": "HIGH", "timeline_days": 45},
    )
    assert post_m.status_code == 200
    m_data = post_m.json()
    assert "mission_id" in m_data

    # Strategies
    res = client.get("/api/v1/organization/strategies")
    assert res.status_code == 200

    # Structure
    res = client.get("/api/v1/organization/structure")
    assert res.status_code == 200
    assert "departments" in res.json()

    # Agents
    res = client.get("/api/v1/organization/agents")
    assert res.status_code == 200
    assert len(res.json()) >= 4

    # Projects
    res = client.get("/api/v1/organization/projects")
    assert res.status_code == 200

    # Resources
    res = client.get("/api/v1/organization/resources")
    assert res.status_code == 200
    assert "pool" in res.json()

    # Performance Scorecard
    res = client.get("/api/v1/organization/scorecard")
    assert res.status_code == 200
    assert "overall_roi_multiplier" in res.json()

    # ROI & Finance
    res = client.get("/api/v1/organization/roi")
    assert res.status_code == 200

    # Negotiations
    res = client.get("/api/v1/organization/negotiations")
    assert res.status_code == 200

    # Governance
    res = client.get("/api/v1/organization/governance/reviews")
    assert res.status_code == 200

    # Simulations
    res = client.get("/api/v1/organization/simulations")
    assert res.status_code == 200

    # Full Cycle Execution
    res = client.post(
        "/api/v1/organization/cycle",
        json={"mission_goal": "Optimize document batch dispatching pipeline"},
    )
    assert res.status_code == 200
    cycle_res = res.json()
    assert cycle_res["status"] == "COMPLETED"
