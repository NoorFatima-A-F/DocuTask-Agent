"""
AMRS-RSIP Phase 13.9 - REST API Endpoints
REST API for Autonomous Meta-Reasoning, Strategic Planning, Recursive Reflection, Replay Experimentation, Capability Discovery, Policy Evolution, and Self-Improvement Governance.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel, Field

from app.runtime.meta import (
    get_meta_runtime,
    ReflectionTier,
    ImprovementStatus,
)

router = APIRouter()


# Request Models
class TriggerReasoningRequest(BaseModel):
    goal_description: str
    execution_context: Dict[str, Any] = Field(default_factory=dict)


class TriggerReflectionRequest(BaseModel):
    subject: str = "PLATFORM_AUTONOMOUS_OPERATIONS"
    max_depth: int = 7


class TriggerExperimentRequest(BaseModel):
    name: str
    control_strategy: str
    treatment_strategy: str
    historical_sample_size: int = 50
    control_latency: float = 340.0
    treatment_latency: float = 195.0
    control_cost: float = 0.045
    treatment_cost: float = 0.032


class EvolvePolicyRequest(BaseModel):
    policy_name: str
    category: str
    current_rule: str
    proposed_rule: str
    rationale: str
    evidence_backing: List[str] = Field(default_factory=list)
    predicted_impact: Dict[str, Any] = Field(default_factory=dict)


class ProposeArchitectureRequest(BaseModel):
    target_subsystem: str
    optimization_type: str
    description: str
    latency_saving_ms: float = 120.0
    memory_delta_mb: float = -15.0
    confidence_score: float = 0.98


class ApproveProposalRequest(BaseModel):
    target_proposal_id: str
    proposal_type: str = "POLICY_UPGRADE"
    approver_role: str = "EXECUTIVE_DIRECTOR"
    decision: str = "APPROVED"
    rationale: str = "Empirically verified via historical replay experimentation."


class RollbackCycleRequest(BaseModel):
    cycle_id: str
    reason: str = "Empirical regression or operator intervention"


# Endpoints


@router.get("/overview")
def get_meta_overview():
    runtime = get_meta_runtime()
    return runtime.get_meta_overview()


@router.get("/reasoning")
def list_reasoning_graphs():
    runtime = get_meta_runtime()
    graphs = runtime.reasoning.get_all_reasoning_graphs()
    bottlenecks = runtime.reasoning.get_bottlenecks()
    return {
        "graphs": [g.__dict__ for g in graphs],
        "bottlenecks": [b.__dict__ for b in bottlenecks],
    }


@router.post("/reason")
def trigger_meta_reasoning(req: TriggerReasoningRequest):
    runtime = get_meta_runtime()
    graph = runtime.reasoning.analyze_goal_and_synthesize(
        goal_description=req.goal_description,
        execution_context=req.execution_context,
    )
    return {"status": "REASONING_COMPLETED", "graph": graph.__dict__}


@router.get("/reflections")
def list_reflection_trees():
    runtime = get_meta_runtime()
    trees = runtime.reflection.get_all_trees()
    return [
        {
            "tree_id": t.tree_id,
            "target_subject": t.target_subject,
            "root_node_id": t.root_node_id,
            "merkle_tree_hash": t.merkle_tree_hash,
            "nodes_count": len(t.nodes),
            "nodes": [n.__dict__ for n in t.nodes.values()],
            "created_at": t.created_at,
        }
        for t in trees
    ]


@router.post("/reflect")
def trigger_reflection(req: TriggerReflectionRequest):
    runtime = get_meta_runtime()
    tree = runtime.reflection.execute_recursive_reflection(
        subject=req.subject,
        max_depth=req.max_depth,
    )
    return {
        "status": "REFLECTION_COMPLETED",
        "tree_id": tree.tree_id,
        "nodes": [n.__dict__ for n in tree.nodes.values()],
        "merkle_root": tree.merkle_tree_hash,
    }


@router.get("/strategies")
def list_strategic_roadmaps():
    runtime = get_meta_runtime()
    roadmaps = runtime.strategy.get_all_roadmaps()
    return [r.__dict__ for r in roadmaps]


@router.get("/experiments")
def list_experiments():
    runtime = get_meta_runtime()
    experiments = runtime.experiments.get_all_experiments()
    return [e.__dict__ for e in experiments]


@router.post("/experiment")
def trigger_replay_experiment(req: TriggerExperimentRequest):
    runtime = get_meta_runtime()
    result = runtime.experiments.run_replay_ab_test(
        name=req.name,
        control_strategy=req.control_strategy,
        treatment_strategy=req.treatment_strategy,
        historical_sample_size=req.historical_sample_size,
        control_latency=req.control_latency,
        treatment_latency=req.treatment_latency,
        control_cost=req.control_cost,
        treatment_cost=req.treatment_cost,
    )
    return {"status": "EXPERIMENT_CONCLUDED", "result": result.__dict__}


@router.get("/capabilities")
def list_capabilities():
    runtime = get_meta_runtime()
    capabilities = runtime.capabilities.get_all_capabilities()
    return [c.__dict__ for c in capabilities]


@router.get("/policies")
def list_policy_proposals():
    runtime = get_meta_runtime()
    proposals = runtime.policies.get_all_proposals()
    return [p.__dict__ for p in proposals]


@router.post("/evolve-policy")
def evolve_policy(req: EvolvePolicyRequest):
    runtime = get_meta_runtime()
    proposal = runtime.policies.propose_policy_upgrade(
        policy_name=req.policy_name,
        category=req.category,
        current_rule=req.current_rule,
        proposed_rule=req.proposed_rule,
        rationale=req.rationale,
        evidence_backing=req.evidence_backing,
        predicted_impact=req.predicted_impact,
    )
    return {"status": "PROPOSED", "proposal": proposal.__dict__}


@router.get("/architecture")
def list_architecture_proposals():
    runtime = get_meta_runtime()
    optimizations = runtime.architecture.get_all_proposals()
    return [o.__dict__ for o in optimizations]


@router.post("/propose-architecture")
def propose_architecture(req: ProposeArchitectureRequest):
    runtime = get_meta_runtime()
    proposal = runtime.architecture.propose_optimization(
        target_subsystem=req.target_subsystem,
        optimization_type=req.optimization_type,
        description=req.description,
        latency_saving_ms=req.latency_saving_ms,
        memory_delta_mb=req.memory_delta_mb,
        confidence_score=req.confidence_score,
    )
    return {"status": "PROPOSED", "optimization": proposal.__dict__}


@router.get("/self-improvement")
def list_self_improvement_cycles():
    runtime = get_meta_runtime()
    cycles = runtime.self_improvement.get_all_cycles()
    return [c.__dict__ for c in cycles]


@router.get("/history")
def get_strategic_history():
    runtime = get_meta_runtime()
    observations = runtime.observation.get_recent_observations()
    audit = runtime.governance.get_audit_trail()
    return {
        "observations": observations,
        "governance_audit": audit,
    }


@router.post("/approve")
def approve_proposal(req: ApproveProposalRequest):
    runtime = get_meta_runtime()
    ok, record, msg = runtime.governance.review_and_approve(
        target_proposal_id=req.target_proposal_id,
        proposal_type=req.proposal_type,
        approver_role=req.approver_role,
        decision=req.decision,
        rationale=req.rationale,
    )
    if not ok:
        raise HTTPException(status_code=400, detail=msg)

    # If policy proposal, mark approved
    prop = runtime.policies.get_proposal(req.target_proposal_id)
    if prop and req.decision == "APPROVED":
        prop.status = "APPROVED"

    return {"status": "APPROVED", "record": record.__dict__, "message": msg}


@router.post("/rollback")
def rollback_cycle(req: RollbackCycleRequest):
    runtime = get_meta_runtime()
    ok = runtime.self_improvement.rollback_cycle(req.cycle_id, req.reason)
    if not ok:
        raise HTTPException(status_code=404, detail=f"Self-improvement cycle {req.cycle_id} not found.")
    return {"status": "ROLLED_BACK", "cycle_id": req.cycle_id, "reason": req.reason}
