"""Test Data Retention Policies and Legal Hold Preservation."""

import pytest
from app.data_governance.registry.models import AssetType, DataOwnership, AssetLifecycleState
from app.data_governance.registry.service import DataGovernanceRegistryService
from app.data_governance.assets.lifecycle import AssetLifecycleManager
from app.data_governance.retention.scheduler import RetentionAndLegalHoldEngine
from app.data_governance.retention.policies import DEFAULT_RETENTION_POLICIES


def test_retention_and_legal_hold_blocking():
    """Verify legal hold blocks deletion and archival transitions."""
    service = DataGovernanceRegistryService()
    lifecycle = AssetLifecycleManager()
    retention_engine = RetentionAndLegalHoldEngine()
    org_id = "org_legal_test"

    owner = DataOwnership(owner_user_id="user_legal", responsible_team="Legal", department="Legal")
    asset = service.register_asset(
        asset_id="asset_disputed_contract",
        organization_id=org_id,
        workspace_id="ws_legal",
        name="Disputed Vendor Agreement.pdf",
        asset_type=AssetType.DOCUMENT,
        source="upload",
        location_uri="storage://legal/dispute.pdf",
        owner=owner,
        creator_id="user_legal",
    )
    lifecycle.transition(asset, AssetLifecycleState.ACTIVE)

    # 1. Place Legal Hold
    hold = retention_engine.apply_legal_hold(
        organization_id=org_id,
        matter_name="Vendor Litigation 2026",
        reason="Preservation subpoena",
        placed_by="attorney_smith",
        affected_assets=[asset],
    )
    assert asset.is_legal_hold is True
    assert hold.is_active is True

    # 2. Expiration check must return False while under Legal Hold
    policy = DEFAULT_RETENTION_POLICIES["temp_cache"]
    assert retention_engine.is_asset_expired(asset, policy) is False

    # 3. Attempting deletion or archival MUST fail with ValueError
    with pytest.raises(ValueError, match="Active Legal Hold in effect"):
        lifecycle.transition(asset, AssetLifecycleState.ARCHIVED)

    # 4. Release Legal Hold
    retention_engine.release_legal_hold(hold.hold_id, [asset])
    assert asset.is_legal_hold is False

    # 5. Transition succeeds now
    lifecycle.transition(asset, AssetLifecycleState.ARCHIVED)
    assert asset.status == AssetLifecycleState.ARCHIVED
