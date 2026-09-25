"""Event Intelligence, Pattern Detection, and Operational Correlation."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import List, Optional

from ..core.events import EventCategory, EventStream


@dataclass
class OperationalInsight:
    insight_id: str
    title: str
    description: str
    severity: str
    detected_at: float = field(default_factory=time.time)
    related_events: List[str] = field(default_factory=list)
    confidence: float = 0.9
    suggested_action: str = ""


class EventAnalyzer:
    """Analyzes streams of platform events to detect known failure patterns and correlate incidents."""

    def __init__(self, event_stream: Optional[EventStream] = None):
        self.event_stream = event_stream or EventStream()
        self._insights: List[OperationalInsight] = []

    def analyze_recent_events(self, window_seconds: float = 300.0) -> List[OperationalInsight]:
        """Analyze events within the sliding window for complex correlation signatures."""
        now = time.time()
        events = self.event_stream.get_history(limit=500)
        recent_events = [e for e in events if (now - e.timestamp) <= window_seconds]

        insights: List[OperationalInsight] = []

        # 1. Pattern: Worker Saturation (Worker Failure + High Queue Depth + CPU Spike)
        worker_failures = [e for e in recent_events if "worker.fail" in e.name or "worker.crash" in e.name]
        queue_spikes = [e for e in recent_events if "queue.backlog" in e.name or "queue.high" in e.name]
        cpu_spikes = [e for e in recent_events if "cpu.high" in e.name]

        if worker_failures and (queue_spikes or cpu_spikes):
            insight = OperationalInsight(
                insight_id=f"insight-worker-sat-{int(now)}",
                title="Worker Node Saturation & Queue Congestion",
                description="Correlated worker process crashes accompanied by rising queue depth and CPU pressure.",
                severity="CRITICAL",
                related_events=[e.event_id for e in worker_failures + queue_spikes + cpu_spikes],
                confidence=0.95,
                suggested_action="Auto-scale worker pool and restart degraded runtime nodes.",
            )
            insights.append(insight)

        # 2. Pattern: AI Model Degraded / Rate Limited
        model_errors = [e for e in recent_events if "ai.model.rate_limit" in e.name or "ai.model.timeout" in e.name]
        if len(model_errors) >= 3:
            insight = OperationalInsight(
                insight_id=f"insight-ai-degraded-{int(now)}",
                title="Upstream AI Model Provider Degraded",
                description="Repeated rate limiting or timeouts observed from upstream LLM provider.",
                severity="WARNING",
                related_events=[e.event_id for e in model_errors],
                confidence=0.88,
                suggested_action="Engage local model fallback and activate token rate-limit governor.",
            )
            insights.append(insight)

        # 3. Pattern: Security Authentication Storm
        auth_failures = [e for e in recent_events if e.category == EventCategory.SECURITY and "auth.failed" in e.name]
        if len(auth_failures) >= 5:
            insight = OperationalInsight(
                insight_id=f"insight-sec-auth-{int(now)}",
                title="Potential Credential Stuffing or Auth Storm",
                description="High volume of authentication failures detected from isolated IP ranges.",
                severity="ERROR",
                related_events=[e.event_id for e in auth_failures],
                confidence=0.92,
                suggested_action="Apply temporary IP rate limiting and trigger security alert.",
            )
            insights.append(insight)

        self._insights.extend(insights)
        return insights

    def get_insights(self) -> List[OperationalInsight]:
        return list(self._insights)
