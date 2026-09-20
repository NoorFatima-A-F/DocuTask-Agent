"""
Prediction Validation Engine - Prediction Validator
Enforces maximum error tolerance bounds on model predictions.
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from app.runtime.predictions.prediction_error import PredictionAccuracyMetrics


@dataclass
class PredictionValidationReport:
    is_within_tolerance: bool
    breach_reasons: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class PredictionValidator:
    """Validates that predictive models satisfy enterprise accuracy criteria."""

    def __init__(
        self,
        max_allowed_mae_accuracy: float = 0.08,
        max_allowed_mae_latency: float = 150.0,
        max_allowed_mape: float = 15.0,
    ):
        self.max_allowed_mae_accuracy = max_allowed_mae_accuracy
        self.max_allowed_mae_latency = max_allowed_mae_latency
        self.max_allowed_mape = max_allowed_mape

    def validate_prediction_bounds(
        self,
        accuracy_metrics: PredictionAccuracyMetrics,
        latency_metrics: PredictionAccuracyMetrics,
    ) -> PredictionValidationReport:
        breaches = []
        if accuracy_metrics.mae > self.max_allowed_mae_accuracy:
            breaches.append(f"Accuracy MAE {accuracy_metrics.mae} exceeds tolerance {self.max_allowed_mae_accuracy}")
        if latency_metrics.mae > self.max_allowed_mae_latency:
            breaches.append(f"Latency MAE {latency_metrics.mae} exceeds tolerance {self.max_allowed_mae_latency}")

        return PredictionValidationReport(
            is_within_tolerance=len(breaches) == 0,
            breach_reasons=breaches,
        )

    @staticmethod
    def validate_accuracy(metrics: PredictionAccuracyMetrics, max_allowed_mape: float = 15.0) -> Tuple[bool, List[str]]:
        errors = []
        if metrics.mape_percent > max_allowed_mape and metrics.mae > 0.10:
            errors.append(f"Dimension '{metrics.dimension}' MAPE ({metrics.mape_percent:.1f}%) exceeds threshold ({max_allowed_mape:.1f}%)")

        if abs(metrics.mean_bias) > 0.15:
            errors.append(f"Dimension '{metrics.dimension}' shows severe systematic prediction bias ({metrics.mean_bias:.4f})")

        return len(errors) == 0, errors
