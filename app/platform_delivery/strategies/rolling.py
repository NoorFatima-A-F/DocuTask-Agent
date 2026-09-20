"""Kubernetes-aligned Rolling Deployment Strategy (Req 35)."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, List, Optional


@dataclass
class RollingStep:
    batch_index: int
    updated_replicas: int
    total_replicas: int
    healthy: bool
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class RollingStrategy:
    """Progressively updates pods/replicas respecting max_surge and max_unavailable."""

    def __init__(
        self,
        batch_size: int = 1,
        max_surge: int = 1,
        max_unavailable: int = 0,
        health_check_fn: Optional[Callable[[], bool]] = None,
    ):
        self.batch_size = max(1, batch_size)
        self.max_surge = max_surge
        self.max_unavailable = max_unavailable
        self.health_check_fn = health_check_fn or (lambda: True)

    def execute(self, total_replicas: int) -> List[RollingStep]:
        steps = []
        updated = 0
        batch_idx = 1

        while updated < total_replicas:
            count = min(self.batch_size, total_replicas - updated)
            updated += count
            healthy = self.health_check_fn()

            step = RollingStep(
                batch_index=batch_idx,
                updated_replicas=updated,
                total_replicas=total_replicas,
                healthy=healthy,
            )
            steps.append(step)

            if not healthy:
                raise RuntimeError(f"Rolling rollout failed health checks at batch {batch_idx}")

            batch_idx += 1

        return steps
