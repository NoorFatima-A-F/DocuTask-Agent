"""
REST API Router for Clean Architecture Dependency Validation (PART 2B).
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from app.platform_verification.clean_architecture.runtime.clean_architecture_runtime import (
    EnterpriseCleanArchitectureRuntime,
)

router = APIRouter(prefix="/architecture/dependencies", tags=["Clean Architecture & Dependency Validation"])
_runtime = EnterpriseCleanArchitectureRuntime()


class DependencyScanRequest(BaseModel):
    repository_path: Optional[str] = None
    commit_sha: str = "HEAD"


@router.post("/scan", response_model=Dict[str, Any])
def run_dependency_validation_scan(req: DependencyScanRequest):
    """Executes Clean Architecture inward dependency scan and returns evidence."""
    package = _runtime.run_full_validation(
        target_dir=req.repository_path,
        commit_sha=req.commit_sha,
    )
    return {
        "scan_id": package.scan_id,
        "clean_architecture_certified": package.clean_architecture_certified,
        "violations_count": len(package.violations),
        "circular_cycles_count": len(package.circular_dependency_cycles),
        "total_modules_analyzed": package.total_modules_analyzed,
        "evidence_sha256": package.evidence_sha256,
    }


@router.get("/report/{scan_id}", response_model=Dict[str, Any])
def get_dependency_report(scan_id: str):
    """Retrieves full Clean Architecture evidence report by scan ID."""
    pkg = _runtime.evidence_store.get_evidence(scan_id)
    if not pkg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scan '{scan_id}' not found.",
        )
    return {
        "scan_id": pkg.scan_id,
        "certified": pkg.clean_architecture_certified,
        "violations": [
            {
                "id": v.violation_id,
                "source": v.source_file,
                "target": v.target_module,
                "severity": v.severity.value,
                "message": v.message,
                "fix": v.suggested_fix,
            }
            for v in pkg.violations
        ],
        "metrics_count": len(pkg.module_metrics),
        "evidence_sha256": pkg.evidence_sha256,
    }


@router.get("/violations", response_model=List[Dict[str, Any]])
def get_latest_dependency_violations():
    """Retrieves latest Clean Architecture violations."""
    latest = _runtime.get_latest_scan()
    if not latest:
        return []
    return [
        {
            "violation_id": v.violation_id,
            "source": v.source_file,
            "target": v.target_module,
            "message": v.message,
            "action": v.action.value,
        }
        for v in latest.violations
    ]


@router.get("/metrics", response_model=Dict[str, Any])
def get_latest_module_metrics():
    """Retrieves coupling, instability (I), and distance from main sequence (D)."""
    latest = _runtime.get_latest_scan()
    if not latest:
        return {}
    return {
        mod: {
            "ca": m.afferent_coupling_ca,
            "ce": m.efferent_coupling_ce,
            "instability": m.instability_i,
            "distance": m.distance_from_main_sequence_d,
            "risk": m.architecture_risk,
        }
        for mod, m in latest.module_metrics.items()
    }
