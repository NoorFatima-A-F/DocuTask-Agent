"""
Health Intelligence API Router.
Exposes FastAPI endpoints for health verification execution, state timeline, alerts, and degradation status.
"""
from fastapi import APIRouter, Response, status
from typing import Dict, Any, List
from dataclasses import asdict

from app.platform_verification.health_transition_intelligence.runtime.health_intelligence_runtime import HealthIntelligenceRuntime

router = APIRouter(prefix="/verification/health-intelligence", tags=["Health Intelligence"])
runtime = HealthIntelligenceRuntime()


@router.get("/verify")
def run_health_intelligence_verification() -> Dict[str, Any]:
    """
    Triggers end-to-end verification across all 15 parts of Phase 3H.3.3.
    """
    results = runtime.execute_full_verification()
    scorecard = results["scorecard"]
    return {
        "status": "COMPLETED",
        "overall_score": scorecard.overall_score,
        "certification_tier": scorecard.certification_tier.value,
        "certification_verdict": scorecard.certification_verdict,
        "passed": scorecard.passed,
        "scores": {
            "state_accuracy": scorecard.state_accuracy_score,
            "transition_logic": scorecard.transition_logic_score,
            "failure_detection": scorecard.failure_detection_score,
            "recovery_validation": scorecard.recovery_validation_score,
            "alerting": scorecard.alerting_score,
            "evidence_quality": scorecard.evidence_quality_score,
        },
        "exported_files": results["exported_files"],
    }


@router.get("/timeline")
def get_incident_timeline() -> Dict[str, Any]:
    """
    Returns the latest reconstructed incident timeline.
    """
    events = runtime.history_storage.get_all_events()
    timeline = runtime.incident_reconstructor.reconstruct_timeline(events=events)
    return asdict(timeline)


@router.get("/alerts")
def get_active_alerts() -> Dict[str, Any]:
    """
    Returns generated alerts in Prometheus AlertManager format.
    """
    events = runtime.history_storage.get_all_events()
    alerts = runtime.alerting_engine.evaluate_events(events)
    return asdict(alerts)


@router.get("/events")
def get_health_events() -> List[Dict[str, Any]]:
    """
    Returns recorded health state transition events.
    """
    events = runtime.history_storage.get_all_events()
    return [asdict(e) for e in events]
