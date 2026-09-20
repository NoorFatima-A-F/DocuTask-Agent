"""FastAPI REST API Routes for Audit Ingestion, Search, Integrity, Compliance, and Investigations."""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from ..core.events import AuditEvent
from ..collector.gateway import AuditCollectorGateway
from ..storage.repository import AuditRepository
from ..integrity.verification import AuditIntegrityVerifier, IntegrityVerificationResult
from ..evidence.manager import EvidenceManager, EvidenceBundle
from ..evidence.artifacts import EvidenceArtifact
from ..compliance.mappings import ComplianceAssessmentEngine, ComplianceAssessmentReport
from ..search.engine import AuditSearchEngine, AuditSearchResult, ExecutionTimelineGraph
from ..search.filters import AuditSearchFilter
from ..investigations.cases import InvestigationManager, InvestigationCase
from ..investigations.timeline import InvestigationTimelineBuilder, InvestigationTimeline
from .schemas import (
    CreateEventRequest,
    VerifyIntegrityRequest,
    CreateArtifactRequest,
    CreateBundleRequest,
    EvaluateComplianceRequest,
    CreateInvestigationCaseRequest,
    TransitionCaseRequest,
)

router = APIRouter(prefix="/api/v1/audit", tags=["Enterprise Audit & Compliance Evidence Platform"])

# Shared singletons for control plane
audit_repository = AuditRepository()
audit_gateway = AuditCollectorGateway(repository=audit_repository)
audit_verifier = AuditIntegrityVerifier()
evidence_manager = EvidenceManager(repository=audit_repository)
compliance_engine = ComplianceAssessmentEngine(repository=audit_repository, evidence_manager=evidence_manager)
search_engine = AuditSearchEngine(repository=audit_repository)
investigation_manager = InvestigationManager()
timeline_builder = InvestigationTimelineBuilder(repository=audit_repository, evidence_manager=evidence_manager)


@router.post("/events", response_model=AuditEvent)
def record_event(request: CreateEventRequest):
    event = audit_gateway.record(request.model_dump())
    return event


@router.get("/events", response_model=AuditSearchResult)
def search_events(
    tenant_id: str = Query(...),
    event_type: Optional[str] = None,
    actor_id: Optional[str] = None,
    correlation_id: Optional[str] = None,
    query: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
):
    filt = AuditSearchFilter(
        tenant_id=tenant_id,
        event_type=event_type,
        actor_id=actor_id,
        correlation_id=correlation_id,
        query=query,
        limit=limit,
        offset=offset,
    )
    return search_engine.search(filt)


@router.get("/events/{event_id}", response_model=AuditEvent)
def get_event(event_id: str, tenant_id: Optional[str] = None):
    event = audit_repository.get_by_id(event_id, tenant_id=tenant_id)
    if not event:
        raise HTTPException(status_code=404, detail=f"Audit event '{event_id}' not found")
    return event


@router.post("/verify", response_model=IntegrityVerificationResult)
def verify_integrity(request: VerifyIntegrityRequest):
    events = audit_repository.list_by_tenant(request.tenant_id)
    return audit_verifier.verify_chain(events)


@router.get("/timeline/{correlation_id}", response_model=ExecutionTimelineGraph)
def get_timeline(correlation_id: str, tenant_id: str = Query(...)):
    return search_engine.reconstruct_timeline(correlation_id, tenant_id=tenant_id)


@router.post("/evidence/artifacts", response_model=EvidenceArtifact)
def create_artifact(request: CreateArtifactRequest):
    return evidence_manager.create_artifact(
        tenant_id=request.tenant_id,
        name=request.name,
        evidence_type=request.evidence_type,
        source=request.source,
        content=request.content,
        related_event_ids=request.related_event_ids,
        classification=request.classification,
    )


@router.post("/evidence/bundle", response_model=EvidenceBundle)
def create_evidence_bundle(request: CreateBundleRequest):
    return evidence_manager.create_evidence_bundle(
        tenant_id=request.tenant_id,
        title=request.title,
        purpose=request.purpose,
        generated_by=request.generated_by,
        correlation_id=request.correlation_id,
        event_ids=request.event_ids,
        artifact_ids=request.artifact_ids,
    )


@router.post("/compliance/evaluate", response_model=ComplianceAssessmentReport)
def evaluate_compliance(request: EvaluateComplianceRequest):
    return compliance_engine.evaluate_compliance(request.tenant_id, request.framework)


@router.post("/investigations", response_model=InvestigationCase)
def create_investigation_case(request: CreateInvestigationCaseRequest):
    return investigation_manager.create_case(
        tenant_id=request.tenant_id,
        title=request.title,
        summary=request.summary,
        severity=request.severity,
        assigned_to=request.assigned_to,
        event_ids=request.event_ids,
        evidence_ids=request.evidence_ids,
    )


@router.get("/investigations", response_model=List[InvestigationCase])
def list_investigations(tenant_id: str = Query(...)):
    return investigation_manager.list_cases(tenant_id=tenant_id)


@router.get("/investigations/{case_id}/timeline", response_model=InvestigationTimeline)
def get_investigation_timeline(case_id: str, tenant_id: str = Query(...)):
    case = investigation_manager.get_case(case_id, tenant_id=tenant_id)
    if not case:
        raise HTTPException(status_code=404, detail="Investigation case not found")
    return timeline_builder.build_timeline(case)
