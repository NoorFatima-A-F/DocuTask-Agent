"""
FastAPI Router for Phase 3I.5 Enterprise Alerting & Incident Detection Verification
"""
from fastapi import APIRouter
from typing import Dict, Any
from ..runtime.alerting_verification_runtime import AlertingVerificationRuntime

router = APIRouter(prefix="/api/v1/alerting-verification", tags=["Alerting Verification"])
runtime = AlertingVerificationRuntime()


@router.post("/verify")
def run_verification() -> Dict[str, Any]:
    """Execute complete enterprise alerting verification suite and export signed manifests."""
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
    """Retrieve 6-pillar alerting scorecard and certification status."""
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
    """Retrieve alerting architecture and notification dispatch channels report."""
    report = runtime.arch_verifier.verify_alerting_architecture()
    return report.model_dump(mode="json")


@router.get("/signals")
def get_signals() -> Dict[str, Any]:
    """Retrieve multi-source signal coverage report."""
    report = runtime.signal_verifier.verify_signal_coverage()
    return report.model_dump(mode="json")


@router.get("/rules")
def get_rules() -> Dict[str, Any]:
    """Retrieve SRE Golden Signals and alert rules report."""
    report = runtime.rule_verifier.verify_alert_rules()
    return report.model_dump(mode="json")


@router.get("/ai-agent")
def get_ai_agent() -> Dict[str, Any]:
    """Retrieve AI agent failure, retry, and accuracy degradation alerts report."""
    report = runtime.ai_verifier.verify_ai_agent_alerts()
    return report.model_dump(mode="json")


@router.get("/routing")
def get_routing() -> Dict[str, Any]:
    """Retrieve incident severity classification and team routing report."""
    report = runtime.routing_verifier.verify_severity_routing()
    return report.model_dump(mode="json")


@router.get("/remediation")
def get_remediation() -> Dict[str, Any]:
    """Retrieve automated self-healing remediation and ticket workflow report."""
    report = runtime.remediation_verifier.verify_remediation_workflows()
    return report.model_dump(mode="json")


@router.get("/security")
def get_security() -> Dict[str, Any]:
    """Retrieve alert security and notification sanitization report."""
    report = runtime.sec_verifier.verify_alert_security()
    return report.model_dump(mode="json")


@router.get("/testing")
def get_testing() -> Dict[str, Any]:
    """Retrieve alert chaos testing and failure simulation report."""
    report = runtime.testing_verifier.verify_alert_testing_scenarios()
    return report.model_dump(mode="json")


@router.get("/health")
def get_health() -> Dict[str, Any]:
    """Health check endpoint for Alerting Verification API."""
    return {
        "status": "HEALTHY",
        "subsystem": "alerting_infrastructure",
        "engine": "DocuTask Enterprise Incident Engine",
        "phase": "3I.5"
    }
