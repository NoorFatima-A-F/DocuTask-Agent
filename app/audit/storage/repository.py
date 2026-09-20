"""Audit Repository Interface with Multi-Key Indexing."""

from typing import List, Optional, Dict, Any
from ..core.events import AuditEvent
from .immutable_store import ImmutableAuditStore


class AuditRepository:
    """Repository handling indexing, lookups, and queries over the immutable audit store."""

    def __init__(self, store: Optional[ImmutableAuditStore] = None):
        self.store = store or ImmutableAuditStore()

    def record(self, event: AuditEvent) -> AuditEvent:
        return self.store.append(event)

    def get_by_id(self, event_id: str, tenant_id: Optional[str] = None) -> Optional[AuditEvent]:
        event = self.store.get_event(event_id)
        if not event:
            return None
        if tenant_id and event.tenant_id != tenant_id:
            return None
        return event

    def list_by_tenant(self, tenant_id: str) -> List[AuditEvent]:
        return self.store.get_tenant_events(tenant_id)

    def find_by_correlation(self, correlation_id: str, tenant_id: Optional[str] = None) -> List[AuditEvent]:
        results: List[AuditEvent] = []
        for event in self.store._event_index.values():
            if tenant_id and event.tenant_id != tenant_id:
                continue
            if event.correlation_id == correlation_id:
                results.append(event)
        return results

    def find_by_request(self, request_id: str, tenant_id: Optional[str] = None) -> List[AuditEvent]:
        results: List[AuditEvent] = []
        for event in self.store._event_index.values():
            if tenant_id and event.tenant_id != tenant_id:
                continue
            if event.request_id == request_id:
                results.append(event)
        return results

    def find_by_resource(self, resource_type: str, resource_id: str, tenant_id: Optional[str] = None) -> List[AuditEvent]:
        results: List[AuditEvent] = []
        for event in self.store._event_index.values():
            if tenant_id and event.tenant_id != tenant_id:
                continue
            if event.resource_type == resource_type and event.resource_id == resource_id:
                results.append(event)
        return results
