"""
Phase 3H.4.12: Observability Audit Certification API
"""
from fastapi import APIRouter, HTTPException, Query
from ..runtime.observability_audit_certification_runtime import ObservabilityAuditCertificationRuntime

router = APIRouter(prefix="/platform-verification/observability-certification", tags=["Observability Audit & Certification"])
runtime = ObservabilityAuditCertificationRuntime()


@router.post("/execute", summary="Execute full observability audit, PRR review, and certification pipeline")
def execute_observability_certification():
    try:
        results = runtime.run_full_audit_and_certification()
        return {
            "status": "SUCCESS",
            "composite_score": results["composite_score"],
            "tier": results["tier"],
            "decision": results["decision"],
            "exported_files": results["exported_files"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status", summary="Get current certification and PRR status")
def get_certification_status():
    results = runtime.run_full_audit_and_certification()
    return {
        "certification": results["certification_report"],
        "cicd_gate": results["cicd_gate_report"],
        "prr_review": results["prr_report"],
    }
