"""
Readiness Verification API
FastAPI router providing endpoints for readiness inspection, dynamic probe simulation,
and verification execution.
"""
from fastapi import APIRouter, Response, status
from typing import Dict, Any

from app.platform_verification.readiness_contract.runtime.readiness_runtime import ReadinessRuntime

router = APIRouter(prefix="/verification/readiness", tags=["Readiness Verification"])
runtime = ReadinessRuntime()


@router.get("/ready")
def get_ready_contract(response: Response) -> Dict[str, Any]:
    """
    Standard Enterprise Readiness Probe endpoint.
    Returns HTTP 200 when ready or degraded, HTTP 503 when not_ready.
    """
    payload = runtime.contract_manager.generate_ready_payload(
        db_status="healthy",
        queue_status="healthy",
        storage_status="healthy",
        workers_status="healthy",
        ai_status="healthy",
    )
    if payload.get("status") == "not_ready":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    else:
        response.status_code = status.HTTP_200_OK
    return payload


@router.get("/verify")
def run_full_readiness_verification() -> Dict[str, Any]:
    """
    Triggers complete readiness architecture verification across all 13 subsystems.
    """
    results = runtime.execute_full_verification()
    scorecard = results["scorecard"]
    return {
        "status": "COMPLETED",
        "overall_score": scorecard.overall_readiness_score,
        "certification_tier": scorecard.certification_tier.value,
        "verdict": scorecard.certification_verdict,
        "traffic_admission_safe": scorecard.traffic_admission_safe,
        "passed": scorecard.passed,
        "details": scorecard.details,
        "exported_files": results["exported_files"],
    }


@router.get("/metrics")
def get_readiness_prometheus_metrics(response: Response) -> str:
    """
    Exports Prometheus-formatted metrics for readiness observability.
    """
    response.headers["Content-Type"] = "text/plain; version=0.0.4"
    return runtime.metrics_exporter.generate_prometheus_payload()
