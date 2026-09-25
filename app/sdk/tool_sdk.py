"""Enterprise Agent SDK - Tool Abstractions."""

from __future__ import annotations

import abc
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ToolSchema:
    name: str
    description: str
    parameters_schema: Dict[str, Any]
    returns_schema: Dict[str, Any]
    required_permissions: List[str] = field(default_factory=list)
    cost_per_call_usd: float = 0.0001
    p95_latency_ms: float = 100.0


class BaseTool(abc.ABC):
    def __init__(self, schema: ToolSchema):
        self.schema = schema

    @abc.abstractmethod
    def invoke(self, arguments: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke external or local tool with argument verification."""
        pass
