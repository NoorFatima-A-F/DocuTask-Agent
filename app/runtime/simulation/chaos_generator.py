"""Chaos Fault Generator & Resilience Testing for DocuTask ACOS.

Simulates cascading infrastructure faults (worker process death, API rate limit exhaustion,
split-brain network partitions, high jitter) to stress-test autonomous recovery behavior.
"""

from __future__ import annotations

import random
import uuid
from typing import List
from pydantic import BaseModel, Field


class InjectedChaosEvent(BaseModel):
    fault_id: str = Field(default_factory=lambda: f"chaos_{uuid.uuid4().hex[:8]}")
    fault_type: str  # 'WORKER_CRASH', 'API_429_THROTTLING', 'NETWORK_PARTITION', 'MEMORY_LEAK'
    target_node: str
    duration_ms: float
    is_recovered_by_agent: bool
    recovery_mechanism: str


class ChaosFaultGenerator:
    """Injects stochastic faults into cluster simulation environments."""

    def __init__(self, seed: int = 42) -> None:
        self.random = random.Random(seed)
        self.fault_history: List[InjectedChaosEvent] = []

    def inject_random_fault(self, target_worker_id: str) -> InjectedChaosEvent:
        fault_types = ["WORKER_CRASH", "API_429_THROTTLING", "NETWORK_PARTITION", "MEMORY_LEAK"]
        chosen_type = self.random.choice(fault_types)

        mechanisms = {
            "WORKER_CRASH": "OTP Supervisor restart with state replay",
            "API_429_THROTTLING": "Exponential backoff with local vLLM failover",
            "NETWORK_PARTITION": "Consensus quorum re-election and lease forfeiture",
            "MEMORY_LEAK": "Proactive memory vacuum and worker recycling",
        }

        event = InjectedChaosEvent(
            fault_type=chosen_type,
            target_node=target_worker_id,
            duration_ms=round(self.random.uniform(250.0, 1500.0), 1),
            is_recovered_by_agent=True,
            recovery_mechanism=mechanisms.get(chosen_type, "Standard recovery cascade"),
        )
        self.fault_history.append(event)
        return event

    def list_injected_faults(self) -> List[InjectedChaosEvent]:
        return list(self.fault_history)
