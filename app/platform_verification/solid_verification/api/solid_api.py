"""
REST API Router for SOLID Principle Verification (PART 2C).
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.platform_verification.solid_verification.runtime.solid_verification_runtime import (
    EnterpriseSolidVerificationRuntime,
)

router = APIRouter(prefix="/architecture/solid", tags=["SOLID Principle Architecture Governance"])
_runtime = EnterpriseSolidVerificationRuntime()


class SolidScanRequest(BaseModel):
    repository_path: Optional[str] = None
    commit_sha: str = "HEAD"


@router.post("/scan", response_model=Dict[str, Any])
def run_solid_analysis(req: SolidScanRequest):
    """Executes full SOLID AST analysis, scores design quality, and saves evidence."""
    package = _runtime.run_full_scan(
        commit_sha=req.commit_sha,
    )
    score = package.scorecard.total_score if package.scorecard else 0.0
    band = package.scorecard.certification_band.value if package.scorecard else "FAILED"

    return {
        "scan_id": package.scan_id,
        "total_score": score,
        "certification_band": band,
        "is_design_certified": package.clean_architecture_certified if hasattr(package, "clean_architecture_certified") else True,
        "violations_count": len(package.violations),
        "total_classes_analyzed": package.total_classes_analyzed,
        "evidence_sha256": package.evidence_sha256,
    }


@router.get("/report/{scan_id}", response_model=Dict[str, Any])
def get_solid_report(scan_id: str):
    """Retrieves full SOLID design scorecard and violations by scan ID."""
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
            "principles": [
                {"principle": ps.principle.value, "raw": ps.raw_score, "weighted": ps.weighted_score}
                for ps in (pkg.scorecard.principle_scores if pkg.scorecard else [])
            ],
        },
        "violations": [
            {
                "id": v.violation_id,
                "principle": v.principle.value,
                "class": v.class_name,
                "file": v.file_path,
                "severity": v.severity.value,
                "message": v.message,
                "refactoring": v.suggested_refactoring,
            }
            for v in pkg.violations
        ],
        "evidence_sha256": pkg.evidence_sha256,
    }


@router.get("/violations", response_model=List[Dict[str, Any]])
def get_latest_solid_violations():
    """Retrieves list of latest SOLID design violations."""
    latest = _runtime.get_latest_scan()
    if not latest:
        return []
    return [
        {
            "id": v.violation_id,
            "principle": v.principle.value,
            "class": v.class_name,
            "severity": v.severity.value,
            "message": v.message,
        }
        for v in latest.violations
    ]


@router.get("/metrics", response_model=Dict[str, Any])
def get_latest_solid_metrics():
    """Retrieves latest class and interface metrics."""
    latest = _runtime.get_latest_scan()
    if not latest:
        return {}
    return {
        "classes_count": len(latest.class_metrics),
        "interfaces_count": len(latest.interface_metrics),
        "total_score": latest.scorecard.total_score if latest.scorecard else 0.0,
    }
