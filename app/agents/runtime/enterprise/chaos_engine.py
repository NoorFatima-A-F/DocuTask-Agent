"""
Chaos Testing Engine.
Automates resilience verification experiments by injecting controlled faults and verifying recovery behaviors,
measuring time-to-recovery (TTR) and recovery success ratios.
"""

import time
import logging
from typing import Any, Callable, Coroutine, Optional
from app.agents.runtime.enterprise.fault_injector import FaultInjector, FaultType

logger = logging.getLogger(__name__)


class ChaosExperimentResult:
    """Outcome of a chaos experiment."""

    def __init__(
        self,
        experiment_name: str,
        passed: bool,
        error: Optional[str] = None,
        duration_ms: float = 0.0,
        recovered: bool = False,
    ) -> None:
        self.experiment_name = experiment_name
        self.passed = passed
        self.error = error
        self.duration_ms = duration_ms
        self.recovered = recovered


class ChaosEngine:
    """Coordinates automated chaos testing and resilience validation."""

    def __init__(self, injector: Optional[FaultInjector] = None) -> None:
        self.injector = injector or FaultInjector()

    async def run_experiment(
        self,
        experiment_name: str,
        target_subsystem: str,
        fault_type: FaultType,
        workload_fn: Callable[[], Coroutine[Any, Any, Any]],
        recovery_assertion: Callable[[], Coroutine[Any, Any, bool]],
        burst_count: Optional[int] = None,
        probability: float = 1.0,
        delay_seconds: float = 0.0,
    ) -> ChaosExperimentResult:
        """Executes a chaos experiment: arms fault -> executes workload -> asserts recovery."""
        start_time = time.perf_counter()
        logger.info(f"Running chaos experiment '{experiment_name}' on '{target_subsystem}' with {fault_type.value}")
        self.injector.inject_fault(
            target_subsystem,
            fault_type,
            probability=probability,
            burst_count=burst_count,
            delay_seconds=delay_seconds,
        )

        try:
            await workload_fn()
        except Exception as ex:
            logger.info(f"Expected fault triggered: {ex}")
        finally:
            self.injector.clear_fault(target_subsystem)

        try:
            recovered = await recovery_assertion()
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            return ChaosExperimentResult(
                experiment_name,
                passed=recovered,
                recovered=recovered,
                duration_ms=duration_ms,
            )
        except Exception as ex:
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            return ChaosExperimentResult(
                experiment_name,
                passed=False,
                error=str(ex),
                duration_ms=duration_ms,
            )
