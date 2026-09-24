"""
FastAPI Endpoints for Quantitative Decision Intelligence & Optimization Platform (QDIOP / SDIOP).
Exposes real-time endpoints for multi-objective optimization, confidence calibration, model routing,
retry optimization, benchmarking, and policy management.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.runtime.feature_store import feature_registry, feature_statistics_tracker
from app.runtime.confidence import scientific_confidence_engine
from app.runtime.optimization import MultiObjectivePlanOptimizer
from app.runtime.risk import ProbabilisticRiskEstimator, MultiDimensionalUncertainty, RiskMitigationEngine
from app.runtime.constraints import ConstraintSolver
from app.runtime.routing import ScientificModelRouter
from app.runtime.retry import RetryOptimizer
from app.runtime.calibration import scientific_calibration_engine
from app.runtime.evaluation import policy_evaluator
from app.runtime.benchmarking import scientific_benchmark_engine
from app.runtime.learning import policy_store, AdaptiveWeightLearner

router = APIRouter()


class OptimizeRequest(BaseModel):
    candidates: List[Dict[str, Any]] = Field(..., description="List of candidate execution plans")
    constraints: Optional[Dict[str, float]] = Field(default=None, description="Operational constraints (budget, latency, accuracy)")
    weights: Optional[Dict[str, float]] = Field(default=None, description="Multi-objective scalarization weights")
    context_id: str = Field(default="default_mission", description="Context or mission ID")


class ConfidenceRequest(BaseModel):
    features: Dict[str, float] = Field(..., description="Runtime feature dictionary")
    entity_key: str = Field(default="default_worker", description="Entity key for reliability tracking")


class ModelRouteRequest(BaseModel):
    task_id: str = Field(default="extract_task_1", description="Task identifier")
    document_complexity: float = Field(default=0.5, ge=0.0, le=1.0)
    token_estimate: int = Field(default=2500, ge=1)
    max_budget_usd: Optional[float] = None
    max_latency_ms: Optional[float] = None


class RetryRequest(BaseModel):
    current_retry_count: int = Field(default=0, ge=0)
    failure_type: str = Field(default="timeout", description="Category of failure observed")
    base_cost_usd: float = Field(default=0.005)
    base_latency_ms: float = Field(default=800.0)


class WeightProposalRequest(BaseModel):
    observed_outcomes: List[Dict[str, float]] = Field(..., description="List of outcome metrics from recent missions")
    learning_rate: float = Field(default=0.05)


@router.post("/optimize", summary="Execute Multi-Objective Plan Optimization")
async def optimize_plan(req: OptimizeRequest):
    """Computes Pareto frontier, evaluates Chebyshev and weighted utility, and selects optimal plan."""
    try:
        result = MultiObjectivePlanOptimizer.optimize(
            candidate_plans=req.candidates,
            constraints=req.constraints,
            weights=req.weights,
            context_id=req.context_id,
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/features", summary="Inspect Feature Store Registry & Statistics")
async def get_feature_store_data():
    """Returns canonical feature definitions, current population summaries, and default bounds."""
    defs = [
        {
            "name": d.name,
            "category": d.category.value,
            "min_bound": d.min_bound,
            "max_bound": d.max_bound,
            "default_value": d.default_value,
            "normalization_type": d.normalization_type.value,
            "description": d.description,
            "unit": d.unit,
        }
        for d in feature_registry.list_all()
    ]
    stats = feature_statistics_tracker.get_all_summaries()
    return {"success": True, "definitions": defs, "statistics": stats}


@router.post("/confidence", summary="Decompose and Calibrate Scientific Confidence")
async def evaluate_confidence(req: ConfidenceRequest):
    """Computes Bayesian posterior, Platt calibrated probability, Wilson CI, and uncertainty decomposition."""
    try:
        report = scientific_confidence_engine.evaluate(
            normalized_features=req.features,
            entity_key=req.entity_key,
        )
        return {"success": True, "data": report.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/calibration", summary="Get Calibration Curves & Reliability Diagram Data")
async def get_calibration_lab_data(num_bins: int = Query(default=10, ge=5, le=20)):
    """Returns empirical reliability bins, ECE, MCE, and Brier score."""
    data = scientific_calibration_engine.evaluate_calibration(num_bins=num_bins)
    return {"success": True, "data": data}


@router.post("/route-model", summary="Select Mathematically Optimal AI Model")
async def route_model(req: ModelRouteRequest):
    """Evaluates candidate models across expected accuracy, cost, latency, and utility."""
    res = ScientificModelRouter.route_task(
        task_id=req.task_id,
        document_complexity=req.document_complexity,
        token_estimate=req.token_estimate,
        max_budget_usd=req.max_budget_usd,
        max_latency_ms=req.max_latency_ms,
    )
    return {"success": True, "data": res}


@router.post("/retry-decision", summary="Evaluate Quantitative Marginal Retry Benefit")
async def evaluate_retry(req: RetryRequest):
    """Calculates expected improvement, recovery probability, delay cost, and decides Retry vs Fallback vs Escalate."""
    eval_res = RetryOptimizer.evaluate(
        current_retry_count=req.current_retry_count,
        failure_type=req.failure_type,
        base_cost_usd=req.base_cost_usd,
        base_latency_ms=req.base_latency_ms,
    )
    return {"success": True, "data": eval_res.to_dict()}


@router.post("/benchmark", summary="Run Reproducible Scientific Benchmarks")
async def run_benchmarks(seed: int = Query(default=42)):
    """Runs standardized workload benchmark suites against Greedy, Random, and Single-Objective baselines."""
    res = scientific_benchmark_engine.run_all_benchmarks(seed=seed)
    return {"success": True, "data": res}


@router.get("/policy-evaluation", summary="Evaluate Active Planner Policy Regret & Stability")
async def get_policy_evaluation():
    """Returns instantaneous & cumulative regret curves, baseline comparison, and sensitivity gradients."""
    data = policy_evaluator.evaluate_active_policy()
    return {"success": True, "data": data}


@router.get("/risk", summary="Get Probabilistic Risk Estimations & Mitigations")
async def get_risk_assessment():
    """Computes joint failure probabilities, uncertainty vectors, and prescriptive mitigation actions."""
    defaults = feature_registry.get_defaults()
    probs = ProbabilisticRiskEstimator.estimate_probabilities(defaults)
    unc = MultiDimensionalUncertainty.calculate_uncertainty_vector(defaults)
    mits = RiskMitigationEngine.generate_mitigations(probs)

    return {
        "success": True,
        "failure_probabilities": probs.to_dict(),
        "uncertainty_vector": unc,
        "mitigation_actions": [
            {
                "action_id": m.action_id,
                "target_risk": m.target_risk,
                "recommended_action": m.recommended_action,
                "expected_risk_reduction": m.expected_risk_reduction,
                "cost_impact_usd": m.cost_impact_usd,
                "latency_impact_ms": m.latency_impact_ms,
                "auto_applicable": m.auto_applicable,
            }
            for m in mits
        ],
    }


@router.get("/constraints", summary="Get Constraint Solver Graph & Binding Analysis")
async def get_constraints_info():
    """Returns constraint graph structure, binding identifiers, and feasibility metrics."""
    default_candidates = [
        {"id": "cand_1", "plan_name": "Pro Tier Plan", "cost_usd": 0.045, "latency_ms": 2200.0, "accuracy": 0.99, "overall_risk": 0.02},
        {"id": "cand_2", "plan_name": "Standard Plan", "cost_usd": 0.015, "latency_ms": 950.0, "accuracy": 0.95, "overall_risk": 0.05},
        {"id": "cand_3", "plan_name": "Budget Fast Plan", "cost_usd": 0.003, "latency_ms": 320.0, "accuracy": 0.90, "overall_risk": 0.12},
    ]
    constraints = {"max_budget_usd": 0.03, "max_latency_ms": 1500.0, "min_accuracy": 0.92, "max_risk": 0.10}
    solver_res = ConstraintSolver.solve(default_candidates, constraints)

    return {
        "success": True,
        "is_satisfiable": solver_res.is_satisfiable,
        "feasible_count": len(solver_res.feasible_candidates),
        "infeasible_count": len(solver_res.infeasible_candidates),
        "active_bindings": solver_res.active_bindings,
        "graph": solver_res.graph,
    }


@router.post("/learn-weights", summary="Propose Adaptive Weight Adjustment")
async def propose_weights(req: WeightProposalRequest):
    """Proposes Bayesian weight updates based on empirical outcome feedback."""
    active_pol = policy_store.get_active_policy()
    proposal = AdaptiveWeightLearner.propose_weights(
        current_weights=active_pol.weights,
        observed_outcomes=req.observed_outcomes,
        learning_rate=req.learning_rate,
    )
    return {
        "success": True,
        "proposal": {
            "proposal_id": proposal.proposal_id,
            "proposed_weights": proposal.proposed_weights,
            "current_weights": proposal.current_weights,
            "rationale": proposal.rationale,
            "expected_utility_delta": proposal.expected_utility_delta,
            "requires_human_approval": proposal.requires_human_approval,
            "status": proposal.status,
        },
    }


# ===========================================================================
# Phase 13.6 ARIA-EOP Endpoints
# ===========================================================================

from app.runtime.optimization.optimization.optimization_engine import optimization_engine
from app.runtime.optimization.economics.economic_engine import economic_engine
from app.runtime.optimization.resource.resource_registry import resource_registry
from app.runtime.optimization.routing.model_router import ModelRouter, OCRRouter, ValidationRouter
from app.runtime.optimization.simulation.execution_simulator import ExecutionSimulator, WhatIfEngine
from app.runtime.optimization.prediction.latency_predictor import LatencyPredictor
from app.runtime.optimization.policies.optimization_policy import OptimizationPolicySpec


class SimulateRequest(BaseModel):
    page_count: int = Field(default=4, ge=1)
    target_budget_usd: float = Field(default=0.05)
    target_latency_ms: float = Field(default=3000.0)


class ReoptimizeRequest(BaseModel):
    mission_id: str = Field(default="mission-001")
    objective: str = Field(default="BALANCED_UTILITY")
    max_budget_usd: float = Field(default=0.50)
    max_latency_ms: float = Field(default=5000.0)
    min_confidence: float = Field(default=0.85)


@router.get("/mission/{mission_id}", summary="Get Optimized Execution Plan for Mission")
async def get_mission_optimization(mission_id: str):
    """Returns authoritative ARIA-EOP optimization decision, selected strategy, and directives."""
    report = optimization_engine.optimize_mission(mission_id)
    return report.model_dump()


@router.get("/resources", summary="Get Live Resource Inventory & Capacity")
async def get_resource_inventory():
    """Returns cluster workers, LLM RPM quotas, OCR clusters, and GPU node utilization."""
    return [r.model_dump() for r in resource_registry.list_resources()]


@router.get("/strategies", summary="Get Evaluated Execution Strategies")
async def get_strategies():
    """Returns evaluated Pareto-optimal candidate strategies."""
    report = optimization_engine.optimize_mission("mission-001")
    return [report.selected_strategy.model_dump()]


@router.get("/simulations", summary="Get Monte-Carlo Simulation Scenarios")
async def get_simulations(pages: int = Query(default=4)):
    """Returns stochastic Monte-Carlo execution simulation results."""
    return [s.model_dump() for s in ExecutionSimulator.simulate_scenarios(page_count=pages)]


@router.get("/routes", summary="Get Model and Tool Routing Decisions")
async def get_routes():
    """Returns policy-driven routing decisions for LLMs, OCR engines, and verification depths."""
    m_route = ModelRouter.route_model("task-001", complexity=0.6, confidence_floor=0.90)
    o_route = OCRRouter.route_ocr("task-002", is_scanned_handwriting=False, page_count=4)
    v_route = ValidationRouter.route_validation("task-003", is_financial_audit=True)
    return [m_route.model_dump(), o_route.model_dump(), v_route.model_dump()]


@router.get("/economics", summary="Get Granular Economic & ROI Profile")
async def get_economics(
    model: str = Query(default="gemini-1.5-flash"),
    pages: int = Query(default=4),
):
    """Returns unit cost breakdown, value estimation, and ROI multiples."""
    profile = economic_engine.evaluate_economics(model_name=model, pages=pages)
    return profile.model_dump()


@router.get("/policies", summary="Get Active Optimization Policies & SLA Specs")
async def get_policies():
    """Returns active optimization policies, SLA deadlines, budget caps, and allowed models."""
    return OptimizationPolicySpec().model_dump()


@router.get("/predictions", summary="Get Calibrated Latency and Cost Predictions")
async def get_predictions(
    pages: int = Query(default=4),
    concurrency: int = Query(default=6),
    complexity: float = Query(default=0.5),
):
    """Returns probabilistic latency distribution, token cost, and success rate predictions."""
    pred = LatencyPredictor.predict(page_count=pages, concurrency=concurrency, complexity=complexity)
    return pred.model_dump()


@router.get("/explanations", summary="Get Decision Explainability & Lineage Rationale")
async def get_explanations(mission_id: str = Query(default="mission-001")):
    """Explains why specific strategy and worker allocation was selected over alternatives."""
    report = optimization_engine.optimize_mission(mission_id)
    return {
        "mission_id": mission_id,
        "winning_strategy": report.selected_strategy.strategy_name,
        "utility_score": report.selected_strategy.utility_score,
        "expected_savings_pct": report.expected_savings_pct,
        "expected_speedup_pct": report.expected_speedup_pct,
        "constraints_satisfied": report.constraint_status.is_satisfied,
        "rationale": "Selected highest multi-objective utility strategy within SLA and budget bounds.",
        "lineage_hash": "sha256:7f8a9b0c1d2e3f4a",
    }


@router.get("/history", summary="Get Historical Optimization Reports")
async def get_optimization_history():
    """Returns historical optimization runs and decisions."""
    reports = optimization_engine.list_reports()
    return [r.model_dump() for r in reports]


@router.post("/simulate", summary="Run Interactive What-If Optimization Simulation")
async def simulate_what_if(req: SimulateRequest):
    """Runs interactive what-if scenario testing budget and latency limits."""
    return WhatIfEngine.evaluate_what_if(req.target_budget_usd, req.target_latency_ms)


@router.post("/reoptimize", summary="Trigger Dynamic Re-Optimization Under New Constraints")
async def reoptimize(req: ReoptimizeRequest):
    """Dynamically re-optimizes plan execution under modified operational constraints."""
    report = optimization_engine.optimize_mission(
        mission_id=req.mission_id,
        objective=req.objective,
        max_budget_usd=req.max_budget_usd,
        max_latency_ms=req.max_latency_ms,
        min_confidence=req.min_confidence,
    )
    return report.model_dump()

