"""
Phase 3H.6: Service Level Objectives & Reliability API Router
"""
from fastapi import APIRouter
from ..runtime.service_reliability_runtime import ServiceReliabilityRuntime

router = APIRouter(
    prefix="/service-reliability-verification",
    tags=["Phase 3H.6 - Service Level Objectives, Error Budgets & Reliability Compliance"],
)
runtime = ServiceReliabilityRuntime()


@router.get("/status")
def get_reliability_status():
    return {
        "status": "ACTIVE",
        "phase": "3H.6",
        "capability": "Enterprise Service Level Objectives (SLO), Error Budgets & Reliability Compliance",
    }


@router.post("/verify")
def run_reliability_verification():
    results = runtime.run_full_reliability_verification()
    scorecard = results["scorecard"]
    return {
        "verification_id": scorecard.verification_id,
        "overall_reliability_score": scorecard.overall_reliability_score,
        "certification_tier": scorecard.certification_tier.value,
        "passed": scorecard.passed,
        "measured_availability_pct": scorecard.overall_availability_pct,
        "remaining_error_budget_pct": scorecard.overall_error_budget_remaining_pct,
        "deployment_decision": scorecard.deployment_gate_decision.value,
        "total_manifests_exported": len(results["exported_files"]),
    }


@router.get("/slo")
def get_slo_architecture():
    results = runtime.run_full_reliability_verification()
    return results["slo_report"].model_dump()


@router.get("/gate")
def get_deployment_gate_status():
    results = runtime.run_full_reliability_verification()
    return results["gate_report"].model_dump()
