"""
Phase 3H.5.7: Reliability Intelligence API Router
"""
from fastapi import APIRouter
from ..runtime.reliability_intelligence_runtime import ReliabilityIntelligenceRuntime

router = APIRouter(prefix="/reliability-intelligence", tags=["Phase 3H.5.7 - Reliability Intelligence & Health Scoring"])
runtime = ReliabilityIntelligenceRuntime()


@router.get("/health-score")
def get_reliability_health_score():
    results = runtime.run_full_reliability_verification()
    return {
        "overall_health_score": results["overall_health_score"],
        "composite_score": results["composite_score"],
        "tier": results["tier"],
        "certified": results["certified"],
        "total_manifests_exported": len(results["exported_files"]),
    }
