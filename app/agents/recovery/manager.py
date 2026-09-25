"""
Recovery Manager.
Manages recovery session lifecycles, incident escalations, and dead-letter queues.
"""

from typing import Optional
from app.agents.recovery.context import RecoveryRequest, RecoveryResult
from app.agents.recovery.dead_letter import DeadLetterQueue
from app.agents.recovery.engine import RecoveryEngine
from app.agents.recovery.incident_manager import IncidentManager


class RecoveryManager:
    """Supervises recovery engine operations, dead-lettering, and incident escalation."""

    def __init__(
        self,
        engine: Optional[RecoveryEngine] = None,
        dead_letter_queue: Optional[DeadLetterQueue] = None,
        incident_manager: Optional[IncidentManager] = None
    ):
        self.engine = engine or RecoveryEngine()
        self.dead_letter_queue = dead_letter_queue or DeadLetterQueue()
        self.incident_manager = incident_manager or IncidentManager()

    async def handle_failure(self, request: RecoveryRequest) -> RecoveryResult:
        result = await self.engine.recover(request)
        if not result.is_remediated:
            self.dead_letter_queue.push(
                execution_id=request.failure.identity.execution_id,
                failure=request.failure,
                reason="Automatic recovery strategies exhausted"
            )
        return result
