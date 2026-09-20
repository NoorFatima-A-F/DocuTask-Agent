"""Model Evaluation Metrics (Phase 8C)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, model_validator


class ModelEvaluationMetrics(BaseModel):
    """Multidimensional evaluation scores."""
    evaluation_id: str = Field(default_factory=lambda: "eval_default")
    model_id: str = "model_default"
    benchmark_name: str = "general_benchmark"
    accuracy: float = 0.90
    accuracy_score: Optional[float] = None
    faithfulness: float = 0.90
    faithfulness_score: Optional[float] = None
    completeness: float = 0.90
    completeness_score: Optional[float] = None
    consistency: float = 0.90
    consistency_score: Optional[float] = None
    avg_latency_ms: float = 200.0
    average_latency_ms: Optional[float] = None
    hallucination_rate: float = 0.05
    composite_score: float = 0.0
    composite_quality_score: float = 0.0
    evaluated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @model_validator(mode="before")
    @classmethod
    def sync_metrics_fields(cls, values: Any) -> Any:
        if isinstance(values, dict):
            if "accuracy_score" in values and "accuracy" not in values:
                values["accuracy"] = values["accuracy_score"]
            elif "accuracy" in values and not values.get("accuracy_score"):
                values["accuracy_score"] = values["accuracy"]

            if "faithfulness_score" in values and "faithfulness" not in values:
                values["faithfulness"] = values["faithfulness_score"]
            elif "faithfulness" in values and not values.get("faithfulness_score"):
                values["faithfulness_score"] = values["faithfulness"]

            if "completeness_score" in values and "completeness" not in values:
                values["completeness"] = values["completeness_score"]
            elif "completeness" in values and not values.get("completeness_score"):
                values["completeness_score"] = values["completeness"]

            if "consistency_score" in values and "consistency" not in values:
                values["consistency"] = values["consistency_score"]
            elif "consistency" in values and not values.get("consistency_score"):
                values["consistency_score"] = values["consistency"]

            if "average_latency_ms" in values and "avg_latency_ms" not in values:
                values["avg_latency_ms"] = values["average_latency_ms"]
            elif "avg_latency_ms" in values and not values.get("average_latency_ms"):
                values["average_latency_ms"] = values["avg_latency_ms"]

        return values

    def compute_composite_score(self) -> float:
        acc = self.accuracy if self.accuracy is not None else (self.accuracy_score or 0.0)
        faith = self.faithfulness if self.faithfulness is not None else (self.faithfulness_score or 0.0)
        comp = self.completeness if self.completeness is not None else (self.completeness_score or 0.0)
        halluc = self.hallucination_rate or 0.0

        score = (acc * 0.35 + faith * 0.35 + comp * 0.15 + (1.0 - halluc) * 0.15)
        self.composite_score = round(score, 4)
        self.composite_quality_score = self.composite_score
        return self.composite_score
