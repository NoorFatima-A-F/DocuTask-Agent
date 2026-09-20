"""
Phase 13.17: AI Operations Events & Event Bus
High-throughput asynchronous pub/sub telemetry and operational event bus.
"""

from __future__ import annotations
import asyncio
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Callable, Any, Optional
from pydantic import BaseModel, Field
import uuid


class AIOpsEventType(str, Enum):
    TELEMETRY_INGESTED = "TELEMETRY_INGESTED"
    SPAN_STARTED = "SPAN_STARTED"
    SPAN_COMPLETED = "SPAN_COMPLETED"
    TRACE_RECORDED = "TRACE_RECORDED"
    EVALUATION_TRIGGERED = "EVALUATION_TRIGGERED"
    EVALUATION_COMPLETED = "EVALUATION_COMPLETED"
    ANOMALY_DETECTED = "ANOMALY_DETECTED"
    FAILURE_CLASSIFIED = "FAILURE_CLASSIFIED"
    PROMPT_OPTIMIZED = "PROMPT_OPTIMIZED"
    MODEL_ROUTED = "MODEL_ROUTED"
    EXPERIMENT_STARTED = "EXPERIMENT_STARTED"
    EXPERIMENT_COMPLETED = "EXPERIMENT_COMPLETED"
    PROPOSAL_GENERATED = "PROPOSAL_GENERATED"
    PROPOSAL_APPROVED = "PROPOSAL_APPROVED"
    PROPOSAL_REJECTED = "PROPOSAL_REJECTED"
    DEPLOYMENT_EXECUTED = "DEPLOYMENT_EXECUTED"
    ROLLBACK_TRIGGERED = "ROLLBACK_TRIGGERED"
    POLICY_VIOLATED = "POLICY_VIOLATED"
    AUDIT_LOGGED = "AUDIT_LOGGED"


class AIOpsEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"ev_{uuid.uuid4().hex[:10]}")
    event_type: AIOpsEventType
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    agent_id: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)
    source: str = "ai_operations_runtime"


class AIOpsEventBus:
    """In-memory event bus with subscriber callbacks and historical audit replay."""

    def __init__(self, max_history: int = 5000):
        self._subscribers: Dict[str, List[Callable[[AIOpsEvent], Any]]] = {}
        self._history: List[AIOpsEvent] = []
        self._max_history = max_history

    def subscribe(self, event_type: Union[AIOpsEventType, str], callback: Callable[[AIOpsEvent], Any]):
        key = event_type.value if isinstance(event_type, AIOpsEventType) else event_type
        if key not in self._subscribers:
            self._subscribers[key] = []
        self._subscribers[key].append(callback)

    async def publish(self, event: AIOpsEvent):
        self._history.append(event)
        if len(self._history) > self._max_history:
            self._history.pop(0)

        key = event.event_type.value
        handlers = self._subscribers.get(key, []) + self._subscribers.get("*", [])
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception as ex:
                pass

    def get_history(self, limit: int = 100, event_type: Optional[AIOpsEventType] = None) -> List[AIOpsEvent]:
        if event_type:
            filtered = [e for e in self._history if e.event_type == event_type]
            return filtered[-limit:]
        return self._history[-limit:]
