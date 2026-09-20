"""
Distributed Tracing Interfaces.
Neutral abstractions for Spans and Trace propagation without OpenTelemetry SDK vendor lock-in.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional

class SpanStatus(str, Enum):
    UNSET = "UNSET"
    OK = "OK"
    ERROR = "ERROR"

@dataclass(frozen=True)
class SpanContextContract:
    trace_id: str
    span_id: str
    parent_span_id: Optional[str] = None
    baggage: Dict[str, str] = field(default_factory=dict)

class SpanContract(ABC):
    @abstractmethod
    def set_attribute(self, key: str, value: Any) -> "SpanContract":
        pass

    @abstractmethod
    def set_status(self, status: SpanStatus, description: Optional[str] = None) -> None:
        pass

    @abstractmethod
    def end(self) -> None:
        pass

    @abstractmethod
    def __enter__(self) -> "SpanContract":
        pass

    @abstractmethod
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass

class TracerContract(ABC):
    @abstractmethod
    def start_span(self, name: str, parent: Optional[SpanContextContract] = None) -> SpanContract:
        pass
