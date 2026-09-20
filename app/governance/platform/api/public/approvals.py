"""Public Human Oversight and Approval Management APIs."""

from datetime import datetime, timezone
import secrets
from typing import Any, Dict, List, Optional

from ..schemas.requests import ApprovalDecisionRequest
from ...gateway.authentication import APIRequestContext


class ApprovalApiService:
    """Multi-tenant approval queue management service."""

    def __init__(self) -> None:
        self._approvals: Dict[str, Dict[str, Any]] = {}

    def submit_for_review(
        self,
        tenant_id: str,
        action: str,
        resource: str,
        risk_level: str = "HIGH",
        reason: str = "Requires manual intervention",
    ) -> Dict[str, Any]:
        """Create a pending approval item."""
        req_id = f"appr_{secrets.token_hex(8)}"
        now = datetime.now(timezone.utc).isoformat()
        record = {
            "request_id": req_id,
            "tenant_id": tenant_id,
            "action": action,
            "resource": resource,
            "risk_level": risk_level,
            "reason": reason,
            "status": "PENDING",
            "requested_at": now,
            "reviewed_at": None,
            "reviewer_id": None,
            "decision": None,
            "comments": None,
        }
        self._approvals[req_id] = record
        return record

    def list_approvals(
        self,
        ctx: APIRequestContext,
        status: Optional[str] = None,
        risk_level: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
    ) -> Dict[str, Any]:
        """List review queue items scoped to tenant."""
        results = [
            a for a in self._approvals.values()
            if a["tenant_id"] == ctx.tenant_id
        ]
        if status:
            results = [a for a in results if a.get("status") == status.upper()]
        if risk_level:
            results = [a for a in results if a.get("risk_level") == risk_level.upper()]

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

    def resolve_approval(
        self,
        ctx: APIRequestContext,
        request_id: str,
        decision: str,
        reviewer_id: str,
        comments: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Record decision on pending review request."""
        record = self._approvals.get(request_id)
        if not record or (record["tenant_id"] != ctx.tenant_id and not ctx.has_scope("governance:admin")):
            return None

        record["status"] = decision.upper()
        record["decision"] = decision.upper()
        record["reviewer_id"] = reviewer_id
        record["reviewed_at"] = datetime.now(timezone.utc).isoformat()
        record["comments"] = comments
        return record


approval_api_service = ApprovalApiService()


def handle_list_approvals(ctx: APIRequestContext, query_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    params = query_params or {}
    return approval_api_service.list_approvals(
        ctx=ctx,
        status=params.get("status"),
        risk_level=params.get("risk_level"),
        page=int(params.get("page", 1)),
        page_size=int(params.get("page_size", 50)),
    )


def handle_approve_request(ctx: APIRequestContext, path_params: Dict[str, Any], body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    appr_id = path_params["id"]
    req = ApprovalDecisionRequest(**(body or {"reviewer_id": ctx.user_id or ctx.client_id}))
    res = approval_api_service.resolve_approval(
        ctx=ctx,
        request_id=appr_id,
        decision="APPROVED",
        reviewer_id=req.reviewer_id,
        comments=req.comments,
    )
    if not res:
        return {"error": {"code": "NOT_FOUND", "message": f"Approval request {appr_id} not found", "request_id": ctx.request_id}}
    return res


def handle_reject_request(ctx: APIRequestContext, path_params: Dict[str, Any], body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    appr_id = path_params["id"]
    req = ApprovalDecisionRequest(**(body or {"reviewer_id": ctx.user_id or ctx.client_id, "decision": "REJECTED"}))
    res = approval_api_service.resolve_approval(
        ctx=ctx,
        request_id=appr_id,
        decision="REJECTED",
        reviewer_id=req.reviewer_id,
        comments=req.comments,
    )
    if not res:
        return {"error": {"code": "NOT_FOUND", "message": f"Approval request {appr_id} not found", "request_id": ctx.request_id}}
    return res
