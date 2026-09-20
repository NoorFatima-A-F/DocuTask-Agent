"""
FastAPI REST API router for Enterprise Cloud Readiness Verification (Phase 3M).
"""

import json
import os
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from app.platform_verification.enterprise_cloud_readiness.domain.models import (
    CloudReadinessScorecard,
    VerificationManifest,
)
from app.platform_verification.enterprise_cloud_readiness.runtime.cloud_readiness_runtime import (
    CloudReadinessRuntime,
)

router = APIRouter(prefix="/api/v1/cloud-readiness", tags=["Enterprise Cloud Readiness"])
_runtime = CloudReadinessRuntime()


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check for cloud readiness verification service."""
    return {"status": "healthy", "service": "enterprise-cloud-readiness"}


@router.get("/phases")
async def list_phases() -> List[Dict[str, str]]:
    """List all 15 verification phases supported by Phase 3M."""
    return [
        {"phase_id": "3M.1", "name": "Cloud Architecture Assessment"},
        {"phase_id": "3M.2", "name": "Container Cloud Compatibility Verification"},
        {"phase_id": "3M.3", "name": "Cloud Compute Resource Verification"},
        {"phase_id": "3M.4", "name": "Cloud Networking Verification"},
        {"phase_id": "3M.5", "name": "Cloud Storage Compatibility Verification"},
        {"phase_id": "3M.6", "name": "Managed Database Readiness Verification"},
        {"phase_id": "3M.7", "name": "Cloud Queue and Worker Scalability Verification"},
        {"phase_id": "3M.8", "name": "Auto Scaling Readiness Verification"},
        {"phase_id": "3M.9", "name": "Cloud Secret Management Verification"},
        {"phase_id": "3M.10", "name": "Cloud Observability Compatibility"},
        {"phase_id": "3M.11", "name": "Infrastructure as Code Verification"},
        {"phase_id": "3M.12", "name": "Kubernetes Readiness Verification"},
        {"phase_id": "3M.13", "name": "Cloud Security Verification"},
        {"phase_id": "3M.14", "name": "Multi-Cloud Portability Verification"},
        {"phase_id": "3M.15", "name": "Cloud Migration Simulation"},
    ]


@router.post("/run", response_model=VerificationManifest)
@router.post("/verify/all", response_model=VerificationManifest)
async def run_verification_suite(export_dir: str = "cloud_readiness_verification") -> VerificationManifest:
    """Trigger full execution of all 15 cloud readiness verification phases and export evidence artifacts."""
    manifest = await _runtime.run_all(export_dir=export_dir)
    return manifest


@router.get("/reports/{identifier}")
async def get_phase_report(identifier: str) -> Dict[str, Any]:
    """Execute and retrieve a specific phase verification report by ID or phase number."""
    try:
        report = _runtime.execute_verifier(identifier)
        return report.model_dump()
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/scorecard", response_model=CloudReadinessScorecard)
async def get_scorecard() -> CloudReadinessScorecard:
    """Run full verification or read cached scorecard and return the CloudReadinessScorecard."""
    scorecard = _runtime.get_latest_scorecard()
    if scorecard is None:
        res = _runtime.run_full_verification()
        scorecard = res["scorecard"]
    return scorecard


@router.get("/manifest", response_model=VerificationManifest)
@router.get("/evidence/manifest", response_model=VerificationManifest)
async def get_manifest() -> VerificationManifest:
    """Retrieve the latest cloud readiness verification manifest with SHA-256 hashes."""
    manifest = _runtime.get_latest_manifest()
    if manifest is not None:
        return manifest

    manifest_path = os.path.join("cloud_readiness_verification", "metadata.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return VerificationManifest(**data)
    raise HTTPException(status_code=404, detail="Manifest not found. Run /run or /verify/all endpoint first.")
