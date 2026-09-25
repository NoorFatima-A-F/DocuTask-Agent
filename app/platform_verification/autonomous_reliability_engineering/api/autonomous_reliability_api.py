"""
Phase 3I.12: Autonomous Reliability Engineering REST API Router
Provides endpoints for failure predictions, optimization recommendations, knowledge graph queries, and certification.
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.platform_verification.autonomous_reliability_engineering.runtime.autonomous_reliability_runtime import (
    AutonomousReliabilityRuntime,
)

router = APIRouter(
    prefix="/api/v1/autonomous-reliability",
    tags=["Autonomous Reliability Engineering & Continuous Optimization"],
)

_runtime_instance = AutonomousReliabilityRuntime()


@router.get("/status")
def get_platform_status() -> Dict[str, Any]:
    """Returns the operational status of the Autonomous Reliability Engineering framework."""
    return {
        "status": "ONLINE",
        "phase": "Phase 3I.12 — Autonomous Reliability Engineering & Continuous Optimization",
        "project": "DocuTask-Agent",
        "capability": "Self-Optimizing Autonomous Reliability Platform",
        "loop_status": "ACTIVE_CONTINUOUS_IMPROVEMENT",
    }


@router.post("/run-verification")
def run_full_autonomous_verification() -> Dict[str, Any]:
    """Executes full verification across all 11 modules, evaluates 7-category certification, and exports manifests."""
    try:
        pipeline_result = _runtime_instance.run_pipeline()
        cert_report = pipeline_result["certification_report"]
        return {
            "status": "SUCCESS",
            "certification_granted": pipeline_result["success"],
            "composite_reliability_score_pct": cert_report.composite_reliability_score_pct,
            "certification_tier": cert_report.certification_tier.value,
            "exported_files_count": len(pipeline_result["exported_files"]),
            "exported_files": pipeline_result["exported_files"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Autonomous verification pipeline failed: {str(e)}")


@router.get("/predictions")
def get_failure_predictions() -> Dict[str, Any]:
    """Returns real-time predictive failure assessments and mitigation actions."""
    report = _runtime_instance.prediction_verifier.verify()
    return report.model_dump()


@router.get("/optimizations")
def get_optimization_recommendations() -> Dict[str, Any]:
    """Returns discovered performance, cost, and architecture optimization recommendations."""
    report = _runtime_instance.optimization_verifier.verify()
    return report.model_dump()


@router.get("/self-optimization")
def get_self_optimization_status() -> Dict[str, Any]:
    """Returns closed-loop self-optimization actions and before/after performance deltas."""
    report = _runtime_instance.self_opt_verifier.verify()
    return report.model_dump()


@router.get("/knowledge-graph")
def get_knowledge_graph() -> Dict[str, Any]:
    """Returns the operational reliability knowledge graph containing Failure->Cause->Component->Solution nodes and edges."""
    report = _runtime_instance.knowledge_graph_verifier.verify()
    return report.model_dump()


@router.get("/certification")
def get_autonomous_certification() -> Dict[str, Any]:
    """Computes and returns the 7-category autonomous reliability certification scorecard."""
    verification_results = _runtime_instance.execute_all_verifications()
    cert_report = _runtime_instance.scorer.compute_certification(verification_results)
    return cert_report.model_dump()
