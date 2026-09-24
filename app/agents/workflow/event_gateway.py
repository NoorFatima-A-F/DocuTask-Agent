"""
Workflow Event Gateway.
Listens for external Google Cloud Pub/Sub, Webhook, and Cloud Tasks callback events to resume workflows.
"""

from typing import Any, Dict, List
from uuid import UUID
from pydantic import BaseModel


class GatewaySubscription(BaseModel):
    """Event gateway subscription binding an event topic to a workflow instance."""
    subscription_id: str
    instance_id: UUID
    topic: str
    event_type: str

    model_config = {"frozen": True}


class EventGateway:
    """Manages event subscriptions and event ingestion into workflows."""

    def __init__(self):
        self._subscriptions: Dict[str, List[GatewaySubscription]] = {}

    def subscribe(self, subscription: GatewaySubscription) -> None:
        key = f"{subscription.topic}:{subscription.event_type}"
        if key not in self._subscriptions:
            self._subscriptions[key] = []
        self._subscriptions[key].append(subscription)

    def route_incoming_event(self, topic: str, event_type: str, payload: Dict[str, Any]) -> List[UUID]:
        """Routes an incoming event to matching subscribed workflow instances."""
        key = f"{topic}:{event_type}"
        subs = self._subscriptions.get(key, [])
        return [sub.instance_id for sub in subs]
