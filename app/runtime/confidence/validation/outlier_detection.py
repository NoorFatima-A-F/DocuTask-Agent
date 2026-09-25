"""
Outlier Detection for Phase 13.3 (ASCE-CGP).
Detects anomalous confidence deviations using Z-score statistics.
"""

from typing import Dict, List, Any


class OutlierDetectionEngine:
    """
    Identifies statistical outliers in confidence telemetry.
    """

    @classmethod
    def detect_outliers(cls, scores: List[float], threshold_z: float = 2.5) -> Dict[str, Any]:
        if len(scores) < 4:
            return {"outliers_found": 0, "outlier_scores": []}

        mean = sum(scores) / len(scores)
        std = (sum((x - mean) ** 2 for x in scores) / (len(scores) - 1)) ** 0.5

        if std < 1e-6:
            return {"outliers_found": 0, "outlier_scores": []}

        outliers = []
        for s in scores:
            z = abs(s - mean) / std
            if z > threshold_z:
                outliers.append({"score": s, "z_score": round(z, 2)})

        return {
            "outliers_found": len(outliers),
            "outlier_scores": outliers,
            "mean": round(mean, 4),
            "std_dev": round(std, 4),
        }
