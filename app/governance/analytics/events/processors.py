"""Governance Analytics Event Processing, Validation, and Enrichment Pipeline."""

from typing import Dict, Any, List, Optional, Callable
from .normalizers import GovernanceAnalyticsEvent, AnalyticsEventType


class EventProcessor:
    """Processes, enriches, and validates normalized analytics events."""

    def __init__(self):
        self._enrichers: List[Callable[[GovernanceAnalyticsEvent], GovernanceAnalyticsEvent]] = []

    def register_enricher(self, fn: Callable[[GovernanceAnalyticsEvent], GovernanceAnalyticsEvent]) -> None:
        self._enrichers.append(fn)

    def process(self, event: GovernanceAnalyticsEvent) -> GovernanceAnalyticsEvent:
        # 1. Basic validation and sanity normalization
        if event.risk_score < 0.0:
            event.risk_score = 0.0
        elif event.risk_score > 1.0 and event.risk_score <= 100.0:
            # Normalize 0-100 scale to 0.0-1.0
            event.risk_score = event.risk_score / 100.0

        # Auto-infer risk level if default
        if event.risk_level == "LOW" and event.risk_score >= 0.8:
            event.risk_level = "CRITICAL"
        elif event.risk_level == "LOW" and event.risk_score >= 0.6:
            event.risk_level = "HIGH"
        elif event.risk_level == "LOW" and event.risk_score >= 0.3:
            event.risk_level = "MEDIUM"

        # 2. Run custom enrichment pipeline
        for enricher in self._enrichers:
            event = enricher(event)

        return event

    def process_batch(self, events: List[GovernanceAnalyticsEvent]) -> List[GovernanceAnalyticsEvent]:
        return [self.process(e) for e in events]
