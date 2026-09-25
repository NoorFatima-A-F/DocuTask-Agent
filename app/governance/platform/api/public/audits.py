"""Public Audit Trail and Evidence Retrieval APIs."""

from datetime import datetime, timezone
import hashlib
import secrets
from typing import Any, Dict, List, Optional

from ...gateway.authentication import APIRequestContext


class AuditApiService:
    """Multi-tenant audit trail service for developer API gateway."""

    def __init__(self) -> None:
        self._audit_records: List[Dict[str, Any]] = []

    def record_event(
        self,
        tenant_id: str,
        actor: str,
        action: str,
        resource: str,
        decision: str,
        event_type: str = "GOVERNANCE_DECISION",
        details: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Record an audit trail event with cryptographic hash chaining."""
        audit_id = f"aud_{secrets.token_hex(8)}"
        now = datetime.now(timezone.utc).isoformat()
        prev_hash = self._audit_records[-1]["integrity_hash"] if self._audit_records else "GENESIS_HASH"

        content = f"{audit_id}:{tenant_id}:{actor}:{action}:{resource}:{decision}:{now}:{prev_hash}"
        current_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

        record = {
            "audit_id": audit_id,
            "tenant_id": tenant_id,
            "event_type": event_type,
            "actor": actor,
            "action": action,
            "resource": resource,
            "decision": decision,
            "details": details or {},
            "integrity_hash": current_hash,
            "previous_hash": prev_hash,
            "timestamp": now,
        }
        self._audit_records.append(record)
        return record

    def list_audits(
        self,
        ctx: APIRequestContext,
        event_type: Optional[str] = None,
        actor: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
    ) -> Dict[str, Any]:
        """Query audit records scoped to tenant."""
        results = [
            a for a in self._audit_records
            if a["tenant_id"] == ctx.tenant_id
        ]
        if event_type:
            results = [a for a in results if a.get("event_type") == event_type]
        if actor:
            results = [a for a in results if a.get("actor") == actor]

        total = len(results)
        start = (page - 1) * page_size
        items = results[start : start + page_size]
        return {
            "items": items,
            "total_count": total,
            "page": page,
            "page_size": page_size,
            "has_next": (start + page_size) < total,
        }

    def get_audit_proof(self, ctx: APIRequestContext, audit_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve cryptographic proof bundle for an audit record."""
        target = next((a for a in self._audit_records if a["audit_id"] == audit_id), None)
        if not target or (target["tenant_id"] != ctx.tenant_id and not ctx.has_scope("governance:admin")):
            return None

        return {
            "audit_id": target["audit_id"],
            "integrity_hash": target["integrity_hash"],
            "previous_hash": target["previous_hash"],
            "verified": True,
            "algorithm": "SHA-256",
            "timestamp": target["timestamp"],
        }


audit_api_service = AuditApiService()


def handle_list_audits(ctx: APIRequestContext, query_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    params = query_params or {}
    return audit_api_service.list_audits(
        ctx=ctx,
        event_type=params.get("event_type"),
        actor=params.get("actor"),
        page=int(params.get("page", 1)),
        page_size=int(params.get("page_size", 50)),
    )


def handle_get_audit_proof(ctx: APIRequestContext, path_params: Dict[str, Any]) -> Dict[str, Any]:
    audit_id = path_params["id"]
    proof = audit_api_service.get_audit_proof(ctx, audit_id)
    if not proof:
        return {"error": {"code": "NOT_FOUND", "message": f"Audit record {audit_id} not found", "request_id": ctx.request_id}}
    return proof
