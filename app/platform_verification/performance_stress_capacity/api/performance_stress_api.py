"""
FastAPI Router for Performance Stress Verification & Capacity Boundary Analysis (Phase 3J.2).
"""

from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException, status

from ..runtime.performance_stress_runtime import PerformanceStressRuntime

router = APIRouter(
    prefix="/api/v1/verification/performance-stress",
    tags=["Performance Stress Verification"],
)

_runtime: Optional[PerformanceStressRuntime] = None


def get_runtime() -> PerformanceStressRuntime:
    """Singleton getter for PerformanceStressRuntime."""
    global _runtime
    if _runtime is None:
        _runtime = PerformanceStressRuntime()
    return _runtime


def set_runtime(runtime: PerformanceStressRuntime) -> None:
    """Sets the active runtime instance (useful for testing and dependency injection)."""
    global _runtime
    _runtime = runtime


@router.post("/run", summary="Trigger Full Performance Stress Verification")
def trigger_verification() -> Dict[str, Any]:
    """Runs the complete suite of 10 performance verifiers, calculates certification score, and exports manifests."""
    runtime = get_runtime()
    result = runtime.run_full_verification()
    return {
        "status": "COMPLETED",
        "passed": result["passed"],
        "score": result["score"],
        "tier": result["tier"],
        "exported_files_count": len(result["exported_files"]),
    }


@router.get("/certification", summary="Get Latest Performance Certification")
def get_certification() -> Dict[str, Any]:
    """Retrieves the most recent performance stress and capacity certification report."""
    runtime = get_runtime()
    cert = runtime.get_latest_certification()
    if not cert:
        # Run if not yet executed
        res = runtime.run_full_verification()
        cert = res["certification"]

    if hasattr(cert, "model_dump"):
        return cert.model_dump()
    elif hasattr(cert, "dict"):
        return cert.dict()
    return cert.__dict__


@router.get("/reports/{report_type}", summary="Get Individual Performance Report")
def get_report(report_type: str) -> Dict[str, Any]:
    """Retrieves an individual report by type (e.g., 'baseline', 'load', 'stress', 'boundary', 'scaling', 'database', 'ai', 'memory', 'recovery', 'regression')."""
    runtime = get_runtime()
    if not runtime._latest_reports:
        runtime.run_full_verification()

    key_aliases = {
        "environment": "environment_isolation",
        "baseline": "baseline_stress",
        "load": "progressive_load",
        "stress": "overload_stress",
        "boundary": "capacity_boundary",
        "scaling": "worker_scaling",
        "database": "database_performance",
        "ai": "ai_provider_stress",
        "memory": "memory_stability",
        "recovery": "recovery",
        "regression": "regression",
    }

    lookup_key = key_aliases.get(report_type, report_type)
    report = runtime._latest_reports.get(lookup_key)

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report '{report_type}' not found. Available reports: {list(key_aliases.keys())}",
        )

    if hasattr(report, "model_dump"):
        return report.model_dump()
    elif hasattr(report, "dict"):
        return report.dict()
    return report.__dict__


@router.get("/health", summary="Subsystem Health Check")
def get_health() -> Dict[str, Any]:
    """Returns the operational status of the Performance Verification subsystem."""
    return {
        "status": "HEALTHY",
        "phase": "3J.2",
        "subsystem": "Performance Stress Verification & Capacity Boundary Analysis",
        "verifiers_count": 11,
    }
