"""
Confidence Budget Manager (Phase 82B.8)
=======================================
Tracks error and uncertainty budgets across scientific pipeline stages,
alerting when accumulated noise threatens statistical significance thresholds.
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple


class BudgetStatus(str, Enum):
    WITHIN_BUDGET = "WITHIN_BUDGET"
    NEARING_LIMIT = "NEARING_LIMIT"  # > 80% consumed
    BUDGET_EXCEEDED = "BUDGET_EXCEEDED"


@dataclass(frozen=True)
class StageBudgetConsumption:
    stage_name: str
    allocated_variance: float
    consumed_variance: float
    consumed_pct: float
    is_exceeded: bool


@dataclass(frozen=True)
class ConfidenceBudgetReport:
    total_budget_variance: float
    total_consumed_variance: float
    total_consumed_pct: float
    status: BudgetStatus
    stage_consumptions: Tuple[StageBudgetConsumption, ...]
    remaining_budget_variance: float
    recommendation: str


class ConfidenceBudgetManager:
    """
    Allocates and monitors uncertainty budgets.
    """

    def __init__(self, max_allowed_std_error: float = 0.05):
        self.max_allowed_std_error = max_allowed_std_error
        self.max_variance = max_allowed_std_error**2

    def audit_budget(
        self,
        stage_errors: List[Tuple[str, float]],  # (stage_name, std_err)
    ) -> ConfidenceBudgetReport:
        """Audit total accumulated variance against variance budget."""
        total_consumed_var = sum(serr**2 for _, serr in stage_errors)
        consumed_pct = (total_consumed_var / self.max_variance) * 100.0 if self.max_variance > 0 else 100.0
        remaining = max(0.0, self.max_variance - total_consumed_var)

        if consumed_pct <= 80.0:
            status = BudgetStatus.WITHIN_BUDGET
            rec = "Uncertainty is well within statistical significance bounds."
        elif consumed_pct <= 100.0:
            status = BudgetStatus.NEARING_LIMIT
            rec = "Accumulated uncertainty is nearing budget threshold. Consider increasing sample size."
        else:
            status = BudgetStatus.BUDGET_EXCEEDED
            rec = "Uncertainty budget exceeded! Results may have insufficient statistical power."

        consumptions: List[StageBudgetConsumption] = []
        n_stages = max(1, len(stage_errors))
        equal_alloc = self.max_variance / n_stages

        for name, serr in stage_errors:
            c_var = serr**2
            c_pct = (c_var / equal_alloc) * 100.0 if equal_alloc > 0 else 0.0
            consumptions.append(StageBudgetConsumption(
                stage_name=name,
                allocated_variance=equal_alloc,
                consumed_variance=c_var,
                consumed_pct=c_pct,
                is_exceeded=(c_var > equal_alloc),
            ))

        return ConfidenceBudgetReport(
            total_budget_variance=self.max_variance,
            total_consumed_variance=total_consumed_var,
            total_consumed_pct=consumed_pct,
            status=status,
            stage_consumptions=tuple(consumptions),
            remaining_budget_variance=remaining,
            recommendation=rec,
        )
