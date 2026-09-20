"""Blue-Green Deployment Strategy with Atomic Traffic Cutover."""

from dataclasses import dataclass
from typing import Callable, Optional


class BlueGreenDeploymentStrategy:
    """Provisions a standalone Green environment, verifies health, and executes atomic cutover."""

    def execute(
        self,
        deploy_green_fn: Callable[[], bool],
        verify_green_fn: Callable[[], bool],
        switch_traffic_to_green_fn: Callable[[], bool],
        shutdown_blue_fn: Optional[Callable[[], bool]] = None,
    ) -> bool:
        """Run full blue/green transition."""
        # 1. Deploy new version to green
        if not deploy_green_fn():
            return False

        # 2. Comprehensive green environment verification
        if not verify_green_fn():
            return False

        # 3. Atomic router cutover
        if not switch_traffic_to_green_fn():
            return False

        # 4. Optional blue shutdown after grace period
        if shutdown_blue_fn:
            shutdown_blue_fn()

        return True
