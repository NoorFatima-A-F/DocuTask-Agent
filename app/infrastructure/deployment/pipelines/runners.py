"""Stage Runners supporting sequential and parallel stage execution with retry logic."""

from datetime import datetime, timezone
from typing import Any, Dict
import time

from .stages import PipelineStageConfig, StageExecutionResult, StageStatus


class StageRunner:
    """Executes a pipeline stage with timing, logs, and retries."""

    def run_stage(self, stage: PipelineStageConfig, context: Dict[str, Any]) -> StageExecutionResult:
        """Run single stage synchronously."""
        if not stage.enabled:
            return StageExecutionResult(
                stage_name=stage.name,
                stage_type=stage.stage_type,
                status=StageStatus.SKIPPED,
                logs=["Stage disabled, skipping"],
            )

        start_time = time.time()
        started_at = datetime.now(timezone.utc)
        result = StageExecutionResult(
            stage_name=stage.name,
            stage_type=stage.stage_type,
            status=StageStatus.RUNNING,
            started_at=started_at,
        )

        attempts = 0
        max_attempts = max(1, stage.retry_count)

        while attempts < max_attempts:
            attempts += 1
            try:
                result.logs.append(f"Executing attempt {attempts}/{max_attempts}")
                if stage.handler:
                    output = stage.handler(context)
                    if isinstance(output, dict):
                        context.update(output)
                        if "artifacts" in output:
                            result.output_artifacts.extend(output["artifacts"])

                result.status = StageStatus.PASSED
                result.logs.append("Stage passed successfully")
                break
            except Exception as e:
                result.logs.append(f"Attempt {attempts} failed: {e}")
                if attempts >= max_attempts:
                    result.status = StageStatus.FAILED
                    result.error_message = str(e)

        result.duration_ms = (time.time() - start_time) * 1000.0
        result.completed_at = datetime.now(timezone.utc)
        return result
