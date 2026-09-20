"""
Deployment Rollback and Reversibility Manager.
Coordinates automated, audited rollback procedures for artifacts, configurations, and schemas.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Dict, Any

@dataclass(frozen=True)
class RollbackRecord:
    target_version: str
    prior_version: str
    initiated_by: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    reason: str = "Automated quality gate failure"

class DeploymentRollbackManager:
    """Executes state-preserving rollbacks with full audit history."""
    def __init__(self):
        self._history: List[RollbackRecord] = []

    def execute_rollback(self, prior_version: str, target_version: str, reason: str = "Rollback triggered") -> RollbackRecord:
        record = RollbackRecord(
            target_version=target_version,
            prior_version=prior_version,
            initiated_by="system-governance",
            reason=reason
        )
        self._history.append(record)
        return record

    def get_rollback_history(self) -> List[RollbackRecord]:
        return list(self._history)
