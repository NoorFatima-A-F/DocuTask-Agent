"""
Replication Conflict Resolver.

Provides deterministic conflict resolution across distributed replicas using
Last-Write-Wins (LWW), Vector Clocks, Quorum Consensus, and Manual Review triage.
"""

from __future__ import annotations

import enum
import logging
from datetime import datetime, timezone
from typing import Any, Dict
from pydantic import BaseModel, Field

logger = logging.getLogger("infrastructure.replication.conflict_resolution")


class ConflictResolutionStrategy(str, enum.Enum):
    """Supported conflict resolution strategies."""
    LAST_WRITE_WINS = "LAST_WRITE_WINS"
    VECTOR_CLOCK = "VECTOR_CLOCK"
    QUORUM_BASED = "QUORUM_BASED"
    MANUAL_REVIEW = "MANUAL_REVIEW"


class ReplicationConflict(BaseModel):
    """Specification of a detected replication conflict."""
    conflict_id: str
    entity_id: str
    local_value: Any
    remote_value: Any
    local_timestamp: datetime
    remote_timestamp: datetime
    local_version: int = 1
    remote_version: int = 1
    local_vector_clock: Dict[str, int] = Field(default_factory=dict)
    remote_vector_clock: Dict[str, int] = Field(default_factory=dict)
    quorum_votes: Dict[str, Any] = Field(default_factory=dict)  # node_id -> voted_value


class ResolutionResult(BaseModel):
    """Result of resolving a replication conflict."""
    conflict_id: str
    entity_id: str
    strategy_used: ConflictResolutionStrategy
    resolved_value: Any
    requires_manual_intervention: bool = False
    details: str = ""
    resolved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ConflictResolver:
    """
    Deterministic resolution engine for cross-region data discrepancies.
    """

    def resolve(
        self,
        conflict: ReplicationConflict,
        strategy: ConflictResolutionStrategy = ConflictResolutionStrategy.LAST_WRITE_WINS,
    ) -> ResolutionResult:
        """
        Resolve a replication conflict according to the requested strategy.
        """
        if strategy == ConflictResolutionStrategy.LAST_WRITE_WINS:
            return self._resolve_lww(conflict)
        elif strategy == ConflictResolutionStrategy.VECTOR_CLOCK:
            return self._resolve_vector_clock(conflict)
        elif strategy == ConflictResolutionStrategy.QUORUM_BASED:
            return self._resolve_quorum(conflict)
        else:
            return ResolutionResult(
                conflict_id=conflict.conflict_id,
                entity_id=conflict.entity_id,
                strategy_used=ConflictResolutionStrategy.MANUAL_REVIEW,
                resolved_value=conflict.local_value,
                requires_manual_intervention=True,
                details="Conflict flagged for manual operator review.",
            )

    def _resolve_lww(self, conflict: ReplicationConflict) -> ResolutionResult:
        """Last-Write-Wins based on highest timestamp."""
        if conflict.remote_timestamp > conflict.local_timestamp:
            winner = conflict.remote_value
            details = "Remote value chosen (more recent timestamp)."
        elif conflict.remote_timestamp == conflict.local_timestamp:
            # Tie-breaker on version
            if conflict.remote_version > conflict.local_version:
                winner = conflict.remote_value
                details = "Remote value chosen (higher version tie-breaker)."
            else:
                winner = conflict.local_value
                details = "Local value retained (equal timestamp / local tie-breaker)."
        else:
            winner = conflict.local_value
            details = "Local value retained (more recent timestamp)."

        return ResolutionResult(
            conflict_id=conflict.conflict_id,
            entity_id=conflict.entity_id,
            strategy_used=ConflictResolutionStrategy.LAST_WRITE_WINS,
            resolved_value=winner,
            requires_manual_intervention=False,
            details=details,
        )

    def _resolve_vector_clock(self, conflict: ReplicationConflict) -> ResolutionResult:
        """Vector clock causality comparison."""
        local_vc = conflict.local_vector_clock
        remote_vc = conflict.remote_vector_clock

        all_keys = set(local_vc.keys()).union(set(remote_vc.keys()))
        local_dominates = True
        remote_dominates = True

        for k in all_keys:
            l_val = local_vc.get(k, 0)
            r_val = remote_vc.get(k, 0)
            if l_val < r_val:
                local_dominates = False
            if r_val < l_val:
                remote_dominates = False

        if local_dominates and not remote_dominates:
            return ResolutionResult(
                conflict_id=conflict.conflict_id,
                entity_id=conflict.entity_id,
                strategy_used=ConflictResolutionStrategy.VECTOR_CLOCK,
                resolved_value=conflict.local_value,
                details="Local vector clock causally dominates remote.",
            )
        elif remote_dominates and not local_dominates:
            return ResolutionResult(
                conflict_id=conflict.conflict_id,
                entity_id=conflict.entity_id,
                strategy_used=ConflictResolutionStrategy.VECTOR_CLOCK,
                resolved_value=conflict.remote_value,
                details="Remote vector clock causally dominates local.",
            )
        else:
            # Concurrent divergence -> fallback to LWW or Manual
            return self._resolve_lww(conflict)

    def _resolve_quorum(self, conflict: ReplicationConflict) -> ResolutionResult:
        """Quorum-based consensus resolution."""
        votes = conflict.quorum_votes
        if not votes:
            return self._resolve_lww(conflict)

        # Count frequencies
        counts: Dict[str, int] = {}
        for val in votes.values():
            val_str = str(val)
            counts[val_str] = counts.get(val_str, 0) + 1

        majority_val_str, count = max(counts.items(), key=lambda x: x[1])
        total_votes = len(votes)

        if count > total_votes / 2.0:
            # Find original value matching string
            chosen = next(v for v in votes.values() if str(v) == majority_val_str)
            return ResolutionResult(
                conflict_id=conflict.conflict_id,
                entity_id=conflict.entity_id,
                strategy_used=ConflictResolutionStrategy.QUORUM_BASED,
                resolved_value=chosen,
                details=f"Quorum majority consensus reached ({count}/{total_votes} nodes).",
            )
        else:
            return ResolutionResult(
                conflict_id=conflict.conflict_id,
                entity_id=conflict.entity_id,
                strategy_used=ConflictResolutionStrategy.QUORUM_BASED,
                resolved_value=conflict.local_value,
                requires_manual_intervention=True,
                details="Quorum split; no majority vote achieved.",
            )
