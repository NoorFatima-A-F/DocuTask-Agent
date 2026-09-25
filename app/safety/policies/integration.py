"""Governance Policy Integration & Tenant Safety Policy Configuration."""

from typing import Dict
from pydantic import BaseModel


class TenantSafetyPolicy(BaseModel):
    """Tenant-specific safety governance parameters."""
    tenant_id: str
    max_input_length: int = 100_000
    block_on_prompt_injection: bool = True
    block_on_jailbreak: bool = True
    auto_redact_pii: bool = True
    require_tool_approval: bool = True
    min_grounding_score: float = 0.70
    max_risk_score_threshold: float = 0.85
    enabled_pii_detection: bool = True


class SafetyPolicyBridge:
    """Bridges runtime safety guardrails with Phase 8A enterprise governance control plane."""

    def __init__(self):
        self._policies: Dict[str, TenantSafetyPolicy] = {}

    def get_policy(self, tenant_id: str) -> TenantSafetyPolicy:
        if tenant_id in self._policies:
            return self._policies[tenant_id]
        # Return default policy
        return TenantSafetyPolicy(tenant_id=tenant_id)

    def set_policy(self, policy: TenantSafetyPolicy) -> None:
        self._policies[policy.tenant_id] = policy

    def update_policy(self, tenant_id: str, **kwargs) -> TenantSafetyPolicy:
        policy = self.get_policy(tenant_id)
        updated_data = policy.model_dump()
        updated_data.update(kwargs)
        new_policy = TenantSafetyPolicy(**updated_data)
        self._policies[tenant_id] = new_policy
        return new_policy
