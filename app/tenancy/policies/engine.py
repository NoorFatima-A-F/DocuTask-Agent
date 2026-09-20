"""Tenant Policy Engine (ESP-MOOS).

Enforces governance constraints at the organization and workspace levels:
- Allowed AI Models & Providers
- Allowed Connectors & External APIs
- Data Residency Rules
- AI Monthly Budget & Spend Thresholds
- Data Retention Constraints
- High-Risk Operation Approval Gates
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set
from pydantic import BaseModel, Field
from app.tenancy.core.models import Region
from app.tenancy.core.exceptions import TenancyError, ComplianceViolationError


class TenantPolicyRule(BaseModel):
    """Specific governance policy rules assigned to a tenant."""
    allowed_models: Set[str] = Field(default_factory=lambda: {"*"})
    allowed_connectors: Set[str] = Field(default_factory=lambda: {"*"})
    allowed_regions: Set[Region] = Field(default_factory=lambda: {Region.US_EAST, Region.US_WEST, Region.EU_WEST, Region.EU_CENTRAL})
    max_monthly_ai_budget_usd: float = 1000.0
    require_approval_for_external_email: bool = False
    enforce_pii_redaction: bool = True
    max_workflow_timeout_seconds: int = 3600


class TenantPolicyEngine:
    """Evaluates and enforces tenant governance policies across platform engines."""

    def __init__(self):
        self._org_policies: Dict[str, TenantPolicyRule] = {}

    def set_policy(self, organization_id: str, policy: TenantPolicyRule) -> None:
        """Register or update tenant policy."""
        self._org_policies[organization_id] = policy

    def get_policy(self, organization_id: str) -> TenantPolicyRule:
        """Retrieve policy for organization (defaults to standard permissive policy)."""
        return self._org_policies.get(organization_id, TenantPolicyRule())

    def validate_model_access(self, organization_id: str, model_name: str) -> bool:
        """Validate if model is allowed by tenant policy."""
        policy = self.get_policy(organization_id)
        if "*" in policy.allowed_models or model_name in policy.allowed_models:
            return True
        raise ComplianceViolationError(
            f"Model '{model_name}' is not permitted by organization policy"
        )

    def validate_connector_access(self, organization_id: str, connector_type: str) -> bool:
        """Validate if connector is allowed by tenant policy."""
        policy = self.get_policy(organization_id)
        if "*" in policy.allowed_connectors or connector_type in policy.allowed_connectors:
            return True
        raise ComplianceViolationError(
            f"Connector '{connector_type}' is blocked by organization policy"
        )

    def validate_data_residency(self, organization_id: str, target_region: Region) -> bool:
        """Validate data residency compliance."""
        policy = self.get_policy(organization_id)
        if target_region not in policy.allowed_regions:
            raise ComplianceViolationError(
                f"Region '{target_region.value}' violates tenant data residency policy"
            )
        return True

    def validate_budget(self, organization_id: str, current_spend_usd: float, estimated_cost_usd: float) -> bool:
        """Validate AI budget constraint."""
        policy = self.get_policy(organization_id)
        if current_spend_usd + estimated_cost_usd > policy.max_monthly_ai_budget_usd:
            raise TenancyError(
                f"Monthly AI spend limit of ${policy.max_monthly_ai_budget_usd:.2f} exceeded. (Current: ${current_spend_usd:.2f})"
            )
        return True
