"""
Resilience Risk Management Subsystem for Disaster Recovery Governance (Part 3G.4).
Manages, assesses, and mitigates enterprise DR risks across 5 key dimensions:
1. INFRASTRUCTURE_DEPENDENCY
2. DATA_INTEGRITY_AND_CORRUPTION
3. SECURITY_AND_SECRETS
4. OPERATIONAL_AND_HUMAN
5. COMPLIANCE_AND_AUDIT
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List
from enum import Enum


class RiskCategory(str, Enum):
    INFRASTRUCTURE_DEPENDENCY = "INFRASTRUCTURE_DEPENDENCY"
    DATA_INTEGRITY_AND_CORRUPTION = "DATA_INTEGRITY_AND_CORRUPTION"
    SECURITY_AND_SECRETS = "SECURITY_AND_SECRETS"
    OPERATIONAL_AND_HUMAN = "OPERATIONAL_AND_HUMAN"
    COMPLIANCE_AND_AUDIT = "COMPLIANCE_AND_AUDIT"


class RiskLevel(str, Enum):
    LOW = "LOW"            # 1 - 5
    MEDIUM = "MEDIUM"      # 6 - 11
    HIGH = "HIGH"          # 12 - 19
    CRITICAL = "CRITICAL"  # 20 - 25


@dataclass
class RiskItem:
    risk_id: str
    category: RiskCategory
    title: str
    description: str
    likelihood: int  # 1 to 5
    impact: int      # 1 to 5
    inherent_score: int
    inherent_level: RiskLevel
    mitigating_control: str
    control_status: str  # VERIFIED_ACTIVE / IN_REMEDIATION
    residual_likelihood: int
    residual_impact: int
    residual_score: int
    residual_level: RiskLevel
    owner: str


@dataclass
class ResilienceRiskReport:
    total_risks_cataloged: int
    high_critical_risks_unmitigated: int
    risks: List[RiskItem] = field(default_factory=list)
    passed: bool = True
    details: Dict[str, Any] = field(default_factory=dict)


class ResilienceRiskManager:
    """
    Evaluates enterprise resilience risk posture and ensures all critical DR risks have active controls.
    """

    DEFAULT_RISKS = [
        RiskItem(
            risk_id="RSK-DR-001",
            category=RiskCategory.INFRASTRUCTURE_DEPENDENCY,
            title="Cloud Provider Multi-AZ Failure & Network Partition",
            description="Simultaneous loss of connectivity to primary availability zone hosting PostgreSQL master.",
            likelihood=3,
            impact=5,
            inherent_score=15,
            inherent_level=RiskLevel.HIGH,
            mitigating_control="Automated Patroni DCS quorum failover to secondary AZ with sync replication (RTO < 5m, RPO = 0s).",
            control_status="VERIFIED_ACTIVE",
            residual_likelihood=1,
            residual_impact=2,
            residual_score=2,
            residual_level=RiskLevel.LOW,
            owner="Principal Database Reliability Engineer",
        ),
        RiskItem(
            risk_id="RSK-DR-002",
            category=RiskCategory.DATA_INTEGRITY_AND_CORRUPTION,
            title="Silent Database Data Corruption or Uncommitted WAL Gap",
            description="Bit rot, storage controller bug, or uncommitted transaction loss during sudden node crash.",
            likelihood=2,
            impact=5,
            inherent_score=10,
            inherent_level=RiskLevel.MEDIUM,
            mitigating_control="pg_checksums enabled on all blocks; continuous pgBackRest PITR verification with sha256 checksums.",
            control_status="VERIFIED_ACTIVE",
            residual_likelihood=1,
            residual_impact=1,
            residual_score=1,
            residual_level=RiskLevel.LOW,
            owner="Principal Database Reliability Engineer",
        ),
        RiskItem(
            risk_id="RSK-DR-003",
            category=RiskCategory.SECURITY_AND_SECRETS,
            title="KMS Key Revocation / Secret Vault Unavailability During Restore",
            description="Decryption keys unavailable when restoring encrypted backups in a disaster recovery region.",
            likelihood=2,
            impact=5,
            inherent_score=10,
            inherent_level=RiskLevel.MEDIUM,
            mitigating_control="Multi-region replicated Vault clusters & backup key escrow with split-key Shamir recovery protocol.",
            control_status="VERIFIED_ACTIVE",
            residual_likelihood=1,
            residual_impact=2,
            residual_score=2,
            residual_level=RiskLevel.LOW,
            owner="Principal Cloud Security Architect",
        ),
        RiskItem(
            risk_id="RSK-DR-004",
            category=RiskCategory.OPERATIONAL_AND_HUMAN,
            title="Runbook Drift & Operational Human Error during Outage",
            description="Engineers executing outdated runbook commands during an emergency leading to extended outage.",
            likelihood=4,
            impact=4,
            inherent_score=16,
            inherent_level=RiskLevel.HIGH,
            mitigating_control="100% automated CI/CD documentation drift detection and self-executing runbook automation scripts.",
            control_status="VERIFIED_ACTIVE",
            residual_likelihood=1,
            residual_impact=2,
            residual_score=2,
            residual_level=RiskLevel.LOW,
            owner="Platform SRE Lead",
        ),
        RiskItem(
            risk_id="RSK-DR-005",
            category=RiskCategory.COMPLIANCE_AND_AUDIT,
            title="Non-compliant Backup Retention & Missing Audit Trail",
            description="Failure to satisfy SOC2 / ISO 27001 regulatory requirements for immutable 90-day recovery logs.",
            likelihood=2,
            impact=4,
            inherent_score=8,
            inherent_level=RiskLevel.MEDIUM,
            mitigating_control="Automated WORM storage compliance policies, daily audit package generation, and immutable log signing.",
            control_status="VERIFIED_ACTIVE",
            residual_likelihood=1,
            residual_impact=1,
            residual_score=1,
            residual_level=RiskLevel.LOW,
            owner="Enterprise Compliance Lead",
        ),
    ]

    def __init__(self, risk_items: List[RiskItem] = None):
        self.risks = risk_items if risk_items is not None else list(self.DEFAULT_RISKS)

    def assess_risk_posture(self) -> ResilienceRiskReport:
        """
        Calculates overall residual risk posture and ensures all high/critical risks are mitigated.
        """
        unmitigated_count = 0
        category_distribution: Dict[str, int] = {}

        for item in self.risks:
            cat_name = item.category.value
            category_distribution[cat_name] = category_distribution.get(cat_name, 0) + 1

            if item.residual_level in [RiskLevel.HIGH, RiskLevel.CRITICAL] or item.control_status != "VERIFIED_ACTIVE":
                unmitigated_count += 1

        passed = unmitigated_count == 0

        details = {
            "category_distribution": category_distribution,
            "total_risks": len(self.risks),
            "unmitigated_risks_count": unmitigated_count,
            "risk_mitigation_percentage": 100.0 if passed else round((len(self.risks) - unmitigated_count) / len(self.risks) * 100, 2),
            "risk_assessment_framework": "ISO_31000_RESILIENCE_RISK_MODEL",
        }

        return ResilienceRiskReport(
            total_risks_cataloged=len(self.risks),
            high_critical_risks_unmitigated=unmitigated_count,
            risks=self.risks,
            passed=passed,
            details=details,
        )
