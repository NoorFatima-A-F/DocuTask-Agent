"""Retention Lifecycle Manager & Legal Hold Enforcement."""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field
import uuid
from ..core.events import AuditEvent
from ..storage.repository import AuditRepository
from .policies import RetentionPolicy, RetentionAction


class LegalHold(BaseModel):
    hold_id: str = Field(default_factory=lambda: f"hold_{uuid.uuid4().hex[:8]}")
    tenant_id: str
    case_id: Optional[str] = None
    reason: str
    applied_by: str
    applied_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True
    event_ids: List[str] = Field(default_factory=list)  # Empty means all tenant events locked


class RetentionEvaluationResult(BaseModel):
    tenant_id: str
    total_events: int
    retained_events: int
    eligible_for_archive: List[str] = Field(default_factory=list)
    eligible_for_deletion: List[str] = Field(default_factory=list)
    locked_by_legal_hold: List[str] = Field(default_factory=list)


class RetentionLifecycleManager:
    """Evaluates retention lifecycle rules and enforces tamper-resistant legal hold locks."""

    def __init__(self, repository: Optional[AuditRepository] = None):
        self.repository = repository or AuditRepository()
        self._policies: Dict[str, RetentionPolicy] = {}
        self._legal_holds: Dict[str, LegalHold] = {}

    def add_policy(self, policy: RetentionPolicy) -> RetentionPolicy:
        self._policies[policy.policy_id] = policy
        return policy

    def apply_legal_hold(
        self,
        tenant_id: str,
        reason: str,
        applied_by: str,
        case_id: Optional[str] = None,
        event_ids: Optional[List[str]] = None,
    ) -> LegalHold:
        hold = LegalHold(
            tenant_id=tenant_id,
            case_id=case_id,
            reason=reason,
            applied_by=applied_by,
            event_ids=event_ids or [],
        )
        self._legal_holds[hold.hold_id] = hold
        return hold

    def release_legal_hold(self, hold_id: str) -> bool:
        if hold_id in self._legal_holds:
            self._legal_holds[hold_id].is_active = False
            return True
        return False

    def is_event_under_hold(self, event: AuditEvent) -> bool:
        for hold in self._legal_holds.values():
            if not hold.is_active or hold.tenant_id != event.tenant_id:
                continue
            if not hold.event_ids or event.event_id in hold.event_ids:
                return True
        return False

    def evaluate_retention(
        self,
        tenant_id: str,
        as_of_date: Optional[datetime] = None,
    ) -> RetentionEvaluationResult:
        now = as_of_date or datetime.now(timezone.utc)
        events = self.repository.list_by_tenant(tenant_id)
        tenant_policies = [p for p in self._policies.values() if p.tenant_id == tenant_id and p.is_active]

        # Default 365-day archive policy if no custom policy set
        if not tenant_policies:
            tenant_policies = [RetentionPolicy(tenant_id=tenant_id, name="Default Archive", action=RetentionAction.ARCHIVE, retention_days=365)]

        eligible_archive: List[str] = []
        eligible_delete: List[str] = []
        locked_hold: List[str] = []

        for ev in events:
            if self.is_event_under_hold(ev):
                locked_hold.append(ev.event_id)
                continue

            # Find matching policy
            age_days = (now - ev.timestamp).total_seconds() / 86400.0
            
            for pol in tenant_policies:
                if pol.action == RetentionAction.PERMANENT_RETENTION:
                    continue

                if age_days >= pol.retention_days:
                    if pol.action == RetentionAction.ARCHIVE:
                        eligible_archive.append(ev.event_id)
                    elif pol.action == RetentionAction.DELETE_AFTER_PERIOD:
                        eligible_delete.append(ev.event_id)
                    break

        retained = len(events) - len(eligible_delete)

        return RetentionEvaluationResult(
            tenant_id=tenant_id,
            total_events=len(events),
            retained_events=retained,
            eligible_for_archive=eligible_archive,
            eligible_for_deletion=eligible_delete,
            locked_by_legal_hold=locked_hold,
        )
