"""
Rolling Upgrade Manager.
Coordinates Blue/Green zero-downtime platform upgrades and automated rollback on upgrade failures.
"""

from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class DeploymentSlot(str, Enum):
    """Active deployment color."""
    BLUE = "BLUE"
    GREEN = "GREEN"


class UpgradeStatus(str, Enum):
    """Status of a rolling upgrade."""
    IDLE = "IDLE"
    PREPARING = "PREPARING"
    DRAINING_OLD = "DRAINING_OLD"
    SWITCHED = "SWITCHED"
    ROLLED_BACK = "ROLLED_BACK"


class RollingUpgradeManager:
    """Coordinates zero-downtime rolling upgrades across Blue/Green slots."""

    def __init__(self, initial_slot: DeploymentSlot = DeploymentSlot.BLUE) -> None:
        self.active_slot = initial_slot
        self.status = UpgradeStatus.IDLE
        self._target_version: Optional[str] = None

    def begin_upgrade(self, target_version: str) -> DeploymentSlot:
        """Prepares alternate deployment slot for new version."""
        self.status = UpgradeStatus.PREPARING
        self._target_version = target_version
        target_slot = (
            DeploymentSlot.GREEN
            if self.active_slot == DeploymentSlot.BLUE
            else DeploymentSlot.BLUE
        )
        return target_slot

    def complete_switch(self) -> DeploymentSlot:
        """Switches live traffic to target slot."""
        self.active_slot = (
            DeploymentSlot.GREEN
            if self.active_slot == DeploymentSlot.BLUE
            else DeploymentSlot.BLUE
        )
        self.status = UpgradeStatus.SWITCHED
        return self.active_slot

    def rollback(self, reason: str = "Health check failed") -> DeploymentSlot:
        """Rolls back live traffic to previous slot."""
        self.active_slot = (
            DeploymentSlot.GREEN
            if self.active_slot == DeploymentSlot.BLUE
            else DeploymentSlot.BLUE
        )
        self.status = UpgradeStatus.ROLLED_BACK
        return self.active_slot
