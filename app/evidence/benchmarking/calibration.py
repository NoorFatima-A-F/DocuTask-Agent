"""
Confidence Calibration & Uncertainty Quantification Engine.
Evaluates whether agent reported confidence probabilities align with empirical accuracy:
- Expected Calibration Error (ECE) across M equal-width confidence bins
- Maximum Calibration Error (MCE)
- Brier Score (Mean Squared Probability Error)
- Overconfidence and Underconfidence bias detection
- Reliability diagram data point generation
"""

from __future__ import annotations

import logging
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class CalibrationStatus(str, Enum):
    WELL_CALIBRATED = "WELL_CALIBRATED"
    SLIGHTLY_OVERCONFIDENT = "SLIGHTLY_OVERCONFIDENT"
    SEVERELY_OVERCONFIDENT = "SEVERELY_OVERCONFIDENT"
    UNDERCONFIDENT = "UNDERCONFIDENT"


@dataclass
class ConfidenceBinMetric:
    """Telemetry for a single confidence interval bin."""

    bin_index: int
    bin_lower: float
    bin_upper: float
    sample_count: int
    mean_confidence: float
    empirical_accuracy: float
    calibration_gap: float  # abs(accuracy - confidence)


@dataclass
class CalibrationAnalysisReport:
    """Consolidated confidence calibration report."""

    model_or_benchmark_name: str
    total_samples: int
    expected_calibration_error_ece: float
    maximum_calibration_error_mce: float
    brier_score: float
    status: CalibrationStatus
    confidence_bins: List[ConfidenceBinMetric]
    calibration_summary: str
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_name": self.model_or_benchmark_name,
            "total_samples": self.total_samples,
            "ece": round(self.expected_calibration_error_ece, 4),
            "mce": round(self.maximum_calibration_error_mce, 4),
            "brier_score": round(self.brier_score, 4),
            "status": self.status.value,
            "summary": self.calibration_summary,
            "bins": [asdict(b) for b in self.confidence_bins],
        }


class ConfidenceCalibrationEngine:
    """
    Computes statistical calibration error metrics for agent predictions.
    """

    NUM_BINS: int = 10
    ECE_WELL_CALIBRATED_THRESHOLD: float = 0.05  # < 5% ECE is well-calibrated

    @classmethod
    def evaluate_calibration(
        cls,
        benchmark_name: str,
        confidences: List[float],
        correctness_labels: List[bool],  # True for correct, False for incorrect
    ) -> CalibrationAnalysisReport:
        """Evaluates ECE, MCE, and Brier Score given probability confidences and boolean correctness."""
        n = len(confidences)
        if n == 0 or len(correctness_labels) != n:
            raise ValueError("Confidences and correctness labels must be non-empty and of equal length.")

        # 1. Compute Brier Score: (1/N) * sum((prob - label)^2)
        brier_sum = sum(
            ((confidences[i] - (1.0 if correctness_labels[i] else 0.0)) ** 2)
            for i in range(n)
        )
        brier_score = brier_sum / n

        # 2. Partition into equal-width confidence bins [0, 0.1), [0.1, 0.2) ... [0.9, 1.0]
        bins: List[ConfidenceBinMetric] = []
        bin_width = 1.0 / cls.NUM_BINS
        ece = 0.0
        mce = 0.0
        total_overconf_gap = 0.0

        for b_idx in range(cls.NUM_BINS):
            b_low = b_idx * bin_width
            b_high = (b_idx + 1) * bin_width if b_idx < (cls.NUM_BINS - 1) else 1.0001

            # Filter items in bin
            bin_items = [
                (confidences[i], correctness_labels[i])
                for i in range(n)
                if b_low <= confidences[i] < b_high or (b_idx == cls.NUM_BINS - 1 and confidences[i] == 1.0)
            ]

            b_count = len(bin_items)
            if b_count > 0:
                mean_conf = sum(p for p, _ in bin_items) / b_count
                acc = sum(1 for _, correct in bin_items if correct) / b_count
                gap = abs(acc - mean_conf)
                ece += (b_count / n) * gap
                mce = max(mce, gap)
                if mean_conf > acc:
                    total_overconf_gap += (mean_conf - acc) * (b_count / n)
            else:
                mean_conf = (b_low + b_high) / 2.0
                acc = 0.0
                gap = 0.0

            bins.append(
                ConfidenceBinMetric(
                    bin_index=b_idx,
                    bin_lower=b_low,
                    bin_upper=min(1.0, b_high),
                    sample_count=b_count,
                    mean_confidence=mean_conf,
                    empirical_accuracy=acc,
                    calibration_gap=gap,
                )
            )

        # 3. Determine status
        if ece <= cls.ECE_WELL_CALIBRATED_THRESHOLD:
            status = CalibrationStatus.WELL_CALIBRATED
            summary = f"Model is well-calibrated (ECE={ece:.3f} <= {cls.ECE_WELL_CALIBRATED_THRESHOLD}, Brier Score={brier_score:.3f})."
        elif total_overconf_gap > (ece * 0.6):
            if ece > 0.15:
                status = CalibrationStatus.SEVERELY_OVERCONFIDENT
                summary = f"WARNING: Model exhibits severe overconfidence (ECE={ece:.3f}, MCE={mce:.3f}). Reported probabilities exceed true accuracy."
            else:
                status = CalibrationStatus.SLIGHTLY_OVERCONFIDENT
                summary = f"Model is slightly overconfident (ECE={ece:.3f})."
        else:
            status = CalibrationStatus.UNDERCONFIDENT
            summary = f"Model is underconfident (ECE={ece:.3f}). Empirical accuracy exceeds reported probabilities."

        return CalibrationAnalysisReport(
            model_or_benchmark_name=benchmark_name,
            total_samples=n,
            expected_calibration_error_ece=ece,
            maximum_calibration_error_mce=mce,
            brier_score=brier_score,
            status=status,
            confidence_bins=bins,
            calibration_summary=summary,
        )
