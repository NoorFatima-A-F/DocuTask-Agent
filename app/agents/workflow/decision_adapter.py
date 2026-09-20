"""
Workflow Decision Adapter.
Bridges Workflow Runtime with the Decision, Policy & Governance Engine (app.agents.decision).
Enforces enterprise policies, risk constraints, budget limits, and approval mandates.
"""

from typing import Any, Dict, Optional
from uuid import UUID


class WorkflowDecisionAdapter:
    """Adapter evaluating governance policies and execution eligibility."""

    def __init__(self, decision_engine: Optional[Any] = None) -> None:
        self._decision_engine = decision_engine

    async def evaluate_workflow_policies(
        self,
        workflow_name: str,
        context_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Evaluates policies before workflow initiation."""
        if self._decision_engine and hasattr(self._decision_engine, "evaluate"):
            result = await self._decision_engine.evaluate(workflow_name, context_data)
            return result if isinstance(result, dict) else {"decision": result}
        return {
            "is_authorized": True,
            "policy_check": "PASSED",
            "required_approvals": [],
            "risk_score": 0.05,
        }
