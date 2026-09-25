"""Model Evaluation Scoring & Leaderboard Engine (Phase 8C)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from app.model_governance.evaluation.metrics import ModelEvaluationMetrics


class ModelEvaluationScorer:
    """Manages benchmark score records and competitive model leaderboards."""

    def __init__(self):
        # model_id -> List[ModelEvaluationMetrics]
        self._evaluations: Dict[str, List[ModelEvaluationMetrics]] = {}

    def record_evaluation(self, metrics: ModelEvaluationMetrics) -> ModelEvaluationMetrics:
        """Store evaluation metrics."""
        if metrics.model_id not in self._evaluations:
            self._evaluations[metrics.model_id] = []
        self._evaluations[metrics.model_id].append(metrics)
        return metrics

    def record_score(self, model_id: str, metrics: ModelEvaluationMetrics) -> ModelEvaluationMetrics:
        metrics.model_id = model_id
        return self.record_evaluation(metrics)

    def get_latest_evaluation(self, model_id: str) -> Optional[ModelEvaluationMetrics]:
        """Get most recent evaluation scores."""
        evals = self._evaluations.get(model_id, [])
        return evals[-1] if evals else None

    def get_leaderboard(self) -> List[Dict[str, Any]]:
        """Rank all evaluated models by composite quality score descending."""
        latest = [evals[-1] for evals in self._evaluations.values() if evals]
        sorted_evals = sorted(latest, key=lambda m: (m.composite_quality_score or m.composite_score), reverse=True)
        return [
            {
                "model_id": m.model_id,
                "composite_score": m.composite_score or m.composite_quality_score,
                "accuracy": m.accuracy or m.accuracy_score,
                "faithfulness": m.faithfulness or m.faithfulness_score,
                "evaluated_at": m.evaluated_at,
            }
            for m in sorted_evals
        ]
