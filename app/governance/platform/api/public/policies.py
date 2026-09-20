"""Public Policy Management APIs."""

from datetime import datetime, timezone
import secrets
from typing import Any, Dict, List, Optional

from ..schemas.requests import PolicyCreateRequest, PolicyPublishRequest
from ..schemas.responses import PaginatedResponse, PolicyResponse
from ...gateway.authentication import APIRequestContext


class PolicyService:
    """In-memory multi-tenant policy repository and manager."""

    def __init__(self) -> None:
        self._policies: Dict[str, Dict[str, Any]] = {}

    def create_policy(self, ctx: APIRequestContext, request: PolicyCreateRequest) -> Dict[str, Any]:
        """Create a new policy in draft state for the calling tenant."""
        policy_id = f"pol_{secrets.token_hex(8)}"
        now = datetime.now(timezone.utc)
        record = {
            "policy_id": policy_id,
            "tenant_id": ctx.tenant_id,
            "name": request.name,
            "description": request.description,
            "policy_type": request.policy_type,
            "severity": request.severity,
            "rules": request.rules,
            "enforcement_action": request.enforcement_action,
            "status": "DRAFT",
            "version": "1.0.0",
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
        }
        self._policies[policy_id] = record
        return record

    def list_policies(
        self,
        ctx: APIRequestContext,
        policy_type: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
    ) -> Dict[str, Any]:
        """List policies scoped to tenant."""
        results = [
            p for p in self._policies.values()
            if p["tenant_id"] == ctx.tenant_id
        ]
        if policy_type:
            results = [p for p in results if p.get("policy_type") == policy_type]
        if status:
            results = [p for p in results if p.get("status") == status]

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

    def get_policy(self, ctx: APIRequestContext, policy_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve policy ensuring tenant boundary."""
        policy = self._policies.get(policy_id)
        if not policy or (policy["tenant_id"] != ctx.tenant_id and not ctx.has_scope("governance:admin")):
            return None
        return policy

    def publish_policy(self, ctx: APIRequestContext, policy_id: str, request: PolicyPublishRequest) -> Optional[Dict[str, Any]]:
        """Publish a policy, making it active."""
        policy = self.get_policy(ctx, policy_id)
        if not policy:
            return None
        policy["status"] = "ACTIVE"
        if request.version:
            policy["version"] = request.version
        policy["updated_at"] = datetime.now(timezone.utc).isoformat()
        return policy


# Singleton service instance
policy_service = PolicyService()


def handle_create_policy(ctx: APIRequestContext, body: Dict[str, Any]) -> Dict[str, Any]:
    req = PolicyCreateRequest(**body)
    return policy_service.create_policy(ctx, req)


def handle_list_policies(ctx: APIRequestContext, query_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    params = query_params or {}
    return policy_service.list_policies(
        ctx=ctx,
        policy_type=params.get("policy_type"),
        status=params.get("status"),
        page=int(params.get("page", 1)),
        page_size=int(params.get("page_size", 50)),
    )


def handle_get_policy(ctx: APIRequestContext, path_params: Dict[str, Any]) -> Dict[str, Any]:
    policy_id = path_params["id"]
    res = policy_service.get_policy(ctx, policy_id)
    if not res:
        return {"error": {"code": "NOT_FOUND", "message": f"Policy {policy_id} not found", "request_id": ctx.request_id}}
    return res


def handle_publish_policy(ctx: APIRequestContext, path_params: Dict[str, Any], body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    policy_id = path_params["id"]
    req = PolicyPublishRequest(**(body or {}))
    res = policy_service.publish_policy(ctx, policy_id, req)
    if not res:
        return {"error": {"code": "NOT_FOUND", "message": f"Policy {policy_id} not found", "request_id": ctx.request_id}}
    return res
