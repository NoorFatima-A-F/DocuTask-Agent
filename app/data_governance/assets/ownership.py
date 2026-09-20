"""Data Ownership & Stewardship Management (Phase 8B)."""

from __future__ import annotations

from typing import Dict, List, Optional
from app.data_governance.registry.models import DataOwnership, DataAsset


class DataOwnershipManager:
    """Manages enterprise data ownership and stewardship assignments."""

    def __init__(self):
        # asset_id -> DataOwnership
        self._ownerships: Dict[str, DataOwnership] = {}

    def assign_ownership(
        self,
        asset_id: str,
        owner_user_id: str,
        responsible_team: str,
        department: str,
        data_steward_id: Optional[str] = None,
        approver_id: Optional[str] = None,
        business_purpose: str = "Enterprise Operations",
    ) -> DataOwnership:
        """Assign or update ownership and stewardship for an asset."""
        ownership = DataOwnership(
            owner_user_id=owner_user_id,
            responsible_team=responsible_team,
            department=department,
            data_steward_id=data_steward_id,
            approver_id=approver_id,
            business_purpose=business_purpose,
        )
        self._ownerships[asset_id] = ownership
        return ownership

    def get_ownership(self, asset_id: str) -> Optional[DataOwnership]:
        """Retrieve ownership metadata."""
        return self._ownerships.get(asset_id)
