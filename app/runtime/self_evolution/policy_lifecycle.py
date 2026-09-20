"""
Self-Evolution Runtime - Policy Lifecycle
Defines the versioned policy schema and stage transition state machine.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict, field
import uuid
import time


@dataclass
class PolicyDefinition:
    policy_id: str
    version: str
    name: str
    stage: str  # DRAFT | SHADOW_EVAL | CANARY_STAGING | PRODUCTION | ROLLED_BACK | RETIRED
    parameters: Dict[str, float]
    provenance_hash: str
    created_at: float = field(default_factory=time.time)
    deployed_at: Optional[float] = None
    rolled_back_at: Optional[float] = None
    rollback_reason: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class PolicyLifecycleManager:
    """Manages policy stage transitions with safety invariants."""

    VALID_TRANSITIONS = {
        "DRAFT": ["SHADOW_EVAL"],
        "SHADOW_EVAL": ["CANARY_STAGING", "RETIRED"],
        "CANARY_STAGING": ["PRODUCTION", "ROLLED_BACK"],
        "PRODUCTION": ["ROLLED_BACK", "RETIRED"],
        "ROLLED_BACK": ["DRAFT", "RETIRED"],
        "RETIRED": [],
    }

    def __init__(self):
        self.policies: Dict[str, PolicyDefinition] = {}
        self._seed_policies()

    def _seed_policies(self):
        p1 = PolicyDefinition(
            policy_id="pol_v4_2",
            version="v4.2.0",
            name="Baseline Balanced Pareto Optimization",
            stage="PRODUCTION",
            parameters={
                "weight_accuracy": 0.45,
                "weight_latency": 0.25,
                "weight_cost": 0.30,
                "confidence_threshold": 0.85,
                "timeout_ms": 3000.0,
            },
            provenance_hash="a1f89c44b3e210984dca88921e1a89c9",
            deployed_at=time.time() - 86400 * 5,
        )
        self.policies[p1.policy_id] = p1

    def list_policies(self) -> List[PolicyDefinition]:
        return list(self.policies.values())

    def get_active_production_policy(self) -> Optional[PolicyDefinition]:
        for p in self.policies.values():
            if p.stage == "PRODUCTION":
                return p
        return None

    def transition_stage(self, policy_id: str, new_stage: str, reason: Optional[str] = None) -> PolicyDefinition:
        if policy_id not in self.policies:
            raise ValueError(f"Policy {policy_id} not found")
        pol = self.policies[policy_id]
        if new_stage not in self.VALID_TRANSITIONS.get(pol.stage, []):
            raise ValueError(f"Invalid transition from {pol.stage} to {new_stage}")

        pol.stage = new_stage
        if new_stage == "PRODUCTION":
            pol.deployed_at = time.time()
        elif new_stage == "ROLLED_BACK":
            pol.rolled_back_at = time.time()
            pol.rollback_reason = reason or "Manual rollback requested"
        return pol
