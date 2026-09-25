"""
Phase 3H.12: FastAPI Router for Enterprise Automated Recovery & Self-Healing Verification
"""
from fastapi import APIRouter
from typing import Dict, Any
from ..runtime.automated_recovery_runtime import AutomatedRecoveryRuntime

router = APIRouter(prefix="/api/v1/automated-recovery", tags=["Automated Recovery Verification"])
runtime = AutomatedRecoveryRuntime()


@router.post("/verify")
def run_verification() -> Dict[str, Any]:
    """Execute complete automated recovery verification suite and export signed manifests."""
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
    """Retrieve 6-pillar recovery scorecard and certification status."""
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


@router.get("/policies")
def get_policies() -> Dict[str, Any]:
    """Retrieve automated recovery decision policies."""
    report = runtime.policy_verifier.verify_recovery_policies()
    return report.model_dump(mode="json")


@router.get("/circuit-breaker")
def get_circuit_breaker() -> Dict[str, Any]:
    """Retrieve circuit breaker status and transition logs."""
    report = runtime.circuit_verifier.verify_circuit_breaker()
    return report.model_dump(mode="json")


@router.get("/validation")
def get_recovery_validation() -> Dict[str, Any]:
    """Retrieve synthetic document processing validation flow report."""
    report = runtime.validation_verifier.verify_validation_engine()
    return report.model_dump(mode="json")


@router.get("/metrics")
def get_reliability_metrics() -> Dict[str, Any]:
    """Retrieve MTTD, MTTR, and MTBF metrics."""
    report = runtime.metrics_verifier.verify_reliability_metrics()
    return report.model_dump(mode="json")


@router.get("/safety")
def get_safety_controls() -> Dict[str, Any]:
    """Retrieve recovery safety and restart throttle limits."""
    report = runtime.safety_verifier.verify_recovery_safety()
    return report.model_dump(mode="json")


@router.get("/audit")
def get_audit_trail() -> Dict[str, Any]:
    """Retrieve immutable recovery audit history."""
    report = runtime.audit_verifier.verify_recovery_audit()
    return report.model_dump(mode="json")


@router.get("/health")
def get_health() -> Dict[str, Any]:
    """Health check endpoint for Automated Recovery API."""
    return {
        "status": "HEALTHY",
        "subsystem": "automated_recovery_verification",
        "engine": "DocuTask Self-Healing Engine",
        "phase": "3H.12"
    }
