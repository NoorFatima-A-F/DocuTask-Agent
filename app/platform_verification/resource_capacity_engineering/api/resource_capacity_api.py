"""
FastAPI Router for Phase 3J.4: Resource Utilization & Capacity Engineering Verification Framework.
"""

from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException, Query, status

from ..domain.models import ResourceCapacityCertificationReport
from ..runtime.resource_capacity_runtime import ResourceCapacityRuntime

router = APIRouter(
    prefix="/api/v1/verification/resource-capacity",
    tags=["Resource Capacity Engineering Verification"],
)

_runtime: Optional[ResourceCapacityRuntime] = None


def get_runtime() -> ResourceCapacityRuntime:
    """Singleton getter for ResourceCapacityRuntime."""
    global _runtime
    if _runtime is None:
        _runtime = ResourceCapacityRuntime()
    return _runtime


def set_runtime(runtime: ResourceCapacityRuntime) -> None:
    """Sets active runtime instance (for tests and DI)."""
    global _runtime
    _runtime = runtime


@router.post("/run", summary="Trigger Full Resource Capacity Verification")
def trigger_verification() -> Dict[str, Any]:
    """Runs complete suite of 11 resource and capacity verifiers, calculates certification score, and exports manifests."""
    runtime = get_runtime()
    result = runtime.run_full_verification()
    return {
        "status": "COMPLETED",
        "passed": result["passed"],
        "score": result["score"],
        "tier": result["tier"],
        "exported_files_count": len(result["exported_files"]),
    }


@router.get("/certification", summary="Get Latest Resource Capacity Certification")
def get_certification() -> Dict[str, Any]:
    """Retrieves the most recent resource utilization and capacity certification report."""
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


@router.get("/reports/{report_type}", summary="Get Individual Resource Report")
def get_report(report_type: str) -> Dict[str, Any]:
    """Retrieves an individual report by type (e.g., 'profile', 'policy', 'cpu', 'memory', 'worker', 'queue', 'database', 'ai', 'model', 'scaling', 'alert')."""
    runtime = get_runtime()
    if not runtime._latest_reports:
        runtime.run_full_verification()

    key_aliases = {
        "profile": "resource_profiling",
        "policy": "container_policy",
        "cpu": "cpu_capacity",
        "memory": "memory_leak",
        "worker": "worker_capacity",
        "queue": "queue_capacity",
        "database": "database_capacity",
        "ai": "ai_resource_profile",
        "model": "capacity_modeling",
        "scaling": "autoscaling_readiness",
        "alert": "resource_alerting",
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
    """Returns operational status of the Resource Capacity Verification subsystem."""
    return {
        "status": "HEALTHY",
        "phase": "3J.4",
        "subsystem": "Resource Utilization & Capacity Engineering Verification Framework",
        "verifiers_count": 11,
    }
