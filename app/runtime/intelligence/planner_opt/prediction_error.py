"""
Prediction Error Model and Tracking for Phase 10 (AISLCOP).

Measures delta between predicted mission performance and actual runtime telemetry.
Tracks loss functions and convergence over iterations.
"""

from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List


@dataclass
class PredictionErrorRecord:
    mission_id: str
    timestamp: float = field(default_factory=time.time)
    
    # Latency Error
    predicted_latency_ms: float = 1200.0
    actual_latency_ms: float = 1250.0
    latency_error_ms: float = 50.0
    latency_rel_error: float = 0.0417
    
    # Cost Error
    predicted_cost_usd: float = 0.010
    actual_cost_usd: float = 0.012
    cost_error_usd: float = 0.002
    cost_rel_error: float = 0.20
    
    # Confidence Error
    predicted_confidence: float = 0.95
    actual_confidence: float = 0.96
    confidence_error: float = 0.01
    
    # Retries / Depth Error
    predicted_retries: int = 0
    actual_retries: int = 0
    retry_error: int = 0
    
    predicted_dag_depth: int = 3
    actual_dag_depth: int = 3
    depth_error: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class PredictionErrorAnalyzer:
    """
    Accumulates prediction errors and evaluates model loss convergence.
    """

    def __init__(self):
        self._records: List[PredictionErrorRecord] = []

    def record_error(
        self,
        mission_id: str,
        predicted: Dict[str, float],
        actual: Dict[str, float],
    ) -> PredictionErrorRecord:
        pred_lat = predicted.get("latency_ms", 1200.0)
        act_lat = actual.get("latency_ms", 1250.0)
        lat_err = abs(act_lat - pred_lat)
        lat_rel = lat_err / max(act_lat, 1.0)

        pred_cost = predicted.get("cost_usd", 0.010)
        act_cost = actual.get("cost_usd", 0.012)
        cost_err = abs(act_cost - pred_cost)
        cost_rel = cost_err / max(act_cost, 0.0001)

        pred_conf = predicted.get("confidence", 0.95)
        act_conf = actual.get("confidence", 0.96)
        conf_err = abs(act_conf - pred_conf)

        pred_retries = int(predicted.get("retries", 0))
        act_retries = int(actual.get("retries", 0))
        ret_err = abs(act_retries - pred_retries)

        pred_depth = int(predicted.get("dag_depth", 3))
        act_depth = int(actual.get("dag_depth", 3))
        depth_err = abs(act_depth - pred_depth)

        rec = PredictionErrorRecord(
            mission_id=mission_id,
            timestamp=time.time(),
            predicted_latency_ms=pred_lat,
            actual_latency_ms=act_lat,
            latency_error_ms=round(lat_err, 2),
            latency_rel_error=round(lat_rel, 4),
            predicted_cost_usd=pred_cost,
            actual_cost_usd=act_cost,
            cost_error_usd=round(cost_err, 6),
            cost_rel_error=round(cost_rel, 4),
            predicted_confidence=pred_conf,
            actual_confidence=act_conf,
            confidence_error=round(conf_err, 4),
            predicted_retries=pred_retries,
            actual_retries=act_retries,
            retry_error=ret_err,
            predicted_dag_depth=pred_depth,
            actual_dag_depth=act_depth,
            depth_error=depth_err,
        )

        self._records.append(rec)
        return rec

    def compute_summary(self) -> Dict[str, Any]:
        if not self._records:
            return {
                "count": 0,
                "mean_latency_mae_ms": 0.0,
                "mean_latency_mape": 0.0,
                "mean_cost_mae_usd": 0.0,
                "mean_confidence_mae": 0.0,
                "convergence_score": 1.0,
            }

        n = len(self._records)
        mae_lat = sum(r.latency_error_ms for r in self._records) / n
        mape_lat = sum(r.latency_rel_error for r in self._records) / n
        mae_cost = sum(r.cost_error_usd for r in self._records) / n
        mae_conf = sum(r.confidence_error for r in self._records) / n

        # Convergence score: ratio of recent 20% errors vs initial 20% errors
        convergence = 0.95
        if n >= 10:
            window = max(2, n // 5)
            initial_lat_err = sum(r.latency_error_ms for r in self._records[:window]) / window
            recent_lat_err = sum(r.latency_error_ms for r in self._records[-window:]) / window
            if initial_lat_err > 0:
                convergence = round(max(0.1, 1.0 - (recent_lat_err / initial_lat_err) * 0.5), 4)

        return {
            "count": n,
            "mean_latency_mae_ms": round(mae_lat, 2),
            "mean_latency_mape": round(mape_lat, 4),
            "mean_cost_mae_usd": round(mae_cost, 6),
            "mean_confidence_mae": round(mae_conf, 4),
            "convergence_score": convergence,
        }

    def get_recent(self, limit: int = 50) -> List[PredictionErrorRecord]:
        return list(reversed(self._records[-limit:]))
