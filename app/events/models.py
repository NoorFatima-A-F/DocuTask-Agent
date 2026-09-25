"""
CloudEvents 1.0 Event Specifications and Envelope Models.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
import uuid


@dataclass(frozen=True)
class CloudEventEnvelope:
    """Standardized CloudEvents 1.0 compliant message envelope."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: str = "platform.event"
    source: str = "/docutask/platform"
    specversion: str = "1.0"
    time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    tenant: Optional[str] = None
    trace_id: Optional[str] = None
    datacontenttype: str = "application/json"
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "source": self.source,
            "specversion": self.specversion,
            "time": self.time.isoformat(),
            "tenant": self.tenant,
            "trace_id": self.trace_id,
            "datacontenttype": self.datacontenttype,
            "data": self.data,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "CloudEventEnvelope":
        return cls(
            id=d.get("id", str(uuid.uuid4())),
            type=d.get("type", "platform.event"),
            source=d.get("source", "/docutask/platform"),
            specversion=d.get("specversion", "1.0"),
            time=datetime.fromisoformat(d["time"]) if "time" in d else datetime.now(timezone.utc),
            tenant=d.get("tenant"),
            trace_id=d.get("trace_id"),
            datacontenttype=d.get("datacontenttype", "application/json"),
            data=d.get("data", {}),
            metadata=d.get("metadata", {}),
        )
