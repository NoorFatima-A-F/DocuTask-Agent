"""
Planner Strategy Switch Engine.

Enables runtime switching between distinct planning heuristics (Greedy, Beam Search,
A*, Probabilistic, Cost-Optimized, Risk-Optimized) with recorded utility improvements.
"""

from __future__ import annotations

import enum
import time
import uuid
from typing import Any, Dict, List
from pydantic import BaseModel, Field


class PlanningStrategy(str, enum.Enum):
    GREEDY = "GREEDY"
    BEAM_SEARCH = "BEAM_SEARCH"
    A_STAR = "A_STAR"
    PROBABILISTIC = "PROBABILISTIC"
    COST_OPTIMIZED = "COST_OPTIMIZED"
    RISK_OPTIMIZED = "RISK_OPTIMIZED"


class StrategySwitchRecord(BaseModel):
    switch_id: str = Field(default_factory=lambda: f"strat-{uuid.uuid4().hex[:8]}")
    mission_id: str
    previous_strategy: PlanningStrategy
    new_strategy: PlanningStrategy
    trigger_reason: str
    expected_utility_delta: float
    expected_cost_delta_usd: float
    expected_latency_delta_ms: float
    timestamp: float = Field(default_factory=time.time)


class StrategySwitcher:
    """Manages adaptive switching of planning strategies based on runtime conditions."""

    @classmethod
    def evaluate_and_switch(
        cls,
        mission_id: str,
        current_strategy: PlanningStrategy,
        budget_remaining_usd: float,
        latency_budget_ms: float,
        current_error_rate: float,
    ) -> StrategySwitchRecord:
        """
        Recommends and executes a strategy switch if constraints are strained:
        - Low budget -> COST_OPTIMIZED
        - Tight latency deadline -> GREEDY or BEAM_SEARCH
        - High error rate -> RISK_OPTIMIZED / PROBABILISTIC
        """
        new_strategy = current_strategy
        reason = "Operating within nominal budget and latency constraints"
        utility_delta = 0.0
        cost_delta = 0.0
        lat_delta = 0.0

        if budget_remaining_usd < 0.005 and current_strategy != PlanningStrategy.COST_OPTIMIZED:
            new_strategy = PlanningStrategy.COST_OPTIMIZED
            reason = f"Budget critical (${budget_remaining_usd:.4f} remaining): Switching to cost-minimal operator pruning."
            utility_delta = -0.05
            cost_delta = -0.003
            lat_delta = +50.0

        elif current_error_rate > 0.30 and current_strategy != PlanningStrategy.RISK_OPTIMIZED:
            new_strategy = PlanningStrategy.RISK_OPTIMIZED
            reason = f"High error rate ({current_error_rate*100:.1f}%): Switching to redundant verification branches."
            utility_delta = +0.15
            cost_delta = +0.001
            lat_delta = +80.0

        elif latency_budget_ms < 500.0 and current_strategy != PlanningStrategy.GREEDY:
            new_strategy = PlanningStrategy.GREEDY
            reason = f"Latency deadline tight ({latency_budget_ms:.0f}ms remaining): Fast-path greedy dispatch."
            utility_delta = -0.02
            cost_delta = 0.0
            lat_delta = -120.0

        return StrategySwitchRecord(
            mission_id=mission_id,
            previous_strategy=current_strategy,
            new_strategy=new_strategy,
            trigger_reason=reason,
            expected_utility_delta=utility_delta,
            expected_cost_delta_usd=cost_delta,
            expected_latency_delta_ms=lat_delta,
        )
