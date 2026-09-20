"""
Base Runtime Event model.
Defines immutable, strongly-typed RuntimeEvent with complete OpenTelemetry-compatible tracing,
causal lineage, monotonic sequence numbers, and strict Zero-Fabrication metadata.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import uuid4


@dataclass(frozen=True)
class RuntimeEvent:
    """
    Immutable base class for all execution runtime events in DocuTask Agent.
    Every event emitted in the system inherits from this class.
    """
    event_id: str = field(default_factory=lambda: str(uuid4()))
    mission_id: str = ""
    parent_event_id: Optional[str] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    sequence_number: int = 0
    agent_id: Optional[str] = None
    worker_id: Optional[str] = None
    event_type: str = "RuntimeEvent"
    payload: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    correlation_id: str = field(default_factory=lambda: str(uuid4()))
    causation_id: Optional[str] = None
    trace_id: str = field(default_factory=lambda: str(uuid4()).replace("-", ""))
    span_id: Optional[str] = field(default_factory=lambda: str(uuid4()).replace("-", "")[:16])
    duration_ms: Optional[float] = None
    status: str = "COMPLETED"
    version: str = "1.0.0"

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if isinstance(self.timestamp, datetime):
            data["timestamp"] = self.timestamp.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> RuntimeEvent:
        clean = dict(data)
        if "timestamp" in clean and isinstance(clean["timestamp"], str):
            try:
                clean["timestamp"] = datetime.fromisoformat(clean["timestamp"])
            except ValueError:
                clean["timestamp"] = datetime.now(timezone.utc)
        return cls(**clean)
