"""AI Health Monitoring API Endpoints.

FastAPI router exposing AI observability pipelines, metric collections, dashboards, and scorecards.
"""

from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
import json

from app.platform_verification.ai_health_monitoring.runtime.ai_health_monitoring_runtime import AIHealthMonitoringRuntime
from app.platform_verification.ai_health_monitoring.exporter.ai_monitoring_evidence_exporter import EnhancedJSONEncoder

router = APIRouter(prefix="/health/ai-monitoring", tags=["AI Health Monitoring"])
_runtime = AIHealthMonitoringRuntime()


def _to_dict(obj: Any) -> Any:
    return json.loads(json.dumps(obj, cls=EnhancedJSONEncoder))


@router.get("/architecture", summary="Get AI Observability Architecture & Pipelines")
def get_architecture() -> Dict[str, Any]:
    report = _runtime.arch_verifier.verify_architecture()
    return _to_dict(report)


@router.get("/metrics", summary="Get 5-Dimension AI Metrics Collection")
def get_metrics() -> Dict[str, Any]:
    report = _runtime.metrics_verifier.verify_metrics_collection()
    return _to_dict(report)


@router.get("/dashboards", summary="Get 4 Enterprise AI Grafana Dashboards")
def get_dashboards() -> Dict[str, Any]:
    report = _runtime.dashboard_verifier.verify_dashboards()
    return _to_dict(report)


@router.get("/logging", summary="Get Structured AI Logging Verification")
def get_logging() -> Dict[str, Any]:
    report = _runtime.logging_verifier.verify_logging()
    return _to_dict(report)


@router.get("/tracing", summary="Get AI Distributed Tracing & Bottleneck Analysis")
def get_tracing() -> Dict[str, Any]:
    report = _runtime.tracing_verifier.verify_tracing()
    return _to_dict(report)


@router.get("/alerting", summary="Get AlertManager AI Rules & Escalations")
def get_alerting() -> Dict[str, Any]:
    report = _runtime.alerting_verifier.verify_alerting()
    return _to_dict(report)


@router.get("/slos", summary="Get AI SLO Attainment & Compliance")
def get_slos() -> Dict[str, Any]:
    report = _runtime.slo_verifier.verify_slos()
    return _to_dict(report)


@router.get("/incidents", summary="Get AI Incident Simulation & Detection Results")
def get_incidents() -> Dict[str, Any]:
    report = _runtime.incident_verifier.verify_incident_detection()
    return _to_dict(report)


@router.get("/automation", summary="Get Automated Mitigation Responses")
def get_automation() -> Dict[str, Any]:
    report = _runtime.automation_verifier.verify_automated_response()
    return _to_dict(report)


@router.get("/security", summary="Get Observability Tier Security & RBAC Checks")
def get_security() -> Dict[str, Any]:
    report = _runtime.security_verifier.verify_security()
    return _to_dict(report)


@router.get("/scorecard", summary="Get Enterprise AI Observability Scorecard")
def get_scorecard() -> Dict[str, Any]:
    res = _runtime.run_full_verification()
    return _to_dict(res["scorecard"])


@router.post("/verify", summary="Execute Full AI Monitoring Verification & Export Manifests")
def execute_full_verification() -> Dict[str, Any]:
    res = _runtime.run_full_verification()
    return _to_dict(res)
