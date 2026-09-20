"""Grafana Verification API Router.

Exposes endpoints for triggering Grafana dashboard verification and querying scorecard / audit results.
"""

from dataclasses import asdict
from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any

from ..runtime.grafana_verification_runtime import GrafanaVerificationRuntime

router = APIRouter(prefix="/api/v1/verification/grafana", tags=["Grafana Verification"])
runtime = GrafanaVerificationRuntime()


@router.post("/run", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def run_verification() -> Dict[str, Any]:
    """Execute complete Grafana Dashboard Verification pipeline and export evidence manifests."""
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
            detail=f"Grafana verification pipeline execution failed: {str(e)}",
        )


@router.get("/scorecard", response_model=Dict[str, Any])
def get_scorecard() -> Dict[str, Any]:
    """Retrieve the latest quality scorecard for Grafana dashboards."""
    scorecard, _ = runtime.execute_full_verification()
    return asdict(scorecard)
