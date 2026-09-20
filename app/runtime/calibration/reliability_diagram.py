"""
Scientific Calibration Platform - Reliability Diagram Data Generator
Bins predictions and empirical observations into confidence intervals for reliability visualization.
"""

from typing import List, Dict, Any, Tuple
import math


class ReliabilityDiagramGenerator:
    """Generates binned accuracy vs confidence points for reliability diagrams."""

    @staticmethod
    def generate_bins(
        predictions: List[float],
        labels: List[int],
        num_bins: int = 10,
    ) -> List[Dict[str, Any]]:
        if not predictions or len(predictions) != len(labels):
            return []

        bin_size = 1.0 / num_bins
        bins_data: List[Dict[str, Any]] = []

        for b in range(num_bins):
            bin_lower = b * bin_size
            bin_upper = (b + 1) * bin_size

            bin_preds = []
            bin_labels = []

            for p, y in zip(predictions, labels):
                if b == num_bins - 1:
                    in_bin = bin_lower <= p <= bin_upper
                else:
                    in_bin = bin_lower <= p < bin_upper

                if in_bin:
                    bin_preds.append(p)
                    bin_labels.append(y)

            count = len(bin_preds)
            avg_confidence = (sum(bin_preds) / count) if count > 0 else (bin_lower + bin_upper) / 2.0
            empirical_accuracy = (sum(bin_labels) / count) if count > 0 else 0.0
            calibration_gap = abs(empirical_accuracy - avg_confidence) if count > 0 else 0.0

            bins_data.append({
                "bin_index": b,
                "bin_range": f"{bin_lower:.1f}-{bin_upper:.1f}",
                "sample_count": count,
                "average_confidence": round(avg_confidence, 4),
                "empirical_accuracy": round(empirical_accuracy, 4),
                "calibration_gap": round(calibration_gap, 4),
            })

        return bins_data
