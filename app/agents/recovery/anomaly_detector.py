"""
Anomaly Detector.
Detects abnormal failure spikes or sudden latency degradation.
"""

from typing import List


class AnomalyDetector:
    """Detects statistical execution anomalies across sliding windows."""

    def detect_failure_spike(self, failure_rates: List[float], spike_threshold: float = 0.5) -> bool:
        if not failure_rates:
            return False
        avg = sum(failure_rates) / len(failure_rates)
        return avg >= spike_threshold
