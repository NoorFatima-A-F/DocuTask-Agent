"""Capability Registry Models."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class CapabilityProvider:
    provider_id: str
    plugin_id: str
    implementation_name: str
    priority: int = 100
    cost_per_unit_usd: float = 0.001
    p95_latency_ms: float = 250.0
    quality_score: float = 0.98
    health_status: str = "HEALTHY"
    supported_formats: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    registered_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "plugin_id": self.plugin_id,
            "implementation_name": self.implementation_name,
            "priority": self.priority,
            "cost_per_unit_usd": self.cost_per_unit_usd,
            "p95_latency_ms": self.p95_latency_ms,
            "quality_score": self.quality_score,
            "health_status": self.health_status,
            "supported_formats": self.supported_formats,
            "metadata": self.metadata,
        }


@dataclass
class CapabilityDefinition:
    capability_name: str
    category: str
    description: str
    input_schema: Dict[str, Any] = field(default_factory=dict)
    output_schema: Dict[str, Any] = field(default_factory=dict)
    providers: Dict[str, CapabilityProvider] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "capability_name": self.capability_name,
            "category": self.category,
            "description": self.description,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
            "provider_count": len(self.providers),
            "providers": [p.to_dict() for p in self.providers.values()],
        }
