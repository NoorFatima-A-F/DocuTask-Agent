"""
Phase 3H.4.10: Observability Security Verification API
"""
from fastapi import APIRouter, HTTPException, Query
from ..runtime.observability_security_runtime import ObservabilitySecurityRuntime

router = APIRouter(prefix="/platform-verification/observability-security", tags=["Observability Security Verification"])
runtime = ObservabilitySecurityRuntime()


@router.post("/execute-all", summary="Run full observability security verification suite")
def run_observability_security_verification(output_dir: str = Query("observability_security_verification", description="Output directory for manifests")):
    try:
        results = runtime.run_all_verifications(output_dir=output_dir)
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
