"""GitOps Controller managing synchronization and reconciliation loops."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import logging
import threading

from .synchronizer import GitOpsManifest, GitOpsSynchronizer
from .reconciler import GitOpsReconciler, DriftItem

logger = logging.getLogger("app.infrastructure.deployment.gitops")


class GitOpsController:
    """Coordinates Git repository syncing and cluster state reconciliation."""

    def __init__(
        self,
        synchronizer: Optional[GitOpsSynchronizer] = None,
        reconciler: Optional[GitOpsReconciler] = None,
    ) -> None:
        self.synchronizer = synchronizer or GitOpsSynchronizer()
        self.reconciler = reconciler or GitOpsReconciler(self.synchronizer)
        self._auto_sync_enabled = True
        self._lock = threading.RLock()
        self._sync_history: List[Dict[str, Any]] = []

    def trigger_sync(
        self,
        repo_url: str,
        branch: str,
        commit_sha: str,
        manifests: List[GitOpsManifest],
        actual_resources: Optional[Dict[str, Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """Process incoming Git webhook/sync event."""
        with self._lock:
            manifest_count = self.synchronizer.sync_manifests(repo_url, branch, commit_sha, manifests)

            corrections = 0
            drifts_detected = 0
            if actual_resources is not None and self._auto_sync_enabled:
                for env in set(m.environment for m in manifests):
                    drifts = self.reconciler.detect_drift(env, actual_resources)
                    drifts_detected += len(drifts)
                    corrections += self.reconciler.reconcile_drift(env, actual_resources)

            record = {
                "commit_sha": commit_sha,
                "branch": branch,
                "manifest_count": manifest_count,
                "drifts_detected": drifts_detected,
                "corrections_applied": corrections,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            self._sync_history.append(record)
            return record

    def get_sync_history(self) -> List[Dict[str, Any]]:
        """Return history of sync events."""
        with self._lock:
            return list(self._sync_history)
