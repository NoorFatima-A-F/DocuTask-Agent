"""
Coordination Decision Adapter.
Delegates policy compliance and risk evaluations to the Decision & Governance Engine.
"""

from typing import Any, Dict, Optional
from uuid import UUID


class CoordinationDecisionAdapter:
    """Adapter verifying governance policies before authorizing agent delegation or team actions."""

    def __init__(self, decision_engine: Optional[Any] = None):
        self._decision_engine = decision_engine

    async def check_delegation_authorized(self, delegator_id: UUID, target_agent_id: UUID, task_name: str) -> bool:
        """Verifies policy allows delegating this task to the target agent."""
        if self._decision_engine and hasattr(self._decision_engine, "evaluate_policy"):
            return await self._decision_engine.evaluate_policy(task_name)
        return True
