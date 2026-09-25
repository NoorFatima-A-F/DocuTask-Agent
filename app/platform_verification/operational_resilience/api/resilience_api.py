"""
FastAPI REST API Router for Operational Resilience & Recovery Automation (Part 3G.5).
Exposes endpoints for querying resilience scorecard, failure experiments, self-healing status,
incident lifecycle automation, executable runbooks, DR drills, and CI/CD quality gate evaluation.
"""
from typing import Dict, Any
from fastapi import APIRouter

from app.platform_verification.operational_resilience.runtime.resilience_runtime import (
    ResilienceRuntime,
)

router = APIRouter(prefix="/api/v1/resilience", tags=["Operational Resilience & Recovery Automation"])
runtime = ResilienceRuntime(base_dir=".")


@router.get("/status", summary="Get Operational Resilience Status & Scorecard")
def get_resilience_status() -> Dict[str, Any]:
    """
    Returns overall operational resilience scorecard, tier, and certification verdict.
    """
    result = runtime.execute_resilience_verification(export_artifacts=False)
    return {
        "overall_resilience_score": result.scorecard.overall_resilience_score,
        "resilience_tier": result.scorecard.resilience_tier.value,
        "certification_verdict": result.scorecard.certification_verdict,
        "ci_cd_deployment_approved": result.scorecard.ci_cd_deployment_approved,
        "passed": result.passed,
        "category_scores": {
            "detection_score": result.scorecard.detection_score,
            "recovery_automation_score": result.scorecard.recovery_automation_score,
            "data_integrity_score": result.scorecard.data_integrity_score,
            "failure_containment_score": result.scorecard.failure_containment_score,
            "operational_visibility_score": result.scorecard.operational_visibility_score,
            "documentation_score": result.scorecard.documentation_score,
        },
    }


@router.get("/experiments", summary="Get Failure Injection Experiments Results")
def get_failure_experiments() -> Dict[str, Any]:
    """
    Returns results of all simulated failure experiments across 6 enterprise domains.
    """
    experiments = runtime.failure_injector.run_all_failure_experiments()
    return {
        "total_experiments": len(experiments),
        "passed_count": sum(1 for e in experiments if e.status == "PASS"),
        "experiments": [
            {
                "id": e.experiment_id,
                "category": e.category.value,
                "target": e.target_component,
                "description": e.failure_description,
                "detection_sec": e.detection_time_seconds,
                "recovery_sec": e.recovery_duration_seconds,
                "data_loss": e.data_loss,
                "status": e.status,
            }
            for e in experiments
        ],
    }


@router.get("/self-healing", summary="Get Self-Healing System Metrics")
def get_self_healing_status() -> Dict[str, Any]:
    """
    Returns container, queue, and database connection pool self-healing status.
    """
    report = runtime.self_healing_engine.verify_self_healing()
    return {
        "container_healing_passed": report.container_healing_passed,
        "container_restart_sec": report.container_restart_time_sec,
        "queue_healing_passed": report.queue_healing_passed,
        "queue_preserved_pct": report.queue_messages_preserved_pct,
        "db_recovery_passed": report.db_connection_recovery_passed,
        "mttd_seconds": report.mttd_seconds,
        "mttr_seconds": report.mttr_seconds,
        "recovery_success_rate_pct": report.recovery_success_rate_pct,
        "passed": report.passed,
        "details": report.details,
    }


@router.get("/incidents", summary="Get Incident Automation & Alerting")
def get_incident_automation() -> Dict[str, Any]:
    """
    Returns automated incident lifecycle, routing, and postmortem generation status.
    """
    report = runtime.incident_engine.verify_incident_automation()
    return {
        "total_incidents": report.total_incidents_simulated,
        "average_mttd_sec": report.average_mttd_seconds,
        "average_mttr_sec": report.average_mttr_seconds,
        "paged_oncall_verified": report.paged_oncall_verified,
        "passed": report.passed,
        "incidents": [
            {
                "id": t.incident_id,
                "severity": t.severity.value,
                "title": t.title,
                "component": t.component,
                "owner": t.assigned_owner,
                "status": t.status,
            }
            for t in report.incidents
        ],
    }


@router.get("/runbooks", summary="Get Validated Executable Runbooks")
def get_runbooks() -> Dict[str, Any]:
    """
    Returns all 6 validated runbooks and automated CLI execution commands.
    """
    report = runtime.runbook_engine.validate_runbooks()
    return {
        "total_runbooks": report.total_runbooks,
        "automated_count": report.automated_runbooks_count,
        "passed": report.passed,
        "runbooks": [
            {
                "id": r.runbook_id,
                "title": r.title,
                "file": r.file_path,
                "automated_cli": r.automated_cli_supported,
            }
            for r in report.runbooks
        ],
    }


@router.post("/drills/run", summary="Trigger Automated Resilience Drill")
def trigger_resilience_drill() -> Dict[str, Any]:
    """
    Executes an automated resilience drill and returns drill score and recovery latency.
    """
    drill = runtime.drill_scheduler.execute_resilience_drill(0)
    return {
        "drill_id": drill.drill_id,
        "drill_name": drill.drill_name,
        "injected_failure": drill.injected_failure,
        "rto_seconds": drill.rto_seconds,
        "data_loss_bytes": drill.data_loss_bytes,
        "drill_score": drill.drill_score,
        "passed": drill.passed,
        "details": drill.details,
    }


@router.post("/cicd-gate", summary="Evaluate CI/CD Resilience Quality Gate")
def evaluate_cicd_gate() -> Dict[str, Any]:
    """
    Evaluates CI/CD quality gate and returns deployment approval verdict.
    """
    result = runtime.execute_resilience_verification(export_artifacts=False)
    return {
        "deployment_approved": result.scorecard.ci_cd_deployment_approved,
        "resilience_tier": result.scorecard.resilience_tier.value,
        "overall_score": result.scorecard.overall_resilience_score,
        "gate_passed": result.passed,
        "certification_verdict": result.scorecard.certification_verdict,
    }
