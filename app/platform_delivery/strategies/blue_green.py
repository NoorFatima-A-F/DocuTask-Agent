"""Blue-Green Deployment Strategy with Standby Rollback Retention (Req 38)."""
from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class EnvironmentSlot:
    name: str  # "blue" or "green"
    release_version: str
    traffic_percentage: float
    is_healthy: bool


class BlueGreenStrategy:
    """Manages active and standby environment slots with instantaneous traffic switching."""

    def __init__(self, health_fn: Optional[Callable[[str], bool]] = None):
        self.health_fn = health_fn or (lambda slot: True)
        self.blue = EnvironmentSlot(name="blue", release_version="1.0.0", traffic_percentage=100.0, is_healthy=True)
        self.green = EnvironmentSlot(name="green", release_version="", traffic_percentage=0.0, is_healthy=False)

    @property
    def active_slot(self) -> EnvironmentSlot:
        return self.blue if self.blue.traffic_percentage > 0 else self.green

    @property
    def standby_slot(self) -> EnvironmentSlot:
        return self.green if self.blue.traffic_percentage > 0 else self.blue

    def deploy_to_standby(self, new_version: str) -> None:
        standby = self.standby_slot
        standby.release_version = new_version
        standby.is_healthy = self.health_fn(standby.name)
        if not standby.is_healthy:
            raise RuntimeError(f"Standby slot '{standby.name}' failed pre-cutover health verification")

    def switch_traffic(self) -> None:
        new_active = self.standby_slot
        old_active = self.active_slot

        if not new_active.is_healthy:
            raise RuntimeError("Cannot cutover traffic to unhealthy standby slot")

        new_active.traffic_percentage = 100.0
        old_active.traffic_percentage = 0.0

    def rollback_traffic(self) -> None:
        # Revert back instantly to previous slot
        current_active = self.active_slot
        previous_active = self.standby_slot

        previous_active.traffic_percentage = 100.0
        current_active.traffic_percentage = 0.0
