# GitOps Continuous Reconciliation Operational Guide

## 1. Git Repository as Single Source of Truth
All cluster resources and application manifests are maintained declaratively in Git repositories:
- Repository layout: `deployments/{environment}/{namespace}/{resource_kind}_{resource_name}.yaml`
- Each commit triggers an automated GitOps sync event via `GitOpsController`.

## 2. Drift Detection & Automated Reconciliation
```python
from app.infrastructure.deployment.gitops import GitOpsSynchronizer, GitOpsReconciler, GitOpsController

sync = GitOpsSynchronizer()
reconciler = GitOpsReconciler(sync)
controller = GitOpsController(synchronizer=sync, reconciler=reconciler)

# Trigger sync on Git commit
sync_result = controller.trigger_sync(
    repo_url="https://github.com/docutask/infrastructure-gitops",
    branch="main",
    commit_sha="commit-9988",
    manifests=desired_manifests,
    actual_resources=live_cluster_state,
)
```

## 3. Drift Types Handled
- `MISSING`: Declared resource does not exist in cluster -> Automatically created.
- `MODIFIED`: Spec field changed manually -> Automatically reverted to Git spec.
- `EXTRA`: Unmanaged rogue resource in namespace -> Automatically pruned.
