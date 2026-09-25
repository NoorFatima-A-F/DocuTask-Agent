"""
Temperature Scaling for Phase 13.3 (ASCE-CGP).
Post-hoc Platt/Temperature scaling calibration for confidence probabilities.
"""

import math


class TemperatureScalingCalibrator:
    """
    Applies temperature scaling: calibrated = sigmoid(logit(score) / T)
    """

    @classmethod
    def calibrate(cls, uncalibrated_score: float, temperature: float = 1.05) -> float:
        if uncalibrated_score <= 0.001:
            return 0.001
        if uncalibrated_score >= 0.999:
            return 0.999

        # Logit transformation
        logit = math.log(uncalibrated_score / (1.0 - uncalibrated_score))
        scaled_logit = logit / max(0.1, temperature)
        calibrated = 1.0 / (1.0 + math.exp(-scaled_logit))
        return round(calibrated, 4)
