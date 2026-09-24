"""
FastAPI Endpoints for Autonomous Scientific Validation & Self-Evolution Platform (ASVSP).
Exposes comprehensive validation, prediction error quantification, counterfactual replay,
digital twin execution, online drift detection, experiment engines, SCM causal analysis,
policy self-evolution, and cryptographic certification.
"""

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

# 1. Outcomes
from app.runtime.outcomes import (
    OutcomeCollector,
    OutcomeStatisticsTracker,
)

# 2. Predictions
from app.runtime.predictions import (
    PredictionErrorEngine,
    ResidualAnalyzer,
    PredictionValidator,
)

# 3. Counterfactual
from app.runtime.counterfactual import (
    CounterfactualSimulator,
)

# 4. Digital Twin
from app.runtime.digital_twin import (
    DigitalTwinEngine,
)

# 5. Drift
from app.runtime.drift import (
    OnlineDriftDetector,
)

# 6. Experiments
from app.runtime.experiments import (
    ExperimentEngine,
)

# 7. Causal Analysis
from app.runtime.causal_analysis import (
    CausalAnalysisEngine,
)

# 8. Self-Evolution
from app.runtime.self_evolution import (
    SelfEvolutionEngine,
)

# 9. Research
from app.runtime.research import (
    AutonomousResearchEngine,
)

# 10. Certification
from app.runtime.certification import (
    ScientificCertificationEngine,
)

router = APIRouter()

# Singletons for runtime state
outcome_collector = OutcomeCollector()
outcome_stats = OutcomeStatisticsTracker()
pred_error_engine = PredictionErrorEngine()
pred_validator = PredictionValidator()
counterfactual_sim = CounterfactualSimulator()
digital_twin_engine = DigitalTwinEngine()
drift_detector = OnlineDriftDetector()
experiment_engine = ExperimentEngine()
causal_engine = CausalAnalysisEngine()
evolution_engine = SelfEvolutionEngine()
research_engine = AutonomousResearchEngine()
certification_engine = ScientificCertificationEngine()

# Seed default outcomes for live demonstration
for i in range(15):
    outcome_collector.record_outcome(
        mission_id=f"mission_seed_{i}",
        task_id=f"task_parse_{i}",
        predicted_accuracy=0.96 + (i % 3) * 0.01,
        observed_accuracy=0.95 + (i % 4) * 0.01,
        predicted_latency_ms=480.0 + (i % 5) * 20.0,
        observed_latency_ms=475.0 + (i % 6) * 25.0,
        predicted_cost_usd=0.0020,
        observed_cost_usd=0.0019 + (i % 3) * 0.0001,
        sla_target_ms=1000.0,
    )


# -------------------------------------------------------------
# Request Schemas
# -------------------------------------------------------------
class VerifyOutcomeRequest(BaseModel):
    mission_id: str
    task_id: str
    predicted_accuracy: float
    observed_accuracy: float
    predicted_latency_ms: float
    observed_latency_ms: float
    predicted_cost_usd: float
    observed_cost_usd: float
    sla_target_ms: float = 1000.0


class CounterfactualReplayRequest(BaseModel):
    mission_id: str = "mission_demo_1"
    factual_model: str = "gemini-2.5-flash"
    factual_accuracy: float = 0.962
    factual_latency_ms: float = 480.0
    factual_cost_usd: float = 0.0018
    factual_utility: float = 0.884
    scenario_id: str = "sc_nominal"


class ShadowRunRequest(BaseModel):
    mission_id: str = "mission_shadow_001"
    prod_policy: str = "v4.2-pareto"
    shadow_policy: str = "v5.0-bayesian-candidate"
    prod_output: str = "Invoice INV-2026 total $1,420.50 parsed with high confidence."
    prod_latency_ms: float = 520.0
    prod_tokens: int = 1250
    prod_decision: str = "EXECUTE_PARALLEL_FLASH"


class RecordDriftPointRequest(BaseModel):
    metric_name: str
    value: float


class AnalyzeExperimentRequest(BaseModel):
    experiment_id: str
    mode: str = Field(default="frequentist", description="'frequentist' or 'bayesian'")
    alpha: float = 0.05


class DoInterventionRequest(BaseModel):
    treatment: str = "model_choice"
    treatment_value: str = "gemini-1.5-pro"
    outcome: str = "accuracy"
    baseline_value: str = "gemini-2.5-flash"


class CausalAttributionRequest(BaseModel):
    target_metric: str = "latency_ms"
    observed_value: float = 2450.0
    expected_baseline: float = 480.0
    observed_retry_count: int = 3
    observed_ocr_confidence: float = 0.68
    selected_model: str = "gemini-1.5-pro"


class MutatePolicyRequest(BaseModel):
    base_policy_id: str
    mutation_name: str
    delta_weight_cost: float = 0.05


class RollbackRequest(BaseModel):
    active_policy_id: str
    reason: str


class GateSignoffRequest(BaseModel):
    package_id: str
    stage: str
    approver_role: str
    approver_identity: str
    comments: str = ""


# -------------------------------------------------------------
# Endpoints
# -------------------------------------------------------------

# 1. Outcomes
@router.get("/outcomes", summary="List verified empirical outcomes")
async def get_outcomes():
    records = outcome_collector.get_all_records()
    summary = outcome_stats.compute_window_statistics(records)
    return {
        "total_verified": len(records),
        "statistics": summary.to_dict(),
        "recent_records": [r.to_dict() for r in records[-30:]],
    }


@router.post("/outcomes/verify", summary="Verify and store empirical outcome")
async def verify_outcome(req: VerifyOutcomeRequest):
    record = outcome_collector.record_outcome(
        mission_id=req.mission_id,
        task_id=req.task_id,
        predicted_accuracy=req.predicted_accuracy,
        observed_accuracy=req.observed_accuracy,
        predicted_latency_ms=req.predicted_latency_ms,
        observed_latency_ms=req.observed_latency_ms,
        predicted_cost_usd=req.predicted_cost_usd,
        observed_cost_usd=req.observed_cost_usd,
        sla_target_ms=req.sla_target_ms,
    )
    return record.to_dict()


# 2. Predictions
@router.get("/predictions/metrics", summary="Quantify prediction error metrics")
async def get_prediction_metrics():
    records = outcome_collector.get_all_records()
    if not records:
        return {"error": "No verified records available"}

    preds_acc = [r.predicted_accuracy for r in records]
    obs_acc = [r.observed_accuracy for r in records]
    preds_lat = [r.predicted_latency_ms for r in records]
    obs_lat = [r.observed_latency_ms for r in records]

    acc_error = pred_error_engine.evaluate_errors(preds_acc, obs_acc)
    lat_error = pred_error_engine.evaluate_errors(preds_lat, obs_lat)
    residuals = ResidualAnalyzer.analyze_residuals(preds_lat, obs_lat)
    validation = pred_validator.validate_prediction_bounds(acc_error, lat_error)

    return {
        "accuracy_error_metrics": acc_error.to_dict(),
        "latency_error_metrics": lat_error.to_dict(),
        "residual_analysis": residuals.to_dict(),
        "validation_report": validation.to_dict(),
    }


# 3. Counterfactual Simulator
@router.get("/counterfactual/scenarios", summary="List counterfactual environmental scenarios")
async def list_counterfactual_scenarios():
    return counterfactual_sim.get_available_scenarios()


@router.post("/counterfactual/replay", summary="Run counterfactual branch replay")
async def replay_counterfactual(req: CounterfactualReplayRequest):
    return counterfactual_sim.run_replay(
        mission_id=req.mission_id,
        factual_model=req.factual_model,
        factual_accuracy=req.factual_accuracy,
        factual_latency_ms=req.factual_latency_ms,
        factual_cost_usd=req.factual_cost_usd,
        factual_utility=req.factual_utility,
        scenario_id=req.scenario_id,
    )


# 4. Digital Twin
@router.get("/digital-twin/status", summary="Get digital twin status and aggregate fidelity")
async def get_digital_twin_status():
    return {
        "aggregate_fidelity": digital_twin_engine.get_aggregated_fidelity(),
        "recent_shadow_runs": digital_twin_engine.get_shadow_history(limit=20),
    }


@router.post("/digital-twin/shadow-run", summary="Execute shadow mission in safety sandbox")
async def run_shadow_simulation(req: ShadowRunRequest):
    return digital_twin_engine.run_shadow_simulation(
        mission_id=req.mission_id,
        prod_policy=req.prod_policy,
        shadow_policy=req.shadow_policy,
        prod_output=req.prod_output,
        prod_latency_ms=req.prod_latency_ms,
        prod_tokens=req.prod_tokens,
        prod_decision=req.prod_decision,
    )


# 5. Drift Detection
@router.get("/drift/status", summary="Get statistical drift and sequential alarm status")
async def get_drift_status():
    return drift_detector.analyze_drift()


@router.post("/drift/record", summary="Record streaming metric value into drift detector")
async def record_drift_point(req: RecordDriftPointRequest):
    drift_detected = drift_detector.record_observation(req.metric_name, req.value)
    return {
        "metric_name": req.metric_name,
        "recorded_value": req.value,
        "drift_detected": drift_detected,
    }


# 6. Experiments
@router.get("/experiments", summary="List scientific experiments")
async def list_experiments():
    return experiment_engine.list_all_experiments()


@router.post("/experiments/analyze", summary="Run frequentist or Bayesian analysis on an experiment")
async def analyze_experiment(req: AnalyzeExperimentRequest):
    if req.mode == "bayesian":
        return experiment_engine.run_bayesian_analysis(req.experiment_id)
    return experiment_engine.run_frequentist_analysis(req.experiment_id, alpha=req.alpha)


# 7. Causal Analysis
@router.get("/causal/graph", summary="Get SCM DAG graph")
async def get_causal_graph():
    return causal_engine.get_causal_graph()


@router.post("/causal/do-intervention", summary="Compute Pearl's do-calculus intervention ATE")
async def compute_do_intervention(req: DoInterventionRequest):
    return causal_engine.simulate_do_intervention(
        treatment=req.treatment,
        treatment_value=req.treatment_value,
        outcome=req.outcome,
        baseline_value=req.baseline_value,
    )


@router.post("/causal/attribution", summary="Attribute performance anomaly to root causes")
async def compute_causal_attribution(req: CausalAttributionRequest):
    return causal_engine.run_root_cause_attribution(
        target_metric=req.target_metric,
        observed_value=req.observed_value,
        expected_baseline=req.expected_baseline,
        observed_retry_count=req.observed_retry_count,
        observed_ocr_confidence=req.observed_ocr_confidence,
        selected_model=req.selected_model,
    )


# 8. Self-Evolution
@router.get("/evolution/policies", summary="List versioned policy lifecycle states")
async def list_evolution_policies():
    return {
        "policies": evolution_engine.list_all_policies(),
        "rollback_log": evolution_engine.get_rollback_audit_log(),
    }


@router.post("/evolution/mutate", summary="Propose candidate policy mutation")
async def mutate_policy(req: MutatePolicyRequest):
    return evolution_engine.propose_candidate_mutation(
        base_policy_id=req.base_policy_id,
        mutation_name=req.mutation_name,
        delta_weight_cost=req.delta_weight_cost,
    )


@router.post("/evolution/rollback", summary="Execute instant atomic rollback")
async def execute_rollback(req: RollbackRequest):
    return evolution_engine.trigger_instant_rollback(
        active_policy_id=req.active_policy_id,
        reason=req.reason,
    )


# 9. Autonomous Research
@router.get("/research/hypotheses", summary="Generate research hypotheses from telemetry")
async def get_research_hypotheses(
    p95_lat: float = Query(default=950.0),
    cost: float = Query(default=0.008),
    ocr: float = Query(default=0.82),
):
    return research_engine.generate_hypotheses(
        p95_latency_ms=p95_lat,
        avg_cost_usd=cost,
        ocr_confidence=ocr,
    )


@router.post("/research/bandit/sample", summary="Sample exploration arm from multi-armed bandit")
async def sample_bandit():
    return research_engine.select_exploration_candidate()


# 10. Certification & Governance
@router.get("/certification/packages", summary="List scientific certification packages")
async def list_certification_packages():
    return certification_engine.list_packages()


@router.post("/certification/signoff", summary="Submit governance gate approval")
async def submit_signoff(req: GateSignoffRequest):
    return certification_engine.submit_gate_signoff(
        package_id=req.package_id,
        stage=req.stage,
        approver_role=req.approver_role,
        approver_identity=req.approver_identity,
        comments=req.comments,
    )
