"""
Phase 13.19: Immutable Enterprise Audit Ledger & SOC2 Compliance Engine.
Maintains a cryptographic SHA-256 hash-chained audit log of all tenant, workspace, and user actions.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import uuid
import hashlib
from app.platform_saas.models.schemas import AuditEvent


class EnterpriseAuditService:
    def __init__(self):
        self._events: List[AuditEvent] = []
        self._last_hash_by_tenant: Dict[str, str] = {}
        self._seed_default_audit_log()

    def _seed_default_audit_log(self) -> None:
        self.log_event(
            tenant_id="tenant_acme_corp",
            actor_id="usr_acme_admin",
            actor_email="admin@acmecorp.com",
            action="TENANT_PROVISIONED",
            resource_type="TENANT",
            resource_id="tenant_acme_corp",
            ip_address="198.51.100.1",
        )
        self.log_event(
            tenant_id="tenant_acme_corp",
            actor_id="usr_acme_admin",
            actor_email="admin@acmecorp.com",
            action="SSO_CONFIGURED",
            resource_type="SSO_PROVIDER",
            resource_id="sso_okta_acme",
            ip_address="198.51.100.1",
        )
        self.log_event(
            tenant_id="tenant_globex_health",
            actor_id="usr_globex_lead",
            actor_email="compliance@globexhealth.com",
            action="DATA_RESIDENCY_POLICY_APPLIED",
            resource_type="POLICY",
            resource_id="pol_globex_eu_geofence",
            ip_address="195.176.255.10",
        )

    def log_event(
        self,
        tenant_id: str,
        actor_id: str,
        actor_email: str,
        action: str,
        resource_type: str,
        resource_id: str,
        organization_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        ip_address: str = "127.0.0.1",
    ) -> AuditEvent:
        audit_id = f"aud_{uuid.uuid4().hex[:8]}"
        prev_hash = self._last_hash_by_tenant.get(tenant_id, "00000000000000000000000000000000")
        ts = datetime.now(timezone.utc).isoformat()
        
        payload = f"{audit_id}:{tenant_id}:{actor_id}:{action}:{resource_type}:{resource_id}:{prev_hash}:{ts}"
        event_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()

        event = AuditEvent(
            audit_id=audit_id,
            tenant_id=tenant_id,
            organization_id=organization_id,
            workspace_id=workspace_id,
            actor_id=actor_id,
            actor_email=actor_email,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=ip_address,
            previous_hash=prev_hash,
            event_hash=event_hash,
            timestamp=ts,
        )
        self._events.append(event)
        self._last_hash_by_tenant[tenant_id] = event_hash
        return event

    def verify_integrity(self, tenant_id: str) -> Dict[str, Any]:
        """Verifies cryptographic hash chain integrity for the tenant audit trail."""
        events = [e for e in self._events if e.tenant_id == tenant_id]
        if not events:
            return {"valid": True, "count": 0, "status": "NO_EVENTS"}

        prev = "00000000000000000000000000000000"
        for idx, ev in enumerate(events):
            if ev.previous_hash != prev:
                return {
                    "valid": False,
                    "tampered_at_index": idx,
                    "event_id": ev.audit_id,
                    "status": "CHAIN_BROKEN",
                }
            payload = f"{ev.audit_id}:{ev.tenant_id}:{ev.actor_id}:{ev.action}:{ev.resource_type}:{ev.resource_id}:{ev.previous_hash}:{ev.timestamp}"
            expected_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
            if ev.event_hash != expected_hash:
                return {
                    "valid": False,
                    "tampered_at_index": idx,
                    "event_id": ev.audit_id,
                    "status": "HASH_CORRUPTED",
                }
            prev = ev.event_hash

        return {"valid": True, "verified_events_count": len(events), "status": "VERIFIED"}

    def list_events(self, tenant_id: Optional[str] = None) -> List[AuditEvent]:
        if tenant_id:
            return [e for e in self._events if e.tenant_id == tenant_id]
        return self._events
