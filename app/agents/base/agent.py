"""
Abstract Base Agent Lifecycle.
Defines the template method and contract for all autonomous agents:
initialize() -> receive_goal() -> plan() -> execute() -> observe() -> reflect() -> finish() -> cleanup().
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
from app.agents.config import AgentConfig
from app.agents.context import AgentContext
from app.agents.events import (
    AgentCompletedEvent,
    AgentFailedEvent,
    ExecutionCompletedEvent,
    ExecutionStartedEvent,
    GoalReceivedEvent,
    ObservationCompletedEvent,
    PlanningCompletedEvent,
    PlanningStartedEvent,
    ReflectionStartedEvent,
)
from app.agents.exceptions import AgentException
from app.agents.interfaces.event_bus import AgentEventBus
from app.agents.logging import AgentLogger
from app.agents.metrics import AgentMetricsCollector, NoOpAgentMetricsCollector
from app.agents.observability import AgentObservabilityHook, NoOpAgentObservabilityHook
from app.agents.state import AgentState, AgentStateMachine


class BaseAgent(ABC):
    """
    Abstract Base Class defining the lifecycle contract for autonomous agents.
    Provides execution template methods, state machine management, event emission,
    context tracking, and error handling.
    """

    def __init__(
        self,
        config: AgentConfig,
        event_bus: AgentEventBus | None = None,
        metrics_collector: AgentMetricsCollector | None = None,
        observability_hook: AgentObservabilityHook | None = None,
        agent_name: str = "BaseAgent"
    ):
        self.config = config
        self.event_bus = event_bus
        self.metrics = metrics_collector or NoOpAgentMetricsCollector()
        self.observability = observability_hook or NoOpAgentObservabilityHook()
        self.agent_name = agent_name
        self.state_machine = AgentStateMachine(initial_state=AgentState.CREATED)
        self.logger = AgentLogger(agent_name=agent_name)

    @property
    def current_state(self) -> AgentState:
        """Returns current agent state."""
        return self.state_machine.current_state

    async def initialize(self, context: AgentContext) -> AgentContext:
        """Initializes agent context and transitions state machine to INITIALIZED."""
        self.state_machine.transition_to(AgentState.INITIALIZED)
        self.logger.log("INFO", "Initializing agent...", context, self.current_state)
        return context.with_history_entry("INITIALIZED", {"agent_name": self.agent_name})

    async def receive_goal(self, goal_statement: str, context: AgentContext) -> AgentContext:
        """Receives and registers execution goal statement."""
        self.logger.log("INFO", f"Goal received: '{goal_statement}'", context, self.current_state)
        if self.event_bus:
            await self.event_bus.publish(
                GoalReceivedEvent(
                    execution_id=str(context.metadata.execution_id),
                    document_id=str(context.document_id),
                    payload={"goal": goal_statement}
                )
            )
        return context.with_history_entry("GOAL_RECEIVED", {"goal": goal_statement})

    async def plan(self, goal_statement: str, context: AgentContext) -> Dict[str, Any]:
        """Lifecycle hook for goal planning phase."""
        self.state_machine.transition_to(AgentState.PLANNING)
        self.logger.log("INFO", "Starting goal planning...", context, self.current_state)
        if self.event_bus:
            await self.event_bus.publish(
                PlanningStartedEvent(
                    execution_id=str(context.metadata.execution_id),
                    document_id=str(context.document_id),
                    payload={"goal": goal_statement}
                )
            )
        plan_result = await self._do_plan(goal_statement, context)
        if self.event_bus:
            await self.event_bus.publish(
                PlanningCompletedEvent(
                    execution_id=str(context.metadata.execution_id),
                    document_id=str(context.document_id),
                    payload=plan_result
                )
            )
        return plan_result

    async def execute(self, plan: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        """Lifecycle hook for execution phase."""
        self.state_machine.transition_to(AgentState.EXECUTING)
        self.logger.log("INFO", "Starting plan execution...", context, self.current_state)
        if self.event_bus:
            await self.event_bus.publish(
                ExecutionStartedEvent(
                    execution_id=str(context.metadata.execution_id),
                    document_id=str(context.document_id),
                    payload=plan
                )
            )
        exec_result = await self._do_execute(plan, context)
        if self.event_bus:
            await self.event_bus.publish(
                ExecutionCompletedEvent(
                    execution_id=str(context.metadata.execution_id),
                    document_id=str(context.document_id),
                    payload=exec_result
                )
            )
        return exec_result

    async def observe(self, execution_output: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        """Lifecycle hook for observation phase."""
        self.state_machine.transition_to(AgentState.OBSERVING)
        self.logger.log("INFO", "Observing execution results...", context, self.current_state)
        obs_result = await self._do_observe(execution_output, context)
        if self.event_bus:
            await self.event_bus.publish(
                ObservationCompletedEvent(
                    execution_id=str(context.metadata.execution_id),
                    document_id=str(context.document_id),
                    payload=obs_result
                )
            )
        return obs_result

    async def reflect(self, observation: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        """Lifecycle hook for self-reflection phase."""
        self.state_machine.transition_to(AgentState.REFLECTING)
        self.logger.log("INFO", "Reflecting on execution and observation...", context, self.current_state)
        if self.event_bus:
            await self.event_bus.publish(
                ReflectionStartedEvent(
                    execution_id=str(context.metadata.execution_id),
                    document_id=str(context.document_id),
                    payload=observation
                )
            )
        return await self._do_reflect(observation, context)

    async def finish(self, context: AgentContext) -> AgentContext:
        """Lifecycle hook completing agent execution."""
        self.state_machine.transition_to(AgentState.COMPLETED)
        self.metrics.increment_successes(self.agent_name)
        self.logger.log("INFO", "Agent execution successfully completed.", context, self.current_state)
        if self.event_bus:
            await self.event_bus.publish(
                AgentCompletedEvent(
                    execution_id=str(context.metadata.execution_id),
                    document_id=str(context.document_id)
                )
            )
        return context.with_history_entry("COMPLETED", {"status": "SUCCESS"})

    async def cleanup(self, context: AgentContext) -> None:
        """Lifecycle hook releasing transient agent resources."""
        self.logger.log("INFO", "Cleaning up transient resources...", context, self.current_state)
        await self._do_cleanup(context)

    async def run(self, goal_statement: str, context: AgentContext) -> Dict[str, Any]:
        """
        Complete agent execution workflow template method.
        Executes full lifecycle contract:
        initialize -> receive_goal -> plan -> execute -> observe -> reflect -> finish -> cleanup.
        """
        try:
            current_ctx = await self.initialize(context)
            current_ctx = await self.receive_goal(goal_statement, current_ctx)
            plan_res = await self.plan(goal_statement, current_ctx)
            exec_res = await self.execute(plan_res, current_ctx)
            obs_res = await self.observe(exec_res, current_ctx)
            refl_res = await self.reflect(obs_res, current_ctx)
            await self.finish(current_ctx)
            return {
                "status": "COMPLETED",
                "goal": goal_statement,
                "plan": plan_res,
                "execution": exec_res,
                "observation": obs_res,
                "reflection": refl_res
            }
        except Exception as exc:
            self.metrics.increment_failures(self.agent_name, str(exc))
            if self.state_machine.can_transition_to(AgentState.FAILED):
                self.state_machine.transition_to(AgentState.FAILED)
            if self.event_bus:
                await self.event_bus.publish(
                    AgentFailedEvent(
                        execution_id=str(context.metadata.execution_id),
                        document_id=str(context.document_id),
                        payload={"error": str(exc)}
                    )
                )
            raise AgentException(f"Agent execution failed: {str(exc)}") from exc
        finally:
            await self.cleanup(context)

    # Abstract extension points for concrete subclasses
    @abstractmethod
    async def _do_plan(self, goal_statement: str, context: AgentContext) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def _do_execute(self, plan: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def _do_observe(self, execution_output: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def _do_reflect(self, observation: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def _do_cleanup(self, context: AgentContext) -> None:
        pass
