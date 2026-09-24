"""
REST API Router for Enterprise CI/CD Continuous Verification Pipeline (PART 7).
"""
from __future__ import annotations
from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.platform_verification.cicd_pipeline.domain.models import (
    RollbackTriggerReason,
    TargetEnvironment,
)
from app.platform_verification.cicd_pipeline.runtime.cicd_platform_runtime import (
    EnterpriseCICDPlatformRuntime,
)

router = APIRouter(prefix="/pipelines", tags=["Continuous Verification CI/CD Pipeline"])
_runtime = EnterpriseCICDPlatformRuntime()


class TriggerPipelineRequest(BaseModel):
    change_id: str
    commit_sha: str
    branch: str = "main"
    author: str
    changed_paths: List[str]
    target_env: TargetEnvironment = TargetEnvironment.STAGING


class PromoteEnvironmentRequest(BaseModel):
    pipeline_id: str
    target_env: TargetEnvironment
    approved_by: str


class RollbackRequest(BaseModel):
    pipeline_id: str
    target_env: TargetEnvironment
    reason: RollbackTriggerReason
    failed_version: str
    previous_stable_version: str


@router.post("/run", response_model=Dict[str, Any])
def trigger_verification_pipeline(req: TriggerPipelineRequest):
    """Triggers adaptive continuous verification pipeline based on changed files."""
    change_ctx = _runtime.change_detector.analyze_changes(
        change_id=req.change_id,
        commit_sha=req.commit_sha,
        branch=req.branch,
        author=req.author,
        changed_paths=req.changed_paths,
    )

    record = _runtime.orchestrator.trigger_pipeline(
        change_context=change_ctx,
        target_env=req.target_env,
    )
    _runtime.observability.record_pipeline_run(record)

    return {
        "pipeline_id": record.pipeline_id,
        "pipeline_name": record.pipeline_name,
        "status": record.status.value,
        "primary_change_type": record.change_context.primary_change_type.value,
        "risk_level": record.change_context.risk_level.value,
        "duration_seconds": record.duration_seconds,
        "deployment_decision": record.deployment_decision,
        "certification_id": record.certification_id,
        "stages_executed": len(record.stage_records),
    }


@router.get("/{pipeline_id}", response_model=Dict[str, Any])
def get_pipeline_status(pipeline_id: str):
    """Retrieves full stage lifecycle and status of a pipeline run."""
    record = _runtime.orchestrator.get_pipeline_status(pipeline_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pipeline '{pipeline_id}' not found.",
        )
    return {
        "pipeline_id": record.pipeline_id,
        "status": record.status.value,
        "target_environment": record.target_environment.value,
        "deployment_decision": record.deployment_decision,
        "stages": [
            {
                "stage_type": s.stage_type.value,
                "stage_name": s.stage_name,
                "status": s.status.value,
                "duration_seconds": s.duration_seconds,
                "errors": s.errors,
            }
            for s in record.stage_records
        ],
        "explainable_summary": record.explainable_summary,
    }


@router.post("/promote", response_model=Dict[str, Any])
def promote_pipeline_build(req: PromoteEnvironmentRequest):
    """Promotes a verified pipeline build to the next environment."""
    record = _runtime.orchestrator.get_pipeline_status(req.pipeline_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pipeline '{req.pipeline_id}' not found.",
        )
    promo = _runtime.promotion_engine.evaluate_and_promote(
        pipeline_record=record,
        target_env=req.target_env,
        approved_by=req.approved_by,
    )
    return {
        "promotion_id": promo.promotion_id,
        "status": promo.status.value,
        "target_env": promo.target_env.value,
        "actual_certification_level": promo.actual_certification_level,
        "rejection_reason": promo.rejection_reason,
    }


@router.post("/rollback", response_model=Dict[str, Any])
def execute_deployment_rollback(req: RollbackRequest):
    """Executes automated rollback upon incident or health drop."""
    rlbk = _runtime.rollback_engine.execute_rollback(
        pipeline_id=req.pipeline_id,
        target_env=req.target_env,
        reason=req.reason,
        failed_version=req.failed_version,
        previous_stable_version=req.previous_stable_version,
    )
    return {
        "rollback_id": rlbk.rollback_id,
        "status": rlbk.status,
        "invalidated_certification_id": rlbk.invalidated_certification_id,
        "incident_evidence_id": rlbk.incident_evidence_id,
    }


@router.get("/metrics/observability", response_model=Dict[str, Any])
def get_pipeline_observability():
    """Retrieves pipeline DORA and quality metrics."""
    metrics = _runtime.observability.get_metrics()
    return {
        "total_pipeline_runs": metrics.total_pipeline_runs,
        "successful_runs": metrics.successful_runs,
        "failed_runs": metrics.failed_runs,
        "avg_duration_seconds": metrics.avg_duration_seconds,
        "change_failure_rate": metrics.change_failure_rate,
        "deployment_frequency_per_day": metrics.deployment_frequency_per_day,
    }
