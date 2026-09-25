"""
Enterprise Messaging, Event Bus & Agent Communication Foundation Package.
Provides MessageEnvelope, EventBus, CommandBus, QueryBus, UnifiedMessageBus,
DeadLetterQueue, TracingHook, MessagingFactory, and typed message contracts.
Decouples communication from execution across all agent subsystems.
"""

from app.agents.messaging.acknowledgements import AckStatus, MessageAcknowledgement
from app.agents.messaging.broker import BaseMessageBroker, InMemoryMessageBroker
from app.agents.messaging.builders import (
    CommandBuilder,
    EnvelopeBuilder,
    EventBuilder,
    QueryBuilder,
)
from app.agents.messaging.bus import (
    CommandBus,
    EventBus,
    QueryBus,
    UnifiedMessageBus,
)
from app.agents.messaging.channels import ChannelType, MessageChannel
from app.agents.messaging.commands import AgentCommand, CommandResult
from app.agents.messaging.consumers import EventConsumer
from app.agents.messaging.correlation import CorrelationManager
from app.agents.messaging.dead_letter import DeadLetterQueue, FailedMessage
from app.agents.messaging.delivery import DeliveryMode, DeliveryPolicy
from app.agents.messaging.dispatcher import MessageDispatcher
from app.agents.messaging.envelopes import MessageEnvelope
from app.agents.messaging.events import (
    AgentEvent,
    DomainEvent,
    HeartbeatMessage,
    ProgressEvent,
    SystemEvent,
)
from app.agents.messaging.exceptions import (
    DeadLetterException,
    HandlerNotFoundException,
    MessageRoutingException,
    MessageSerializationException,
    MessageValidationException,
    MessagingException,
)
from app.agents.messaging.factory import MessagingFactory
from app.agents.messaging.handlers import CommandHandler, EventHandler, QueryHandler
from app.agents.messaging.interfaces import ICommandBus, IEventBus, IQueryBus
from app.agents.messaging.lifecycle import MessageLifecycleState
from app.agents.messaging.metadata import (
    CorrelationContext,
    MessageMetadata,
    TraceContext,
)
from app.agents.messaging.metrics import MessagingMetricRecord, MessagingMetricsCollector
from app.agents.messaging.notifications import AgentNotification
from app.agents.messaging.policies import MessagingPolicy
from app.agents.messaging.publishers import EventPublisher
from app.agents.messaging.queries import AgentQuery, QueryResult
from app.agents.messaging.queues import MessageQueue
from app.agents.messaging.registry import HandlerRegistry
from app.agents.messaging.requests import AgentRequest
from app.agents.messaging.responses import AgentResponse
from app.agents.messaging.retry import MessageRetryPolicy
from app.agents.messaging.router import MessageRouter
from app.agents.messaging.routing import RoutingRule
from app.agents.messaging.serialization import MessageSerializer
from app.agents.messaging.streams import MessageStream
from app.agents.messaging.subscriptions import EventSubscription
from app.agents.messaging.topics import MessageTopic
from app.agents.messaging.tracing import TracingHook
from app.agents.messaging.validators import MessageValidator

__all__ = [
    # Metadata & Tracing
    "CorrelationContext",
    "TraceContext",
    "MessageMetadata",
    "TracingHook",
    "MessageEnvelope",
    "MessageLifecycleState",
    # Messages
    "AgentCommand",
    "CommandResult",
    "AgentEvent",
    "DomainEvent",
    "SystemEvent",
    "ProgressEvent",
    "HeartbeatMessage",
    "AgentQuery",
    "QueryResult",
    "AgentResponse",
    "AgentRequest",
    "AgentNotification",
    # Bus & Broker
    "IEventBus",
    "ICommandBus",
    "IQueryBus",
    "EventBus",
    "CommandBus",
    "QueryBus",
    "UnifiedMessageBus",
    "BaseMessageBroker",
    "InMemoryMessageBroker",
    "HandlerRegistry",
    "CommandHandler",
    "EventHandler",
    "QueryHandler",
    # Delivery & DLQ & Tracing
    "DeliveryMode",
    "DeliveryPolicy",
    "AckStatus",
    "MessageAcknowledgement",
    "MessageRetryPolicy",
    "DeadLetterQueue",
    "FailedMessage",
    "CorrelationManager",
    "MessageDispatcher",
    "MessageRouter",
    "RoutingRule",
    "EventSubscription",
    "EventPublisher",
    "EventConsumer",
    "MessageStream",
    "MessageChannel",
    "ChannelType",
    "MessageTopic",
    "MessageQueue",
    # Validators & Serializers & Builders & Metrics & Factory
    "MessageValidator",
    "MessageSerializer",
    "MessagingPolicy",
    "EventBuilder",
    "CommandBuilder",
    "QueryBuilder",
    "EnvelopeBuilder",
    "MessagingMetricsCollector",
    "MessagingMetricRecord",
    "MessagingFactory",
    # Exceptions
    "MessagingException",
    "MessageRoutingException",
    "HandlerNotFoundException",
    "DeadLetterException",
    "MessageValidationException",
    "MessageSerializationException",
]
