"""FastAPI REST API router for Enterprise Bottleneck Discovery (Phase 3J.7)."""

import json
import os
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from app.platform_verification.enterprise_performance_bottleneck.domain.models import (
    BottleneckVerificationManifest,
    EnterpriseBottleneckCertificationReport,
)
from app.platform_verification.enterprise_performance_bottleneck.runtime.bottleneck_discovery_runtime import (
    BottleneckDiscoveryRuntime,
)

router = APIRouter(prefix="/api/v1/bottleneck-discovery", tags=["Enterprise Bottleneck Discovery"])
_runtime = BottleneckDiscoveryRuntime()


@router.get("/health")
async def health_check() -> Dict[str, str]:
    return {"status": "healthy", "service": "enterprise-bottleneck-discovery"}


@router.get("/phases")
async def list_phases() -> List[Dict[str, str]]:
    return [
        {"phase_id": "3J.7.1", "name": "Performance Architecture Profiling"},
        {"phase_id": "3J.7.2", "name": "Resource Saturation Analysis"},
        {"phase_id": "3J.7.3", "name": "Application-Level Bottleneck Analysis"},
        {"phase_id": "3J.7.4", "name": "Database Bottleneck Verification"},
        {"phase_id": "3J.7.5", "name": "Queue Bottleneck Analysis"},
        {"phase_id": "3J.7.6", "name": "Worker Capacity Modeling"},
        {"phase_id": "3J.7.7", "name": "AI Provider Performance Analysis"},
        {"phase_id": "3J.7.8", "name": "Performance Regression Detection"},
        {"phase_id": "3J.7.9", "name": "Capacity Boundary Discovery"},
        {"phase_id": "3J.7.10", "name": "Performance Optimization Recommendations"},
    ]


@router.post("/run", response_model=BottleneckVerificationManifest)
async def run_verification_suite() -> BottleneckVerificationManifest:
    manifest = await _runtime.run_all()
    return manifest


@router.get("/reports/{phase_id}")
async def get_phase_report(phase_id: str) -> Dict[str, Any]:
    try:
        report = _runtime.execute_verifier(phase_id)
        return report.model_dump()
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/certification", response_model=EnterpriseBottleneckCertificationReport)
async def get_certification() -> EnterpriseBottleneckCertificationReport:
    await _runtime.run_all()
    cert_path = os.path.join("performance_verification", "certification_report.json")
    if os.path.exists(cert_path):
        with open(cert_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return EnterpriseBottleneckCertificationReport(**data)
    raise HTTPException(status_code=500, detail="Certification report could not be generated.")


@router.get("/manifest", response_model=BottleneckVerificationManifest)
async def get_manifest() -> BottleneckVerificationManifest:
    manifest_path = os.path.join("performance_verification", "metadata.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return BottleneckVerificationManifest(**data)
    raise HTTPException(status_code=404, detail="Manifest not found. Run /run endpoint first.")
