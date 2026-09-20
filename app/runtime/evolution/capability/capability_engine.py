"""
Capability Gap Analyzer Engine for Phase 13.13 (ASEAORIP).
Discovers missing capabilities, redundant agent roles, unused modules, and knowledge blind spots.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.evolution.events.evolution_events import (
    CapabilityDeprecated,
    CapabilityExpanded,
    CapabilityGapDetected,
    CapabilityState,
    EvolutionEventBus,
)


@dataclass
class CapabilityDescriptor:
    capability_id: str = field(default_factory=lambda: f"cap_{uuid.uuid4().hex[:8]}")
    name: str = "Speculative Layout Pre-Warming"
    domain: str = "performance"
    description: str = "High precision bounding-box token grouping"
    maturity_level: str = "PRODUCTION"
    state: CapabilityState = CapabilityState.ACTIVE
    is_gap: bool = False
    gap_rationale: str = ""
    redundancy_source_id: Optional[str] = None
    efficiency_score: float = 0.92
    accuracy_score: float = 0.96
    latency_ms: float = 18.5
    cost_per_invocation: float = 0.0012
    discovered_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "capability_id": self.capability_id,
            "name": self.name,
            "domain": self.domain,
            "description": self.description,
            "maturity_level": self.maturity_level,
            "state": self.state.value if hasattr(self.state, "value") else str(self.state),
            "is_gap": self.is_gap,
            "gap_rationale": self.gap_rationale,
            "redundancy_source_id": self.redundancy_source_id,
            "efficiency_score": round(self.efficiency_score, 4),
            "accuracy_score": round(self.accuracy_score, 4),
            "latency_ms": round(self.latency_ms, 2),
            "cost_per_invocation": round(self.cost_per_invocation, 5),
            "discovered_at": self.discovered_at.isoformat(),
        }


class CapabilityEngine:
    """
    Autonomous Capability Gap & Redundancy Discovery Engine.
    """

    def __init__(self, event_bus: Optional[EvolutionEventBus] = None) -> None:
        self.event_bus = event_bus or EvolutionEventBus()
        self.capabilities: Dict[str, CapabilityDescriptor] = {}
        self._initialize_bootstrap_capabilities()

    def _initialize_bootstrap_capabilities(self) -> None:
        c1 = CapabilityDescriptor(
            capability_id="cap_doc_parsing",
            name="Multi-Column Financial Table Parsing",
            domain="document_extraction",
            description="Extracts multi-span table cells from dense financial invoices",
            state=CapabilityState.ACTIVE,
            efficiency_score=0.94,
        )
        c2 = CapabilityDescriptor(
            capability_id="cap_spec_caching",
            name="Speculative GPU Tensor Layout Caching",
            domain="caching",
            description="Pre-computes tensor layouts for recurring document geometries",
            state=CapabilityState.ACTIVE,
            efficiency_score=0.98,
        )
        c3 = CapabilityDescriptor(
            capability_id="cap_gap_streaming_ocr",
            name="Zero-Copy Direct Stream OCR Pipeline",
            domain="ocr_streaming",
            description="Zero-copy direct stream pipeline bypassing intermediate disk I/O",
            state=CapabilityState.PROPOSED,
            is_gap=True,
            gap_rationale="Current ingestion serializes to disk before OCR ingestion, introducing 45ms avoidable I/O latency.",
            efficiency_score=0.60,
        )
        self.capabilities[c1.capability_id] = c1
        self.capabilities[c2.capability_id] = c2
        self.capabilities[c3.capability_id] = c3

    def detect_capability_gaps(self, telemetry: Optional[Dict[str, Any]] = None) -> List[CapabilityDescriptor]:
        """Scans current platform state and uncovers missing architectural capabilities."""
        telemetry = telemetry or {}
        gaps: List[CapabilityDescriptor] = []

        # Simulated empirical capability gap detection
        if telemetry.get("streaming_pipeline_missing", True):
            gap_id = "cap_gap_async_event_sourcing"
            if gap_id not in self.capabilities:
                gap = CapabilityDescriptor(
                    capability_id=gap_id,
                    name="High-Throughput Lock-Free Event Sourcing Dispatcher",
                    domain="event_orchestration",
                    description="Lock-free ring buffer for ultra-high throughput event sourcing",
                    state=CapabilityState.PROPOSED,
                    is_gap=True,
                    gap_rationale="Synchronous queue locks throttle concurrency past 250 tasks/sec under peak load.",
                    efficiency_score=0.55,
                )
                self.capabilities[gap_id] = gap
                gaps.append(gap)
                self.event_bus.publish(
                    CapabilityGapDetected(payload=gap.to_dict())
                )

        return [c for c in self.capabilities.values() if c.is_gap]

    def discover_capability_gaps(self, telemetry: Optional[Dict[str, Any]] = None) -> List[CapabilityDescriptor]:
        """Alias for detect_capability_gaps."""
        return self.detect_capability_gaps(telemetry)

    def register_capability(
        self,
        name: str,
        domain: str,
        description: str = "",
        maturity_level: str = "PRODUCTION",
        accuracy_score: float = 0.95,
        latency_ms: float = 20.0,
        cost_per_invocation: float = 0.001,
        efficiency_score: float = 0.90,
        state: CapabilityState = CapabilityState.ACTIVE,
    ) -> CapabilityDescriptor:
        cap_id = f"cap_{uuid.uuid4().hex[:8]}"
        cap = CapabilityDescriptor(
            capability_id=cap_id,
            name=name,
            domain=domain,
            description=description or name,
            maturity_level=maturity_level,
            state=state,
            efficiency_score=efficiency_score,
            accuracy_score=accuracy_score,
            latency_ms=latency_ms,
            cost_per_invocation=cost_per_invocation,
            is_gap=False,
        )
        self.capabilities[cap_id] = cap

        self.event_bus.publish(
            CapabilityExpanded(payload=cap.to_dict())
        )
        return cap

    def get_capability(self, capability_id: str) -> Optional[CapabilityDescriptor]:
        return self.capabilities.get(capability_id)

    def deprecate_redundant_capability(self, capability_id: str, rationale: str) -> CapabilityDescriptor:
        cap = self.capabilities.get(capability_id)
        if not cap:
            raise ValueError(f"Capability {capability_id} not found")

        cap.state = CapabilityState.DEPRECATED
        cap.gap_rationale = rationale

        self.event_bus.publish(
            CapabilityDeprecated(payload=cap.to_dict())
        )
        return cap

    def list_capabilities(self, state: Optional[CapabilityState] = None) -> List[CapabilityDescriptor]:
        res = list(self.capabilities.values())
        if state:
            res = [c for c in res if c.state == state]
        return res

    def list_gaps(self) -> List[CapabilityDescriptor]:
        return [c for c in self.capabilities.values() if c.is_gap and c.state == CapabilityState.PROPOSED]
