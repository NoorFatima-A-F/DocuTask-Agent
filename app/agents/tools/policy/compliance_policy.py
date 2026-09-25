"""
Compliance Policy for Advanced Tool Policy Engine.
Enforces regulatory compliance frameworks (HIPAA, GDPR, SOC2, PCI-DSS)
on tool execution and document dispatching.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set

from app.agents.tools.policy.privacy_policy import PrivacyPolicy

logger = logging.getLogger(__name__)


class ComplianceFramework(str, Enum):
    HIPAA = "HIPAA"
    GDPR = "GDPR"
    SOC2 = "SOC2"
    PCI_DSS = "PCI_DSS"


@dataclass
class ComplianceResult:
    """Outcome of compliance verification."""

    compliant: bool
    frameworks_evaluated: List[ComplianceFramework]
    violations: List[str] = field(default_factory=list)
    requires_masking: bool = False


class CompliancePolicy:
    """Validates that tool calls comply with statutory and enterprise data regulations."""

    EXTERNAL_UNENCRYPTED_TOOLS: Set[str] = {
        "public_ocr_api",
        "third_party_summarizer",
        "untrusted_web_search",
    }

    def __init__(self, active_frameworks: Optional[List[ComplianceFramework]] = None) -> None:
        self.active_frameworks = active_frameworks or [
            ComplianceFramework.HIPAA,
            ComplianceFramework.GDPR,
            ComplianceFramework.SOC2,
        ]

    def evaluate(
        self,
        tool_name: str,
        document_domain: str,
        payload: Dict[str, Any],
    ) -> ComplianceResult:
        """Verifies compliance against active frameworks."""
        violations: List[str] = []
        requires_masking = False
        payload_str = str(payload)
        has_pii = PrivacyPolicy.contains_pii(payload_str)

        # 1. HIPAA checks
        if ComplianceFramework.HIPAA in self.active_frameworks:
            if "medical" in document_domain.lower() or "health" in document_domain.lower():
                if tool_name.lower() in self.EXTERNAL_UNENCRYPTED_TOOLS:
                    violations.append(
                        f"HIPAA violation: Cannot dispatch PHI to external unverified tool '{tool_name}'."
                    )
                if has_pii:
                    requires_masking = True

        # 2. GDPR checks
        if ComplianceFramework.GDPR in self.active_frameworks:
            if has_pii and tool_name.lower() in self.EXTERNAL_UNENCRYPTED_TOOLS:
                violations.append(
                    f"GDPR violation: Transmitting unmasked personal data to external tool '{tool_name}' is prohibited."
                )

        # 3. PCI-DSS checks
        if ComplianceFramework.PCI_DSS in self.active_frameworks:
            if "CREDIT_CARD" in PrivacyPolicy.mask_pii(payload_str).detected_pii_types:
                violations.append("PCI-DSS violation: Unmasked primary account numbers (PAN) in tool payload.")

        is_compliant = len(violations) == 0
        return ComplianceResult(
            compliant=is_compliant,
            frameworks_evaluated=list(self.active_frameworks),
            violations=violations,
            requires_masking=requires_masking,
        )
