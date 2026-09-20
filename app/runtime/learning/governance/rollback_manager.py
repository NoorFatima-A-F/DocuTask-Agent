"""
Rollback Manager for Phase 13.5 (ARLP-KIP).
Provides 1-click atomic rollback to baseline or known-good policy configurations upon anomaly detection.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field

from app.runtime.learning.policy.policy_registry import evolution_policy_registry, ActivePolicyEntry


class RollbackRecord(BaseModel):
    rollback_id: str = Field(default_factory=lambda: f"rb_{uuid.uuid4().hex[:8]}")
    policy_id: str
    restored_baseline_id: str
    status: str = "ROLLED_BACK"
    operator_id: str = "system-operator"
    reason: str = "Operational safety rollback"
    rolled_back_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class RollbackManager:
    """
    Executes atomic rollbacks of active policies to baseline configurations.
    """

    def __init__(self):
        self._rollbacks: List[RollbackRecord] = []

    def rollback(self, policy_id: str, operator_id: str = "system-operator", reason: str = "Safety rollback") -> RollbackRecord:
        baseline_id = "pol-baseline-planner"
        baseline_policy = ActivePolicyEntry(
            policy_id=policy_id,
            target_component="planner",
            policy_name="Baseline Dynamic Partitioning Policy (Restored)",
            version="1.0.0",
            parameters={"max_retries": 3, "concurrency_limit": 6, "confidence_threshold": 0.85},
            promoter_id=operator_id,
        )
        evolution_policy_registry.set_active_policy(baseline_policy)

        rec = RollbackRecord(
            policy_id=policy_id,
            restored_baseline_id=baseline_id,
            status="ROLLED_BACK",
            operator_id=operator_id,
            reason=reason,
        )
        self._rollbacks.append(rec)
        return rec

    def list_rollbacks(self) -> List[RollbackRecord]:
        return self._rollbacks


rollback_manager = RollbackManager()
