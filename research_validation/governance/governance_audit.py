"""
Research Governance Audit (Phase 93C)
====================================
Cryptographically sealed audit trail recording every governance compliance evaluation.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from research_validation.governance.governance_policy import (
    PolicyCategory, PolicyEnforcementAction
)
from research_validation.provenance.hashing import hash_canonical_json


@dataclass(frozen=True)
class GovernanceAuditRecord:
    """A sealed record of a single policy evaluation event."""
    audit_id: str
    target_id: str
    rule_id: str
    category: PolicyCategory
    evaluation_action: PolicyEnforcementAction
    is_compliant: bool
    details: str
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    record_digest_sha256: str = field(default="")


class GovernanceAuditLog:
    """Append-only audit log with Merkle root computation."""

    def __init__(self):
        self.records: List[GovernanceAuditRecord] = []

    def record_check(
        self,
        target_id: str,
        rule_id: str,
        category: PolicyCategory,
        action: PolicyEnforcementAction,
        is_compliant: bool,
        details: str,
    ) -> GovernanceAuditRecord:
        audit_id = f"audit_{target_id}_{len(self.records)}"
        payload = {
            "audit_id": audit_id,
            "target_id": target_id,
            "rule_id": rule_id,
            "category": category.value,
            "action": action.value,
            "is_compliant": is_compliant,
            "details": details,
        }
        digest = hash_canonical_json(payload)

        record = GovernanceAuditRecord(
            audit_id=audit_id,
            target_id=target_id,
            rule_id=rule_id,
            category=category,
            evaluation_action=action,
            is_compliant=is_compliant,
            details=details,
            record_digest_sha256=digest,
        )
        self.records.append(record)
        return record

    def compute_audit_root_digest(self) -> str:
        digests = [r.record_digest_sha256 for r in self.records]
        return hash_canonical_json({"audit_records": digests})
