"""
Regression Testing & Historical Quality Detection Subsystem.
Detects extraction quality degradation across prompt, model, or provider iterations.
"""

from app.core.logging import logger
from app.validation.schemas import MetricEvaluationResult, RegressionComparison


class RegressionEngine:
    """Engine comparing evaluation metrics against baseline to detect regressions."""

    MINOR_THRESHOLD = 0.02    # 2% drop
    WARNING_THRESHOLD = 0.05  # 5% drop

    @classmethod
    def compare(
        cls,
        current_metrics: MetricEvaluationResult,
        baseline_accuracy: float = 0.95,
        baseline_version: str = "v1.0_baseline",
        current_version: str = "v1.1_candidate"
    ) -> RegressionComparison:
        """
        Compares current evaluation field accuracy against baseline accuracy.
        """
        curr_acc = current_metrics.field_accuracy
        delta = round(curr_acc - baseline_accuracy, 4)

        is_regression = delta < 0
        severity = "NONE"

        if is_regression:
            abs_drop = abs(delta)
            if abs_drop > cls.WARNING_THRESHOLD:
                severity = "CRITICAL"
            elif abs_drop >= cls.MINOR_THRESHOLD:
                severity = "WARNING"
            else:
                severity = "MINOR"

            logger.warning(
                f"Quality regression detected ({severity}): Baseline={baseline_accuracy}, Current={curr_acc}, Drop={abs_drop * 100:.1f}%"
            )

        return RegressionComparison(
            baseline_version=baseline_version,
            current_version=current_version,
            baseline_accuracy=baseline_accuracy,
            current_accuracy=curr_acc,
            accuracy_delta=delta,
            regression_severity=severity,
            is_regression=is_regression,
            details={
                "precision": current_metrics.precision,
                "recall": current_metrics.recall,
                "f1_score": current_metrics.f1_score,
                "hallucination_rate": current_metrics.hallucination_rate
            }
        )
