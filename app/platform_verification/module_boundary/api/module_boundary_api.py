"""
REST API Router for Module Boundary & Plugin Verification (PART 2D).
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from app.platform_verification.module_boundary.runtime.module_boundary_runtime import (
    EnterpriseModuleBoundaryRuntime,
)

router = APIRouter(prefix="/architecture/modules", tags=["Module Boundary & Plugin Architecture Governance"])
_runtime = EnterpriseModuleBoundaryRuntime()


class ModuleScanRequest(BaseModel):
    commit_sha: str = "HEAD"


@router.post("/scan", response_model=Dict[str, Any])
def run_module_boundary_scan(req: ModuleScanRequest):
    """Executes full module boundary, plugin compliance, and modularity index scan."""
    package = _runtime.run_full_scan(commit_sha=req.commit_sha)
    return {
        "scan_id": package.scan_id,
        "total_score": package.total_modularity_score,
        "certification_band": package.certification_band.value,
        "is_certified": package.is_certified,
        "violations_count": len(package.boundary_violations),
        "plugins_verified": len(package.plugin_reports),
        "evidence_sha256": package.evidence_sha256,
    }


@router.get("/report/{scan_id}", response_model=Dict[str, Any])
def get_module_report(scan_id: str):
    """Retrieves full module boundary scorecard and plugin compliance report."""
    pkg = _runtime.evidence_store.get_evidence(scan_id)
    if not pkg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scan '{scan_id}' not found.",
        )
    return {
        "scan_id": pkg.scan_id,
        "total_score": pkg.total_modularity_score,
        "certification_band": pkg.certification_band.value,
        "violations": [
            {
                "id": v.violation_id,
                "source": v.source_module,
                "target": v.target_module,
                "severity": v.severity.value,
                "message": v.message,
                "remediation": v.remediation,
            }
            for v in pkg.boundary_violations
        ],
        "plugins": [
            {
                "name": p.plugin_name,
                "type": p.plugin_type,
                "passed": p.passed,
                "errors": p.errors,
            }
            for p in pkg.plugin_reports
        ],
        "evidence_sha256": pkg.evidence_sha256,
    }


@router.get("/plugins", response_model=List[Dict[str, Any]])
def list_verified_plugins():
    """Retrieves all registered and verified plugins."""
    latest = _runtime.get_latest_scan()
    if not latest:
        return []
    return [
        {
            "plugin_id": p.plugin_id,
            "name": p.plugin_name,
            "version": p.version,
            "type": p.plugin_type,
            "passed": p.passed,
        }
        for p in latest.plugin_reports
    ]


@router.get("/metrics", response_model=Dict[str, Any])
def get_latest_module_metrics():
    """Retrieves modularity, independence, and cohesion metrics per module."""
    latest = _runtime.get_latest_scan()
    if not latest:
        return {}
    return {
        mod: {
            "independence": m.independence_score,
            "cohesion": m.cohesion_score,
            "extension": m.extension_score,
            "composite_index": m.composite_modularity_index,
            "risk": m.risk_level,
        }
        for mod, m in latest.module_metrics.items()
    }
