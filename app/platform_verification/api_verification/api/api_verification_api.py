"""
REST API Router for API Architecture Verification (PART 2E).
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from app.platform_verification.api_verification.runtime.api_verification_runtime import (
    EnterpriseApiVerificationRuntime,
)

router = APIRouter(prefix="/architecture/api", tags=["API Architecture & Contract Governance"])
_runtime = EnterpriseApiVerificationRuntime()


class ApiScanRequest(BaseModel):
    commit_sha: str = "HEAD"


@router.post("/scan", response_model=Dict[str, Any])
def run_api_architecture_scan(req: ApiScanRequest):
    """Executes full API purity, security, and compatibility analysis."""
    package = _runtime.run_full_scan(commit_sha=req.commit_sha)
    score = package.scorecard.total_score if package.scorecard else 0.0
    band = package.scorecard.certification_band.value if package.scorecard else "FAILED"

    return {
        "scan_id": package.scan_id,
        "total_score": score,
        "certification_band": band,
        "is_deployable": package.scorecard.is_deployable if package.scorecard else False,
        "endpoints_analyzed": package.endpoints_analyzed_count,
        "breaking_changes_count": len(package.breaking_changes),
        "security_findings_count": len(package.security_findings),
        "evidence_sha256": package.evidence_sha256,
    }


@router.get("/report/{scan_id}", response_model=Dict[str, Any])
def get_api_report(scan_id: str):
    """Retrieves full API architecture report by scan ID."""
    pkg = _runtime.evidence_store.get_evidence(scan_id)
    if not pkg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scan '{scan_id}' not found.",
        )
    return {
        "scan_id": pkg.scan_id,
        "scorecard": {
            "total_score": pkg.scorecard.total_score if pkg.scorecard else 0.0,
            "band": pkg.scorecard.certification_band.value if pkg.scorecard else "",
            "layer_purity": pkg.scorecard.layer_purity_score if pkg.scorecard else 0.0,
            "security": pkg.scorecard.security_score if pkg.scorecard else 0.0,
            "compatibility": pkg.scorecard.compatibility_score if pkg.scorecard else 0.0,
        },
        "breaking_changes": [
            {"type": b.change_type, "path": b.path, "field": b.field_name, "desc": b.description}
            for b in pkg.breaking_changes
        ],
        "evidence_sha256": pkg.evidence_sha256,
    }
