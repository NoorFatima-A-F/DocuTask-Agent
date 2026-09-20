"""Unit tests for Database Migration Manager."""
import pytest
from app.deployment.core.exceptions import MigrationException
from app.deployment.migrations.database import MigrationManager
from app.deployment.migrations.schema import MigrationPhase, SchemaMigration
from app.deployment.migrations.validation import ExpandContractValidator


def test_expand_contract_validator_catches_unsafe_ddl():
    validator = ExpandContractValidator()

    # Unsafe EXPAND phase containing DROP COLUMN
    unsafe_mig = SchemaMigration(
        version="001",
        name="drop_old_column",
        phase=MigrationPhase.EXPAND,
        up_sql="ALTER TABLE users DROP COLUMN legacy_phone;",
        down_sql="ALTER TABLE users ADD COLUMN legacy_phone VARCHAR(50);",
    )
    with pytest.raises(MigrationException, match="Unsafe EXPAND phase"):
        validator.validate_migration(unsafe_mig)

    # Valid EXPAND phase
    valid_mig = SchemaMigration(
        version="002",
        name="add_email_verified",
        phase=MigrationPhase.EXPAND,
        up_sql="ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT FALSE;",
        down_sql="ALTER TABLE users DROP COLUMN email_verified;",
    )
    assert validator.validate_migration(valid_mig) is True


def test_migration_manager_apply_and_rollback():
    manager = MigrationManager()
    mig = SchemaMigration(
        version="001",
        name="create_documents_table",
        phase=MigrationPhase.EXPAND,
        up_sql="CREATE TABLE documents (id VARCHAR(50) PRIMARY KEY);",
        down_sql="DROP TABLE documents;",
    )
    manager.register_migration(mig)

    # Check pending
    pending = manager.get_pending_migrations("tenant_a")
    assert len(pending) == 1

    # Apply
    applied = manager.apply_migration("tenant_a", mig.migration_id)
    assert applied.applied_at is not None
    assert len(manager.get_applied_migrations("tenant_a")) == 1

    # Rollback
    rolled_back = manager.rollback_migration("tenant_a", mig.migration_id)
    assert len(manager.get_applied_migrations("tenant_a")) == 0
