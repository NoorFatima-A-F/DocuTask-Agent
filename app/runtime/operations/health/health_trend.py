"""
AOIS-HROP Phase 13.7 - Health Trend Analyzer
Historical health trend analysis, moving averages, EMA, and drift detection.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional


@dataclass
class HealthPoint:
    timestamp_utc: str
    composite_score: float


class HealthTrendAnalyzer:
    """
    Computes moving averages, exponential moving averages, and trajectory slopes for health history.
    """

    def __init__(self, ema_alpha: float = 0.2):
        self.ema_alpha = ema_alpha
        self._history: List[HealthPoint] = []

    def record_health(self, score: float, timestamp: Optional[str] = None):
        ts = timestamp or datetime.now(timezone.utc).isoformat()
        self._history.append(HealthPoint(timestamp_utc=ts, composite_score=score))
        if len(self._history) > 1000:
            self._history.pop(0)

    def calculate_ema(self) -> float:
        if not self._history:
            return 100.0
        ema = self._history[0].composite_score
        for pt in self._history[1:]:
            ema = (self.ema_alpha * pt.composite_score) + ((1.0 - self.ema_alpha) * ema)
        return round(ema, 2)

    def calculate_trend_slope(self, window: int = 10) -> float:
        """
        Positive slope indicates improving health; negative indicates degradation.
        """
        pts = self._history[-window:]
        if len(pts) < 2:
            return 0.0
        delta = pts[-1].composite_score - pts[0].composite_score
        return round(delta / len(pts), 4)

    def detect_drift(self, threshold: float = 5.0) -> bool:
        if len(self._history) < 5:
            return False
        recent_avg = sum(p.composite_score for p in self._history[-5:]) / 5.0
        baseline = self._history[0].composite_score
        return (baseline - recent_avg) > threshold
