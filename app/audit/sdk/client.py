"""Audit Developer SDK & Automated @audited Function Decorator."""

import functools
import inspect
import time
from typing import Optional, Dict, Any, Callable
from ..core.events import AuditEvent, ActorType, AuditSeverity, OutcomeType, EventCategory
from ..collector.gateway import AuditCollectorGateway
from ..storage.repository import AuditRepository
from ..integrity.verification import AuditIntegrityVerifier, IntegrityVerificationResult
from ..evidence.manager import EvidenceManager, EvidenceBundle
from ..compliance.mappings import ComplianceAssessmentEngine, ComplianceAssessmentReport
from ..compliance.frameworks import ComplianceFramework
from ..search.engine import AuditSearchEngine, AuditSearchResult
from ..search.filters import AuditSearchFilter


class AuditSDK:
    """Developer SDK client providing unified audit recording, compliance assessment, and integrity verification."""

    def __init__(
        self,
        gateway: Optional[AuditCollectorGateway] = None,
        repository: Optional[AuditRepository] = None,
    ):
        self.repository = repository or (gateway.repository if gateway else AuditRepository())
        self.gateway = gateway or AuditCollectorGateway(repository=self.repository)
        self.verifier = AuditIntegrityVerifier()
        self.evidence_manager = EvidenceManager(self.repository)
        self.compliance_engine = ComplianceAssessmentEngine(self.repository, self.evidence_manager)
        self.search_engine = AuditSearchEngine(self.repository)

    def record(
        self,
        action: str,
        resource_type: str,
        resource_id: str,
        tenant_id: str = "default",
        actor_id: str = "system",
        actor_type: ActorType = ActorType.SYSTEM,
        event_type: Optional[str] = None,
        category: EventCategory = EventCategory.SYSTEM,
        severity: AuditSeverity = AuditSeverity.INFO,
        outcome: OutcomeType = OutcomeType.SUCCESS,
        risk_score: float = 0.0,
        correlation_id: Optional[str] = None,
        request_id: Optional[str] = None,
        workflow_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        duration_ms: Optional[float] = None,
        payload_summary: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> AuditEvent:
        event = AuditEvent(
            event_type=event_type or f"{resource_type}.{action}",
            category=category,
            tenant_id=tenant_id,
            actor_id=actor_id,
            actor_type=actor_type,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            severity=severity,
            outcome=outcome,
            risk_score=risk_score,
            correlation_id=correlation_id,
            request_id=request_id,
            workflow_id=workflow_id,
            agent_id=agent_id,
            duration_ms=duration_ms,
            payload_summary=payload_summary,
            metadata=metadata or {},
        )
        return self.gateway.record(event)

    def verify_integrity(self, tenant_id: str) -> IntegrityVerificationResult:
        events = self.repository.list_by_tenant(tenant_id)
        return self.verifier.verify_chain(events)

    def evaluate_compliance(self, tenant_id: str, framework: ComplianceFramework) -> ComplianceAssessmentReport:
        return self.compliance_engine.evaluate_compliance(tenant_id, framework)

    def search(self, search_filter: AuditSearchFilter) -> AuditSearchResult:
        return self.search_engine.search(search_filter)

    def create_evidence_bundle(
        self,
        tenant_id: str,
        title: str,
        purpose: str,
        correlation_id: Optional[str] = None,
    ) -> EvidenceBundle:
        return self.evidence_manager.create_evidence_bundle(
            tenant_id=tenant_id,
            title=title,
            purpose=purpose,
            correlation_id=correlation_id,
        )


def audited(
    action: str,
    resource_type: str = "function",
    tenant_id: str = "default",
    category: EventCategory = EventCategory.SYSTEM,
    severity: AuditSeverity = AuditSeverity.INFO,
    sdk: Optional[AuditSDK] = None,
):
    """Decorator that automatically captures function start, completion, failure, duration, and error details."""
    audit_client = sdk or AuditSDK()

    def decorator(func: Callable):
        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                start_time = time.perf_counter()
                resource_id = func.__name__
                try:
                    result = await func(*args, **kwargs)
                    duration_ms = (time.perf_counter() - start_time) * 1000.0
                    audit_client.record(
                        action=action,
                        resource_type=resource_type,
                        resource_id=resource_id,
                        tenant_id=tenant_id,
                        category=category,
                        severity=severity,
                        outcome=OutcomeType.SUCCESS,
                        duration_ms=round(duration_ms, 2),
                    )
                    return result
                except Exception as ex:
                    duration_ms = (time.perf_counter() - start_time) * 1000.0
                    audit_client.record(
                        action=action,
                        resource_type=resource_type,
                        resource_id=resource_id,
                        tenant_id=tenant_id,
                        category=category,
                        severity=AuditSeverity.HIGH,
                        outcome=OutcomeType.ERROR,
                        duration_ms=round(duration_ms, 2),
                        metadata={"error": str(ex), "error_type": type(ex).__name__},
                    )
                    raise
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                start_time = time.perf_counter()
                resource_id = func.__name__
                try:
                    result = func(*args, **kwargs)
                    duration_ms = (time.perf_counter() - start_time) * 1000.0
                    audit_client.record(
                        action=action,
                        resource_type=resource_type,
                        resource_id=resource_id,
                        tenant_id=tenant_id,
                        category=category,
                        severity=severity,
                        outcome=OutcomeType.SUCCESS,
                        duration_ms=round(duration_ms, 2),
                    )
                    return result
                except Exception as ex:
                    duration_ms = (time.perf_counter() - start_time) * 1000.0
                    audit_client.record(
                        action=action,
                        resource_type=resource_type,
                        resource_id=resource_id,
                        tenant_id=tenant_id,
                        category=category,
                        severity=AuditSeverity.HIGH,
                        outcome=OutcomeType.ERROR,
                        duration_ms=round(duration_ms, 2),
                        metadata={"error": str(ex), "error_type": type(ex).__name__},
                    )
                    raise
            return sync_wrapper
    return decorator
