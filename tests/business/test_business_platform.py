"""
Phase 13.19: Test Suite for Enterprise Process Intelligence & Autonomous Business Orchestration Platform (EPI-ABOP).
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.runtime.business.models.schemas import (
    BusinessProcess,
    ProcessStep,
    StepType,
    StepStatus,
    ProcessStatus,
    HumanApprovalTask,
    ApprovalStatus,
    ProcessSimulationConfig,
    BusinessGoal,
)
from app.runtime.business.process_engine.business_process_engine import BusinessProcessEngine
from app.runtime.business.organization_graph.enterprise_knowledge_graph import EnterpriseKnowledgeGraph
from app.runtime.business.goal_manager.business_goal_manager import BusinessGoalManager
from app.runtime.business.process_discovery.process_discovery_engine import ProcessDiscoveryEngine
from app.runtime.business.optimization.process_optimizer import ProcessOptimizer
from app.runtime.business.decision_engine.enterprise_decision_engine import EnterpriseDecisionEngine
from app.runtime.business.sla.sla_intelligence import SLAIntelligenceEngine
from app.runtime.business.collaboration.human_collaboration_engine import HumanCollaborationEngine
from app.runtime.business.kpi.enterprise_kpi_engine import EnterpriseKPIEngine
from app.runtime.business.simulation.business_simulation_engine import BusinessSimulationEngine
from app.runtime.business.digital_twin.digital_twin_organization import DigitalTwinOrganization
from app.runtime.business.runtime.business_orchestrator import BusinessOrchestrator


@pytest.fixture
def client():
    return TestClient(app)


def test_business_process_engine_execution():
    engine = BusinessProcessEngine()
    proc = engine.get_process("proc_invoice_enterprise_01")
    assert proc is not None
    assert len(proc.steps) == 6

    # Execute until human gate
    res = engine.run_process_until_pause_or_completion("proc_invoice_enterprise_01")
    assert res["final_status"] in ["PAUSED", "COMPLETED", "RUNNING"]
    assert res["steps_executed_count"] >= 1


def test_human_approval_gate_and_resumption():
    engine = BusinessProcessEngine()
    # Resume step
    res = engine.resume_process_after_approval(
        process_id="proc_invoice_enterprise_01",
        step_id="step_manager_approval",
        approved=True,
    )
    assert res["final_status"] in ["COMPLETED", "RUNNING", "PAUSED"]


def test_enterprise_knowledge_graph():
    graph = EnterpriseKnowledgeGraph()
    org = graph.get_organization_graph()
    assert len(org.departments) >= 4
    assert len(org.roles) >= 3
    assert len(org.systems) >= 3

    # Approver search for $45,000
    approver = graph.find_approver_for_amount("dept_finance", 45000.0)
    assert approver is not None
    assert approver.approval_limit_amount >= 45000.0


def test_business_goal_manager_and_decomposition():
    mgr = BusinessGoalManager()
    goals = mgr.list_goals()
    assert len(goals) >= 2

    # HTN decomposition
    plan = mgr.decompose_goal_to_action_plan("goal_invoice_velocity")
    assert len(plan["recommended_actions"]) >= 2
    assert "act_parallelize_ocr_tax" in [a["action_id"] for a in plan["recommended_actions"]]


def test_process_discovery_mining():
    disc_engine = ProcessDiscoveryEngine()
    procs = disc_engine.list_discovered_processes()
    assert len(procs) >= 2
    assert procs[0].frequency > 0

    # Ingest synthetic logs
    mined = disc_engine.mine_processes_from_logs([
        {"activity": "OCR", "timestamp": "2026-09-13T10:00:00Z"},
        {"activity": "Validation", "timestamp": "2026-09-13T10:01:00Z"},
    ])
    assert len(mined) >= 3


def test_process_optimizer():
    optimizer = ProcessOptimizer()
    recs = optimizer.list_recommendations()
    assert len(recs) >= 2
    assert recs[0].estimated_annual_savings_usd > 0.0
    assert recs[0].estimated_cycle_time_reduction_pct > 0.0


def test_enterprise_decision_engine():
    decision_engine = EnterpriseDecisionEngine()
    # Micro invoice under $1k
    res1 = decision_engine.evaluate_decision("dt_invoice_approval_policy", {"amount": 500.0, "vendor_tier": "TIER_1"})
    assert res1["action"] == "AUTO_APPROVE"

    # Executive invoice over $50k
    res2 = decision_engine.evaluate_decision("dt_invoice_approval_policy", {"amount": 75000.0})
    assert res2["action"] == "ROUTE_CFO_APPROVAL"


def test_sla_intelligence_engine():
    sla_engine = SLAIntelligenceEngine()
    risk = sla_engine.assess_step_sla_risk(
        process_id="proc_invoice_enterprise_01",
        step_id="step_ocr_extraction",
        elapsed_sec=55.0,
        target_sec=60.0,
    )
    assert 0.0 <= risk.breach_probability <= 1.0
    assert risk.is_breached is False


def test_human_collaboration_engine():
    collab = HumanCollaborationEngine()
    tasks = collab.list_tasks(status=ApprovalStatus.PENDING)
    assert len(tasks) >= 1

    # Decide task
    decided = collab.decide_task(
        task_id=tasks[0].task_id,
        decision=ApprovalStatus.APPROVED,
        rationale="Verified and approved",
        decided_by="role_finance_director",
    )
    assert decided.status == ApprovalStatus.APPROVED


def test_enterprise_kpi_engine():
    kpi_engine = EnterpriseKPIEngine()
    kpis = kpi_engine.get_kpis()
    assert len(kpis) >= 4
    assert any(k.kpi_id == "kpi_invoice_turnaround" for k in kpis)


def test_business_simulation_engine():
    sim_engine = BusinessSimulationEngine()
    res = sim_engine.run_simulation(
        ProcessSimulationConfig(
            process_id="proc_invoice_enterprise_01",
            simulated_transactions_count=500,
        )
    )
    assert res.cost_reduction_usd > 0.0
    assert res.throughput_increase_pct > 0.0


def test_digital_twin_organization():
    dto = DigitalTwinOrganization()
    state = dto.get_digital_twin_state()
    assert state.total_departments == 4
    assert state.active_agent_workers > 0
    assert "dept_finance" in state.department_workloads


def test_business_orchestrator_master():
    orchestrator = BusinessOrchestrator.get_instance()
    overview = orchestrator.get_executive_overview()
    assert overview.total_active_processes >= 1
    assert overview.mean_sla_compliance_pct > 90.0

    cycle_res = orchestrator.run_business_cycle()
    assert cycle_res["cycle_status"] == "SUCCESS"


# API Endpoints Test
def test_business_api_endpoints(client):
    # Overview
    r = client.get("/api/v1/business/overview")
    assert r.status_code == 200
    assert "total_active_processes" in r.json()

    # Processes
    r = client.get("/api/v1/business/processes")
    assert r.status_code == 200
    assert len(r.json()) >= 1

    # Goals
    r = client.get("/api/v1/business/goals")
    assert r.status_code == 200
    assert len(r.json()) >= 2

    # Organization
    r = client.get("/api/v1/business/organization")
    assert r.status_code == 200
    assert len(r.json()["departments"]) >= 4

    # Approvals
    r = client.get("/api/v1/business/approvals")
    assert r.status_code == 200

    # Discovery
    r = client.get("/api/v1/business/discovery")
    assert r.status_code == 200
    assert len(r.json()) >= 2

    # KPIs
    r = client.get("/api/v1/business/kpis")
    assert r.status_code == 200

    # Digital Twin
    r = client.get("/api/v1/business/digital-twin")
    assert r.status_code == 200

    # Simulation
    r = client.post(
        "/api/v1/business/simulations",
        json={"process_id": "proc_invoice_enterprise_01", "simulated_transactions_count": 100},
    )
    assert r.status_code == 200
    assert r.json()["cost_reduction_usd"] > 0.0

    # Orchestration Cycle
    r = client.post("/api/v1/business/orchestration/cycle")
    assert r.status_code == 200
    assert r.json()["cycle_status"] == "SUCCESS"
