"""
FastAPI REST API Router for Continuous Infrastructure Verification & CI/CD Assurance (Phase 3Q).
"""

import json
import os
from typing import Dict, List
from fastapi import APIRouter, HTTPException

from ..domain.models import (
    InfrastructureDriftReport,
    PerformanceRegressionReport,
    ProductionReadinessCertificate,
    ReleaseDecision,
    SecurityGateReport,
    VerificationManifest,
)
from ..runtime.continuous_verification_runtime import (
    ContinuousVerificationRuntime,
)

router = APIRouter(prefix="/api/v1/pipeline", tags=["Enterprise Continuous Verification"])
_runtime = ContinuousVerificationRuntime()


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check for continuous verification pipeline service."""
    return {"status": "healthy", "service": "enterprise-continuous-verification"}


@router.get("/stages")
async def list_stages() -> List[Dict[str, str]]:
    """List the 7 automated CI/CD continuous infrastructure verification stages."""
    return [
        {"stage": "1. Change Impact Analysis", "description": "Detects modified architectural components & required tests"},
        {"stage": "2. Build & Metadata Verification", "description": "Deterministic container builds & image digests"},
        {"stage": "3. Automated Security Gates", "description": "Zero Critical CVEs (Trivy) & Zero Secret Leaks (Gitleaks)"},
        {"stage": "4. Disposable Test Environments", "description": "Ephemeral Docker test network & deep health probes"},
        {"stage": "5. End-to-End Integration", "description": "Full document processing flow validation"},
        {"stage": "6. Performance Regression Gate", "description": "Automated P95 latency & throughput SLA verification"},
        {"stage": "7. Release Decision & Certification", "description": "Automated PASS/BLOCK decision & production certificate"},
    ]


@router.post("/run", response_model=VerificationManifest)
@router.post("/verify/all", response_model=VerificationManifest)
async def run_pipeline(export_dir: str = "pipeline_evidence") -> VerificationManifest:
    """Execute the complete end-to-end continuous verification CI/CD pipeline."""
    manifest = await _runtime.run_all(export_dir=export_dir)
    return manifest


@router.get("/decision", response_model=ReleaseDecision)
async def get_decision() -> ReleaseDecision:
    """Retrieve the latest production release gate decision (APPROVED / BLOCKED)."""
    dec = _runtime.get_latest_decision()
    if dec is None:
        res = _runtime.run_pipeline()
        dec = res["decision"]
    return dec


@router.get("/certificate", response_model=ProductionReadinessCertificate)
async def get_certificate() -> ProductionReadinessCertificate:
    """Retrieve the official production readiness certificate."""
    cert = _runtime.get_latest_certificate()
    if cert is None:
        res = _runtime.run_pipeline()
        cert = res["certificate"]
    return cert


@router.get("/security", response_model=SecurityGateReport)
async def get_security_gate() -> SecurityGateReport:
    """Retrieve the automated CI/CD security gate report."""
    sec = _runtime.get_latest_security()
    if sec is None:
        res = _runtime.run_pipeline()
        sec = res["security"]
    return sec


@router.get("/performance", response_model=PerformanceRegressionReport)
async def get_performance_regression() -> PerformanceRegressionReport:
    """Retrieve the automated CI/CD performance regression report."""
    perf = _runtime.get_latest_performance()
    if perf is None:
        res = _runtime.run_pipeline()
        perf = res["performance"]
    return perf


@router.get("/drift", response_model=InfrastructureDriftReport)
async def get_drift_report() -> InfrastructureDriftReport:
    """Retrieve the infrastructure configuration drift detection report."""
    drift = _runtime.get_latest_drift()
    if drift is None:
        res = _runtime.run_pipeline()
        drift = res["drift"]
    return drift


@router.get("/manifest", response_model=VerificationManifest)
@router.get("/evidence/manifest", response_model=VerificationManifest)
async def get_manifest() -> VerificationManifest:
    """Retrieve the latest cryptographic SHA-256 verification manifest."""
    manifest = _runtime.get_latest_manifest()
    if manifest is not None:
        return manifest

    manifest_path = os.path.join("pipeline_evidence", "metadata.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return VerificationManifest(**data)
    raise HTTPException(status_code=404, detail="Manifest not found. Run /run endpoint first.")
