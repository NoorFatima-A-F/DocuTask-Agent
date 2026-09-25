"""Incident Signal Verification API Router.

Exposes endpoints for triggering incident signal verification and retrieving scorecards.
"""

from dataclasses import asdict
from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any

from ..runtime.incident_signal_verification_runtime import IncidentSignalVerificationRuntime

router = APIRouter(prefix="/api/v1/verification/incidents", tags=["Incident Signal Verification"])
runtime = IncidentSignalVerificationRuntime()


@router.post("/run", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def run_verification() -> Dict[str, Any]:
    """Execute complete Incident Signal Verification pipeline and export evidence manifests."""
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
            detail=f"Incident signal verification pipeline execution failed: {str(e)}",
        )


@router.get("/scorecard", response_model=Dict[str, Any])
def get_scorecard() -> Dict[str, Any]:
    """Retrieve the latest quality scorecard for incident signals."""
    scorecard, _ = runtime.execute_full_verification()
    return asdict(scorecard)
