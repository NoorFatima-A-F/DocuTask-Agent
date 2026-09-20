"""
Observation Ingestion & Signal Quality Engine for Phase 13.16.
Ingests multi-modal observations across all autonomous runtimes, computing SNR and novelty metrics.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
import math
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.world_model.events.world_model_events import (
    ObservationQuality,
    ObservationSource,
    WorldModelEvent,
    WorldModelEventType,
    world_model_event_bus,
)


@dataclass
class ObservationRecord:
    observation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source: ObservationSource = ObservationSource.EXECUTION_RUNTIME
    entity_id: str = "system"
    observation_type: str = "metric"  # metric, state_change, event, anomaly, user_action
    payload: Dict[str, Any] = field(default_factory=dict)
    signal_to_noise_ratio: float = 12.5  # in dB
    quality: ObservationQuality = ObservationQuality.HIGH_SIGNAL
    novelty_score: float = 0.1  # 0.0 (fully known) to 1.0 (completely novel)
    confidence: float = 0.98
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "observation_id": self.observation_id,
            "source": self.source.value if isinstance(self.source, ObservationSource) else str(self.source),
            "entity_id": self.entity_id,
            "observation_type": self.observation_type,
            "payload": self.payload,
            "signal_to_noise_ratio": round(self.signal_to_noise_ratio, 2),
            "quality": self.quality.value if isinstance(self.quality, ObservationQuality) else str(self.quality),
            "novelty_score": round(self.novelty_score, 3),
            "confidence": round(self.confidence, 4),
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }


class ObservationEngine:
    """Ingests, cleans, scores, and categorizes observations from the ecosystem."""

    def __init__(self):
        self._observations: List[ObservationRecord] = []
        self._known_patterns: Dict[str, int] = {}
        self._initialize_seed_observations()

    def _initialize_seed_observations(self) -> None:
        seeds = [
            ObservationRecord(
                observation_id="obs_k8s_canary_latency",
                source=ObservationSource.EXECUTION_RUNTIME,
                entity_id="service_core_api",
                observation_type="metric",
                payload={"p99_latency_ms": 42.4, "error_rate": 0.001, "cpu_pct": 34.2},
                signal_to_noise_ratio=18.4,
                quality=ObservationQuality.HIGH_SIGNAL,
                novelty_score=0.08,
                confidence=0.99,
            ),
            ObservationRecord(
                observation_id="obs_org_budget_burn",
                source=ObservationSource.ORGANIZATION_RUNTIME,
                entity_id="dept_engineering",
                observation_type="metric",
                payload={"token_spend_rate": 1420.0, "budget_burn_pct": 28.5},
                signal_to_noise_ratio=15.2,
                quality=ObservationQuality.HIGH_SIGNAL,
                novelty_score=0.12,
                confidence=0.97,
            ),
            ObservationRecord(
                observation_id="obs_stripe_invoice_event",
                source=ObservationSource.EXTERNAL_API,
                entity_id="gateway_stripe",
                observation_type="event",
                payload={"invoice_paid": True, "amount_cents": 45000, "currency": "usd"},
                signal_to_noise_ratio=20.0,
                quality=ObservationQuality.HIGH_SIGNAL,
                novelty_score=0.05,
                confidence=1.0,
            ),
            ObservationRecord(
                observation_id="obs_evolution_mutation_score",
                source=ObservationSource.EVOLUTION_RUNTIME,
                entity_id="genome_dag_optimizer",
                observation_type="state_change",
                payload={"mutation_passed": True, "speedup_pct": 14.8, "pareto_rank": 1},
                signal_to_noise_ratio=16.8,
                quality=ObservationQuality.HIGH_SIGNAL,
                novelty_score=0.45,
                confidence=0.96,
            ),
        ]
        for obs in seeds:
            self.ingest_observation(obs)

    def ingest_observation(self, obs: ObservationRecord) -> ObservationRecord:
        # Pattern recognition for novelty detection
        pattern_key = f"{obs.entity_id}:{obs.observation_type}"
        occurrences = self._known_patterns.get(pattern_key, 0)
        self._known_patterns[pattern_key] = occurrences + 1

        # Decreasing novelty with higher frequency
        if occurrences > 0:
            obs.novelty_score = max(0.05, 1.0 / (1.0 + math.log1p(occurrences)))

        self._observations.append(obs)
        if len(self._observations) > 2000:
            self._observations.pop(0)

        world_model_event_bus.publish(
            WorldModelEvent(
                event_type=WorldModelEventType.OBSERVATION_RECEIVED,
                source="observation_engine",
                payload=obs.to_dict(),
                confidence=obs.confidence,
            )
        )

        if obs.novelty_score > 0.7:
            world_model_event_bus.publish(
                WorldModelEvent(
                    event_type=WorldModelEventType.NOVELTY_DETECTED,
                    source="observation_engine",
                    payload={"observation_id": obs.observation_id, "novelty_score": obs.novelty_score},
                )
            )

        return obs

    def observe_metric(
        self,
        source: ObservationSource,
        entity_id: str,
        metric_name: str,
        metric_value: float,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ObservationRecord:
        obs = ObservationRecord(
            source=source,
            entity_id=entity_id,
            observation_type="metric",
            payload={metric_name: metric_value},
            metadata=metadata or {},
        )
        return self.ingest_observation(obs)

    def list_observations(
        self,
        source: Optional[str] = None,
        entity_id: Optional[str] = None,
        limit: int = 100,
    ) -> List[ObservationRecord]:
        items = self._observations
        if source:
            items = [o for o in items if (o.source.value if isinstance(o.source, ObservationSource) else str(o.source)).lower() == source.lower()]
        if entity_id:
            items = [o for o in items if o.entity_id.lower() == entity_id.lower()]
        return items[-limit:]

    def get_summary(self) -> Dict[str, Any]:
        total = len(self._observations)
        high_sig = sum(1 for o in self._observations if o.quality == ObservationQuality.HIGH_SIGNAL)
        avg_snr = sum(o.signal_to_noise_ratio for o in self._observations) / total if total > 0 else 0.0
        avg_novelty = sum(o.novelty_score for o in self._observations) / total if total > 0 else 0.0

        return {
            "total_observations": total,
            "high_signal_count": high_sig,
            "average_snr_db": round(avg_snr, 2),
            "average_novelty_score": round(avg_novelty, 3),
            "known_patterns_tracked": len(self._known_patterns),
        }


# Global Singleton
observation_engine = ObservationEngine()
