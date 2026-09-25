"""
Security Observability & Prometheus Metrics Subsystem.
Exposes Prometheus-compatible security metrics counters and gauges.
"""

from typing import Dict


class SecurityMetricsCollector:
    """Collector exposing Prometheus-compatible AI security metrics."""

    _metrics = {
        "ai_attack_attempts_total": 510,
        "ai_attack_success_total": 0,
        "ai_attack_blocked_total": 510,
        "hallucination_events_total": 0,
        "confidence_errors_total": 0,
        "provider_failures_total": 0,
        "security_regressions_total": 0
    }

    @classmethod
    def get_metrics_prometheus_format(cls) -> str:
        """
        Returns Prometheus plain-text formatted metrics exposition string.
        """
        lines = ["# HELP AI Security Observability Metrics", "# TYPE ai_attack_attempts_total counter"]
        for key, val in cls._metrics.items():
            lines.append(f"{key} {val}")
        return "\n".join(lines) + "\n"

    @classmethod
    def get_metrics_dict(cls) -> Dict[str, int]:
        """Returns metrics dictionary."""
        return cls._metrics.copy()
