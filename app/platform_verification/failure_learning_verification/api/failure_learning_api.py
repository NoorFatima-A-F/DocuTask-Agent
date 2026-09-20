"""
Phase 3H.5.6: Failure Learning & RCA API Router
"""
from fastapi import APIRouter
from ..runtime.failure_learning_runtime import FailureLearningRuntime

router = APIRouter(prefix="/failure-learning", tags=["Phase 3H.5.6 - Failure Learning & RCA"])
runtime = FailureLearningRuntime()


@router.get("/status")
def get_failure_learning_status():
    return {"status": "ACTIVE", "phase": "3H.5.6", "engine": "Adaptive Reliability Intelligence"}


@router.post("/verify")
def run_failure_learning_verification():
    results = runtime.run_full_failure_learning_verification()
    return {
        "composite_score": results["composite_score"],
        "tier": results["tier"],
        "certified": results["certified"],
        "total_manifests_exported": len(results["exported_files"]),
    }
