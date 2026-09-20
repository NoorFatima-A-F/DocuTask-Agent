"""
Uncertainty Quantification & Entropy Engine for Phase 13.16.
Decomposes epistemic and aleatoric uncertainty, computing entropy and belief stability metrics.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import math
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.world_model.events.world_model_events import (
    WorldModelEvent,
    WorldModelEventType,
    world_model_event_bus,
)


@dataclass
class UncertaintyProfile:
    profile_id: str = field(default_factory=lambda: f"unc_{uuid.uuid4().hex[:8]}")
    target_domain: str = "infrastructure_capacity"
    epistemic_uncertainty: float = 0.08  # Model reducible uncertainty
    aleatoric_uncertainty: float = 0.04  # Inherent stochastic noise
    total_entropy: float = 0.28  # Shannon entropy
    belief_stability_index: float = 0.94  # 0.0 to 1.0
    novelty_coefficient: float = 0.12
    missing_evidence_score: float = 0.05
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "profile_id": self.profile_id,
            "target_domain": self.target_domain,
            "epistemic_uncertainty": round(self.epistemic_uncertainty, 4),
            "aleatoric_uncertainty": round(self.aleatoric_uncertainty, 4),
            "total_entropy": round(self.total_entropy, 4),
            "belief_stability_index": round(self.belief_stability_index, 3),
            "novelty_coefficient": round(self.novelty_coefficient, 3),
            "missing_evidence_score": round(self.missing_evidence_score, 3),
            "timestamp": self.timestamp,
        }


class UncertaintyEngine:
    """Measures epistemic and aleatoric uncertainty across knowledge and prediction domains."""

    def __init__(self):
        self._profiles: Dict[str, UncertaintyProfile] = {}
        self._initialize_seed_profiles()

    def _initialize_seed_profiles(self) -> None:
        seeds = [
            UncertaintyProfile(
                profile_id="unc_latency_profile",
                target_domain="service_p99_latency",
                epistemic_uncertainty=0.06,
                aleatoric_uncertainty=0.03,
                total_entropy=0.22,
                belief_stability_index=0.96,
                novelty_coefficient=0.08,
            ),
            UncertaintyProfile(
                profile_id="unc_budget_forecast_profile",
                target_domain="cloud_spend_forecasting",
                epistemic_uncertainty=0.10,
                aleatoric_uncertainty=0.05,
                total_entropy=0.34,
                belief_stability_index=0.91,
                novelty_coefficient=0.15,
            ),
        ]
        for p in seeds:
            self._profiles[p.profile_id] = p

    def compute_uncertainty(self, domain: str, observation_count: int, variance: float) -> UncertaintyProfile:
        uid = f"unc_{uuid.uuid4().hex[:8]}"
        # Epistemic decays with observation count: 1 / sqrt(N)
        epistemic = max(0.01, 1.0 / math.sqrt(max(1, observation_count)))
        aleatoric = min(0.5, variance * 0.1)
        entropy = -0.5 * (math.log2(max(0.001, epistemic * aleatoric)))

        profile = UncertaintyProfile(
            profile_id=uid,
            target_domain=domain,
            epistemic_uncertainty=epistemic,
            aleatoric_uncertainty=aleatoric,
            total_entropy=entropy,
            belief_stability_index=max(0.1, 1.0 - epistemic),
            novelty_coefficient=epistemic * 1.2,
        )
        self._profiles[uid] = profile

        world_model_event_bus.publish(
            WorldModelEvent(
                event_type=WorldModelEventType.UNCERTAINTY_DECOMPOSED,
                source="uncertainty_engine",
                payload=profile.to_dict(),
            )
        )
        return profile

    def list_profiles(self) -> List[UncertaintyProfile]:
        return list(self._profiles.values())

    def get_summary(self) -> Dict[str, Any]:
        return {
            "total_profiles": len(self._profiles),
            "profiles": [p.to_dict() for p in self._profiles.values()],
        }


# Global Singleton
uncertainty_engine = UncertaintyEngine()
