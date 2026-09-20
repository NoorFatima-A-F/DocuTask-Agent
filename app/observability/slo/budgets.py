"""Error Budget Management and Automated Release Freeze Gates."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

from .calculator import SLOCalculator
from .models import ServiceLevelObjective


class BudgetStatus(str, Enum):
    HEALTHY = "HEALTHY"
    AT_RISK = "AT_RISK"
    EXHAUSTED = "EXHAUSTED"


@dataclass
class ErrorBudgetSnapshot:
    slo_id: str
    service_name: str
    target_percent: float
    total_budget_events: int
    consumed_budget_events: int
    remaining_budget_events: int
    remaining_percent: float
    status: BudgetStatus
    release_freeze_enforced: bool


class ErrorBudgetEngine:
    """Manages error budget balances and automates release freeze governance."""

    def __init__(self, at_risk_threshold_percent: float = 20.0):
        self.at_risk_threshold_percent = at_risk_threshold_percent
        self._slos: Dict[str, ServiceLevelObjective] = {}

    def register_slo(self, slo: ServiceLevelObjective) -> None:
        self._slos[slo.slo_id] = slo

    def calculate_budget(
        self,
        slo_id: str,
        total_events: int,
        bad_events: int,
    ) -> Optional[ErrorBudgetSnapshot]:
        slo = self._slos.get(slo_id)
        if not slo:
            return None

        allowed_failure_rate = (100.0 - slo.target_percent) / 100.0
        total_allowed_bad = int(total_events * allowed_failure_rate)

        if total_allowed_bad <= 0:
            remaining_bad = 0 if bad_events > 0 else 1
            remaining_pct = 0.0 if bad_events > 0 else 100.0
        else:
            remaining_bad = max(0, total_allowed_bad - bad_events)
            remaining_pct = (remaining_bad / total_allowed_bad) * 100.0

        if remaining_pct <= 0.0:
            status = BudgetStatus.EXHAUSTED
            freeze = True
        elif remaining_pct <= self.at_risk_threshold_percent:
            status = BudgetStatus.AT_RISK
            freeze = False
        else:
            status = BudgetStatus.HEALTHY
            freeze = False

        return ErrorBudgetSnapshot(
            slo_id=slo.slo_id,
            service_name=slo.service_name,
            target_percent=slo.target_percent,
            total_budget_events=total_allowed_bad,
            consumed_budget_events=bad_events,
            remaining_budget_events=remaining_bad,
            remaining_percent=round(remaining_pct, 2),
            status=status,
            release_freeze_enforced=freeze,
        )
