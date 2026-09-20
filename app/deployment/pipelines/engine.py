"""Pipeline Execution Engine."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid
from ..core.exceptions import DeploymentException
from .stages import PipelineStage, PipelineStageResult


class PipelineRunStatus(str, Enum):
    """Execution status of a pipeline run."""
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    ABORTED = "ABORTED"


@dataclass
class PipelineRun:
    """Execution trace of a complete deployment pipeline run."""
    pipeline_name: str
    run_id: str = field(default_factory=lambda: f"run-{uuid.uuid4().hex[:8]}")
    status: PipelineRunStatus = PipelineRunStatus.RUNNING
    stage_results: List[PipelineStageResult] = field(default_factory=list)
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    context: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


class PipelineEngine:
    """Orchestrates multi-stage continuous delivery pipelines."""

    def __init__(self, name: str = "default-delivery-pipeline"):
        self.name = name
        self._stages: List[PipelineStage] = []
        self._runs: Dict[str, PipelineRun] = {}

    def add_stage(self, stage: PipelineStage) -> "PipelineEngine":
        """Appends an execution stage to pipeline sequence."""
        self._stages.append(stage)
        return self

    def get_run(self, run_id: str) -> Optional[PipelineRun]:
        """Retrieves past pipeline run by ID."""
        return self._runs.get(run_id)

    def execute(self, initial_context: Optional[Dict[str, Any]] = None) -> PipelineRun:
        """Executes all pipeline stages sequentially."""
        run = PipelineRun(
            pipeline_name=self.name,
            context=initial_context or {},
        )
        self._runs[run.run_id] = run

        for stage in self._stages:
            result = stage.run(run.context)
            run.stage_results.append(result)

            # Propagate output data to next stages
            run.context.update(result.output_data)

            if not result.passed and stage.critical:
                run.status = PipelineRunStatus.FAILED
                run.completed_at = datetime.now(timezone.utc)
                run.error = f"Critical stage '{stage.name}' failed: {result.details}"
                return run

        run.status = PipelineRunStatus.SUCCESS
        run.completed_at = datetime.now(timezone.utc)
        return run
