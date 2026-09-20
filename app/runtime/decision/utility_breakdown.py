"""
Utility Breakdown & Objective Scoring for Explainable Decision Provenance.
Computes multi-objective Pareto trade-offs (Cost, Latency, Risk, Accuracy) without exposing hidden chain-of-thought.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class PlanUtilityScore(BaseModel):
    plan_name: str
    total_utility: float = Field(..., description="Weighted composite utility [0.0, 1.0]")
    accuracy_score: float = Field(..., description="Accuracy utility [0.0, 1.0]")
    latency_score: float = Field(..., description="Latency utility [0.0, 1.0]")
    cost_score: float = Field(..., description="Cost efficiency utility [0.0, 1.0]")
    risk_score: float = Field(..., description="Risk resilience utility [0.0, 1.0]")
    pareto_optimal: bool = Field(default=False, description="True if on Pareto frontier")
    rejection_reason: Optional[str] = Field(default=None, description="Explicit reason why not selected")


class MultiObjectiveUtilityCalculator:
    """Computes observable Pareto utility breakdown for candidate plans."""

    @staticmethod
    def calculate_utility(
        accuracy: float,
        latency_ms: float,
        cost_usd: float,
        risk: float,
        weights: Optional[Dict[str, float]] = None,
    ) -> Dict[str, float]:
        w = weights or {"accuracy": 0.40, "latency": 0.25, "cost": 0.20, "risk": 0.15}

        # Normalize metrics to [0, 1] range
        acc_norm = max(0.0, min(1.0, accuracy))
        lat_norm = max(0.0, min(1.0, 1.0 - (latency_ms / 2000.0)))
        cost_norm = max(0.0, min(1.0, 1.0 - (cost_usd / 0.05)))
        risk_norm = max(0.0, min(1.0, 1.0 - risk))

        composite = (
            w["accuracy"] * acc_norm
            + w["latency"] * lat_norm
            + w["cost"] * cost_norm
            + w["risk"] * risk_norm
        )

        return {
            "composite": round(composite, 4),
            "accuracy": round(acc_norm, 4),
            "latency": round(lat_norm, 4),
            "cost": round(cost_norm, 4),
            "risk": round(risk_norm, 4),
        }
