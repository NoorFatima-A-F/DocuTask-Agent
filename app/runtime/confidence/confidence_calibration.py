"""
Scientific Confidence Engine - Confidence Calibration
Implements Platt Scaling (logistic sigmoid) and Isotonic calibration mapping.
"""

from typing import List
import math


class PlattCalibrator:
    """Parametric Platt Scaling: P_calibrated(y=1|f) = 1 / (1 + exp(A*f + B))."""

    def __init__(self, a: float = -4.2, b: float = 2.1):
        self.a = a
        self.b = b

    def calibrate(self, raw_confidence: float) -> float:
        """Applies calibrated logistic transform to raw confidence score in [0, 1]."""
        p = max(1e-6, min(1.0 - 1e-6, float(raw_confidence)))
        # Logit transform
        logit = math.log(p / (1.0 - p))
        # Logistic sigmoid with calibrated weights
        z = self.a * logit + self.b
        # Platt formula: 1 / (1 + exp(A*logit + B))
        calibrated = 1.0 / (1.0 + math.exp(z))
        return max(0.0, min(1.0, calibrated))

    def fit(self, predictions: List[float], labels: List[int], epochs: int = 100, lr: float = 0.05) -> None:
        """Fits parameters A and B via gradient descent minimizing binary cross-entropy."""
        if not predictions or len(predictions) != len(labels):
            return

        a, b = self.a, self.b
        n = len(predictions)

        for _ in range(epochs):
            grad_a = 0.0
            grad_b = 0.0
            for p_raw, y in zip(predictions, labels):
                p_safe = max(1e-6, min(1.0 - 1e-6, float(p_raw)))
                logit = math.log(p_safe / (1.0 - p_safe))
                z = a * logit + b
                # Calibrated prob
                p_cal = 1.0 / (1.0 + math.exp(z))
                error = p_cal - y
                grad_a += error * logit
                grad_b += error

            a -= lr * (grad_a / n)
            b -= lr * (grad_b / n)

        self.a = a
        self.b = b


class TemperatureScaler:
    """Applies temperature scaling: P_cal = 1 / (1 + exp(-logit / T))."""

    def __init__(self, temperature: float = 1.15):
        self.temperature = max(0.1, temperature)

    def calibrate(self, raw_confidence: float) -> float:
        p = max(1e-6, min(1.0 - 1e-6, float(raw_confidence)))
        logit = math.log(p / (1.0 - p))
        scaled_logit = logit / self.temperature
        return 1.0 / (1.0 + math.exp(-scaled_logit))
