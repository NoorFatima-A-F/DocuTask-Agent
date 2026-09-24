"""
Tests for EMAIP Agent Domain, Entity Models, Registry, and Lifecycle State Machine.
"""

import pytest
from app.agents.domain.agent_entity import (
    Agent,
    AgentLifecycleState,
    AgentType,
    TrustLevel,
)
from app.agents.lifecycle.manager import (
    AgentLifecycleManager,
    InvalidAgentStateTransitionError,
)
from app.agents.registry.agent_registry import AgentRegistry


def test_agent_entity_creation_and_serialization():
    agent = Agent(
        name="InvoiceProcessor",
        type=AgentType.INVOICE,
        capabilities=["ocr", "extraction"],
        skills=["document.ocr", "tax.compliance"],
        trust_level=TrustLevel.HIGH,
    )
    data = agent.to_dict()
    assert data["name"] == "InvoiceProcessor"
    assert data["type"] == "InvoiceAgent"
    assert data["trust_level"] == "HIGH"
    assert "ocr" in data["capabilities"]

    restored = Agent.from_dict(data)
    assert restored.name == agent.name
    assert restored.type == AgentType.INVOICE
    assert restored.trust_level == TrustLevel.HIGH


def test_agent_lifecycle_transitions():
    events = []
    manager = AgentLifecycleManager(event_listener=lambda e: events.append(e))

    agent = Agent(name="TestAgent")
    assert agent.status == AgentLifecycleState.CREATED

    # Valid transitions: CREATED -> REGISTERED -> INITIALIZED -> PLANNING -> EXECUTING -> COMPLETED
    manager.transition(agent, AgentLifecycleState.REGISTERED, reason="Agent registered in catalog")
    assert agent.status == AgentLifecycleState.REGISTERED

    manager.transition(agent, AgentLifecycleState.INITIALIZED, reason="Context loaded")
    assert agent.status == AgentLifecycleState.INITIALIZED

    manager.transition(agent, AgentLifecycleState.PLANNING, reason="Decomposing goal")
    assert agent.status == AgentLifecycleState.PLANNING

    manager.transition(agent, AgentLifecycleState.EXECUTING, reason="Running tasks")
    assert agent.status == AgentLifecycleState.EXECUTING

    manager.transition(agent, AgentLifecycleState.COMPLETED, reason="Done")
    assert agent.status == AgentLifecycleState.COMPLETED

    assert len(events) == 5
    assert len(manager.get_history(agent.id)) == 5


def test_invalid_lifecycle_transition_raises_error():
    manager = AgentLifecycleManager()
    agent = Agent(name="BadTransitionAgent")
    assert agent.status == AgentLifecycleState.CREATED

    # Cannot jump directly from CREATED to COMPLETED
    with pytest.raises(InvalidAgentStateTransitionError):
        manager.transition(agent, AgentLifecycleState.COMPLETED)


def test_agent_registry_discovery_and_matching():
    registry = AgentRegistry()

    agent1 = Agent(
        name="LegalAgent1",
        type=AgentType.LEGAL,
        capabilities=["contract.review", "compliance"],
        skills=["analysis", "summarization"],
    )
    agent2 = Agent(
        name="InvoiceAgent1",
        type=AgentType.INVOICE,
        capabilities=["invoice.processing", "ocr"],
        skills=["extraction", "tax"],
    )
    registry.register(agent1)
    registry.register(agent2)

    # Lookup
    found_legal = registry.find_capable_agents(capability="contract.review")
    assert len(found_legal) == 1
    assert found_legal[0].name == "LegalAgent1"

    found_extraction = registry.find_capable_agents(skill="extraction")
    assert len(found_extraction) == 1
    assert found_extraction[0].name == "InvoiceAgent1"

    best = registry.find_best_agent(capability="invoice.processing")
    assert best is not None
    assert best.name == "InvoiceAgent1"

    # Compatibility validation
    assert registry.validate_compatibility(agent1, ["contract.review"], ["analysis"])
    assert not registry.validate_compatibility(agent1, ["invoice.processing"], ["analysis"])
