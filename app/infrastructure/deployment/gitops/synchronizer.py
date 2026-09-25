"""GitOps Manifest Synchronization and Desired State Tracking."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import threading


@dataclass
class GitOpsManifest:
    """A versioned declarative resource manifest."""
    resource_id: str
    kind: str
    name: str
    namespace: str
    environment: str
    desired_spec: Dict[str, Any]
    commit_sha: str
    repo_url: str = "https://github.com/docutask/infrastructure-gitops"
    branch: str = "main"
    synced_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class GitOpsSynchronizer:
    """Maintains local mirror of desired declarative state from Git repositories."""

    def __init__(self) -> None:
        self._manifests: Dict[str, GitOpsManifest] = {}  # f"{env}:{kind}:{namespace}:{name}" -> GitOpsManifest
        self._lock = threading.RLock()
        self._last_sync_commit: str = ""

    def sync_manifests(self, repo_url: str, branch: str, commit_sha: str, manifests: List[GitOpsManifest]) -> int:
        """Update desired state catalog with new manifests from Git commit."""
        with self._lock:
            self._last_sync_commit = commit_sha
            count = 0
            for m in manifests:
                key = f"{m.environment}:{m.kind}:{m.namespace}:{m.name}"
                m.commit_sha = commit_sha
                m.repo_url = repo_url
                m.branch = branch
                m.synced_at = datetime.now(timezone.utc)
                self._manifests[key] = m
                count += 1
            return count

    def get_desired_manifest(self, environment: str, kind: str, namespace: str, name: str) -> Optional[GitOpsManifest]:
        """Fetch desired manifest."""
        key = f"{environment}:{kind}:{namespace}:{name}"
        with self._lock:
            return self._manifests.get(key)

    def list_manifests_for_environment(self, environment: str) -> List[GitOpsManifest]:
        """List all desired manifests for an environment."""
        with self._lock:
            return [m for m in self._manifests.values() if m.environment == environment]
