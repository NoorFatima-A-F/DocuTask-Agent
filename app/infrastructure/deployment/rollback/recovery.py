"""Rollback Recovery Management, Post-Rollback Health Validation, and RCA Reporting."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional
import threading

from .executor import RollbackRequest, RollbackExecutor, RollbackTriggerType
from ..control_plane.state import DeploymentRecord


@dataclass
class PostRollbackRCAReport:
    """Post-incident Root Cause Analysis report for a rolled back deployment."""
    report_id: str
    deployment_id: str
    service_name: str
    failed_version: str
    restored_version: str
    trigger_type: RollbackTriggerType
    root_cause_summary: str
    metrics_at_failure: Dict[str, Any] = field(default_factory=dict)
    remediation_actions: List[str] = field(default_factory=list)
    generated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class RollbackRecoveryManager:
    """Manages rollback lifecycle, health verification, and incident report generation."""

    def __init__(self, executor: Optional[RollbackExecutor] = None) -> None:
        self.executor = executor or RollbackExecutor()
        self._reports: List[PostRollbackRCAReport] = []
        self._lock = threading.RLock()

    def trigger_and_recover(
        self,
        deployment: DeploymentRecord,
        reason: str,
        trigger_type: RollbackTriggerType = RollbackTriggerType.METRIC_ANOMALY,
        health_check_fn: Optional[Callable[[], bool]] = None,
        restore_fn: Optional[Callable[[str], bool]] = None,
    ) -> PostRollbackRCAReport:
        """Trigger rollback, verify health, and generate RCA report."""
        req = RollbackRequest(
            deployment_id=deployment.deployment_id,
            trigger_type=trigger_type,
            reason=reason,
            target_previous_version=deployment.previous_version,
        )

        res = self.executor.execute_rollback(deployment, req, restore_fn=restore_fn)

        # Health verification
        healthy = health_check_fn() if health_check_fn else True

        report = PostRollbackRCAReport(
            report_id=f"rca-{deployment.deployment_id}",
            deployment_id=deployment.deployment_id,
            service_name=deployment.service_name,
            failed_version=deployment.target_version,
            restored_version=res.restored_version,
            trigger_type=trigger_type,
            root_cause_summary=f"Deployment {deployment.deployment_id} rolled back due to {reason}. Post-rollback healthy: {healthy}",
            remediation_actions=[
                "Halt automatic promotion pipeline for release",
                "Investigate error logs and telemetry in Phase 9E",
                "Run regression tests on canary environment before redeploying",
            ],
        )

        with self._lock:
            self._reports.append(report)

        return report
