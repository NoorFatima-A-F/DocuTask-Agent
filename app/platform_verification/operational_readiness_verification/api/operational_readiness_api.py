"""
Phase 3H.4.11: Operational Readiness Verification API
"""
from fastapi import APIRouter, HTTPException, Query
from ..runtime.operational_readiness_runtime import OperationalReadinessRuntime

router = APIRouter(prefix="/platform-verification/operational-readiness", tags=["Operational Readiness Verification"])
runtime = OperationalReadinessRuntime()


@router.post("/evaluate", summary="Evaluate operational readiness and generate certification")
def evaluate_readiness():
    try:
        results = runtime.evaluate_operational_readiness()
        return {
            "status": "SUCCESS",
            "composite_score": results["composite_score"],
            "certification": results["certification"],
            "maturity_level": results["maturity_level"],
            "release_approved": results["release_approved"],
            "exported_files": results["exported_files"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/scorecard", summary="Get current operational readiness scorecard")
def get_readiness_scorecard():
    results = runtime.evaluate_operational_readiness()
    return results["scorecard"]
