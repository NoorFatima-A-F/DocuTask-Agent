"""
Accuracy and quality comparative evaluation engine.
"""

from typing import Dict, Any
from app.business_value_verification.domain.models import AccuracyComparison


class AccuracyComparator:
    """Evaluates field-level error rates and anomaly detection between human and AI workflows."""

    @staticmethod
    def compare_accuracy(
        human_error_pct: float = 8.2,
        ai_error_pct: float = 0.55,
        human_missed_anomalies_pct: float = 14.5,
        ai_caught_anomalies_pct: float = 98.8,
    ) -> AccuracyComparison:
        quality_improvement = ((human_error_pct - ai_error_pct) / human_error_pct * 100.0) if human_error_pct > 0 else 0.0

        return AccuracyComparison(
            human_field_error_rate_pct=human_error_pct,
            ai_field_error_rate_pct=ai_error_pct,
            human_missed_anomalies_pct=human_missed_anomalies_pct,
            ai_caught_anomalies_pct=ai_caught_anomalies_pct,
            overall_quality_improvement_pct=quality_improvement,
        )
