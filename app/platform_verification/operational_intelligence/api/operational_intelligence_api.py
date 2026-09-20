"""
Phase 3H.9: Operational Intelligence Verification FastAPI Endpoints
"""
from fastapi import APIRouter, Query
from typing import Dict, Any, Optional

from app.platform_verification.operational_intelligence.runtime.operational_intelligence_runtime import OperationalIntelligenceRuntime

router = APIRouter(
    prefix="/api/v1/platform-verification/operational-intelligence",
    tags=["Phase 3H.9: Operational Intelligence Verification"],
)

_runtime = OperationalIntelligenceRuntime()


@router.post("/verify", summary="Execute Full Operational Intelligence Verification")
async def run_intelligence_verification(export_evidence: bool = Query(True, description="Whether to export verification reports to disk")) -> Dict[str, Any]:
    result = _runtime.run_full_verification(export_evidence=export_evidence)
    return {
        "status": "SUCCESS",
        "scorecard": result["scorecard"].model_dump(),
        "summary": {
            "tier": result["scorecard"].certification_tier.value,
            "overall_score": result["scorecard"].overall_intelligence_score,
            "passed": result["scorecard"].passed,
            "reports_exported": bool(result["export_metadata"]),
        },
    }


@router.get("/scorecard", summary="Get Latest Intelligence Scorecard")
async def get_intelligence_scorecard() -> Dict[str, Any]:
    result = _runtime.run_full_verification(export_evidence=False)
    return {
        "scorecard": result["scorecard"].model_dump(),
    }


@router.get("/anomalies", summary="Get Detected Operational Anomalies")
async def get_anomalies() -> Dict[str, Any]:
    report = _runtime.anomaly_verifier.verify_anomaly_detection()
    return report.model_dump()


@router.get("/forecasts", summary="Get Multi-Horizon Capacity Forecasts")
async def get_capacity_forecasts() -> Dict[str, Any]:
    report = _runtime.forecast_verifier.verify_capacity_forecasting()
    return report.model_dump()


@router.get("/recommendations", summary="Get Operational Optimization Recommendations")
async def get_recommendations() -> Dict[str, Any]:
    report = _runtime.recom_verifier.verify_recommendation_engine()
    return report.model_dump()


@router.get("/decisions", summary="Get Operational Decision Support Inquiries")
async def get_decision_support() -> Dict[str, Any]:
    report = _runtime.decision_verifier.verify_decision_support()
    return report.model_dump()


@router.get("/dashboard", summary="Get Executive Operational Dashboard")
async def get_executive_dashboard() -> Dict[str, Any]:
    report = _runtime.dash_verifier.generate_executive_dashboard()
    return report.model_dump()


@router.get("/health", summary="Operational Intelligence Verification Engine Health")
async def get_engine_health() -> Dict[str, Any]:
    return {
        "status": "HEALTHY",
        "framework": "DocuTask Agent Platform Verification (Phase 3H.9)",
        "engine": "Operational Intelligence Verification Engine",
        "ready": True,
    }
