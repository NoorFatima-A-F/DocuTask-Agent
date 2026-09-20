"""
Temporal Reasoning Engine for Phase 13.16.
Models time series sequences, periodicity patterns, seasonality cycles, and concept drift across world events.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import math
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.world_model.events.world_model_events import (
    TemporalResolution,
    WorldModelEvent,
    WorldModelEventType,
    world_model_event_bus,
)


@dataclass
class TemporalPattern:
    pattern_id: str = field(default_factory=lambda: f"pattern_{uuid.uuid4().hex[:8]}")
    name: str = ""
    target_metric: str = ""
    period_hours: float = 24.0
    seasonality_type: str = "daily_cycle"  # daily_cycle, weekly_batch, monthly_close, burst
    amplitude: float = 1.2
    confidence: float = 0.94
    drift_rate: float = 0.02  # per week
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pattern_id": self.pattern_id,
            "name": self.name,
            "target_metric": self.target_metric,
            "period_hours": self.period_hours,
            "seasonality_type": self.seasonality_type,
            "amplitude": round(self.amplitude, 3),
            "confidence": round(self.confidence, 4),
            "drift_rate": round(self.drift_rate, 4),
            "created_at": self.created_at,
        }


class TemporalEngine:
    """Discovers temporal dynamics, seasonal cycles, and trend progressions."""

    def __init__(self):
        self._patterns: Dict[str, TemporalPattern] = {}
        self._initialize_seed_patterns()

    def _initialize_seed_patterns(self) -> None:
        seeds = [
            TemporalPattern(
                pattern_id="pat_daily_api_traffic_peak",
                name="Daily Enterprise API Workload Wave",
                target_metric="service_core_api.rps",
                period_hours=24.0,
                seasonality_type="daily_cycle",
                amplitude=2.4,
                confidence=0.98,
                drift_rate=0.015,
            ),
            TemporalPattern(
                pattern_id="pat_monthly_billing_surge",
                name="End-of-Month Invoice Settlement Surge",
                target_metric="gateway_stripe.volume_usd",
                period_hours=720.0,  # 30 days
                seasonality_type="monthly_close",
                amplitude=4.5,
                confidence=0.96,
                drift_rate=0.01,
            ),
            TemporalPattern(
                pattern_id="pat_hourly_db_checkpoint_latency",
                name="Hourly Warehouse Vacuum & Checkpoint Spike",
                target_metric="postgres_warehouse.disk_io_pct",
                period_hours=1.0,
                seasonality_type="burst",
                amplitude=1.8,
                confidence=0.99,
                drift_rate=0.005,
            ),
        ]
        for p in seeds:
            self._patterns[p.pattern_id] = p

    def register_pattern(self, pattern: TemporalPattern) -> TemporalPattern:
        self._patterns[pattern.pattern_id] = pattern
        world_model_event_bus.publish(
            WorldModelEvent(
                event_type=WorldModelEventType.TEMPORAL_PATTERN_DISCOVERED,
                source="temporal_engine",
                payload=pattern.to_dict(),
            )
        )
        return pattern

    def list_patterns(self) -> List[TemporalPattern]:
        return list(self._patterns.values())

    def detect_drift(self, target_metric: str, observed_values: List[float]) -> Dict[str, Any]:
        """Detects whether recent observations deviate significantly from expected distribution."""
        if not observed_values:
            return {"has_drift": False, "p_value": 1.0}

        mean = sum(observed_values) / len(observed_values)
        variance = sum((x - mean) ** 2 for x in observed_values) / max(1, len(observed_values) - 1)
        std_dev = math.sqrt(variance) if variance > 0 else 0.01

        # Drift score relative to baseline
        baseline = 40.0
        z_score = abs(mean - baseline) / std_dev
        has_drift = z_score > 2.5

        if has_drift:
            world_model_event_bus.publish(
                WorldModelEvent(
                    event_type=WorldModelEventType.CONCEPT_DRIFT_DETECTED,
                    source="temporal_engine",
                    payload={"target_metric": target_metric, "z_score": z_score, "mean": mean},
                )
            )

        return {
            "target_metric": target_metric,
            "has_drift": has_drift,
            "z_score": round(z_score, 3),
            "sample_mean": round(mean, 2),
            "std_dev": round(std_dev, 2),
        }

    def get_summary(self) -> Dict[str, Any]:
        return {
            "total_patterns": len(self._patterns),
            "patterns": [p.to_dict() for p in self._patterns.values()],
            "mean_confidence": round(sum(p.confidence for p in self._patterns.values()) / max(1, len(self._patterns)), 4),
        }


# Global Singleton
temporal_engine = TemporalEngine()
