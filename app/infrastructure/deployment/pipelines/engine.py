"""CI/CD Pipeline Engine for full delivery orchestration."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import threading
import uuid

from .stages import PipelineStageConfig, StageExecutionResult, StageStatus, StageType
from .runners import StageRunner


@dataclass
class PipelineRun:
    """Represents a complete execution instance of a CI/CD pipeline."""
    run_id: str
    pipeline_name: str
    commit_sha: str
    branch: str = "main"
    status: StageStatus = StageStatus.PENDING
    stages: List[StageExecutionResult] = field(default_factory=list)
    artifacts_produced: List[str] = field(default_factory=list)
    total_duration_ms: float = 0.0
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    context: Dict[str, Any] = field(default_factory=dict)


class PipelineEngine:
    """Orchestrates end-to-end CI/CD delivery pipelines."""

    def __init__(self, runner: Optional[StageRunner] = None) -> None:
        self.runner = runner or StageRunner()
        self._history: Dict[str, PipelineRun] = {}
        self._lock = threading.RLock()

    def build_standard_ci_pipeline(
        self,
        service_name: str,
        custom_test_handler: Optional[Any] = None,
        custom_build_handler: Optional[Any] = None,
    ) -> List[PipelineStageConfig]:
        """Generate a standard 8-stage enterprise CI/CD pipeline."""
        return [
            PipelineStageConfig(name="Source Checkout", stage_type=StageType.SOURCE),
            PipelineStageConfig(name="Compile & Container Build", stage_type=StageType.BUILD, handler=custom_build_handler),
            PipelineStageConfig(name="Unit & Integration Tests", stage_type=StageType.TEST, handler=custom_test_handler),
            PipelineStageConfig(name="Vulnerability & SAST Scan", stage_type=StageType.SECURITY_SCAN),
            PipelineStageConfig(name="Artifact Cryptographic Signing", stage_type=StageType.ARTIFACT_SIGN),
            PipelineStageConfig(name="Registry Publish", stage_type=StageType.PUBLISH),
            PipelineStageConfig(name="Deploy to Environment", stage_type=StageType.DEPLOY),
            PipelineStageConfig(name="Health & Canary Verification", stage_type=StageType.VERIFY),
        ]

    def execute_pipeline(
        self,
        pipeline_name: str,
        commit_sha: str,
        stages: List[PipelineStageConfig],
        initial_context: Optional[Dict[str, Any]] = None,
        branch: str = "main",
    ) -> PipelineRun:
        """Run a configured CI/CD pipeline."""
        run = PipelineRun(
            run_id=f"run-{uuid.uuid4().hex[:8]}",
            pipeline_name=pipeline_name,
            commit_sha=commit_sha,
            branch=branch,
            status=StageStatus.RUNNING,
            context=initial_context or {},
        )

        all_passed = True
        for stage in stages:
            stage_res = self.runner.run_stage(stage, run.context)
            run.stages.append(stage_res)
            run.total_duration_ms += stage_res.duration_ms
            run.artifacts_produced.extend(stage_res.output_artifacts)

            if stage_res.status == StageStatus.FAILED and stage.required:
                all_passed = False
                break

        run.status = StageStatus.PASSED if all_passed else StageStatus.FAILED
        run.completed_at = datetime.now(timezone.utc)

        with self._lock:
            self._history[run.run_id] = run

        return run

    def get_run(self, run_id: str) -> Optional[PipelineRun]:
        """Fetch pipeline run by ID."""
        with self._lock:
            return self._history.get(run_id)

    def list_runs(self, pipeline_name: Optional[str] = None) -> List[PipelineRun]:
        """List pipeline runs."""
        with self._lock:
            runs = list(self._history.values())
            if pipeline_name:
                runs = [r for r in runs if r.pipeline_name == pipeline_name]
            return sorted(runs, key=lambda r: r.started_at, reverse=True)
