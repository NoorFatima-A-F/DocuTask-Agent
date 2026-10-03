"""
Log Retention & Lifecycle Archival.

Enforces compliance-driven tiered log retention policies (hot, warm, cold storage),
compression, and legal hold exemptions.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set
from pydantic import BaseModel, Field

from app.infrastructure.observability.logs.models import LogRecord

logger = logging.getLogger("infrastructure.observability.logs.retention")


class LogRetentionPolicy(BaseModel):
    """Retention rule configuration per tenant or environment."""
    policy_id: str
    tenant_id: str = "global"
    hot_retention_days: int = Field(default=7, ge=1)
    warm_retention_days: int = Field(default=30, ge=1)
    cold_retention_days: int = Field(default=365, ge=1)
    legal_hold_active: bool = False
    compression_enabled: bool = True


class LogRetentionManager:
    """
    Manages log pruning and legal hold protections.
    """

    def __init__(self, default_retention_days: int = 30) -> None:
        self.default_retention_days = default_retention_days
        self._policies: Dict[str, LogRetentionPolicy] = {}  # tenant_id -> LogRetentionPolicy
        self._legal_holds: Set[str] = set()  # tenant_ids under active legal hold

    def set_policy(self, policy: LogRetentionPolicy) -> None:
        self._policies[policy.tenant_id] = policy
        if policy.legal_hold_active:
            self._legal_holds.add(policy.tenant_id)
        else:
            self._legal_holds.discard(policy.tenant_id)

    def set_legal_hold(self, tenant_id: str, active: bool = True) -> None:
        if active:
            self._legal_holds.add(tenant_id)
        else:
            self._legal_holds.discard(tenant_id)

    def is_under_legal_hold(self, tenant_id: str) -> bool:
        return tenant_id in self._legal_holds

    def should_retain(self, record: LogRecord, now: Optional[datetime] = None) -> bool:
        """Evaluate whether a log record should be kept or pruned."""
        if self.is_under_legal_hold(record.tenant_id):
            return True  # Retain indefinitely while under legal hold

        policy = self._policies.get(record.tenant_id)
        max_days = policy.cold_retention_days if policy else self.default_retention_days

        current_time = now or datetime.now(timezone.utc)
        age_days = (current_time - record.timestamp).total_seconds() / 86400.0
        return age_days <= max_days
