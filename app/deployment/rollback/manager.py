"""Enterprise Rollback & Recovery Orchestrator."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid
from ..core.controller import DeploymentController
from ..core.deployment import Deployment
from ..core.exceptions import RollbackException
from .recovery import AutomatedRecoveryEngine, RecoveryDecision


@dataclass
class RollbackRecord:
    """Audit log entry for a rollback execution."""
    rollback_id: str
    failed_deployment_id: str
    target_release_id: str
    environment: str
    reason: str
    initiated_by: str  # "automated_recovery" or "operator"
    success: bool = True
    executed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    details: Dict[str, Any] = field(default_factory=dict)


class RollbackManager:
    """Coordinates multi-tier rollback procedures across traffic, application, and data layers."""

    def __init__(
        self,
        controller: DeploymentController,
        recovery_engine: Optional[AutomatedRecoveryEngine] = None,
    ):
        self.controller = controller
        self.recovery_engine = recovery_engine or AutomatedRecoveryEngine()
        self.rollback_history: List[RollbackRecord] = []

    def execute_rollback(
        self,
        deployment_id: str,
        target_release_id: Optional[str] = None,
        reason: str = "Unspecified rollback trigger",
        initiated_by: str = "operator",
    ) -> RollbackRecord:
        """Executes full rollback for a specified deployment."""
        dep = self.controller.get_deployment(deployment_id)
        if not dep:
            raise RollbackException(f"Deployment '{deployment_id}' not found for rollback")

        rollback_id = f"rb-{uuid.uuid4().hex[:8]}"

        try:
            # Revert deployment state in controller
            rolled_back_dep = self.controller.rollback_deployment(
                deployment_id=deployment_id,
                target_release_id=target_release_id,
                reason=reason,
            )

            record = RollbackRecord(
                rollback_id=rollback_id,
                failed_deployment_id=deployment_id,
                target_release_id=rolled_back_dep.rollback_target_id or "baseline",
                environment=dep.target_environment,
                reason=reason,
                initiated_by=initiated_by,
                success=True,
                details={
                    "strategy": dep.strategy.value,
                    "reverted_status": rolled_back_dep.status.value,
                },
            )
            self.rollback_history.append(record)
            return record

        except Exception as e:
            record = RollbackRecord(
                rollback_id=rollback_id,
                failed_deployment_id=deployment_id,
                target_release_id=target_release_id or "unknown",
                environment=dep.target_environment,
                reason=reason,
                initiated_by=initiated_by,
                success=False,
                details={"error": str(e)},
            )
            self.rollback_history.append(record)
            raise RollbackException(f"Rollback execution failed: {e}") from e

    def monitor_and_auto_recover(
        self,
        deployment_id: str,
        error_rate: float,
        p99_latency_ms: float,
    ) -> Optional[RollbackRecord]:
        """Inspects telemetry and automatically executes rollback if safety thresholds breached."""
        decision = self.recovery_engine.evaluate_health(
            deployment_id=deployment_id,
            error_rate=error_rate,
            p99_latency_ms=p99_latency_ms,
        )

        if decision.should_rollback:
            return self.execute_rollback(
                deployment_id=deployment_id,
                reason=f"Automated recovery trigger: {decision.trigger_reason}",
                initiated_by="automated_recovery",
            )
        return None
