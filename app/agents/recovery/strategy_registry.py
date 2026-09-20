"""
Recovery Strategy Registry.
Registry mapping failure categories to applicable recovery strategies.
"""

from typing import Dict, List
from app.agents.recovery.failure import FailureCategory
from app.agents.recovery.recovery_strategy import RecoveryStrategy


class RecoveryStrategyRegistry:
    """Registry maintaining mappings of failure categories to candidate strategies."""

    MAPPINGS: Dict[FailureCategory, List[RecoveryStrategy]] = {
        FailureCategory.TOOL_FAILURE: [
            RecoveryStrategy.RETRY,
            RecoveryStrategy.ALTERNATE_TOOL,
            RecoveryStrategy.RESTORE_CHECKPOINT
        ],
        FailureCategory.WORKER_FAILURE: [
            RecoveryStrategy.ALTERNATE_WORKER,
            RecoveryStrategy.RETRY,
            RecoveryStrategy.RESTORE_CHECKPOINT
        ],
        FailureCategory.TIMEOUT_FAILURE: [
            RecoveryStrategy.RETRY,
            RecoveryStrategy.RESTORE_CHECKPOINT
        ],
        FailureCategory.TOKEN_BUDGET_FAILURE: [
            RecoveryStrategy.PLANNER_RE_ENTRY,
            RecoveryStrategy.HUMAN_APPROVAL,
            RecoveryStrategy.PERMANENT_FAILURE
        ],
        FailureCategory.DEPENDENCY_FAILURE: [
            RecoveryStrategy.ROLLBACK,
            RecoveryStrategy.PLANNER_RE_ENTRY
        ],
        FailureCategory.CHECKPOINT_FAILURE: [
            RecoveryStrategy.REPLAY_EXECUTION,
            RecoveryStrategy.ROLLBACK
        ],
        FailureCategory.EXECUTION_FAILURE: [
            RecoveryStrategy.RETRY,
            RecoveryStrategy.RESTORE_CHECKPOINT,
            RecoveryStrategy.COMPENSATION
        ],
        FailureCategory.UNKNOWN_FAILURE: [
            RecoveryStrategy.RESTORE_CHECKPOINT,
            RecoveryStrategy.HUMAN_APPROVAL
        ]
    }

    @classmethod
    def get_candidate_strategies(cls, category: FailureCategory) -> List[RecoveryStrategy]:
        return cls.MAPPINGS.get(category, [RecoveryStrategy.RESTORE_CHECKPOINT])
