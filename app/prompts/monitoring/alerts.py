"""Prompt Degradation & Anomaly Alerting Engine (Phase 8D).

Issues automated alerts when prompt error rates spike, latency degrades, or evaluation quality drops.
"""

from __future__ import annotations

import time
from typing import List, Optional
from pydantic import BaseModel, Field


class PromptAlert(BaseModel):
    """Alert record for prompt health issues."""
    alert_id: str
    prompt_id: str
    organization_id: str
    alert_type: str  # ERROR_SPIKE, LATENCY_SPIKE, QUALITY_DROP
    severity: str  # WARNING, CRITICAL
    message: str
    metric_value: float
    threshold_value: float
    timestamp: float = Field(default_factory=time.time)


class PromptAlertManager:
    """Monitors telemetry streams and triggers actionable alerts."""

    def __init__(
        self,
        max_error_rate: float = 0.05,
        max_latency_ms: float = 3000.0,
    ):
        self.max_error_rate = max_error_rate
        self.max_latency_ms = max_latency_ms
        self._alerts: List[PromptAlert] = []

    def check_health(
        self,
        prompt_id: str,
        organization_id: str,
        error_rate: float,
        avg_latency_ms: float,
    ) -> List[PromptAlert]:
        """Evaluate operational health metrics and emit alerts."""
        alerts = []

        if error_rate > self.max_error_rate:
            alert = PromptAlert(
                alert_id=f"alert_err_{int(time.time())}_{prompt_id}",
                prompt_id=prompt_id,
                organization_id=organization_id,
                alert_type="ERROR_SPIKE",
                severity="CRITICAL" if error_rate > 0.15 else "WARNING",
                message=f"Prompt '{prompt_id}' error rate ({error_rate:.2%}) exceeded threshold ({self.max_error_rate:.2%})",
                metric_value=error_rate,
                threshold_value=self.max_error_rate,
            )
            alerts.append(alert)
            self._alerts.append(alert)

        if avg_latency_ms > self.max_latency_ms:
            alert = PromptAlert(
                alert_id=f"alert_lat_{int(time.time())}_{prompt_id}",
                prompt_id=prompt_id,
                organization_id=organization_id,
                alert_type="LATENCY_SPIKE",
                severity="WARNING",
                message=f"Prompt '{prompt_id}' average latency ({avg_latency_ms:.1f}ms) exceeded SLA threshold ({self.max_latency_ms:.1f}ms)",
                metric_value=avg_latency_ms,
                threshold_value=self.max_latency_ms,
            )
            alerts.append(alert)
            self._alerts.append(alert)

        return alerts

    def get_alerts(self, prompt_id: Optional[str] = None) -> List[PromptAlert]:
        """List active alerts."""
        if prompt_id:
            return [a for a in self._alerts if a.prompt_id == prompt_id]
        return list(self._alerts)
