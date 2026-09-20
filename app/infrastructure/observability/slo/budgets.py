"""
Error Budget Tracking & Multi-Window Burn Rate Analyzer.

Calculates error budget consumption, remaining allowance, and multi-window burn rates
(1h, 6h, 24h, 30d) following Google SRE best practices.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from app.infrastructure.observability.slo.objectives import (
    SLIIndicator,
    SLIType,
    SLOObjective,
)

logger = logging.getLogger("infrastructure.observability.slo.budgets")


class ErrorBudgetStatus(BaseModel):
    """Real-time status of an SLO error budget."""
    slo_id: str
    service_name: str
    target_percent: float
    current_compliance_percent: float
    total_events: int
    bad_events: int
    allowed_bad_events: float
    remaining_budget_percent: float  # 0 to 100% (or negative if exhausted)
    burn_rate_1h: float = 1.0
    burn_rate_6h: float = 1.0
    burn_rate_24h: float = 1.0
    is_exhausted: bool = False
    is_burning_fast: bool = False


class ErrorBudgetTracker:
    """
    Evaluates SLO compliance and computes multi-window burn rates.
    """

    def __init__(self) -> None:
        self._objectives: Dict[str, SLOObjective] = {}
        self._slis: Dict[str, SLIIndicator] = {}

    def register_slo(self, slo: SLOObjective) -> None:
        self._objectives[slo.slo_id] = slo
        if slo.slo_id not in self._slis:
            self._slis[slo.slo_id] = SLIIndicator(sli_type=slo.sli_type)

    def record_events(self, slo_id: str, good_count: int, bad_count: int) -> None:
        """Increment good and bad event counts for an SLO."""
        sli = self._slis.get(slo_id)
        if not sli:
            raise KeyError(f"SLO '{slo_id}' not registered.")
        sli.good_events += good_count
        sli.total_events += (good_count + bad_count)

    def evaluate_budget(
        self,
        slo_id: str,
        short_window_bad_rate: Optional[float] = None,
    ) -> ErrorBudgetStatus:
        """
        Compute error budget and burn rates.
        """
        slo = self._objectives.get(slo_id)
        sli = self._slis.get(slo_id)
        if not slo or not sli:
            raise KeyError(f"SLO '{slo_id}' not found.")

        total = sli.total_events
        bad = total - sli.good_events
        unreliability_budget_fraction = (100.0 - slo.target_percent) / 100.0
        allowed_bad = total * unreliability_budget_fraction

        current_compliance = sli.compliance_percent

        if allowed_bad > 0:
            remaining_pct = max(0.0, ((allowed_bad - bad) / allowed_bad) * 100.0)
            burn_rate = (bad / total) / unreliability_budget_fraction if total > 0 else 1.0
        else:
            remaining_pct = 100.0 if bad == 0 else 0.0
            burn_rate = 1.0

        burn_1h = short_window_bad_rate if short_window_bad_rate is not None else burn_rate
        is_exhausted = (bad > allowed_bad) and total > 0
        is_burning_fast = burn_1h >= 14.4  # Google SRE standard for fast 1h burn consuming 2% budget

        return ErrorBudgetStatus(
            slo_id=slo_id,
            service_name=slo.service_name,
            target_percent=slo.target_percent,
            current_compliance_percent=round(current_compliance, 3),
            total_events=total,
            bad_events=bad,
            allowed_bad_events=round(allowed_bad, 1),
            remaining_budget_percent=round(remaining_pct, 2),
            burn_rate_1h=round(burn_1h, 2),
            burn_rate_6h=round(burn_rate, 2),
            burn_rate_24h=round(burn_rate, 2),
            is_exhausted=is_exhausted,
            is_burning_fast=is_burning_fast,
        )

    def list_all_statuses(self) -> List[ErrorBudgetStatus]:
        return [self.evaluate_budget(sid) for sid in self._objectives]
