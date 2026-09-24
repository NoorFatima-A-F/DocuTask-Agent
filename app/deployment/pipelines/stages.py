"""Pipeline Stages and Execution Results."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict


class PipelineStageType(str, Enum):
    """Supported pipeline execution stages."""
    LINT = "LINT"
    UNIT_TEST = "UNIT_TEST"
    SECURITY_SCAN = "SECURITY_SCAN"
    BUILD_ARTIFACT = "BUILD_ARTIFACT"
    DEPLOY_DEV = "DEPLOY_DEV"
    INTEGRATION_TEST = "INTEGRATION_TEST"
    APPROVAL_GATE = "APPROVAL_GATE"
    DEPLOY_STAGING = "DEPLOY_STAGING"
    E2E_VERIFY = "E2E_VERIFY"
    DEPLOY_PROD = "DEPLOY_PROD"
    POST_DEPLOY_VERIFY = "POST_DEPLOY_VERIFY"


@dataclass
class PipelineStageResult:
    """Result of a pipeline stage execution."""
    stage_name: str
    stage_type: PipelineStageType
    passed: bool
    duration_ms: float
    details: str
    output_data: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class PipelineStage:
    """Individual executable stage within a delivery pipeline."""

    def __init__(
        self,
        name: str,
        stage_type: PipelineStageType,
        action_fn: Callable[[Dict[str, Any]], Dict[str, Any]],
        critical: bool = True,
    ):
        self.name = name
        self.stage_type = stage_type
        self.action_fn = action_fn
        self.critical = critical

    def run(self, context: Dict[str, Any]) -> PipelineStageResult:
        """Runs the stage action and measures execution duration."""
        start_time = datetime.now(timezone.utc)
        try:
            out = self.action_fn(context)
            duration_ms = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000.0
            return PipelineStageResult(
                stage_name=self.name,
                stage_type=self.stage_type,
                passed=True,
                duration_ms=round(duration_ms, 2),
                details="Stage executed successfully",
                output_data=out or {},
            )
        except Exception as e:
            duration_ms = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000.0
            return PipelineStageResult(
                stage_name=self.name,
                stage_type=self.stage_type,
                passed=False,
                duration_ms=round(duration_ms, 2),
                details=f"Stage failed: {e}",
                output_data={"error": str(e)},
            )
