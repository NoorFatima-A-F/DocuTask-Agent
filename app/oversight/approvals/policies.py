"""Approval Policy Engine & Condition Evaluators."""

from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field
import uuid
from ..core.context import OversightContext
from .models import ApprovalPolicyType, ApprovalStrategy


class ApprovalPolicyCondition(BaseModel):
    field: str
    operator: str  # ">", ">=", "<", "<=", "==", "!=", "in", "contains"
    value: Any


class ApprovalPolicy(BaseModel):
    policy_id: str = Field(default_factory=lambda: f"app_pol_{uuid.uuid4().hex[:8]}")
    tenant_id: str
    name: str
    policy_type: ApprovalPolicyType
    description: Optional[str] = None
    conditions: List[ApprovalPolicyCondition] = Field(default_factory=list)
    required_approval_level: int = 1
    required_roles: List[str] = Field(default_factory=lambda: ["approver"])
    min_approvers: int = 1
    approval_strategy: ApprovalStrategy = ApprovalStrategy.SEQUENTIAL
    is_active: bool = True


class ApprovalPolicyEngine:
    """Evaluates contextual risk and rules to determine if human approval is mandatory."""

    DEFAULT_POLICIES: List[ApprovalPolicy] = [
        ApprovalPolicy(
            policy_id="pol_high_risk",
            tenant_id="*",
            name="High Risk AI Oversight",
            policy_type=ApprovalPolicyType.HIGH_RISK_AI_APPROVAL,
            conditions=[ApprovalPolicyCondition(field="risk_score", operator=">=", value=0.60)],
            required_approval_level=2,
            required_roles=["compliance_officer", "secops_lead"],
        ),
        ApprovalPolicy(
            policy_id="pol_low_confidence",
            tenant_id="*",
            name="Low Confidence Extraction Review",
            policy_type=ApprovalPolicyType.WORKFLOW_APPROVAL,
            conditions=[ApprovalPolicyCondition(field="confidence_score", operator="<", value=0.85)],
            required_approval_level=1,
            required_roles=["operator", "reviewer"],
        ),
        ApprovalPolicy(
            policy_id="pol_financial_threshold",
            tenant_id="*",
            name="High Value Financial Transaction",
            policy_type=ApprovalPolicyType.FINANCIAL_APPROVAL,
            conditions=[ApprovalPolicyCondition(field="financial_impact", operator=">=", value=50000.0)],
            required_approval_level=2,
            required_roles=["finance_manager"],
        ),
        ApprovalPolicy(
            policy_id="pol_restricted_data",
            tenant_id="*",
            name="Restricted / PHI Data Access",
            policy_type=ApprovalPolicyType.DATA_ACCESS_APPROVAL,
            conditions=[ApprovalPolicyCondition(field="data_classification", operator="in", value=["RESTRICTED", "PHI", "PCI"])],
            required_approval_level=2,
            required_roles=["data_steward", "privacy_officer"],
        ),
    ]

    def __init__(self, custom_policies: Optional[List[ApprovalPolicy]] = None):
        self.policies = list(self.DEFAULT_POLICIES)
        if custom_policies:
            self.policies.extend(custom_policies)

    def add_policy(self, policy: ApprovalPolicy) -> ApprovalPolicy:
        self.policies.append(policy)
        return policy

    def _eval_condition(self, ctx_dict: Dict[str, Any], cond: ApprovalPolicyCondition) -> bool:
        field_val = ctx_dict.get(cond.field)
        if field_val is None:
            return False

        op = cond.operator
        target = cond.value

        if op == "==":
            return field_val == target
        elif op == "!=":
            return field_val != target
        elif op == ">":
            return float(field_val) > float(target)
        elif op == ">=":
            return float(field_val) >= float(target)
        elif op == "<":
            return float(field_val) < float(target)
        elif op == "<=":
            return float(field_val) <= float(target)
        elif op == "in":
            return field_val in target if isinstance(target, (list, set, tuple)) else str(field_val) in str(target)
        elif op == "contains":
            return target in field_val if isinstance(field_val, (list, str)) else False
        return False

    def evaluate(self, context: OversightContext) -> Tuple[bool, Optional[ApprovalPolicy], str]:
        """Returns (requires_human_approval, matching_policy, reason)."""
        ctx_dict = context.model_dump()

        # Check tenant specific and global policies
        applicable_policies = [p for p in self.policies if p.is_active and (p.tenant_id == "*" or p.tenant_id == context.tenant_id)]

        for pol in applicable_policies:
            if not pol.conditions:
                continue
            all_match = all(self._eval_condition(ctx_dict, c) for c in pol.conditions)
            if all_match:
                return True, pol, f"Triggered oversight policy '{pol.name}' ({pol.policy_type.value})"

        return False, None, "Autonomous execution permitted: no oversight policy triggered"
