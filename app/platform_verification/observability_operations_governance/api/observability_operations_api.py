"""
Phase 3I.10: Observability Intelligence Governance REST API Router
Provides endpoints for triggering governance verification, inspecting maturity, and querying operational runbooks.
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.platform_verification.observability_operations_governance.runtime.observability_operations_runtime import (
    ObservabilityOperationsRuntime,
)

router = APIRouter(
    prefix="/api/v1/observability-governance",
    tags=["Observability Operations Governance & Certification"],
)

_runtime_instance = ObservabilityOperationsRuntime()


@router.get("/status")
def get_governance_status() -> Dict[str, Any]:
    """Returns the operational status of the observability governance verification framework."""
    return {
        "status": "ONLINE",
        "phase": "Phase 3I.10 — Observability Intelligence Governance, Reliability Automation Maturity & Enterprise Operations Certification",
        "system": "DocuTask Agent Platform",
        "target_level": "Level 5: Autonomous",
    }


@router.post("/run-verification")
def run_full_governance_verification() -> Dict[str, Any]:
    """Triggers end-to-end execution of all 10 governance verifiers, scoring, and artifact export."""
    try:
        pipeline_result = _runtime_instance.run_pipeline()
        cert_report = pipeline_result["certification_report"]
        return {
            "status": "SUCCESS",
            "autonomous_operations_certified": pipeline_result["success"],
            "composite_operations_score_pct": cert_report.composite_operations_score_pct,
            "certification_tier": cert_report.certification_tier.value,
            "exported_files_count": len(pipeline_result["exported_files"]),
            "exported_files": pipeline_result["exported_files"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Governance verification pipeline failed: {str(e)}")


@router.get("/maturity")
def get_reliability_maturity() -> Dict[str, Any]:
    """Returns the platform reliability maturity assessment."""
    report = _runtime_instance.maturity_verifier.verify()
    return report.model_dump()


@router.get("/runbooks")
def get_operational_runbooks() -> Dict[str, Any]:
    """Returns the automated operational runbook catalog and execution specs."""
    report = _runtime_instance.runbook_verifier.verify()
    return report.model_dump()


@router.get("/policies")
def get_observability_policies() -> Dict[str, Any]:
    """Returns the active alert, automation permission, and escalation policies."""
    report = _runtime_instance.policy_verifier.verify()
    return report.model_dump()


@router.get("/certification")
def get_certification_summary() -> Dict[str, Any]:
    """Executes verifications and returns the official enterprise certification score."""
    verification_results = _runtime_instance.execute_all_verifications()
    cert_report = _runtime_instance.scorer.compute_certification(verification_results)
    return cert_report.model_dump()
