"""Unit tests for Deployment Core and Control Plane."""
import pytest
from app.deployment.core.controller import DeploymentController
from app.deployment.core.deployment import Deployment, DeploymentStrategyType
from app.deployment.core.exceptions import DeploymentException, ReleaseException
from app.deployment.core.lifecycle import DeploymentStateEngine, DeploymentStatus
from app.deployment.core.release import Release, ReleaseStatus


def test_deployment_state_engine_valid_lifecycle():
    engine = DeploymentStateEngine()
    assert engine.current_status == DeploymentStatus.PENDING

    engine.transition_to(DeploymentStatus.VALIDATING, reason="Pre-flight checks")
    assert engine.current_status == DeploymentStatus.VALIDATING

    engine.transition_to(DeploymentStatus.PREPARING)
    engine.transition_to(DeploymentStatus.DEPLOYING)
    engine.transition_to(DeploymentStatus.VERIFYING)
    engine.transition_to(DeploymentStatus.ACTIVE)
    assert engine.current_status == DeploymentStatus.ACTIVE
    assert len(engine.history) == 6


def test_deployment_state_engine_invalid_transition():
    engine = DeploymentStateEngine()
    with pytest.raises(DeploymentException, match="Invalid state transition"):
        engine.transition_to(DeploymentStatus.ACTIVE)


def test_release_lifecycle():
    rel = Release(
        version="1.0.0",
        name="Initial Release",
        commit_sha="abcdef123456",
        artifact_ids=["art-001"],
    )
    assert rel.status == ReleaseStatus.DRAFT

    rel.publish()
    assert rel.status == ReleaseStatus.PUBLISHED

    rel.deprecate(reason="Replaced by 1.1.0")
    assert rel.status == ReleaseStatus.DEPRECATED
    assert rel.metadata.get("deprecation_reason") == "Replaced by 1.1.0"


def test_release_publish_without_artifacts_fails():
    rel = Release(version="1.0.1", name="Empty Release", commit_sha="123")
    with pytest.raises(ReleaseException, match="without any attached artifacts"):
        rel.publish()


def test_controller_create_and_execute_deployment():
    controller = DeploymentController()
    rel = controller.create_release(
        version="2.0.0",
        name="V2 Architecture",
        commit_sha="987654321",
        artifact_ids=["art-core", "art-ai"],
    )
    rel.publish()

    dep = controller.create_deployment(
        release_id=rel.release_id,
        target_environment="prod",
        strategy=DeploymentStrategyType.CANARY,
        replicas=5,
    )
    assert dep.status == DeploymentStatus.PENDING

    executed = controller.execute_deployment(dep.deployment_id)
    assert executed.status == DeploymentStatus.ACTIVE
    assert executed.traffic_weight == 1.0
    assert controller.get_active_deployment("prod") == executed


def test_controller_duplicate_release_version_fails():
    controller = DeploymentController()
    controller.create_release(version="1.0.0", name="V1", commit_sha="aaa", artifact_ids=["a1"])
    with pytest.raises(ReleaseException, match="already exists"):
        controller.create_release(version="1.0.0", name="V1 Duplicate", commit_sha="bbb", artifact_ids=["a2"])
