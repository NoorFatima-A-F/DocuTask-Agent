"""
Performance Tracker for Dynamic Agent Reputation System.
Maintains live metrics per agent, monitors performance drift, and flags degraded agents.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.agents.collaboration.reputation.agent_metrics import (
    AgentExecutionMetrics,
    RollingPerformanceWindow,
    SingleExecutionOutcome,
)

logger = logging.getLogger(__name__)


class PerformanceTracker:
    """Tracks per-agent historical metrics and detects performance drift."""

    def __init__(self, rolling_window_size: int = 50, drift_threshold: float = 0.15) -> None:
        self.rolling_window_size = rolling_window_size
        self.drift_threshold = drift_threshold
        self._metrics: Dict[str, AgentExecutionMetrics] = {}
        self._windows: Dict[str, RollingPerformanceWindow] = {}

    def get_metrics(self, agent_id: str) -> AgentExecutionMetrics:
        """Retrieves or creates execution metrics for an agent."""
        if agent_id not in self._metrics:
            self._metrics[agent_id] = AgentExecutionMetrics(agent_id=agent_id)
            self._windows[agent_id] = RollingPerformanceWindow(capacity=self.rolling_window_size)
        return self._metrics[agent_id]

    def record_outcome(
        self,
        agent_id: str,
        task_id: str,
        success: bool,
        latency_ms: float,
        accuracy_score: float = 1.0,
        reflection_penalty: float = 0.0,
        human_override: bool = False,
    ) -> SingleExecutionOutcome:
        """Records a completed task execution outcome for an agent."""
        metrics = self.get_metrics(agent_id)
        window = self._windows[agent_id]

        outcome = SingleExecutionOutcome(
            task_id=task_id,
            success=success,
            latency_ms=latency_ms,
            accuracy_score=accuracy_score,
            reflection_penalty=reflection_penalty,
            human_override=human_override,
        )

        # Update cumulative metrics
        metrics.total_invocations += 1
        if success:
            metrics.successful_invocations += 1
        else:
            metrics.failed_invocations += 1

        metrics.total_latency_ms += latency_ms
        if reflection_penalty > 0.0:
            metrics.total_reflection_penalties += 1
        if human_override:
            metrics.total_human_overrides += 1

        # Incremental moving average for accuracy
        prev_acc_sum = metrics.average_accuracy * (metrics.total_invocations - 1)
        metrics.average_accuracy = (prev_acc_sum + accuracy_score) / metrics.total_invocations
        metrics.last_updated = datetime.now(timezone.utc)

        # Update rolling window
        window.record(outcome)

        # Check for performance drift
        drift = self.check_drift(agent_id)
        if drift.get("has_drift"):
            logger.warning("Performance drift detected for agent %s: %s", agent_id, drift.get("reason"))

        return outcome

    def check_drift(self, agent_id: str) -> Dict[str, Any]:
        """Detects whether recent performance significantly lags behind historical baseline."""
        metrics = self.get_metrics(agent_id)
        window = self._windows.get(agent_id)

        if not window or len(window) < 10:
            return {"has_drift": False, "reason": "Insufficient samples"}

        rolling_success = window.rolling_success_rate
        historical_success = metrics.success_rate

        # Significant drop in success rate
        if (historical_success - rolling_success) > self.drift_threshold:
            return {
                "has_drift": True,
                "reason": f"Success rate dropped from {historical_success:.2f} to {rolling_success:.2f}",
                "drop": historical_success - rolling_success,
            }

        # Check for frequent reflection penalties in recent window
        recent_penalties = sum(1 for o in window.outcomes if o.reflection_penalty > 0.0)
        if recent_penalties / len(window) > 0.30:
            return {
                "has_drift": True,
                "reason": f"High recent reflection penalty rate ({recent_penalties}/{len(window)})",
            }

        return {"has_drift": False, "reason": "Nominal"}
