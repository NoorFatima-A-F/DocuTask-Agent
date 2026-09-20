"""
Recovery Orchestrator.
Orchestrates multi-failure recovery across distributed execution sessions.
"""

from typing import List, Optional
from app.agents.recovery.context import RecoveryRequest, RecoveryResult
from app.agents.recovery.engine import RecoveryEngine


class RecoveryOrchestrator:
    """Orchestrates concurrent failure handling and bulk remediation."""

    def __init__(self, engine: Optional[RecoveryEngine] = None):
        self.engine = engine or RecoveryEngine()

    async def orchestrate_recoveries(self, requests: List[RecoveryRequest]) -> List[RecoveryResult]:
        results = []
        for req in requests:
            res = await self.engine.recover(req)
            results.append(res)
        return results
