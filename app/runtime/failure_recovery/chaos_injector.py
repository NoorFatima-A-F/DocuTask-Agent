"""
ARTEICP Failure Recovery - Chaos Fault Injector
Injects controlled runtime faults (OCR crash, Gemini 429 rate limit, schema mismatch) to demonstrate self-healing autonomy.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import time


@dataclass
class ChaosFaultScenario:
    fault_id: str
    target_component: str
    fault_type: str  # PROCESS_CRASH | HTTP_429_RATE_LIMIT | SCHEMA_CORRUPTION | LATENCY_SPIKE
    description: str
    injected: bool = False
    injected_at: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


CANONICAL_FAULTS = [
    ChaosFaultScenario(
        fault_id="fault_ocr_crash",
        target_component="OCR_INGEST",
        fault_type="PROCESS_CRASH",
        description="Simulates unexpected OCR engine SIGSEGV crash on corrupted multi-layer PDF.",
    ),
    ChaosFaultScenario(
        fault_id="fault_gemini_429",
        target_component="LLM_EXTRACT",
        fault_type="HTTP_429_RATE_LIMIT",
        description="Simulates transient HTTP 429 quota exhaustion on primary LLM provider.",
    ),
    ChaosFaultScenario(
        fault_id="fault_schema_drift",
        target_component="VALIDATION",
        fault_type="SCHEMA_CORRUPTION",
        description="Simulates unexpected invoice tax table schema mutation violating JSON schema invariants.",
    ),
]


class ChaosFaultInjector:
    """Controls runtime fault injection experiments."""

    def __init__(self):
        self.scenarios = {f.fault_id: f for f in CANONICAL_FAULTS}

    def list_faults(self) -> List[Dict[str, Any]]:
        return [f.to_dict() for f in self.scenarios.values()]

    def trigger_fault(self, fault_id: str) -> ChaosFaultScenario:
        if fault_id not in self.scenarios:
            raise ValueError(f"Unknown fault scenario: {fault_id}")
        f = self.scenarios[fault_id]
        f.injected = True
        f.injected_at = time.time()
        return f


chaos_injector = ChaosFaultInjector()
