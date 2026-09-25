"""Shadow Traffic Mirroring Strategy."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class ShadowComparison:
    """Telemetry comparing primary production response with shadowed release response."""
    request_id: str
    primary_status_code: int
    shadow_status_code: int
    primary_latency_ms: float
    shadow_latency_ms: float
    payload_match: bool
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = field(default_factory=dict)


class ShadowStrategy:
    """Mirrors live production requests to shadow environment for dark launching and behavioral validation."""

    def __init__(self, sampling_rate: float = 1.0):
        self.sampling_rate = max(0.0, min(1.0, sampling_rate))
        self.comparisons: List[ShadowComparison] = []

    def record_comparison(
        self,
        primary_status: int,
        shadow_status: int,
        primary_latency: float,
        shadow_latency: float,
        payload_match: bool,
        request_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ShadowComparison:
        """Records a single live vs shadow request comparison."""
        req_id = request_id or f"req-{uuid.uuid4().hex[:8]}"
        comp = ShadowComparison(
            request_id=req_id,
            primary_status_code=primary_status,
            shadow_status_code=shadow_status,
            primary_latency_ms=primary_latency,
            shadow_latency_ms=shadow_latency,
            payload_match=payload_match,
            metadata=metadata or {},
        )
        self.comparisons.append(comp)
        return comp

    def calculate_parity_score(self) -> float:
        """Calculates response parity percentage (status match + payload match)."""
        if not self.comparisons:
            return 1.0
        matching = sum(
            1 for c in self.comparisons
            if c.primary_status_code == c.shadow_status_code and c.payload_match
        )
        return matching / len(self.comparisons)

    def get_latency_metrics(self) -> Dict[str, float]:
        """Calculates average latency comparison."""
        if not self.comparisons:
            return {"primary_avg_ms": 0.0, "shadow_avg_ms": 0.0, "delta_pct": 0.0}

        avg_primary = sum(c.primary_latency_ms for c in self.comparisons) / len(self.comparisons)
        avg_shadow = sum(c.shadow_latency_ms for c in self.comparisons) / len(self.comparisons)
        delta_pct = ((avg_shadow - avg_primary) / max(0.001, avg_primary)) * 100.0

        return {
            "primary_avg_ms": round(avg_primary, 2),
            "shadow_avg_ms": round(avg_shadow, 2),
            "delta_pct": round(delta_pct, 2),
        }

    def is_ready_for_promotion(
        self,
        min_parity: float = 0.99,
        max_latency_delta_pct: float = 25.0,
    ) -> bool:
        """Determines if shadow deployment meets quality bar for promotion."""
        if len(self.comparisons) < 5:
            return False

        parity = self.calculate_parity_score()
        lat_metrics = self.get_latency_metrics()

        return (parity >= min_parity) and (lat_metrics["delta_pct"] <= max_latency_delta_pct)
