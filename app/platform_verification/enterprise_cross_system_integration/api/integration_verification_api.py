"""FastAPI REST Endpoints for Enterprise Cross-System Integration."""

from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException, Query
from ..domain.models import CrossSystemIntegrationQualityReport, CrossSystemIntegrationQualityScore
from ..runtime.integration_verification_runtime import CrossSystemIntegrationVerificationRuntime

router = APIRouter(prefix="/api/v1/verification/cross-system-integration", tags=["Cross-System Integration Verification"])

# Singleton runtime instance
_runtime = CrossSystemIntegrationVerificationRuntime()
_latest_report: Optional[CrossSystemIntegrationQualityReport] = None


@router.get("/health", summary="Check verification subsystem health")
def get_health() -> Dict[str, Any]:
    return {
        "status": "HEALTHY",
        "phase": "Phase 4 - Enterprise Cross-System Integration & End-to-End Platform Validation",
        "verifiers_count": len(_runtime.verifiers),
    }


@router.post("/run", response_model=CrossSystemIntegrationQualityReport, summary="Execute complete integration verification suite")
def run_verification(output_dir: Optional[str] = Query(None, description="Custom evidence output directory")) -> CrossSystemIntegrationQualityReport:
    global _latest_report
    _latest_report = _runtime.execute_all(output_dir=output_dir)
    return _latest_report


@router.get("/score", response_model=CrossSystemIntegrationQualityScore, summary="Get latest integration certification score")
def get_latest_score() -> CrossSystemIntegrationQualityScore:
    global _latest_report
    if not _latest_report:
        _latest_report = _runtime.execute_all()
    return _latest_report.score


@router.get("/report", response_model=CrossSystemIntegrationQualityReport, summary="Get latest full integration quality report")
def get_latest_report() -> CrossSystemIntegrationQualityReport:
    global _latest_report
    if not _latest_report:
        _latest_report = _runtime.execute_all()
    return _latest_report


@router.get("/subsystem/{subsystem_key}", summary="Get specific subsystem verification report")
def get_subsystem_report(subsystem_key: str) -> Dict[str, Any]:
    global _latest_report
    if not _latest_report:
        _latest_report = _runtime.execute_all()
    if subsystem_key not in _latest_report.reports:
        raise HTTPException(status_code=404, detail=f"Subsystem verification '{subsystem_key}' not found.")
    rep = _latest_report.reports[subsystem_key]
    return rep.model_dump() if hasattr(rep, "model_dump") else rep
