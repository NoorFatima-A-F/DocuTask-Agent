"""Rollback Executor for Halting Rollouts and Restoring Stable Releases."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Callable, Optional
import logging
import uuid

from ..control_plane.state import DeploymentRecord, DeploymentStatus

logger = logging.getLogger("app.infrastructure.deployment.rollback")


class RollbackTriggerType(str, Enum):
    """Reason for triggering automated or manual rollback."""
    MANUAL = "manual"
    METRIC_ANOMALY = "metric_anomaly"
    HEALTH_FAILURE = "health_failure"
    GOVERNANCE_VIOLATION = "governance_violation"
    AI_QUALITY_DEGRADATION = "ai_quality_degradation"


@dataclass
class RollbackRequest:
    """Request payload to initiate a rollback."""
    deployment_id: str
    trigger_type: RollbackTriggerType
    reason: str
    target_previous_version: Optional[str] = None
    initiated_by: str = "system-sre-controller"


@dataclass
class RollbackResult:
    """Outcome of a rollback execution."""
    success: bool
    rollback_id: str
    deployment_id: str
    restored_version: str
    duration_ms: float
    completed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    error_message: Optional[str] = None


class RollbackExecutor:
    """Executes immediate rollback actions to recover from failed rollouts."""

    def execute_rollback(
        self,
        deployment: DeploymentRecord,
        request: RollbackRequest,
        restore_fn: Optional[Callable[[str], bool]] = None,
    ) -> RollbackResult:
        """Halt rollout and restore prior known good version."""
        start_time = datetime.now(timezone.utc)
        rollback_id = f"rb-{uuid.uuid4().hex[:8]}"

        deployment.transition_to(DeploymentStatus.ROLLING_BACK, f"Rollback initiated: {request.reason}")
        deployment.rollback_reason = request.reason

        restored_version = request.target_previous_version or deployment.previous_version or "1.0.0"

        try:
            if restore_fn:
                ok = restore_fn(restored_version)
                if not ok:
                    deployment.transition_to(DeploymentStatus.FAILED, "Rollback restoration action failed")
                    return RollbackResult(
                        success=False,
                        rollback_id=rollback_id,
                        deployment_id=deployment.deployment_id,
                        restored_version=restored_version,
                        duration_ms=(datetime.now(timezone.utc) - start_time).total_seconds() * 1000.0,
                        error_message="Underlying restore handler failed",
                    )

            deployment.transition_to(DeploymentStatus.ROLLED_BACK, f"Successfully restored version {restored_version}")
            return RollbackResult(
                success=True,
                rollback_id=rollback_id,
                deployment_id=deployment.deployment_id,
                restored_version=restored_version,
                duration_ms=(datetime.now(timezone.utc) - start_time).total_seconds() * 1000.0,
            )

        except Exception as e:
            logger.error("Exception during rollback execution: %s", e)
            deployment.transition_to(DeploymentStatus.FAILED, f"Rollback error: {e}")
            return RollbackResult(
                success=False,
                rollback_id=rollback_id,
                deployment_id=deployment.deployment_id,
                restored_version=restored_version,
                duration_ms=(datetime.now(timezone.utc) - start_time).total_seconds() * 1000.0,
                error_message=str(e),
            )
