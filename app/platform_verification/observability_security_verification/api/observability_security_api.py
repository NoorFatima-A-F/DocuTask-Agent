"""
Phase 3H.4.10: Observability Security Verification API
"""
from fastapi import APIRouter, HTTPException, Query
from ..runtime.observability_security_runtime import ObservabilitySecurityRuntime

router = APIRouter(prefix="/platform-verification/observability-security", tags=["Observability Security Verification"])
runtime = ObservabilitySecurityRuntime()


@router.post("/execute-all", summary="Run full observability security verification suite")
def run_observability_security_verification():
    try:
        results = runtime.run_all_verifications()
        return {
            "status": "SUCCESS",
            "composite_score": results["scorecard"].composite_score,
            "tier": results["scorecard"].tier.value,
            "certified": results["scorecard"].certified_enterprise_ready,
            "exported_files": results["exported_files"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/scorecard", summary="Get observability security scorecard")
def get_observability_security_scorecard():
    results = runtime.run_all_verifications()
    return results["scorecard"]
