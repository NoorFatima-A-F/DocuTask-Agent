"""
FastAPI REST API router for Enterprise Backup, Disaster Recovery & Business Continuity (Phase 3L).
"""

import json
import os
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from app.platform_verification.enterprise_disaster_recovery.domain.models import (
    DisasterRecoveryScorecard,
    VerificationManifest,
)
from app.platform_verification.enterprise_disaster_recovery.runtime.disaster_recovery_runtime import (
    DisasterRecoveryRuntime,
)

router = APIRouter(prefix="/api/v1/disaster-recovery", tags=["Enterprise Disaster Recovery"])
_runtime = DisasterRecoveryRuntime()


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check for disaster recovery verification service."""
    return {"status": "healthy", "service": "enterprise-disaster-recovery"}


@router.get("/phases")
async def list_phases() -> List[Dict[str, str]]:
    """List all 13 verification phases supported by Phase 3L."""
    return [
        {"phase_id": "3L.1", "name": "Disaster Recovery Architecture Design"},
        {"phase_id": "3L.2", "name": "Business Impact Analysis Verification"},
        {"phase_id": "3L.3", "name": "Recovery Objective Definition (RTO & RPO)"},
        {"phase_id": "3L.4", "name": "Database Backup & Recovery Verification"},
        {"phase_id": "3L.5", "name": "Document Storage Backup & Integrity Verification"},
        {"phase_id": "3L.6", "name": "Application Configuration Recovery"},
        {"phase_id": "3L.7", "name": "Secret and Credential Recovery Verification"},
        {"phase_id": "3L.8", "name": "Complete System Restore Test"},
        {"phase_id": "3L.9", "name": "Point-in-Time Recovery Verification"},
        {"phase_id": "3L.10", "name": "Backup Security Verification"},
        {"phase_id": "3L.11", "name": "Disaster Recovery Automation Pipeline"},
        {"phase_id": "3L.12", "name": "Disaster Recovery Failure Simulations"},
        {"phase_id": "3L.13", "name": "Recovery Observability"},
    ]


@router.post("/run", response_model=VerificationManifest)
@router.post("/verify/all", response_model=VerificationManifest)
async def run_verification_suite(export_dir: str = "disaster_recovery_verification") -> VerificationManifest:
    """Trigger full execution of all 13 disaster recovery verification phases and export evidence artifacts."""
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


@router.get("/scorecard", response_model=DisasterRecoveryScorecard)
async def get_scorecard() -> DisasterRecoveryScorecard:
    """Run full verification or read cached scorecard and return the DisasterRecoveryScorecard."""
    scorecard = _runtime.get_latest_scorecard()
    if scorecard is None:
        res = _runtime.run_full_verification()
        scorecard = res["scorecard"]
    return scorecard


@router.get("/manifest", response_model=VerificationManifest)
@router.get("/evidence/manifest", response_model=VerificationManifest)
async def get_manifest() -> VerificationManifest:
    """Retrieve the latest disaster recovery verification manifest with SHA-256 hashes."""
    manifest = _runtime.get_latest_manifest()
    if manifest is not None:
        return manifest

    manifest_path = os.path.join("disaster_recovery_verification", "metadata.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return VerificationManifest(**data)
    raise HTTPException(status_code=404, detail="Manifest not found. Run /run or /verify/all endpoint first.")
