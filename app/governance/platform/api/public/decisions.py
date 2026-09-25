"""Public Decision Evaluation and History APIs."""

from datetime import datetime, timezone
import secrets
import time
from typing import Any, Dict, List, Optional

from ..schemas.requests import DecisionEvaluationRequest
from ...gateway.authentication import APIRequestContext
from .policies import policy_service


class DecisionService:
    """Core decision evaluation and history store."""

    def __init__(self) -> None:
        self._decision_history: List[Dict[str, Any]] = []

    def evaluate(self, ctx: APIRequestContext, request: DecisionEvaluationRequest) -> Dict[str, Any]:
        """Evaluate an action against tenant policies and safety constraints."""
        start_time = time.time()
        decision_id = f"dec_{secrets.token_hex(8)}"

        # Fetch active policies for tenant
        policies_list = policy_service.list_policies(ctx, status="ACTIVE", page_size=100)["items"]
        applied_policies = []
        is_allowed = True
        decision_str = "ALLOW"
        reason = "All governance policies satisfied."
        risk_level = "LOW"

        # Check explicit high risk in context
        req_risk = request.context.get("risk_level", "low").upper()
        if req_risk in ["CRITICAL", "HIGH"]:
            risk_level = req_risk

        # Apply active policies
        for p in policies_list:
            applied_policies.append(p["name"])
            # Example rule evaluation
            if request.action == "model.invoke" and request.resource == "unauthorized_model":
                is_allowed = False
                decision_str = "DENY"
                reason = f"Blocked by policy '{p['name']}': Unauthorized model access."
                risk_level = "HIGH"
                break
            elif req_risk == "CRITICAL" and p.get("enforcement_action") == "APPROVAL_REQUIRED":
                is_allowed = False
                decision_str = "APPROVAL_REQUIRED"
                reason = f"Policy '{p['name']}' requires human approval for high-risk action."
                break

        # If action is dangerous by default without authorization
        if "delete" in request.action.lower() and not ctx.has_scope("governance:admin"):
            is_allowed = False
            decision_str = "DENY"
            reason = "Deletion operations require governance:admin scope."
            risk_level = "CRITICAL"

        eval_ms = (time.time() - start_time) * 1000.0
        now = datetime.now(timezone.utc)

        record = {
            "decision_id": decision_id,
            "tenant_id": ctx.tenant_id,
            "client_id": ctx.client_id,
            "action": request.action,
            "resource": request.resource,
            "decision": decision_str,
            "allowed": is_allowed,
            "reason": reason,
            "policies_applied": applied_policies,
            "risk_level": risk_level,
            "evaluation_time_ms": round(eval_ms, 2),
            "timestamp": now.isoformat(),
        }

        self._decision_history.append(record)
        return record

    def list_decisions(
        self,
        ctx: APIRequestContext,
        decision_type: Optional[str] = None,
        risk_level: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
    ) -> Dict[str, Any]:
        """Query decision history for tenant."""
        results = [
            d for d in self._decision_history
            if d["tenant_id"] == ctx.tenant_id
        ]
        if decision_type:
            results = [d for d in results if d.get("decision") == decision_type.upper()]
        if risk_level:
            results = [d for d in results if d.get("risk_level") == risk_level.upper()]

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


# Singleton decision service instance
decision_service = DecisionService()


def handle_evaluate_action(ctx: APIRequestContext, body: Dict[str, Any]) -> Dict[str, Any]:
    req = DecisionEvaluationRequest(**body)
    return decision_service.evaluate(ctx, req)


def handle_list_decisions(ctx: APIRequestContext, query_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    params = query_params or {}
    return decision_service.list_decisions(
        ctx=ctx,
        decision_type=params.get("decision_type"),
        risk_level=params.get("risk_level"),
        page=int(params.get("page", 1)),
        page_size=int(params.get("page_size", 50)),
    )
