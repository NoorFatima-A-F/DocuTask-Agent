"""
Tool Decision Engine for Advanced Tool Policy.
Unifies security, compliance, and privacy verification into a pre-execution authorization gate.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from app.agents.tools.policy.compliance_policy import CompliancePolicy
from app.agents.tools.policy.privacy_policy import PIIMaskResult, PrivacyPolicy
from app.agents.tools.policy.security_policy import SecurityPolicy

logger = logging.getLogger(__name__)


class PolicyDecision(str, Enum):
    APPROVED = "APPROVED"
    APPROVED_WITH_MASKING = "APPROVED_WITH_MASKING"
    DENIED = "DENIED"


@dataclass
class ToolAuthorizationResult:
    """Complete authorization decision with actionable transformed payload."""

    decision: PolicyDecision
    tool_name: str
    effective_payload: Dict[str, Any]
    violations: List[str] = field(default_factory=list)
    masking_metadata: Optional[PIIMaskResult] = None
    audit_notes: str = ""


class ToolDecisionEngine:
    """Pre-execution governance gate evaluating safety, privacy, and compliance."""

    def __init__(
        self,
        security_policy: Optional[SecurityPolicy] = None,
        compliance_policy: Optional[CompliancePolicy] = None,
    ) -> None:
        self.security_policy = security_policy or SecurityPolicy()
        self.compliance_policy = compliance_policy or CompliancePolicy()

    def evaluate_tool_call(
        self,
        tool_name: str,
        payload: Dict[str, Any],
        document_domain: str = "general",
        agent_role: str = "general_agent",
    ) -> ToolAuthorizationResult:
        """Evaluates whether the tool call is authorized, denied, or requires sanitization."""
        # 1. Security Check
        sec_result = self.security_policy.validate(tool_name=tool_name, input_payload=payload)
        if not sec_result.is_allowed:
            return ToolAuthorizationResult(
                decision=PolicyDecision.DENIED,
                tool_name=tool_name,
                effective_payload=payload,
                violations=sec_result.violations,
                audit_notes="Blocked by security policy.",
            )

        # 2. Compliance Check
        comp_result = self.compliance_policy.evaluate(
            tool_name=tool_name,
            document_domain=document_domain,
            payload=payload,
        )
        if not comp_result.compliant:
            return ToolAuthorizationResult(
                decision=PolicyDecision.DENIED,
                tool_name=tool_name,
                effective_payload=payload,
                violations=comp_result.violations,
                audit_notes="Blocked by regulatory compliance policy.",
            )

        # 3. Privacy & Masking Check
        payload_str = str(payload)
        has_pii = PrivacyPolicy.contains_pii(payload_str)
        if has_pii or comp_result.requires_masking:
            sanitized_payload = {}
            mask_info = None
            for k, v in payload.items():
                if isinstance(v, str):
                    res = PrivacyPolicy.mask_pii(v)
                    sanitized_payload[k] = res.sanitized_text
                    mask_info = res
                else:
                    sanitized_payload[k] = v

            logger.info("Tool %s approved with PII masking applied", tool_name)
            return ToolAuthorizationResult(
                decision=PolicyDecision.APPROVED_WITH_MASKING,
                tool_name=tool_name,
                effective_payload=sanitized_payload,
                violations=[],
                masking_metadata=mask_info,
                audit_notes="Authorized with synthetic token substitution for PII entities.",
            )

        # 4. Clean Approval
        return ToolAuthorizationResult(
            decision=PolicyDecision.APPROVED,
            tool_name=tool_name,
            effective_payload=payload,
            violations=[],
            audit_notes="Tool invocation authorized without restrictions.",
        )
