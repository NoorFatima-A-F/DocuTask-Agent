"""Multi-factor Risk Analyzer and Anomaly Detector."""

from typing import Dict, Any, List, Optional
import collections
from datetime import datetime, timezone
from pydantic import BaseModel, Field

from .scoring import RiskCategory, RiskScoringModel, RiskScoreBreakdown
from ..warehouse.repositories import GovernanceDataWarehouseRepository
from ..warehouse.schemas import WarehouseQueryFilter


class RiskAnalysisSummary(BaseModel):
    tenant_id: str
    overall_risk_score: float = 0.0
    enterprise_risk_level: str = "LOW"  # LOW, MEDIUM, HIGH, CRITICAL
    category_scores: Dict[str, float] = Field(default_factory=dict)
    critical_risk_events_count: int = 0
    top_risk_entities: List[Dict[str, Any]] = Field(default_factory=list)
    risk_anomalies_detected: List[str] = Field(default_factory=list)


class RiskAnalyzer:
    """Analyzes multi-dimensional risk posture and detects anomalies."""

    def __init__(self, repository: Optional[GovernanceDataWarehouseRepository] = None):
        self.repo = repository or GovernanceDataWarehouseRepository()

    def analyze_risk_posture(self, tenant_id: str = "*") -> RiskAnalysisSummary:
        q = WarehouseQueryFilter(tenant_id=tenant_id)
        risk_events = self.repo.query_risk_events(q)
        decisions = self.repo.query_decisions(q)
        executions = self.repo.query_ai_executions(q)

        category_events: Dict[str, List[float]] = collections.defaultdict(list)
        for r in risk_events:
            category_events[r.category].append(r.risk_score)

        category_scores = {}
        for cat in RiskCategory:
            scores = category_events.get(cat.value, [])
            avg_score = (sum(scores) / len(scores)) if scores else 0.05
            category_scores[cat.value] = round(avg_score, 4)

        overall_score = (sum(category_scores.values()) / len(category_scores)) if category_scores else 0.0

        if overall_score >= 0.7:
            level = "CRITICAL"
        elif overall_score >= 0.5:
            level = "HIGH"
        elif overall_score >= 0.25:
            level = "MEDIUM"
        else:
            level = "LOW"

        crit_count = sum(1 for r in risk_events if r.severity in {"CRITICAL", "HIGH"} or r.risk_score >= 0.75)

        # Entity risk aggregation
        entity_scores: Dict[str, List[float]] = collections.defaultdict(list)
        for r in risk_events:
            entity_scores[r.entity_id].append(r.risk_score)

        top_entities = [
            {"entity_id": eid, "avg_risk": round(sum(scores) / len(scores), 4), "events_count": len(scores)}
            for eid, scores in entity_scores.items()
        ]
        top_entities.sort(key=lambda x: x["avg_risk"], reverse=True)

        # Anomaly detection
        anomalies = []
        if crit_count > 5:
            anomalies.append(f"Elevated frequency of high/critical risk events ({crit_count} detected)")
        for eid, item in entity_scores.items():
            if len(item) >= 3 and (sum(item) / len(item)) > 0.8:
                anomalies.append(f"Entity '{eid}' exhibiting persistent critical risk score ({sum(item)/len(item):.2f})")

        return RiskAnalysisSummary(
            tenant_id=tenant_id,
            overall_risk_score=round(overall_score, 4),
            enterprise_risk_level=level,
            category_scores=category_scores,
            critical_risk_events_count=crit_count,
            top_risk_entities=top_entities[:5],
            risk_anomalies_detected=anomalies,
        )
