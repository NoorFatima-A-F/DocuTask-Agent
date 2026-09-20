"""
AOIS-HROP Phase 13.7 - Healing Strategy Selector
Evaluates incident severity, blast radius, and historical success rates to select the optimal automated healing strategy.
"""

from typing import Dict, List, Optional
from app.runtime.operations.events.operation_events import HealingActionType, OperationalSeverity, SubsystemType


class HealingStrategySelector:
    """
    Selects the least disruptive yet most effective self-healing remediation plan.
    """

    def select_strategy(
        self,
        subsystem: SubsystemType,
        error_type: str,
        severity: OperationalSeverity,
    ) -> HealingActionType:
        if subsystem == SubsystemType.WORKERS:
            if error_type in ("WORKER_CRASH", "HUNG_WORKER"):
                return HealingActionType.WORKER_RESTART
            elif error_type == "RETRY_STORM":
                return HealingActionType.CONCURRENCY_ADJUST
            return HealingActionType.WORKER_REPLACE

        if subsystem == SubsystemType.PLANNER:
            if severity == OperationalSeverity.CRITICAL:
                return HealingActionType.PLANNER_ROLLBACK
            return HealingActionType.PLANNER_REPLAN

        if subsystem == SubsystemType.MEMORY:
            return HealingActionType.MEMORY_REPAIR

        if subsystem in (SubsystemType.API, SubsystemType.OPTIMIZATION):
            if error_type == "MODEL_RATE_LIMIT":
                return HealingActionType.FALLBACK_MODEL_ENGAGE
            return HealingActionType.CONCURRENCY_ADJUST

        return HealingActionType.RESOURCE_REALLOCATE
