"""
Self-Evolution Runtime - Rollback Manager
Performs atomic instant rollback to the last verified safe baseline policy.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict, field
import time
from app.runtime.self_evolution.policy_lifecycle import PolicyLifecycleManager, PolicyDefinition


@dataclass
class RollbackEvent:
    rollback_id: str
    from_policy_id: str
    to_policy_id: str
    trigger_reason: str
    executed_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class RollbackManager:
    """Safely and instantaneously reverts experimental policies upon SLA breaches."""

    def __init__(self, lifecycle_mgr: PolicyLifecycleManager):
        self.lifecycle_mgr = lifecycle_mgr
        self.rollback_history: List[RollbackEvent] = []

    def execute_instant_rollback(
        self,
        active_policy_id: str,
        safe_fallback_policy_id: str,
        reason: str,
    ) -> RollbackEvent:
        # Revert active policy
        self.lifecycle_mgr.transition_stage(active_policy_id, "ROLLED_BACK", reason=reason)
        # Restore fallback policy to PRODUCTION
        fallback = self.lifecycle_mgr.policies.get(safe_fallback_policy_id)
        if fallback:
            fallback.stage = "PRODUCTION"
            fallback.deployed_at = time.time()

        event = RollbackEvent(
            rollback_id=f"rbk_{int(time.time())}",
            from_policy_id=active_policy_id,
            to_policy_id=safe_fallback_policy_id,
            trigger_reason=reason,
        )
        self.rollback_history.append(event)
        return event
