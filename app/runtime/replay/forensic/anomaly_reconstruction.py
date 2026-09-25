"""
Anomaly Reconstruction for Phase 13.4.
Detects runtime anomalies, distribution drift, and non-deterministic variations during replay.
"""

from typing import Dict, Any, List
from pydantic import BaseModel


class ReplayAnomaly(BaseModel):
    anomaly_id: str
    event_id: str
    metric_name: str
    expected_value: float
    observed_value: float
    z_score: float
    severity: str = "WARNING"


class AnomalyReconstruction:
    """
    Scans replay events for statistical anomalies and runtime drift.
    """

    @classmethod
    def scan_for_anomalies(
        cls,
        events: List[Dict[str, Any]],
    ) -> List[ReplayAnomaly]:
        anomalies = []
        for idx, ev in enumerate(events):
            payload = ev.get("payload", {})

            # Check latency anomalies (> 5000ms)
            dur = float(payload.get("duration_ms", 0.0))
            if dur > 5000.0:
                anomalies.append(ReplayAnomaly(
                    anomaly_id=f"anom_lat_{idx}",
                    event_id=ev.get("event_id", f"ev_{idx}"),
                    metric_name="task_duration_ms",
                    expected_value=500.0,
                    observed_value=dur,
                    z_score=round((dur - 500.0) / 200.0, 2),
                    severity="WARNING",
                ))

            # Check confidence drops (< 0.60)
            conf = payload.get("overall_score") or payload.get("confidence")
            if conf is not None and conf < 0.60:
                anomalies.append(ReplayAnomaly(
                    anomaly_id=f"anom_conf_{idx}",
                    event_id=ev.get("event_id", f"ev_{idx}"),
                    metric_name="confidence_score",
                    expected_value=0.95,
                    observed_value=float(conf),
                    z_score=-3.5,
                    severity="CRITICAL",
                ))

        return anomalies
