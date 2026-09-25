"""
Fluent Builder Suite for Messaging Subsystem.
Provides MessageBuilder, EnvelopeBuilder, CommandBuilder, EventBuilder, and QueryBuilder.
"""

from typing import Any, Dict
from app.agents.messaging.commands import AgentCommand
from app.agents.messaging.envelopes import MessageEnvelope
from app.agents.messaging.events import DomainEvent
from app.agents.messaging.queries import AgentQuery
from app.agents.messaging.validators import MessageValidator


class EventBuilder:
    """Fluent builder for DomainEvent models."""

    def __init__(self, event_type: str = "DomainEvent"):
        self._event_type = event_type
        self._payload: Dict[str, Any] = {}

    def with_payload(self, payload: Dict[str, Any]) -> "EventBuilder":
        self._payload.update(payload)
        return self

    def build(self) -> DomainEvent:
        return DomainEvent(event_type=self._event_type, payload=self._payload)


class CommandBuilder:
    """Fluent builder for AgentCommand models."""

    def __init__(self, command_type: str = "AgentCommand"):
        self._command_type = command_type
        self._parameters: Dict[str, Any] = {}

    def with_parameters(self, parameters: Dict[str, Any]) -> "CommandBuilder":
        self._parameters.update(parameters)
        return self

    def build(self) -> AgentCommand:
        return AgentCommand(command_type=self._command_type, parameters=self._parameters)


class QueryBuilder:
    """Fluent builder for AgentQuery models."""

    def __init__(self, query_type: str = "AgentQuery"):
        self._query_type = query_type
        self._parameters: Dict[str, Any] = {}

    def with_parameters(self, parameters: Dict[str, Any]) -> "QueryBuilder":
        self._parameters.update(parameters)
        return self

    def build(self) -> AgentQuery:
        return AgentQuery(query_type=self._query_type, parameters=self._parameters)


class EnvelopeBuilder:
    """Fluent builder for MessageEnvelope models."""

    def __init__(self, payload: Any):
        self._payload = payload
        self._payload_type = type(payload).__name__

    def build(self) -> MessageEnvelope:
        envelope = MessageEnvelope(payload=self._payload, payload_type=self._payload_type)
        MessageValidator.validate_envelope(envelope)
        return envelope
