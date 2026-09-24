"""Agent Message Model for Inter-Agent Communication Protocol.

Standardized envelope for asynchronous agent messages including task delegation,
results, telemetry, negotiation offers, and reflection updates.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict


class MessageType(str, Enum):
    TASK_REQUEST = "TASK_REQUEST"
    TASK_RESULT = "TASK_RESULT"
    FAILURE_EVENT = "FAILURE_EVENT"
    HELP_REQUEST = "HELP_REQUEST"
    NEGOTIATION_OFFER = "NEGOTIATION_OFFER"
    NEGOTIATION_ACCEPT = "NEGOTIATION_ACCEPT"
    REFLECTION_UPDATE = "REFLECTION_UPDATE"
    HEARTBEAT = "HEARTBEAT"


@dataclass
class AgentMessage:
    """Standard message envelope exchanged between autonomous agents."""

    sender_id: str
    recipient_id: str
    message_type: MessageType
    payload: Dict[str, Any] = field(default_factory=dict)
    message_id: str = field(default_factory=lambda: f"msg_{uuid.uuid4().hex[:10]}")
    correlation_id: str = field(default_factory=lambda: f"corr_{uuid.uuid4().hex[:10]}")
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    priority: int = 1  # 0: highest, 1: normal, 2: low
    metadata: Dict[str, Any] = field(default_factory=dict)
