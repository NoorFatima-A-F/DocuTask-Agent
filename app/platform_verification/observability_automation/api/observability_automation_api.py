"""
Phase 3I.8: Observability Automation & Autonomous Operations REST API Router
Provides endpoints for triggering autonomous operations verification, querying remediation workflows, and inspecting root cause hypotheses.
"""
from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any

from ..runtime.observability_automation_runtime import ObservabilityAutomationRuntime

router = APIRouter(
    prefix="/api/v1/observability-automation",
    tags=["Observability Automation, Self-Healing Operations & Autonomous Reliability"],
)

_runtime = ObservabilityAutomationRuntime()


@router.post("/run-verification", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def trigger_observability_automation_verification() -> Dict[str, Any]:
    """Execute complete Phase 3I.8 Autonomous Operations & Reliability Verification suite."""
    try:
        results = _runtime.run_full_verification()
        return results
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Observability automation verification failed: {str(exc)}",
        )


@router.get("/status", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def get_autonomous_certification_status() -> Dict[str, Any]:
    """Retrieve current autonomous operations certification status and 6-pillar score."""
    arch = _runtime.arch_verifier.verify_architecture()
    anomaly = _runtime.anomaly_verifier.verify_anomaly_detection()
    corr = _runtime.corr_verifier.verify_event_correlation()
    rca = _runtime.rca_verifier.verify_root_cause_analysis()
    remediation = _runtime.remediation_verifier.verify_automated_remediation()
    safety = _runtime.safety_verifier.verify_safety_controls()
    healing = _runtime.healing_verifier.verify_self_healing_workflows()
    incident = _runtime.incident_verifier.verify_incident_automation()
    learning = _runtime.learning_verifier.verify_reliability_learning()
    testing = _runtime.testing_verifier.verify_autonomous_testing()
    human = _runtime.human_verifier.verify_human_control_policies()
    dash = _runtime.dash_verifier.verify_autonomous_dashboards()

    cert = _runtime.scorer.calculate_certification_score(
        arch_report=arch,
        anomaly_report=anomaly,
        corr_report=corr,
        rca_report=rca,
        remediation_report=remediation,
        safety_report=safety,
        healing_report=healing,
        incident_report=incident,
        learning_report=learning,
        testing_report=testing,
        human_report=human,
        dash_report=dash,
    )

    return {
        "certification_tier": cert.certification_tier.value,
        "overall_score_pct": cert.overall_score_pct,
        "certification_granted": cert.certification_granted,
        "evaluated_at": cert.evaluated_at,
        "pillar_scores": [p.model_dump(mode="json") for p in cert.pillar_scores],
    }


@router.get("/remediations", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def get_remediation_status() -> Dict[str, Any]:
    """Retrieve automated remediation actions, safety guardrails, and self-healing validation metrics."""
    remediation = _runtime.remediation_verifier.verify_automated_remediation()
    safety = _runtime.safety_verifier.verify_safety_controls()
    healing = _runtime.healing_verifier.verify_self_healing_workflows()

    return {
        "remediations": remediation.model_dump(mode="json"),
        "safety_guardrails": safety.model_dump(mode="json"),
        "self_healing_loops": healing.model_dump(mode="json"),
    }


@router.get("/root-cause-analysis", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def get_root_cause_analysis() -> Dict[str, Any]:
    """Retrieve AI-assisted root cause hypotheses, multi-signal correlations, and learning lessons."""
    rca = _runtime.rca_verifier.verify_root_cause_analysis()
    corr = _runtime.corr_verifier.verify_event_correlation()
    learning = _runtime.learning_verifier.verify_reliability_learning()

    return {
        "root_cause_analysis": rca.model_dump(mode="json"),
        "event_correlation": corr.model_dump(mode="json"),
        "reliability_learning": learning.model_dump(mode="json"),
    }
