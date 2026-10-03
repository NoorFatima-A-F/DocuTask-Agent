"""Tests for Rollback Executor, Anomaly Tripping, and RCA Report Generation."""

from app.infrastructure.deployment.control_plane import (
    DeploymentRecord,
    DeploymentStatus,
)
from app.infrastructure.deployment.rollback import (
    RollbackTriggerType,
    RollbackRequest,
    RollbackExecutor,
    RollbackRecoveryManager,
)


def test_rollback_executor_and_recovery_flow() -> None:
    rec = DeploymentRecord(
        deployment_id="dep-failing-01",
        release_id="rel-failing-01",
        service_name="payment-connector",
        target_environment="prod",
        target_version="3.0.0",
        previous_version="2.9.4",
        status=DeploymentStatus.RUNNING,
    )

    executor = RollbackExecutor()
    restored_batches = []

    req = RollbackRequest(
        deployment_id="dep-failing-01",
        trigger_type=RollbackTriggerType.METRIC_ANOMALY,
        reason="P99 Latency exceeded 2000ms threshold",
    )

    res = executor.execute_rollback(rec, req, restore_fn=lambda ver: restored_batches.append(ver) or True)

    assert res.success is True
    assert res.restored_version == "2.9.4"
    assert rec.status == DeploymentStatus.ROLLED_BACK
    assert restored_batches == ["2.9.4"]


def test_rollback_recovery_manager_rca_generation() -> None:
    rec = DeploymentRecord(
        deployment_id="dep-rca-01",
        release_id="rel-rca-01",
        service_name="knowledge-retriever",
        target_environment="prod",
        target_version="1.4.0",
        previous_version="1.3.9",
        status=DeploymentStatus.RUNNING,
    )

    mgr = RollbackRecoveryManager()
    rca = mgr.trigger_and_recover(
        deployment=rec,
        reason="Model hallucinations spiked above 5%",
        trigger_type=RollbackTriggerType.AI_QUALITY_DEGRADATION,
    )

    assert rca.report_id == "rca-dep-rca-01"
    assert rca.restored_version == "1.3.9"
    assert rca.trigger_type == RollbackTriggerType.AI_QUALITY_DEGRADATION
    assert len(rca.remediation_actions) >= 1
