"""Release Management Domain Model."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid
from .exceptions import ReleaseException


class ReleaseStatus(str, Enum):
    """Lifecycle status for platform releases."""
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    DEPRECATED = "DEPRECATED"
    REVOKED = "REVOKED"


@dataclass
class Release:
    """Immutable release package representation."""
    version: str
    name: str
    commit_sha: str
    artifact_ids: List[str] = field(default_factory=list)
    changelog: str = ""
    created_by: str = "system"
    release_id: str = field(default_factory=lambda: f"rel-{uuid.uuid4().hex[:10]}")
    status: ReleaseStatus = ReleaseStatus.DRAFT
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def publish(self) -> None:
        """Publishes the release making it available for deployment."""
        if self.status != ReleaseStatus.DRAFT:
            raise ReleaseException(f"Cannot publish release {self.release_id} in state {self.status.value}")
        if not self.artifact_ids:
            raise ReleaseException(f"Cannot publish release {self.release_id} without any attached artifacts")
        self.status = ReleaseStatus.PUBLISHED

    def deprecate(self, reason: Optional[str] = None) -> None:
        """Marks the release as deprecated."""
        if self.status == ReleaseStatus.REVOKED:
            raise ReleaseException(f"Cannot deprecate revoked release {self.release_id}")
        self.status = ReleaseStatus.DEPRECATED
        if reason:
            self.metadata["deprecation_reason"] = reason

    def revoke(self, reason: str) -> None:
        """Revokes a release due to security or critical fault."""
        self.status = ReleaseStatus.REVOKED
        self.metadata["revocation_reason"] = reason
        self.metadata["revoked_at"] = datetime.now(timezone.utc).isoformat()

    def add_tag(self, tag: str) -> None:
        """Appends a search tag if not already present."""
        if tag not in self.tags:
            self.tags.append(tag)

    def to_dict(self) -> Dict[str, Any]:
        """Serializes release model to dictionary."""
        return {
            "release_id": self.release_id,
            "version": self.version,
            "name": self.name,
            "commit_sha": self.commit_sha,
            "artifact_ids": self.artifact_ids,
            "changelog": self.changelog,
            "created_by": self.created_by,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "tags": self.tags,
            "metadata": self.metadata,
        }
