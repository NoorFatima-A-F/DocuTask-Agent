"""Investigation Timeline Builder."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from ..storage.repository import AuditRepository
from ..evidence.manager import EvidenceManager
from .cases import InvestigationCase


class TimelineItem(BaseModel):
    timestamp: datetime
    item_type: str  # "EVENT" or "EVIDENCE"
    item_id: str
    title: str
    description: str
    actor: str
    outcome: Optional[str] = None
    severity: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class InvestigationTimeline(BaseModel):
    case_id: str
    tenant_id: str
    title: str
    total_items: int
    items: List[TimelineItem] = Field(default_factory=list)


class InvestigationTimelineBuilder:
    """Builds unified, chronological evidence and audit event timelines for investigation cases."""

    def __init__(
        self,
        repository: Optional[AuditRepository] = None,
        evidence_manager: Optional[EvidenceManager] = None,
    ):
        self.repository = repository or AuditRepository()
        self.evidence_manager = evidence_manager or EvidenceManager(self.repository)

    def build_timeline(self, case: InvestigationCase) -> InvestigationTimeline:
        timeline_items: List[TimelineItem] = []

        # 1. Fetch attached audit events
        for eid in case.attached_event_ids:
            ev = self.repository.get_by_id(eid, tenant_id=case.tenant_id)
            if ev:
                timeline_items.append(
                    TimelineItem(
                        timestamp=ev.timestamp,
                        item_type="EVENT",
                        item_id=ev.event_id,
                        title=f"Event: {ev.event_type} ({ev.action})",
                        description=ev.payload_summary or f"Action on {ev.resource_type}:{ev.resource_id}",
                        actor=f"{ev.actor_id} ({ev.actor_type.value if hasattr(ev.actor_type, 'value') else ev.actor_type})",
                        outcome=ev.outcome.value if hasattr(ev.outcome, "value") else str(ev.outcome),
                        severity=ev.severity.value if hasattr(ev.severity, "value") else str(ev.severity),
                        metadata={"risk_score": ev.risk_score, "correlation_id": ev.correlation_id},
                    )
                )

        # 2. Fetch attached evidence artifacts
        for aid in case.attached_evidence_ids:
            art = self.evidence_manager.get_artifact(aid, tenant_id=case.tenant_id)
            if art:
                timeline_items.append(
                    TimelineItem(
                        timestamp=art.created_at,
                        item_type="EVIDENCE",
                        item_id=art.evidence_id,
                        title=f"Evidence: {art.name} ({art.evidence_type.value})",
                        description=f"Source: {art.source} (Hash: {art.content_hash[:16]}...)",
                        actor=art.owner,
                        metadata={"classification": art.classification},
                    )
                )

        # Sort chronologically
        timeline_items.sort(key=lambda item: item.timestamp)

        return InvestigationTimeline(
            case_id=case.case_id,
            tenant_id=case.tenant_id,
            title=case.title,
            total_items=len(timeline_items),
            items=timeline_items,
        )
