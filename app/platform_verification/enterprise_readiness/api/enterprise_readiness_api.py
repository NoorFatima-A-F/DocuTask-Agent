"""FastAPI Router for Enterprise Readiness Endpoints."""

from fastapi import APIRouter
from dataclasses import asdict
from typing import Dict, Any
from ..runtime.enterprise_readiness_runtime import EnterpriseReadinessRuntime

router = APIRouter(tags=["Enterprise Readiness"])

_runtime = EnterpriseReadinessRuntime()


@router.get("/ready")
def get_ready() -> Dict[str, Any]:
    """Standardized Kubernetes / Cloud LB GET /ready probe endpoint."""
    res = _runtime.run_full_verification()
    dep_rep = res["dependency_report"]
    return {
        "status": "ready" if dep_rep.overall_readiness_state.value == "READY" else "not_ready",
        "state": dep_rep.overall_readiness_state.value,
        "timestamp": res["scorecard"].timestamp,
        "version": "1.0.0",
        "checks": {item.name: item.status for item in dep_rep.evaluated_dependencies},
    }


@router.get("/health/readiness/status")
def get_readiness_status() -> Dict[str, Any]:
    """Detailed health and readiness status."""
    res = _runtime.run_full_verification()
    return {
        "scorecard": asdict(res["scorecard"]),
        "dependency_report": asdict(res["dependency_report"]),
        "startup_report": asdict(res["startup_report"]),
        "orchestration_report": asdict(res["orchestration_report"]),
    }


@router.post("/health/readiness/verify")
def trigger_readiness_verification() -> Dict[str, Any]:
    """Triggers full 12-part enterprise readiness verification."""
    res = _runtime.run_full_verification()
    return {
        "scorecard": asdict(res["scorecard"]),
        "manifests": res["exported_manifests"],
    }
