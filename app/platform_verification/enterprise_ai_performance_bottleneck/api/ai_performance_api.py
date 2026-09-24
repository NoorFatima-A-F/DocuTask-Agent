"""FastAPI REST API router for AI Performance Bottleneck & Capacity (Phase 3J.9)."""

import json
import os
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from app.platform_verification.enterprise_ai_performance_bottleneck.domain.models import (
    AIPerformanceVerificationManifest,
    EnterpriseAIPerformanceCertificationReport,
)
from app.platform_verification.enterprise_ai_performance_bottleneck.runtime.ai_performance_runtime import (
    AIPerformanceRuntime,
)

router = APIRouter(prefix="/api/v1/ai-performance", tags=["Enterprise AI Performance Verification"])
_runtime = AIPerformanceRuntime()


@router.get("/health")
async def health_check() -> Dict[str, str]:
    return {"status": "healthy", "service": "enterprise-ai-performance-verification"}


@router.get("/phases")
async def list_phases() -> List[Dict[str, str]]:
    return [
        {"phase_id": "3J.9.1", "name": "Performance Architecture Modeling"},
        {"phase_id": "3J.9.2", "name": "End-to-End Latency Profiling"},
        {"phase_id": "3J.9.3", "name": "Throughput Capacity Verification"},
        {"phase_id": "3J.9.4", "name": "Resource Bottleneck Analysis"},
        {"phase_id": "3J.9.5", "name": "Database Performance Analysis"},
        {"phase_id": "3J.9.6", "name": "Queue Performance Analysis"},
        {"phase_id": "3J.9.7", "name": "Worker Scaling Analysis"},
        {"phase_id": "3J.9.8", "name": "AI Model Performance Verification"},
        {"phase_id": "3J.9.9", "name": "Performance Regression Detection"},
        {"phase_id": "3J.9.10", "name": "Capacity Planning Model"},
        {"phase_id": "3J.9.11", "name": "Performance Failure Simulation"},
        {"phase_id": "3J.9.12", "name": "Performance Observability Validation"},
    ]


@router.post("/run", response_model=AIPerformanceVerificationManifest)
async def run_verification_suite() -> AIPerformanceVerificationManifest:
    manifest = await _runtime.run_all()
    return manifest


@router.get("/reports/{phase_id}")
async def get_phase_report(phase_id: str) -> Dict[str, Any]:
    try:
        report = _runtime.execute_verifier(phase_id)
        return report.model_dump()
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/certification", response_model=EnterpriseAIPerformanceCertificationReport)
async def get_certification() -> EnterpriseAIPerformanceCertificationReport:
    await _runtime.run_all()
    cert_path = os.path.join("performance_ai_verification", "certification_report.json")
    if os.path.exists(cert_path):
        with open(cert_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return EnterpriseAIPerformanceCertificationReport(**data)
    raise HTTPException(status_code=500, detail="Certification report could not be generated.")


@router.get("/manifest", response_model=AIPerformanceVerificationManifest)
async def get_manifest() -> AIPerformanceVerificationManifest:
    manifest_path = os.path.join("performance_ai_verification", "metadata.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return AIPerformanceVerificationManifest(**data)
    raise HTTPException(status_code=404, detail="Manifest not found. Run /run endpoint first.")
