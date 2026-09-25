"""
Phase 3H.4.9: Incident Recovery Verification API
"""
from fastapi import APIRouter, HTTPException, Query
from ..runtime.recovery_verification_runtime import RecoveryVerificationRuntime

router = APIRouter(prefix="/platform-verification/incident-recovery", tags=["Incident Recovery Verification"])
runtime = RecoveryVerificationRuntime()


@router.post("/execute-all", summary="Run full incident recovery verification suite")
def run_recovery_verification():
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


@router.get("/scorecard", summary="Get incident recovery scorecard")
def get_recovery_scorecard():
    results = runtime.run_all_verifications()
    return results["scorecard"]
