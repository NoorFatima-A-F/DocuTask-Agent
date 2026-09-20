"""
Agent Workflow Manager Interface.
Defines contract for workflow DAG orchestration and multi-agent task routing.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
from app.agents.context import AgentContext


class AgentWorkflowManager(ABC):
    """Abstract interface for agent workflow orchestration."""

    @abstractmethod
    async def orchestrate(self, workflow_definition: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        """Orchestrates multi-step agent workflow execution."""
        pass
