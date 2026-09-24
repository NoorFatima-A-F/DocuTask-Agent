"""Rolling Deployment Strategy with batch sizing and instance health validation."""

from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class RollingStrategyConfig:
    """Configuration for rolling updates."""
    batch_size: int = 2
    max_unavailable: int = 1
    health_check_interval_seconds: float = 0.5


class RollingDeploymentStrategy:
    """Executes a rolling replacement across service worker instances."""

    def __init__(self, config: Optional[RollingStrategyConfig] = None) -> None:
        self.config = config or RollingStrategyConfig()

    def execute(
        self,
        total_instances: int,
        upgrade_batch_fn: Callable[[int, int], bool],
        health_check_fn: Optional[Callable[[], bool]] = None,
    ) -> bool:
        """Upgrade instances in batches while maintaining availability."""
        upgraded = 0
        while upgraded < total_instances:
            batch_count = min(self.config.batch_size, total_instances - upgraded)
            ok = upgrade_batch_fn(upgraded, batch_count)
            if not ok:
                return False

            if health_check_fn and not health_check_fn():
                return False

            upgraded += batch_count

        return True
