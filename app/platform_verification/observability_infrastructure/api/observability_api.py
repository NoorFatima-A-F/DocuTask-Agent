"""
FastAPI Router for Part 3I: Enterprise Observability Infrastructure (Logging & Metrics)
"""
from fastapi import APIRouter
from typing import Dict, Any
from ..runtime.observability_runtime import ObservabilityRuntime

router = APIRouter(prefix="/api/v1/observability", tags=["Observability Infrastructure Verification"])
runtime = ObservabilityRuntime()


@router.post("/verify")
def run_full_verification() -> Dict[str, Any]:
    """Execute complete logging & metrics verification pipelines and export signed manifests."""
    results = runtime.run_full_verification()
    return {
        "status": "COMPLETED",
        "logging_score_pct": results["unified_certification"].logging_score_pct,
        "metrics_score_pct": results["unified_certification"].metrics_score_pct,
        "overall_score_pct": results["unified_certification"].overall_score_pct,
        "certification_tier": results["unified_certification"].certification_tier.value,
        "certification_granted": results["unified_certification"].certification_granted,
        "total_artifacts_exported": results["metadata"]["logging_artifacts"] + results["metadata"]["metrics_artifacts"] + 1,
    }


@router.get("/scorecard")
def get_scorecard() -> Dict[str, Any]:
    """Retrieve dual logging and metrics scorecards with unified certification."""
    results = runtime.run_full_verification()
    log_cert = results["logging"]["certification"]
    met_cert = results["metrics"]["certification"]
    uni_cert = results["unified_certification"]

    return {
        "unified_certification": uni_cert.model_dump(mode="json"),
        "logging_scorecard": log_cert.model_dump(mode="json"),
        "metrics_scorecard": met_cert.model_dump(mode="json"),
    }


@router.get("/logging/correlation")
def get_logging_correlation() -> Dict[str, Any]:
    """Retrieve 10-hop request lifecycle correlation report."""
    report = runtime.log_corr.verify_correlation()
    return report.model_dump(mode="json")


@router.get("/logging/security")
def get_security_scan() -> Dict[str, Any]:
    """Retrieve security and PII masking verification report."""
    report = runtime.log_sec.verify_security_scanning()
    return report.model_dump(mode="json")


@router.get("/metrics/golden-signals")
def get_golden_signals() -> Dict[str, Any]:
    """Retrieve four golden signals tracking status."""
    report = runtime.met_golden.verify_golden_signals()
    return report.model_dump(mode="json")


@router.get("/metrics/sli-slo")
def get_sli_slo() -> Dict[str, Any]:
    """Retrieve SLI / SLO compliance report."""
    report = runtime.met_sli.verify_sli_slo()
    return report.model_dump(mode="json")


@router.get("/metrics/dashboards")
def get_dashboards() -> Dict[str, Any]:
    """Retrieve Grafana dashboard specs and panel coverage."""
    report = runtime.met_dash.verify_dashboards()
    return report.model_dump(mode="json")


@router.get("/health")
def get_health() -> Dict[str, Any]:
    """Health check endpoint for Observability Infrastructure API."""
    return {
        "status": "HEALTHY",
        "subsystem": "observability_infrastructure",
        "tracks": ["3I.1 Logging", "3I.2 Metrics"],
        "engine": "DocuTask Observability Verification Engine",
        "phase": "3I"
    }
