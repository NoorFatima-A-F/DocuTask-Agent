"""Blue-Green Zero-Downtime Deployment Strategy."""
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional
from ..core.exceptions import StrategyExecutionException


class BlueGreenPhase(str, Enum):
    """Phases in a Blue-Green deployment."""
    IDLE = "IDLE"
    GREEN_PROVISIONED = "GREEN_PROVISIONED"
    GREEN_VERIFIED = "GREEN_VERIFIED"
    TRAFFIC_SWITCHED = "TRAFFIC_SWITCHED"
    BLUE_STANDBY = "BLUE_STANDBY"
    BLUE_DECOMMISSIONED = "BLUE_DECOMMISSIONED"
    ROLLED_BACK = "ROLLED_BACK"


@dataclass
class EnvironmentSlot:
    """State of an environment slot (Blue or Green)."""
    name: str  # "blue" or "green"
    release_id: Optional[str] = None
    is_live: bool = False
    is_healthy: bool = False
    traffic_pct: float = 0.0


class BlueGreenStrategy:
    """Orchestrates zero-downtime blue/green environment transitions."""

    def __init__(
        self,
        health_check_fn: Optional[Callable[[str], bool]] = None,
    ):
        self.health_check_fn = health_check_fn or (lambda slot: True)
        self.blue = EnvironmentSlot(name="blue", is_live=True, traffic_pct=100.0, is_healthy=True)
        self.green = EnvironmentSlot(name="green", is_live=False, traffic_pct=0.0, is_healthy=False)
        self.phase = BlueGreenPhase.IDLE

    @property
    def live_slot(self) -> EnvironmentSlot:
        """Returns the currently active live environment slot."""
        return self.blue if self.blue.is_live else self.green

    @property
    def idle_slot(self) -> EnvironmentSlot:
        """Returns the standby environment slot."""
        return self.green if self.blue.is_live else self.blue

    def provision_standby(self, new_release_id: str) -> None:
        """Provisions the inactive slot with the new release."""
        standby = self.idle_slot
        standby.release_id = new_release_id
        standby.is_healthy = False
        standby.traffic_pct = 0.0
        self.phase = BlueGreenPhase.GREEN_PROVISIONED

    def verify_standby(self) -> bool:
        """Runs pre-cutover verification against the standby slot."""
        standby = self.idle_slot
        if not standby.release_id:
            raise StrategyExecutionException("Cannot verify unprovisioned standby environment")

        is_healthy = self.health_check_fn(standby.name)
        standby.is_healthy = is_healthy
        if not is_healthy:
            raise StrategyExecutionException(f"Health verification failed on {standby.name} environment")

        self.phase = BlueGreenPhase.GREEN_VERIFIED
        return True

    def cutover(self) -> None:
        """Atomically shifts 100% of user traffic to the verified slot."""
        if self.phase != BlueGreenPhase.GREEN_VERIFIED:
            raise StrategyExecutionException(f"Cannot cutover traffic in state {self.phase.value}; must be GREEN_VERIFIED")

        old_live = self.live_slot
        new_live = self.idle_slot

        new_live.is_live = True
        new_live.traffic_pct = 100.0
        old_live.is_live = False
        old_live.traffic_pct = 0.0

        self.phase = BlueGreenPhase.TRAFFIC_SWITCHED

    def rollback(self) -> None:
        """Instantly reverts traffic back to the standby slot."""
        old_live = self.live_slot
        target = self.idle_slot

        if not target.is_healthy:
            raise StrategyExecutionException("Cannot rollback: target slot is marked unhealthy")

        target.is_live = True
        target.traffic_pct = 100.0
        old_live.is_live = False
        old_live.traffic_pct = 0.0

        self.phase = BlueGreenPhase.ROLLED_BACK

    def decommission_standby(self) -> None:
        """Decommissions old release running on the inactive slot."""
        standby = self.idle_slot
        standby.release_id = None
        standby.is_healthy = False
        self.phase = BlueGreenPhase.BLUE_DECOMMISSIONED
