"""Chaos Fault Injection Engine for Resilience Testing."""

from __future__ import annotations

import random
import time
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

from ..mesh.data_plane import MeshRequest, MeshResponse


class FaultType(str, Enum):
    LATENCY = "LATENCY"
    ABORT = "ABORT"
    CORRUPTION = "CORRUPTION"


@dataclass
class FaultInjectionRule:
    rule_id: str
    target_service: str
    target_namespace: str = "default"
    fault_type: FaultType = FaultType.LATENCY
    percentage: float = 10.0  # 0.0 to 100.0%
    delay_ms: float = 500.0
    status_code: int = 503
    error_message: str = "Injected chaos fault"
    enabled: bool = True


class FaultInjectionEngine:
    """Injects synthetic latency and errors into requests matching chaos testing rules."""

    def __init__(self):
        self._rules: Dict[str, FaultInjectionRule] = {}

    def add_rule(self, rule: FaultInjectionRule) -> None:
        self._rules[rule.rule_id] = rule

    def remove_rule(self, rule_id: str) -> bool:
        if rule_id in self._rules:
            del self._rules[rule_id]
            return True
        return False

    def list_rules(self) -> List[FaultInjectionRule]:
        return list(self._rules.values())

    def evaluate_and_inject(self, request: MeshRequest) -> Optional[MeshResponse]:
        """Check if any fault injection rule applies, and execute the fault if triggered."""
        for rule in self._rules.values():
            if not rule.enabled:
                continue

            if rule.target_service != "*" and rule.target_service != request.target_service:
                continue
            if rule.target_namespace != "*" and rule.target_namespace != request.target_namespace:
                continue

            # Check percentage trigger
            if random.uniform(0, 100) > rule.percentage:
                continue

            # Fault triggered!
            if rule.fault_type == FaultType.LATENCY:
                time.sleep(rule.delay_ms / 1000.0)
                return None  # Continue with normal execution after injected delay
            elif rule.fault_type == FaultType.ABORT:
                return MeshResponse(
                    status_code=rule.status_code,
                    error_message=rule.error_message,
                    request_id=request.request_id,
                    applied_policy=f"fault_injection:{rule.rule_id}",
                )
            elif rule.fault_type == FaultType.CORRUPTION:
                return MeshResponse(
                    status_code=200,
                    payload={"corrupted_payload": "!!!MALFORMED_AI_DATA_FRAME!!!"},
                    request_id=request.request_id,
                    applied_policy=f"fault_injection:{rule.rule_id}",
                )

        return None
