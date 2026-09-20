"""
Health Evaluator & Flap Detector.

Performs multi-level composite health scoring, flap detection,
and state aggregation across components, services, and clusters.
"""

from __future__ import annotations

import logging
import time
from collections import deque
from datetime import datetime, timezone
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from app.infrastructure.health.probes import ProbeRegistry, ProbeStatus, ProbeType

logger = logging.getLogger("infrastructure.health.evaluator")


class HealthScore(BaseModel):
    """Composite health score and evaluation summary."""
    component_id: str
    overall_status: ProbeStatus
    score: float = Field(default=100.0, ge=0.0, le=100.0)
    is_flapping: bool = False
    probe_breakdown: Dict[str, str] = Field(default_factory=dict)
    reasons: List[str] = Field(default_factory=list)
    evaluated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class FlapDetector:
    """
    Detects state oscillations (flapping) over a sliding time window to prevent alert fatigue
    and unnecessary rapid failover cycles.
    """

    def __init__(self, window_seconds: float = 60.0, flap_threshold_transitions: int = 4) -> None:
        self.window_seconds = window_seconds
        self.flap_threshold_transitions = flap_threshold_transitions
        self._transitions: Dict[str, deque] = {}  # component_id -> deque of (timestamp, status)

    def record_status(self, component_id: str, status: ProbeStatus) -> bool:
        """Record status observation and return whether component is currently flapping."""
        now = time.time()
        dq = self._transitions.setdefault(component_id, deque())

        # Clean old entries
        while dq and (now - dq[0][0]) > self.window_seconds:
            dq.popleft()

        # If status changed from last entry, append
        if not dq or dq[-1][1] != status:
            dq.append((now, status))

        is_flapping = len(dq) >= self.flap_threshold_transitions
        return is_flapping

    def is_flapping(self, component_id: str) -> bool:
        now = time.time()
        dq = self._transitions.get(component_id)
        if not dq:
            return False
        # Filter window
        recent = [entry for entry in dq if (now - entry[0]) <= self.window_seconds]
        return len(recent) >= self.flap_threshold_transitions


class HealthEvaluator:
    """
    Evaluates probe registry outcomes and heartbeat signals to compute composite health scores.
    """

    def __init__(self, probe_registry: ProbeRegistry, flap_detector: Optional[FlapDetector] = None) -> None:
        self.probe_registry = probe_registry
        self.flap_detector = flap_detector or FlapDetector()

    def evaluate_component(self, component_id: str) -> HealthScore:
        """Evaluate composite health for a given component."""
        probes = self.probe_registry.list_probes_for_component(component_id)
        if not probes:
            return HealthScore(
                component_id=component_id,
                overall_status=ProbeStatus.UNKNOWN,
                score=100.0,
                is_flapping=False,
                reasons=["No probes configured for component."],
            )

        probe_breakdown: Dict[str, str] = {}
        unhealthy_count = 0
        degraded_count = 0
        healthy_count = 0
        total_weight = 0.0
        earned_weight = 0.0
        reasons: List[str] = []

        # Weights per probe type
        type_weights = {
            ProbeType.LIVENESS: 30.0,
            ProbeType.READINESS: 25.0,
            ProbeType.STARTUP: 15.0,
            ProbeType.DEPENDENCY: 15.0,
            ProbeType.RESOURCE: 10.0,
            ProbeType.BUSINESS: 5.0,
        }

        for probe in probes:
            status = self.probe_registry.get_probe_status(probe.probe_id)
            probe_breakdown[probe.probe_id] = status.value
            weight = type_weights.get(probe.probe_type, 10.0)
            total_weight += weight

            if status == ProbeStatus.HEALTHY:
                healthy_count += 1
                earned_weight += weight
            elif status == ProbeStatus.DEGRADED:
                degraded_count += 1
                earned_weight += weight * 0.5
                reasons.append(f"Probe '{probe.probe_id}' ({probe.probe_type.value}) is DEGRADED.")
            elif status == ProbeStatus.UNHEALTHY:
                unhealthy_count += 1
                reasons.append(f"Probe '{probe.probe_id}' ({probe.probe_type.value}) is UNHEALTHY.")
            else:
                earned_weight += weight * 0.7  # UNKNOWN receives neutral score

        score = (earned_weight / total_weight * 100.0) if total_weight > 0 else 100.0
        score = round(max(0.0, min(100.0, score)), 2)

        # Determine overall status
        if unhealthy_count > 0 or score < 50.0:
            overall = ProbeStatus.UNHEALTHY
        elif degraded_count > 0 or score < 85.0:
            overall = ProbeStatus.DEGRADED
        else:
            overall = ProbeStatus.HEALTHY

        is_flapping = self.flap_detector.record_status(component_id, overall)
        if is_flapping:
            reasons.append("Component health is oscillating rapidly (FLAPPING detected).")

        return HealthScore(
            component_id=component_id,
            overall_status=overall,
            score=score,
            is_flapping=is_flapping,
            probe_breakdown=probe_breakdown,
            reasons=reasons,
        )
