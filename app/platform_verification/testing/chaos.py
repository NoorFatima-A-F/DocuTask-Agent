"""
Chaos Engineering and Controlled Fault Injection Framework.
Simulates network latency, storage outages, process crashes, and corrupted payloads.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional
import time

class ChaosFaultType(str, Enum):
    LATENCY_INJECTION = "LATENCY_INJECTION"
    STORAGE_OUTAGE = "STORAGE_OUTAGE"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    PAYLOAD_CORRUPTION = "PAYLOAD_CORRUPTION"
    TIMEOUT_SIMULATION = "TIMEOUT_SIMULATION"

@dataclass(frozen=True)
class FaultInjectionConfig:
    fault_type: ChaosFaultType
    enabled: bool = True
    delay_ms: float = 0.0
    failure_rate: float = 1.0 # 1.0 = 100% fail

class ChaosFaultInjector:
    """Injects faults into execution pipelines to measure resilience and recovery."""
    def __init__(self, config: Optional[FaultInjectionConfig] = None):
        self.config = config

    def maybe_inject_fault(self) -> None:
        if not self.config or not self.config.enabled:
            return

        if self.config.fault_type == ChaosFaultType.LATENCY_INJECTION:
            time.sleep(self.config.delay_ms / 1000.0)
        elif self.config.fault_type == ChaosFaultType.STORAGE_OUTAGE:
            raise IOError("ChaosFault: Storage backend simulated outage")
        elif self.config.fault_type == ChaosFaultType.SERVICE_UNAVAILABLE:
            raise ConnectionError("ChaosFault: Downstream service unavailable (503)")
        elif self.config.fault_type == ChaosFaultType.TIMEOUT_SIMULATION:
            raise TimeoutError("ChaosFault: Hard execution deadline exceeded")
        elif self.config.fault_type == ChaosFaultType.PAYLOAD_CORRUPTION:
            raise ValueError("ChaosFault: Tampered/corrupted payload received")
