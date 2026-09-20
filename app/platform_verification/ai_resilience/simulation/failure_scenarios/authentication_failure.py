"""Scenario: AI Authentication & Authorization Failure (HTTP 401 / 403)."""

from typing import Dict, Any


class AuthenticationFailureScenario:
    """Simulates invalid or expired credentials for external AI APIs."""

    @staticmethod
    def execute(request_payload: Dict[str, Any], status_code: int = 401) -> Dict[str, Any]:
        doc_id = request_payload.get("document_id", "DOC-UNKNOWN")
        provider = request_payload.get("provider", "gemini-2.5-flash")

        return {
            "success": False,
            "status_code": status_code,
            "error_type": "UNAUTHENTICATED" if status_code == 401 else "PERMISSION_DENIED",
            "message": f"Authentication failed for {provider}: API Key invalid or expired.",
            "retryable": False,  # Non-retryable without human / credential intervention
            "document_id": doc_id,
        }
