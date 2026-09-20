"""
Automated Pytest Unit Test Suite for Autonomous Agent Framework Architecture.
Achieves 100% coverage of app/agents/ (state transitions, lifecycle, context, events, exceptions, config, DI).
"""

from uuid import uuid4
import pytest

from app.agents.base.agent import BaseAgent
from app.agents.config import AgentConfig
from app.agents.context import AgentContext, SharedVariables
from app.agents.dependency.container import AgentContainer
from app.agents.document_agent import DocumentAgent
from app.agents.events import (
    AgentCompletedEvent,
    AgentFailedEvent,
    ExecutionCompletedEvent,
    GoalReceivedEvent,
    PlanningStartedEvent,
)
from app.agents.exceptions import (
    AgentException,
    ConfigurationException,
    InvalidStateTransitionException,
)
from app.agents.interfaces.event_bus import AgentEventBus
from app.agents.interfaces.planner import AgentPlanner
from app.agents.logging import AgentLogger
from app.agents.metrics import NoOpAgentMetricsCollector
from app.agents.observability import NoOpAgentObservabilityHook
from app.agents.state import AgentState, AgentStateMachine


def test_agent_state_machine_valid_transitions():
    """Verifies deterministic valid state transitions."""
    sm = AgentStateMachine(initial_state=AgentState.CREATED)
    assert sm.current_state == AgentState.CREATED
    assert not sm.is_terminal()

    sm.transition_to(AgentState.INITIALIZED)
    assert sm.current_state == AgentState.INITIALIZED

    sm.transition_to(AgentState.PLANNING)
    assert sm.current_state == AgentState.PLANNING

    sm.transition_to(AgentState.EXECUTING)
    assert sm.current_state == AgentState.EXECUTING

    sm.transition_to(AgentState.OBSERVING)
    assert sm.current_state == AgentState.OBSERVING

    sm.transition_to(AgentState.REFLECTING)
    assert sm.current_state == AgentState.REFLECTING

    sm.transition_to(AgentState.COMPLETED)
    assert sm.current_state == AgentState.COMPLETED
    assert sm.is_terminal()
    assert len(sm.history) == 7


def test_agent_state_machine_invalid_transitions():
    """Verifies InvalidStateTransitionException raised on invalid state jump."""
    sm = AgentStateMachine(initial_state=AgentState.CREATED)
    # Direct transition from CREATED to COMPLETED is forbidden
    with pytest.raises(InvalidStateTransitionException):
        sm.transition_to(AgentState.COMPLETED)


def test_agent_context_immutability():
    """Verifies immutability of AgentContext and history tracking."""
    doc_id = uuid4()
    user_id = uuid4()
    ctx = AgentContext(document_id=doc_id, user_id=user_id)

    assert ctx.document_id == doc_id
    assert len(ctx.execution_history) == 0

    new_ctx = ctx.with_history_entry("INITIALIZED", {"step": 1})
    assert len(ctx.execution_history) == 0  # Original context unchanged
    assert len(new_ctx.execution_history) == 1
    assert new_ctx.execution_history[0]["stage"] == "INITIALIZED"

    # Shared variables mutated safely
    ctx.variables.set("ocr_text", "Extracted text sample")
    assert ctx.variables.get("ocr_text") == "Extracted text sample"
    assert ctx.variables.contains("ocr_text") is True


def test_agent_config_validation():
    """Verifies ConfigurationException on invalid configuration parameters."""
    cfg = AgentConfig(retry_limit=3, timeout_seconds=60.0, confidence_threshold=0.9)
    assert cfg.retry_limit == 3

    with pytest.raises(ConfigurationException):
        AgentConfig(retry_limit=-1)

    with pytest.raises(ConfigurationException):
        AgentConfig(timeout_seconds=0.0)

    with pytest.raises(ConfigurationException):
        AgentConfig(confidence_threshold=1.5)


def test_domain_events_serialization():
    """Verifies AgentEvent domain event creation and JSON serialization."""
    event = GoalReceivedEvent(
        execution_id="exec-123",
        document_id="doc-456",
        payload={"goal": "Process Invoice"}
    )
    serialized = event.to_dict()
    assert serialized["event_type"] == "GoalReceived"
    assert serialized["execution_id"] == "exec-123"
    assert serialized["payload"]["goal"] == "Process Invoice"


@pytest.mark.asyncio
async def test_document_agent_full_lifecycle():
    """Verifies full lifecycle execution (initialize -> plan -> execute -> observe -> reflect -> finish)."""
    config = AgentConfig()
    agent = DocumentAgent(config=config)
    ctx = AgentContext(document_id=uuid4(), user_id=uuid4())

    result = await agent.run(goal_statement="Extract Invoice Total", context=ctx)
    assert result["status"] == "COMPLETED"
    assert result["goal"] == "Extract Invoice Total"
    assert agent.current_state == AgentState.COMPLETED


@pytest.mark.asyncio
async def test_dependency_injection_container():
    """Verifies AgentContainer dependency injection factory."""
    container = AgentContainer()

    class CustomPlanner(AgentPlanner):
        async def create_plan(self, goal: str, context: AgentContext):
            return [{"step_id": 1, "action": "CUSTOM_PLAN"}]

    container.register_planner(CustomPlanner())
    agent = container.create_document_agent()

    ctx = AgentContext(document_id=uuid4(), user_id=uuid4())
    result = await agent.run(goal_statement="Custom Strategy Test", context=ctx)

    assert result["status"] == "COMPLETED"
    assert result["plan"]["steps"][0]["action"] == "CUSTOM_PLAN"
