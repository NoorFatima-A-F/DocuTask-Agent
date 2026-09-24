"""Data Access Permission & Policy Enforcer (Phase 8B)."""

from __future__ import annotations

from app.data_governance.registry.models import DataAsset, ClassificationLevel


class DataAccessPermissionEnforcer:
    """Validates user and agent permissions before granting access to governed data assets."""

    # Maximum classification allowed per clearance level
    CLEARANCE_LEVELS = {
        "PUBLIC": {ClassificationLevel.PUBLIC},
        "INTERNAL": {ClassificationLevel.PUBLIC, ClassificationLevel.INTERNAL},
        "CONFIDENTIAL": {ClassificationLevel.PUBLIC, ClassificationLevel.INTERNAL, ClassificationLevel.CONFIDENTIAL},
        "RESTRICTED": {ClassificationLevel.PUBLIC, ClassificationLevel.INTERNAL, ClassificationLevel.CONFIDENTIAL, ClassificationLevel.RESTRICTED},
        "HIGHLY_RESTRICTED": {ClassificationLevel.PUBLIC, ClassificationLevel.INTERNAL, ClassificationLevel.CONFIDENTIAL, ClassificationLevel.RESTRICTED, ClassificationLevel.HIGHLY_RESTRICTED},
    }

    def can_access(
        self,
        asset: DataAsset,
        user_clearance: str,
        user_organization_id: str,
    ) -> bool:
        """Evaluate if user is authorized to access the asset."""
        # Enforce organization isolation
        if asset.organization_id != user_organization_id:
            return False

        allowed_classifications = self.CLEARANCE_LEVELS.get(user_clearance.upper(), set())
        return asset.classification in allowed_classifications
