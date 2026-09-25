"""
Phase 3H.8: Operational Governance Verification FastAPI Endpoints
"""
from fastapi import APIRouter, Query
from typing import Dict, Any

from app.platform_verification.operational_governance.runtime.operational_governance_runtime import OperationalGovernanceRuntime

router = APIRouter(
    prefix="/api/v1/platform-verification/operational-governance",
    tags=["Phase 3H.8: Operational Governance Verification"],
)

_runtime = OperationalGovernanceRuntime()


@router.post("/verify", summary="Execute Full Operational Governance Verification")
async def run_governance_verification(export_evidence: bool = Query(True, description="Whether to export verification reports to disk")) -> Dict[str, Any]:
    result = _runtime.run_full_verification(export_evidence=export_evidence)
    return {
        "status": "SUCCESS",
        "scorecard": result["scorecard"].model_dump(),
        "summary": {
            "tier": result["scorecard"].certification_tier.value,
            "overall_score": result["scorecard"].overall_governance_score,
            "passed": result["scorecard"].passed,
            "reports_exported": bool(result["export_metadata"]),
        },
    }


@router.get("/scorecard", summary="Get Latest Governance Scorecard")
async def get_governance_scorecard() -> Dict[str, Any]:
    result = _runtime.run_full_verification(export_evidence=False)
    return {
        "scorecard": result["scorecard"].model_dump(),
    }


@router.get("/changes", summary="Get Evaluated Operational Changes")
async def get_operational_changes() -> Dict[str, Any]:
    report = _runtime.change_verifier.verify_change_governance()
    return report.model_dump()


@router.get("/deployments", summary="Get Deployment Safety & Progressive Rollout Status")
async def get_deployments() -> Dict[str, Any]:
    report = _runtime.deploy_verifier.verify_deployment_safety()
    return report.model_dump()


@router.get("/audit-trail", summary="Get Immutable Operational Audit Trail")
async def get_audit_trail() -> Dict[str, Any]:
    report = _runtime.audit_verifier.verify_audit_trails()
    return report.model_dump()


@router.get("/dashboard", summary="Get Operational Governance Dashboard")
async def get_governance_dashboard() -> Dict[str, Any]:
    report = _runtime.dashboard_verifier.generate_governance_dashboard()
    return report.model_dump()


@router.get("/health", summary="Governance Verification Engine Health")
async def get_engine_health() -> Dict[str, Any]:
    return {
        "status": "HEALTHY",
        "framework": "DocuTask Agent Platform Verification (Phase 3H.8)",
        "engine": "Operational Governance Verification Engine",
        "ready": True,
    }
