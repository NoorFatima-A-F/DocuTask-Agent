"""Test Privacy Masking, Redaction, Tokenization & Access Tracking."""

import pytest
from app.data_governance.privacy.masking import PrivacyMaskingEngine
from app.data_governance.access.tracking import DataAccessTracker, DataActionType
from app.data_governance.access.permissions import DataAccessPermissionEnforcer
from app.data_governance.registry.models import DataAsset, ClassificationLevel, AssetType, DataOwnership


def test_privacy_masking_redaction_and_tokenization():
    """Verify masking, redaction, and reversible tokenization."""
    privacy = PrivacyMaskingEngine()

    text = "User email is john.doe@company.com and SSN is 123-45-6789."

    # 1. Masking
    masked = privacy.mask(text)
    assert "j***@company.com" in masked
    assert "***-**-6789" in masked

    # 2. Redaction
    redacted = privacy.redact(text)
    assert "[REDACTED]" in redacted
    assert "john.doe@company.com" not in redacted

    # 3. Tokenization & Reversible Detokenization
    tokenized = privacy.tokenize(text)
    assert "TOK_EMAIL_" in tokenized
    assert "TOK_SSN_" in tokenized

    detokenized = privacy.detokenize(tokenized)
    assert detokenized == text


def test_data_access_tracking_and_permission_enforcement():
    """Verify access tracking and clearance-level permission checks."""
    tracker = DataAccessTracker()
    enforcer = DataAccessPermissionEnforcer()

    owner = DataOwnership(owner_user_id="user_admin", responsible_team="SecOps", department="Security")
    asset = DataAsset(
        asset_id="asset_conf_1",
        organization_id="org_alpha",
        workspace_id="ws_1",
        name="Secret Key Store",
        asset_type=AssetType.DOCUMENT,
        source="vault",
        location_uri="vault://secret",
        owner=owner,
        creator_id="user_admin",
        classification=ClassificationLevel.RESTRICTED,
    )

    # Clearance check: PUBLIC clearance cannot access RESTRICTED asset
    assert enforcer.can_access(asset, user_clearance="PUBLIC", user_organization_id="org_alpha") is False
    # Clearance check: RESTRICTED clearance CAN access RESTRICTED asset
    assert enforcer.can_access(asset, user_clearance="RESTRICTED", user_organization_id="org_alpha") is True
    # Cross-tenant check: Different org cannot access
    assert enforcer.can_access(asset, user_clearance="RESTRICTED", user_organization_id="org_beta") is False

    # Track access
    event = tracker.record_access(
        asset_id=asset.asset_id,
        organization_id="org_alpha",
        user_id="user_auditor",
        action=DataActionType.READ,
        purpose="Security Audit",
    )
    assert event.event_id.startswith("acc_")
    assert len(tracker.get_asset_access_history(asset.asset_id)) == 1
