"""
Phase 3H.5.10: Health Security Verification API Router
"""
from fastapi import APIRouter
from ..runtime.health_security_runtime import HealthSecurityRuntime

router = APIRouter(
    prefix="/health-security-verification",
    tags=["Phase 3H.5.10 - Health Security, Privacy & Information Exposure Verification"],
)
runtime = HealthSecurityRuntime()


@router.get("/status")
def get_health_security_status():
    return {
        "status": "ACTIVE",
        "phase": "3H.5.10",
        "capability": "Enterprise Health Security, Privacy & Information Exposure Verification",
    }


@router.post("/verify")
def run_health_security_verification():
    results = runtime.run_full_verification()
    scorecard = results["scorecard"]
    return {
        "verification_id": scorecard.verification_id,
        "overall_health_security_score": scorecard.overall_health_security_score,
        "certification_tier": scorecard.certification_tier.value,
        "passed": scorecard.passed,
        "zero_critical_vulnerabilities": scorecard.zero_critical_vulnerabilities,
        "total_audits_performed": scorecard.total_audits_performed,
        "total_manifests_exported": len(results["exported_files"]),
    }
