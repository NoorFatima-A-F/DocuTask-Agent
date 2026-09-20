"""
Phase 3H.5.12: Automated Health Recovery API Router
"""
from fastapi import APIRouter
from ..runtime.health_recovery_runtime import HealthRecoveryRuntime

router = APIRouter(
    prefix="/health-recovery-verification",
    tags=["Phase 3H.5.12 - Automated Health Recovery Verification"],
)
runtime = HealthRecoveryRuntime()


@router.get("/status")
def get_health_recovery_status():
    return {
        "status": "ACTIVE",
        "phase": "3H.5.12",
        "capability": "Automated Health Recovery Verification Framework",
    }


@router.post("/verify")
def run_health_recovery_verification():
    results = runtime.run_full_recovery_verification()
    scorecard = results["scorecard"]
    return {
        "verification_id": scorecard.verification_id,
        "overall_recovery_score": scorecard.overall_recovery_score,
        "certification_tier": scorecard.certification_tier.value,
        "passed": scorecard.passed,
        "mttr_seconds": scorecard.mttr_seconds,
        "mttd_seconds": scorecard.mttd_seconds,
        "recovery_success_rate": scorecard.recovery_success_rate,
        "total_manifests_exported": len(results["exported_files"]),
    }
