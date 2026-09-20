"""
Phase 3I.11: Enterprise Observability Platform REST API Router
Provides endpoints for querying multi-environment telemetry, drift detection, readiness gates, and global certification.
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.platform_verification.enterprise_observability_platform.runtime.enterprise_observability_runtime import (
    EnterpriseObservabilityRuntime,
)

router = APIRouter(
    prefix="/api/v1/enterprise-observability",
    tags=["Enterprise Observability & Global Reliability Control"],
)

_runtime_instance = EnterpriseObservabilityRuntime()


@router.get("/status")
def get_platform_status() -> Dict[str, Any]:
    """Returns the operational status of the Enterprise Observability Control Plane."""
    return {
        "status": "ONLINE",
        "phase": "Phase 3I.11 — Enterprise Observability Platform Integration & Global Reliability Control",
        "project": "DocuTask-Agent",
        "control_plane": "Centralized Multi-Environment Reliability Control Plane",
        "connected_environments": 5,
    }


@router.post("/run-verification")
def run_full_enterprise_verification() -> Dict[str, Any]:
    """Executes full verification across all 11 modules, evaluates 7-category certification, and exports manifests."""
    try:
        pipeline_result = _runtime_instance.run_pipeline()
        cert_report = pipeline_result["certification_report"]
        return {
            "status": "SUCCESS",
            "certification_granted": pipeline_result["success"],
            "composite_global_score_pct": cert_report.composite_global_score_pct,
            "certification_tier": cert_report.certification_tier.value,
            "exported_files_count": len(pipeline_result["exported_files"]),
            "exported_files": pipeline_result["exported_files"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enterprise verification pipeline failed: {str(e)}")


@router.get("/environments")
def get_federated_environments() -> Dict[str, Any]:
    """Returns telemetry federation status across Development, Testing, Staging, Production, and DR."""
    report = _runtime_instance.telemetry_verifier.verify()
    return report.model_dump()


@router.get("/drift")
def get_drift_detection_report() -> Dict[str, Any]:
    """Returns environment drift detection across infrastructure, configuration, and observability layers."""
    report = _runtime_instance.drift_verifier.verify()
    return report.model_dump()


@router.get("/readiness-gates")
def get_production_readiness_gates() -> Dict[str, Any]:
    """Returns multi-stage production release approval gate status and health scores."""
    report = _runtime_instance.readiness_verifier.verify()
    return report.model_dump()


@router.get("/multi-region")
def get_multi_region_status() -> Dict[str, Any]:
    """Returns multi-region health, replication lag, and automated failover telemetry."""
    report = _runtime_instance.multi_region_verifier.verify()
    return report.model_dump()


@router.get("/certification")
def get_global_certification() -> Dict[str, Any]:
    """Computes and returns the 7-category enterprise global certification scorecard."""
    verification_results = _runtime_instance.execute_all_verifications()
    cert_report = _runtime_instance.scorer.compute_certification(verification_results)
    return cert_report.model_dump()
