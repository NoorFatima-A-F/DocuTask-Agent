"""Unit tests for Rollback and Automated Recovery Engine."""
from app.deployment.core.controller import DeploymentController
from app.deployment.core.lifecycle import DeploymentStatus
from app.deployment.rollback.manager import RollbackManager
from app.deployment.rollback.recovery import AutomatedRecoveryEngine


def test_automated_recovery_engine_slo_breach():
    recovery = AutomatedRecoveryEngine(max_error_rate=0.01, max_p99_latency_ms=200.0)

    # Healthy
    d1 = recovery.evaluate_health(deployment_id="dep-1", error_rate=0.005, p99_latency_ms=150.0)
    assert d1.should_rollback is False

    # Error rate spike
    d2 = recovery.evaluate_health(deployment_id="dep-1", error_rate=0.03, p99_latency_ms=150.0)
    assert d2.should_rollback is True
    assert "Error rate" in (d2.trigger_reason or "")


def test_rollback_manager_execution():
    controller = DeploymentController()
    rel1 = controller.create_release("1.0.0", "V1", "sha1", ["art-1"])
    rel1.publish()
    dep1 = controller.create_deployment(rel1.release_id, "prod")
    controller.execute_deployment(dep1.deployment_id)

    rel2 = controller.create_release("1.1.0", "V2", "sha2", ["art-2"])
    rel2.publish()
    dep2 = controller.create_deployment(rel2.release_id, "prod")
    controller.execute_deployment(dep2.deployment_id)

    manager = RollbackManager(controller=controller)
    rollback_rec = manager.execute_rollback(
        deployment_id=dep2.deployment_id,
        reason="P0 Regression in parsing",
    )

    assert rollback_rec.success is True
    assert dep2.status == DeploymentStatus.ROLLED_BACK
    assert dep2.rollback_target_id == rel1.release_id
