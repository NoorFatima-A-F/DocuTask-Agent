"""
Phase 3J.12: Continuous Performance Engineering REST API Endpoints.
"""

from typing import Any, Dict
from fastapi import APIRouter, HTTPException

from ..runtime.continuous_performance_runtime import ContinuousPerformanceRuntime

router = APIRouter(prefix="/api/v1/continuous-performance", tags=["Continuous Performance Engineering"])


@router.get("/health")
def get_health() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "service": "continuous-performance-engineering",
        "phase": "3J.12",
        "timestamp": "2026-09-16T22:30:00Z",
    }


@router.get("/status")
def get_status() -> Dict[str, Any]:
    runtime = ContinuousPerformanceRuntime()
    return {
        "status": "ready",
        "framework": "DocuTask Continuous Performance Engineering & Regression Intelligence",
        "total_verifiers": len(runtime.verifiers),
        "export_dir": str(runtime.export_dir),
    }


@router.post("/verify/all")
def run_all_verifications() -> Dict[str, Any]:
    runtime = ContinuousPerformanceRuntime()
    result = runtime.run_all()
    return {
        "status": result["status"],
        "overall_score": result["overall_score"],
        "certification_tier": result["certification_tier"],
        "execution_time_seconds": result["execution_time_seconds"],
        "total_reports": len(result["reports"]),
        "export_dir": result["export_dir"],
    }


@router.get("/reports/{verifier_id}")
def get_verification_report(verifier_id: str) -> Dict[str, Any]:
    runtime = ContinuousPerformanceRuntime()
    report = runtime.run_verifier(verifier_id)
    if not report:
        raise HTTPException(status_code=404, detail=f"Verifier {verifier_id} not found")
    return report.model_dump()


@router.get("/scorecard")
def get_scorecard() -> Dict[str, Any]:
    runtime = ContinuousPerformanceRuntime()
    result = runtime.run_all()
    return result["scorecard"].model_dump()


@router.get("/evidence/manifest")
def get_evidence_manifest() -> Dict[str, Any]:
    runtime = ContinuousPerformanceRuntime()
    result = runtime.run_all()
    return result["manifest"].model_dump()
