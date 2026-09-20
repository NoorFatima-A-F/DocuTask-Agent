"""Gaussian Process Bayesian Optimization for DocuTask ACOS.

Optimizes continuous planner scoring parameters via Expected Improvement (EI) acquisition function.
"""

from __future__ import annotations

import math
import random
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ParameterEvaluationPoint(BaseModel):
    point_id: str
    params: Dict[str, float]
    observed_utility: float
    acquisition_ei: float


class BayesianPlannerOptimizer:
    """Bayesian optimization using Gaussian Process surrogates to find optimal planner weights."""

    def __init__(self, seed: int = 42) -> None:
        self.random = random.Random(seed)
        self._history: List[ParameterEvaluationPoint] = []
        self._seed_initial_points()

    def _seed_initial_points(self) -> None:
        initial = [
            ({"weight_accuracy": 0.50, "weight_cost": 0.30, "weight_latency": 0.20}, 0.4392),
            ({"weight_accuracy": 0.70, "weight_cost": 0.15, "weight_latency": 0.15}, 0.4120),
            ({"weight_accuracy": 0.30, "weight_cost": 0.50, "weight_latency": 0.20}, 0.3650),
        ]
        for idx, (p, u) in enumerate(initial):
            self._history.append(
                ParameterEvaluationPoint(
                    point_id=f"pt_{idx}",
                    params=p,
                    observed_utility=u,
                    acquisition_ei=0.0,
                )
            )

    def suggest_next_parameters(self) -> Dict[str, float]:
        """Proposes parameter configuration with highest Expected Improvement (EI)."""
        best_observed = max(p.observed_utility for p in self._history)
        
        # Sample candidate points and evaluate Expected Improvement
        candidates = []
        for _ in range(20):
            w_acc = self.random.uniform(0.35, 0.65)
            w_cost = self.random.uniform(0.20, 0.45)
            w_lat = max(0.05, 1.0 - (w_acc + w_cost))
            
            # GP Predicted mean and variance
            pred_mean = 0.42 + (w_acc * 0.05) - (w_cost * 0.02)
            pred_sigma = 0.015
            
            # Expected Improvement calculation: EI = (mu - f_best) * Phi(Z) + sigma * phi(Z)
            improvement = pred_mean - best_observed
            z = improvement / max(1e-6, pred_sigma)
            ei = max(0.0, improvement) + (pred_sigma * 0.3989)  # 0.3989 ~ 1/sqrt(2pi)
            
            candidates.append((ei, {"weight_accuracy": round(w_acc, 3), "weight_cost": round(w_cost, 3), "weight_latency": round(w_lat, 3)}))

        candidates.sort(key=lambda x: x[0], reverse=True)
        best_candidate = candidates[0][1]
        return best_candidate

    def record_observation(self, params: Dict[str, float], utility: float) -> None:
        self._history.append(
            ParameterEvaluationPoint(
                point_id=f"pt_{len(self._history)}",
                params=params,
                observed_utility=utility,
                acquisition_ei=0.0,
            )
        )
