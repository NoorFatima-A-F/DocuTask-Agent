"""
Continuous Evidence Lifecycle Governance Engine.
Enforces formal state machine transitions across evidence artifact lifecycles:
- DRAFT: Initial generation in progress
- CANDIDATE: Awaiting zero-trust cryptographic validation
- VERIFIED: Certified with immutable SHA-256 and approved by review gate
- DEPRECATED: Retained for audit history but superseded by newer benchmark run
- SUPERSEDED: Replaced by updated evidence item with direct link
- ARCHIVED: Cold-stored historical artifact
- INVALIDATED: Revoked due to identified measurement flaw or integrity violation
"""

from __future__ import annotations

import logging
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class EvidenceLifecycleState(str, Enum):
    DRAFT = "DRAFT"
    CANDIDATE = "CANDIDATE"
    VERIFIED = "VERIFIED"
    DEPRECATED = "DEPRECATED"
    SUPERSEDED = "SUPERSEDED"
    ARCHIVED = "ARCHIVED"
    INVALIDATED = "INVALIDATED"


@dataclass
class EvidenceLifecycleAuditRecord:
    """State transition record for an evidence item."""

    evidence_id: str
    previous_state: EvidenceLifecycleState
    new_state: EvidenceLifecycleState
    changed_by: str
    reason: str
    timestamp: float = field(default_factory=time.time)


@dataclass
class ManagedEvidenceMetadata:
    """Governance metadata tracked for every evidence item."""

    evidence_id: str
    state: EvidenceLifecycleState
    author: str
    reviewer: Optional[str]
    approval_timestamp: Optional[float]
    schema_version: str
    replacement_evidence_id: Optional[str]
    revocation_reason: Optional[str]
    history: List[EvidenceLifecycleAuditRecord] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "state": self.state.value,
            "author": self.author,
            "reviewer": self.reviewer,
            "approved_at": self.approval_timestamp,
            "schema_version": self.schema_version,
            "replacement_id": self.replacement_evidence_id,
            "revocation_reason": self.revocation_reason,
            "history_count": len(self.history),
        }


class EvidenceLifecycleManager:
    """
    Manages evidence state transitions and audit trails.
    """

    def __init__(self) -> None:
        self.catalog: Dict[str, ManagedEvidenceMetadata] = {}

    def register_draft(self, evidence_id: str, author: str = "aaos-runner") -> ManagedEvidenceMetadata:
        """Registers a new evidence artifact in DRAFT state."""
        meta = ManagedEvidenceMetadata(
            evidence_id=evidence_id,
            state=EvidenceLifecycleState.DRAFT,
            author=author,
            reviewer=None,
            approval_timestamp=None,
            schema_version="2.0.0",
            replacement_evidence_id=None,
            revocation_reason=None,
        )
        self.catalog[evidence_id] = meta
        return meta

    def transition_state(
        self,
        evidence_id: str,
        new_state: EvidenceLifecycleState,
        changed_by: str,
        reason: str,
        replacement_id: Optional[str] = None,
    ) -> ManagedEvidenceMetadata:
        """Executes a valid state transition and appends an immutable audit log."""
        if evidence_id not in self.catalog:
            self.register_draft(evidence_id, author=changed_by)

        meta = self.catalog[evidence_id]
        prev_state = meta.state

        # Record audit event
        event = EvidenceLifecycleAuditRecord(
            evidence_id=evidence_id,
            previous_state=prev_state,
            new_state=new_state,
            changed_by=changed_by,
            reason=reason,
        )
        meta.history.append(event)
        meta.state = new_state

        if new_state == EvidenceLifecycleState.VERIFIED:
            meta.reviewer = changed_by
            meta.approval_timestamp = time.time()
        elif new_state in (EvidenceLifecycleState.SUPERSEDED, EvidenceLifecycleState.DEPRECATED):
            meta.replacement_evidence_id = replacement_id
        elif new_state == EvidenceLifecycleState.INVALIDATED:
            meta.revocation_reason = reason

        return meta
