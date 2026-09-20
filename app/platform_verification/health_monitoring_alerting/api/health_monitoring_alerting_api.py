"""FastAPI router for Enterprise Health Monitoring, Alerting & Incident Signal Verification.

Exposes REST endpoints for health signal architecture, metrics, Prometheus scraping,
Grafana dashboards, alert rules, accuracy, incidents, fatigue prevention, chaos simulations,
security audits, scorecard, and full execution.
"""

from fastapi import APIRouter
from typing import Dict, Any
import json

from app.platform_verification.health_monitoring_alerting.runtime.health_monitoring_alerting_runtime import (
    HealthMonitoringAlertingRuntime,
)
from app.platform_verification.health_monitoring_alerting.exporter.health_monitoring_evidence_exporter import (
    EnhancedJSONEncoder,
)

router = APIRouter(prefix="/health/monitoring", tags=["Health Monitoring & Alerting"])
_runtime = HealthMonitoringAlertingRuntime()


def _to_dict(obj: Any) -> Any:
    return json.loads(json.dumps(obj, cls=EnhancedJSONEncoder))


@router.get("/signals", summary="Get 12-Signal Health Architecture")
def get_signals() -> Dict[str, Any]:
    return _to_dict(_runtime.signal_verifier.verify_signal_architecture())


@router.get("/metrics", summary="Get 19 Operational Metrics across 5 Domains")
def get_metrics() -> Dict[str, Any]:
    return _to_dict(_runtime.metrics_verifier.verify_metrics_collection())


@router.get("/prometheus", summary="Get Prometheus /metrics Scrape & OpenTelemetry Bridge Report")
def get_prometheus() -> Dict[str, Any]:
    return _to_dict(_runtime.prometheus_verifier.verify_prometheus_scraping())


@router.get("/dashboards", summary="Get 4 Enterprise Grafana Dashboards")
def get_dashboards() -> Dict[str, Any]:
    return _to_dict(_runtime.dashboard_verifier.verify_dashboards())


@router.get("/alerts", summary="Get AlertManager Rules (Critical & Warning)")
def get_alerts() -> Dict[str, Any]:
    return _to_dict(_runtime.alert_verifier.verify_alert_rules())


@router.get("/accuracy", summary="Get Alert Precision, Recall, and Auto-Resolution Metrics")
def get_accuracy() -> Dict[str, Any]:
    return _to_dict(_runtime.accuracy_verifier.verify_alert_accuracy())


@router.get("/incidents", summary="Get Actionable Incident Signals & Diagnostic Payloads")
def get_incidents() -> Dict[str, Any]:
    return _to_dict(_runtime.incident_verifier.verify_incident_signals())


@router.get("/fatigue", summary="Get Alert Fatigue Prevention & Deduplication Report")
def get_fatigue() -> Dict[str, Any]:
    return _to_dict(_runtime.fatigue_verifier.verify_fatigue_prevention())


@router.get("/simulation", summary="Get Chaos & Failure Injection Monitoring Results")
def get_simulation() -> Dict[str, Any]:
    return _to_dict(_runtime.simulation_verifier.run_monitoring_failure_tests())


@router.get("/security", summary="Get Telemetry Security & PII/Secret Leak Audit")
def get_security() -> Dict[str, Any]:
    return _to_dict(_runtime.security_auditor.audit_security())


@router.get("/scorecard", summary="Get Operational Readiness Scorecard")
def get_scorecard() -> Dict[str, Any]:
    res = _runtime.run_full_verification()
    return _to_dict(res["scorecard"])


@router.post("/verify", summary="Run Full Health Monitoring & Alerting Verification Engine")
def execute_full_verification() -> Dict[str, Any]:
    res = _runtime.run_full_verification()
    return _to_dict(res)
