"""
Plan Selector for Autonomous Plan Optimization Engine.
Conducts multi-objective Pareto evaluation across candidate execution plans,
scoring Quality, Cost, Latency, Reliability, and Risk against strategic goals.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from app.agents.planning.execution_plan import ExecutionPlan
from app.agents.planning.optimizer.cost_optimizer import CostOptimizer
from app.agents.planning.optimizer.latency_optimizer import LatencyOptimizer
from app.agents.planning.optimizer.optimization_strategy import (
    OptimizationStrategy,
    STRATEGY_PRESETS,
    StrategyWeights,
)
from app.agents.planning.optimizer.risk_optimizer import RiskOptimizer

logger = logging.getLogger(__name__)


@dataclass
class PlanEvaluationMetrics:
    """Detailed score breakdown for an evaluated plan."""

    plan_name: str
    composite_score: float
    quality_score: float
    cost_usd: float
    cost_score: float
    latency_ms: float
    latency_score: float
    reliability_score: float
    risk_score: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plan_name": self.plan_name,
            "composite_score": round(self.composite_score, 4),
            "quality_score": round(self.quality_score, 4),
            "cost_usd": round(self.cost_usd, 6),
            "cost_score": round(self.cost_score, 4),
            "latency_ms": round(self.latency_ms, 2),
            "latency_score": round(self.latency_score, 4),
            "reliability_score": round(self.reliability_score, 4),
            "risk_score": round(self.risk_score, 4),
        }


@dataclass
class PlanOptimizationResult:
    """Final selection deliverable from the optimizer."""

    selected_plan: ExecutionPlan
    winning_strategy: str
    winning_metrics: PlanEvaluationMetrics
    all_evaluated_metrics: List[PlanEvaluationMetrics]
    optimization_summary: str


class PlanSelector:
    """Orchestrates candidate generation, multi-criteria scoring, and final plan selection."""

    def __init__(
        self,
        cost_optimizer: Optional[CostOptimizer] = None,
        latency_optimizer: Optional[LatencyOptimizer] = None,
        risk_optimizer: Optional[RiskOptimizer] = None,
    ) -> None:
        self.cost_optimizer = cost_optimizer or CostOptimizer()
        self.latency_optimizer = latency_optimizer or LatencyOptimizer()
        self.risk_optimizer = risk_optimizer or RiskOptimizer()

    def score_plan(
        self,
        plan: ExecutionPlan,
        plan_name: str,
        weights: StrategyWeights,
        max_cost_bound: float = 0.05,
        max_latency_bound: float = 1000.0,
    ) -> PlanEvaluationMetrics:
        """Evaluates a single plan across all 5 dimensions."""
        cost = self.cost_optimizer.estimate_plan_cost(plan)
        latency = self.latency_optimizer.estimate_total_latency(plan)
        risk = self.risk_optimizer.estimate_plan_risk(plan)

        # Baseline quality from plan validation checks
        validation_count = sum(1 for t in plan.tasks if "val" in t.action.lower() or "check" in t.action.lower())
        quality_score = min(1.0, 0.85 + (0.05 * validation_count))

        # Reliability from retries and fallbacks
        fallback_ratio = len(plan.fallback_strategies) / max(1, len(plan.tasks))
        reliability_score = min(1.0, 0.70 + (0.30 * fallback_ratio))

        # Normalized scores in [0, 1] where 1.0 is best
        norm_cost_score = max(0.0, 1.0 - (cost / max_cost_bound))
        norm_latency_score = max(0.0, 1.0 - (latency / max_latency_bound))
        norm_risk_penalty = risk

        # Composite multi-objective Pareto score
        composite = (
            weights.weight_quality * quality_score
            + weights.weight_cost * norm_cost_score
            + weights.weight_latency * norm_latency_score
            + weights.weight_reliability * reliability_score
            - weights.weight_risk * norm_risk_penalty
        )

        return PlanEvaluationMetrics(
            plan_name=plan_name,
            composite_score=max(0.0, composite),
            quality_score=quality_score,
            cost_usd=cost,
            cost_score=norm_cost_score,
            latency_ms=latency,
            latency_score=norm_latency_score,
            reliability_score=reliability_score,
            risk_score=risk,
        )

    def optimize_and_select(
        self,
        base_plan: ExecutionPlan,
        strategy: OptimizationStrategy = OptimizationStrategy.BALANCED,
    ) -> PlanOptimizationResult:
        """
        Generates candidate plans (original, cost-optimized, latency-optimized, risk-hardened),
        evaluates all candidates with strategy weights, and returns the highest-scoring plan.
        """
        weights = STRATEGY_PRESETS.get(strategy, STRATEGY_PRESETS[OptimizationStrategy.BALANCED])

        # Generate candidates
        candidates: List[Tuple[str, ExecutionPlan]] = [
            ("Baseline_Plan", base_plan),
        ]

        cost_plan, _ = self.cost_optimizer.optimize(base_plan)
        candidates.append(("Cost_Optimized_Plan", cost_plan))

        lat_plan, _ = self.latency_optimizer.optimize(base_plan)
        candidates.append(("Latency_Optimized_Plan", lat_plan))

        risk_plan, _ = self.risk_optimizer.optimize(base_plan)
        candidates.append(("Risk_Hardened_Plan", risk_plan))

        # Combined multi-optimized candidate
        combo_plan, _ = self.latency_optimizer.optimize(risk_plan)
        candidates.append(("Combined_Optimal_Plan", combo_plan))

        # Score all candidates
        evaluated_metrics: List[Tuple[ExecutionPlan, PlanEvaluationMetrics]] = []
        for name, plan in candidates:
            metrics = self.score_plan(plan=plan, plan_name=name, weights=weights)
            evaluated_metrics.append((plan, metrics))

        # Sort descending by composite score
        evaluated_metrics.sort(key=lambda x: x[1].composite_score, reverse=True)
        winner_plan, winner_metrics = evaluated_metrics[0]

        summary = (
            f"Selected '{winner_metrics.plan_name}' using '{strategy.value}' strategy with "
            f"composite score {winner_metrics.composite_score:.3f} "
            f"(Quality: {winner_metrics.quality_score:.2f}, Latency: {winner_metrics.latency_ms:.1f}ms, "
            f"Cost: ${winner_metrics.cost_usd:.5f}, Risk: {winner_metrics.risk_score:.2f})."
        )
        logger.info(summary)

        return PlanOptimizationResult(
            selected_plan=winner_plan,
            winning_strategy=strategy.value,
            winning_metrics=winner_metrics,
            all_evaluated_metrics=[m for _, m in evaluated_metrics],
            optimization_summary=summary,
        )
