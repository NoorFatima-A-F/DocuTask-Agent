"""Release Lifecycle Management, Tracking, and Artifact Association."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import threading
import uuid

from .versions import ReleaseVersion
from .approvals import ReleaseApprovalGate, ApprovalDecision


class ReleaseLifecycleStatus(str, Enum):
    """Lifecycle statuses for an enterprise software release."""
    CREATED = "created"
    VALIDATED = "validated"
    APPROVED = "approved"
    RELEASED = "released"
    DEPLOYED = "deployed"
    MONITORED = "monitored"
    COMPLETED = "completed"
    ARCHIVED = "archived"


@dataclass
class ReleaseMetadata:
    """Full lifecycle tracking metadata for an enterprise release."""
    release_id: str
    version: str
    components_changed: List[str]
    artifact_ids: List[str]
    status: ReleaseLifecycleStatus = ReleaseLifecycleStatus.CREATED
    target_environments: List[str] = field(default_factory=lambda: ["staging", "prod"])
    changelog: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    released_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class ReleaseManager:
    """Oversees the full end-to-end lifecycle of platform releases."""

    def __init__(self, approval_gate: Optional[ReleaseApprovalGate] = None) -> None:
        self.approval_gate = approval_gate or ReleaseApprovalGate()
        self._releases: Dict[str, ReleaseMetadata] = {}
        self._lock = threading.RLock()

    def create_release(
        self,
        version: str,
        components_changed: List[str],
        artifact_ids: List[str],
        changelog: str = "",
        target_environments: Optional[List[str]] = None,
    ) -> ReleaseMetadata:
        """Initialize a new release record."""
        # Validate version syntax
        ReleaseVersion.parse(version)

        rel = ReleaseMetadata(
            release_id=f"rel-{uuid.uuid4().hex[:8]}",
            version=version,
            components_changed=components_changed,
            artifact_ids=artifact_ids,
            changelog=changelog,
            target_environments=target_environments or ["staging", "prod"],
            status=ReleaseLifecycleStatus.CREATED,
        )

        with self._lock:
            self._releases[rel.release_id] = rel

        return rel

    def transition_status(self, release_id: str, new_status: ReleaseLifecycleStatus) -> bool:
        """Advance release through its lifecycle states."""
        with self._lock:
            rel = self._releases.get(release_id)
            if not rel:
                return False

            if new_status == ReleaseLifecycleStatus.RELEASED:
                if not self.approval_gate.is_release_approved(release_id):
                    raise PermissionError(f"Cannot mark release '{release_id}' as RELEASED without mandatory stakeholder approvals")
                rel.released_at = datetime.now(timezone.utc)

            if new_status == ReleaseLifecycleStatus.COMPLETED:
                rel.completed_at = datetime.now(timezone.utc)

            rel.status = new_status
            return True

    def get_release(self, release_id: str) -> Optional[ReleaseMetadata]:
        """Fetch release by ID."""
        with self._lock:
            return self._releases.get(release_id)

    def list_releases(self, status: Optional[ReleaseLifecycleStatus] = None) -> List[ReleaseMetadata]:
        """List releases."""
        with self._lock:
            res = list(self._releases.values())
            if status:
                res = [r for r in res if r.status == status]
            return sorted(res, key=lambda r: r.created_at, reverse=True)
