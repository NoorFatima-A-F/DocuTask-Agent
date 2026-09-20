"""Artifact Retention and Immutability Policy Engine."""
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional
from .models import ArtifactIdentity, ArtifactQuarantineStatus


@dataclass
class RetentionPolicy:
    """Retention rule configuration."""
    min_retention_days: int = 90
    keep_production_forever: bool = True
    allow_delete_active: bool = False


class ArtifactRetentionManager:
    """Enforces immutability locks and retention periods."""

    def __init__(self, policy: Optional[RetentionPolicy] = None):
        self.policy = policy or RetentionPolicy()

    def can_prune(self, artifact: ArtifactIdentity, is_in_production: bool = False) -> bool:
        """Determines if an artifact can be pruned based on policy."""
        if self.policy.keep_production_forever and is_in_production:
            return False
        if artifact.immutable and not self.policy.allow_delete_active:
            if artifact.quarantine_status == ArtifactQuarantineStatus.ACTIVE:
                return False

        age_days = (datetime.now(timezone.utc) - artifact.created_at).days
        return age_days >= self.policy.min_retention_days
