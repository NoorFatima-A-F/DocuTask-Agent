"""Multi-Objective Utility Engine for DocuTask Autonomous Planning Platform.

Calculates mathematically rigorous, versioned multi-objective utility scores across accuracy, latency,
cost, risk, episodic memory synergy, and constraint satisfaction.
"""

from __future__ import annotations

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

from app.runtime.planning.strategy_generator import CandidateStrategy
from app.runtime.planning.cost_predictor import CostPredictionResult
from app.runtime.planning.latency_predictor import LatencyPredictionResult
from app.runtime.planning.risk_engine import StrategyRiskProfile


class UtilityWeights(BaseModel):
    """Normalized weights for multi-objective optimization (sum = 1.0)."""
    w_accuracy: float = 0.40
    w_latency: float = 0.20
    w_cost: float = 0.20
    w_risk: float = 0.10
    w_memory: float = 0.05
    w_satisfaction: float = 0.05


class UtilityScore(BaseModel):
    """Detailed utility calculation with full term breakdown and algebraic provenance."""
    strategy_id: str
    total_utility: float
    accuracy_term: float
    latency_penalty_term: float
    cost_penalty_term: float
    risk_penalty_term: float
    memory_bonus_term: float
    satisfaction_bonus_term: float
    soft_constraint_penalty: float
    raw_accuracy: float
    normalized_latency: float
    normalized_cost: float
    raw_risk: float
    weights: UtilityWeights
    equation: str = "U = w_{acc}\\cdot Acc - w_{lat}\\cdot \\tilde{L} - w_{cost}\\cdot \\tilde{C} - w_{risk}\\cdot R + w_{mem}\\cdot M + w_{sat}\\cdot S - P_{soft}"
    version: str = "2.0.0"


class MultiObjectiveUtilityEngine:
    """Calculates verifiable utility scores for strategy ranking and counterfactual evaluation."""

    MAX_NORMALIZATION_LATENCY_MS = 10000.0
    MAX_NORMALIZATION_COST_USD = 0.10

    def __init__(self, weights: Optional[UtilityWeights] = None) -> None:
        self.weights = weights or UtilityWeights()

    def calculate_utility(
        self,
        strategy: CandidateStrategy,
        cost_pred: CostPredictionResult,
        lat_pred: LatencyPredictionResult,
        risk_profile: StrategyRiskProfile,
        memory_synergy_bonus: float = 0.95,
        soft_penalty: float = 0.0,
    ) -> UtilityScore:
        w = self.weights

        # 1. Accuracy Component (Higher is better, range [0, 1])
        acc = strategy.estimated_accuracy
        acc_term = w.w_accuracy * acc

        # 2. Normalized Latency Component (Lower is better, normalized to [0, 1])
        norm_lat = min(1.0, lat_pred.critical_path_ms / self.MAX_NORMALIZATION_LATENCY_MS)
        lat_term = w.w_latency * norm_lat

        # 3. Normalized Cost Component (Lower is better, normalized to [0, 1])
        norm_cost = min(1.0, cost_pred.total_cost_usd / self.MAX_NORMALIZATION_COST_USD)
        cost_term = w.w_cost * norm_cost

        # 4. Risk Component (Lower is better, range [0, 1])
        risk = risk_profile.overall_risk_score
        risk_term = w.w_risk * risk

        # 5. Memory Synergy Bonus (Range [0, 1])
        mem_term = w.w_memory * memory_synergy_bonus

        # 6. Satisfaction Bonus (1.0 if no hard violations, else 0.0)
        is_valid = strategy.constraint_compliance.get("is_valid", True)
        sat_term = w.w_satisfaction * (1.0 if is_valid else 0.0)

        # Composite utility
        raw_utility = acc_term - lat_term - cost_term - risk_term + mem_term + sat_term - soft_penalty
        total_utility = max(-1.0, min(1.0, raw_utility))

        return UtilityScore(
            strategy_id=strategy.strategy_id,
            total_utility=round(total_utility, 4),
            accuracy_term=round(acc_term, 4),
            latency_penalty_term=round(lat_term, 4),
            cost_penalty_term=round(cost_term, 4),
            risk_penalty_term=round(risk_term, 4),
            memory_bonus_term=round(mem_term, 4),
            satisfaction_bonus_term=round(sat_term, 4),
            soft_constraint_penalty=round(soft_penalty, 4),
            raw_accuracy=round(acc, 4),
            normalized_latency=round(norm_lat, 4),
            normalized_cost=round(norm_cost, 4),
            raw_risk=round(risk, 4),
            weights=w,
        )
