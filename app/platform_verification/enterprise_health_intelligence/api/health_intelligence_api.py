"""
Phase 3H.5: Enterprise Health Intelligence API Router
"""
from fastapi import APIRouter
from ..runtime.health_intelligence_runtime import HealthIntelligenceRuntime

router = APIRouter(prefix="/health-intelligence", tags=["Phase 3H.5 - Health Intelligence & Remediation"])
runtime = HealthIntelligenceRuntime()


@router.get("/status")
def get_health_intelligence_status():
    return {"status": "ACTIVE", "phase": "3H.5", "capability": "Health Intelligence & Automated Remediation"}


@router.post("/verify")
def run_health_intelligence_verification():
    results = runtime.run_full_verification()
    return {
        "composite_score": results["composite_score"],
        "tier": results["tier"],
        "certified": results["certified"],
        "total_manifests_exported": len(results["exported_files"]),
    }
