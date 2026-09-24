"""Automated Post-Deployment Recovery and Telemetry Sentry."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional


@dataclass
class TelemetryObservation:
    """Snapshot of service operational health after deployment."""
    deployment_id: str
    error_rate: float
    p99_latency_ms: float
    cpu_utilization_pct: float
    memory_utilization_pct: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class RecoveryDecision:
    """Automated assessment indicating whether deployment should be rolled back."""
    deployment_id: str
    should_rollback: bool
    trigger_reason: Optional[str]
    observation: TelemetryObservation
    evaluated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class AutomatedRecoveryEngine:
    """Monitors live telemetry during soak period and triggers automatic recovery on SLO breach."""

    def __init__(
        self,
        max_error_rate: float = 0.02,  # 2% error rate threshold
        max_p99_latency_ms: float = 300.0,
        max_cpu_pct: float = 85.0,
        max_memory_pct: float = 90.0,
    ):
        self.max_error_rate = max_error_rate
        self.max_p99_latency_ms = max_p99_latency_ms
        self.max_cpu_pct = max_cpu_pct
        self.max_memory_pct = max_memory_pct
        self.decisions: List[RecoveryDecision] = []

    def evaluate_health(
        self,
        deployment_id: str,
        error_rate: float,
        p99_latency_ms: float,
        cpu_pct: float = 50.0,
        memory_pct: float = 60.0,
    ) -> RecoveryDecision:
        """Evaluates health against hard safety thresholds."""
        obs = TelemetryObservation(
            deployment_id=deployment_id,
            error_rate=error_rate,
            p99_latency_ms=p99_latency_ms,
            cpu_utilization_pct=cpu_pct,
            memory_utilization_pct=memory_pct,
        )

        reasons = []
        if error_rate > self.max_error_rate:
            reasons.append(f"Error rate {error_rate*100:.2f}% breached max {self.max_error_rate*100:.2f}%")
        if p99_latency_ms > self.max_p99_latency_ms:
            reasons.append(f"P99 latency {p99_latency_ms:.1f}ms breached max {self.max_p99_latency_ms:.1f}ms")
        if cpu_pct > self.max_cpu_pct:
            reasons.append(f"CPU usage {cpu_pct:.1f}% breached max {self.max_cpu_pct:.1f}%")
        if memory_pct > self.max_memory_pct:
            reasons.append(f"Memory usage {memory_pct:.1f}% breached max {self.max_memory_pct:.1f}%")

        should_rollback = len(reasons) > 0
        trigger_reason = "; ".join(reasons) if should_rollback else None

        decision = RecoveryDecision(
            deployment_id=deployment_id,
            should_rollback=should_rollback,
            trigger_reason=trigger_reason,
            observation=obs,
        )
        self.decisions.append(decision)
        return decision
