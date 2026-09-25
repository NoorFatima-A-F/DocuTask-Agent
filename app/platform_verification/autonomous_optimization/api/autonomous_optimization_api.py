"""
Phase 3H.10: FastAPI Router for Autonomous Operational Intelligence & Self-Optimization
"""
from fastapi import APIRouter
from typing import Dict, Any
from ..runtime.autonomous_optimization_runtime import AutonomousOptimizationRuntime

router = APIRouter(prefix="/api/v1/autonomous-optimization", tags=["Autonomous Optimization Verification"])
runtime = AutonomousOptimizationRuntime()


@router.post("/verify")
def run_verification() -> Dict[str, Any]:
    """Execute full autonomous optimization verification suite and export evidence artifacts."""
    results = runtime.run_full_verification()
    return {
        "status": "COMPLETED",
        "overall_score_pct": results["certification_report"].overall_score_pct,
        "certification_tier": results["certification_report"].certification_tier.value,
        "certification_granted": results["certification_report"].certification_granted,
        "total_artifacts_exported": results["metadata"]["total_artifacts"],
    }


@router.get("/scorecard")
def get_scorecard() -> Dict[str, Any]:
    """Retrieve 7-pillar scorecard and certification status."""
    results = runtime.run_full_verification()
    cert = results["certification_report"]
    return {
        "report_title": cert.report_title,
        "evaluated_at": cert.evaluated_at,
        "overall_score_pct": cert.overall_score_pct,
        "certification_tier": cert.certification_tier.value,
        "certification_granted": cert.certification_granted,
        "pillar_scores": [p.model_dump(mode="json") for p in cert.pillar_scores],
    }


@router.get("/graph")
def get_operational_graph() -> Dict[str, Any]:
    """Retrieve the operational knowledge graph topology."""
    report = runtime.graph_verifier.verify_operational_graph()
    return report.model_dump(mode="json")


@router.get("/correlations")
def get_correlations() -> Dict[str, Any]:
    """Retrieve cross-signal narrative correlations."""
    report = runtime.correlation_verifier.verify_signal_correlation()
    return report.model_dump(mode="json")


@router.get("/predictions")
def get_predictions() -> Dict[str, Any]:
    """Retrieve predictive reliability and breach forecasts."""
    report = runtime.predictive_verifier.verify_predictive_reliability()
    return report.model_dump(mode="json")


@router.get("/recommendations")
def get_recommendations() -> Dict[str, Any]:
    """Retrieve autonomous self-optimization recommendations."""
    report = runtime.recommendations_verifier.verify_optimization_recommendations()
    return report.model_dump(mode="json")


@router.get("/safety")
def get_execution_safety() -> Dict[str, Any]:
    """Retrieve autonomous execution safety and blast-radius validations."""
    report = runtime.execution_verifier.verify_autonomous_execution()
    return report.model_dump(mode="json")


@router.get("/governance")
def get_governance() -> Dict[str, Any]:
    """Retrieve governance compliance and immutable audit logs."""
    report = runtime.governance_verifier.verify_governance()
    return report.model_dump(mode="json")


@router.get("/health")
def get_health() -> Dict[str, Any]:
    """Health check endpoint for Autonomous Optimization API."""
    return {
        "status": "HEALTHY",
        "subsystem": "autonomous_optimization",
        "engine": "DocuTask Autonomous Reliability Engine",
        "phase": "3H.10"
    }
