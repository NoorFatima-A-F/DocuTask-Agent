"""
Delegation Executor.
Dispatches planned tasks to assigned agents and manages fallback execution if primary fails.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID
from app.agents.coordination.agent_registry import AgentRegistry
from app.agents.coordination.delegation import DelegationRequest, DelegationResult, DelegationStatus, DelegationTask
from app.agents.coordination.interfaces import IDelegationEngine


class DelegationExecutor(IDelegationEngine):
    """Executes delegation plans by routing work to assigned agents."""

    def __init__(self, registry: AgentRegistry):
        self.registry = registry

    async def delegate_task(self, request: DelegationRequest) -> DelegationResult:
        """Dispatches tasks to assigned agents and returns aggregated results."""
        results: Dict[str, Any] = {}
        errors: List[str] = []
        chain: List[UUID] = [request.delegator_agent_id]

        for task in request.tasks:
            target_id = task.assigned_agent_id
            if not target_id:
                errors.append(f"Task {task.task_id} has no assigned agent.")
                continue

            agent = await self.registry.get_by_id(target_id)
            if not agent or not agent.state.is_operational():
                # Attempt fallback
                if task.fallback_agent_id:
                    fallback_agent = await self.registry.get_by_id(task.fallback_agent_id)
                    if fallback_agent and fallback_agent.state.is_operational():
                        agent = fallback_agent
                        target_id = task.fallback_agent_id

            if not agent:
                errors.append(f"No operational agent available for task {task.task_id}.")
                continue

            chain.append(target_id)
            # Record assignment on agent
            updated_agent = agent.assign_task(task.task_id)
            await self.registry.update_agent(updated_agent)

            # Mark task simulated completed in coordination layer
            completed_agent = updated_agent.complete_task(task.task_id, success=True)
            await self.registry.update_agent(completed_agent)

            results[task.task_id] = {
                "status": "COMPLETED",
                "executed_by": str(target_id),
                "task_name": task.task_name
            }

        status = DelegationStatus.COMPLETED if not errors else (
            DelegationStatus.FAILED if len(results) == 0 else DelegationStatus.FALLBACK_TRIGGERED
        )

        return DelegationResult(
            delegation_id=request.delegation_id,
            status=status,
            results=results,
            errors=errors,
            delegation_chain=chain
        )
