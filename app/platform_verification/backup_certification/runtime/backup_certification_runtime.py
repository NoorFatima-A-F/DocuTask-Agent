"""
Master Runtime Orchestrator for Backup Certification Framework (Part 3G.2G).
Coordinates evidence collection, analyzers, scoring, policy validation, risk generation,
and report export.
"""
import time
from typing import Dict, Any, Optional

from app.platform_verification.backup_certification.collector.evidence_collector import (
    EvidenceCollector,
)
from app.platform_verification.backup_certification.analyzers.completeness_analyzer import (
    CompletenessAnalyzer,
)
from app.platform_verification.backup_certification.analyzers.integrity_analyzer import (
    IntegrityAnalyzer,
)
from app.platform_verification.backup_certification.analyzers.restore_capability_analyzer import (
    RestoreCapabilityAnalyzer,
)
from app.platform_verification.backup_certification.analyzers.operational_readiness_analyzer import (
    OperationalReadinessAnalyzer,
)
from app.platform_verification.backup_certification.analyzers.rto_rpo_certifier import (
    RTORPOCertifier,
)
from app.platform_verification.backup_certification.policies.backup_policy_validator import (
    BackupPolicyValidator,
)
from app.platform_verification.backup_certification.validators.continuous_validation_engine import (
    ContinuousValidationEngine,
)
from app.platform_verification.backup_certification.risk.risk_register_generator import (
    RiskRegisterGenerator,
)
from app.platform_verification.backup_certification.scoring.backup_readiness_scoring_engine import (
    BackupReadinessScoringEngine,
)
from app.platform_verification.backup_certification.dashboard.backup_dashboard_engine import (
    BackupDashboardEngine,
)
from app.platform_verification.backup_certification.reports.certification_report_engine import (
    CertificationReportEngine,
)


class BackupCertificationRuntime:
    """
    Master coordinator for Enterprise Backup Readiness Certification.
    Proves objectively that the backup and restore infrastructure satisfies enterprise
    reliability, recovery speed, data integrity, and compliance standards.
    """

    def __init__(
        self,
        evidence_collector: Optional[EvidenceCollector] = None,
        completeness_analyzer: Optional[CompletenessAnalyzer] = None,
        integrity_analyzer: Optional[IntegrityAnalyzer] = None,
        restore_analyzer: Optional[RestoreCapabilityAnalyzer] = None,
        operational_analyzer: Optional[OperationalReadinessAnalyzer] = None,
        rto_rpo_certifier: Optional[RTORPOCertifier] = None,
        policy_validator: Optional[BackupPolicyValidator] = None,
        continuous_engine: Optional[ContinuousValidationEngine] = None,
        risk_generator: Optional[RiskRegisterGenerator] = None,
        scoring_engine: Optional[BackupReadinessScoringEngine] = None,
        dashboard_engine: Optional[BackupDashboardEngine] = None,
        report_engine: Optional[CertificationReportEngine] = None,
    ):
        self.evidence_collector = evidence_collector or EvidenceCollector()
        self.completeness_analyzer = completeness_analyzer or CompletenessAnalyzer()
        self.integrity_analyzer = integrity_analyzer or IntegrityAnalyzer()
        self.restore_analyzer = restore_analyzer or RestoreCapabilityAnalyzer()
        self.operational_analyzer = operational_analyzer or OperationalReadinessAnalyzer()
        self.rto_rpo_certifier = rto_rpo_certifier or RTORPOCertifier()
        self.policy_validator = policy_validator or BackupPolicyValidator()
        self.continuous_engine = continuous_engine or ContinuousValidationEngine()
        self.risk_generator = risk_generator or RiskRegisterGenerator()
        self.scoring_engine = scoring_engine or BackupReadinessScoringEngine()
        self.dashboard_engine = dashboard_engine or BackupDashboardEngine()
        self.report_engine = report_engine or CertificationReportEngine()

    def execute_full_certification(
        self, output_dir: str = "backup_certification"
    ) -> Dict[str, Any]:
        """
        Executes complete end-to-end backup certification pipeline.
        """
        start_time = time.perf_counter()

        # 1. Evidence Collection
        evidence = self.evidence_collector.collect_all_evidence()

        # 2. Comprehensive Analyzers
        completeness = self.completeness_analyzer.analyze_completeness(evidence)
        integrity = self.integrity_analyzer.analyze_integrity(evidence)
        restore = self.restore_analyzer.analyze_restore_capability(evidence)
        operational = self.operational_analyzer.analyze_operational_readiness(evidence)
        rto_rpo = self.rto_rpo_certifier.certify_rto_rpo(evidence)
        policy = self.policy_validator.validate_policies(evidence)
        schedule = self.continuous_engine.generate_verification_schedule()
        risks = self.risk_generator.generate_risk_register(
            completeness, integrity, restore, policy, operational
        )

        # 3. Security score from collected evidence
        security_score = float(
            evidence.security_validation.get("compliance_score_percent", 100.0)
        )

        # 4. Weighted Scoring & Tier Assignment
        scorecard = self.scoring_engine.compute_certification_score(
            completeness_score=completeness.completeness_score,
            restore_score=restore.restore_capability_score,
            integrity_score=integrity.integrity_score,
            security_score=security_score,
            automation_score=100.0 if operational.automation_enabled else 50.0,
            monitoring_score=100.0 if operational.monitoring_configured else 50.0,
            documentation_score=100.0 if operational.documentation_complete else 50.0,
        )

        # 5. Operational Dashboard Generation
        dashboard = self.dashboard_engine.generate_dashboard(scorecard, rto_rpo, evidence)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        scorecard.evaluation_metadata["execution_duration_ms"] = elapsed_ms

        # 6. Artifact & Evidence Serialization
        manifests = self.report_engine.export_all_certification_artifacts(
            scorecard=scorecard,
            completeness=completeness,
            integrity=integrity,
            restore=restore,
            operational=operational,
            rto_rpo=rto_rpo,
            policy=policy,
            risks=risks,
            schedule=schedule,
            dashboard=dashboard,
            evidence=evidence,
            output_dir=output_dir,
        )

        # Also mirror to evidence/backup_certification for unified evidence indexing
        evidence_dir = "evidence/backup_certification"
        if output_dir != evidence_dir:
            self.report_engine.export_all_certification_artifacts(
                scorecard=scorecard,
                completeness=completeness,
                integrity=integrity,
                restore=restore,
                operational=operational,
                rto_rpo=rto_rpo,
                policy=policy,
                risks=risks,
                schedule=schedule,
                dashboard=dashboard,
                evidence=evidence,
                output_dir=evidence_dir,
            )

        return {
            "evidence": evidence,
            "completeness": completeness,
            "integrity": integrity,
            "restore": restore,
            "operational": operational,
            "rto_rpo": rto_rpo,
            "policy": policy,
            "schedule": schedule,
            "risks": risks,
            "scorecard": scorecard,
            "dashboard": dashboard,
            "manifests": manifests,
            "passed": scorecard.passed,
            "ci_cd_deployment_approved": scorecard.ci_cd_deployment_approved,
        }
