"""Predictive Health API Endpoints.

FastAPI router providing observability and predictive health status endpoints.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, Optional

from fastapi import APIRouter, Response, status

from app.platform_verification.predictive_health_intelligence.runtime.predictive_health_runtime import (
    PredictiveHealthRuntime,
)

router = APIRouter(prefix="/health/predictive", tags=["Predictive Health Intelligence"])

# Shared runtime singleton for the API
_runtime_instance: Optional[PredictiveHealthRuntime] = None


def get_runtime() -> PredictiveHealthRuntime:
    global _runtime_instance
    if _runtime_instance is None:
        _runtime_instance = PredictiveHealthRuntime()
    return _runtime_instance


@router.get("/summary", summary="Get Predictive Health Summary Scorecard")
async def get_summary() -> Dict[str, Any]:
    """Returns the latest predictive health evaluation scorecard."""
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
            "telemetry_quality": scorecard.telemetry_quality_score,
            "anomaly_detection": scorecard.anomaly_detection_score,
            "prediction_accuracy": scorecard.prediction_accuracy_score,
            "early_warning": scorecard.early_warning_score,
            "preventive_actions": scorecard.preventive_actions_score,
            "observability": scorecard.observability_score,
        },
    }


@router.get("/telemetry", summary="Get Current Health Telemetry")
async def get_telemetry() -> Dict[str, Any]:
    """Returns the aggregated health telemetry metrics."""
    runtime = get_runtime()
    report = runtime.collector.collect_comprehensive_telemetry()
    return {"status": "success", "data": asdict(report)}


@router.get("/baseline", summary="Get Health Baselines")
async def get_baseline() -> Dict[str, Any]:
    """Returns current operational baseline profiles."""
    runtime = get_runtime()
    report = runtime.baseline_manager.get_baseline_report()
    return {"status": "success", "data": asdict(report)}


@router.get("/anomalies", summary="Get Detected Anomalies")
async def get_anomalies() -> Dict[str, Any]:
    """Returns anomalies detected in recent telemetry."""
    runtime = get_runtime()
    report = runtime.anomaly_detector.detect_anomalies()
    return {"status": "success", "data": asdict(report)}


@router.get("/risks", summary="Get Health Risk Predictions")
async def get_risks() -> Dict[str, Any]:
    """Returns predictive failure probabilities and risk levels."""
    runtime = get_runtime()
    report = runtime.risk_engine.compute_risk_predictions()
    return {"status": "success", "data": asdict(report)}


@router.get("/early-warnings", summary="Get Early Warning Alerts")
async def get_early_warnings() -> Dict[str, Any]:
    """Returns proactive early warning alerts across the 5 failure categories."""
    runtime = get_runtime()
    report = runtime.early_warning_system.generate_early_warnings()
    return {"status": "success", "data": asdict(report)}


@router.get("/recommendations", summary="Get Preventive Action Recommendations")
async def get_recommendations() -> Dict[str, Any]:
    """Returns recommended automated/manual preventive actions."""
    runtime = get_runtime()
    report = runtime.recommender.generate_recommendations()
    return {"status": "success", "data": asdict(report)}


@router.get("/accuracy", summary="Get Anomaly & Prediction Accuracy Benchmarks")
async def get_accuracy() -> Dict[str, Any]:
    """Returns precision, recall, F1, and false positive benchmark metrics."""
    runtime = get_runtime()
    report = runtime.validator.evaluate_accuracy()
    return {"status": "success", "data": asdict(report)}


@router.get("/metrics", summary="Prometheus Telemetry Metrics Endpoint")
async def get_prometheus_metrics() -> Response:
    """Exports all health and predictive metrics in Prometheus text exposition format."""
    runtime = get_runtime()
    content = runtime.metrics_exporter.generate_prometheus_payload()
    return Response(content=content, media_type="text/plain; version=0.0.4; charset=utf-8")


@router.post("/run", status_code=status.HTTP_200_OK, summary="Trigger Full Verification Cycle")
async def run_verification() -> Dict[str, Any]:
    """Executes an end-to-end predictive health verification run and exports evidence."""
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
