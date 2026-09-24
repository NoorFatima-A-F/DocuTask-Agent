"""
Chaos Fault Injector.
Injects synthetic faults (worker crashes, network partitions, dependency timeouts, memory pressure, latency jitter)
to validate platform resilience under adverse conditions with probability, burst count, and jitter control.
"""

import asyncio
import random
from enum import Enum
from typing import Dict, Optional
from pydantic import BaseModel
from app.agents.runtime.exceptions import RuntimeKernelException


class FaultType(str, Enum):
    """Typology of synthetic faults injected during chaos testing."""
    WORKER_CRASH = "WORKER_CRASH"
    NETWORK_FAILURE = "NETWORK_FAILURE"
    DEPENDENCY_TIMEOUT = "DEPENDENCY_TIMEOUT"
    MEMORY_PRESSURE = "MEMORY_PRESSURE"
    LATENCY_JITTER = "LATENCY_JITTER"


class InjectedFaultException(RuntimeKernelException):
    """Exception raised when a synthetic fault is triggered."""
    pass


class FaultSpec(BaseModel):
    """Configuration specification for an armed fault."""
    fault_type: FaultType
    probability: float = 1.0
    remaining_bursts: Optional[int] = None
    delay_seconds: float = 0.0


class FaultInjector:
    """Configurable fault injector for chaos verification experiments."""

    def __init__(self) -> None:
        self._active_faults: Dict[str, FaultSpec] = {}

    def inject_fault(
        self,
        target_subsystem: str,
        fault_type: FaultType,
        probability: float = 1.0,
        burst_count: Optional[int] = None,
        delay_seconds: float = 0.0,
    ) -> None:
        """Arms a fault on a target subsystem with optional probability and burst limits."""
        self._active_faults[target_subsystem] = FaultSpec(
            fault_type=fault_type,
            probability=probability,
            remaining_bursts=burst_count,
            delay_seconds=delay_seconds,
        )

    def clear_fault(self, target_subsystem: str) -> None:
        """Disarms any fault on target subsystem."""
        self._active_faults.pop(target_subsystem, None)

    async def maybe_fail(self, target_subsystem: str) -> None:
        """Triggers fault if one is armed for target subsystem."""
        spec = self._active_faults.get(target_subsystem)
        if not spec:
            return

        if spec.remaining_bursts is not None and spec.remaining_bursts <= 0:
            self.clear_fault(target_subsystem)
            return

        # Check probability
        if spec.probability < 1.0 and random.random() > spec.probability:
            return

        if spec.remaining_bursts is not None:
            spec.remaining_bursts -= 1
            if spec.remaining_bursts <= 0:
                self.clear_fault(target_subsystem)

        if spec.delay_seconds > 0:
            await asyncio.sleep(spec.delay_seconds)

        if spec.fault_type == FaultType.WORKER_CRASH:
            raise InjectedFaultException(f"Chaos: Simulated worker crash in '{target_subsystem}'")
        elif spec.fault_type == FaultType.NETWORK_FAILURE:
            raise ConnectionResetError(f"Chaos: Simulated network partition in '{target_subsystem}'")
        elif spec.fault_type == FaultType.DEPENDENCY_TIMEOUT:
            await asyncio.sleep(0.2)
            raise TimeoutError(f"Chaos: Simulated dependency timeout in '{target_subsystem}'")
        elif spec.fault_type == FaultType.MEMORY_PRESSURE:
            raise MemoryError(f"Chaos: Simulated memory pressure in '{target_subsystem}'")
        elif spec.fault_type == FaultType.LATENCY_JITTER:
            # Latency delay already applied above
            return
