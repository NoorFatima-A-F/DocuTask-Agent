"""Data Retention Scheduler & Legal Hold Platform (Phase 8B).

Enforces legal preservation holds and automated lifecycle expiry actions.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from app.data_governance.registry.models import DataAsset, AssetLifecycleState
from app.data_governance.retention.policies import RetentionPolicy, RetentionAction, DEFAULT_RETENTION_POLICIES


class LegalHold(BaseModel):
    """Legal preservation order preventing modification or deletion."""
    hold_id: str
    organization_id: str
    reason: str
    matter_name: str
    placed_by: str
    affected_asset_ids: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True


class RetentionAndLegalHoldEngine:
    """Evaluates retention schedules and enforces legal hold preservation."""

    def __init__(self, policies: Optional[Dict[str, RetentionPolicy]] = None):
        self.policies = policies or dict(DEFAULT_RETENTION_POLICIES)
        # hold_id -> LegalHold
        self._legal_holds: Dict[str, LegalHold] = {}

    def apply_legal_hold(
        self,
        organization_id: str,
        matter_name: str,
        reason: str,
        placed_by: str,
        affected_assets: List[DataAsset],
    ) -> LegalHold:
        """Place a legal hold across specified assets."""
        hold = LegalHold(
            hold_id=f"hold_{uuid.uuid4().hex[:8]}",
            organization_id=organization_id,
            matter_name=matter_name,
            reason=reason,
            placed_by=placed_by,
            affected_asset_ids=[a.asset_id for a in affected_assets],
            is_active=True,
        )

        for asset in affected_assets:
            asset.is_legal_hold = True

        self._legal_holds[hold.hold_id] = hold
        return hold

    def release_legal_hold(self, hold_id: str, assets: List[DataAsset]) -> None:
        """Release a legal hold."""
        hold = self._legal_holds.get(hold_id)
        if hold:
            hold.is_active = False
            for asset in assets:
                if asset.asset_id in hold.affected_asset_ids:
                    asset.is_legal_hold = False

    def is_asset_expired(self, asset: DataAsset, policy: RetentionPolicy) -> bool:
        """Check if an asset has exceeded its retention period."""
        if asset.is_legal_hold:
            return False  # Legal hold overrides expiration

        now = datetime.now(timezone.utc)
        age_days = (now - asset.created_at).total_seconds() / 86400.0
        return age_days >= policy.retention_days
