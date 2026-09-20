"""
Evolution Policy Registry for Phase 13.5 (ARLP-KIP).
Stores active, candidate, and archived evolution policies with lineage links.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field


class ActivePolicyEntry(BaseModel):
    policy_id: str
    target_component: str
    policy_name: str
    version: str
    status: str = "ACTIVE"
    parameters: Dict[str, Any] = Field(default_factory=dict)
    promoted_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    promoter_id: str = "system-governance"


class EvolutionPolicyRegistry:
    """
    Manages active production policies and tracks policy version branches.
    """

    def __init__(self):
        self._active: Dict[str, ActivePolicyEntry] = {}
        self._versions: List[Dict[str, Any]] = []
        self._seed_default_policies()

    def _seed_default_policies(self):
        p1 = ActivePolicyEntry(
            policy_id="pol-baseline-planner",
            target_component="planner",
            policy_name="Baseline Dynamic Partitioning Policy",
            version="1.0.0",
            parameters={"max_retries": 3, "concurrency_limit": 6, "confidence_threshold": 0.85},
        )
        p2 = ActivePolicyEntry(
            policy_id="pol-baseline-worker",
            target_component="worker",
            policy_name="Adaptive Jitter Backoff Worker Policy",
            version="1.0.0",
            parameters={"base_delay_ms": 250, "max_retries": 3},
        )
        self._active[p1.policy_id] = p1
        self._active[p2.policy_id] = p2

    def list_active_policies(self) -> List[ActivePolicyEntry]:
        return list(self._active.values())

    def get_active_policy(self, policy_id: str) -> Optional[ActivePolicyEntry]:
        return self._active.get(policy_id)

    def set_active_policy(self, policy: ActivePolicyEntry):
        self._active[policy.policy_id] = policy
        self._versions.append(policy.model_dump())

    def list_all_versions(self) -> List[Dict[str, Any]]:
        return self._versions


evolution_policy_registry = EvolutionPolicyRegistry()
