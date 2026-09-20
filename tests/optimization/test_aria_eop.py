"""
Comprehensive Pytest Test Suite for Phase 13.6:
Autonomous Resource Intelligence, Adaptive Optimization & Economic Orchestration Platform (ARIA-EOP).
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.runtime.optimization.events.optimization_events import (
    OptimizationStarted,
    OptimizationCompleted,
    StrategyEvaluated,
    ResourceAllocated,
    ModelSelected,
    WorkerSelected,
    BudgetReserved,
    BudgetExceeded,
    ConstraintViolated,
    SimulationCompleted,
    OptimizationRejected,
    OptimizationApplied,
)
from app.runtime.optimization.optimization.optimization_engine import OptimizationEngine, optimization_engine
from app.runtime.optimization.optimization.optimization_pipeline import OptimizationPipeline
from app.runtime.optimization.optimization.strategy_selector import StrategySelector, CandidateExecutionStrategy
from app.runtime.optimization.optimization.constraint_solver import ConstraintSolver
from app.runtime.optimization.optimization.decision_optimizer import DecisionOptimizer
from app.runtime.optimization.optimization.execution_optimizer import ExecutionOptimizer

from app.runtime.optimization.economics.economic_engine import EconomicEngine, economic_engine
from app.runtime.optimization.economics.cost_model import CostModel
from app.runtime.optimization.economics.value_estimator import ValueEstimator
from app.runtime.optimization.economics.roi_engine import ROIEngine
from app.runtime.optimization.economics.business_priority import BusinessPriority
from app.runtime.optimization.economics.budget_allocator import BudgetAllocator, budget_allocator

from app.runtime.optimization.resource.resource_registry import ResourceRegistry, resource_registry
from app.runtime.optimization.resource.capacity_manager import CapacityManager
from app.runtime.optimization.resource.allocation_engine import AllocationEngine, allocation_engine

from app.runtime.optimization.routing.model_router import ModelRouter, OCRRouter, ValidationRouter
from app.runtime.optimization.simulation.execution_simulator import ExecutionSimulator, WhatIfEngine
from app.runtime.optimization.scheduling.adaptive_scheduler import AdaptiveScheduler
from app.runtime.optimization.prediction.latency_predictor import LatencyPredictor
from app.runtime.optimization.policies.optimization_policy import OptimizationPolicySpec, PolicyValidator


@pytest.fixture
def client():
    return TestClient(app)


# ---------------------------------------------------------------------------
# 1. Domain Events Tests
# ---------------------------------------------------------------------------

def test_optimization_domain_events():
    e1 = OptimizationStarted(objective="MINIMIZE_COST", budget_limit_usd=0.25)
    assert e1.event_type == "optimization.started"
    assert e1.budget_limit_usd == 0.25

    e2 = OptimizationCompleted(selected_strategy_id="strat_test", utility_score=0.95)
    assert e2.event_type == "optimization.completed"
    assert e2.utility_score == 0.95

    e3 = StrategyEvaluated(strategy_name="Wavefront", utility_score=0.91)
    assert e3.event_type == "optimization.strategy.evaluated"

    e4 = ResourceAllocated(resource_id="pool-1", allocated_units=4)
    assert e4.allocated_units == 4

    e5 = ModelSelected(model_id="gemini-1.5-flash", task_id="t-1")
    assert e5.model_id == "gemini-1.5-flash"

    e6 = WorkerSelected(task_id="t-1", worker_id="w-1")
    assert e6.worker_id == "w-1"

    e7 = BudgetReserved(envelope_id="env-1", amount_usd=0.04)
    assert e7.amount_usd == 0.04

    e8 = BudgetExceeded(requested_usd=1.50)
    assert e8.requested_usd == 1.50

    e9 = ConstraintViolated(constraint_name="MAX_LATENCY_MS", threshold=3000.0)
    assert e9.constraint_name == "MAX_LATENCY_MS"

    e10 = SimulationCompleted(scenarios_evaluated=4)
    assert e10.scenarios_evaluated == 4

    e11 = OptimizationRejected(reason="High latency")
    assert e11.reason == "High latency"

    e12 = OptimizationApplied(runtime_directives_count=3)
    assert e12.runtime_directives_count == 3


# ---------------------------------------------------------------------------
# 2. Optimization Core Tests
# ---------------------------------------------------------------------------

def test_strategy_selector_and_pareto():
    cands = [
        CandidateExecutionStrategy(
            strategy_name="Budget Fast",
            target_model="gemini-1.5-flash",
            estimated_cost_usd=0.001,
            estimated_latency_ms=1200.0,
            estimated_confidence=0.94,
        ),
        CandidateExecutionStrategy(
            strategy_name="High Reasoning",
            target_model="gemini-1.5-pro",
            estimated_cost_usd=0.015,
            estimated_latency_ms=3500.0,
            estimated_confidence=0.99,
        ),
    ]

    selected_balanced = StrategySelector.score_and_select(cands, objective="BALANCED_UTILITY")
    assert selected_balanced.utility_score > 0.0

    selected_cost = StrategySelector.score_and_select(cands, objective="MINIMIZE_COST")
    assert selected_cost.strategy_name == "Budget Fast"

    selected_conf = StrategySelector.score_and_select(cands, objective="MAXIMIZE_CONFIDENCE")
    assert selected_conf.strategy_name == "High Reasoning"


def test_constraint_solver():
    res_sat = ConstraintSolver.solve(
        candidate_cost=0.005,
        candidate_latency_ms=2000.0,
        candidate_confidence=0.96,
        candidate_concurrency=4,
        max_budget_usd=0.10,
        max_latency_ms=4000.0,
        min_confidence=0.90,
    )
    assert res_sat.is_satisfied is True
    assert len(res_sat.violations) == 0

    res_viol = ConstraintSolver.solve(
        candidate_cost=0.50,  # exceeds 0.10
        candidate_latency_ms=6000.0,  # exceeds 4000.0
        candidate_confidence=0.80,  # below 0.90
        candidate_concurrency=4,
        max_budget_usd=0.10,
        max_latency_ms=4000.0,
        min_confidence=0.90,
    )
    assert res_viol.is_satisfied is False
    assert len(res_viol.violations) >= 3


def test_decision_and_execution_optimizers():
    dec = DecisionOptimizer.optimize_memory_decision(cache_similarity=0.95, recompute_cost_usd=0.004)
    assert dec.selected_option == "USE_CACHED_SCHEMA"
    assert dec.expected_gain_pct == 85.0

    dirs = ExecutionOptimizer.generate_directives(page_count=12, complexity=0.8)
    assert dirs.concurrency_pool_size == 8
    assert dirs.validation_depth == "SMT_SYMBOLIC"


def test_optimization_engine_and_pipeline():
    engine = OptimizationEngine()
    report = engine.optimize_mission("mission-opt-01")
    assert report.mission_id == "mission-opt-01"
    assert report.selected_strategy is not None
    assert report.expected_savings_pct > 0
    assert len(engine.list_reports()) >= 1


# ---------------------------------------------------------------------------
# 3. Economic Intelligence Tests
# ---------------------------------------------------------------------------

def test_cost_model_and_roi():
    costs = CostModel.calculate_cost("gemini-1.5-flash", input_tokens=4000, output_tokens=800, pages=4)
    assert costs.total_cost_usd > 0.0
    assert costs.model_cost_usd > 0.0

    val = ValueEstimator.estimate(confidence=0.97, page_count=4, execution_cost=costs.total_cost_usd)
    assert val.gross_business_value_usd > 0.0

    roi = ROIEngine.calculate_roi(costs.total_cost_usd, val.gross_business_value_usd, confidence=0.97)
    assert roi.expected_roi_ratio > 0.0

    weights = BusinessPriority.get_tier_weights("CRITICAL_SLA")
    assert weights.weight_latency > weights.weight_cost

    res = budget_allocator.reserve_budget("mission-001", requested_usd=0.02, total_budget_usd=1.0)
    assert res.status == "RESERVED"


# ---------------------------------------------------------------------------
# 4. Resource & Routing Tests
# ---------------------------------------------------------------------------

def test_resource_registry_and_allocation():
    reg = ResourceRegistry()
    resources = reg.list_resources()
    assert len(resources) >= 4

    cap = CapacityManager.get_capacity_status()
    assert cap.total_workers == 16
    assert cap.system_utilization_pct > 0

    alloc = AllocationEngine()
    tkt = alloc.allocate("m-1", "res-pool-worker-01", 4)
    assert tkt.status == "ALLOCATED"
    rel = alloc.release(tkt.ticket_id)
    assert rel.status == "RELEASED"


def test_routing_engines():
    m_route = ModelRouter.route_model("t-1", complexity=0.9, confidence_floor=0.99)
    assert m_route.target_engine == "gemini-1.5-pro"

    ocr_route = OCRRouter.route_ocr("t-2", is_scanned_handwriting=True, page_count=2)
    assert ocr_route.target_engine == "DOCUMENT_AI_ADVANCED"

    val_route = ValidationRouter.route_validation("t-3", is_financial_audit=True)
    assert val_route.target_engine == "SMT_SYMBOLIC_PROVER"


# ---------------------------------------------------------------------------
# 5. Simulation, Scheduling, Prediction & Policies Tests
# ---------------------------------------------------------------------------

def test_simulation_and_what_if():
    scenarios = ExecutionSimulator.simulate_scenarios(page_count=4)
    assert len(scenarios) == 3
    assert scenarios[0].projected_latency_ms > scenarios[2].projected_latency_ms

    what_if = WhatIfEngine.evaluate_what_if(target_budget_usd=0.05, target_latency_ms=2500.0)
    assert what_if["is_feasible"] is True


def test_scheduling_prediction_policies():
    sched = AdaptiveScheduler.schedule(total_tasks=12, deadline_ms=5000.0)
    assert sched.optimal_parallelism >= 4
    assert sched.projected_makespan_ms > 0

    pred = LatencyPredictor.predict(page_count=6, concurrency=4, complexity=0.5)
    assert pred.predicted_latency_ms > 0
    assert pred.latency_p95_ms > pred.predicted_latency_ms

    pol_val = PolicyValidator.validate_against_policy({"cost_usd": 0.02, "latency_ms": 2000.0, "confidence": 0.95})
    assert pol_val["is_compliant"] is True


# ---------------------------------------------------------------------------
# 6. FastAPI REST Endpoints Integration Tests
# ---------------------------------------------------------------------------

def test_api_optimization_endpoints(client: TestClient):
    resp_miss = client.get("/api/v1/optimization/mission/mission-001")
    assert resp_miss.status_code == 200
    data = resp_miss.json()
    assert data["mission_id"] == "mission-001"
    assert "selected_strategy" in data

    resp_res = client.get("/api/v1/optimization/resources")
    assert resp_res.status_code == 200
    assert len(resp_res.json()) >= 1

    resp_strat = client.get("/api/v1/optimization/strategies")
    assert resp_strat.status_code == 200
    assert isinstance(resp_strat.json(), list)

    resp_sim = client.get("/api/v1/optimization/simulations?pages=4")
    assert resp_sim.status_code == 200
    assert len(resp_sim.json()) == 3

    resp_routes = client.get("/api/v1/optimization/routes")
    assert resp_routes.status_code == 200
    assert len(resp_routes.json()) == 3

    resp_econ = client.get("/api/v1/optimization/economics?pages=4")
    assert resp_econ.status_code == 200
    econ = resp_econ.json()
    assert "cost_breakdown" in econ
    assert "roi_metrics" in econ

    resp_pol = client.get("/api/v1/optimization/policies")
    assert resp_pol.status_code == 200
    assert "max_budget_per_mission_usd" in resp_pol.json()

    resp_pred = client.get("/api/v1/optimization/predictions?pages=4&concurrency=6")
    assert resp_pred.status_code == 200
    assert "predicted_latency_ms" in resp_pred.json()

    resp_exp = client.get("/api/v1/optimization/explanations?mission_id=mission-001")
    assert resp_exp.status_code == 200
    assert "winning_strategy" in resp_exp.json()

    resp_hist = client.get("/api/v1/optimization/history")
    assert resp_hist.status_code == 200
    assert isinstance(resp_hist.json(), list)

    resp_sim_post = client.post("/api/v1/optimization/simulate", json={
        "page_count": 4,
        "target_budget_usd": 0.05,
        "target_latency_ms": 3000.0,
    })
    assert resp_sim_post.status_code == 200
    assert resp_sim_post.json()["is_feasible"] is True

    resp_reopt = client.post("/api/v1/optimization/reoptimize", json={
        "mission_id": "mission-001",
        "objective": "MINIMIZE_COST",
        "max_budget_usd": 0.20,
        "max_latency_ms": 4000.0,
        "min_confidence": 0.88,
    })
    assert resp_reopt.status_code == 200
    assert resp_reopt.json()["objective"] == "MINIMIZE_COST"
