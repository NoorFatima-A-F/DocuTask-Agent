"""Scenario: AI Network Failure (TCP reset, TLS handshake drop, connection drop)."""

from typing import Dict, Any


class NetworkFailureScenario:
    """Simulates transient transport and socket level network failures."""

    @staticmethod
    def execute(request_payload: Dict[str, Any], fault_type: str = "TCP_RESET") -> Dict[str, Any]:
        doc_id = request_payload.get("document_id", "DOC-UNKNOWN")
        provider = request_payload.get("provider", "gemini-2.5-flash")

        return {
            "success": False,
            "status_code": 0,
            "error_type": fault_type,
            "message": f"Network transport error [{fault_type}] while communicating with {provider}",
            "retryable": True,
            "document_id": doc_id,
        }
