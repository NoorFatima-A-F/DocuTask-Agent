"""
Throughput Measurement & Little's Law Validation Framework.
Calculates rigorous operational throughput (operations/sec), saturation curves,
and verifies queue behavior against Little's Law: L = lambda * W.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)


@dataclass
class LittlesLawVerification:
    """Mathematical verification of Little's Law (L = lambda * W)."""

    observed_concurrency_L: float
    observed_arrival_rate_lambda: float
    observed_mean_latency_W_sec: float
    predicted_concurrency: float
    error_percentage: float
    law_holds: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "observed_concurrency_L": round(self.observed_concurrency_L, 2),
            "observed_arrival_rate_lambda": round(self.observed_arrival_rate_lambda, 2),
            "observed_mean_latency_W_sec": round(self.observed_mean_latency_W_sec, 5),
            "predicted_concurrency": round(self.predicted_concurrency, 2),
            "error_percentage": round(self.error_percentage, 2),
            "law_holds": self.law_holds,
        }


@dataclass
class ThroughputCurvePoint:
    """Individual point on a throughput vs latency saturation curve."""

    concurrency: int
    throughput_ops_sec: float
    mean_latency_ms: float
    p95_latency_ms: float
    saturation_index: float  # 0.0 (unsaturated) to 1.0 (fully saturated)


class ThroughputEngine:
    """Calculates formal throughput metrics and Little's Law validation."""

    @classmethod
    def calculate_throughput(cls, completed_ops: int, elapsed_seconds: float) -> float:
        """Throughput = completed_operations / elapsed_seconds."""
        if elapsed_seconds <= 0:
            return 0.0
        return completed_ops / elapsed_seconds

    @classmethod
    def verify_littles_law(
        cls,
        concurrency: int,
        throughput_ops_sec: float,
        mean_latency_ms: float,
        tolerance_pct: float = 15.0,
    ) -> LittlesLawVerification:
        """
        Validates Little's Law: L = lambda * W
        L = Average number of items in system (Concurrency)
        lambda = Arrival / Throughput rate (ops/sec)
        W = Average time in system (Mean Latency in seconds)
        """
        w_sec = mean_latency_ms / 1000.0
        predicted_l = throughput_ops_sec * w_sec
        error_pct = (abs(concurrency - predicted_l) / max(1.0, concurrency)) * 100.0
        law_holds = error_pct <= tolerance_pct

        return LittlesLawVerification(
            observed_concurrency_L=float(concurrency),
            observed_arrival_rate_lambda=throughput_ops_sec,
            observed_mean_latency_W_sec=w_sec,
            predicted_concurrency=predicted_l,
            error_percentage=error_pct,
            law_holds=law_holds,
        )

    @classmethod
    def build_saturation_curve(cls, points: List[Tuple[int, float, float, float]]) -> List[ThroughputCurvePoint]:
        """
        Constructs a saturation curve from (concurrency, throughput, mean_lat, p95_lat) tuples.
        Calculates saturation index = 1.0 - (current_throughput / (concurrency * base_single_worker_throughput)).
        """
        if not points:
            return []

        base_throughput = points[0][1] if points[0][1] > 0 else 1.0
        curve: List[ThroughputCurvePoint] = []

        for conc, thru, mean_l, p95_l in points:
            ideal_thru = conc * base_throughput
            sat_index = max(0.0, min(1.0, 1.0 - (thru / max(thru, ideal_thru))))
            curve.append(
                ThroughputCurvePoint(
                    concurrency=conc,
                    throughput_ops_sec=thru,
                    mean_latency_ms=mean_l,
                    p95_latency_ms=p95_l,
                    saturation_index=round(sat_index, 3),
                )
            )
        return curve
