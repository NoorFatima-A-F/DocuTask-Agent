"""
FastAPI REST API router for Enterprise Chaos Engineering Verification (Phase 3K).
"""

import json
import os
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from app.platform_verification.enterprise_chaos_verification.domain.models import (
    ChaosScorecard,
    VerificationManifest,
)
from app.platform_verification.enterprise_chaos_verification.runtime.chaos_runtime import (
    ChaosRuntime,
)

router = APIRouter(prefix="/api/v1/chaos", tags=["Enterprise Chaos Engineering"])
_runtime = ChaosRuntime()


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check for chaos verification service."""
    return {"status": "healthy", "service": "enterprise-chaos-verification"}


@router.get("/phases")
async def list_phases() -> List[Dict[str, str]]:
    """List all 12 verification phases supported by Phase 3K."""
    return [
        {"phase_id": "3K.1", "name": "Chaos Experiment Readiness & Steady-State Verification"},
        {"phase_id": "3K.2", "name": "Container & Service Crash Failure Verification"},
        {"phase_id": "3K.3", "name": "Database Failure & Replication Degradation Verification"},
        {"phase_id": "3K.4", "name": "Message Queue & Broker Failure Verification"},
        {"phase_id": "3K.5", "name": "Network Partition, Latency & Packet Loss Verification"},
        {"phase_id": "3K.6", "name": "AI Model Provider & External Dependency Failure Verification"},
        {"phase_id": "3K.7", "name": "Resource Exhaustion & Starvation Verification"},
        {"phase_id": "3K.8", "name": "Worker & Agent Failure Recovery Verification"},
        {"phase_id": "3K.9", "name": "Cascading Failure & Blast Radius Verification"},
        {"phase_id": "3K.10", "name": "Automated Chaos Experiment Pipeline Verification"},
        {"phase_id": "3K.11", "name": "Chaos Observability & Telemetry Verification"},
        {"phase_id": "3K.12", "name": "Chaos Engineering Reporting & Continuous Verification"},
    ]


@router.post("/run", response_model=VerificationManifest)
@router.post("/verify/all", response_model=VerificationManifest)
async def run_verification_suite() -> VerificationManifest:
    """Trigger full execution of all 12 chaos verification phases and export evidence artifacts."""
    manifest = await _runtime.run_all(export_dir="chaos_verification")
    return manifest


@router.get("/reports/{identifier}")
async def get_phase_report(identifier: str) -> Dict[str, Any]:
    """Execute and retrieve a specific phase verification report by ID or phase number."""
    try:
        report = _runtime.execute_verifier(identifier)
        return report.model_dump()
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/scorecard", response_model=ChaosScorecard)
async def get_scorecard() -> ChaosScorecard:
    """Run full verification or read cached scorecard and return the ChaosScorecard."""
    scorecard = _runtime.get_latest_scorecard()
    if scorecard is None:
        res = _runtime.run_full_verification()
        scorecard = res["scorecard"]
    return scorecard


@router.get("/manifest", response_model=VerificationManifest)
@router.get("/evidence/manifest", response_model=VerificationManifest)
async def get_manifest() -> VerificationManifest:
    """Retrieve the latest chaos verification manifest with SHA-256 hashes."""
    manifest = _runtime.get_latest_manifest()
    if manifest is not None:
        return manifest

    manifest_path = os.path.join("chaos_verification", "metadata.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return VerificationManifest(**data)
    raise HTTPException(status_code=404, detail="Manifest not found. Run /run or /verify/all endpoint first.")
