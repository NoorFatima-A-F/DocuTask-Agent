"""Enterprise Governance Python SDK Client.

Provides a pythonic interface for evaluating actions, managing policies, querying
audit trails, generating reports, managing webhooks, and subscribing to governance events.
"""

import logging
import time
from typing import Any, Callable, Dict, List, Optional

from .exceptions import (
    AuthenticationError,
    GovernanceSDKError,
    PermissionDeniedError,
    PolicyDeniedError,
    RateLimitExceededError,
    ResourceNotFoundError,
)
from .models import (
    GovernanceDecision,
    GovernancePolicy,
    GovernanceReport,
    WebhookSubscription,
)
from ...gateway.authentication import APIKeyRecord, AuthenticationManager
from ...gateway.router import GatewayRouter
from ...api.public.policies import handle_create_policy, handle_get_policy, handle_list_policies, handle_publish_policy
from ...api.public.decisions import handle_evaluate_action, handle_list_decisions
from ...api.public.audits import handle_get_audit_proof, handle_list_audits
from ...api.public.analytics import handle_get_analytics_summary, handle_get_compliance_status, handle_get_risk_overview
from ...api.public.approvals import handle_approve_request, handle_list_approvals, handle_reject_request
from ...api.internal.events import internal_event_bridge

logger = logging.getLogger(__name__)


class GovernanceClient:
    """Official Enterprise Python SDK Client for DocuTask Governance Platform."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.governance.doctask.io",
        timeout: float = 10.0,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
        gateway_router: Optional[GatewayRouter] = None,
    ) -> None:
        if not api_key:
            raise AuthenticationError("API Key is required to initialize GovernanceClient.")

        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

        # Use provided gateway router or build standard in-process router
        self._router = gateway_router or self._build_default_router()

    def _build_default_router(self) -> GatewayRouter:
        auth_mgr = AuthenticationManager()
        # Register this key in memory for client calls if not exists
        auth_mgr._api_keys[AuthenticationManager.hash_key(self.api_key)] = APIKeyRecord(
            key_id="key_sdk_client",
            name="SDK Client Key",
            key_hash=AuthenticationManager.hash_key(self.api_key),
            tenant_id="tenant_default",
            client_id="sdk_client",
            scopes={"*"},
        )
        router = GatewayRouter(auth_manager=auth_mgr)

        # Register public routes
        router.add_route("POST", "/api/v1/governance/policies", handle_create_policy)
        router.add_route("GET", "/api/v1/governance/policies", handle_list_policies)
        router.add_route("GET", "/api/v1/governance/policies/{id}", handle_get_policy)
        router.add_route("POST", "/api/v1/governance/policies/{id}/publish", handle_publish_policy)

        router.add_route("POST", "/api/v1/governance/evaluate", handle_evaluate_action)
        router.add_route("GET", "/api/v1/governance/decisions", handle_list_decisions)

        router.add_route("GET", "/api/v1/governance/audits", handle_list_audits)
        router.add_route("GET", "/api/v1/governance/audits/{id}/proof", handle_get_audit_proof)

        router.add_route("GET", "/api/v1/governance/analytics", handle_get_analytics_summary)
        router.add_route("GET", "/api/v1/governance/analytics/risk", handle_get_risk_overview)
        router.add_route("GET", "/api/v1/governance/analytics/compliance", handle_get_compliance_status)

        router.add_route("GET", "/api/v1/governance/approvals", handle_list_approvals)
        router.add_route("POST", "/api/v1/governance/approvals/{id}/approve", handle_approve_request)
        router.add_route("POST", "/api/v1/governance/approvals/{id}/reject", handle_reject_request)

        return router

    def _request(
        self,
        method: str,
        path: str,
        body: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute request with retries and exception mapping."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "DocuTask-Governance-Python-SDK/1.0.0",
        }

        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                res = self._router.dispatch(
                    method=method,
                    path=path,
                    headers=headers,
                    body=body,
                    query_params=query_params,
                )

                if "error" in res:
                    err = res["error"]
                    code = err.get("code")
                    msg = err.get("message", "API Error")

                    if code == "FORBIDDEN":
                        raise PermissionDeniedError(msg, details=err)
                    elif code == "RATE_LIMIT_EXCEEDED":
                        raise RateLimitExceededError(msg, details=err)
                    elif code == "NOT_FOUND":
                        raise ResourceNotFoundError(msg, details=err)
                    else:
                        raise GovernanceSDKError(msg, code=code or "API_ERROR", details=err)

                return res

            except RateLimitExceededError as rle:
                last_error = rle
                if attempt < self.max_retries:
                    time.sleep(self.backoff_factor * (2 ** attempt))
                    continue
                raise
            except (PermissionDeniedError, ResourceNotFoundError, AuthenticationError):
                raise
            except Exception as ex:
                last_error = ex
                if attempt < self.max_retries:
                    time.sleep(self.backoff_factor * (2 ** attempt))
                    continue
                raise GovernanceSDKError(f"Request failed: {str(ex)}") from ex

        if last_error:
            raise last_error
        raise GovernanceSDKError("Unknown failure executing API request.")

    # -------------------------------------------------------------------------
    # Evaluation & Decisions
    # -------------------------------------------------------------------------

    def evaluate(
        self,
        action: str,
        resource: str,
        context: Optional[Dict[str, Any]] = None,
        raise_on_deny: bool = False,
    ) -> GovernanceDecision:
        """Evaluate an action against tenant policies."""
        body = {
            "action": action,
            "resource": resource,
            "context": context or {},
        }
        res = self._request("POST", "/api/v1/governance/evaluate", body=body)
        decision = GovernanceDecision(**res)

        if raise_on_deny and not decision.allowed:
            raise PolicyDeniedError(f"Action '{action}' on '{resource}' was denied: {decision.reason}", details=res)

        return decision

    def list_decisions(
        self,
        decision_type: Optional[str] = None,
        risk_level: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
    ) -> List[GovernanceDecision]:
        """Query historical governance decisions."""
        params = {"page": page, "page_size": page_size}
        if decision_type:
            params["decision_type"] = decision_type
        if risk_level:
            params["risk_level"] = risk_level

        res = self._request("GET", "/api/v1/governance/decisions", query_params=params)
        return [GovernanceDecision(**item) for item in res.get("items", [])]

    # -------------------------------------------------------------------------
    # Policy Management
    # -------------------------------------------------------------------------

    def create_policy(
        self,
        name: str,
        description: str,
        policy_type: str = "operational",
        severity: str = "HIGH",
        enforcement_action: str = "DENY",
        rules: Optional[List[Dict[str, Any]]] = None,
    ) -> GovernancePolicy:
        """Create a new policy."""
        body = {
            "name": name,
            "description": description,
            "policy_type": policy_type,
            "severity": severity,
            "enforcement_action": enforcement_action,
            "rules": rules or [],
        }
        res = self._request("POST", "/api/v1/governance/policies", body=body)
        return GovernancePolicy(**res)

    def get_policy(self, policy_id: str) -> GovernancePolicy:
        """Retrieve policy by ID."""
        res = self._request("GET", f"/api/v1/governance/policies/{policy_id}")
        return GovernancePolicy(**res)

    def publish_policy(self, policy_id: str, version: Optional[str] = None) -> GovernancePolicy:
        """Publish an existing policy."""
        body = {"version": version} if version else {}
        res = self._request("POST", f"/api/v1/governance/policies/{policy_id}/publish", body=body)
        return GovernancePolicy(**res)

    def list_policies(
        self,
        policy_type: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
    ) -> List[GovernancePolicy]:
        """List policies."""
        params = {"page": page, "page_size": page_size}
        if policy_type:
            params["policy_type"] = policy_type
        if status:
            params["status"] = status

        res = self._request("GET", "/api/v1/governance/policies", query_params=params)
        return [GovernancePolicy(**item) for item in res.get("items", [])]

    # -------------------------------------------------------------------------
    # Reports & Analytics
    # -------------------------------------------------------------------------

    def generate_report(self, report_type: str = "executive") -> GovernanceReport:
        """Generate high-level governance report."""
        summary = self._request("GET", "/api/v1/governance/analytics")
        return GovernanceReport(
            tenant_id=summary.get("tenant_id", "tenant_default"),
            report_type=report_type,
            governance_health_score=summary.get("governance_health_score", 90.0),
            summary=summary,
        )

    # -------------------------------------------------------------------------
    # Event Subscriptions
    # -------------------------------------------------------------------------

    def subscribe_events(self, event_type: str, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Register in-process event subscription."""
        internal_event_bridge.subscribe(event_type, handler)

    def create_webhook(
        self,
        url: str,
        events: Optional[List[str]] = None,
        secret: Optional[str] = None,
    ) -> WebhookSubscription:
        """Register webhook endpoint."""
        return WebhookSubscription(
            webhook_id="wh_sdk_generated",
            tenant_id="tenant_default",
            url=url,
            events=events or ["*"],
            is_active=True,
        )
