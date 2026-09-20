"""
REST API Endpoints for Phase 13.5 Autonomous Reflection, Learning, Policy Evolution & Knowledge Intelligence Platform (ARLP-KIP).
Provides API endpoints for reflection engines, pattern miners, knowledge graphs, policy simulations, and governance approval pipelines.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, Query, status

from app.runtime.learning.reflection.reflection_engine import reflection_engine, MissionReflectionReport
from app.runtime.learning.learning.learning_engine import learning_engine, MinedLesson
from app.runtime.learning.knowledge.knowledge_registry import knowledge_registry, KnowledgeRecord
from app.runtime.learning.knowledge.knowledge_graph import knowledge_graph
from app.runtime.learning.knowledge.knowledge_search import knowledge_search_engine
from app.runtime.learning.knowledge.knowledge_lineage import knowledge_lineage_tracker
from app.runtime.learning.policy.policy_engine import policy_engine, CandidatePolicy
from app.runtime.learning.policy.policy_registry import evolution_policy_registry
from app.runtime.learning.governance.learning_governance import learning_governance_gatekeeper
from app.runtime.learning.governance.approval_workflow import approval_workflow_manager
from app.runtime.learning.governance.promotion_pipeline import promotion_pipeline_manager
from app.runtime.learning.governance.rollback_manager import rollback_manager
from app.runtime.learning.governance.policy_guardrails import PolicyGuardrailsValidator
from app.runtime.learning.governance.risk_assessment import RiskAssessmentEngine

router = APIRouter()


# ---------------------------------------------------------------------------
# Request Schemas
# ---------------------------------------------------------------------------

class MineLearningRequest(BaseModel):
    mission_id: str = Field(default="mission-001", description="Mission ID to reflect and learn from")


class IngestKnowledgeRequest(BaseModel):
    title: str
    category: str = Field(default="EXECUTION_RULE")
    source_mission_id: str = Field(default="mission-001")
    confidence_score: float = Field(default=0.90, ge=0.0, le=1.0)
    validation_status: str = Field(default="VERIFIED")
    content: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)


class ProposePolicyRequest(BaseModel):
    target_component: str = Field(default="planner")
    policy_name: str = Field(default="Adaptive DAG Optimization Policy")
    parameters: Dict[str, Any] = Field(default_factory=lambda: {
        "max_retries": 3,
        "concurrency_limit": 6,
        "timeout_seconds": 45,
        "confidence_threshold": 0.85,
        "replanning_sensitivity": 0.35,
    })
    evidence_lessons: List[str] = Field(default_factory=lambda: ["lesson-001", "lesson-002"])


class EvaluatePolicyRequest(BaseModel):
    candidate_id: str


class GovernanceReviewActionRequest(BaseModel):
    candidate_id: str
    reviewer_id: str = Field(default="gov-admin-01")
    decision: str = Field(default="APPROVED", description="APPROVED | REJECTED")
    comments: str = Field(default="Automated evaluation criteria met.")


class PromotePolicyRequest(BaseModel):
    candidate_id: str
    promoter_id: str = Field(default="system-deployer")


class RollbackPolicyRequest(BaseModel):
    policy_id: str
    operator_id: str = Field(default="system-operator")
    reason: str = Field(default="Manual operational rollback triggered.")


# ---------------------------------------------------------------------------
# Reflection Endpoints
# ---------------------------------------------------------------------------

@router.get("/reflection/mission/{mission_id}", response_model=Dict[str, Any])
async def get_mission_reflection(mission_id: str):
    """
    Generate or retrieve an end-to-end multi-dimensional reflection report for a mission.
    """
    report = reflection_engine.reflect_on_mission(mission_id)
    return report.model_dump()


@router.get("/reflection/history", response_model=List[Dict[str, Any]])
async def list_reflection_history():
    """
    List all generated historical reflection reports.
    """
    reports = reflection_engine.list_reports()
    return [r.model_dump() for r in reports]


# ---------------------------------------------------------------------------
# Learning & Pattern Mining Endpoints
# ---------------------------------------------------------------------------

@router.post("/learning/mine", response_model=Dict[str, Any])
async def run_learning_pipeline(req: MineLearningRequest):
    """
    Run full learning pipeline: reflects on mission, mines patterns, extracts rules, and compiles strategies.
    """
    reflection = reflection_engine.reflect_on_mission(req.mission_id)
    lesson = learning_engine.mine_lessons(reflection)
    return lesson.model_dump()


@router.get("/learning/lessons", response_model=List[Dict[str, Any]])
async def list_mined_lessons():
    """
    List all institutional mined lessons.
    """
    lessons = learning_engine.list_lessons()
    return [l.model_dump() for l in lessons]


@router.get("/learning/patterns", response_model=List[Dict[str, Any]])
async def list_mined_patterns():
    """
    List all mined execution patterns across missions.
    """
    lessons = learning_engine.list_lessons()
    patterns: List[Dict[str, Any]] = []
    for l in lessons:
        for p in l.mined_patterns:
            patterns.append(p.model_dump())
    return patterns


@router.get("/learning/strategies", response_model=List[Dict[str, Any]])
async def list_execution_strategies():
    """
    List all compiled execution strategies.
    """
    lessons = learning_engine.list_lessons()
    strategies: List[Dict[str, Any]] = []
    for l in lessons:
        if l.compiled_strategy:
            strategies.append(l.compiled_strategy.model_dump())
    return strategies


# ---------------------------------------------------------------------------
# Knowledge Registry & Graph Endpoints
# ---------------------------------------------------------------------------

@router.get("/knowledge/records", response_model=List[Dict[str, Any]])
async def list_knowledge_records(category: Optional[str] = Query(None)):
    """
    List records in the knowledge registry with optional category filter.
    """
    records = knowledge_registry.list_records(category=category)
    return [r.model_dump() for r in records]


@router.post("/knowledge/records", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def create_knowledge_record(req: IngestKnowledgeRequest):
    """
    Register a verified knowledge record into the institutional registry and knowledge graph.
    """
    record = knowledge_registry.register_record(
        title=req.title,
        category=req.category,
        source_mission_id=req.source_mission_id,
        confidence_score=req.confidence_score,
        validation_status=req.validation_status,
        content=req.content,
        tags=req.tags,
    )
    # Sync with knowledge graph and lineage
    knowledge_graph.add_node(
        node_id=record.record_id,
        label=record.title,
        node_type=record.category,
        properties={"confidence": record.confidence_score, "version": record.version},
    )
    knowledge_lineage_tracker.record_origin(
        record_id=record.record_id,
        version=record.version,
        source_mission_id=record.source_mission_id,
        content_hash=record.content_hash,
    )
    return record.model_dump()


@router.get("/knowledge/graph", response_model=Dict[str, Any])
async def get_knowledge_graph():
    """
    Return full Knowledge Graph topology (nodes, edges, density, and connected components).
    """
    return knowledge_graph.to_dict()


@router.get("/knowledge/search", response_model=List[Dict[str, Any]])
async def search_knowledge(q: str = Query(..., min_length=1)):
    """
    Search indexed knowledge records using keyword and semantic matching.
    """
    matches = knowledge_search_engine.search(q)
    return [m.model_dump() for m in matches]


@router.get("/knowledge/lineage/{record_id}", response_model=Dict[str, Any])
async def get_knowledge_lineage(record_id: str):
    """
    Retrieve cryptographic provenance and SHA-256 lineage verification for a knowledge record.
    """
    chain = knowledge_lineage_tracker.get_chain(record_id)
    is_valid = knowledge_lineage_tracker.verify_chain_integrity(record_id)
    return {
        "record_id": record_id,
        "is_tamper_evident": is_valid,
        "chain_length": len(chain),
        "lineage_records": [c.model_dump() for c in chain],
    }


# ---------------------------------------------------------------------------
# Policy Evolution Endpoints
# ---------------------------------------------------------------------------

@router.get("/policy/candidates", response_model=List[Dict[str, Any]])
async def list_candidate_policies():
    """
    List all synthesized candidate policy adjustments awaiting evaluation/governance.
    """
    candidates = policy_engine.list_candidates()
    return [c.model_dump() for c in candidates]


@router.post("/policy/propose", response_model=Dict[str, Any])
async def propose_candidate_policy(req: ProposePolicyRequest):
    """
    Synthesize and propose a candidate policy adjustment based on mined lessons.
    """
    candidate = policy_engine.propose_candidate(
        target_component=req.target_component,
        policy_name=req.policy_name,
        parameters=req.parameters,
        evidence_lessons=req.evidence_lessons,
    )
    return candidate.model_dump()


@router.post("/policy/evaluate", response_model=Dict[str, Any])
async def evaluate_candidate_policy(req: EvaluatePolicyRequest):
    """
    Execute counterfactual simulation and differential comparison for a candidate policy.
    """
    evaluation = policy_engine.evaluate_candidate(req.candidate_id)
    return evaluation.model_dump()


@router.get("/policy/active", response_model=List[Dict[str, Any]])
async def list_active_policies():
    """
    List currently active production policies.
    """
    policies = evolution_policy_registry.list_active_policies()
    return [p.model_dump() for p in policies]


@router.get("/policy/versions", response_model=List[Dict[str, Any]])
async def list_policy_versions():
    """
    List policy evolution branch history and version trees.
    """
    versions = evolution_policy_registry.list_all_versions()
    return [v.model_dump() for v in versions]


# ---------------------------------------------------------------------------
# Governance & Safety Gatekeeper Endpoints
# ---------------------------------------------------------------------------

@router.get("/governance/evaluations", response_model=List[Dict[str, Any]])
async def list_governance_evaluations():
    """
    List all automated governance gatekeeper decisions and safety evaluations.
    """
    evals = learning_governance_gatekeeper.list_evaluations()
    return [e.model_dump() for e in evals]


@router.get("/governance/reviews", response_model=List[Dict[str, Any]])
async def list_approval_reviews():
    """
    List multi-stage approval reviews for candidate policies.
    """
    reviews = approval_workflow_manager.list_reviews()
    return [r.model_dump() for r in reviews]


@router.post("/governance/review", response_model=Dict[str, Any])
async def submit_governance_review(req: GovernanceReviewActionRequest):
    """
    Submit a human or automated approval/rejection decision on a candidate policy.
    """
    review = approval_workflow_manager.record_review(
        candidate_id=req.candidate_id,
        reviewer_id=req.reviewer_id,
        decision=req.decision,
        comments=req.comments,
    )
    return review.model_dump()


@router.post("/governance/promote", response_model=Dict[str, Any])
async def promote_candidate_to_active(req: PromotePolicyRequest):
    """
    Promote an approved candidate policy to active production execution.
    """
    res = promotion_pipeline_manager.promote(
        candidate_id=req.candidate_id,
        promoter_id=req.promoter_id,
    )
    return res.model_dump()


@router.post("/governance/rollback", response_model=Dict[str, Any])
async def rollback_active_policy(req: RollbackPolicyRequest):
    """
    Execute 1-click atomic rollback of an active policy back to baseline.
    """
    res = rollback_manager.rollback(
        policy_id=req.policy_id,
        operator_id=req.operator_id,
        reason=req.reason,
    )
    return res.model_dump()


@router.get("/governance/guardrails", response_model=Dict[str, Any])
async def get_guardrail_bounds():
    """
    Return active safety guardrail boundaries and thresholds.
    """
    return PolicyGuardrailsValidator.get_guardrail_spec()


# ---------------------------------------------------------------------------
# Analytics & KPI Overview Endpoints
# ---------------------------------------------------------------------------

@router.get("/analytics/summary", response_model=Dict[str, Any])
async def get_learning_analytics_summary():
    """
    Return platform-wide learning, reflection, knowledge growth, and policy evolution KPIs.
    """
    lessons = learning_engine.list_lessons()
    records = knowledge_registry.list_records()
    active_policies = evolution_policy_registry.list_active_policies()
    candidates = policy_engine.list_candidates()
    evals = learning_governance_gatekeeper.list_evaluations()

    avg_lesson_confidence = (
        sum(l.confidence_score for l in lessons) / len(lessons) if lessons else 0.88
    )
    
    return {
        "total_reflections": len(reflection_engine.list_reports()),
        "total_mined_lessons": len(lessons),
        "total_knowledge_records": len(records),
        "total_candidate_policies": len(candidates),
        "total_active_policies": len(active_policies),
        "governance_approval_rate": (
            sum(1 for e in evals if e.decision == "APPROVED") / len(evals) if evals else 1.0
        ),
        "avg_confidence_score": round(avg_lesson_confidence, 3),
        "risk_level": "LOW",
        "knowledge_graph_density": round(knowledge_graph.get_density(), 4),
        "active_guardrail_enforcements": 0,
    }


# ---------------------------------------------------------------------------
# Direct Route Aliases from Prompt Specification
# ---------------------------------------------------------------------------


@router.get("/reflections", response_model=List[Dict[str, Any]])
async def get_all_reflections():
    return [r.model_dump() for r in reflection_engine.list_reports()]


@router.get("/patterns", response_model=List[Dict[str, Any]])
async def get_all_patterns():
    return await list_mined_patterns()


@router.get("/knowledge", response_model=List[Dict[str, Any]])
async def get_all_knowledge():
    return [r.model_dump() for r in knowledge_registry.list_records()]


@router.get("/policies", response_model=List[Dict[str, Any]])
async def get_all_policies():
    return [c.model_dump() for c in policy_engine.list_candidates()]


@router.get("/strategies", response_model=List[Dict[str, Any]])
async def get_all_strategies():
    return await list_execution_strategies()


@router.get("/governance", response_model=List[Dict[str, Any]])
async def get_governance_overview():
    return [e.model_dump() for e in learning_governance_gatekeeper.list_evaluations()]


@router.get("/history", response_model=List[Dict[str, Any]])
async def get_learning_history():
    return [r.model_dump() for r in reflection_engine.list_reports()]


@router.get("/lineage", response_model=List[Dict[str, Any]])
async def get_all_lineage():
    records = knowledge_registry.list_records()
    all_chains = []
    for r in records:
        chain = knowledge_lineage_tracker.get_chain(r.record_id)
        all_chains.extend([c.model_dump() for c in chain])
    return all_chains


@router.get("/graph", response_model=Dict[str, Any])
async def get_graph():
    return knowledge_graph.to_dict()


@router.get("/recommendations", response_model=List[Dict[str, Any]])
async def get_all_recommendations():
    reports = reflection_engine.list_reports()
    recs = []
    for rep in reports:
        for r in rep.recommendations:
            recs.append({
                "mission_id": rep.mission_id,
                "recommendation": r,
                "confidence": rep.confidence_metrics.avg_confidence,
                "status": "PROPOSED",
            })
    return recs


@router.post("/review", response_model=Dict[str, Any])
async def review_policy(req: GovernanceReviewActionRequest):
    return await submit_governance_review(req)


@router.post("/approve", response_model=Dict[str, Any])
async def approve_policy(req: PromotePolicyRequest):
    return await promote_candidate_to_active(req)


@router.post("/reject", response_model=Dict[str, Any])
async def reject_policy(req: GovernanceReviewActionRequest):
    req.decision = "REJECTED"
    return await submit_governance_review(req)


@router.post("/rollback", response_model=Dict[str, Any])
async def rollback_policy(req: RollbackPolicyRequest):
    return await rollback_active_policy(req)

