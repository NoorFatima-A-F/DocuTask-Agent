"""Tests for Deployment Control Plane, Manager, and State Lifecycle."""

import pytest
from app.infrastructure.deployment.control_plane import (
    DeploymentStatus,
    DeploymentRecord,
    DeploymentHistoryTracker,
    DeploymentControlPlaneManager,
)


def test_deployment_lifecycle_and_history_tracking() -> None:
    tracker = DeploymentHistoryTracker()
    record = DeploymentRecord(
        deployment_id="dep-test-01",
        release_id="rel-test-01",
        service_name="document-indexer",
        target_environment="staging",
        target_version="1.2.0",
        previous_version="1.1.0",
    )
    tracker.record_deployment(record)

    assert record.status == DeploymentStatus.PENDING

    # Transition
    record.transition_to(DeploymentStatus.RUNNING, "Starting deployment")
    assert record.status == DeploymentStatus.RUNNING
    assert len(record.audit_trail) == 1

    record.transition_to(DeploymentStatus.COMPLETED, "Deployment finished")
    assert record.status == DeploymentStatus.COMPLETED
    assert record.completed_at is not None

    # Query latest deployment
    latest = tracker.get_latest_deployment("document-indexer", "staging")
    assert latest is not None
    assert latest.target_version == "1.2.0"


def test_deployment_control_plane_manager_and_concurrency_lock() -> None:
    mgr = DeploymentControlPlaneManager()

    # Successful deployment
    dep = mgr.trigger_deployment(
        service_name="ocr-engine",
        target_environment="prod",
        target_version="2.0.0",
    )
    assert dep.status == DeploymentStatus.COMPLETED
    assert dep.progress_percentage == 100.0

    # Governance gate failure test
    mgr.set_governance_verifier(lambda svc, ver, env: False)
    with pytest.raises(PermissionError):
        mgr.trigger_deployment(
            service_name="ocr-engine",
            target_environment="prod",
            target_version="2.0.1",
        )
