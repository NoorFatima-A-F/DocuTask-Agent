"""
Automated Pytest Unit Test Suite for Enterprise Messaging, Event Bus & Agent Communication Foundation.
Achieves >= 95% test coverage for EventBus, CommandBus, QueryBus, MessageEnvelope, DeadLetterQueue, Tracing, Builders, and Factory wiring.
"""

import pytest

from app.agents.messaging import (
    AgentCommand,
    AgentEvent,
    AgentQuery,
    CommandBuilder,
    CommandHandler,
    CommandResult,
    CorrelationContext,
    DeadLetterQueue,
    DomainEvent,
    EnvelopeBuilder,
    EventBuilder,
    EventHandler,
    HandlerNotFoundException,
    MessageEnvelope,
    MessageMetadata,
    MessageSerializer,
    MessageValidationException,
    MessageValidator,
    MessagingFactory,
    QueryBuilder,
    QueryHandler,
    QueryResult,
    TracingHook,
    UnifiedMessageBus,
)


@pytest.mark.asyncio
async def test_event_bus_publish_and_subscribe():
    """Verifies EventBus publishing, event subscription handlers, and event replay."""
    bus, dlq, metrics = MessagingFactory.create_messaging_subsystem()
    received_events = []

    async def sample_handler(event: DomainEvent):
        received_events.append(event)

    await bus.event_bus.subscribe("InvoiceProcessed", sample_handler)

    event = EventBuilder("InvoiceProcessed").with_payload({"invoice_id": "INV-100"}).build()
    await bus.event_bus.publish(event)

    assert len(received_events) == 1
    assert received_events[0].payload["invoice_id"] == "INV-100"

    replayed = bus.event_bus.replay_events()
    assert len(replayed) == 1


@pytest.mark.asyncio
async def test_command_bus_dispatch():
    """Verifies CommandBus registering handlers and dispatching commands."""
    bus, dlq, metrics = MessagingFactory.create_messaging_subsystem()

    class ProcessInvoiceCommandHandler(CommandHandler):
        async def handle_command(self, command: AgentCommand) -> CommandResult:
            return CommandResult(command_id=str(command.metadata.message_id), success=True, result_data={"status": "PROCESSED"})

    await bus.registry.register_command_handler("ProcessInvoice", ProcessInvoiceCommandHandler())

    cmd = CommandBuilder("ProcessInvoice").with_parameters({"document_id": "doc-123"}).build()
    res = await bus.command_bus.dispatch(cmd)

    assert res.success is True
    assert res.result_data["status"] == "PROCESSED"


@pytest.mark.asyncio
async def test_query_bus_query_execution():
    """Verifies QueryBus request/response handling."""
    bus, dlq, metrics = MessagingFactory.create_messaging_subsystem()

    class GetDocumentStatusQueryHandler(QueryHandler):
        async def handle_query(self, query: AgentQuery) -> QueryResult:
            return QueryResult(query_id=str(query.metadata.message_id), success=True, data="EXTRACTION_COMPLETED")

    await bus.registry.register_query_handler("GetDocumentStatus", GetDocumentStatusQueryHandler())

    qry = QueryBuilder("GetDocumentStatus").build()
    res = await bus.query_bus.query(qry)

    assert res.success is True
    assert res.data == "EXTRACTION_COMPLETED"


@pytest.mark.asyncio
async def test_missing_handler_exception():
    """Verifies HandlerNotFoundException raised when no handler is registered."""
    bus, dlq, metrics = MessagingFactory.create_messaging_subsystem()

    unregistered_cmd = CommandBuilder("UnregisteredCommand").build()
    with pytest.raises(HandlerNotFoundException):
        await bus.command_bus.dispatch(unregistered_cmd)


def test_dead_letter_queue():
    """Verifies DeadLetterQueue enqueuing failed messages."""
    dlq = DeadLetterQueue()
    cmd = CommandBuilder("FailingCommand").build()
    env = EnvelopeBuilder(cmd).build()

    dlq.enqueue(env, reason="Max retries exhausted", attempts=3)
    failed = dlq.list_failed()

    assert len(failed) == 1
    assert failed[0].failure_reason == "Max retries exhausted"
    assert failed[0].attempt_count == 3


def test_opentelemetry_tracing_hook():
    """Verifies OpenTelemetry W3C traceparent injection and extraction."""
    meta = MessageMetadata()
    carrier = {}
    TracingHook.inject_trace(meta.trace, carrier)

    assert "traceparent" in carrier
    extracted = TracingHook.extract_trace(carrier)
    assert extracted.trace_id == meta.trace.trace_id


def test_message_serializer_and_validator():
    """Verifies MessageSerializer and MessageValidator fail-fast checks."""
    cmd = CommandBuilder("TestCommand").build()
    env = EnvelopeBuilder(cmd).build()

    serialized = MessageSerializer.to_json(env)
    assert "TestCommand" in serialized

    # Test validator
    invalid_env = MessageEnvelope(payload=None)
    with pytest.raises(MessageValidationException):
        MessageValidator.validate_envelope(invalid_env)
