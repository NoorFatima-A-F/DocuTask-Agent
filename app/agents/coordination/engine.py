"""
Enterprise Multi-Agent Coordination Engine.
Primary distributed intelligence facade managing agent capability matching, team formation,
delegation orchestration, and collaborative goal achievement.
"""

import time
from typing import Optional
from uuid import uuid4
from app.agents.coordination.context import CoordinationRequest, CoordinationResult
from app.agents.coordination.coordinator import AgentCoordinator
from app.agents.coordination.delegation import DelegationMode, DelegationRequest, DelegationTask
from app.agents.coordination.interfaces import IAgentCoordinator
from app.agents.coordination.lifecycle import CoordinationLifecycleState
from app.agents.coordination.manager import CoordinationManager
from app.agents.coordination.metadata import CoordinationIdentity, CoordinationStatistics
from app.agents.coordination.metrics import CoordinationMetricsCollector
from app.agents.coordination.orchestrator import CoordinationOrchestrator


class CoordinationEngine(IAgentCoordinator):
    """
    Primary Multi-Agent Coordination Engine.
    Coordinates agents, teams, swarms, and delegation flows.
    Never executes tasks directly; delegates work via adapters to the Execution Engine.
    """

    def __init__(
        self,
        manager: Optional[CoordinationManager] = None,
        coordinator: Optional[AgentCoordinator] = None,
        orchestrator: Optional[CoordinationOrchestrator] = None,
        metrics_collector: Optional[CoordinationMetricsCollector] = None
    ):
        self.manager = manager or CoordinationManager()
        self.coordinator = coordinator or AgentCoordinator(registry=self.manager.registry)
        self.orchestrator = orchestrator or CoordinationOrchestrator(
            registry=self.manager.registry,
            coordinator=self.coordinator
        )
        self.metrics = metrics_collector or CoordinationMetricsCollector()

    async def coordinate(self, request: CoordinationRequest) -> CoordinationResult:
        """Executes distributed multi-agent coordination workflow for a goal."""
        start_time = time.monotonic()
        identity = CoordinationIdentity(
            tenant_id=request.context.tenant_id,
            correlation_id=request.context.correlation_id
        )

        self.metrics.record_delegation_started()

        try:
            available_agents = await self.manager.registry.list_available()
            if not available_agents:
                self.metrics.record_delegation_failed()
                return CoordinationResult(
                    identity=identity,
                    lifecycle_state=CoordinationLifecycleState.FAILED,
                    errors=["Zero available agents in registry to coordinate."]
                )

            # Create delegation task for the goal
            task = DelegationTask(
                task_id=f"task_{uuid4().hex[:8]}",
                task_name=f"Process: {request.goal[:40]}",
                required_skills=request.required_capabilities,
                payload=request.input_data
            )
            del_request = DelegationRequest(
                delegator_agent_id=request.initiator_agent_id,
                mode=DelegationMode.SINGLE,
                tasks=[task]
            )

            del_result = await self.coordinator.coordinate(del_request)
            duration_ms = (time.monotonic() - start_time) * 1000.0

            if del_result.errors:
                self.metrics.record_delegation_failed()
            else:
                self.metrics.record_delegation_completed(duration_ms)

            stats = CoordinationStatistics(
                discovery_duration_ms=duration_ms * 0.3,
                delegation_duration_ms=duration_ms * 0.7,
                total_duration_ms=duration_ms,
                agents_discovered=len(available_agents),
                agents_allocated=len(del_result.delegation_chain)
            )

            state = (
                CoordinationLifecycleState.COMPLETED
                if not del_result.errors else CoordinationLifecycleState.FAILED
            )

            return CoordinationResult(
                identity=identity,
                lifecycle_state=state,
                outputs=del_result.results,
                participating_agents=del_result.delegation_chain,
                statistics=stats,
                errors=del_result.errors
            )

        except Exception as e:
            self.metrics.record_delegation_failed()
            duration_ms = (time.monotonic() - start_time) * 1000.0
            return CoordinationResult(
                identity=identity,
                lifecycle_state=CoordinationLifecycleState.FAILED,
                statistics=CoordinationStatistics(total_duration_ms=duration_ms),
                errors=[str(e)]
            )
