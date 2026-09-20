"""
Enterprise Rolling Upgrade & State Migration Test Suite.
Validates:
- Blue/Green slot targeting and switching
- Upgrade rollback on failure
- State migration pipeline application across version schemas
"""

import pytest
from app.agents.runtime.enterprise.migration_manager import MigrationManager
from app.agents.runtime.enterprise.rolling_upgrade import (
    DeploymentSlot,
    RollingUpgradeManager,
    UpgradeStatus,
)


def test_blue_green_upgrade_switch():
    mgr = RollingUpgradeManager(initial_slot=DeploymentSlot.BLUE)
    assert mgr.active_slot == DeploymentSlot.BLUE
    assert mgr.status == UpgradeStatus.IDLE

    target_slot = mgr.begin_upgrade(target_version="23.1.0")
    assert target_slot == DeploymentSlot.GREEN
    assert mgr.status == UpgradeStatus.PREPARING

    switched_slot = mgr.complete_switch()
    assert switched_slot == DeploymentSlot.GREEN
    assert mgr.active_slot == DeploymentSlot.GREEN
    assert mgr.status == UpgradeStatus.SWITCHED


def test_rolling_upgrade_rollback():
    mgr = RollingUpgradeManager(initial_slot=DeploymentSlot.BLUE)
    mgr.begin_upgrade("23.1.0")
    mgr.complete_switch()
    assert mgr.active_slot == DeploymentSlot.GREEN

    # Trigger rollback
    rolled_back = mgr.rollback(reason="Canary error rate high")
    assert rolled_back == DeploymentSlot.BLUE
    assert mgr.active_slot == DeploymentSlot.BLUE
    assert mgr.status == UpgradeStatus.ROLLED_BACK


def test_state_migration_pipeline():
    mgr = MigrationManager()

    # Step 1: Add schema_version
    def step1(data: dict) -> dict:
        data["schema_version"] = 1
        data["full_name"] = f"{data.pop('first_name', '')} {data.pop('last_name', '')}".strip()
        return data

    # Step 2: Convert status
    def step2(data: dict) -> dict:
        data["schema_version"] = 2
        data["active"] = data.get("status") == "ENABLED"
        return data

    mgr.register_step(step1)
    mgr.register_step(step2)

    raw_state = {
        "first_name": "Jane",
        "last_name": "Doe",
        "status": "ENABLED",
    }

    migrated = mgr.migrate_session_state(raw_state)
    assert migrated["schema_version"] == 2
    assert migrated["full_name"] == "Jane Doe"
    assert migrated["active"] is True
    assert "first_name" not in migrated
