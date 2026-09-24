"""FastAPI REST API router for Enterprise Performance Baseline & Capacity Verification."""

import os
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from app.platform_verification.enterprise_performance_capacity.domain.models import (
    EnterprisePerformanceCertificationReport,
    PerformanceVerificationManifest,
)
from app.platform_verification.enterprise_performance_capacity.runtime.performance_quality_runtime import (
    PerformanceQualityRuntime,
)

router = APIRouter(prefix="/api/v1/performance-verification", tags=["Enterprise Performance Verification"])
_runtime = PerformanceQualityRuntime()


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check for performance verification service."""
    return {"status": "healthy", "service": "enterprise-performance-verification"}


@router.get("/phases")
async def list_phases() -> List[Dict[str, str]]:
    """List all 15 verification phases supported by Phase 3J.5."""
    return [
        {"phase_id": "3J.5.1", "name": "Performance Baseline Definition"},
        {"phase_id": "3J.5.2", "name": "Latency Verification & Component Breakdown"},
        {"phase_id": "3J.5.3", "name": "Throughput Capacity Testing"},
        {"phase_id": "3J.5.4", "name": "Concurrent User Simulation & Controlled Load Testing"},
        {"phase_id": "3J.5.6", "name": "Stress Testing Framework"},
        {"phase_id": "3J.5.7", "name": "Spike Testing Framework"},
        {"phase_id": "3J.5.8", "name": "72-Hour Endurance & Long-Running Soak Testing"},
        {"phase_id": "3J.5.9", "name": "AI Workload Performance & Cost Profiling"},
        {"phase_id": "3J.5.10", "name": "Queue Performance & Backpressure Verification"},
        {"phase_id": "3J.5.11", "name": "Database Performance & Concurrency Verification"},
        {"phase_id": "3J.5.12", "name": "Storage Performance & Large File Handling Verification"},
        {"phase_id": "3J.5.13", "name": "Resource Utilization Verification"},
        {"phase_id": "3J.5.14", "name": "Automated Bottleneck Detection & Remediation Analysis"},
        {"phase_id": "3J.5.15", "name": "Capacity Planning & Scaling Modeling"},
        {"phase_id": "3J.5.16", "name": "Performance Regression & Release Comparison Verification"},
    ]


@router.post("/run", response_model=PerformanceVerificationManifest)
async def run_verification_suite(output_dir: str = "performance_verification") -> PerformanceVerificationManifest:
    """Trigger full execution of all 15 verification phases and export evidence artifacts."""
    manifest = await _runtime.run_all(output_dir=output_dir)
    return manifest


@router.get("/reports/{phase_id}")
async def get_phase_report(phase_id: str) -> Dict[str, Any]:
    """Execute and retrieve a specific phase verification report."""
    try:
        report = _runtime.execute_verifier(phase_id)
        return report.model_dump()
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))



@router.get("/certification", response_model=EnterprisePerformanceCertificationReport)
async def get_certification() -> EnterprisePerformanceCertificationReport:
    """Run full verification and return only the final Enterprise Performance Certification Report."""
    await _runtime.run_all()
    # Read certification report
    cert_path = os.path.join("performance_verification", "certification_report.json")
    if os.path.exists(cert_path):
        import json
        with open(cert_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return EnterprisePerformanceCertificationReport(**data)
    raise HTTPException(status_code=500, detail="Certification report could not be generated.")


@router.get("/manifest", response_model=PerformanceVerificationManifest)
async def get_manifest() -> PerformanceVerificationManifest:
    """Retrieve the latest performance verification manifest with SHA-256 hashes."""
    manifest_path = os.path.join("performance_verification", "metadata.json")
    if os.path.exists(manifest_path):
        import json
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return PerformanceVerificationManifest(**data)
    raise HTTPException(status_code=404, detail="Manifest not found. Run /run endpoint first.")
