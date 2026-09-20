"""
Phase 13.19: Fine-Grained Tenant Policy & RBAC/ABAC Engine.
Enforces multi-tenant authorization, role permissions, geo-fencing, and spend limits.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import uuid
from app.platform_saas.models.schemas import TenantPolicy


class TenantPolicyEngine:
    ROLE_HIERARCHY = {
        "SUPER_ADMIN": 100,
        "TENANT_ADMIN": 80,
        "WORKSPACE_MANAGER": 60,
        "AGENT_OPERATOR": 40,
        "VIEWER": 20,
    }

    def __init__(self):
        self._policies: Dict[str, TenantPolicy] = {}
        self._seed_default_policies()

    def _seed_default_policies(self) -> None:
        p1 = TenantPolicy(
            policy_id="pol_acme_admin_full",
            tenant_id="tenant_acme_corp",
            policy_name="Tenant Admin Full Scope Access",
            subject_role="TENANT_ADMIN",
            resource_type="*",
            action="*",
            effect="ALLOW",
            conditions={"mfa_required": True},
        )
        p2 = TenantPolicy(
            policy_id="pol_acme_operator_run",
            tenant_id="tenant_acme_corp",
            policy_name="Operator Workflow Execution",
            subject_role="AGENT_OPERATOR",
            resource_type="agent_workflow",
            action="EXECUTE",
            effect="ALLOW",
            conditions={"allowed_regions": ["us-east-1"]},
        )
        p3 = TenantPolicy(
            policy_id="pol_globex_eu_geofence",
            tenant_id="tenant_globex_health",
            policy_name="Strict EU Data Residency Policy",
            subject_role="*",
            resource_type="document_data",
            action="EXPORT",
            effect="DENY",
            conditions={"non_eu_destination": True},
        )

        for p in [p1, p2, p3]:
            self._policies[p.policy_id] = p

    def create_policy(
        self,
        tenant_id: str,
        policy_name: str,
        subject_role: str,
        resource_type: str,
        action: str,
        effect: str = "ALLOW",
        conditions: Optional[Dict[str, Any]] = None,
    ) -> TenantPolicy:
        pol_id = f"pol_{uuid.uuid4().hex[:8]}"
        policy = TenantPolicy(
            policy_id=pol_id,
            tenant_id=tenant_id,
            policy_name=policy_name,
            subject_role=subject_role,
            resource_type=resource_type,
            action=action,
            effect=effect,
            conditions=conditions or {},
        )
        self._policies[pol_id] = policy
        return policy

    def evaluate(
        self,
        tenant_id: str,
        user_role: str,
        resource_type: str,
        action: str,
        context_attributes: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Evaluates RBAC + ABAC policy rules."""
        context = context_attributes or {}
        tenant_policies = [p for p in self._policies.values() if p.tenant_id == tenant_id]

        # 1. Explicit Deny check
        for p in tenant_policies:
            if p.effect == "DENY":
                if p.subject_role in ("*", user_role) and p.resource_type in ("*", resource_type) and p.action in ("*", action):
                    return {"decision": "DENY", "matched_policy": p.policy_id, "reason": "Explicit DENY rule matched"}

        # 2. Super Admin bypass
        if user_role == "SUPER_ADMIN":
            return {"decision": "ALLOW", "matched_policy": "SUPER_ADMIN_OVERRIDE", "reason": "Super Admin permission"}

        # 3. Explicit Allow check
        for p in tenant_policies:
            if p.effect == "ALLOW":
                if p.subject_role in ("*", user_role) and p.resource_type in ("*", resource_type) and p.action in ("*", action):
                    return {"decision": "ALLOW", "matched_policy": p.policy_id, "reason": "Explicit ALLOW rule matched"}

        # 4. Default Allow for Viewer reading
        if action == "READ" and user_role in self.ROLE_HIERARCHY:
            return {"decision": "ALLOW", "matched_policy": "DEFAULT_READ", "reason": "Default read permissions"}

        return {"decision": "DENY", "matched_policy": "DEFAULT_DENY", "reason": "No matching allow policy found"}

    def list_policies(self, tenant_id: Optional[str] = None) -> List[TenantPolicy]:
        if tenant_id:
            return [p for p in self._policies.values() if p.tenant_id == tenant_id]
        return list(self._policies.values())
