"""Incident Automation API Endpoints.

FastAPI router exposing incident response automation and self-healing verification status.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, Optional

from fastapi import APIRouter, status

from app.platform_verification.incident_response_automation.runtime.incident_automation_runtime import (
    IncidentAutomationRuntime,
)

router = APIRouter(prefix="/incident/automation", tags=["Incident Response Automation"])

# Shared runtime instance
_runtime_instance: Optional[IncidentAutomationRuntime] = None


def get_runtime() -> IncidentAutomationRuntime:
    global _runtime_instance
    if _runtime_instance is None:
        _runtime_instance = IncidentAutomationRuntime()
    return _runtime_instance


@router.get("/summary", summary="Get Incident Automation Scorecard & Summary")
async def get_summary() -> Dict[str, Any]:
    """Returns the comprehensive incident automation scorecard and verification status."""
    runtime = get_runtime()
    results = runtime.run_full_verification()
    scorecard = results["scorecard"]
    return {
        "status": "success",
        "overall_score": scorecard.overall_score,
        "certification_tier": scorecard.certification_tier.value,
        "certification_verdict": scorecard.certification_verdict,
        "passed": scorecard.passed,
        "dimension_scores": {
            "detection_accuracy": scorecard.detection_accuracy_score,
            "recovery_automation": scorecard.recovery_automation_score,
            "safety_controls": scorecard.safety_controls_score,
            "incident_diagnosis": scorecard.incident_diagnosis_score,
            "operational_learning": scorecard.operational_learning_score,
            "security": scorecard.security_score,
        },
    }


@router.get("/architecture", summary="Get Incident Architecture Report")
async def get_architecture() -> Dict[str, Any]:
    """Returns the subsystem separation and architecture audit report."""
    runtime = get_runtime()
    report = runtime.arch_verifier.verify_architecture()
    return {"status": "success", "data": asdict(report)}


@router.get("/detection", summary="Get Automated Incident Detection Report")
async def get_detection() -> Dict[str, Any]:
    """Returns detected signals, detection latency, and precision/recall benchmarks."""
    runtime = get_runtime()
    report = runtime.detector.detect_incidents()
    return {"status": "success", "data": asdict(report)}


@router.get("/classification", summary="Get Incident Classification Report")
async def get_classification() -> Dict[str, Any]:
    """Returns categorized incidents across SEV-1 to SEV-4 and business impact."""
    runtime = get_runtime()
    report = runtime.classifier.classify_incidents()
    return {"status": "success", "data": asdict(report)}


@router.get("/runbooks", summary="Get Runbook Execution & Audit Report")
async def get_runbooks() -> Dict[str, Any]:
    """Returns step-by-step execution results for declarative remediation runbooks."""
    runtime = get_runtime()
    report = runtime.runbook_engine.execute_runbook("restart_worker.yaml")
    return {"status": "success", "data": asdict(report)}


@router.get("/self-healing", summary="Get Self-Healing Execution Report")
async def get_self_healing() -> Dict[str, Any]:
    """Returns self-healing test results, MTTR measurements, and zero-task-loss validation."""
    runtime = get_runtime()
    report = runtime.healing_engine.execute_self_healing_tests()
    return {"status": "success", "data": asdict(report)}


@router.get("/recovery-policies", summary="Get Recovery Safety Policy Report")
async def get_recovery_policies() -> Dict[str, Any]:
    """Returns safety policy rules, auto-execution gates, and blocked destructive actions."""
    runtime = get_runtime()
    report = runtime.policy_engine.evaluate_recovery_policies()
    return {"status": "success", "data": asdict(report)}


@router.get("/correlation", summary="Get Cross-Signal Incident Correlation Report")
async def get_correlation() -> Dict[str, Any]:
    """Returns causal graph nodes isolating primary root causes from symptoms."""
    runtime = get_runtime()
    report = runtime.correlation_engine.correlate_incident()
    return {"status": "success", "data": asdict(report)}


@router.get("/knowledge", summary="Get Operational Knowledge Base Report")
async def get_knowledge() -> Dict[str, Any]:
    """Returns indexed incident patterns, root causes, and recommended solutions."""
    runtime = get_runtime()
    report = runtime.knowledge_base.get_knowledge_report()
    return {"status": "success", "data": asdict(report)}


@router.get("/postmortem", summary="Get Automated Postmortem Report")
async def get_postmortem() -> Dict[str, Any]:
    """Returns blameless postmortem report with timeline and MTTD/MTTR metrics."""
    runtime = get_runtime()
    report = runtime.postmortem_gen.generate_postmortem()
    return {"status": "success", "data": asdict(report)}


@router.get("/security", summary="Get Automation Security Audit Report")
async def get_security() -> Dict[str, Any]:
    """Returns security audit checks confirming tamper-proof audit trails and RBAC."""
    runtime = get_runtime()
    report = runtime.security_auditor.audit_security()
    return {"status": "success", "data": asdict(report)}


@router.post("/run", status_code=status.HTTP_200_OK, summary="Execute Full Verification Cycle")
async def run_verification() -> Dict[str, Any]:
    """Triggers an end-to-end incident automation verification run and exports evidence."""
    runtime = get_runtime()
    results = runtime.run_full_verification()
    scorecard = results["scorecard"]
    return {
        "status": "completed",
        "overall_score": scorecard.overall_score,
        "certification_tier": scorecard.certification_tier.value,
        "certification_verdict": scorecard.certification_verdict,
        "passed": scorecard.passed,
        "manifests_generated": [str(p) for p in results["manifest_files"].values()],
    }
