"""
Execution Performance & Cost Predictor.

Compares analytical pre-execution predictions against live actuals as nodes finish.
"""

from __future__ import annotations

from typing import Any, Dict
from pydantic import BaseModel
from app.runtime.planning.graph.dag import ExecutionDAG


class PredictionComparison(BaseModel):
    predicted_runtime_ms: float
    actual_runtime_ms: float
    runtime_variance_pct: float
    predicted_cost_usd: float
    actual_cost_usd: float
    cost_variance_pct: float
    accuracy_score: float  # [0.0, 1.0]


class ExecutionPredictor:
    """Evaluates prediction accuracy against real execution results."""

    @classmethod
    def compare_prediction_vs_actual(
        cls, dag: ExecutionDAG, actual_runtime_ms: float, actual_cost_usd: float
    ) -> PredictionComparison:
        _, pred_dur = dag.compute_critical_path()
        pred_cost = sum(n.estimated_cost_usd for n in dag.nodes.values())

        runtime_var = ((actual_runtime_ms - pred_dur) / max(1.0, pred_dur)) * 100.0
        cost_var = ((actual_cost_usd - pred_cost) / max(0.0001, pred_cost)) * 100.0

        # Accuracy score penalizes large divergence
        divergence = (abs(runtime_var) + abs(cost_var)) / 200.0
        accuracy = max(0.0, min(1.0, 1.0 - divergence))

        return PredictionComparison(
            predicted_runtime_ms=round(pred_dur, 2),
            actual_runtime_ms=round(actual_runtime_ms, 2),
            runtime_variance_pct=round(runtime_var, 2),
            predicted_cost_usd=round(pred_cost, 5),
            actual_cost_usd=round(actual_cost_usd, 5),
            cost_variance_pct=round(cost_var, 2),
            accuracy_score=round(accuracy, 3),
        )
