"""
Phase 3H.5.5: Self-Healing Verification API
"""
from fastapi import APIRouter, HTTPException, Query
from ..runtime.self_healing_runtime import SelfHealingRuntime

router = APIRouter(prefix="/platform-verification/self-healing", tags=["Self-Healing & Recovery Verification"])
runtime = SelfHealingRuntime()


@router.post("/execute", summary="Execute full 5-layer self-healing verification suite")
def execute_self_healing_verification():
    try:
        results = runtime.run_full_self_healing_verification()
        return {
            "status": "SUCCESS",
            "composite_score": results["composite_score"],
            "tier": results["tier"],
            "certified": results["certified"],
            "exported_files": results["exported_files"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status", summary="Get self-healing verification status and scorecard")
def get_self_healing_status():
    results = runtime.run_full_self_healing_verification()
    return {
        "scorecard": results["scorecard"],
        "validation_report": results["validation_report"],
    }
