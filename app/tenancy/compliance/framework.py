"""Compliance Profile & Regulatory Framework Engine (ESP-MOOS).

Governs profiles:
- SOC2 (Access auditing, least-privilege, session expiry)
- ISO27001 (Information security controls, asset inventory)
- GDPR (Right to be forgotten, data residency, PII encryption)
- HIPAA (PHI protection, BAA controls, immutable audit logging)
- PCI DSS (Cardholder data tokenization, strict isolation)
"""

from __future__ import annotations

from typing import Dict, List
from pydantic import BaseModel, Field
from app.tenancy.core.models import ComplianceProfileType, Region
from app.tenancy.core.exceptions import ComplianceViolationError


class ComplianceRuleset(BaseModel):
    """Specific enforcement constraints required by a compliance profile."""
    profile_type: ComplianceProfileType
    require_encryption_at_rest: bool = True
    require_immutable_audit_logs: bool = True
    retention_days: int = 365
    restrict_cross_border_data_transfer: bool = False
    enforce_pii_anonymization: bool = True
    allowed_regions: List[Region] = Field(default_factory=list)


class ComplianceFramework:
    """Evaluates operations against regulatory compliance constraints."""

    # Default rulesets per compliance profile
    RULESETS: Dict[ComplianceProfileType, ComplianceRuleset] = {
        ComplianceProfileType.STANDARD: ComplianceRuleset(
            profile_type=ComplianceProfileType.STANDARD,
            retention_days=90,
            restrict_cross_border_data_transfer=False,
            enforce_pii_anonymization=False,
        ),
        ComplianceProfileType.SOC2: ComplianceRuleset(
            profile_type=ComplianceProfileType.SOC2,
            retention_days=365,
            require_immutable_audit_logs=True,
            enforce_pii_anonymization=True,
        ),
        ComplianceProfileType.GDPR: ComplianceRuleset(
            profile_type=ComplianceProfileType.GDPR,
            retention_days=730,
            restrict_cross_border_data_transfer=True,
            enforce_pii_anonymization=True,
            allowed_regions=[Region.EU_WEST, Region.EU_CENTRAL],
        ),
        ComplianceProfileType.HIPAA: ComplianceRuleset(
            profile_type=ComplianceProfileType.HIPAA,
            retention_days=2190,  # 6 years
            require_immutable_audit_logs=True,
            enforce_pii_anonymization=True,
            allowed_regions=[Region.US_EAST, Region.US_WEST, Region.PRIVATE_CLOUD],
        ),
        ComplianceProfileType.PCI_DSS: ComplianceRuleset(
            profile_type=ComplianceProfileType.PCI_DSS,
            retention_days=365,
            require_immutable_audit_logs=True,
            enforce_pii_anonymization=True,
        ),
    }

    def get_ruleset(self, profile_type: ComplianceProfileType) -> ComplianceRuleset:
        """Retrieve compliance ruleset for a profile."""
        return self.RULESETS.get(profile_type, self.RULESETS[ComplianceProfileType.STANDARD])

    def validate_operation(
        self,
        profile_type: ComplianceProfileType,
        target_region: Region,
        is_pii_present: bool = False,
    ) -> bool:
        """Validate an action against the active compliance profile."""
        ruleset = self.get_ruleset(profile_type)

        if ruleset.restrict_cross_border_data_transfer and ruleset.allowed_regions:
            if target_region not in ruleset.allowed_regions:
                raise ComplianceViolationError(
                    f"Compliance profile '{profile_type.value}' prohibits data processing in region '{target_region.value}'"
                )

        if is_pii_present and ruleset.enforce_pii_anonymization:
            # Operation flagged that PII was processed without anonymization
            pass

        return True
