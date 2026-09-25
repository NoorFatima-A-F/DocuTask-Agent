"""Shadow Traffic Mirroring Strategy (Req 39)."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List


@dataclass
class ShadowTrace:
    request_id: str
    primary_status: int
    shadow_status: int
    primary_latency_ms: float
    shadow_latency_ms: float
    payload_parity: bool
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class ShadowStrategy:
    """Mirrors production requests asynchronously to validate agent/model changes without customer impact."""

    def __init__(self, sampling_rate: float = 1.0):
        self.sampling_rate = max(0.0, min(1.0, sampling_rate))
        self.traces: List[ShadowTrace] = []

    def record_trace(
        self,
        request_id: str,
        primary_status: int,
        shadow_status: int,
        primary_lat: float,
        shadow_lat: float,
        parity: bool,
    ) -> ShadowTrace:
        trace = ShadowTrace(
            request_id=request_id,
            primary_status=primary_status,
            shadow_status=shadow_status,
            primary_latency_ms=primary_lat,
            shadow_latency_ms=shadow_lat,
            payload_parity=parity,
        )
        self.traces.append(trace)
        return trace

    def compute_parity_score(self) -> float:
        if not self.traces:
            return 1.0
        matching = sum(1 for t in self.traces if t.primary_status == t.shadow_status and t.payload_parity)
        return matching / len(self.traces)
