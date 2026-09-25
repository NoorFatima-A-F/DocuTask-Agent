"""
Autonomous Research Planning Engine for Phase 13.12 (ASD-HGCKEP).
Research Roadmaps, Parallel Scientific Streams, Backlog Prioritization, and Scientific Resource Allocation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.science.events.science_events import (
    ResearchPriority,
    ScienceEventBus,
    ScientificDomainEvent,
    ScientificEventType,
)


@dataclass
class ResearchStream:
    stream_id: str = field(default_factory=lambda: f"stream_{uuid.uuid4().hex[:8]}")
    title: str = "Low-Latency Speculative Acceleration"
    description: str = "Autonomous research into latency optimization."
    domain: str = "performance"
    priority: ResearchPriority = ResearchPriority.BREAKTHROUGH
    allocated_compute_units: float = 100.0
    assigned_hypothesis_ids: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def name(self) -> str:
        return self.title

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stream_id": self.stream_id,
            "title": self.title,
            "name": self.name,
            "description": self.description,
            "domain": self.domain,
            "priority": self.priority.value if hasattr(self.priority, "value") else str(self.priority),
            "allocated_compute_units": round(self.allocated_compute_units, 2),
            "assigned_hypothesis_ids": self.assigned_hypothesis_ids,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class ResearchRoadmap:
    roadmap_id: str = field(default_factory=lambda: f"roadmap_{uuid.uuid4().hex[:8]}")
    title: str = "2026 Core Discovery Roadmap"
    theme: str = "Sub-millisecond Swarm Coordination"
    stream_ids: List[str] = field(default_factory=list)
    milestones: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "roadmap_id": self.roadmap_id,
            "title": self.title,
            "theme": self.theme,
            "stream_ids": self.stream_ids,
            "milestones": self.milestones,
            "created_at": self.created_at.isoformat(),
        }


class ResearchEngine:
    """
    Scientific Research Stream & Roadmap Orchestration Engine.
    """

    def __init__(self, event_bus: Optional[ScienceEventBus] = None) -> None:
        self.event_bus = event_bus or ScienceEventBus()
        self.streams: Dict[str, ResearchStream] = {}
        self.roadmaps: Dict[str, ResearchRoadmap] = {}
        self._initialize_bootstrap_research()

    def _initialize_bootstrap_research(self) -> None:
        s1 = ResearchStream(
            stream_id="stream_seed_01",
            title="Swarm Latency & Memory Scaling",
            description="Parallel exploration into memory compaction and coordination protocols.",
            domain="performance",
            allocated_compute_units=150.0,
        )
        self.streams[s1.stream_id] = s1

        r1 = ResearchRoadmap(
            roadmap_id="roadmap_seed_01",
            title="Strategic Foundation Discovery 2026",
            theme="Autonomous Deep Cognitive Discovery",
            stream_ids=[s1.stream_id],
            milestones=["Vector Cache Formalization", "Swarm Consensus Arbitration", "Peer Publication Automation"],
        )
        self.roadmaps[r1.roadmap_id] = r1

    def create_stream(
        self,
        title: str,
        description: str,
        domain: str = "performance",
        allocated_compute_units: float = 100.0,
        priority: ResearchPriority = ResearchPriority.HIGH,
    ) -> ResearchStream:
        stream_id = f"stream_{uuid.uuid4().hex[:8]}"
        stream = ResearchStream(
            stream_id=stream_id,
            title=title,
            description=description,
            domain=domain,
            allocated_compute_units=allocated_compute_units,
            priority=priority,
        )
        self.streams[stream_id] = stream

        self.event_bus.publish(
            ScientificDomainEvent(
                event_type=ScientificEventType.RESEARCH_STREAM_CREATED,
                payload=stream.to_dict(),
            )
        )
        return stream

    def create_roadmap(
        self,
        title: str,
        theme: str,
        stream_ids: Optional[List[str]] = None,
        milestones: Optional[List[str]] = None,
    ) -> ResearchRoadmap:
        roadmap_id = f"roadmap_{uuid.uuid4().hex[:8]}"
        roadmap = ResearchRoadmap(
            roadmap_id=roadmap_id,
            title=title,
            theme=theme,
            stream_ids=stream_ids or [],
            milestones=milestones or [],
        )
        self.roadmaps[roadmap_id] = roadmap

        self.event_bus.publish(
            ScientificDomainEvent(
                event_type=ScientificEventType.ROADMAP_CREATED,
                payload=roadmap.to_dict(),
            )
        )
        return roadmap

    def assign_hypothesis(self, stream_id: str, hypothesis_id: str) -> ResearchStream:
        stream = self.streams.get(stream_id)
        if not stream:
            raise ValueError(f"Stream {stream_id} not found")
        if hypothesis_id not in stream.assigned_hypothesis_ids:
            stream.assigned_hypothesis_ids.append(hypothesis_id)
        return stream

    def list_streams(self, domain: Optional[str] = None) -> List[ResearchStream]:
        res = list(self.streams.values())
        if domain:
            res = [s for s in res if s.domain.lower() == domain.lower()]
        return res

    def list_roadmaps(self) -> List[ResearchRoadmap]:
        return list(self.roadmaps.values())
