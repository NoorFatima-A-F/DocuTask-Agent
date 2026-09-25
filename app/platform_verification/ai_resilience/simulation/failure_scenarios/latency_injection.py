"""Scenario: AI Latency Injection Chaos (5s, 10s, 30s delay)."""

from typing import Dict, Any


class LatencyInjectionScenario:
    """Simulates severe inference latency degradation."""

    @staticmethod
    def execute(
        request_payload: Dict[str, Any],
        injected_delay_ms: float = 5000.0,
        timeout_threshold_ms: float = 3000.0,
    ) -> Dict[str, Any]:
        doc_id = request_payload.get("document_id", "DOC-UNKNOWN")
        timed_out = injected_delay_ms > timeout_threshold_ms

        if timed_out:
            return {
                "success": False,
                "status_code": 408,
                "error_type": "AI_INFERENCE_TIMEOUT",
                "injected_delay_ms": injected_delay_ms,
                "timeout_threshold_ms": timeout_threshold_ms,
                "message": f"AI request timed out after {timeout_threshold_ms}ms (simulated delay: {injected_delay_ms}ms)",
                "retryable": True,
                "document_id": doc_id,
            }
        else:
            return {
                "success": True,
                "status_code": 200,
                "injected_delay_ms": injected_delay_ms,
                "latency_ms": injected_delay_ms,
                "document_id": doc_id,
                "data": {"extraction": "Valid Extracted Content", "confidence": 0.98},
            }
