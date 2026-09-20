"""FastAPI Router for Autonomous Health Remediation & Recovery Verification.

Exposes REST endpoints for remediation policies, execution tracking, validation proofs,
rollback history, chaos scenario tests, metrics, security audits, scorecard, and full execution.
"""

from fastapi import APIRouter
from typing import Dict, Any
import json

from ..runtime.autonomous_remediation_runtime import AutonomousRemediationRuntime
from ..exporter.remediation_evidence_exporter import EnhancedJSONEncoder
from ..domain.models import FailureContext

router = APIRouter(prefix="/health/remediation", tags=["Autonomous Health Remediation"])
_runtime = AutonomousRemediationRuntime()


def _to_dict(obj: Any) -> Any:
    return json.loads(json.dumps(obj, cls=EnhancedJSONEncoder))


@router.get("/policies", summary="Get Registered Remediation Policies & Action Levels")
def get_policies() -> Dict[str, Any]:
    return _to_dict(_runtime.policy_engine.get_policy_report())


@router.get("/executions", summary="Get Remediation Execution History & Before/After States")
def get_executions() -> Dict[str, Any]:
    return _to_dict(_runtime.executor.get_execution_report())


@router.get("/validations", summary="Get Post-Remediation Health Restoration Validations")
def get_validations() -> Dict[str, Any]:
    return _to_dict(_runtime.validator.get_validation_report())


@router.get("/rollbacks", summary="Get Rollback Operations & Failure Escalation Records")
def get_rollbacks() -> Dict[str, Any]:
    return _to_dict(_runtime.rollback_mgr.get_rollback_report())


@router.get("/scenarios", summary="Get 5 Real-World Self-Healing Chaos Scenario Results")
def get_scenarios() -> Dict[str, Any]:
    return _to_dict(_runtime.scenarios_verifier.verify_scenarios())


@router.get("/metrics", summary="Get MTTR, MTTD, and Automation Success Rate Metrics")
def get_metrics() -> Dict[str, Any]:
    return _to_dict(_runtime.metrics_collector.collect_metrics())


@router.get("/security", summary="Get Security, RBAC, and Destructive Command Whitelisting Audit")
def get_security() -> Dict[str, Any]:
    return _to_dict(_runtime.security_auditor.audit_security())


@router.get("/scorecard", summary="Get 6-Dimension Autonomous Remediation Scorecard")
def get_scorecard() -> Dict[str, Any]:
    res = _runtime.run_full_verification()
    return _to_dict(res["scorecard"])


@router.post("/trigger", summary="Trigger Autonomous Remediation for a Detected Failure")
def trigger_remediation(payload: Dict[str, Any]) -> Dict[str, Any]:
    context = FailureContext(
        failure_id=payload.get("failure_id", "FAIL-MANUAL-001"),
        root_cause=payload.get("root_cause", "worker_heartbeat_missing"),
        severity=payload.get("severity", "SEV-2"),
        confidence=payload.get("confidence", 0.95),
        affected_component=payload.get("affected_component", "celery_worker_01"),
        impact_scope=payload.get("impact_scope", "local_service"),
        current_metrics=payload.get("current_metrics", {}),
    )
    result = _runtime.trigger_remediation_pipeline(context)
    return _to_dict(result)


@router.post("/verify", summary="Run Full Autonomous Remediation Verification & Export Manifests")
def execute_full_verification() -> Dict[str, Any]:
    res = _runtime.run_full_verification()
    return _to_dict(res)
