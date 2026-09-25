"""Rolling Deployment Strategy Engine."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, List, Optional
from ..core.exceptions import StrategyExecutionException


@dataclass
class RollingStepResult:
    """Outcome of a single rolling batch step."""
    batch_index: int
    updated_replicas: int
    total_replicas: int
    healthy: bool
    details: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class RollingStrategy:
    """Executes progressive rolling update across worker/pod replicas."""

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

    def execute(
        self,
        total_replicas: int,
        step_callback: Optional[Callable[[RollingStepResult], None]] = None,
    ) -> List[RollingStepResult]:
        """Executes the rolling rollout in batches."""
        if total_replicas <= 0:
            raise StrategyExecutionException("Total replicas must be greater than 0")

        results: List[RollingStepResult] = []
        current_updated = 0
        batch_idx = 1

        while current_updated < total_replicas:
            step_count = min(self.batch_size, total_replicas - current_updated)
            current_updated += step_count

            # Run health check
            is_healthy = False
            try:
                is_healthy = self.health_check_fn()
            except Exception:
                is_healthy = False

            step_res = RollingStepResult(
                batch_index=batch_idx,
                updated_replicas=current_updated,
                total_replicas=total_replicas,
                healthy=is_healthy,
                details=f"Batch {batch_idx}: updated {step_count} replicas ({current_updated}/{total_replicas})",
            )
            results.append(step_res)

            if step_callback:
                step_callback(step_res)

            if not is_healthy:
                raise StrategyExecutionException(
                    f"Rolling strategy failed health verification at batch {batch_idx} ({current_updated}/{total_replicas} replicas)"
                )

            batch_idx += 1

        return results
