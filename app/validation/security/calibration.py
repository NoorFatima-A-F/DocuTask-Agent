"""
Confidence Calibration & Uncertainty Evaluation Subsystem.
Computes Expected Calibration Error (ECE), Brier Score, and Reliability Calibration Curves.
"""

import math
from typing import List, Tuple
from pydantic import BaseModel, Field
from app.core.logging import logger


class CalibrationMetrics(BaseModel):
    """Metrics quantifying confidence calibration error."""
    expected_calibration_error: float = Field(..., description="Expected Calibration Error (ECE)")
    brier_score: float = Field(..., description="Brier Score (lower is better, 0.0 is perfect)")
    calibration_bins: List[dict] = Field(default_factory=list, description="Reliability diagram bin breakdown")


class ConfidenceCalibrator:
    """Calibrator computing ECE, Brier Score, and reliability diagrams."""

    @classmethod
    def compute_calibration(
        cls,
        confidences: List[float],
        accuracies: List[float],
        num_bins: int = 5
    ) -> CalibrationMetrics:
        """
        Computes ECE and Brier Score over paired confidence and accuracy samples.
        """
        if not confidences or not accuracies or len(confidences) != len(accuracies):
            return CalibrationMetrics(
                expected_calibration_error=0.0,
                brier_score=0.0,
                calibration_bins=[]
            )

        n = len(confidences)

        # 1. Brier Score
        brier_sum = sum((conf - acc) ** 2 for conf, acc in zip(confidences, accuracies))
        brier_score = round(brier_sum / n, 4)

        # 2. Expected Calibration Error (ECE)
        bins = [[] for _ in range(num_bins)]
        bin_width = 1.0 / num_bins

        for conf, acc in zip(confidences, accuracies):
            bin_idx = min(int(conf / bin_width), num_bins - 1)
            bins[bin_idx].append((conf, acc))

        ece = 0.0
        bin_records = []

        for idx, bin_samples in enumerate(bins):
            bin_lower = idx * bin_width
            bin_upper = (idx + 1) * bin_width
            count = len(bin_samples)

            if count > 0:
                avg_conf = sum(c for c, _ in bin_samples) / count
                avg_acc = sum(a for _, a in bin_samples) / count
                ece += (count / n) * abs(avg_acc - avg_conf)

                bin_records.append({
                    "bin": f"[{bin_lower:.1f}-{bin_upper:.1f}]",
                    "sample_count": count,
                    "avg_confidence": round(avg_conf, 4),
                    "avg_accuracy": round(avg_acc, 4),
                    "bin_calibration_error": round(abs(avg_acc - avg_conf), 4)
                })

        logger.info(f"Calculated Confidence Calibration: ECE={ece:.4f}, BrierScore={brier_score:.4f}")

        return CalibrationMetrics(
            expected_calibration_error=round(ece, 4),
            brier_score=brier_score,
            calibration_bins=bin_records
        )
