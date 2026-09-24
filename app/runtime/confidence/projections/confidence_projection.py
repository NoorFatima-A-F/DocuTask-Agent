"""
Confidence Projection Read Model for Phase 13.3 (ASCE-CGP).
Subscribes to domain events and maintains real-time confidence states.
"""

from __future__ import annotations

from typing import Any, Dict
from datetime import datetime, timezone
from app.runtime.events.bus.subscriber import EventSubscriber
from app.runtime.events.models.event import DomainEvent
from app.runtime.events.models.event_types import EventSubsystem


class ConfidenceProjection(EventSubscriber):
    """
    Event-driven read projection that continuously updates confidence scores from runtime events.
    """

    def __init__(self, mission_id: str = "mission-001"):
        super().__init__(
            subscriber_id=f"ConfidenceProjection-{mission_id}",
            handler=self.on_event,
            subsystems={
                EventSubsystem.PLANNER,
                EventSubsystem.WORKER_POOL,
                EventSubsystem.OCR_SERVICE,
                EventSubsystem.VALIDATION_ENGINE,
                EventSubsystem.TRUTH_LEDGER,
            },
        )
        self.mission_id = mission_id
        self.overall_score = 0.985
        self.uncertainty = 0.015
        self.events_processed = 0
        self.last_updated = datetime.now(timezone.utc).isoformat()

    async def on_event(self, event: DomainEvent) -> None:
        self.events_processed += 1
        payload = event.payload

        if "confidence" in payload and isinstance(payload["confidence"], (int, float)):
            # Update running average
            alpha = 0.3
            self.overall_score = round(alpha * float(payload["confidence"]) + (1.0 - alpha) * self.overall_score, 4)

        self.last_updated = datetime.now(timezone.utc).isoformat()

    def get_projection(self) -> Dict[str, Any]:
        return {
            "mission_id": self.mission_id,
            "overall_score": self.overall_score,
            "uncertainty": self.uncertainty,
            "events_processed": self.events_processed,
            "last_updated": self.last_updated,
        }
