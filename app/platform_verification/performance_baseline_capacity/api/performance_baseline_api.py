"""
FastAPI Router for Phase 3J.3: Enterprise Performance Baseline & Capacity Verification Framework.
"""

from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException, Query, status

from ..domain.models import PerformanceQualityCertificationReport
from ..runtime.performance_baseline_runtime import PerformanceBaselineRuntime

router = APIRouter(
    prefix="/api/v1/verification/performance-baseline",
    tags=["Performance Baseline & Capacity Verification"],
)

_runtime: Optional[PerformanceBaselineRuntime] = None


def get_runtime() -> PerformanceBaselineRuntime:
    """Singleton getter for PerformanceBaselineRuntime."""
    global _runtime
    if _runtime is None:
        _runtime = PerformanceBaselineRuntime()
    return _runtime


def set_runtime(runtime: PerformanceBaselineRuntime) -> None:
    """Sets active runtime instance (for tests and DI)."""
    global _runtime
    _runtime = runtime


@router.post("/run", summary="Trigger Full Performance Baseline & Capacity Verification")
def trigger_verification() -> Dict[str, Any]:
    """Runs complete suite of 12 performance verifiers, calculates certification score, and exports manifests."""
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
    """Retrieves the most recent performance baseline and capacity certification report."""
    runtime = get_runtime()
    cert = runtime.get_latest_certification()
    if not cert:
        res = runtime.run_full_verification()
        cert = res["certification"]

    if hasattr(cert, "model_dump"):
        return cert.model_dump()
    elif hasattr(cert, "dict"):
        return cert.dict()
    return cert.__dict__


@router.get("/reports/{report_type}", summary="Get Individual Performance Report")
def get_report(report_type: str) -> Dict[str, Any]:
    """Retrieves an individual report by type (e.g., 'baseline', 'load', 'capacity', 'ai', 'latency', 'resource', 'database', 'queue', 'scaling', 'failure', 'regression')."""
    runtime = get_runtime()
    if not runtime._latest_reports:
        runtime.run_full_verification()

    key_aliases = {
        "architecture": "performance_architecture",
        "baseline": "baseline_performance",
        "ai": "ai_pipeline_performance",
        "load": "concurrent_load",
        "capacity": "capacity_model",
        "latency": "latency_distribution",
        "resource": "resource_utilization",
        "database": "database_performance",
        "queue": "queue_capacity",
        "scaling": "worker_scaling",
        "failure": "performance_failure",
        "regression": "performance_regression",
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
    """Returns the operational status of the Performance Baseline Verification subsystem."""
    return {
        "status": "HEALTHY",
        "phase": "3J.3",
        "subsystem": "Enterprise Performance Baseline & Capacity Verification Framework",
        "verifiers_count": 12,
    }
