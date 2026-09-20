"""FastAPI Router for AI Resilience & Chaos Verification endpoints."""

from fastapi import APIRouter, Query
from dataclasses import asdict
from typing import Dict, Any, Optional
from ..runtime.ai_resilience_runtime import AIResilienceRuntime

router = APIRouter(prefix="/health/ai-resilience", tags=["AI Failure Simulation & Resilience"])

_runtime = AIResilienceRuntime()


@router.get("/status")
def get_resilience_status() -> Dict[str, Any]:
    """Get high-level AI resilience status and circuit breaker state."""
    cb = _runtime.circuit_breaker_verifier.verify_circuit_breaker()
    return {
        "status": "HEALTHY",
        "circuit_breaker": asdict(cb),
        "target_primary_model": "gemini-2.5-flash",
        "target_fallback_model": "claude-3-5-sonnet",
        "resilience_mode": "ACTIVE",
    }


@router.get("/metrics")
def get_recovery_metrics() -> Dict[str, Any]:
    """Get SRE and resilience recovery metrics."""
    exp = _runtime.chaos_runner.run_all_experiments(documents_per_experiment=20)
    metrics = _runtime.metrics_collector.collect_recovery_metrics(exp)
    return asdict(metrics)


@router.post("/verify")
def run_full_resilience_verification() -> Dict[str, Any]:
    """Triggers the full 15-part AI Resilience verification pipeline."""
    results = _runtime.run_full_verification()
    return {
        "scorecard": asdict(results["scorecard"]),
        "outage_report": asdict(results["outage_report"]),
        "recovery_metrics": asdict(results["recovery_metrics"]),
        "circuit_breaker": asdict(results["circuit_breaker_report"]),
        "manifests_exported": results["exported_manifests"],
    }
