"""Scenario: AI Quota Exhaustion & Rate Limiting (HTTP 429)."""

from typing import Dict, Any


class QuotaExhaustionScenario:
    """Simulates AI provider rate limit and quota exhaustion faults."""

    @staticmethod
    def execute(request_payload: Dict[str, Any], retry_after_seconds: int = 5) -> Dict[str, Any]:
        doc_id = request_payload.get("document_id", "DOC-UNKNOWN")
        provider = request_payload.get("provider", "gemini-2.5-flash")

        return {
            "success": False,
            "status_code": 429,
            "error_type": "RESOURCE_EXHAUSTED",
            "message": f"Quota exceeded for model {provider}: Rate limit reached. Please retry after {retry_after_seconds}s.",
            "retry_after_seconds": retry_after_seconds,
            "retryable": True,
            "document_id": doc_id,
        }
