# Event Subscription and Filtering
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Optional, Set
from app.runtime.events.base import RuntimeEvent

@dataclass
class EventSubscription:
    subscription_id: str
    mission_id: Optional[str] = None
    agent_ids: Optional[Set[str]] = None
    event_types: Optional[Set[str]] = None
    since_timestamp: Optional[datetime] = None
    custom_predicate: Optional[Callable[[RuntimeEvent], bool]] = None

    def matches(self, event: RuntimeEvent):
        if self.mission_id and event.mission_id != self.mission_id:
            return False
        if self.agent_ids and (not event.agent_id or event.agent_id not in self.agent_ids):
            return False
        if self.event_types and event.event_type not in self.event_types:
            return False
        if self.since_timestamp and event.timestamp < self.since_timestamp:
            return False
        if self.custom_predicate and not self.custom_predicate(event):
            return False
        return True
