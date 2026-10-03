"""Test Data Asset Registry and 8-State Lifecycle FSM."""

from app.data_governance.registry.models import (
    AssetType,
    ClassificationLevel,
    AssetLifecycleState,
    DataOwnership,
)
from app.data_governance.registry.repository import DataAssetRepository
from app.data_governance.registry.service import DataGovernanceRegistryService
from app.data_governance.assets.lifecycle import AssetLifecycleManager


def test_data_asset_registration_and_versioning():
    """Verify asset registration, checksum calculation, and version snapshotting."""
    repo = DataAssetRepository()
    service = DataGovernanceRegistryService(repository=repo)

    owner = DataOwnership(
        owner_user_id="user_alice",
        responsible_team="Finance AI",
        department="Finance",
        data_steward_id="user_steward_bob",
    )

    asset = service.register_asset(
        asset_id="asset_invoice_001",
        organization_id="org_acme",
        workspace_id="ws_finance",
        name="Q3 Vendor Invoice.pdf",
        asset_type=AssetType.DOCUMENT,
        source="s3://invoices/q3_001.pdf",
        location_uri="storage://invoices/q3_001.pdf",
        owner=owner,
        creator_id="user_alice",
        classification=ClassificationLevel.CONFIDENTIAL,
        content_for_checksum="Sample Invoice Content v1",
        size_bytes=1024,
    )

    assert asset.asset_id == "asset_invoice_001"
    assert asset.version == 1
    assert asset.checksum_sha256 != ""
    assert asset.status == AssetLifecycleState.REGISTERED

    # Increment version
    updated_asset = service.create_version(
        asset_id="asset_invoice_001",
        organization_id="org_acme",
        updated_by="user_alice",
        change_summary="Corrected line item amounts",
        new_content_for_checksum="Sample Invoice Content v2",
        new_size_bytes=1050,
    )

    assert updated_asset.version == 2
    assert updated_asset.status == AssetLifecycleState.UPDATED
    versions = service.list_versions("asset_invoice_001")
    assert len(versions) == 2
    assert versions[1].change_summary == "Corrected line item amounts"


def test_asset_lifecycle_transitions_and_audit():
    """Verify 8-state FSM lifecycle transitions and audit trail logging."""
    lifecycle = AssetLifecycleManager()
    repo = DataAssetRepository()
    service = DataGovernanceRegistryService(repository=repo)

    owner = DataOwnership(owner_user_id="user_1", responsible_team="Data", department="IT")
    asset = service.register_asset(
        asset_id="asset_contract_99",
        organization_id="org_acme",
        workspace_id="ws_legal",
        name="Master Services Agreement.docx",
        asset_type=AssetType.DOCUMENT,
        source="upload",
        location_uri="storage://legal/msa.docx",
        owner=owner,
        creator_id="user_1",
    )

    # REGISTERED -> CLASSIFIED
    lifecycle.transition(asset, AssetLifecycleState.CLASSIFIED, actor_id="classifier_daemon")
    assert asset.status == AssetLifecycleState.CLASSIFIED

    # CLASSIFIED -> ACTIVE
    lifecycle.transition(asset, AssetLifecycleState.ACTIVE, actor_id="user_1")
    assert asset.status == AssetLifecycleState.ACTIVE

    # ACTIVE -> ARCHIVED
    lifecycle.transition(asset, AssetLifecycleState.ARCHIVED, actor_id="retention_daemon")
    assert asset.status == AssetLifecycleState.ARCHIVED

    # Verify audit trail
    trail = lifecycle.get_audit_trail("asset_contract_99")
    assert len(trail) == 3
    assert trail[0].from_state == AssetLifecycleState.REGISTERED
    assert trail[0].to_state == AssetLifecycleState.CLASSIFIED
