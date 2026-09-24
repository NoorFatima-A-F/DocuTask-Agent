"""FastAPI REST API router for Enterprise Autoscaling & Elastic Capacity (Phase 3J.8)."""

import json
import os
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from app.platform_verification.enterprise_performance_autoscaling.domain.models import (
    AutoscalingVerificationManifest,
    EnterpriseAutoscalingCertificationReport,
)
from app.platform_verification.enterprise_performance_autoscaling.runtime.autoscaling_runtime import (
    AutoscalingRuntime,
)

router = APIRouter(prefix="/api/v1/autoscaling", tags=["Enterprise Autoscaling Verification"])
_runtime = AutoscalingRuntime()


@router.get("/health")
async def health_check() -> Dict[str, str]:
    return {"status": "healthy", "service": "enterprise-autoscaling-verification"}


@router.get("/phases")
async def list_phases() -> List[Dict[str, str]]:
    return [
        {"phase_id": "3J.8.1", "name": "Elastic Scaling Architecture Design"},
        {"phase_id": "3J.8.2", "name": "Scaling Metric Verification"},
        {"phase_id": "3J.8.3", "name": "Horizontal Worker Scaling Verification"},
        {"phase_id": "3J.8.4", "name": "Queue-Based Autoscaling Verification"},
        {"phase_id": "3J.8.5", "name": "API Service Scaling Verification"},
        {"phase_id": "3J.8.6", "name": "Scaling Decision Algorithm Verification"},
        {"phase_id": "3J.8.7", "name": "Scale-Up Performance Verification"},
        {"phase_id": "3J.8.8", "name": "Scale-Down Safety Verification"},
        {"phase_id": "3J.8.9", "name": "Database Scaling Impact Verification"},
        {"phase_id": "3J.8.10", "name": "AI Provider Scaling Verification"},
        {"phase_id": "3J.8.11", "name": "Kubernetes Autoscaling Readiness Verification"},
        {"phase_id": "3J.8.12", "name": "Cloud Scaling Compatibility Verification"},
        {"phase_id": "3J.8.13", "name": "Cost-Aware Scaling Verification"},
        {"phase_id": "3J.8.14", "name": "Scaling Failure Simulation"},
    ]


@router.post("/run", response_model=AutoscalingVerificationManifest)
async def run_verification_suite() -> AutoscalingVerificationManifest:
    manifest = await _runtime.run_all()
    return manifest


@router.get("/reports/{phase_id}")
async def get_phase_report(phase_id: str) -> Dict[str, Any]:
    try:
        report = _runtime.execute_verifier(phase_id)
        return report.model_dump()
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/certification", response_model=EnterpriseAutoscalingCertificationReport)
async def get_certification() -> EnterpriseAutoscalingCertificationReport:
    await _runtime.run_all()
    cert_path = os.path.join("performance_scaling_verification", "certification_report.json")
    if os.path.exists(cert_path):
        with open(cert_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return EnterpriseAutoscalingCertificationReport(**data)
    raise HTTPException(status_code=500, detail="Certification report could not be generated.")


@router.get("/manifest", response_model=AutoscalingVerificationManifest)
async def get_manifest() -> AutoscalingVerificationManifest:
    manifest_path = os.path.join("performance_scaling_verification", "metadata.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return AutoscalingVerificationManifest(**data)
    raise HTTPException(status_code=404, detail="Manifest not found. Run /run endpoint first.")
