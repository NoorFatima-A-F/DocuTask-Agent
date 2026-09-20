"""
Readiness Engine API Router.
Exposes FastAPI endpoints for /ready, /worker/ready, verification execution, and Prometheus metrics.
"""
from fastapi import APIRouter, Response, status
from typing import Dict, Any

from app.platform_verification.readiness_engine.runtime.readiness_engine_runtime import ReadinessEngineRuntime
from app.platform_verification.readiness_engine.domain.models import ReadinessState

router = APIRouter(prefix="", tags=["Readiness Engine"])
runtime = ReadinessEngineRuntime()


@router.get("/ready")
def get_service_readiness(response: Response) -> Dict[str, Any]:
    """
    Kubernetes / Production Load Balancer Readiness Probe Endpoint.
    Returns HTTP 200 when READY or DEGRADED, HTTP 503 when NOT_READY or STARTING.
    """
    db_report = runtime.db_checker.check_readiness()
    queue_report = runtime.queue_checker.check_readiness()
    storage_report = runtime.storage_checker.check_readiness()
    ai_report = runtime.ai_checker.check_readiness()
    worker_report = runtime.worker_checker.check_readiness()

    result = runtime.evaluator.evaluate_readiness(
        db_report=db_report,
        queue_report=queue_report,
        storage_report=storage_report,
        ai_report=ai_report,
        worker_report=worker_report,
    )

    if result.state in [ReadinessState.NOT_READY, ReadinessState.STARTING, ReadinessState.UNKNOWN]:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    else:
        response.status_code = status.HTTP_200_OK

    return {
        "service": result.service,
        "state": result.state.value,
        "traffic_allowed": result.traffic_allowed,
        "reason": result.reason,
        "checks": result.checks,
        "timestamp": result.timestamp,
    }


@router.get("/worker/ready")
def get_worker_readiness(response: Response, worker_id: str = "worker-001") -> Dict[str, Any]:
    """
    Worker fleet readiness probe endpoint.
    """
    report = runtime.worker_checker.check_readiness(worker_id=worker_id)
    if not report.passed:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    else:
        response.status_code = status.HTTP_200_OK

    return {
        "worker_id": report.worker_id,
        "status": report.status,
        "active_jobs": report.active_jobs,
        "capacity": report.capacity,
        "can_process_tasks": report.can_process_tasks,
    }


@router.get("/verification/readiness-engine/verify")
def run_readiness_engine_verification() -> Dict[str, Any]:
    """
    Triggers end-to-end verification across all 14 parts.
    """
    results = runtime.execute_full_verification()
    scorecard = results["scorecard"]
    return {
        "status": "COMPLETED",
        "overall_score": scorecard.overall_readiness_score,
        "certification_tier": scorecard.certification_tier.value,
        "certification_verdict": scorecard.certification_verdict,
        "traffic_admission_safe": scorecard.traffic_admission_safe,
        "passed": scorecard.passed,
        "scores": {
            "dependency_detection": scorecard.dependency_detection_score,
            "failure_accuracy": scorecard.failure_accuracy_score,
            "policy_correctness": scorecard.policy_correctness_score,
            "kubernetes_compatibility": scorecard.kubernetes_compatibility_score,
            "security": scorecard.security_score,
            "observability": scorecard.observability_score,
        },
        "exported_files": results["exported_files"],
    }


@router.get("/verification/readiness-engine/metrics")
def get_readiness_prometheus_metrics(response: Response) -> str:
    """
    Exports Prometheus metrics for readiness engine monitoring.
    """
    response.headers["Content-Type"] = "text/plain; version=0.0.4"
    return runtime.metrics_exporter.generate_prometheus_payload()
