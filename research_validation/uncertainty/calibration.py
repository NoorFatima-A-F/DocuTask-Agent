"""
Probability & Confidence Calibration (Phase 82B.9)
==================================================
Evaluates empirical probability calibration for model predictions and decision
engines. Computes Expected Calibration Error (ECE), Maximum Calibration Error (MCE),
and Brier Score.
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from research_validation.provenance.hashing import hash_canonical_json


@dataclass(frozen=True)
class CalibrationBin:
    bin_index: int
    confidence_min: float
    confidence_max: float
    mean_confidence: float
    empirical_accuracy: float
    sample_count: int
    bin_error: float


@dataclass(frozen=True)
class CalibrationAuditReport:
    report_id: str
    expected_calibration_error: float  # ECE
    maximum_calibration_error: float   # MCE
    brier_score: float
    is_well_calibrated: bool           # ECE < 0.05
    total_samples: int
    bins: Tuple[CalibrationBin, ...]
    timestamp_utc: str
    calibration_digest: str


class EmpiricalCalibrationEngine:
    """
    Computes ECE, MCE, and reliability binning.
    """

    @classmethod
    def evaluate_calibration(
        cls,
        confidences: List[float],
        ground_truths: List[int],  # 1 for correct, 0 for incorrect
        num_bins: int = 10,
    ) -> CalibrationAuditReport:
        """Calculate ECE, MCE, and Brier Score across uniform confidence bins."""
        if len(confidences) != len(ground_truths) or not confidences:
            raise ValueError("Confidences and ground_truths must have equal non-zero lengths.")

        now_str = datetime.now(timezone.utc).isoformat()
        n = len(confidences)

        # Brier Score = (1/N) * sum((conf - gt)^2)
        brier = sum((c - gt)**2 for c, gt in zip(confidences, ground_truths)) / n

        bin_width = 1.0 / num_bins
        bins: List[CalibrationBin] = []
        ece = 0.0
        mce = 0.0

        for b_idx in range(num_bins):
            b_min = b_idx * bin_width
            b_max = (b_idx + 1) * bin_width

            # Find samples in bin
            bin_samples = [
                (c, gt) for c, gt in zip(confidences, ground_truths)
                if (b_min <= c < b_max) or (b_idx == num_bins - 1 and c == b_max)
            ]
            count = len(bin_samples)

            if count > 0:
                mean_conf = sum(c for c, _ in bin_samples) / count
                emp_acc = sum(gt for _, gt in bin_samples) / count
                err = abs(emp_acc - mean_conf)
                ece += (count / n) * err
                if err > mce:
                    mce = err
            else:
                mean_conf = (b_min + b_max) / 2.0
                emp_acc = 0.0
                err = 0.0

            bins.append(CalibrationBin(
                bin_index=b_idx,
                confidence_min=b_min,
                confidence_max=b_max,
                mean_confidence=mean_conf,
                empirical_accuracy=emp_acc,
                sample_count=count,
                bin_error=err,
            ))

        well_calibrated = (ece < 0.05)
        h_payload = {
            "ece": ece,
            "mce": mce,
            "brier": brier,
            "samples": n,
        }
        digest = hash_canonical_json(h_payload)

        return CalibrationAuditReport(
            report_id=f"calib_{int(datetime.now(timezone.utc).timestamp())}",
            expected_calibration_error=ece,
            maximum_calibration_error=mce,
            brier_score=brier,
            is_well_calibrated=well_calibrated,
            total_samples=n,
            bins=tuple(bins),
            timestamp_utc=now_str,
            calibration_digest=digest,
        )
