"""Alert Accuracy API Router.

Exposes endpoints for triggering alert accuracy verification and querying reliability scorecards.
"""

from dataclasses import asdict
from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any

from ..runtime.alert_accuracy_verification_runtime import AlertAccuracyVerificationRuntime

router = APIRouter(prefix="/api/v1/verification/alert-accuracy", tags=["Alert Accuracy Verification"])
runtime = AlertAccuracyVerificationRuntime()


@router.post("/run", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def run_verification() -> Dict[str, Any]:
    """Execute complete Alert Accuracy & Intelligence Verification pipeline and export evidence manifests."""
    try:
        scorecard, manifests = runtime.execute_full_verification()
        return {
            "status": "success",
            "scorecard": asdict(scorecard),
            "manifests_exported": list(manifests.keys()),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Alert accuracy verification pipeline execution failed: {str(e)}",
        )


@router.get("/scorecard", response_model=Dict[str, Any])
def get_scorecard() -> Dict[str, Any]:
    """Retrieve the latest quality scorecard for alert accuracy."""
    scorecard, _ = runtime.execute_full_verification()
    return asdict(scorecard)
