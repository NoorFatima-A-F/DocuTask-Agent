"""Deployment Orchestrator coordinating execution workflows across deployment strategies."""

from typing import Callable, Optional
import logging
import threading

from .state import DeploymentRecord, DeploymentStatus, DeploymentStrategyType

logger = logging.getLogger("app.infrastructure.deployment.orchestrator")


class DeploymentOrchestrator:
    """Coordinates the step-by-step rollout of a deployment record."""

    def __init__(self) -> None:
        self._lock = threading.RLock()

    def execute_rollout(
        self,
        record: DeploymentRecord,
        health_checker: Optional[Callable[[], bool]] = None,
        strategy_executor: Optional[Callable[[DeploymentRecord, float], bool]] = None,
    ) -> bool:
        """Execute a progressive deployment workflow."""
        try:
            # 1. Validating
            record.transition_to(DeploymentStatus.VALIDATING, "Validating deployment prerequisites")
            record.progress_percentage = 10.0

            if health_checker and not health_checker():
                record.transition_to(DeploymentStatus.FAILED, "Initial health check failed")
                return False

            # 2. Running Deployment Strategy
            record.transition_to(DeploymentStatus.RUNNING, f"Executing {record.strategy.value} rollout")

            steps = [25.0, 50.0, 75.0, 100.0]
            if record.strategy == DeploymentStrategyType.CANARY:
                steps = [1.0, 5.0, 25.0, 50.0, 100.0]

            for step in steps:
                record.progress_percentage = step
                if strategy_executor:
                    ok = strategy_executor(record, step)
                    if not ok:
                        record.transition_to(DeploymentStatus.FAILED, f"Rollout failed at {step}% progression")
                        return False

                if health_checker and not health_checker():
                    record.transition_to(DeploymentStatus.FAILED, f"Health check failed at {step}% progression")
                    return False

            # 3. Verification & Completion
            record.progress_percentage = 100.0
            record.transition_to(DeploymentStatus.COMPLETED, "Rollout verified and completed successfully")
            return True

        except Exception as e:
            logger.error("Deployment rollout encountered exception: %s", e)
            record.error_message = str(e)
            record.transition_to(DeploymentStatus.FAILED, f"Exception during rollout: {e}")
            return False
