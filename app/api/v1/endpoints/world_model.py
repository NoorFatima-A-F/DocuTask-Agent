"""
Phase 13.16: Autonomous World Modeling, Predictive Intelligence & Causal Reasoning Platform (AWMPICRP).
FastAPI REST API Router exposing all 15 cognitive world model subsystems.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.runtime.world_model.events.world_model_events import (
    ObservationSource,
    WorldModelEventType,
    world_model_event_bus,
)
from app.runtime.world_model.observation.observation_engine import observation_engine
from app.runtime.world_model.knowledge.knowledge_fusion_engine import knowledge_fusion_engine
from app.runtime.world_model.world.world_engine import (
    WorldEntityNode,
    WorldGraphEdge,
    world_engine,
)
from app.runtime.world_model.temporal.temporal_engine import temporal_engine
from app.runtime.world_model.causal.causal_engine import causal_engine
from app.runtime.world_model.hypothesis.hypothesis_engine import hypothesis_engine
from app.runtime.world_model.scenario.scenario_engine import scenario_engine
from app.runtime.world_model.counterfactual.counterfactual_engine import counterfactual_engine
from app.runtime.world_model.forecasting.predictive_engine import predictive_engine
from app.runtime.world_model.decision.decision_engine import decision_engine
from app.runtime.world_model.uncertainty.uncertainty_engine import uncertainty_engine
from app.runtime.world_model.verification.prediction_verification_engine import prediction_verification_engine
from app.runtime.world_model.memory.memory_consolidation_engine import memory_consolidation_engine
from app.runtime.world_model.runtime.world_runtime import world_runtime

router = APIRouter()


# Request Models
class CognitiveCycleRequest(BaseModel):
    goal: str = "Optimize enterprise operational stability and cloud ROI"


class ObservationIngestRequest(BaseModel):
    source: str = "execution_runtime"
    entity_id: str = "service_core_api"
    metric_name: str = "p99_latency_ms"
    metric_value: float = 42.0
    metadata: Dict[str, Any] = Field(default_factory=dict)


class FactIntegrateRequest(BaseModel):
    subject: str
    predicate: str
    object_value: Any
    source_runtime: str = "execution_runtime"
    confidence: float = 0.95
    evidence_refs: List[str] = Field(default_factory=list)


class EntityNodeRequest(BaseModel):
    entity_id: str
    name: str
    category: str = "service"
    properties: Dict[str, Any] = Field(default_factory=dict)
    state: str = "healthy"
    health_score: float = 0.98


class GraphEdgeRequest(BaseModel):
    source_entity_id: str
    target_entity_id: str
    relation_type: str = "depends_on"
    weight: float = 1.0
    confidence: float = 0.95


class CausalInterventionRequest(BaseModel):
    target_variable: str
    intervention_value: Any
    observed_context: Dict[str, Any] = Field(default_factory=dict)


class HypothesisCreateRequest(BaseModel):
    title: str
    explanation: str
    phenomenon_observed: str
    prior_probability: float = 0.5
    supporting_evidence: List[str] = Field(default_factory=list)


class ScenarioGenerateRequest(BaseModel):
    context: str = "Capacity expansion 2026"


class CounterfactualQueryRequest(BaseModel):
    title: str
    intervention: str
    target_entity: str
    actual_metrics: Dict[str, Any] = Field(default_factory=dict)


class PredictionGenerateRequest(BaseModel):
    target_metric: str
    predicted_value: float
    horizon_hours: float = 24.0
    uncertainty_band: float = 0.1


class DecisionEvaluateRequest(BaseModel):
    goal_context: str = "Capacity scaling"


class UncertaintyComputeRequest(BaseModel):
    domain: str
    observation_count: int = 10
    variance: float = 0.1


class VerificationRecordRequest(BaseModel):
    prediction_id: str
    actual_value: float


# Endpoints

@router.get("/status")
def get_world_model_status():
    """Get executive overview and status of the Autonomous World Model Platform."""
    summary = world_runtime.get_world_overview()
    return {
        "status": "online",
        "phase": "13.16",
        "name": "Autonomous World Modeling, Predictive Intelligence & Causal Reasoning Platform (AWMPICRP)",
        "summary": summary,
    }


@router.post("/cycle")
def execute_cognitive_cycle(req: CognitiveCycleRequest):
    """Execute end-to-end cognitive intelligence cycle across all 15 subsystems."""
    result = world_runtime.execute_cognitive_learning_cycle(context_goal=req.goal)
    return {
        "success": True,
        "cycle": result,
    }


# Observation Subsystem
@router.post("/observations")
def ingest_observation(req: ObservationIngestRequest):
    """Ingest metric or telemetry observation."""
    try:
        src = ObservationSource(req.source)
    except Exception:
        src = ObservationSource.EXECUTION_RUNTIME

    obs = observation_engine.observe_metric(
        source=src,
        entity_id=req.entity_id,
        metric_name=req.metric_name,
        metric_value=req.metric_value,
        metadata=req.metadata,
    )
    return {"success": True, "observation": obs.to_dict()}


@router.get("/observations")
def list_observations(limit: int = Query(50, ge=1, le=500)):
    """List ingested observations."""
    obs_list = observation_engine.list_observations()
    return {
        "count": len(obs_list),
        "observations": [o.to_dict() for o in obs_list[-limit:]],
        "summary": observation_engine.get_summary(),
    }


# Knowledge Fusion Subsystem
@router.post("/knowledge/facts")
def integrate_fact(req: FactIntegrateRequest):
    """Integrate fact into knowledge graph with truth ranking."""
    fact = knowledge_fusion_engine.integrate_fact(
        subject=req.subject,
        predicate=req.predicate,
        object_value=req.object_value,
        source_runtime=req.source_runtime,
        confidence=req.confidence,
        evidence_refs=req.evidence_refs,
    )
    return {"success": True, "fact": fact.to_dict()}


@router.get("/knowledge/facts")
def list_facts(limit: int = Query(50, ge=1, le=500)):
    """List fused knowledge facts."""
    facts = knowledge_fusion_engine.list_facts()
    return {
        "count": len(facts),
        "facts": [f.to_dict() for f in facts[-limit:]],
        "summary": knowledge_fusion_engine.get_knowledge_summary(),
    }


# World Graph Subsystem
@router.post("/world/entities")
def add_world_entity(req: EntityNodeRequest):
    """Add entity node to world graph."""
    node = world_engine.add_node(
        WorldEntityNode(
            entity_id=req.entity_id,
            name=req.name,
            category=req.category,
            properties=req.properties,
            state=req.state,
            health_score=req.health_score,
        )
    )
    return {"success": True, "entity": node.to_dict()}


@router.post("/world/relations")
def add_world_relation(req: GraphEdgeRequest):
    """Add relation edge to world graph."""
    edge = world_engine.add_edge(
        WorldGraphEdge(
            source_entity_id=req.source_entity_id,
            target_entity_id=req.target_entity_id,
            relation_type=req.relation_type,
            weight=req.weight,
            confidence=req.confidence,
        )
    )
    return {"success": True, "relation": edge.to_dict()}


@router.get("/world/graph")
def get_world_graph():
    """Retrieve full probabilistic entity graph and metadata."""
    return world_engine.get_graph()


@router.post("/world/snapshots")
def create_world_snapshot():
    """Create point-in-time cryptographic checkpoint of world state."""
    chk = world_engine.create_checkpoint()
    return {"success": True, "checkpoint": chk.to_dict()}


# Temporal Subsystem
@router.get("/temporal/patterns")
def list_temporal_patterns():
    """List discovered temporal rhythms, cycles, and seasonality patterns."""
    patterns = temporal_engine.list_patterns()
    return {
        "count": len(patterns),
        "patterns": [p.to_dict() for p in patterns],
        "summary": temporal_engine.get_summary(),
    }


# Causal Reasoning Subsystem
@router.get("/causal/graph")
def get_causal_graph():
    """Get active Structural Causal Model DAG."""
    edges = causal_engine.list_causal_edges()
    return {
        "edge_count": len(edges),
        "edges": [e.to_dict() for e in edges],
        "summary": causal_engine.get_summary(),
    }


@router.post("/causal/intervene")
def perform_causal_intervention(req: CausalInterventionRequest):
    """Simulate Pearl's do-calculus intervention."""
    res = causal_engine.simulate_do_intervention(
        target_variable=req.target_variable,
        intervention_value=req.intervention_value,
    )
    return {"success": True, "intervention": res.to_dict()}


# Hypothesis Subsystem
@router.post("/hypotheses")
def create_hypothesis(req: HypothesisCreateRequest):
    """Formulate an abductive hypothesis."""
    hyp = hypothesis_engine.create_hypothesis(
        title=req.title,
        explanation=req.explanation,
        phenomenon_observed=req.phenomenon_observed,
        prior_probability=req.prior_probability,
        supporting_evidence=req.supporting_evidence,
    )
    return {"success": True, "hypothesis": hyp.to_dict()}


@router.get("/hypotheses")
def list_hypotheses():
    """List operational hypotheses and Bayesian probabilities."""
    hyps = hypothesis_engine.list_hypotheses()
    return {
        "count": len(hyps),
        "hypotheses": [h.to_dict() for h in hyps],
        "summary": hypothesis_engine.get_summary(),
    }


# Scenario Subsystem
@router.post("/scenarios/simulate")
def generate_scenarios(req: ScenarioGenerateRequest):
    """Generate multi-branch stochastic scenarios."""
    scens = scenario_engine.generate_scenarios_for_context(context_title=req.context)
    return {
        "success": True,
        "count": len(scens),
        "scenarios": [s.to_dict() for s in scens],
    }


@router.get("/scenarios")
def list_scenarios():
    """List simulated future scenario branches."""
    scens = scenario_engine.list_scenarios()
    return {
        "count": len(scens),
        "scenarios": [s.to_dict() for s in scens],
        "summary": scenario_engine.get_summary(),
    }


# Counterfactual Subsystem
@router.post("/counterfactuals/simulate")
def run_counterfactual(req: CounterfactualQueryRequest):
    """Execute counterfactual twin-world query."""
    exp = counterfactual_engine.run_counterfactual_query(
        title=req.title,
        intervention=req.intervention,
        target_entity=req.target_entity,
        actual_metrics=req.actual_metrics,
    )
    return {"success": True, "counterfactual": exp.to_dict()}


@router.get("/counterfactuals")
def list_counterfactuals():
    """List counterfactual experiments."""
    exps = counterfactual_engine.list_experiments()
    return {
        "count": len(exps),
        "counterfactuals": [e.to_dict() for e in exps],
        "summary": counterfactual_engine.get_summary(),
    }


# Forecasting Subsystem
@router.post("/forecasts/generate")
def generate_prediction(req: PredictionGenerateRequest):
    """Generate multi-horizon forecast with 95% CI."""
    pred = predictive_engine.generate_prediction(
        target_metric=req.target_metric,
        predicted_value=req.predicted_value,
        horizon_hours=req.horizon_hours,
        uncertainty_band=req.uncertainty_band,
    )
    return {"success": True, "prediction": pred.to_dict()}


@router.get("/forecasts")
def list_predictions():
    """List active forecast predictions."""
    preds = predictive_engine.list_predictions()
    return {
        "count": len(preds),
        "predictions": [p.to_dict() for p in preds],
        "summary": predictive_engine.get_summary(),
    }


# Decision Intelligence Subsystem
@router.post("/decisions/evaluate")
def evaluate_decisions(req: DecisionEvaluateRequest):
    """Evaluate and rank decision portfolio by expected utility."""
    decs = decision_engine.evaluate_decision_portfolio(context_goal=req.goal_context)
    return {
        "success": True,
        "count": len(decs),
        "decisions": [d.to_dict() for d in decs],
    }


@router.get("/decisions/portfolios")
def list_decisions():
    """List ranked decision options."""
    decs = decision_engine.list_decisions()
    return {
        "count": len(decs),
        "decisions": [d.to_dict() for d in decs],
        "summary": decision_engine.get_summary(),
    }


# Uncertainty Subsystem
@router.post("/uncertainty/compute")
def compute_uncertainty(req: UncertaintyComputeRequest):
    """Compute epistemic vs. aleatoric uncertainty profile."""
    prof = uncertainty_engine.compute_uncertainty(
        domain=req.domain,
        observation_count=req.observation_count,
        variance=req.variance,
    )
    return {"success": True, "uncertainty": prof.to_dict()}


@router.get("/uncertainty")
def list_uncertainty_profiles():
    """List uncertainty profiles."""
    profs = uncertainty_engine.list_profiles()
    return {
        "count": len(profs),
        "profiles": [p.to_dict() for p in profs],
        "summary": uncertainty_engine.get_summary(),
    }


# Verification & Calibration Subsystem
@router.post("/verifications/record")
def record_verification(req: VerificationRecordRequest):
    """Record ground truth verification and update calibration."""
    res = prediction_verification_engine.record_ground_truth(
        prediction_id=req.prediction_id,
        actual_value=req.actual_value,
    )
    return {"success": True, "verification": res.to_dict()}


@router.get("/verifications")
def list_verifications():
    """List verification records and calibration accuracy metrics."""
    records = prediction_verification_engine.list_verifications()
    return {
        "count": len(records),
        "verifications": [r.to_dict() for r in records],
        "calibration": prediction_verification_engine.get_calibration_summary(),
    }


# Cognitive Memory Subsystem
@router.get("/memory/records")
def list_memory_records():
    """List consolidated cognitive memory blocks."""
    mems = memory_consolidation_engine.list_memories()
    return {
        "count": len(mems),
        "memories": [m.to_dict() for m in mems],
        "summary": memory_consolidation_engine.get_summary(),
    }


# Events Stream & Audit Trail
@router.get("/events")
def list_world_events(limit: int = Query(100, ge=1, le=1000)):
    """List recent world model domain events from event bus."""
    history = world_model_event_bus.get_history(limit=limit)
    return {
        "count": len(history),
        "events": history,
    }
