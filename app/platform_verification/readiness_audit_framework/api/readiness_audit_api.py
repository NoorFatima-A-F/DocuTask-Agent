"""FastAPI Router for Readiness Audit & Evidence endpoints."""

from fastapi import APIRouter
from dataclasses import asdict
from typing import Dict, Any
from ..runtime.readiness_audit_runtime import ReadinessAuditRuntime

router = APIRouter(prefix="/health/readiness-audit", tags=["Readiness Evidence & Audit"])

_runtime = ReadinessAuditRuntime()


@router.get("/status")
def get_audit_status() -> Dict[str, Any]:
    """Get high-level audit summary and scorecard."""
    results = _runtime.run_full_audit()
    return {
        "status": "HEALTHY",
        "scorecard": asdict(results["scorecard"]),
        "metadata": asdict(results["metadata"]),
        "cicd_decision": results["cicd_decision"],
    }


@router.get("/integrity")
def get_integrity_status() -> Dict[str, Any]:
    """Get SHA-256 evidence integrity status."""
    results = _runtime.run_full_audit()
    return asdict(results["integrity_report"])


@router.post("/package")
def generate_evidence_package() -> Dict[str, Any]:
    """Generates and returns the complete 13-manifest readiness audit package."""
    results = _runtime.run_full_audit()
    return {
        "scorecard": asdict(results["scorecard"]),
        "cicd_decision": results["cicd_decision"],
        "manifests_generated": results["manifests"],
    }
