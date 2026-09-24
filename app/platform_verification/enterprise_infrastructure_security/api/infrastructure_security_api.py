"""
FastAPI REST API router for Enterprise Infrastructure Security Verification (Phase 3N).
"""

import json
import os
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from app.platform_verification.enterprise_infrastructure_security.domain.models import (
    SecurityScorecard,
    VerificationManifest,
)
from app.platform_verification.enterprise_infrastructure_security.runtime.infrastructure_security_runtime import (
    InfrastructureSecurityRuntime,
)

router = APIRouter(prefix="/api/v1/security", tags=["Enterprise Infrastructure Security"])
_runtime = InfrastructureSecurityRuntime()


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check for infrastructure security verification service."""
    return {"status": "healthy", "service": "enterprise-infrastructure-security"}


@router.get("/phases")
async def list_phases() -> List[Dict[str, str]]:
    """List all 16 verification phases supported by Phase 3N."""
    return [
        {"phase_id": "3N.1", "name": "Infrastructure Security Architecture Verification"},
        {"phase_id": "3N.2", "name": "Threat Modeling & STRIDE Verification"},
        {"phase_id": "3N.3", "name": "Container Security & Isolation Verification"},
        {"phase_id": "3N.4", "name": "Container Image & Supply Chain Security Verification"},
        {"phase_id": "3N.5", "name": "Vulnerability Management & CVE Verification"},
        {"phase_id": "3N.6", "name": "Secret Management & Credential Security Verification"},
        {"phase_id": "3N.7", "name": "Identity & Access Management (IAM) Verification"},
        {"phase_id": "3N.8", "name": "Network Security & Segmentation Verification"},
        {"phase_id": "3N.9", "name": "Service-to-Service Security & mTLS Verification"},
        {"phase_id": "3N.10", "name": "API Infrastructure Security Verification"},
        {"phase_id": "3N.11", "name": "Database & Data Layer Security Verification"},
        {"phase_id": "3N.12", "name": "Storage & Document Security Verification"},
        {"phase_id": "3N.13", "name": "AI Model & Inference Infrastructure Security Verification"},
        {"phase_id": "3N.14", "name": "CI/CD & Pipeline Security Gate Verification"},
        {"phase_id": "3N.15", "name": "Security Failure & Attack Simulation Verification"},
        {"phase_id": "3N.16", "name": "Security Observability & SIEM Verification"},
    ]


@router.post("/run", response_model=VerificationManifest)
@router.post("/verify/all", response_model=VerificationManifest)
async def run_verification_suite() -> VerificationManifest:
    """Trigger full execution of all 16 security verification phases and export evidence artifacts."""
    manifest = await _runtime.run_all(export_dir="security_verification")
    return manifest


@router.get("/reports/{identifier}")
async def get_phase_report(identifier: str) -> Dict[str, Any]:
    """Execute and retrieve a specific phase verification report by ID or phase number."""
    try:
        report = _runtime.execute_verifier(identifier)
        return report.model_dump()
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/scorecard", response_model=SecurityScorecard)
async def get_scorecard() -> SecurityScorecard:
    """Run full verification or read cached scorecard and return the SecurityScorecard."""
    scorecard = _runtime.get_latest_scorecard()
    if scorecard is None:
        res = _runtime.run_full_verification()
        scorecard = res["scorecard"]
    return scorecard


@router.get("/manifest", response_model=VerificationManifest)
@router.get("/evidence/manifest", response_model=VerificationManifest)
async def get_manifest() -> VerificationManifest:
    """Retrieve the latest security verification manifest with SHA-256 hashes."""
    manifest = _runtime.get_latest_manifest()
    if manifest is not None:
        return manifest

    manifest_path = os.path.join("security_verification", "metadata.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return VerificationManifest(**data)
    raise HTTPException(status_code=404, detail="Manifest not found. Run /run or /verify/all endpoint first.")
