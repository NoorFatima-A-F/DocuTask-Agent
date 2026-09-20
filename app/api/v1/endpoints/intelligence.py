"""
Intelligence & Continuous Optimization REST API Endpoints for Phase 10 (AISLCOP).

Provides RESTful access to experiences, mined strategies, hypotheses, A/B experiments,
planner evolution, evidence knowledge graphs, consensus, predictions, and continuous improvement pipelines.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.runtime.intelligence.consensus.consensus_engine import (
    AgentContribution,
    ConsensusEngine,
)
from app.runtime.intelligence.continuous.continuous_improvement import (
    ContinuousImprovementEngine,
)
from app.runtime.intelligence.experience.experience_extractor import ExperienceExtractor
from app.runtime.intelligence.experience.experience_record import (
    ExperienceRecord,
    ExperienceStore,
)
from app.runtime.intelligence.experiments.ab_validator import ABValidator
from app.runtime.intelligence.hypothesis.hypothesis_engine import HypothesisEngine
from app.runtime.intelligence.knowledge.graph_query import GraphQueryEngine
from app.runtime.intelligence.knowledge.knowledge_graph import (
    AdaptiveKnowledgeGraph,
    GraphEdge,
    GraphNode,
)
from app.runtime.intelligence.organizational.org_learning import OrgLearningEngine
from app.runtime.intelligence.planner_opt.planner_optimizer import PlannerOptimizer
from app.runtime.intelligence.planner_opt.planner_version import PlannerVersionManager
from app.runtime.intelligence.planner_opt.prediction_error import PredictionErrorAnalyzer
from app.runtime.intelligence.predictive.predictive_mission import (
    PredictiveMissionEngine,
)
from app.runtime.intelligence.routing.adaptive_routing import (
    AdaptiveResourceOptimizer,
)
from app.runtime.intelligence.strategy.strategy_library import StrategyLibrary
from app.runtime.intelligence.strategy.strategy_miner import StrategyMiner

router = APIRouter()

# Singleton in-memory platform state
_exp_store = ExperienceStore()
_exp_extractor = ExperienceExtractor(_exp_store)
_strat_miner = StrategyMiner()
_strat_lib = StrategyLibrary()
_hyp_engine = HypothesisEngine()
_ab_validator = ABValidator()
_ver_manager = PlannerVersionManager()
_err_analyzer = PredictionErrorAnalyzer()
_planner_opt = PlannerOptimizer(_ver_manager, _err_analyzer)
_kg = AdaptiveKnowledgeGraph()
_kg_query = GraphQueryEngine(_kg)
_consensus_engine = ConsensusEngine()
_routing_opt = AdaptiveResourceOptimizer()
_pred_engine = PredictiveMissionEngine()
_org_learning = OrgLearningEngine()
_ci_engine = ContinuousImprovementEngine(
    strategy_library=_strat_lib,
    strategy_miner=_strat_miner,
    hypothesis_engine=_hyp_engine,
    ab_validator=_ab_validator,
    planner_optimizer=_planner_opt,
)


def _seed_initial_intelligence_data():
    """Seeds rich initial operational data for demonstrations and live testing."""
    if _exp_store.count() > 0:
        return

    # Seed 15 diverse experience records
    domains = ["invoice", "contract", "medical", "receipt", "purchase_order"]
    for i in range(15):
        dom = domains[i % len(domains)]
        _exp_extractor.extract_from_mission(
            mission_id=f"msn_{1000 + i}",
            document_type=dom,
            task_type="extraction",
            telemetry={
                "total_latency_ms": 900.0 + (i * 75.0) % 800,
                "total_cost_usd": 0.008 + (i * 0.002) % 0.02,
                "initial_confidence": 0.86,
                "final_confidence": 0.96 + (i % 3) * 0.01,
                "retries_count": 1 if i % 4 == 0 else 0,
                "validation_failures_count": 1 if i % 5 == 0 else 0,
                "planner_version": "v1.0.0",
                "department": "Financial Operations" if "invoice" in dom or "receipt" in dom else "Legal & Compliance",
            },
            dag_info={"depth": 4, "node_count": 6, "nodes": ["ocr", "extract", "validate", "sign"]},
            evidence_root_hash=f"0x{i:04x}abcdef1234567890",
        )

    # Seed strategies
    all_exps = _exp_store.list_all()
    inv_exps = [e for e in all_exps if e.document_type == "invoice"]
    if inv_exps:
        strat = _strat_miner.mine_from_experiences(inv_exps, strategy_name="Standard High-Speed Invoice Pipeline")
        if strat:
            strat.is_promoted = True
            _strat_lib.register_strategy(strat)

    # Seed hypotheses
    _hyp_engine.generate_from_experiences(all_exps)

    # Seed Knowledge Graph
    n_mission = GraphNode(node_id="msn_1001", node_type="MISSION", label="Invoice Mission 1001")
    n_entity = GraphNode(node_id="ent_invoice", node_type="ENTITY", label="Invoice Schema")
    n_strat = GraphNode(node_id="strat_invoice_fast", node_type="STRATEGY", label="High-Speed Invoice Pipeline")
    n_evidence = GraphNode(node_id="ev_root_001", node_type="EVIDENCE", label="Merkle Root 0x0001abcdef")
    n_outcome = GraphNode(node_id="out_success_001", node_type="OUTCOME", label="Verified Output JSON")

    _kg.add_node(n_mission)
    _kg.add_node(n_entity)
    _kg.add_node(n_strat)
    _kg.add_node(n_evidence)
    _kg.add_node(n_outcome)

    _kg.add_edge(GraphEdge(edge_id="e1", source_id="msn_1001", target_id="ent_invoice", relationship="PROCESSES_ENTITY"))
    _kg.add_edge(GraphEdge(edge_id="e2", source_id="msn_1001", target_id="strat_invoice_fast", relationship="APPLIES_STRATEGY"))
    _kg.add_edge(GraphEdge(edge_id="e3", source_id="msn_1001", target_id="ev_root_001", relationship="SUPPORTED_BY_EVIDENCE", evidence_hash="0x0001abcdef"))
    _kg.add_edge(GraphEdge(edge_id="e4", source_id="ev_root_001", target_id="out_success_001", relationship="PRODUCED_OUTCOME", evidence_hash="0x0001abcdef"))


_seed_initial_intelligence_data()


# ---------------------------------------------------------------------------
# Request / Response Schemas
# ---------------------------------------------------------------------------

class ExtractExperienceRequest(BaseModel):
    mission_id: str
    document_type: str
    task_type: str = "extraction"
    telemetry: Dict[str, Any] = Field(default_factory=dict)
    dag_info: Optional[Dict[str, Any]] = None
    evidence_root_hash: str = ""
    status: str = "SUCCESS"


class MineStrategyRequest(BaseModel):
    document_type: str
    strategy_name: Optional[str] = None


class PromoteStrategyRequest(BaseModel):
    strategy_id: str


class RunExperimentRequest(BaseModel):
    title: str
    hypothesis_id: str
    control_strategy_id: str
    candidate_strategy_id: str
    sample_size: int = 10


class EvaluateConsensusRequest(BaseModel):
    contributions: List[Dict[str, Any]]
    consensus_id: Optional[str] = None


class ForecastMissionRequest(BaseModel):
    mission_id: str
    document_type: str
    task_type: str = "extraction"
    doc_size_bytes: int = 150000


class EvaluatePredictionRequest(BaseModel):
    prediction_id: str
    actual_telemetry: Dict[str, Any]


class ContinuousCycleRequest(BaseModel):
    domain: str = "invoice"
    auto_deploy: bool = True


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/summary")
def get_intelligence_summary() -> Dict[str, Any]:
    return {
        "status": "OPERATIONAL",
        "total_experiences": _exp_store.count(),
        "total_strategies": _strat_lib.count(),
        "total_hypotheses": len(_hyp_engine.list_all()),
        "total_experiments": len(_ab_validator.list_all()),
        "active_planner_version": _ver_manager.get_active().version_id,
        "knowledge_graph_nodes": len(_kg._nodes),
        "knowledge_graph_edges": len(_kg._edges),
        "prediction_accuracy_summary": _err_analyzer.compute_summary(),
        "departments_tracked": len(_org_learning.list_departments()),
        "continuous_pipelines": len(_ci_engine.list_pipelines()),
    }


# Pillar 1: Experience Endpoints
@router.get("/experience")
def list_experiences(
    document_type: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    records = _exp_store.query(document_type=document_type, status=status, limit=limit)
    return [r.to_dict() for r in records]


@router.get("/experience/{experience_id}")
def get_experience(experience_id: str) -> Dict[str, Any]:
    rec = _exp_store.get(experience_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Experience record not found")
    return rec.to_dict()


@router.post("/experience/extract")
def extract_experience(req: ExtractExperienceRequest) -> Dict[str, Any]:
    rec = _exp_extractor.extract_from_mission(
        mission_id=req.mission_id,
        document_type=req.document_type,
        task_type=req.task_type,
        telemetry=req.telemetry,
        dag_info=req.dag_info,
        evidence_root_hash=req.evidence_root_hash,
        status=req.status,
    )
    return rec.to_dict()


# Pillar 2: Strategy Endpoints
@router.get("/strategies")
def list_strategies(domain: Optional[str] = None, promoted_only: bool = False) -> List[Dict[str, Any]]:
    strategies = _strat_lib.find_strategies(domain=domain, promoted_only=promoted_only)
    return [s.to_dict() for s in strategies]


@router.post("/strategies/mine")
def mine_strategy(req: MineStrategyRequest) -> Dict[str, Any]:
    exps = _exp_store.query(document_type=req.document_type, limit=50)
    if not exps:
        raise HTTPException(status_code=400, detail="No experiences found for requested document type")
    strat = _strat_miner.mine_from_experiences(exps, strategy_name=req.strategy_name)
    if not strat:
        raise HTTPException(status_code=400, detail="Unable to mine strategy from experiences")
    _strat_lib.register_strategy(strat)
    return strat.to_dict()


@router.post("/strategies/promote")
def promote_strategy(req: PromoteStrategyRequest) -> Dict[str, Any]:
    success = _strat_lib.promote_strategy(req.strategy_id)
    if not success:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return {"promoted": True, "strategy_id": req.strategy_id}


# Pillar 3: Planner Evolution Endpoints
@router.get("/planner/evolution")
def get_planner_evolution() -> Dict[str, Any]:
    return {
        "active_version": _ver_manager.get_active().to_dict(),
        "versions": [v.to_dict() for v in _ver_manager.list_versions()],
        "error_metrics": _err_analyzer.compute_summary(),
        "recent_errors": [r.to_dict() for r in _err_analyzer.get_recent(20)],
    }


@router.post("/planner/optimize")
def optimize_planner(target_metric: str = "latency_ms") -> Dict[str, Any]:
    exps = _exp_store.list_all(50)
    candidate = _planner_opt.formulate_candidate_optimization(target_metric=target_metric, experiences=exps)
    return candidate.to_dict()


@router.post("/planner/rollback")
def rollback_planner(target_version_id: str) -> Dict[str, Any]:
    rolled = _ver_manager.rollback(target_version_id)
    if not rolled:
        raise HTTPException(status_code=404, detail="Target version not found")
    return rolled.to_dict()


# Pillar 4: Hypothesis Endpoints
@router.get("/hypotheses")
def list_hypotheses(status: Optional[str] = None) -> List[Dict[str, Any]]:
    hypotheses = _hyp_engine.list_all()
    return [h.to_dict() for h in hypotheses]


@router.post("/hypotheses/generate")
def generate_hypotheses(domain: Optional[str] = None) -> List[Dict[str, Any]]:
    exps = _exp_store.list_all(50)
    generated = _hyp_engine.generate_from_experiences(exps, domain=domain)
    return [h.to_dict() for h in generated]


# Pillar 5: Experiments & A/B Validation Endpoints
@router.get("/experiments")
def list_experiments() -> List[Dict[str, Any]]:
    runs = _ab_validator.list_all()
    return [r.to_dict() for r in runs]


@router.get("/experiments/{experiment_id}")
def get_experiment(experiment_id: str) -> Dict[str, Any]:
    run = _ab_validator.get(experiment_id)
    if not run:
        raise HTTPException(status_code=404, detail="Experiment run not found")
    return run.to_dict()


@router.post("/experiments/run")
def run_experiment(req: RunExperimentRequest) -> Dict[str, Any]:
    ctrl = _strat_lib.get(req.control_strategy_id)
    cand = _strat_lib.get(req.candidate_strategy_id)
    if not ctrl or not cand:
        raise HTTPException(status_code=404, detail="Control or Candidate strategy not found in library")

    run = _ab_validator.run_experiment(
        title=req.title,
        hypothesis_id=req.hypothesis_id,
        control_strategy=ctrl,
        candidate_strategy=cand,
        sample_size=req.sample_size,
    )
    return run.to_dict()


# Pillar 6: Knowledge Graph Endpoints
@router.get("/knowledge/graph")
def get_knowledge_graph(root_node_id: Optional[str] = None) -> Dict[str, Any]:
    if root_node_id:
        return _kg.get_subgraph(root_node_id)
    return _kg.serialize_full_graph()


@router.post("/knowledge/query")
def query_knowledge_graph(domain_label: str) -> Dict[str, Any]:
    strategies = _kg_query.find_strategies_for_domain(domain_label)
    return {"query": domain_label, "linked_strategies": strategies}


# Pillar 7: Consensus Intelligence Endpoints
@router.get("/consensus/deliberation")
def get_sample_consensus() -> Dict[str, Any]:
    sample_contribs = [
        AgentContribution(
            agent_id="ChiefPlanner",
            department="Planning Dept",
            confidence=0.96,
            recommendation="APPROVE",
            risk_score=0.04,
            supporting_evidence_hashes=["0x0001abcdef", "0x0002abcdef"],
            rationale="All schema invariants passed with >99% confidence.",
            weight_multiplier=1.2,
        ),
        AgentContribution(
            agent_id="ComplianceOfficer",
            department="Governance Dept",
            confidence=0.94,
            recommendation="APPROVE",
            risk_score=0.06,
            supporting_evidence_hashes=["0x0001abcdef"],
            rationale="Policy rules validated with no privacy violations.",
            weight_multiplier=1.1,
        ),
        AgentContribution(
            agent_id="AuditWorker",
            department="QA Dept",
            confidence=0.88,
            recommendation="APPROVE",
            risk_score=0.10,
            supporting_evidence_hashes=["0x0003abcdef"],
            rationale="Merkle integrity verified.",
            weight_multiplier=1.0,
        ),
    ]
    res = _consensus_engine.evaluate_consensus(sample_contribs)
    return res.to_dict()


@router.post("/consensus/evaluate")
def evaluate_consensus(req: EvaluateConsensusRequest) -> Dict[str, Any]:
    contribs = []
    for c in req.contributions:
        contribs.append(
            AgentContribution(
                agent_id=c.get("agent_id", "Agent"),
                department=c.get("department", "Operations"),
                confidence=c.get("confidence", 0.90),
                recommendation=c.get("recommendation", "APPROVE"),
                risk_score=c.get("risk_score", 0.05),
                supporting_evidence_hashes=c.get("supporting_evidence_hashes", []),
                rationale=c.get("rationale", ""),
                weight_multiplier=c.get("weight_multiplier", 1.0),
            )
        )
    res = _consensus_engine.evaluate_consensus(contribs, consensus_id=req.consensus_id)
    return res.to_dict()


# Pillar 8 & 9: Predictions & Routing Endpoints
@router.get("/predictions/forecast")
def forecast_mission(
    mission_id: str = "msn_forecast_sample",
    document_type: str = "invoice",
    doc_size_bytes: int = 150000,
) -> Dict[str, Any]:
    exps = _exp_store.list_all(50)
    pred = _pred_engine.forecast_mission(
        mission_id=mission_id,
        document_type=document_type,
        doc_size_bytes=doc_size_bytes,
        historical_experiences=exps,
    )
    return pred.to_dict()


@router.post("/predictions/evaluate")
def evaluate_prediction(req: EvaluatePredictionRequest) -> Dict[str, Any]:
    pred = _pred_engine.evaluate_actuals(req.prediction_id, req.actual_telemetry)
    if not pred:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return pred.to_dict()


@router.get("/routing/profiles")
def list_routing_profiles() -> List[Dict[str, Any]]:
    return [p.to_dict() for p in _routing_opt.list_profiles()]


# Pillar 10: Organizational Learning Endpoints
@router.get("/organizational/expertise")
def list_department_expertise() -> List[Dict[str, Any]]:
    return [d.to_dict() for d in _org_learning.list_departments()]


# Pillar 11: Continuous Improvement Pipelines
@router.get("/continuous/pipeline")
def list_continuous_pipelines() -> List[Dict[str, Any]]:
    return [p.to_dict() for p in _ci_engine.list_pipelines()]


@router.post("/continuous/cycle")
def trigger_continuous_cycle(req: ContinuousCycleRequest) -> Dict[str, Any]:
    exps = _exp_store.query(document_type=req.domain, limit=50)
    if not exps:
        exps = _exp_store.list_all(50)
    rec = _ci_engine.initiate_cycle(domain=req.domain, experiences=exps, auto_deploy=req.auto_deploy)
    return rec.to_dict()


@router.post("/continuous/rollback")
def rollback_continuous_pipeline(pipeline_id: str) -> Dict[str, Any]:
    success = _ci_engine.rollback_pipeline(pipeline_id)
    if not success:
        raise HTTPException(status_code=400, detail="Pipeline rollback failed or pipeline not found")
    return {"rolled_back": True, "pipeline_id": pipeline_id}
