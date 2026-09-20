"""
DocuTask Agent - Domain Event Platform (ARODP)
Phase 13.1: Autonomous Runtime Observability & Domain Event Platform
"""

# Backwards compatibility imports
from app.runtime.events.base import RuntimeEvent
from app.runtime.events.emitter import EventBus, RuntimeEventEmitter
from app.runtime.events.persistence import EventStore
from app.runtime.events.dispatcher import EventDispatcher

# Phase 13.1 Universal Domain Event Models & Subsystems
from app.runtime.events.models.event import DomainEvent
from app.runtime.events.models.event_types import (
    DomainEventType,
    EventSubsystem,
    EventSeverity,
)
from app.runtime.events.models.event_metadata import EventActor, EventMetadata
from app.runtime.events.models.mission_event import MissionEventFactory
from app.runtime.events.models.planner_event import PlannerEventFactory
from app.runtime.events.models.worker_event import WorkerEventFactory

# Bus & Store
from app.runtime.events.bus.event_bus import domain_event_bus, AsyncDomainEventBus
from app.runtime.events.bus.subscriber import EventSubscriber
from app.runtime.events.bus.publisher import EventPublisher
from app.runtime.events.store.event_store import domain_event_store, DomainEventStore
from app.runtime.events.store.append_log import AppendOnlyEventLog
from app.runtime.events.store.partition import MissionPartitionManager

# Projections
from app.runtime.events.projections.planner_projection import planner_projection, PlannerProjection
from app.runtime.events.projections.mission_projection import mission_projection, MissionProjection
from app.runtime.events.projections.worker_projection import worker_projection, WorkerProjection
from app.runtime.events.projections.telemetry_projection import telemetry_projection, TelemetryProjection
from app.runtime.events.projections.dashboard_projection import dashboard_projection, DashboardProjection

# Serialization, Correlation, Indexing & Queries
from app.runtime.events.serialization.serializer import EventSerializer
from app.runtime.events.serialization.schema_versioning import EventSchemaVersioning
from app.runtime.events.correlation.correlation import correlation_tracker, CorrelationTracker
from app.runtime.events.correlation.causation import CausationDAGBuilder
from app.runtime.events.filters.filtering import EventFilterEngine, EventFilterCriteria
from app.runtime.events.indexing.indexes import EventIndexTree
from app.runtime.events.observability.metrics import EventPlatformMetrics
from app.runtime.events.streaming.sse_stream import SSEEventStream
from app.runtime.events.api.queries import event_query_service, EventQueryService

__all__ = [
    # Legacy compatibility
    "RuntimeEvent",
    "EventBus",
    "RuntimeEventEmitter",
    "EventStore",
    "EventDispatcher",
    # Phase 13.1
    "DomainEvent",
    "DomainEventType",
    "EventSubsystem",
    "EventSeverity",
    "EventActor",
    "EventMetadata",
    "MissionEventFactory",
    "PlannerEventFactory",
    "WorkerEventFactory",
    "domain_event_bus",
    "AsyncDomainEventBus",
    "EventSubscriber",
    "EventPublisher",
    "domain_event_store",
    "DomainEventStore",
    "AppendOnlyEventLog",
    "MissionPartitionManager",
    "planner_projection",
    "PlannerProjection",
    "mission_projection",
    "MissionProjection",
    "worker_projection",
    "WorkerProjection",
    "telemetry_projection",
    "TelemetryProjection",
    "dashboard_projection",
    "DashboardProjection",
    "EventSerializer",
    "EventSchemaVersioning",
    "correlation_tracker",
    "CorrelationTracker",
    "CausationDAGBuilder",
    "EventFilterEngine",
    "EventFilterCriteria",
    "EventIndexTree",
    "EventPlatformMetrics",
    "SSEEventStream",
    "event_query_service",
    "EventQueryService",
]
