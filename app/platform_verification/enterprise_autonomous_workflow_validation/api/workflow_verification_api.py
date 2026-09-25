"""FastAPI REST Endpoints for Enterprise Autonomous Workflow Validation."""

from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException, Query
from ..domain.models import AutonomousWorkflowQualityReport, AutonomousWorkflowQualityScore
from ..runtime.workflow_verification_runtime import AutonomousWorkflowVerificationRuntime

router = APIRouter(prefix="/api/v1/verification/autonomous-workflows", tags=["Autonomous Workflow Validation"])

_runtime = AutonomousWorkflowVerificationRuntime()
_latest_report: Optional[AutonomousWorkflowQualityReport] = None


@router.get("/health", summary="Check workflow verification subsystem health")
def get_health() -> Dict[str, Any]:
    return {
        "status": "HEALTHY",
        "phase": "Phase 5 - Enterprise End-to-End Autonomous Workflow & Business Process Validation",
        "verifiers_count": len(_runtime.verifiers),
    }


@router.post("/run", response_model=AutonomousWorkflowQualityReport, summary="Execute complete autonomous workflow verification suite")
def run_verification() -> AutonomousWorkflowQualityReport:
    global _latest_report
    _latest_report = _runtime.execute_all()
    return _latest_report


@router.get("/score", response_model=AutonomousWorkflowQualityScore, summary="Get latest business workflow certification score")
def get_latest_score() -> AutonomousWorkflowQualityScore:
    global _latest_report
    if not _latest_report:
        _latest_report = _runtime.execute_all()
    return _latest_report.score


@router.get("/report", response_model=AutonomousWorkflowQualityReport, summary="Get latest full workflow quality report")
def get_latest_report() -> AutonomousWorkflowQualityReport:
    global _latest_report
    if not _latest_report:
        _latest_report = _runtime.execute_all()
    return _latest_report


@router.get("/subsystem/{subsystem_key}", summary="Get specific business workflow verification report")
def get_subsystem_report(subsystem_key: str) -> Dict[str, Any]:
    global _latest_report
    if not _latest_report:
        _latest_report = _runtime.execute_all()
    if subsystem_key not in _latest_report.reports:
        raise HTTPException(status_code=404, detail=f"Business workflow verification '{subsystem_key}' not found.")
    rep = _latest_report.reports[subsystem_key]
    return rep.model_dump() if hasattr(rep, "model_dump") else rep
