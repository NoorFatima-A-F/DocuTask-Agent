"""
Scientific Calibration Platform - Calibration Statistics
Computes ECE (Expected Calibration Error), MCE (Maximum Calibration Error), and Brier Score.
"""

from typing import List, Dict, Any
import math


class CalibrationStatistics:
    """Calculates formal calibration metrics: ECE, MCE, and Brier Score."""

    @staticmethod
    def compute_metrics(
        predictions: List[float],
        labels: List[int],
        num_bins: int = 10,
    ) -> Dict[str, float]:
        if not predictions or len(predictions) != len(labels):
            return {"ece": 0.0, "mce": 0.0, "brier_score": 0.0, "log_loss": 0.0}

        n = len(predictions)

        # 1. Brier Score: (1/N) * sum( (p_i - y_i)^2 )
        brier = sum((p - y) ** 2 for p, y in zip(predictions, labels)) / n

        # 2. Log-loss: -(1/N) * sum( y*log(p) + (1-y)*log(1-p) )
        log_loss_sum = 0.0
        for p, y in zip(predictions, labels):
            p_safe = max(1e-6, min(1.0 - 1e-6, p))
            log_loss_sum += -(y * math.log(p_safe) + (1 - y) * math.log(1.0 - p_safe))
        log_loss = log_loss_sum / n

        # 3. ECE & MCE across bins
        bin_size = 1.0 / num_bins
        ece = 0.0
        mce = 0.0

        for b in range(num_bins):
            bin_lower = b * bin_size
            bin_upper = (b + 1) * bin_size

            bin_preds = []
            bin_labels = []

            for p, y in zip(predictions, labels):
                in_bin = (bin_lower <= p <= bin_upper) if b == num_bins - 1 else (bin_lower <= p < bin_upper)
                if in_bin:
                    bin_preds.append(p)
                    bin_labels.append(y)

            k = len(bin_preds)
            if k > 0:
                avg_conf = sum(bin_preds) / k
                acc = sum(bin_labels) / k
                gap = abs(acc - avg_conf)
                ece += (k / n) * gap
                if gap > mce:
                    mce = gap

        return {
            "ece": round(ece, 4),
            "mce": round(mce, 4),
            "brier_score": round(brier, 4),
            "log_loss": round(log_loss, 4),
        }
