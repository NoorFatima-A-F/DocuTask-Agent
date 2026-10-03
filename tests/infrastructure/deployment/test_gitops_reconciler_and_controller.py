"""Tests for GitOps Synchronizer, Reconciler, Drift Detection, and Controller."""

from app.infrastructure.deployment.gitops import (
    GitOpsManifest,
    GitOpsSynchronizer,
    DriftType,
    GitOpsReconciler,
    GitOpsController,
)


def test_gitops_drift_detection_and_reconciliation() -> None:
    sync = GitOpsSynchronizer()
    reconciler = GitOpsReconciler(sync)

    desired_manifests = [
        GitOpsManifest(
            resource_id="m1",
            kind="Deployment",
            name="workflow-service",
            namespace="default",
            environment="prod",
            desired_spec={"replicas": 5, "image": "docutask-workflow:1.0.0"},
            commit_sha="commit-1",
        )
    ]
    sync.sync_manifests("https://github.com/docutask/gitops", "main", "commit-1", desired_manifests)

    # Actual cluster state is drifted (replicas=2, unmanaged pod exists)
    actual_cluster = {
        "Deployment:default:workflow-service": {"replicas": 2, "image": "docutask-workflow:1.0.0"},
        "Pod:default:rogue-debug-pod": {"status": "running"},
    }

    drifts = reconciler.detect_drift("prod", actual_cluster)
    assert len(drifts) == 2

    # Modified drift
    mod_drift = next(d for d in drifts if d.drift_type == DriftType.MODIFIED)
    assert mod_drift.resource_key == "Deployment:default:workflow-service"

    # Extra drift
    extra_drift = next(d for d in drifts if d.drift_type == DriftType.EXTRA)
    assert extra_drift.resource_key == "Pod:default:rogue-debug-pod"

    # Reconcile drift
    corrections = reconciler.reconcile_drift("prod", actual_cluster)
    assert corrections == 2
    assert actual_cluster["Deployment:default:workflow-service"]["replicas"] == 5
    assert "Pod:default:rogue-debug-pod" not in actual_cluster


def test_gitops_controller_sync_trigger() -> None:
    controller = GitOpsController()
    manifests = [
        GitOpsManifest(
            resource_id="m2",
            kind="Service",
            name="api-gateway",
            namespace="gateway",
            environment="prod",
            desired_spec={"port": 443},
            commit_sha="c2",
        )
    ]
    res = controller.trigger_sync(
        repo_url="https://github.com/docutask/gitops",
        branch="main",
        commit_sha="c2",
        manifests=manifests,
        actual_resources={},
    )
    assert res["commit_sha"] == "c2"
    assert res["manifest_count"] == 1
    assert len(controller.get_sync_history()) == 1
