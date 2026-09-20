"""
Phase 3H.5.11: Health Quality & Certification API Router
"""
from fastapi import APIRouter
from ..runtime.health_quality_runtime import HealthQualityRuntime

router = APIRouter(
    prefix="/health-quality-certification",
    tags=["Phase 3H.5.11 - Health Quality Scoring & Operational Certification"],
)
runtime = HealthQualityRuntime()


@router.get("/status")
def get_health_certification_status():
    return {
        "status": "ACTIVE",
        "phase": "3H.5.11",
        "capability": "Enterprise Health Quality Scoring & Operational Certification Framework",
    }


@router.post("/verify")
def run_health_quality_certification():
    results = runtime.run_full_certification()
    scorecard = results["scorecard"]
    return {
        "verification_id": scorecard.verification_id,
        "overall_score": scorecard.overall_score,
        "maturity_level": scorecard.maturity_level.value,
        "certification_status": scorecard.certification_status.value,
        "passed": scorecard.passed,
        "deployment_decision": scorecard.deployment_gate.decision.value,
        "total_manifests_exported": len(results["exported_files"]),
    }


@router.get("/gate")
def check_production_deployment_gate():
    results = runtime.run_full_certification()
    gate = results["deployment_gate"]
    return {
        "decision": gate.decision.value,
        "actual_score": gate.actual_score,
        "minimum_score_required": gate.minimum_score_required,
        "critical_requirements_met": gate.critical_requirements_met,
        "reason": gate.reason,
    }
