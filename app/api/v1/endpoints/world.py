"""
AWM-PSDTIP Phase 13.10 - REST API Endpoints
REST API for Autonomous World Modeling, Predictive Simulation, Digital Twin Intelligence, Causal Reasoning, Forecasting, and Predictive Governance.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel, Field

from app.runtime.world import (
    get_world_runtime,
    RiskLevel,
    HorizonScope,
    ScenarioType,
    CausalRelationType,
    SimulationMode,
)

router = APIRouter()


# Request Models
class PredictPlanRequest(BaseModel):
    mission_goal: str
    sample_trials: int = 1000


class SimulateScenarioRequest(BaseModel):
    name: str
    scenario_type: ScenarioType = ScenarioType.BASELINE
    mode: SimulationMode = SimulationMode.MONTE_CARLO
    parameters: Dict[str, Any] = Field(default_factory=dict)
    concurrency: int = 4
    trials_count: int = 100


class CounterfactualRequest(BaseModel):
    premise: str
    altered_variables: Dict[str, Any]
    target_objectives: List[str] = Field(default_factory=lambda: ["LATENCY", "COST", "SAFETY"])


class GenerateForecastRequest(BaseModel):
    target_metric: str
    horizon: HorizonScope = HorizonScope.MEDIUM_TERM
    baseline_value: float = 180.0
    historical_variance: float = 12.0


class AnalyzeRiskRequest(BaseModel):
    risk_type: str
    severity: RiskLevel
    probability: float
    impact_score: float
    description: str
    affected_components: List[str]
    mitigation: str


class OpportunityRequest(BaseModel):
    title: str
    category: str
    description: str
    latency_gain_pct: float
    cost_saving_pct: float
    confidence: float = 0.98
    directive: str


class ApprovePredictionRequest(BaseModel):
    target_prediction_id: str
    target_type: str = "PLAN_EXECUTION"
    approver_role: str = "EXECUTIVE_DIRECTOR"
    decision: str = "APPROVED"
    rationale: str = "Simulation results verified with 95% confidence bounds and 0% invariant violation risk."


class RollbackStateRequest(BaseModel):
    target_id: str
    reason: str = "Operator requested precautionary rollback"


# Endpoints

@router.get("/overview")
def get_world_overview():
    runtime = get_world_runtime()
    return runtime.get_world_overview()


@router.get("/model")
def get_world_model_state():
    runtime = get_world_runtime()
    summary = runtime.world_model.get_current_state_summary()
    entities = runtime.world_model.list_entities()
    snapshots = runtime.world_model.get_snapshots(limit=10)
    return {
        "summary": summary,
        "entities": [e.__dict__ for e in entities],
        "recent_snapshots": [
            {
                "snapshot_id": s.snapshot_id,
                "sequence_number": s.sequence_number,
                "metrics": s.metrics,
                "state_sha256_hash": s.state_sha256_hash,
                "timestamp": s.timestamp,
            }
            for s in snapshots
        ],
    }


@router.get("/digital-twin")
def get_digital_twin_status():
    runtime = get_world_runtime()
    latest = runtime.digital_twin.get_latest_twin()
    history = runtime.digital_twin.get_sync_history()
    return {
        "latest_twin": latest.__dict__ if latest else None,
        "sync_history": history,
    }


@router.get("/predictions")
def list_predictive_plans():
    runtime = get_world_runtime()
    candidates = runtime.planning.list_candidates()
    return [c.__dict__ for c in candidates]


@router.get("/simulations")
def list_simulations():
    runtime = get_world_runtime()
    results = runtime.simulation.list_results()
    return [r.__dict__ for r in results]


@router.get("/scenarios")
def list_scenarios():
    runtime = get_world_runtime()
    scenarios = runtime.simulation.list_scenarios()
    return [s.__dict__ for s in scenarios]


@router.get("/counterfactuals")
def list_counterfactuals():
    runtime = get_world_runtime()
    outcomes = runtime.counterfactual.list_outcomes()
    queries = runtime.counterfactual.list_queries()
    return {
        "outcomes": [o.__dict__ for o in outcomes],
        "queries": [q.__dict__ for q in queries],
    }


@router.get("/forecasts")
def list_forecasts():
    runtime = get_world_runtime()
    forecasts = runtime.forecasting.list_forecasts()
    return [f.__dict__ for f in forecasts]


@router.get("/risks")
def list_risks():
    runtime = get_world_runtime()
    risks = runtime.risk.list_risks()
    scorecard = runtime.risk.get_risk_scorecard()
    return {
        "scorecard": scorecard,
        "risks": [r.__dict__ for r in risks],
    }


@router.get("/opportunities")
def list_opportunities():
    runtime = get_world_runtime()
    opportunities = runtime.opportunity.list_opportunities()
    return [o.__dict__ for o in opportunities]


@router.get("/causal-graph")
def get_causal_graph():
    runtime = get_world_runtime()
    return runtime.causal.get_graph_summary()


@router.get("/beliefs")
def list_bayesian_beliefs():
    runtime = get_world_runtime()
    beliefs = runtime.bayesian.list_beliefs()
    return [b.__dict__ for b in beliefs]


@router.get("/temporal-graph")
def get_temporal_graph():
    runtime = get_world_runtime()
    return runtime.temporal.get_summary()


@router.post("/predict")
def predict_optimal_plan(req: PredictPlanRequest):
    runtime = get_world_runtime()
    candidates = runtime.planning.evaluate_candidate_plans(
        mission_goal=req.mission_goal,
        sample_trials=req.sample_trials,
    )
    return {
        "status": "PREDICTION_COMPLETED",
        "candidates": [c.__dict__ for c in candidates],
        "selected_plan": next((c.__dict__ for c in candidates if c.is_selected), candidates[0].__dict__),
    }


@router.post("/simulate")
def simulate_scenario(req: SimulateScenarioRequest):
    runtime = get_world_runtime()
    scen = runtime.simulation.create_scenario(
        name=req.name,
        scenario_type=req.scenario_type,
        mode=req.mode,
        parameters=req.parameters,
        concurrency=req.concurrency,
    )
    result = runtime.simulation.run_simulation(scen.scenario_id, trials_count=req.trials_count)
    return {
        "status": "SIMULATION_COMPLETED",
        "scenario": scen.__dict__,
        "result": result.__dict__,
    }


@router.post("/counterfactual")
def evaluate_counterfactual(req: CounterfactualRequest):
    runtime = get_world_runtime()
    outcome = runtime.counterfactual.evaluate_what_if(
        premise=req.premise,
        altered_variables=req.altered_variables,
        target_objectives=req.target_objectives,
    )
    return {
        "status": "COUNTERFACTUAL_EVALUATED",
        "outcome": outcome.__dict__,
    }


@router.post("/forecast")
def create_forecast(req: GenerateForecastRequest):
    runtime = get_world_runtime()
    forecast = runtime.forecasting.generate_forecast(
        target_metric=req.target_metric,
        horizon=req.horizon,
        baseline_value=req.baseline_value,
        historical_variance=req.historical_variance,
    )
    return {
        "status": "FORECAST_GENERATED",
        "forecast": forecast.__dict__,
    }


@router.post("/analyze-risk")
def analyze_risk(req: AnalyzeRiskRequest):
    runtime = get_world_runtime()
    risk = runtime.risk.evaluate_risk(
        risk_type=req.risk_type,
        severity=req.severity,
        probability=req.probability,
        impact_score=req.impact_score,
        description=req.description,
        affected_components=req.affected_components,
        mitigation=req.mitigation,
    )
    return {
        "status": "RISK_RECORDED",
        "risk": risk.__dict__,
    }


@router.post("/discover-opportunities")
def register_opportunity(req: OpportunityRequest):
    runtime = get_world_runtime()
    opp = runtime.opportunity.register_opportunity(
        title=req.title,
        category=req.category,
        description=req.description,
        latency_gain_pct=req.latency_gain_pct,
        cost_saving_pct=req.cost_saving_pct,
        confidence=req.confidence,
        directive=req.directive,
    )
    return {
        "status": "OPPORTUNITY_REGISTERED",
        "opportunity": opp.__dict__,
    }


@router.post("/approve")
def approve_prediction(req: ApprovePredictionRequest):
    runtime = get_world_runtime()
    ok, record, msg = runtime.governance.review_and_authorize(
        target_prediction_id=req.target_prediction_id,
        target_type=req.target_type,
        approver_role=req.approver_role,
        decision=req.decision,
        rationale=req.rationale,
    )
    if not ok:
        raise HTTPException(status_code=400, detail=msg)
    return {
        "status": "APPROVED",
        "record": record.__dict__,
        "message": msg,
    }


@router.post("/rollback")
def rollback_state(req: RollbackStateRequest):
    runtime = get_world_runtime()
    res = runtime.governance.execute_rollback(
        target_id=req.target_id,
        reason=req.reason,
    )
    return res
