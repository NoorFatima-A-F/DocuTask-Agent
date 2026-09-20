"""Health Monitoring Integration API Endpoints.

FastAPI router exposing health monitoring verification endpoints and Prometheus /metrics scrape target.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, Optional

from fastapi import APIRouter, Response, status

from app.platform_verification.health_monitoring_integration.runtime.monitoring_integration_runtime import (
    MonitoringIntegrationRuntime,
)

router = APIRouter(prefix="/health/monitoring", tags=["Health Monitoring Integration"])

# Shared runtime instance
_runtime_instance: Optional[MonitoringIntegrationRuntime] = None


def get_runtime() -> MonitoringIntegrationRuntime:
    global _runtime_instance
    if _runtime_instance is None:
        _runtime_instance = MonitoringIntegrationRuntime()
    return _runtime_instance


@router.get("/summary", summary="Get Health Monitoring Verification Summary")
async def get_summary() -> Dict[str, Any]:
    """Returns the comprehensive observability scorecard and verification status."""
    runtime = get_runtime()
    results = runtime.run_full_verification()
    scorecard = results["scorecard"]
    return {
        "status": "success",
        "overall_score": scorecard.overall_score,
        "certification_tier": scorecard.certification_tier.value,
        "certification_verdict": scorecard.certification_verdict,
        "passed": scorecard.passed,
        "dimension_scores": {
            "metric_coverage": scorecard.metric_coverage_score,
            "alert_accuracy": scorecard.alert_accuracy_score,
            "dashboard_quality": scorecard.dashboard_quality_score,
            "trace_visibility": scorecard.trace_visibility_score,
            "incident_diagnosis": scorecard.incident_diagnosis_score,
            "security": scorecard.security_score,
        },
    }


@router.get("/architecture", summary="Get Observability Architecture Report")
async def get_architecture() -> Dict[str, Any]:
    """Returns the service instrumentation and telemetry routing report."""
    runtime = get_runtime()
    report = runtime.arch_verifier.verify_architecture()
    return {"status": "success", "data": asdict(report)}


@router.get("/metrics-inventory", summary="Get Health Metrics Catalog")
async def get_metrics_inventory() -> Dict[str, Any]:
    """Returns the inventory of cataloged platform health metrics."""
    runtime = get_runtime()
    report = runtime.metrics_collector.collect_inventory()
    return {"status": "success", "data": asdict(report)}


@router.get("/prometheus", summary="Get Prometheus Verification Report")
async def get_prometheus() -> Dict[str, Any]:
    """Returns scrape target health and PromQL query verification results."""
    runtime = get_runtime()
    report = runtime.prometheus_verifier.verify_prometheus()
    return {"status": "success", "data": asdict(report)}


@router.get("/grafana", summary="Get Grafana Dashboard Report")
async def get_grafana() -> Dict[str, Any]:
    """Returns status and panel configurations for the 4 operational dashboards."""
    runtime = get_runtime()
    report = runtime.dashboard_builder.verify_dashboards()
    return {"status": "success", "data": asdict(report)}


@router.get("/alerts", summary="Get AlertManager Rules & Quality Evaluation")
async def get_alerts() -> Dict[str, Any]:
    """Returns alert rules and false positive/noise evaluation metrics."""
    runtime = get_runtime()
    config_rep = runtime.alert_manager.get_alert_configuration()
    quality_rep = runtime.alert_evaluator.evaluate_quality()
    return {
        "status": "success",
        "configuration": asdict(config_rep),
        "quality_evaluation": asdict(quality_rep),
    }


@router.get("/incident-visibility", summary="Get Correlated Incident Visibility Report")
async def get_incident_visibility() -> Dict[str, Any]:
    """Returns unified Metrics + Logs + Traces + Events cross-correlation report."""
    runtime = get_runtime()
    report = runtime.incident_engine.verify_incident_visibility()
    return {"status": "success", "data": asdict(report)}


@router.get("/simulations", summary="Get Outage Simulation Results")
async def get_simulations() -> Dict[str, Any]:
    """Returns the 4 failure scenario simulation benchmark results."""
    runtime = get_runtime()
    report = runtime.simulation_runner.run_simulations()
    return {"status": "success", "data": asdict(report)}


@router.get("/tracing", summary="Get OpenTelemetry Tracing Verification Report")
async def get_tracing() -> Dict[str, Any]:
    """Returns end-to-end distributed trace propagation verification results."""
    runtime = get_runtime()
    report = runtime.trace_verifier.verify_tracing()
    return {"status": "success", "data": asdict(report)}


@router.get("/security", summary="Get Monitoring Security & Redaction Audit")
async def get_security() -> Dict[str, Any]:
    """Returns security audit items verifying zero secret exposure in telemetry."""
    runtime = get_runtime()
    report = runtime.security_auditor.audit_security()
    return {"status": "success", "data": asdict(report)}


@router.post("/run", status_code=status.HTTP_200_OK, summary="Execute Full Verification Cycle")
async def run_verification() -> Dict[str, Any]:
    """Triggers an end-to-end verification cycle and exports all 10 manifests."""
    runtime = get_runtime()
    results = runtime.run_full_verification()
    scorecard = results["scorecard"]
    return {
        "status": "completed",
        "overall_score": scorecard.overall_score,
        "certification_tier": scorecard.certification_tier.value,
        "certification_verdict": scorecard.certification_verdict,
        "passed": scorecard.passed,
        "manifests_generated": [str(p) for p in results["manifest_files"].values()],
    }
