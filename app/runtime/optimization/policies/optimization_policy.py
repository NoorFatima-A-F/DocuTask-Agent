"""
Optimization Policies Subsystem for Phase 13.6 (ARIA-EOP).
Policy specifications and validation engines for SLAs, budgets, priorities, and routing rules.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class OptimizationPolicySpec(BaseModel):
    policy_id: str = "pol-default-opt"
    policy_name: str = "Enterprise Standard Optimization Policy"
    max_budget_per_mission_usd: float = 0.50
    sla_deadline_ms: float = 5000.0
    min_confidence_floor: float = 0.85
    max_concurrency_workers: int = 16
    max_retries: int = 4
    default_priority_tier: str = "BALANCED_STANDARD"
    allowed_models: List[str] = Field(default_factory=lambda: ["gemini-1.5-flash", "gemini-1.5-pro", "claude-3-5-sonnet"])


class PolicyValidator:
    """
    Validates candidate execution configurations against optimization policy specs.
    """

    @classmethod
    def validate_against_policy(cls, config: Dict[str, Any], policy: Optional[OptimizationPolicySpec] = None) -> Dict[str, Any]:
        p = policy or OptimizationPolicySpec()
        errors = []

        cost = config.get("cost_usd", 0.0)
        if cost > p.max_budget_per_mission_usd:
            errors.append(f"Cost ${cost} exceeds policy cap ${p.max_budget_per_mission_usd}")

        latency = config.get("latency_ms", 0.0)
        if latency > p.sla_deadline_ms:
            errors.append(f"Latency {latency}ms exceeds policy SLA {p.sla_deadline_ms}ms")

        conf = config.get("confidence", 1.0)
        if conf < p.min_confidence_floor:
            errors.append(f"Confidence {conf} below policy floor {p.min_confidence_floor}")

        return {
            "is_compliant": len(errors) == 0,
            "violations": errors,
            "enforced_policy_id": p.policy_id,
        }
