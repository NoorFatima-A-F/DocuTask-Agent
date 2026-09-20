"""
Fallback Manager.
Provides static or dynamic degraded fallback responses when all recovery strategies are exhausted.
"""

from typing import Any, Dict


class FallbackManager:
    """Returns safe degraded output payloads when operations fail completely."""

    def get_fallback_output(self, capability: str) -> Dict[str, Any]:
        return {
            "status": "DEGRADED_FALLBACK",
            "capability": capability,
            "message": "Fallback default payload provided due to unrecoverable fault."
        }
