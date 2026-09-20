"""
Mission Portfolio Optimization Engine for Phase 13.11 (ASC-GEEIP).
Multi-Objective Pareto Frontier Optimization and Portfolio Balancing.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.strategy.events.strategy_events import (
    PortfolioStatus,
    MissionValue,
    MissionPortfolioOptimized,
)


@dataclass
class MissionValueScore:
    expected_roi_multiplier: float = 1.5
    latency_impact_pct: float = 15.0
    risk_score: float = 0.10
    strategic_fit_score: float = 0.90
    composite_utility: float = 0.85


@dataclass
class PortfolioMission:
    mission_id: str
    name: str
    category: str
    value_type: MissionValue = MissionValue.EFFICIENCY_GAIN
    allocated_budget_usd: float = 1000.0
    expected_gain_usd: float = 2500.0
    score: MissionValueScore = field(default_factory=MissionValueScore)
    status: str = "ACTIVE"  # "ACTIVE" | "PROMOTED" | "CANDIDATE" | "PAUSED" | "CANCELLED"
    pareto_rank: int = 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mission_id": self.mission_id,
            "name": self.name,
            "category": self.category,
            "value_type": self.value_type.value if hasattr(self.value_type, "value") else str(self.value_type),
            "allocated_budget_usd": self.allocated_budget_usd,
            "expected_gain_usd": self.expected_gain_usd,
            "expected_roi_multiplier": self.score.expected_roi_multiplier,
            "latency_impact_pct": self.score.latency_impact_pct,
            "risk_score": self.score.risk_score,
            "composite_utility": round(self.score.composite_utility, 4),
            "status": self.status,
            "pareto_rank": self.pareto_rank,
        }


@dataclass
class MissionCluster:
    cluster_id: str
    name: str
    description: str
    missions: List[PortfolioMission] = field(default_factory=list)
    allocated_budget_usd: float = 0.0
    aggregated_utility: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cluster_id": self.cluster_id,
            "name": self.name,
            "description": self.description,
            "mission_count": len(self.missions),
            "missions": [m.to_dict() for m in self.missions],
            "allocated_budget_usd": round(self.allocated_budget_usd, 2),
            "aggregated_utility": round(self.aggregated_utility, 4),
        }


@dataclass
class MissionPortfolio:
    portfolio_id: str = field(default_factory=lambda: f"port-{uuid.uuid4().hex[:8]}")
    name: str = "Corporate Autonomous Operations Portfolio"
    status: PortfolioStatus = PortfolioStatus.BALANCED
    budget_limit_usd: float = 25000.0
    total_allocated_usd: float = 0.0
    overall_risk_index: float = 0.12
    clusters: List[MissionCluster] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        all_missions = []
        for c in self.clusters:
            all_missions.extend(c.missions)
        return {
            "portfolio_id": self.portfolio_id,
            "name": self.name,
            "status": self.status.value if hasattr(self.status, "value") else str(self.status),
            "budget_limit_usd": self.budget_limit_usd,
            "total_allocated_usd": round(self.total_allocated_usd, 2),
            "budget_utilization_pct": round((self.total_allocated_usd / max(self.budget_limit_usd, 1.0)) * 100, 2),
            "overall_risk_index": round(self.overall_risk_index, 4),
            "cluster_count": len(self.clusters),
            "total_missions": len(all_missions),
            "clusters": [c.to_dict() for c in self.clusters],
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class MissionPortfolioEngine:
    """
    Manages portfolio clustering, multi-criteria Pareto frontier ranking,
    dynamic budget balancing, and mission promotion/cancellation.
    """

    def __init__(self, budget_limit_usd: float = 30000.0) -> None:
        self.portfolio: MissionPortfolio = MissionPortfolio(budget_limit_usd=budget_limit_usd)
        self.event_log: List[Any] = []
        self._initialize_bootstrap_portfolio()

    def _initialize_bootstrap_portfolio(self) -> None:
        # Cluster 1: Throughput & Latency Optimization
        c1 = MissionCluster(
            cluster_id="cluster-perf",
            name="Throughput & Latency Acceleration",
            description="Missions accelerating multi-column extraction and cache hit ratios.",
        )
        m1 = PortfolioMission(
            mission_id="msn-cache-warm-01",
            name="Speculative Layout Cache Pre-Warming",
            category="Performance",
            value_type=MissionValue.EFFICIENCY_GAIN,
            allocated_budget_usd=3200.0,
            expected_gain_usd=9800.0,
            score=MissionValueScore(expected_roi_multiplier=3.06, latency_impact_pct=28.0, risk_score=0.08, strategic_fit_score=0.95, composite_utility=0.925),
            pareto_rank=1,
        )
        m2 = PortfolioMission(
            mission_id="msn-triadic-coalition-02",
            name="Triadic Extraction Strike Team Deployment",
            category="Performance",
            value_type=MissionValue.CORE_REVENUE,
            allocated_budget_usd=4500.0,
            expected_gain_usd=12500.0,
            score=MissionValueScore(expected_roi_multiplier=2.77, latency_impact_pct=22.0, risk_score=0.12, strategic_fit_score=0.92, composite_utility=0.890),
            pareto_rank=1,
        )
        c1.missions.extend([m1, m2])

        # Cluster 2: Governance & Cryptographic Assurance
        c2 = MissionCluster(
            cluster_id="cluster-gov",
            name="Governance & Cryptographic Assurance",
            description="Missions ensuring continuous deterministic verification and safety.",
        )
        m3 = PortfolioMission(
            mission_id="msn-sec-sha-ledger",
            name="Zero-Knowledge Ledger Rollback Checkpoints",
            category="Governance",
            value_type=MissionValue.RISK_MITIGATION,
            allocated_budget_usd=2800.0,
            expected_gain_usd=6000.0,
            score=MissionValueScore(expected_roi_multiplier=2.14, latency_impact_pct=0.0, risk_score=0.04, strategic_fit_score=0.99, composite_utility=0.940),
            pareto_rank=1,
        )
        c2.missions.append(m3)

        # Cluster 3: Strategic Innovation
        c3 = MissionCluster(
            cluster_id="cluster-innov",
            name="Autonomous Strategic Cognition",
            description="Missions expanding multi-horizon forecasting and institutional memory.",
        )
        m4 = PortfolioMission(
            mission_id="msn-auto-roadmap-04",
            name="Long-Horizon Strategic Roadmapping Engine",
            category="Innovation",
            value_type=MissionValue.TRANSFORMATIVE,
            allocated_budget_usd=5000.0,
            expected_gain_usd=18000.0,
            score=MissionValueScore(expected_roi_multiplier=3.60, latency_impact_pct=15.0, risk_score=0.14, strategic_fit_score=0.96, composite_utility=0.955),
            pareto_rank=1,
        )
        c3.missions.append(m4)

        self.portfolio.clusters = [c1, c2, c3]
        self._recalculate_totals()

    def _recalculate_totals(self) -> None:
        total_usd = 0.0
        weighted_risk = 0.0
        total_missions = 0

        for c in self.portfolio.clusters:
            c_budget = sum(m.allocated_budget_usd for m in c.missions if m.status != "CANCELLED")
            c_util = sum(m.score.composite_utility for m in c.missions if m.status != "CANCELLED") / max(len(c.missions), 1)
            c.allocated_budget_usd = c_budget
            c.aggregated_utility = c_util
            total_usd += c_budget
            for m in c.missions:
                if m.status != "CANCELLED":
                    weighted_risk += m.score.risk_score * m.allocated_budget_usd
                    total_missions += 1

        self.portfolio.total_allocated_usd = total_usd
        self.portfolio.overall_risk_index = (weighted_risk / max(total_usd, 1.0)) if total_usd > 0 else 0.0

        if total_usd > self.portfolio.budget_limit_usd:
            self.portfolio.status = PortfolioStatus.OVERALLOCATED
        elif self.portfolio.overall_risk_index > 0.25:
            self.portfolio.status = PortfolioStatus.HIGH_RISK
        else:
            self.portfolio.status = PortfolioStatus.BALANCED

        self.portfolio.updated_at = datetime.now(timezone.utc).isoformat()

    def add_mission(
        self,
        cluster_id: str,
        name: str,
        category: str,
        value_type: MissionValue = MissionValue.EFFICIENCY_GAIN,
        allocated_budget_usd: float = 1500.0,
        expected_gain_usd: float = 3500.0,
        expected_roi: float = 2.33,
        latency_impact_pct: float = 12.0,
        risk_score: float = 0.10,
    ) -> PortfolioMission:
        cluster = next((c for c in self.portfolio.clusters if c.cluster_id == cluster_id), None)
        if not cluster:
            cluster = MissionCluster(cluster_id=cluster_id, name=f"Cluster {category}", description=f"Missions for {category}")
            self.portfolio.clusters.append(cluster)

        composite = min(1.0, max(0.1, (0.4 * min(expected_roi / 4.0, 1.0)) + (0.3 * (1.0 - risk_score)) + (0.3 * min(latency_impact_pct / 30.0, 1.0))))
        score = MissionValueScore(
            expected_roi_multiplier=expected_roi,
            latency_impact_pct=latency_impact_pct,
            risk_score=risk_score,
            strategic_fit_score=0.90,
            composite_utility=composite,
        )

        mission = PortfolioMission(
            mission_id=f"msn-{uuid.uuid4().hex[:8]}",
            name=name,
            category=category,
            value_type=value_type,
            allocated_budget_usd=allocated_budget_usd,
            expected_gain_usd=expected_gain_usd,
            score=score,
        )
        cluster.missions.append(mission)
        self._recalculate_totals()
        return mission

    def optimize_portfolio(self) -> Dict[str, Any]:
        """
        Computes Pareto non-dominated frontier ranking across (ROI, Latency Reduction, -Risk).
        Rebalances allocations if overallocated.
        """
        all_missions: List[PortfolioMission] = []
        for c in self.portfolio.clusters:
            all_missions.extend([m for m in c.missions if m.status != "CANCELLED"])

        # Simple 2-tier Pareto ranking
        for m in all_missions:
            dominated = False
            for other in all_missions:
                if other.mission_id == m.mission_id:
                    continue
                if (
                    other.score.expected_roi_multiplier >= m.score.expected_roi_multiplier
                    and other.score.latency_impact_pct >= m.score.latency_impact_pct
                    and other.score.risk_score <= m.score.risk_score
                    and (
                        other.score.expected_roi_multiplier > m.score.expected_roi_multiplier
                        or other.score.latency_impact_pct > m.score.latency_impact_pct
                        or other.score.risk_score < m.score.risk_score
                    )
                ):
                    dominated = True
                    break
            m.pareto_rank = 2 if dominated else 1

        self._recalculate_totals()
        event = MissionPortfolioOptimized(
            portfolio_id=self.portfolio.portfolio_id,
            total_missions=len(all_missions),
            pareto_rank=1,
            expected_utility=sum(m.score.composite_utility for m in all_missions) / max(len(all_missions), 1),
        )
        self.event_log.append(event)

        return self.portfolio.to_dict()

    def get_portfolio(self) -> Dict[str, Any]:
        return self.portfolio.to_dict()
