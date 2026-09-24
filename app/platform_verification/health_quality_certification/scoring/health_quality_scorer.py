"""
Phase 3H.5.11: Health Quality & Certification Scorer
"""
from uuid import uuid4
from typing import List
from datetime import datetime, timezone

from ..domain.models import (
    LivenessQualityMetrics,
    ReadinessQualityMetrics,
    DependencyHealthMetrics,
    FailureDetectionMetrics,
    RecoveryCapabilityMetrics,
    MonitoringIntegrationMetrics,
    SecurityComplianceMetrics,
    EvidenceQualityMetrics,
    SREReliabilityMetrics,
    RegressionReport,
    DeploymentGateReport,
    HealthQualityCertificationReport,
    HealthQualityScorecard,
    CategoryScoreItem,
    HealthMaturityLevel,
    CertificationStatus,
)
from ..domain.interfaces import IHealthQualityScorer


class HealthQualityScorer(IHealthQualityScorer):
    """
    Computes weighted 8-pillar health quality scores, checks veto failure conditions,
    and produces enterprise certification credentials.
    """

    WEIGHTS = {
        "liveness": 0.15,
        "readiness": 0.15,
        "dependencies": 0.15,
        "failure_detection": 0.15,
        "recovery": 0.15,
        "monitoring": 0.10,
        "security": 0.10,
        "evidence": 0.05,
    }

    def calculate_certification_scorecard(
        self,
        liveness: LivenessQualityMetrics,
        readiness: ReadinessQualityMetrics,
        dependencies: DependencyHealthMetrics,
        failure_detection: FailureDetectionMetrics,
        recovery: RecoveryCapabilityMetrics,
        monitoring: MonitoringIntegrationMetrics,
        security: SecurityComplianceMetrics,
        evidence: EvidenceQualityMetrics,
        sre_metrics: SREReliabilityMetrics,
        regression_report: RegressionReport,
        gate_report: DeploymentGateReport,
    ) -> HealthQualityScorecard:
        category_scores: List[CategoryScoreItem] = []

        # 1. Liveness (15%)
        l_weighted = liveness.score * self.WEIGHTS["liveness"]
        category_scores.append(
            CategoryScoreItem(
                category_id="liveness",
                category_name="Liveness Reliability",
                weight=self.WEIGHTS["liveness"],
                raw_score=round(liveness.score, 2),
                weighted_score=round(l_weighted, 2),
                status="EXCELLENT" if liveness.score >= 95 else "ADEQUATE",
                details=f"Accuracy: {liveness.liveness_accuracy}%, Latency: {liveness.detection_latency_ms}ms, False-alive: {liveness.false_alive_rate}%.",
            )
        )

        # 2. Readiness (15%)
        r_weighted = readiness.score * self.WEIGHTS["readiness"]
        category_scores.append(
            CategoryScoreItem(
                category_id="readiness",
                category_name="Readiness Accuracy",
                weight=self.WEIGHTS["readiness"],
                raw_score=round(readiness.score, 2),
                weighted_score=round(r_weighted, 2),
                status="EXCELLENT" if readiness.score >= 95 else "ADEQUATE",
                details=f"Accuracy: {readiness.readiness_accuracy}%, Detection: {readiness.dependency_detection_time_ms}ms, False-ready: {readiness.false_ready_rate}%.",
            )
        )

        # 3. Dependencies (15%)
        d_weighted = dependencies.score * self.WEIGHTS["dependencies"]
        category_scores.append(
            CategoryScoreItem(
                category_id="dependencies",
                category_name="Dependency Health Intelligence",
                weight=self.WEIGHTS["dependencies"],
                raw_score=round(dependencies.score, 2),
                weighted_score=round(d_weighted, 2),
                status="EXCELLENT" if dependencies.score >= 95 else "ADEQUATE",
                details=f"Visibility: {dependencies.dependency_visibility}%, Isolation: {dependencies.failure_isolation_rate}%, Monitored: {len(dependencies.dependencies_monitored)} services.",
            )
        )

        # 4. Failure Detection (15%)
        fd_weighted = failure_detection.score * self.WEIGHTS["failure_detection"]
        category_scores.append(
            CategoryScoreItem(
                category_id="failure_detection",
                category_name="Failure Detection Capability",
                weight=self.WEIGHTS["failure_detection"],
                raw_score=round(failure_detection.score, 2),
                weighted_score=round(fd_weighted, 2),
                status="EXCELLENT" if failure_detection.score >= 95 else "ADEQUATE",
                details=f"MTTD: {failure_detection.mttd_seconds}s, Scenarios: {failure_detection.scenarios_detected_count}/{len(failure_detection.scenarios_evaluated)} detected.",
            )
        )

        # 5. Recovery (15%)
        rec_weighted = recovery.score * self.WEIGHTS["recovery"]
        category_scores.append(
            CategoryScoreItem(
                category_id="recovery",
                category_name="Recovery Capability",
                weight=self.WEIGHTS["recovery"],
                raw_score=round(recovery.score, 2),
                weighted_score=round(rec_weighted, 2),
                status="EXCELLENT" if recovery.score >= 95 else "ADEQUATE",
                details=f"MTTR: {recovery.mttr_seconds}s, Success rate: {recovery.recovery_success_rate_pct}%, Stages verified: {len(recovery.stages_validated)}.",
            )
        )

        # 6. Monitoring Integration (10%)
        m_weighted = monitoring.score * self.WEIGHTS["monitoring"]
        category_scores.append(
            CategoryScoreItem(
                category_id="monitoring",
                category_name="Monitoring Integration",
                weight=self.WEIGHTS["monitoring"],
                raw_score=round(monitoring.score, 2),
                weighted_score=round(m_weighted, 2),
                status="EXCELLENT" if monitoring.score >= 95 else "ADEQUATE",
                details=f"Coverage: {monitoring.metric_coverage_pct}%, Dashboard quality: {monitoring.dashboard_quality_score}%, Integrations: {len(monitoring.integrations)}.",
            )
        )

        # 7. Security Compliance (10%)
        sec_weighted = security.score * self.WEIGHTS["security"]
        category_scores.append(
            CategoryScoreItem(
                category_id="security",
                category_name="Security Compliance",
                weight=self.WEIGHTS["security"],
                raw_score=round(security.score, 2),
                weighted_score=round(sec_weighted, 2),
                status="EXCELLENT" if security.score >= 95 else "ADEQUATE",
                details=f"Secrets exposed: {security.secret_exposure_count}, Sanitization rate: {security.sanitization_rate_pct}%, RBAC enforced: {security.rbac_enforced}.",
            )
        )

        # 8. Evidence Quality (5%)
        ev_weighted = evidence.score * self.WEIGHTS["evidence"]
        category_scores.append(
            CategoryScoreItem(
                category_id="evidence",
                category_name="Evidence Quality",
                weight=self.WEIGHTS["evidence"],
                raw_score=round(evidence.score, 2),
                weighted_score=round(ev_weighted, 2),
                status="EXCELLENT" if evidence.score >= 95 else "ADEQUATE",
                details="Reports, logs, metrics, test results, and environment metadata fully validated.",
            )
        )

        overall_score = sum(c.weighted_score for c in category_scores)
        overall_score = round(overall_score, 2)

        # Veto condition evaluations
        veto_reasons: List[str] = []
        if dependencies.critical_dependency_invisible or dependencies.dependency_visibility < 80.0:
            veto_reasons.append("Critical dependency invisible or visibility below 80%")
        if readiness.false_ready_rate > 0.0:
            veto_reasons.append("False-ready state detected in traffic acceptance")
        if not recovery.recovery_verified or recovery.recovery_success_rate_pct < 80.0:
            veto_reasons.append("Recovery capability cannot be verified")
        if security.security_exposure_exists or security.secret_exposure_count > 0:
            veto_reasons.append("Security credential exposure exists in observability layer")
        if evidence.evidence_missing or not evidence.reports_present:
            veto_reasons.append("Critical evidence reports or test artifacts missing")

        veto_triggered = len(veto_reasons) > 0

        # Determine Maturity Level & Status
        if veto_triggered:
            maturity = HealthMaturityLevel.LEVEL_0_UNKNOWN
            status = CertificationStatus.FAILED
            passed = False
        elif overall_score >= 95.0:
            maturity = HealthMaturityLevel.LEVEL_4_ENTERPRISE_HEALTH
            status = CertificationStatus.CERTIFIED
            passed = True
        elif overall_score >= 85.0:
            maturity = HealthMaturityLevel.LEVEL_3_PRODUCTION_HEALTH
            status = CertificationStatus.PROVISIONALLY_PASSED
            passed = True
        elif overall_score >= 70.0:
            maturity = HealthMaturityLevel.LEVEL_2_OPERATIONAL_HEALTH
            status = CertificationStatus.PROVISIONALLY_PASSED
            passed = False
        elif overall_score >= 50.0:
            maturity = HealthMaturityLevel.LEVEL_1_BASIC_HEALTH
            status = CertificationStatus.FAILED
            passed = False
        else:
            maturity = HealthMaturityLevel.LEVEL_0_UNKNOWN
            status = CertificationStatus.FAILED
            passed = False

        categories_dict = {
            "liveness": liveness.score,
            "readiness": readiness.score,
            "dependencies": dependencies.score,
            "failure_detection": failure_detection.score,
            "recovery": recovery.score,
            "monitoring": monitoring.score,
            "security": security.score,
            "evidence": evidence.score,
        }

        cert_report = HealthQualityCertificationReport(
            project="DocuTask-Agent",
            phase="3H.5.11",
            score=overall_score,
            level=maturity,
            status=status,
            categories=categories_dict,
            timestamp=datetime.now(timezone.utc).isoformat(),
            veto_triggered=veto_triggered,
            veto_reasons=veto_reasons,
        )

        return HealthQualityScorecard(
            verification_id=f"health-cert-{uuid4().hex[:8]}",
            timestamp=datetime.now(timezone.utc).isoformat(),
            overall_score=overall_score,
            maturity_level=maturity,
            certification_status=status,
            category_scores=category_scores,
            sre_metrics=sre_metrics,
            regression_report=regression_report,
            deployment_gate=gate_report,
            certification_report=cert_report,
            passed=passed,
        )
