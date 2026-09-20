"""
FastAPI Router for Phase 3I.4 Enterprise Distributed Tracing Infrastructure Verification
"""
from fastapi import APIRouter
from typing import Dict, Any
from ..runtime.tracing_verification_runtime import TracingVerificationRuntime

router = APIRouter(prefix="/api/v1/tracing-verification", tags=["Tracing Verification"])
runtime = TracingVerificationRuntime()


@router.post("/verify")
def run_verification() -> Dict[str, Any]:
    """Execute complete enterprise distributed tracing verification suite and export signed manifests."""
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
    """Retrieve 6-pillar distributed tracing scorecard and certification status."""
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
    """Retrieve tracing architecture report."""
    report = runtime.arch_verifier.verify_tracing_architecture()
    return report.model_dump(mode="json")


@router.get("/propagation")
def get_propagation() -> Dict[str, Any]:
    """Retrieve W3C trace context propagation report."""
    report = runtime.prop_verifier.verify_context_propagation()
    return report.model_dump(mode="json")


@router.get("/workflow")
def get_workflow() -> Dict[str, Any]:
    """Retrieve end-to-end document workflow trace report."""
    report = runtime.wf_verifier.verify_workflow_trace()
    return report.model_dump(mode="json")


@router.get("/ai-agent")
def get_ai_agent() -> Dict[str, Any]:
    """Retrieve autonomous AI agent lifecycle trace report."""
    report = runtime.agent_verifier.verify_agent_trace()
    return report.model_dump(mode="json")


@router.get("/dependencies")
def get_dependencies() -> Dict[str, Any]:
    """Retrieve external dependency latency trace report."""
    report = runtime.dep_verifier.verify_dependency_trace()
    return report.model_dump(mode="json")


@router.get("/errors")
def get_errors() -> Dict[str, Any]:
    """Retrieve error diagnostic and failure span report."""
    report = runtime.err_verifier.verify_error_trace()
    return report.model_dump(mode="json")


@router.get("/correlation")
def get_correlation() -> Dict[str, Any]:
    """Retrieve trace, log, and metric bidirectional correlation report."""
    report = runtime.corr_verifier.verify_correlation()
    return report.model_dump(mode="json")


@router.get("/sampling")
def get_sampling() -> Dict[str, Any]:
    """Retrieve adaptive sampling strategy report."""
    report = runtime.sample_verifier.verify_sampling_strategy()
    return report.model_dump(mode="json")


@router.get("/security")
def get_security() -> Dict[str, Any]:
    """Retrieve trace security and data sanitization report."""
    report = runtime.sec_verifier.verify_trace_security()
    return report.model_dump(mode="json")


@router.get("/performance")
def get_performance() -> Dict[str, Any]:
    """Retrieve tracing performance overhead report."""
    report = runtime.perf_verifier.verify_trace_performance()
    return report.model_dump(mode="json")


@router.get("/chaos")
def get_chaos() -> Dict[str, Any]:
    """Retrieve chaos failure simulation trace reaction report."""
    report = runtime.chaos_verifier.verify_failure_simulation_traces()
    return report.model_dump(mode="json")


@router.get("/health")
def get_health() -> Dict[str, Any]:
    """Health check endpoint for Tracing Verification API."""
    return {
        "status": "HEALTHY",
        "subsystem": "tracing_infrastructure",
        "engine": "DocuTask Enterprise Tracing Engine",
        "phase": "3I.4"
    }
