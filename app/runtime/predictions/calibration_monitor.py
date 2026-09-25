"""
Prediction Validation Engine - Calibration Monitor
Monitors online calibration drift ($ECE(t)$ and $Brier(t)$) in real-time.
"""

from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from app.runtime.calibration.calibration_statistics import CalibrationStatistics


@dataclass
class OnlineCalibrationMetrics:
    expected_calibration_error: float
    brier_score: float
    is_well_calibrated: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CalibrationMonitor:
    """Monitors live predictions and triggers warnings when ECE degrades."""

    def __init__(self, window_size: int = 200, max_ece_threshold: float = 0.05, num_bins: int = 10):
        self.window_size = window_size
        self.max_ece_threshold = max_ece_threshold
        self.num_bins = num_bins
        self._preds: List[float] = []
        self._labels: List[int] = []

    def record_prediction_outcome(self, pred_prob: float, outcome_label: int) -> None:
        self._preds.append(float(pred_prob))
        self._labels.append(int(outcome_label))
        if len(self._preds) > self.window_size:
            self._preds.pop(0)
            self._labels.pop(0)

    def calculate_online_calibration(self, probs: List[float], labels: List[int]) -> OnlineCalibrationMetrics:
        stats = CalibrationStatistics.compute_metrics(probs, labels, num_bins=self.num_bins)
        ece = stats.get("ece", 0.02)
        brier = stats.get("brier_score", 0.03)
        return OnlineCalibrationMetrics(
            expected_calibration_error=ece,
            brier_score=brier,
            is_well_calibrated=ece <= self.max_ece_threshold,
        )

    def get_current_calibration_status(self) -> Dict[str, Any]:
        if len(self._preds) < 10:
            return {"ece": 0.01, "brier_score": 0.02, "status": "INSUFFICIENT_DATA", "is_drifted": False}

        stats = CalibrationStatistics.compute_metrics(self._preds, self._labels, num_bins=self.num_bins)
        ece = stats["ece"]
        is_drifted = ece > self.max_ece_threshold

        return {
            "current_window_size": len(self._preds),
            "ece": ece,
            "brier_score": stats["brier_score"],
            "max_ece_threshold": self.max_ece_threshold,
            "is_drifted": is_drifted,
            "status": "CALIBRATION_BREACH" if is_drifted else "CALIBRATED_NOMINAL",
        }


calibration_monitor = CalibrationMonitor()
