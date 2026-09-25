"""
Recovery Policy Domain Models.
Governs recovery execution budgets, max retries, allowed strategies, and human approval limits.
"""

from typing import List
from pydantic import BaseModel, Field
from app.agents.recovery.recovery_strategy import RecoveryStrategy


class RecoveryPolicy(BaseModel):
    """Enterprise policy governing autonomous recovery behavior."""
    policy_id: str = Field(default="DEFAULT_RECOVERY_POLICY")
    allowed_strategies: List[RecoveryStrategy] = Field(
        default_factory=lambda: [
            RecoveryStrategy.RETRY,
            RecoveryStrategy.ALTERNATE_TOOL,
            RecoveryStrategy.ALTERNATE_WORKER,
            RecoveryStrategy.RESTORE_CHECKPOINT,
            RecoveryStrategy.ROLLBACK,
            RecoveryStrategy.PLANNER_RE_ENTRY
        ]
    )
    max_total_retries: int = Field(default=3, ge=0)
    max_recovery_budget_usd: float = Field(default=2.0, ge=0.0)
    require_human_on_critical: bool = Field(default=True)
    model_config = {"frozen": True}
