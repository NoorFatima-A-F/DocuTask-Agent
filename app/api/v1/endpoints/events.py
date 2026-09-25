"""
DocuTask Agent - Domain Event REST Endpoints (ARODP)
Phase 13.1: Autonomous Runtime Observability & Domain Event Platform
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

from app.runtime.events import (
    DomainEvent,
    DomainEventType,
    EventSubsystem,
    EventSeverity,
    EventActor,
    event_query_service,
    EventPlatformMetrics,
    SSEEventStream,
)

router = APIRouter()


# --- Event Queries ---

@router.get("/missions/{mission_id}")
async def get_mission_events(
    mission_id: str,
    from_offset: int = Query(0, ge=0),
    limit: Optional[int] = Query(100, ge=1, le=1000),
) -> Dict[str, Any]:
    """Returns all domain events for a specific mission partition."""
    events = event_query_service.get_events_for_mission(mission_id, from_offset, limit)
    return {
        "mission_id": mission_id,
        "from_offset": from_offset,
        "total_returned": len(events),
        "events": events,
    }


@router.get("/events")
async def list_events(
    from_offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
) -> Dict[str, Any]:
    """Returns chronological global domain events."""
    events = event_query_service.get_timeline(from_offset=from_offset, limit=limit)
    return {
        "from_offset": from_offset,
        "total_returned": len(events),
        "events": events,
    }


@router.get("/events/{event_id}")
async def get_event_by_id(event_id: str) -> Dict[str, Any]:
    """Retrieves a single domain event by its ID."""
    event = event_query_service.get_event_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail=f"Event {event_id} not found")
    return {"event": event}


@router.get("/timeline")
async def get_event_timeline(
    from_offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    min_timestamp: Optional[float] = Query(None),
    max_timestamp: Optional[float] = Query(None),
) -> Dict[str, Any]:
    """Returns chronological timeline with optional time window bounds."""
    events = event_query_service.get_timeline(
        from_offset=from_offset,
        limit=limit,
        min_timestamp=min_timestamp,
        max_timestamp=max_timestamp,
    )
    return {
        "total_events": len(events),
        "events": events,
    }


@router.get("/correlation/{correlation_id}")
async def get_correlation_trace(correlation_id: str) -> Dict[str, Any]:
    """Returns all events and causal DAG tree for a distributed correlation ID."""
    return event_query_service.get_correlation_trace(correlation_id)


# --- Projections (Read Models) ---

@router.get("/planner")
async def get_planner_projection() -> Dict[str, Any]:
    """Returns the live Planner read projection."""
    return {"planner_projection": event_query_service.get_planner_state()}


@router.get("/workers")
async def get_worker_projection() -> Dict[str, Any]:
    """Returns the live Worker Pool read projection."""
    return {"worker_projection": event_query_service.get_worker_state()}


@router.get("/telemetry")
async def get_telemetry_projection() -> Dict[str, Any]:
    """Returns the live Runtime Telemetry read projection."""
    return {"telemetry_projection": event_query_service.get_telemetry_state()}


@router.get("/dashboard")
async def get_dashboard_projection() -> Dict[str, Any]:
    """Returns the unified Composite Dashboard read projection."""
    return {"dashboard": event_query_service.get_dashboard_state()}


@router.get("/metrics")
async def get_event_platform_metrics() -> Dict[str, Any]:
    """Returns performance, throughput, and capacity metrics for the event platform."""
    return EventPlatformMetrics.get_comprehensive_metrics()


# --- Event Ingestion & Filtering ---

class PublishEventPayload(BaseModel):
    mission_id: str = "global-mission"
    event_type: str = "MissionCreated"
    subsystem: str = "MISSION_CONTROL"
    component: str = "APIController"
    actor_id: str = "user"
    actor_type: str = "HUMAN"
    payload: Dict[str, Any] = Field(default_factory=dict)
    correlation_id: Optional[str] = None
    parent_event_id: Optional[str] = None
    severity: str = "INFO"


@router.post("/publish")
async def publish_event(payload: PublishEventPayload) -> Dict[str, Any]:
    """Publishes a new domain event to the event bus and store."""
    try:
        ev_type = DomainEventType(payload.event_type)
    except ValueError:
        ev_type = DomainEventType.MISSION_CREATED

    try:
        subsystem = EventSubsystem(payload.subsystem)
    except ValueError:
        subsystem = EventSubsystem.MISSION_CONTROL

    try:
        severity = EventSeverity(payload.severity)
    except ValueError:
        severity = EventSeverity.INFO

    event = DomainEvent(
        mission_id=payload.mission_id,
        parent_event_id=payload.parent_event_id,
        correlation_id=payload.correlation_id or f"corr-{payload.mission_id}",
        actor=EventActor(actor_id=payload.actor_id, actor_type=payload.actor_type),
        subsystem=subsystem,
        component=payload.component,
        event_type=ev_type,
        payload=payload.payload,
        severity=severity,
    )

    published = await event_query_service.publish_domain_event(event)
    return {"status": "PUBLISHED", "event": published.to_dict()}


class FilterEventsPayload(BaseModel):
    mission_id: Optional[str] = None
    event_types: Optional[List[str]] = None
    subsystems: Optional[List[str]] = None
    actor_ids: Optional[List[str]] = None
    severities: Optional[List[str]] = None
    min_timestamp: Optional[float] = None
    max_timestamp: Optional[float] = None
    search_text: Optional[str] = None


@router.post("/filter")
async def filter_events(payload: FilterEventsPayload) -> Dict[str, Any]:
    """Filters domain events by multi-attribute search criteria."""
    filtered = event_query_service.filter_events(payload.model_dump(exclude_none=True))
    return {
        "total_matched": len(filtered),
        "events": filtered,
    }


# --- SSE Live Event Streaming ---

@router.get("/streams")
async def stream_live_events():
    """Server-Sent Events (SSE) live domain event stream."""
    return StreamingResponse(
        SSEEventStream.generate_stream(),
        media_type="text/event-stream",
    )
