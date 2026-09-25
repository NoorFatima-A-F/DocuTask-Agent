"""
Phase 3I.6: Observability Governance, SLO Engineering & Reliability Certification API Router
Provides REST endpoints for querying SLOs, error budgets, certification status, and triggering verification runs.
"""
from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any

from ..runtime.reliability_governance_runtime import ReliabilityGovernanceRuntime

router = APIRouter(
    prefix="/api/v1/reliability-governance",
    tags=["Observability Governance & Reliability Certification"],
)

_runtime = ReliabilityGovernanceRuntime()


@router.post("/run-verification", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def trigger_reliability_governance_verification() -> Dict[str, Any]:
    """Execute complete Phase 3I.6 Observability Governance & Reliability Certification run."""
    try:
        results = _runtime.run_full_verification()
        return results
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Reliability governance verification failed: {str(exc)}",
        )


@router.get("/status", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def get_certification_status() -> Dict[str, Any]:
    """Retrieve current reliability governance & certification status."""
    gov = _runtime.gov_verifier.verify_governance_architecture()
    slis = _runtime.sli_verifier.verify_slis()
    slos = _runtime.slo_verifier.verify_slos()
    budgets = _runtime.budget_verifier.verify_error_budgets()
    dashboards = _runtime.dash_verifier.verify_reliability_dashboards()
    trends = _runtime.trend_verifier.verify_reliability_trends()
    gates = _runtime.gate_verifier.verify_production_gates()
    regression = _runtime.reg_verifier.verify_reliability_regression()
    quality = _runtime.qual_verifier.verify_telemetry_quality()
    automation = _runtime.auto_verifier.verify_reliability_automation()

    cert = _runtime.scorer.calculate_certification_score(
        gov_report=gov,
        sli_report=slis,
        slo_report=slos,
        budget_report=budgets,
        dash_report=dashboards,
        trend_report=trends,
        gate_report=gates,
        reg_report=regression,
        qual_report=quality,
        auto_report=automation,
    )

    return {
        "certification_tier": cert.certification_tier.value,
        "overall_score_pct": cert.overall_score_pct,
        "certification_granted": cert.certification_granted,
        "evaluated_at": cert.evaluated_at,
        "pillar_scores": [p.model_dump(mode="json") for p in cert.pillar_scores],
    }


@router.get("/error-budgets", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def get_error_budgets() -> Dict[str, Any]:
    """Retrieve error budgets and burn rates across all platform services."""
    budget_report = _runtime.budget_verifier.verify_error_budgets()
    return budget_report.model_dump(mode="json")


@router.get("/slos", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def get_slos() -> Dict[str, Any]:
    """Retrieve all SLI/SLO definitions, quantitative targets, and 30-day compliance."""
    slo_report = _runtime.slo_verifier.verify_slos()
    return slo_report.model_dump(mode="json")
