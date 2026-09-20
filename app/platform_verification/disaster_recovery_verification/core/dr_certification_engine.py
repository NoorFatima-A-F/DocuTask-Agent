"""
Disaster Recovery Certification & Scorecard Engine.
"""
from typing import List
from app.platform_verification.disaster_recovery_verification.domain.models import (
    DRTestScenarioResult,
    DataRecoveryValidationReport,
    DRSecurityValidationReport,
    RecoveryDependencyGraph,
    DRCertificationScorecard,
    DRCertificationTier,
    DRMaturityLevel,
)
from app.platform_verification.disaster_recovery_verification.domain.interfaces import (
    IDRCertificationEngine,
)


class DRCertificationEngine(IDRCertificationEngine):
    """Calculates weighted DR score and determines enterprise certification tier."""

    def compute_certification(
        self,
        scenarios: List[DRTestScenarioResult],
        data_report: DataRecoveryValidationReport,
        sec_report: DRSecurityValidationReport,
        dep_graph: RecoveryDependencyGraph,
    ) -> DRCertificationScorecard:
        # 1. Recovery Capability (30%): All scenarios passed, RTO < 30min (1800s)
        rec_cap = 100.0 if all(s.status == "PASS" and s.rto_seconds <= 1800.0 for s in scenarios) else 70.0

        # 2. Backup Reliability (20%): All RPO <= 300s (5min), no data loss
        backup_rel = 100.0 if all(not s.data_loss_detected and s.rpo_seconds <= 300.0 for s in scenarios) else 75.0

        # 3. Data Integrity (20%): Hash match, completeness, tenant isolation
        data_integ = 100.0 if data_report.passed else 50.0

        # 4. Automation (15%): 100% automated steps
        avg_auto = sum(s.automated_steps_percent for s in scenarios) / len(scenarios) if scenarios else 0.0
        auto_score = 100.0 if avg_auto >= 95.0 else 75.0

        # 5. Security (10%): Encryption, access control, poisoning protection
        sec_score = 100.0 if sec_report.passed else 60.0

        # 6. Documentation & Dependency Graph (5%): Valid topological order
        doc_score = 100.0 if dep_graph.valid_order else 50.0

        # Weighted composite
        composite = (
            (rec_cap * 0.30)
            + (backup_rel * 0.20)
            + (data_integ * 0.20)
            + (auto_score * 0.15)
            + (sec_score * 0.10)
            + (doc_score * 0.05)
        )

        if composite >= 95.0:
            tier = DRCertificationTier.ENTERPRISE_DR_READY
            maturity = DRMaturityLevel.LEVEL_5_RESILIENT_ARCH
        elif composite >= 90.0:
            tier = DRCertificationTier.PRODUCTION_RECOVERY_READY
            maturity = DRMaturityLevel.LEVEL_4_TESTED_DR
        elif composite >= 80.0:
            tier = DRCertificationTier.PARTIAL_RECOVERY_CAPABILITY
            maturity = DRMaturityLevel.LEVEL_3_AUTOMATED_RECOVERY
        else:
            tier = DRCertificationTier.INSUFFICIENT
            maturity = DRMaturityLevel.LEVEL_1_BACKUP_EXISTS

        passed = tier in [
            DRCertificationTier.ENTERPRISE_DR_READY,
            DRCertificationTier.PRODUCTION_RECOVERY_READY,
        ]

        return DRCertificationScorecard(
            recovery_capability_score=rec_cap,
            backup_reliability_score=backup_rel,
            data_integrity_score=data_integ,
            automation_score=auto_score,
            security_score=sec_score,
            documentation_score=doc_score,
            composite_score=round(composite, 2),
            maturity_level=maturity,
            certification_tier=tier,
            passed=passed,
        )
