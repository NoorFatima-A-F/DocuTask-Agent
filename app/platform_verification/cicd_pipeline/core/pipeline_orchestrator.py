"""
Enterprise Pipeline Orchestration Engine executing stage state machines.
"""
from __future__ import annotations
from datetime import datetime, timezone
import time
from typing import Dict, List, Optional
import uuid
from app.platform_verification.cicd_pipeline.domain.interfaces import (
    IPipelineOrchestrator,
    IStageRunner,
)
from app.platform_verification.cicd_pipeline.domain.models import (
    PipelineChangeContext,
    PipelineExecutionRecord,
    PipelineExecutionStatus,
    PipelineStageType,
    StageExecutionRecord,
    StageExecutionStatus,
    TargetEnvironment,
)


class EnterprisePipelineOrchestrator(IPipelineOrchestrator):
    """Coordinates end-to-end execution of verification pipelines with dynamic branching."""

    def __init__(self, stage_runner: IStageRunner):
        self.stage_runner = stage_runner
        self._executions: Dict[str, PipelineExecutionRecord] = {}

    def trigger_pipeline(
        self,
        change_context: PipelineChangeContext,
        target_env: TargetEnvironment = TargetEnvironment.STAGING,
    ) -> PipelineExecutionRecord:
        pipeline_id = f"PIPE-{uuid.uuid4().hex[:8].upper()}"
        pipeline_name = f"Continuous-Verification-{change_context.primary_change_type.value}-{target_env.value}"
        started_at = datetime.now(timezone.utc).isoformat()
        t0 = time.time()

        stage_records: List[StageExecutionRecord] = []
        previous_outputs: Dict[str, Any] = {}
        pipeline_status = PipelineExecutionStatus.RUNNING
        explainable_summary: List[str] = []

        explainable_summary.append(
            f"Triggered pipeline for {change_context.primary_change_type.value} change (Risk: {change_context.risk_level.value})."
        )

        for stage_type in change_context.required_stages:
            stage_res = self.stage_runner.execute_stage(
                stage_type=stage_type,
                change_context=change_context,
                previous_stage_outputs=previous_outputs,
            )
            stage_records.append(stage_res)
            previous_outputs[stage_type.value] = stage_res.metrics

            if stage_res.status == StageExecutionStatus.FAILED:
                pipeline_status = PipelineExecutionStatus.FAILED
                explainable_summary.append(
                    f"Pipeline FAILED at stage '{stage_res.stage_name}': {', '.join(stage_res.errors)}"
                )
                break
            else:
                explainable_summary.append(f"Stage '{stage_res.stage_name}' PASSED.")

        if pipeline_status == PipelineExecutionStatus.RUNNING:
            pipeline_status = PipelineExecutionStatus.PASSED
            explainable_summary.append("All required verification stages passed. Build certified for promotion.")

        duration = round(time.time() - t0, 3)
        completed_at = datetime.now(timezone.utc).isoformat()

        record = PipelineExecutionRecord(
            pipeline_id=pipeline_id,
            pipeline_name=pipeline_name,
            target_environment=target_env,
            change_context=change_context,
            status=pipeline_status,
            started_at=started_at,
            completed_at=completed_at,
            duration_seconds=duration,
            stage_records=stage_records,
            evidence_package_id=f"EVD-PKG-{pipeline_id}",
            certification_id=f"CERT-{pipeline_id}" if pipeline_status == PipelineExecutionStatus.PASSED else None,
            deployment_decision="APPROVED" if pipeline_status == PipelineExecutionStatus.PASSED else "BLOCKED",
            explainable_summary=explainable_summary,
        )

        self._executions[pipeline_id] = record
        return record

    def get_pipeline_status(self, pipeline_id: str) -> Optional[PipelineExecutionRecord]:
        return self._executions.get(pipeline_id)

    def list_executions(self) -> List[PipelineExecutionRecord]:
        return list(self._executions.values())
