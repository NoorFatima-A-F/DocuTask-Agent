"""
Phase 3H.7: Operational Resilience Verification FastAPI Endpoints
"""
from fastapi import APIRouter, Query
from typing import Dict, Any, Optional

from app.platform_verification.operational_resilience.runtime.operational_resilience_runtime import OperationalResilienceRuntime

router = APIRouter(
    prefix="/api/v1/platform-verification/operational-resilience",
    tags=["Phase 3H.7: Operational Resilience Verification"],
)

_runtime = OperationalResilienceRuntime()


@router.post("/verify", summary="Execute Full Operational Resilience Verification")
async def run_resilience_verification(export_evidence: bool = Query(True, description="Whether to export verification reports to disk")) -> Dict[str, Any]:
    result = _runtime.run_full_verification(export_evidence=export_evidence)
    return {
        "status": "SUCCESS",
        "scorecard": result["scorecard"].model_dump(),
        "summary": {
            "tier": result["scorecard"].certification_tier.value,
            "overall_score": result["scorecard"].overall_resilience_score,
            "passed": result["scorecard"].passed,
            "reports_exported": bool(result["export_metadata"]),
        },
    }


@router.get("/scorecard", summary="Get Latest Resilience Scorecard")
async def get_resilience_scorecard() -> Dict[str, Any]:
    result = _runtime.run_full_verification(export_evidence=False)
    return {
        "scorecard": result["scorecard"].model_dump(),
    }


@router.get("/strategies", summary="Get Defined Enterprise Resilience Strategies")
async def get_resilience_strategies() -> Dict[str, Any]:
    report = _runtime.arch_verifier.verify_resilience_architecture()
    return report.model_dump()


@router.get("/circuit-breakers", summary="Get Subsystem Circuit Breakers Status")
async def get_circuit_breakers() -> Dict[str, Any]:
    report = _runtime.cb_verifier.verify_circuit_breakers()
    return report.model_dump()


@router.get("/metrics", summary="Get Resilience Observability Telemetry Metrics")
async def get_resilience_metrics() -> Dict[str, Any]:
    report = _runtime.metrics_verifier.collect_resilience_metrics()
    return report.model_dump()


@router.get("/health", summary="Resilience Verification Engine Health")
async def get_engine_health() -> Dict[str, Any]:
    return {
        "status": "HEALTHY",
        "framework": "DocuTask Agent Platform Verification (Phase 3H.7)",
        "engine": "Operational Resilience Verification Engine",
        "ready": True,
    }
