"""
Agent Execution Metrics and Performance Window Data Models.
Tracks granular telemetry on agent task outcomes, latency distributions, and quality drift.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Deque, Dict, List, Optional
from uuid import UUID, uuid4


@dataclass
class SingleExecutionOutcome:
    """Outcome telemetry of a single task execution by an agent."""

    task_id: str
    success: bool
    latency_ms: float
    accuracy_score: float = 1.0
    reflection_penalty: float = 0.0
    human_override: bool = False
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class AgentExecutionMetrics:
    """Cumulative operational metrics for a specific agent."""

    agent_id: str
    total_invocations: int = 0
    successful_invocations: int = 0
    failed_invocations: int = 0
    total_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    total_reflection_penalties: int = 0
    total_human_overrides: int = 0
    average_accuracy: float = 1.0
    last_updated: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def success_rate(self) -> float:
        if self.total_invocations == 0:
            return 1.0
        return self.successful_invocations / self.total_invocations

    @property
    def average_latency_ms(self) -> float:
        if self.total_invocations == 0:
            return 0.0
        return self.total_latency_ms / self.total_invocations


class RollingPerformanceWindow:
    """Fixed-capacity rolling deque capturing recent executions for drift analysis."""

    def __init__(self, capacity: int = 50) -> None:
        self.capacity = capacity
        self.outcomes: Deque[SingleExecutionOutcome] = deque(maxlen=capacity)

    def record(self, outcome: SingleExecutionOutcome) -> None:
        self.outcomes.append(outcome)

    @property
    def rolling_success_rate(self) -> float:
        if not self.outcomes:
            return 1.0
        successes = sum(1 for o in self.outcomes if o.success)
        return successes / len(self.outcomes)

    @property
    def rolling_average_latency_ms(self) -> float:
        if not self.outcomes:
            return 0.0
        return sum(o.latency_ms for o in self.outcomes) / len(self.outcomes)

    @property
    def rolling_average_accuracy(self) -> float:
        if not self.outcomes:
            return 1.0
        return sum(o.accuracy_score for o in self.outcomes) / len(self.outcomes)

    def __len__(self) -> int:
        return len(self.outcomes)
