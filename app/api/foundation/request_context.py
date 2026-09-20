"""
API Request Context and Tenant Boundary Envelope.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
import uuid


@dataclass
class RequestContext:
    """Standard execution context extracted from incoming API requests."""
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    organization_id: Optional[str] = None
    workspace_id: Optional[str] = None
    environment_id: str = "production"
    user_id: Optional[str] = None
    client_ip: Optional[str] = None
    user_agent: Optional[str] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "correlation_id": self.correlation_id,
            "organization_id": self.organization_id,
            "workspace_id": self.workspace_id,
            "environment_id": self.environment_id,
            "user_id": self.user_id,
            "client_ip": self.client_ip,
            "user_agent": self.user_agent,
            "timestamp": self.timestamp.isoformat(),
        }
