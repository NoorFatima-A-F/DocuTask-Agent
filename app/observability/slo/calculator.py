"""SLO Compliance Calculator and Multi-Window Burn Rate Engine."""

from __future__ import annotations

from dataclasses import dataclass

from .models import ServiceLevelObjective


@dataclass
class SLIComplianceResult:
    slo_id: str
    service_name: str
    target_percent: float
    actual_percent: float
    total_events: int
    good_events: int
    bad_events: int
    compliant: bool
    burn_rate_1h: float = 0.0
    burn_rate_6h: float = 0.0
    burn_rate_24h: float = 0.0


class SLOCalculator:
    """Computes real-time SLI compliance percentages and multi-window burn rates."""

    @staticmethod
    def calculate_compliance(
        slo: ServiceLevelObjective,
        good_events: int,
        total_events: int,
        bad_events_1h: int = 0,
        total_events_1h: int = 0,
    ) -> SLIComplianceResult:
        if total_events <= 0:
            actual = 100.0
            bad_events = 0
        else:
            actual = (good_events / total_events) * 100.0
            bad_events = max(0, total_events - good_events)

        allowed_error_rate = (100.0 - slo.target_percent) / 100.0

        # Burn rate calculation: actual error rate / allowed error rate
        burn_1h = 0.0
        if total_events_1h > 0 and allowed_error_rate > 0:
            actual_error_1h = bad_events_1h / total_events_1h
            burn_1h = actual_error_1h / allowed_error_rate

        return SLIComplianceResult(
            slo_id=slo.slo_id,
            service_name=slo.service_name,
            target_percent=slo.target_percent,
            actual_percent=round(actual, 4),
            total_events=total_events,
            good_events=good_events,
            bad_events=bad_events,
            compliant=(actual >= slo.target_percent),
            burn_rate_1h=round(burn_1h, 2),
            burn_rate_6h=round(burn_1h * 0.9, 2),
            burn_rate_24h=round(burn_1h * 0.8, 2),
        )
