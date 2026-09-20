"""Tool Definition Domain Model for Autonomous Tool Reasoning.

Defines schemas, performance characteristics, cost metrics, and modality support
for tools dynamically selected by reasoning agents.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Coroutine, Dict, List, Optional


class Modality(str, Enum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    PDF = "PDF"
    HANDWRITING = "HANDWRITING"
    TABLE = "TABLE"
    JSON = "JSON"


@dataclass
class ToolDefinition:
    """Detailed definition and operational constraints of a tool."""

    tool_id: str
    name: str
    category: str  # "OCR", "EXTRACTION", "VALIDATION", "COMPLIANCE", "TRANSFORM"
    description: str = ""
    supported_modalities: List[Modality] = field(default_factory=list)
    cost_per_call: float = 0.001
    latency_ms_avg: float = 150.0
    accuracy_score: float = 0.95
    required_permissions: List[str] = field(default_factory=list)
    executor: Optional[Callable[[Dict[str, Any]], Coroutine[Any, Any, Dict[str, Any]]]] = None
    input_schema: Dict[str, Any] = field(default_factory=dict)
    output_schema: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def supports_modality(self, modality: Modality) -> bool:
        return modality in self.supported_modalities
