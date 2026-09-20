"""
Optimization Strategy Definitions for Plan Optimization Engine.
Defines trade-off profiles, multi-objective weight configurations, and optimization constraints.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict


class OptimizationStrategy(str, Enum):
    """Supported strategic optimization targets."""
    BALANCED = "balanced"
    COST_OPTIMIZED = "cost_optimized"
    LATENCY_OPTIMIZED = "latency_optimized"
    QUALITY_OPTIMIZED = "quality_optimized"
    RISK_MINIMIZED = "risk_minimized"


@dataclass(frozen=True)
class StrategyWeights:
    """Normalized weights across the 5 Pareto dimensions."""
    weight_quality: float = 0.30
    weight_cost: float = 0.20
    weight_latency: float = 0.20
    weight_reliability: float = 0.20
    weight_risk: float = 0.10

    def validate(self) -> bool:
        total = self.weight_quality + self.weight_cost + self.weight_latency + self.weight_reliability + self.weight_risk
        return abs(total - 1.0) < 1e-4


STRATEGY_PRESETS: Dict[OptimizationStrategy, StrategyWeights] = {
    OptimizationStrategy.BALANCED: StrategyWeights(
        weight_quality=0.30,
        weight_cost=0.20,
        weight_latency=0.20,
        weight_reliability=0.20,
        weight_risk=0.10,
    ),
    OptimizationStrategy.COST_OPTIMIZED: StrategyWeights(
        weight_quality=0.20,
        weight_cost=0.45,
        weight_latency=0.15,
        weight_reliability=0.15,
        weight_risk=0.05,
    ),
    OptimizationStrategy.LATENCY_OPTIMIZED: StrategyWeights(
        weight_quality=0.20,
        weight_cost=0.10,
        weight_latency=0.45,
        weight_reliability=0.20,
        weight_risk=0.05,
    ),
    OptimizationStrategy.QUALITY_OPTIMIZED: StrategyWeights(
        weight_quality=0.45,
        weight_cost=0.10,
        weight_latency=0.10,
        weight_reliability=0.25,
        weight_risk=0.10,
    ),
    OptimizationStrategy.RISK_MINIMIZED: StrategyWeights(
        weight_quality=0.25,
        weight_cost=0.05,
        weight_latency=0.10,
        weight_reliability=0.35,
        weight_risk=0.25,
    ),
}
