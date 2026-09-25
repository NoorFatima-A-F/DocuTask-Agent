"""
Autonomous Research - Discovery Validator
Validates discovered experimental policies against enterprise hard safety constraints.
"""

from typing import Dict, List, Any
from dataclasses import dataclass, asdict


@dataclass
class DiscoveryValidationReport:
    candidate_id: str
    is_safe_for_canary: bool
    sla_compliance_predicted: bool
    budget_guardrail_passed: bool
    accuracy_floor_preserved: bool
    violations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class DiscoveryValidator:
    """Verifies discovered research strategies before staging."""

    @staticmethod
    def validate_candidate(
        candidate_id: str,
        predicted_accuracy: float,
        predicted_latency_ms: float,
        predicted_cost_usd: float,
        accuracy_floor: float = 0.92,
        latency_ceiling_ms: float = 2500.0,
        cost_ceiling_usd: float = 0.05,
    ) -> DiscoveryValidationReport:
        violations: List[str] = []

        acc_ok = predicted_accuracy >= accuracy_floor
        if not acc_ok:
            violations.append(f"Predicted accuracy {predicted_accuracy:.3f} below floor {accuracy_floor:.3f}")

        lat_ok = predicted_latency_ms <= latency_ceiling_ms
        if not lat_ok:
            violations.append(f"Predicted latency {predicted_latency_ms:.1f}ms exceeds ceiling {latency_ceiling_ms:.1f}ms")

        cost_ok = predicted_cost_usd <= cost_ceiling_usd
        if not cost_ok:
            violations.append(f"Predicted cost ${predicted_cost_usd:.4f} exceeds ceiling ${cost_ceiling_usd:.4f}")

        is_safe = acc_ok and lat_ok and cost_ok

        return DiscoveryValidationReport(
            candidate_id=candidate_id,
            is_safe_for_canary=is_safe,
            sla_compliance_predicted=lat_ok,
            budget_guardrail_passed=cost_ok,
            accuracy_floor_preserved=acc_ok,
            violations=violations,
        )
