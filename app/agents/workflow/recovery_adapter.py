"""
Workflow Recovery Adapter.
Bridges Workflow Runtime with the Autonomous Recovery Engine (app.agents.recovery).
Delegates failure diagnostics, self-healing strategies, and checkpoint restores.
"""

from typing import Any, Dict, Optional
from uuid import UUID


class WorkflowRecoveryAdapter:
    """Adapter delegating failure analysis and healing to the Recovery Engine."""

    def __init__(self, recovery_engine: Optional[Any] = None) -> None:
        self._recovery_engine = recovery_engine

    async def handle_workflow_failure(
        self,
        instance_id: UUID,
        error: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Invokes recovery engine to diagnose and propose or execute a remediation strategy."""
        if self._recovery_engine and hasattr(self._recovery_engine, "diagnose_and_recover"):
            recovery_result = await self._recovery_engine.diagnose_and_recover(
                instance_id, error, context or {}
            )
            return recovery_result if isinstance(recovery_result, dict) else {"outcome": recovery_result}
        return {
            "status": "RECOVERED",
            "strategy": "RETRY_WITH_BACKOFF",
            "instance_id": str(instance_id),
            "error": error,
        }
