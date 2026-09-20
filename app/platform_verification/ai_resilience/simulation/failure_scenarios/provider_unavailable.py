"""Scenario: Provider Unavailable (HTTP 503, DNS Failure, Connection Refused)."""

from typing import Dict, Any


class ProviderUnavailableScenario:
    """Simulates AI provider endpoint unavailability."""

    @staticmethod
    def execute(request_payload: Dict[str, Any], fault_mode: str = "HTTP_503") -> Dict[str, Any]:
        doc_id = request_payload.get("document_id", "DOC-UNKNOWN")
        provider = request_payload.get("provider", "gemini-2.5-flash")

        if fault_mode == "HTTP_503":
            return {
                "success": False,
                "status_code": 503,
                "error_type": "PROVIDER_UNAVAILABLE",
                "message": f"Service Unavailable: AI Provider {provider} failed to respond to upstream request for document {doc_id}",
                "retryable": True,
                "document_id": doc_id,
            }
        elif fault_mode == "DNS_TIMEOUT":
            return {
                "success": False,
                "status_code": 504,
                "error_type": "DNS_RESOLUTION_FAILURE",
                "message": f"DNS resolution timeout for api.gemini.ai while processing {doc_id}",
                "retryable": True,
                "document_id": doc_id,
            }
        else:
            return {
                "success": False,
                "status_code": 502,
                "error_type": "CONNECTION_REFUSED",
                "message": f"Connection refused by host endpoint for {provider}",
                "retryable": True,
                "document_id": doc_id,
            }
