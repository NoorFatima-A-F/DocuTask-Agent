"""Investigation Case Domain Models & Lifecycle Workflow Engine."""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid


class CaseLifecycleState(str, Enum):
    OPEN = "OPEN"
    TRIAGED = "TRIAGED"
    INVESTIGATING = "INVESTIGATING"
    EVIDENCE_COLLECTED = "EVIDENCE_COLLECTED"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class InvestigationCaseNote(BaseModel):
    note_id: str = Field(default_factory=lambda: f"not_{uuid.uuid4().hex[:8]}")
    author: str
    text: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class InvestigationCase(BaseModel):
    case_id: str = Field(default_factory=lambda: f"case_{uuid.uuid4().hex[:10]}")
    tenant_id: str
    title: str
    summary: str
    state: CaseLifecycleState = CaseLifecycleState.OPEN
    severity: str = "HIGH"
    assigned_to: Optional[str] = None
    attached_event_ids: List[str] = Field(default_factory=list)
    attached_evidence_ids: List[str] = Field(default_factory=list)
    notes: List[InvestigationCaseNote] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class InvestigationManager:
    """Manages creation, state machine transitions, and evidence attachments for investigation cases."""

    VALID_TRANSITIONS: Dict[CaseLifecycleState, List[CaseLifecycleState]] = {
        CaseLifecycleState.OPEN: [CaseLifecycleState.TRIAGED, CaseLifecycleState.CLOSED],
        CaseLifecycleState.TRIAGED: [CaseLifecycleState.INVESTIGATING, CaseLifecycleState.CLOSED],
        CaseLifecycleState.INVESTIGATING: [CaseLifecycleState.EVIDENCE_COLLECTED, CaseLifecycleState.RESOLVED, CaseLifecycleState.CLOSED],
        CaseLifecycleState.EVIDENCE_COLLECTED: [CaseLifecycleState.RESOLVED, CaseLifecycleState.INVESTIGATING],
        CaseLifecycleState.RESOLVED: [CaseLifecycleState.CLOSED, CaseLifecycleState.INVESTIGATING],
        CaseLifecycleState.CLOSED: [],
    }

    def __init__(self):
        self._cases: Dict[str, InvestigationCase] = {}

    def create_case(
        self,
        tenant_id: str,
        title: str,
        summary: str,
        severity: str = "HIGH",
        assigned_to: Optional[str] = None,
        event_ids: Optional[List[str]] = None,
        evidence_ids: Optional[List[str]] = None,
    ) -> InvestigationCase:
        case = InvestigationCase(
            tenant_id=tenant_id,
            title=title,
            summary=summary,
            severity=severity,
            assigned_to=assigned_to,
            attached_event_ids=event_ids or [],
            attached_evidence_ids=evidence_ids or [],
        )
        self._cases[case.case_id] = case
        return case

    def get_case(self, case_id: str, tenant_id: Optional[str] = None) -> Optional[InvestigationCase]:
        case = self._cases.get(case_id)
        if not case:
            return None
        if tenant_id and case.tenant_id != tenant_id:
            return None
        return case

    def list_cases(
        self,
        tenant_id: str,
        state: Optional[CaseLifecycleState] = None,
    ) -> List[InvestigationCase]:
        results = [c for c in self._cases.values() if c.tenant_id == tenant_id]
        if state:
            results = [c for c in results if c.state == state]
        return results

    def transition_state(
        self,
        case_id: str,
        new_state: CaseLifecycleState,
        actor: str,
        notes: Optional[str] = None,
        tenant_id: Optional[str] = None,
    ) -> InvestigationCase:
        case = self.get_case(case_id, tenant_id)
        if not case:
            raise ValueError(f"Investigation case '{case_id}' not found")

        current = case.state
        if new_state not in self.VALID_TRANSITIONS.get(current, []):
            raise ValueError(f"Invalid transition from {current.value} to {new_state.value}")

        case.state = new_state
        case.updated_at = datetime.now(timezone.utc)
        if new_state in [CaseLifecycleState.RESOLVED, CaseLifecycleState.CLOSED]:
            case.resolved_at = datetime.now(timezone.utc)

        if notes:
            case.notes.append(
                InvestigationCaseNote(
                    author=actor,
                    text=f"Transition to {new_state.value}: {notes}",
                )
            )

        return case

    def attach_event(self, case_id: str, event_id: str, tenant_id: Optional[str] = None) -> InvestigationCase:
        case = self.get_case(case_id, tenant_id)
        if not case:
            raise ValueError(f"Case '{case_id}' not found")
        if event_id not in case.attached_event_ids:
            case.attached_event_ids.append(event_id)
            case.updated_at = datetime.now(timezone.utc)
        return case

    def attach_evidence(self, case_id: str, evidence_id: str, tenant_id: Optional[str] = None) -> InvestigationCase:
        case = self.get_case(case_id, tenant_id)
        if not case:
            raise ValueError(f"Case '{case_id}' not found")
        if evidence_id not in case.attached_evidence_ids:
            case.attached_evidence_ids.append(evidence_id)
            case.updated_at = datetime.now(timezone.utc)
        return case

    def add_note(self, case_id: str, author: str, text: str, tenant_id: Optional[str] = None) -> InvestigationCase:
        case = self.get_case(case_id, tenant_id)
        if not case:
            raise ValueError(f"Case '{case_id}' not found")
        case.notes.append(InvestigationCaseNote(author=author, text=text))
        case.updated_at = datetime.now(timezone.utc)
        return case
