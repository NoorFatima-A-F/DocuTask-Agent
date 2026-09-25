"""
FastAPI Router for Phase 3I.2 Enterprise Logging Infrastructure Verification
"""
from fastapi import APIRouter
from typing import Dict, Any
from ..runtime.logging_verification_runtime import LoggingVerificationRuntime

router = APIRouter(prefix="/api/v1/logging-verification", tags=["Logging Verification"])
runtime = LoggingVerificationRuntime()


@router.post("/verify")
def run_verification() -> Dict[str, Any]:
    """Execute complete enterprise logging verification suite and export signed manifests."""
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
    """Retrieve 6-pillar logging scorecard and certification status."""
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


@router.get("/architecture")
def get_architecture() -> Dict[str, Any]:
    """Retrieve logging architecture and service coverage report."""
    report = runtime.arch_verifier.verify_logging_architecture()
    return report.model_dump(mode="json")


@router.get("/correlation")
def get_correlation() -> Dict[str, Any]:
    """Retrieve distributed request correlation report."""
    report = runtime.corr_verifier.verify_correlation()
    return report.model_dump(mode="json")


@router.get("/agent-execution")
def get_agent_execution() -> Dict[str, Any]:
    """Retrieve AI agent lifecycle and error diagnostic logging report."""
    report = runtime.agent_verifier.verify_agent_execution_logging()
    return report.model_dump(mode="json")


@router.get("/security")
def get_security() -> Dict[str, Any]:
    """Retrieve logging security and PII masking report."""
    report = runtime.sec_verifier.verify_security()
    return report.model_dump(mode="json")


@router.get("/performance")
def get_performance() -> Dict[str, Any]:
    """Retrieve logging overhead and retention report."""
    report = runtime.perf_verifier.verify_performance()
    return report.model_dump(mode="json")


@router.get("/failures")
def get_failures() -> Dict[str, Any]:
    """Retrieve failure simulation chaos logging report."""
    report = runtime.failure_verifier.verify_failure_simulation_logging()
    return report.model_dump(mode="json")


@router.get("/health")
def get_health() -> Dict[str, Any]:
    """Health check endpoint for Logging Verification API."""
    return {
        "status": "HEALTHY",
        "subsystem": "logging_infrastructure",
        "engine": "DocuTask Enterprise Logging Engine",
        "phase": "3I.2"
    }
