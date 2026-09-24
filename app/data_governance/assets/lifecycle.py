"""Asset 8-State Lifecycle Finite State Machine (Phase 8B).

Governs:
DISCOVERED -> REGISTERED -> CLASSIFIED -> ACTIVE -> UPDATED -> SUPERSEDED -> ARCHIVED -> DELETED
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List, Set
from pydantic import BaseModel, Field
from app.data_governance.registry.models import DataAsset, AssetLifecycleState


class AssetLifecycleEvent(BaseModel):
    """Immutable audit record of asset lifecycle transition."""
    asset_id: str
    organization_id: str
    from_state: AssetLifecycleState
    to_state: AssetLifecycleState
    actor_id: str
    reason: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AssetLifecycleManager:
    """Enforces valid lifecycle transitions and audit logging for data assets."""

    VALID_TRANSITIONS: Dict[AssetLifecycleState, Set[AssetLifecycleState]] = {
        AssetLifecycleState.DISCOVERED: {AssetLifecycleState.REGISTERED, AssetLifecycleState.DELETED},
        AssetLifecycleState.REGISTERED: {AssetLifecycleState.CLASSIFIED, AssetLifecycleState.ACTIVE, AssetLifecycleState.DELETED},
        AssetLifecycleState.CLASSIFIED: {AssetLifecycleState.ACTIVE, AssetLifecycleState.ARCHIVED, AssetLifecycleState.DELETED},
        AssetLifecycleState.ACTIVE: {AssetLifecycleState.UPDATED, AssetLifecycleState.SUPERSEDED, AssetLifecycleState.ARCHIVED, AssetLifecycleState.DELETED},
        AssetLifecycleState.UPDATED: {AssetLifecycleState.ACTIVE, AssetLifecycleState.SUPERSEDED, AssetLifecycleState.ARCHIVED, AssetLifecycleState.DELETED},
        AssetLifecycleState.SUPERSEDED: {AssetLifecycleState.ACTIVE, AssetLifecycleState.ARCHIVED, AssetLifecycleState.DELETED},
        AssetLifecycleState.ARCHIVED: {AssetLifecycleState.ACTIVE, AssetLifecycleState.DELETED},
        AssetLifecycleState.DELETED: set(),  # Terminal state
    }

    def __init__(self):
        self._audit_log: List[AssetLifecycleEvent] = []

    def can_transition(self, current: AssetLifecycleState, target: AssetLifecycleState) -> bool:
        """Check if transition is allowable."""
        return target in self.VALID_TRANSITIONS.get(current, set())

    def transition(
        self,
        asset: DataAsset,
        target_state: AssetLifecycleState,
        actor_id: str = "system",
        reason: str = "State transition",
    ) -> DataAsset:
        """Execute state transition with validation and audit logging."""
        if asset.is_legal_hold and target_state in (AssetLifecycleState.ARCHIVED, AssetLifecycleState.DELETED):
            raise ValueError(f"Cannot transition asset '{asset.asset_id}' to '{target_state.value}': Active Legal Hold in effect")

        if not self.can_transition(asset.status, target_state):
            raise ValueError(f"Invalid transition from '{asset.status.value}' to '{target_state.value}' for asset '{asset.asset_id}'")

        event = AssetLifecycleEvent(
            asset_id=asset.asset_id,
            organization_id=asset.organization_id,
            from_state=asset.status,
            to_state=target_state,
            actor_id=actor_id,
            reason=reason,
        )
        self._audit_log.append(event)

        asset.status = target_state
        asset.updated_at = datetime.now(timezone.utc)
        return asset

    def get_audit_trail(self, asset_id: str) -> List[AssetLifecycleEvent]:
        """Retrieve complete lifecycle audit history for an asset."""
        return [e for e in self._audit_log if e.asset_id == asset_id]
