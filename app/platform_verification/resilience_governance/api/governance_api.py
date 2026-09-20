"""
FastAPI REST API Router for Disaster Recovery Governance & Operational Resilience (Part 3G.4).
Exposes endpoints for querying platform resilience scorecard, ownership matrix,
policies, live metrics, risk register, and CI/CD gate evaluation.
"""
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.platform_verification.resilience_governance.runtime.governance_runtime import (
    GovernanceRuntime,
)

router = APIRouter(prefix="/api/v1/governance", tags=["Disaster Recovery Governance & Resilience"])
runtime = GovernanceRuntime(base_dir=".")


@router.get("/status", summary="Get Platform Resilience Governance Status")
def get_governance_status() -> Dict[str, Any]:
    """
    Returns overall governance status, scorecard, and certification verdict.
    """
    result = runtime.execute_governance_verification(export_artifacts=False)
    return {
        "overall_score": result.scorecard.overall_governance_score,
        "maturity_tier": result.maturity_score.maturity_level.value,
        "certification_status": result.scorecard.certification_status,
        "ci_cd_deployment_approved": result.scorecard.ci_cd_deployment_approved,
        "passed": result.passed,
        "scorecard": {
            "ownership_score": result.scorecard.ownership_score,
            "policy_governance_score": result.scorecard.policy_governance_score,
            "change_drift_score": result.scorecard.change_drift_score,
            "maturity_score": result.scorecard.maturity_score,
            "incident_learning_score": result.scorecard.incident_learning_score,
            "audit_readiness_score": result.scorecard.audit_readiness_score,
        },
    }


@router.get("/ownership", summary="Get Recovery Component Ownership Matrix")
def get_ownership_matrix() -> Dict[str, Any]:
    """
    Returns the 42/42 platform components ownership matrix and escalation paths.
    """
    report = runtime.ownership_validator.validate_ownership()
    return {
        "total_components": report.total_components,
        "owned_components": report.owned_components,
        "missing_owner": report.missing_owner,
        "passed": report.passed,
        "components": [
            {
                "name": c.component_name,
                "owner": c.owner_role,
                "team": c.team_name,
                "escalation_tier_1": c.escalation_tier_1,
                "escalation_tier_2": c.escalation_tier_2,
                "runbook": c.runbook_reference,
            }
            for c in report.components
        ],
    }


@router.get("/policies", summary="Get DR Policies Compliance Status")
def get_policies_status() -> Dict[str, Any]:
    """
    Returns status of the 4 enterprise disaster recovery policies.
    """
    report = runtime.policy_manager.validate_policies()
    return {
        "policies_evaluated": report.policies_evaluated,
        "backup_policy_compliant": report.backup_policy_compliant,
        "restore_policy_compliant": report.restore_policy_compliant,
        "incident_policy_compliant": report.incident_policy_compliant,
        "testing_policy_compliant": report.testing_policy_compliant,
        "all_policies_enforced": report.all_policies_enforced,
        "passed": report.passed,
        "details": report.details,
    }


@router.get("/metrics", summary="Get Continuous Resilience Metrics & SLAs")
def get_resilience_metrics() -> Dict[str, Any]:
    """
    Returns RTO, RPO, MTTR, restore success rates, and SLA verdicts.
    """
    report = runtime.metrics_engine.calculate_resilience_metrics()
    return {
        "rto_average_minutes": report.rto_average_minutes,
        "rpo_average_minutes": report.rpo_average_minutes,
        "mttr_average_minutes": report.mttr_average_minutes,
        "restore_success_rate_pct": report.restore_success_rate_pct,
        "open_risks_count": report.open_risks_count,
        "overdue_actions_count": report.overdue_actions_count,
        "health_verdict": report.metrics_health_verdict,
        "passed": report.passed,
        "details": report.details,
    }


@router.get("/risks", summary="Get Resilience Risk Register")
def get_risk_register() -> Dict[str, Any]:
    """
    Returns the 5-category enterprise disaster recovery risk register.
    """
    report = runtime.risk_manager.assess_risk_posture()
    return {
        "total_risks": report.total_risks_cataloged,
        "unmitigated_risks": report.high_critical_risks_unmitigated,
        "passed": report.passed,
        "details": report.details,
        "risks": [
            {
                "risk_id": r.risk_id,
                "category": r.category.value,
                "title": r.title,
                "inherent_level": r.inherent_level.value,
                "residual_level": r.residual_level.value,
                "mitigating_control": r.mitigating_control,
                "control_status": r.control_status,
                "owner": r.owner,
            }
            for r in report.risks
        ],
    }


@router.get("/maturity", summary="Get 6-Tier Resilience Maturity Score")
def get_maturity_score() -> Dict[str, Any]:
    """
    Returns detailed 6-tier resilience maturity evaluation and dimensional breakdown.
    """
    result = runtime.execute_governance_verification(export_artifacts=False)
    return {
        "tier": result.maturity_score.maturity_level.value,
        "level_numeric": result.maturity_score.level_numeric,
        "score": result.maturity_score.maturity_score,
        "dimension_scores": result.maturity_score.dimension_scores,
        "passed": result.maturity_score.passed,
    }


@router.post("/cicd-gate", summary="Evaluate CI/CD Deployment Resilience Gate")
def evaluate_cicd_gate() -> Dict[str, Any]:
    """
    Evaluates CI/CD quality gate and returns deployment approval verdict.
    """
    result = runtime.execute_governance_verification(export_artifacts=False)
    return {
        "deployment_approved": result.cicd_gate_result.deployment_approved,
        "gate_passed": result.cicd_gate_result.gate_passed,
        "blocking_reasons": result.cicd_gate_result.blocking_reasons,
        "warnings": result.cicd_gate_result.warnings,
        "quality_score": result.cicd_gate_result.quality_score,
        "details": result.cicd_gate_result.details,
    }
