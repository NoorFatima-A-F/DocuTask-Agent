"""Notification Dispatcher for Human Reviewers and Stakeholders."""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field
import uuid

from .channels import NotificationChannel, NotificationEventType


class NotificationMessage(BaseModel):
    message_id: str = Field(default_factory=lambda: f"notif_{uuid.uuid4().hex[:8]}")
    event_type: NotificationEventType
    recipient_id: str
    recipient_role: Optional[str] = None
    channel: NotificationChannel = NotificationChannel.IN_APP
    title: str
    body: str
    review_id: Optional[str] = None
    sent_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class NotificationDispatcher:
    """Dispatches notifications across channels (in-app, email, slack, webhook)."""

    def __init__(self):
        self._dispatched: List[NotificationMessage] = []

    def dispatch(
        self,
        event_type: NotificationEventType,
        recipient_id: str,
        title: str,
        body: str,
        channel: NotificationChannel = NotificationChannel.IN_APP,
        recipient_role: Optional[str] = None,
        review_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> NotificationMessage:
        msg = NotificationMessage(
            event_type=event_type,
            recipient_id=recipient_id,
            recipient_role=recipient_role,
            channel=channel,
            title=title,
            body=body,
            review_id=review_id,
            metadata=metadata or {},
        )
        self._dispatched.append(msg)
        return msg

    def get_notifications_for_recipient(self, recipient_id: str) -> List[NotificationMessage]:
        return [m for m in self._dispatched if m.recipient_id == recipient_id]

    def get_notifications_for_review(self, review_id: str) -> List[NotificationMessage]:
        return [m for m in self._dispatched if m.review_id == review_id]

    def list_all_notifications(self) -> List[NotificationMessage]:
        return list(self._dispatched)
