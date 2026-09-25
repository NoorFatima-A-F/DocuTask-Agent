"""Prompt Monitoring Analytics Engine (Phase 8D).

Aggregates operational usage, failure distributions, cost attribution, and version performance.
"""

from __future__ import annotations

import statistics
from typing import Any, Dict, List
from pydantic import BaseModel
from app.prompts.monitoring.metrics import PromptExecutionEvent


class PromptUsageSummary(BaseModel):
    """Aggregated usage and cost metrics for a prompt asset."""
    prompt_id: str
    organization_id: str
    total_invocations: int = 0
    successful_invocations: int = 0
    failed_invocations: int = 0
    success_rate_pct: float = 100.0
    total_tokens: int = 0
    total_spend_usd: float = 0.0
    avg_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0


class PromptAnalyticsEngine:
    """Computes aggregated production intelligence across prompt executions."""

    def __init__(self):
        self._events: List[PromptExecutionEvent] = []

    def record_event(self, event: PromptExecutionEvent) -> None:
        """Record runtime invocation telemetry."""
        self._events.append(event)

    def get_prompt_summary(
        self,
        prompt_id: str,
        organization_id: str,
    ) -> PromptUsageSummary:
        """Generate usage and latency summary for a specific prompt."""
        events = [
            e for e in self._events
            if e.organization_id == organization_id and e.prompt_id == prompt_id
        ]
        if not events:
            return PromptUsageSummary(
                prompt_id=prompt_id,
                organization_id=organization_id,
            )

        total = len(events)
        successes = sum(1 for e in events if e.is_success)
        failures = total - successes
        tokens = sum(e.total_tokens for e in events)
        spend = sum(e.cost_usd for e in events)
        latencies = sorted([e.latency_ms for e in events])

        avg_lat = statistics.mean(latencies) if latencies else 0.0
        p95_idx = int(0.95 * (total - 1))
        p95_lat = latencies[p95_idx] if latencies else 0.0

        return PromptUsageSummary(
            prompt_id=prompt_id,
            organization_id=organization_id,
            total_invocations=total,
            successful_invocations=successes,
            failed_invocations=failures,
            success_rate_pct=round((successes / total) * 100.0, 2),
            total_tokens=tokens,
            total_spend_usd=round(spend, 6),
            avg_latency_ms=round(avg_lat, 2),
            p95_latency_ms=round(p95_lat, 2),
        )

    def get_most_used_prompts(
        self,
        organization_id: str,
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        """List top prompts by invocation volume."""
        org_events = [e for e in self._events if e.organization_id == organization_id]
        counts: Dict[str, int] = {}
        for e in org_events:
            counts[e.prompt_id] = counts.get(e.prompt_id, 0) + 1

        sorted_prompts = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:limit]
        return [{"prompt_id": pid, "invocations": cnt} for pid, cnt in sorted_prompts]
