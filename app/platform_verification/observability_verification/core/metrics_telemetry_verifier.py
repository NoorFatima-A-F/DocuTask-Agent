"""
Metrics Telemetry & Golden Signals Verifier.
"""
from typing import List, Dict, Any
from app.platform_verification.observability_verification.domain.models import MetricsInventoryReport
from app.platform_verification.observability_verification.domain.interfaces import IMetricsTelemetryVerifier


class MetricsTelemetryVerifier(IMetricsTelemetryVerifier):
    """Audits Golden Signals (latency, traffic, errors, saturation) and AI-specific metrics."""

    REQUIRED_GOLDEN_SIGNALS = {"http_request_duration_seconds", "http_requests_total", "http_errors_total", "system_cpu_usage_pct", "system_memory_usage_bytes"}
    REQUIRED_AI_METRICS = {"ai_token_usage_total", "ai_model_latency_seconds", "ai_prompt_token_count", "ai_context_size_bytes", "ai_hallucination_score", "ai_retry_count_total"}

    def verify_metrics_inventory(self, metrics: List[Dict[str, Any]]) -> MetricsInventoryReport:
        found_names = {m.get("name") for m in metrics}

        missing_golden = list(self.REQUIRED_GOLDEN_SIGNALS - found_names)
        missing_ai = list(self.REQUIRED_AI_METRICS - found_names)

        golden_ok = len(missing_golden) == 0
        ai_ok = len(missing_ai) == 0
        status = "PASS" if golden_ok and ai_ok else "FAIL"

        return MetricsInventoryReport(
            total_metrics_collected=len(metrics),
            golden_signals_complete=golden_ok,
            ai_metrics_complete=ai_ok,
            missing_golden_signals=missing_golden,
            missing_ai_metrics=missing_ai,
            status=status,
        )
