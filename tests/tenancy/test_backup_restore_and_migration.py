"""Test Backup, Restore, and Migration Engines."""

import pytest
from app.tenancy.core.models import Region
from app.tenancy.organizations.manager import OrganizationManager
from app.tenancy.backup.engine import TenantBackupRestoreEngine
from app.tenancy.migration.engine import TenantMigrationEngine


def test_tenant_backup_and_restore():
    """Verify cryptographic backup creation and verified restore."""
    backup_engine = TenantBackupRestoreEngine()
    org_id = "org_backup_test"

    payload = {
        "workflows": ["wf_1", "wf_2"],
        "agents": ["agent_supervisor"],
        "policies": {"allow_all": True},
    }

    snapshot = backup_engine.create_snapshot(
        organization_id=org_id,
        scope="FULL_ORGANIZATION",
        payload=payload,
    )

    assert snapshot.checksum != ""
    assert snapshot.size_bytes > 0

    restore_result = backup_engine.restore_snapshot(snapshot.snapshot_id)
    assert restore_result["status"] == "RESTORED"
    assert restore_result["organization_id"] == org_id


def test_tenant_migration_and_cloning():
    """Verify tenant export, clone, and regional data residency transfer."""
    org_mgr = OrganizationManager()
    backup_engine = TenantBackupRestoreEngine()
    migration_engine = TenantMigrationEngine(org_mgr, backup_engine)

    org = org_mgr.create_organization(
        org_id="org_source_1",
        name="Source Corp",
        owner_id="user_owner",
        region=Region.US_EAST,
    )

    # 1. Export
    export_info = migration_engine.export_tenant("org_source_1")
    assert export_info["organization_id"] == "org_source_1"

    # 2. Clone
    clone_info = migration_engine.clone_organization(
        source_org_id="org_source_1",
        target_org_id="org_clone_1",
        new_name="Clone Corp",
        new_owner_id="user_clone_owner",
    )
    assert clone_info["status"] == "CLONED"
    assert clone_info["new_organization_id"] == "org_clone_1"

    # 3. Migrate Region to EU
    migrated_info = migration_engine.migrate_region("org_source_1", Region.EU_WEST)
    assert migrated_info["status"] == "MIGRATED"
    assert migrated_info["target_region"] == Region.EU_WEST.value
    assert org_mgr.get_organization("org_source_1").region == Region.EU_WEST
