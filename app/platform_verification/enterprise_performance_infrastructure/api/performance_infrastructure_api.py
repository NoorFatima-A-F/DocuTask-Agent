"""FastAPI REST API router for Enterprise Performance Infrastructure Verification (Phase 3J.6)."""

import os
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from app.platform_verification.enterprise_performance_infrastructure.domain.models import (
    EnterprisePerformanceCertificationReport,
    PerformanceVerificationManifest,
)
from app.platform_verification.enterprise_performance_infrastructure.runtime.performance_infrastructure_runtime import (
    PerformanceInfrastructureRuntime,
)

router = APIRouter(prefix="/api/v1/performance-infrastructure", tags=["Enterprise Performance Infrastructure"])
_runtime = PerformanceInfrastructureRuntime()


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check for performance infrastructure verification service."""
    return {"status": "healthy", "service": "enterprise-performance-infrastructure"}


@router.get("/phases")
async def list_phases() -> List[Dict[str, str]]:
    """List all 13 verification phases supported by Phase 3J.6."""
    return [
        {"phase_id": "3J.6.1", "name": "Performance Test Architecture Design"},
        {"phase_id": "3J.6.2", "name": "Enterprise Workload Modeling"},
        {"phase_id": "3J.6.3", "name": "API Gateway Performance & Endpoint Latency"},
        {"phase_id": "3J.6.4", "name": "End-to-End Document Workflow Performance"},
        {"phase_id": "3J.6.5", "name": "Throughput Scaling & Worker Elasticity"},
        {"phase_id": "3J.6.6", "name": "PostgreSQL Database Performance & Concurrency"},
        {"phase_id": "3J.6.7", "name": "Redis Queue Capacity & Ingestion Dynamics"},
        {"phase_id": "3J.6.8", "name": "Worker Efficiency & Resource Sizing"},
        {"phase_id": "3J.6.9", "name": "System Resource Utilization"},
        {"phase_id": "3J.6.10", "name": "Memory Stability & Soak Leak Detection"},
        {"phase_id": "3J.6.11", "name": "Graceful Degradation & Overload Behavior"},
        {"phase_id": "3J.6.12", "name": "Capacity Limit Discovery & Boundary Specification"},
        {"phase_id": "3J.6.13", "name": "Performance Monitoring & Telemetry Integration"},
    ]


@router.post("/run", response_model=PerformanceVerificationManifest)
async def run_verification_suite(output_dir: str = "performance_verification") -> PerformanceVerificationManifest:
    """Trigger full execution of all 13 verification phases and export evidence artifacts."""
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
