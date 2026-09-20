"""
Recovery Strategy Selector.
Selects optimal recovery strategy based on failure classification, root cause analysis, cost, and policy constraints.
"""

from typing import Optional
from app.agents.recovery.failure import Failure, FailureCategory, FailureSeverity
from app.agents.recovery.recovery_strategy import RecoveryStrategy, RecoveryStrategyDefinition
from app.agents.recovery.root_cause import RootCauseReport
from app.agents.recovery.strategy_registry import RecoveryStrategyRegistry


class RecoveryStrategySelector:
    """Selects best recovery strategy matching failure diagnosis."""

    def select_strategy(self, failure: Failure, root_cause: RootCauseReport) -> RecoveryStrategyDefinition:
        candidates = RecoveryStrategyRegistry.get_candidate_strategies(failure.category)

        # Critical severity or low recoverability score requires rollback or planner re-entry
        if failure.severity == FailureSeverity.CRITICAL or failure.recoverability_score < 0.4:
            if failure.category == FailureCategory.TOKEN_BUDGET_FAILURE:
                selected = RecoveryStrategy.PLANNER_RE_ENTRY
            else:
                selected = RecoveryStrategy.ROLLBACK
        elif failure.category == FailureCategory.TOOL_FAILURE:
            selected = RecoveryStrategy.ALTERNATE_TOOL if failure.recoverability_score > 0.8 else RecoveryStrategy.RETRY
        elif failure.category == FailureCategory.WORKER_FAILURE:
            selected = RecoveryStrategy.ALTERNATE_WORKER
        elif failure.category == FailureCategory.TIMEOUT_FAILURE:
            selected = RecoveryStrategy.RETRY
        else:
            selected = candidates[0] if candidates else RecoveryStrategy.RESTORE_CHECKPOINT

        return RecoveryStrategyDefinition(
            strategy=selected,
            parameters={"failure_id": str(failure.identity.failure_id), "cause": failure.probable_cause},
            estimated_cost_usd=0.05,
            requires_human_gate=(failure.severity == FailureSeverity.CRITICAL)
        )
