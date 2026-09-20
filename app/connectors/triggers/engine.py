"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - Trigger Engine.
Manages the lifecycle of event sources: Webhooks, Polling loops, Schedules, Event Streams, and Cloud Events.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
import logging
from typing import Any, Callable, Dict, List, Optional
import uuid
from pydantic import BaseModel, Field

from app.connectors.core.models import NormalizedEvent, TriggerDescriptor, TriggerType

logger = logging.getLogger(__name__)


class TriggerState(str, Enum):
    """Lifecycle state of an active trigger listener instance."""
    REGISTERED = "REGISTERED"
    VALIDATED = "VALIDATED"
    LISTENING = "LISTENING"
    RECEIVING = "RECEIVING"
    PROCESSING = "PROCESSING"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    ARCHIVED = "ARCHIVED"


class TriggerSubscription(BaseModel):
    """Tenant subscription to an external trigger event stream."""
    id: str = Field(default_factory=lambda: f"sub-{uuid.uuid4().hex[:8]}")
    trigger_name: str
    connector_id: str
    organization_id: str = "org-default"
    workspace_id: str = "ws-default"
    state: TriggerState = TriggerState.REGISTERED
    config: Dict[str, Any] = Field(default_factory=dict)
    callback_url: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_triggered_at: Optional[datetime] = None


class TriggerEngine:
    """
    Coordinates trigger subscriptions, poll dispatching, webhook routing,
    and event publication into the workflow engine and agent event bus.
    """

    def __init__(self, event_sink: Optional[Callable[[NormalizedEvent], None]] = None):
        self._subscriptions: Dict[str, TriggerSubscription] = {}
        self._descriptors: Dict[str, TriggerDescriptor] = {}
        self._event_sink = event_sink

    def register_trigger(self, descriptor: TriggerDescriptor) -> None:
        """Registers a supported trigger descriptor from a connector manifest."""
        self._descriptors[descriptor.name] = descriptor

    def subscribe(
        self,
        trigger_name: str,
        connector_id: str,
        organization_id: str = "org-default",
        workspace_id: str = "ws-default",
        config: Optional[Dict[str, Any]] = None,
        callback_url: Optional[str] = None,
    ) -> TriggerSubscription:
        """Creates an active trigger subscription for an organization/workspace."""
        sub = TriggerSubscription(
            trigger_name=trigger_name,
            connector_id=connector_id,
            organization_id=organization_id,
            workspace_id=workspace_id,
            state=TriggerState.LISTENING,
            config=config or {},
            callback_url=callback_url,
        )
        self._subscriptions[sub.id] = sub
        logger.info(f"Subscribed '{sub.id}' to trigger '{trigger_name}' on connector '{connector_id}'")
        return sub

    def process_incoming_event(
        self,
        subscription_id: str,
        raw_event_payload: Dict[str, Any],
        event_type: str = "external.event",
    ) -> NormalizedEvent:
        """
        Ingests and processes an incoming external event, updates trigger state,
        normalizes into a NormalizedEvent, and dispatches to the platform event sink.
        """
        sub = self._subscriptions.get(subscription_id)
        if not sub:
            sub = TriggerSubscription(
                id=subscription_id,
                trigger_name="unknown",
                connector_id="unknown",
                state=TriggerState.LISTENING,
            )
            self._subscriptions[subscription_id] = sub

        sub.state = TriggerState.RECEIVING
        sub.last_triggered_at = datetime.now(timezone.utc)

        norm_event = NormalizedEvent(
            type=event_type,
            source=f"connector.{sub.connector_id}",
            organization=sub.organization_id,
            workspace_id=sub.workspace_id,
            payload=raw_event_payload,
            metadata={"subscription_id": sub.id, "trigger_name": sub.trigger_name},
        )

        sub.state = TriggerState.PROCESSING
        if self._event_sink:
            try:
                self._event_sink(norm_event)
            except Exception as e:
                logger.error(f"Error publishing trigger event from {sub.id}: {e}")

        sub.state = TriggerState.ACKNOWLEDGED
        return norm_event

    def unsubscribe(self, subscription_id: str) -> bool:
        """Cancels and archives a trigger subscription."""
        if subscription_id in self._subscriptions:
            self._subscriptions[subscription_id].state = TriggerState.ARCHIVED
            return True
        return False

    def list_subscriptions(self, connector_id: Optional[str] = None) -> List[TriggerSubscription]:
        """Lists active subscriptions, optionally filtered by connector."""
        subs = list(self._subscriptions.values())
        if connector_id:
            subs = [s for s in subs if s.connector_id == connector_id]
        return subs
