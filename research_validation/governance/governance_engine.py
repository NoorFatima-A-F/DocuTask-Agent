"""
Research Governance Engine (Phase 93C)
=====================================
Master policy enforcement gateway verifying compliance across manifests,
execution traces, uncertainty bounds, and publication claims.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional

from research_validation.governance.governance_policy import (
    PolicyCategory, PolicyEnforcementAction, GovernancePolicyRule
)
from research_validation.governance.governance_audit import (
    GovernanceAuditRecord, GovernanceAuditLog
)


@dataclass(frozen=True)
class GovernanceVerificationVerdict:
    """Overall compliance verdict across all evaluated governance rules."""
    target_id: str
    is_fully_compliant: bool
    is_blocked: bool
    total_checks: int
    passed_checks: int
    warning_checks: int
    blocked_checks: int
    audit_records: List[GovernanceAuditRecord]
    audit_root_digest: str
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ResearchGovernanceEngine:
    """
    Automated governance and policy enforcement gateway.
    """

    DEFAULT_RULES: List[GovernancePolicyRule] = [
        GovernancePolicyRule(
            rule_id="RULE_ZERO_FABRICATION",
            category=PolicyCategory.ZERO_FABRICATION,
            name="Zero Fabrication Metric Policy",
            description="All reported metrics must have an immutable raw observation digest.",
            enforcement_action=PolicyEnforcementAction.BLOCK_EXECUTION,
        ),
        GovernancePolicyRule(
            rule_id="RULE_PROVENANCE_SEALING",
            category=PolicyCategory.PROVENANCE_INTEGRITY,
            name="Cryptographic Lineage Sealing",
            description="Artifacts must be bound to a valid Merkle DAG root hash.",
            enforcement_action=PolicyEnforcementAction.BLOCK_EXECUTION,
        ),
        GovernancePolicyRule(
            rule_id="RULE_STATISTICAL_POWER",
            category=PolicyCategory.STATISTICAL_RIGOR,
            name="Sample Size & Statistical Power",
            description="Confidence intervals must be explicitly reported alongside point estimates.",
            enforcement_action=PolicyEnforcementAction.FLAG_WARNING,
        ),
        GovernancePolicyRule(
            rule_id="RULE_PRIVACY_MINIMIZATION",
            category=PolicyCategory.PRIVACY_DATA_MINIMIZATION,
            name="Zero PII / Anonymized Dataset Storage",
            description="Raw document images with unmasked PII cannot be stored in unencrypted form.",
            enforcement_action=PolicyEnforcementAction.BLOCK_EXECUTION,
        ),
    ]

    def __init__(self, custom_rules: Optional[List[GovernancePolicyRule]] = None):
        self.rules = custom_rules or list(self.DEFAULT_RULES)
        self.audit_log = GovernanceAuditLog()

    def audit_experiment_plan(
        self,
        plan_id: str,
        has_provenance_digest: bool,
        has_confidence_intervals: bool,
        is_privacy_compliant: bool = True,
    ) -> GovernanceVerificationVerdict:
        """Audits an experiment plan or draft against all governance rules."""
        records: List[GovernanceAuditRecord] = []
        blocked = 0
        warnings = 0
        passed = 0

        # Check 1: Zero Fabrication & Provenance
        if has_provenance_digest:
            rec = self.audit_log.record_check(
                target_id=plan_id,
                rule_id="RULE_PROVENANCE_SEALING",
                category=PolicyCategory.PROVENANCE_INTEGRITY,
                action=PolicyEnforcementAction.ALLOW,
                is_compliant=True,
                details="Valid cryptographic SHA-256 digest present.",
            )
            passed += 1
        else:
            rec = self.audit_log.record_check(
                target_id=plan_id,
                rule_id="RULE_PROVENANCE_SEALING",
                category=PolicyCategory.PROVENANCE_INTEGRITY,
                action=PolicyEnforcementAction.BLOCK_EXECUTION,
                is_compliant=False,
                details="Missing provenance digest! Zero fabrication policy violated.",
            )
            blocked += 1
        records.append(rec)

        # Check 2: Statistical Rigor
        if has_confidence_intervals:
            rec = self.audit_log.record_check(
                target_id=plan_id,
                rule_id="RULE_STATISTICAL_POWER",
                category=PolicyCategory.STATISTICAL_RIGOR,
                action=PolicyEnforcementAction.ALLOW,
                is_compliant=True,
                details="Confidence intervals and uncertainty bounds provided.",
            )
            passed += 1
        else:
            rec = self.audit_log.record_check(
                target_id=plan_id,
                rule_id="RULE_STATISTICAL_POWER",
                category=PolicyCategory.STATISTICAL_RIGOR,
                action=PolicyEnforcementAction.FLAG_WARNING,
                is_compliant=False,
                details="Confidence intervals missing. Flagged as statistical warning.",
            )
            warnings += 1
        records.append(rec)

        # Check 3: Privacy
        if is_privacy_compliant:
            rec = self.audit_log.record_check(
                target_id=plan_id,
                rule_id="RULE_PRIVACY_MINIMIZATION",
                category=PolicyCategory.PRIVACY_DATA_MINIMIZATION,
                action=PolicyEnforcementAction.ALLOW,
                is_compliant=True,
                details="No unmasked PII detected in experiment payloads.",
            )
            passed += 1
        else:
            rec = self.audit_log.record_check(
                target_id=plan_id,
                rule_id="RULE_PRIVACY_MINIMIZATION",
                category=PolicyCategory.PRIVACY_DATA_MINIMIZATION,
                action=PolicyEnforcementAction.BLOCK_EXECUTION,
                is_compliant=False,
                details="Privacy violation detected in dataset payloads.",
            )
            blocked += 1
        records.append(rec)

        audit_root = self.audit_log.compute_audit_root_digest()

        return GovernanceVerificationVerdict(
            target_id=plan_id,
            is_fully_compliant=(blocked == 0 and warnings == 0),
            is_blocked=(blocked > 0),
            total_checks=len(records),
            passed_checks=passed,
            warning_checks=warnings,
            blocked_checks=blocked,
            audit_records=records,
            audit_root_digest=audit_root,
        )
