"""
FastAPI Router for Phase 3I.3 Enterprise Metrics Infrastructure Verification
"""
from fastapi import APIRouter
from typing import Dict, Any
from ..runtime.metrics_verification_runtime import MetricsVerificationRuntime

router = APIRouter(prefix="/api/v1/metrics-verification", tags=["Metrics Verification"])
runtime = MetricsVerificationRuntime()


@router.post("/verify")
def run_verification() -> Dict[str, Any]:
    """Execute complete enterprise metrics verification suite and export signed manifests."""
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
    """Retrieve 6-pillar metrics scorecard and certification status."""
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
    """Retrieve metrics collection architecture report."""
    report = runtime.arch_verifier.verify_metrics_architecture()
    return report.model_dump(mode="json")


@router.get("/standards")
def get_standards() -> Dict[str, Any]:
    """Retrieve Prometheus naming and metric type standards validation report."""
    report = runtime.std_verifier.verify_metrics_standard()
    return report.model_dump(mode="json")


@router.get("/application")
def get_application() -> Dict[str, Any]:
    """Retrieve HTTP request latency, RPS, and error metrics report."""
    report = runtime.app_verifier.verify_application_metrics()
    return report.model_dump(mode="json")


@router.get("/ai-agent")
def get_ai_agent() -> Dict[str, Any]:
    """Retrieve AI agent lifecycle and LLM token/cost efficiency report."""
    report = runtime.ai_verifier.verify_ai_metrics()
    return report.model_dump(mode="json")


@router.get("/infrastructure")
def get_infrastructure() -> Dict[str, Any]:
    """Retrieve Queue, Worker, Database, and Container resource report."""
    report = runtime.infra_verifier.verify_infrastructure_metrics()
    return report.model_dump(mode="json")


@router.get("/business-sla")
def get_business_sla() -> Dict[str, Any]:
    """Retrieve business document extraction accuracy and SLA report."""
    report = runtime.biz_verifier.verify_business_sla_metrics()
    return report.model_dump(mode="json")


@router.get("/dashboards")
def get_dashboards() -> Dict[str, Any]:
    """Retrieve Grafana operational dashboards report."""
    report = runtime.dash_verifier.verify_dashboards()
    return report.model_dump(mode="json")


@router.get("/alerts")
def get_alerts() -> Dict[str, Any]:
    """Retrieve metric-driven alert rules and thresholds report."""
    report = runtime.alert_verifier.verify_alert_metrics()
    return report.model_dump(mode="json")


@router.get("/accuracy")
def get_accuracy() -> Dict[str, Any]:
    """Retrieve metric ingestion accuracy and counter drift report."""
    report = runtime.acc_verifier.verify_metrics_accuracy()
    return report.model_dump(mode="json")


@router.get("/security")
def get_security() -> Dict[str, Any]:
    """Retrieve metric label security and PII sanitization report."""
    report = runtime.sec_verifier.verify_metrics_security()
    return report.model_dump(mode="json")


@router.get("/performance")
def get_performance() -> Dict[str, Any]:
    """Retrieve metric collection overhead and performance report."""
    report = runtime.perf_verifier.verify_metrics_performance()
    return report.model_dump(mode="json")


@router.get("/chaos")
def get_chaos() -> Dict[str, Any]:
    """Retrieve chaos failure simulation metrics report."""
    report = runtime.chaos_verifier.verify_failure_simulation_metrics()
    return report.model_dump(mode="json")


@router.get("/health")
def get_health() -> Dict[str, Any]:
    """Health check endpoint for Metrics Verification API."""
    return {
        "status": "HEALTHY",
        "subsystem": "metrics_infrastructure",
        "engine": "DocuTask Enterprise Metrics Engine",
        "phase": "3I.3"
    }
