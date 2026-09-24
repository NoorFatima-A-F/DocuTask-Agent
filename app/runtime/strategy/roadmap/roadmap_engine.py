"""
Strategic Roadmap Engine for Phase 13.11 (ASC-GEEIP).
Multi-Horizon (30d, 90d, 180d, 365d) Automated Roadmap Generation and Critical Path Scheduling.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.strategy.events.strategy_events import (
    StrategicHorizon,
    RoadmapGenerated,
)


@dataclass
class RoadmapMilestone:
    milestone_id: str
    title: str
    description: str
    target_day_offset: int
    duration_days: int = 7
    deliverables: List[str] = field(default_factory=list)
    confidence: float = 0.95
    status: str = "PENDING"  # "PENDING" | "IN_PROGRESS" | "COMPLETED" | "BLOCKED"
    dependency_ids: List[str] = field(default_factory=list)
    assigned_swarm_or_team: str = "Swarm Alpha"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "milestone_id": self.milestone_id,
            "title": self.title,
            "description": self.description,
            "target_day_offset": self.target_day_offset,
            "duration_days": self.duration_days,
            "deliverables": self.deliverables,
            "confidence": round(self.confidence, 4),
            "status": self.status,
            "dependency_ids": self.dependency_ids,
            "assigned_swarm_or_team": self.assigned_swarm_or_team,
        }


@dataclass
class StrategicRoadmap:
    roadmap_id: str = field(default_factory=lambda: f"rdmp-{uuid.uuid4().hex[:8]}")
    title: str = "Corporate Autonomous Operating Roadmap"
    horizon: StrategicHorizon = StrategicHorizon.DAYS_90
    theme: str = "Scalability, Cryptographic Governance & Autonomous Cognition"
    milestones: List[RoadmapMilestone] = field(default_factory=list)
    critical_path_ids: List[str] = field(default_factory=list)
    estimated_cost_usd: float = 12000.0
    projected_roi_multiplier: float = 3.25
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "roadmap_id": self.roadmap_id,
            "title": self.title,
            "horizon": self.horizon.value if hasattr(self.horizon, "value") else str(self.horizon),
            "theme": self.theme,
            "milestone_count": len(self.milestones),
            "milestones": [m.to_dict() for m in self.milestones],
            "critical_path_ids": self.critical_path_ids,
            "estimated_cost_usd": self.estimated_cost_usd,
            "projected_roi_multiplier": self.projected_roi_multiplier,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class RoadmapEngine:
    """
    Automates 30-day, 90-day, 180-day, and 365-day strategic roadmap generation
    with weighted interval scheduling and critical path resolution.
    """

    def __init__(self) -> None:
        self.roadmaps: Dict[StrategicHorizon, StrategicRoadmap] = {}
        self.event_log: List[Any] = []
        self._initialize_bootstrap_roadmaps()

    def _initialize_bootstrap_roadmaps(self) -> None:
        # 30-Day Tactical Roadmap
        r30 = StrategicRoadmap(
            roadmap_id="rdmp-30d-tactical",
            title="30-Day Rapid Throughput & Speculative Cache Rollout",
            horizon=StrategicHorizon.DAYS_30,
            theme="Low-Latency Cache Ingestion & Specialist Coalition Pre-Warming",
            estimated_cost_usd=4200.0,
            projected_roi_multiplier=3.80,
        )
        m1 = RoadmapMilestone(
            milestone_id="ms-30d-01",
            title="Speculative Layout Cache Activation",
            description="Zero-copy tensor cache for recurrent corporate invoice headers.",
            target_day_offset=5,
            duration_days=5,
            deliverables=["Pre-warmed tensor buffer", "Sub-50ms cache hit path"],
            confidence=0.988,
            status="COMPLETED",
            assigned_swarm_or_team="Optimization Swarm Alpha",
        )
        m2 = RoadmapMilestone(
            milestone_id="ms-30d-02",
            title="Triadic Strike Team Pre-Warming",
            description="Pre-cluster extraction workers to eliminate runtime bidding latency.",
            target_day_offset=12,
            duration_days=7,
            deliverables=["Triadic agent coalition template", "18% latency reduction"],
            confidence=0.975,
            status="IN_PROGRESS",
            dependency_ids=["ms-30d-01"],
            assigned_swarm_or_team="Swarm Coalition Beta",
        )
        m3 = RoadmapMilestone(
            milestone_id="ms-30d-03",
            title="30-Day Benchmark Audit & Certification",
            description="Run automated stress benchmarks and export truth verification certificate.",
            target_day_offset=28,
            duration_days=4,
            deliverables=["Signed provenance audit", "100k doc/day throughput verification"],
            confidence=0.992,
            status="PENDING",
            dependency_ids=["ms-30d-02"],
            assigned_swarm_or_team="Executive Governance Oracle",
        )
        r30.milestones = [m1, m2, m3]
        r30.critical_path_ids = ["ms-30d-01", "ms-30d-02", "ms-30d-03"]
        self.roadmaps[StrategicHorizon.DAYS_30] = r30

        # 90-Day Enterprise Roadmap
        r90 = StrategicRoadmap(
            roadmap_id="rdmp-90d-quarterly",
            title="90-Day Enterprise Strategic Expansion",
            horizon=StrategicHorizon.DAYS_90,
            theme="Multi-Swarm Autonomous Governance & Digital Twin Decisioning",
            estimated_cost_usd=14500.0,
            projected_roi_multiplier=3.45,
        )
        r90.milestones = [
            RoadmapMilestone(
                milestone_id="ms-90d-01",
                title="Predictive Digital Twin Synchronization Sub-20ms",
                description="Live twin state telemetry across all active worker swarms.",
                target_day_offset=20,
                duration_days=15,
                deliverables=["Sub-20ms twin sync", "Pareto optimal Monte Carlo engine"],
                confidence=0.980,
                status="COMPLETED",
            ),
            RoadmapMilestone(
                milestone_id="ms-90d-02",
                title="Autonomous Multi-Swarm Resource Negotiation",
                description="Nash-equilibrium auction protocols for GPU and token distribution.",
                target_day_offset=45,
                duration_days=20,
                deliverables=["Decentralized token exchange", "Dynamic GPU priority scheduler"],
                confidence=0.965,
                status="IN_PROGRESS",
                dependency_ids=["ms-90d-01"],
            ),
            RoadmapMilestone(
                milestone_id="ms-90d-03",
                title="Executive Strategic Decision Support System",
                description="AI Chief Strategy Officer (CSO) dashboard with continuous MCDA.",
                target_day_offset=85,
                duration_days=25,
                deliverables=["Executive Cockpit UI", "100% cryptographically audited approvals"],
                confidence=0.970,
                status="PENDING",
                dependency_ids=["ms-90d-02"],
            ),
        ]
        r90.critical_path_ids = ["ms-90d-01", "ms-90d-02", "ms-90d-03"]
        self.roadmaps[StrategicHorizon.DAYS_90] = r90

        # 180-Day Scale Roadmap
        r180 = StrategicRoadmap(
            roadmap_id="rdmp-180d-semi-annual",
            title="180-Day Semi-Annual Scale & Self-Improvement",
            horizon=StrategicHorizon.DAYS_180,
            theme="Institutional Memory Synthesis & Long-Horizon Policy Evolution",
            estimated_cost_usd=28000.0,
            projected_roi_multiplier=4.10,
        )
        r180.milestones = [
            RoadmapMilestone(
                milestone_id="ms-180d-01",
                title="Institutional Knowledge Graph Expansion",
                description="Consolidate 100,000+ mission traces into reusable organizational playbooks.",
                target_day_offset=60,
                duration_days=30,
                deliverables=["Playbook knowledge store", "Continuous anti-pattern detector"],
                confidence=0.955,
                status="PENDING",
            ),
            RoadmapMilestone(
                milestone_id="ms-180d-02",
                title="Continuous Multi-Year Goal Evolution Engine",
                description="Autonomous strategy mutation and Pareto rebalancing.",
                target_day_offset=150,
                duration_days=45,
                deliverables=["Self-updating roadmaps", "Automated budget reallocation"],
                confidence=0.940,
                status="PENDING",
                dependency_ids=["ms-180d-01"],
            ),
        ]
        r180.critical_path_ids = ["ms-180d-01", "ms-180d-02"]
        self.roadmaps[StrategicHorizon.DAYS_180] = r180

        # 365-Day Visionary Roadmap
        r365 = StrategicRoadmap(
            roadmap_id="rdmp-365d-annual",
            title="365-Day Fully Autonomous Cognitive Enterprise",
            horizon=StrategicHorizon.DAYS_365,
            theme="Zero-Human-Intervention Autonomous Enterprise Strategy Execution",
            estimated_cost_usd=55000.0,
            projected_roi_multiplier=5.50,
        )
        r365.milestones = [
            RoadmapMilestone(
                milestone_id="ms-365d-01",
                title="Autonomous Corporate Strategy Orchestration",
                description="End-to-end mission portfolio decomposition and self-executing governance.",
                target_day_offset=300,
                duration_days=65,
                deliverables=["Autonomous CSO agent runtime", "Multi-datacenter swarm federation"],
                confidence=0.925,
                status="PENDING",
            )
        ]
        r365.critical_path_ids = ["ms-365d-01"]
        self.roadmaps[StrategicHorizon.DAYS_365] = r365

    def generate_roadmap(
        self,
        horizon: StrategicHorizon,
        title: str,
        theme: str,
        milestones_spec: List[Dict[str, Any]],
        estimated_cost_usd: float = 10000.0,
        projected_roi: float = 3.0,
    ) -> StrategicRoadmap:
        milestones = []
        for spec in milestones_spec:
            m = RoadmapMilestone(
                milestone_id=f"ms-{uuid.uuid4().hex[:6]}",
                title=spec.get("title", "Strategic Milestone"),
                description=spec.get("description", ""),
                target_day_offset=spec.get("target_day_offset", 10),
                duration_days=spec.get("duration_days", 7),
                deliverables=spec.get("deliverables", []),
                confidence=spec.get("confidence", 0.95),
                dependency_ids=spec.get("dependency_ids", []),
                assigned_swarm_or_team=spec.get("assigned_swarm_or_team", "Swarm Alpha"),
            )
            milestones.append(m)

        # Compute critical path via simple topological sort on dependency_ids
        critical_path = [m.milestone_id for m in milestones if m.dependency_ids or len(milestones) == 1]
        if not critical_path and milestones:
            critical_path = [milestones[0].milestone_id]

        roadmap = StrategicRoadmap(
            title=title,
            horizon=horizon,
            theme=theme,
            milestones=milestones,
            critical_path_ids=critical_path,
            estimated_cost_usd=estimated_cost_usd,
            projected_roi_multiplier=projected_roi,
        )
        self.roadmaps[horizon] = roadmap

        event = RoadmapGenerated(
            roadmap_id=roadmap.roadmap_id,
            milestone_count=len(milestones),
            horizon=horizon,
        )
        self.event_log.append(event)
        return roadmap

    def get_roadmap(self, horizon: StrategicHorizon) -> Optional[Dict[str, Any]]:
        r = self.roadmaps.get(horizon)
        return r.to_dict() if r else None

    def list_roadmaps(self) -> List[Dict[str, Any]]:
        return [r.to_dict() for r in self.roadmaps.values()]
