"""
Phase 3J.10: Enterprise SLA/SLO Verification REST API Endpoints.
"""

from typing import Any, Dict
from fastapi import APIRouter, HTTPException

from ..runtime.sla_slo_runtime import SLASLORuntime

router = APIRouter(prefix="/api/v1/sla-slo", tags=["Enterprise SLA/SLO Verification"])


@router.get("/health")
def get_health() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "service": "enterprise-sla-slo-verification",
        "phase": "3J.10",
        "timestamp": "2026-09-16T22:30:00Z",
    }


@router.get("/status")
def get_status() -> Dict[str, Any]:
    runtime = SLASLORuntime()
    return {
        "status": "ready",
        "framework": "DocuTask Enterprise SLA/SLO Verification",
        "total_verifiers": len(runtime.verifiers),
        "export_dir": str(runtime.export_dir),
    }


@router.post("/verify/all")
def run_all_verifications() -> Dict[str, Any]:
    runtime = SLASLORuntime()
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
    runtime = SLASLORuntime()
    report = runtime.run_verifier(verifier_id)
    if not report:
        raise HTTPException(status_code=404, detail=f"Verifier {verifier_id} not found")
    return report.model_dump()


@router.get("/scorecard")
def get_scorecard() -> Dict[str, Any]:
    runtime = SLASLORuntime()
    result = runtime.run_all()
    return result["scorecard"].model_dump()


@router.get("/evidence/manifest")
def get_evidence_manifest() -> Dict[str, Any]:
    runtime = SLASLORuntime()
    result = runtime.run_all()
    return result["manifest"].model_dump()
