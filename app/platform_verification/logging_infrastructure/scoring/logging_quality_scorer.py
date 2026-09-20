"""
Phase 3I.2: 6-Pillar Enterprise Logging Quality Scorer
"""
from typing import List
from datetime import datetime, timezone
from ..domain.models import (
    LoggingCertificationTier,
    ArchitectureReport,
    StructuredLoggingReport,
    CorrelationReport,
    AgentLoggingReport,
    SecurityReport,
    PerformanceReport,
    FailureTestReport,
    LoggingPillarScore,
    CertificationReport,
)
from ..domain.interfaces import ILoggingQualityScorer


class LoggingQualityScorer(ILoggingQualityScorer):
    """
    Evaluates 6 core logging categories:
      - Structured logging: 20%
      - Correlation capability: 20%
      - AI workflow visibility: 20%
      - Security protection: 15%
      - Centralization: 15%
      - Performance impact: 10%
    """

    def calculate_certification_score(
        self,
        arch_report: ArchitectureReport,
        struct_report: StructuredLoggingReport,
        corr_report: CorrelationReport,
        agent_report: AgentLoggingReport,
        sec_report: SecurityReport,
        perf_report: PerformanceReport,
        failure_report: FailureTestReport,
    ) -> CertificationReport:
        # 1. Structured Logging (20%)
        struct_score = struct_report.schema_compliance_pct if struct_report.structured_logging_passed else 0.0
        struct_weight = 20.0
        struct_weighted = (struct_score * struct_weight) / 100.0

        # 2. Correlation Capability (20%)
        corr_score = corr_report.correlation_capability_score if corr_report.end_to_end_correlated else 0.0
        corr_weight = 20.0
        corr_weighted = (corr_score * corr_weight) / 100.0

        # 3. AI Workflow Visibility (20%)
        ai_score = agent_report.ai_workflow_visibility_score if agent_report.decision_reconstruction_possible else 0.0
        ai_weight = 20.0
        ai_weighted = (ai_score * ai_weight) / 100.0

        # 4. Security Protection (15%)
        sec_score = sec_report.security_score_pct if (sec_report.secrets_prevented and sec_report.pii_masked) else 0.0
        sec_weight = 15.0
        sec_weighted = (sec_score * sec_weight) / 100.0

        # 5. Centralization (15%)
        cent_score = 100.0 if (arch_report.centralized_collection and arch_report.services_detected >= 8) else 0.0
        cent_weight = 15.0
        cent_weighted = (cent_score * cent_weight) / 100.0

        # 6. Performance Impact (10%)
        perf_score = 100.0 if (perf_report.performance_compliant and perf_report.overhead_pct < 5.0) else 0.0
        perf_weight = 10.0
        perf_weighted = (perf_score * perf_weight) / 100.0

        total_score = struct_weighted + corr_weighted + ai_weighted + sec_weighted + cent_weighted + perf_weighted
        total_score = round(total_score, 2)

        pillar_scores: List[LoggingPillarScore] = [
            LoggingPillarScore(
                pillar_name="Structured Logging Schema & Level Compliance",
                weight_pct=struct_weight,
                achieved_score_pct=round(struct_score, 2),
                weighted_score_pct=round(struct_weighted, 2),
                status="PASSED" if struct_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            LoggingPillarScore(
                pillar_name="Distributed Request Correlation Capability",
                weight_pct=corr_weight,
                achieved_score_pct=round(corr_score, 2),
                weighted_score_pct=round(corr_weighted, 2),
                status="PASSED" if corr_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            LoggingPillarScore(
                pillar_name="AI Agent Execution & Workflow Visibility",
                weight_pct=ai_weight,
                achieved_score_pct=round(ai_score, 2),
                weighted_score_pct=round(ai_weighted, 2),
                status="PASSED" if ai_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            LoggingPillarScore(
                pillar_name="Security Protection & Sensitive Data Masking",
                weight_pct=sec_weight,
                achieved_score_pct=round(sec_score, 2),
                weighted_score_pct=round(sec_weighted, 2),
                status="PASSED" if sec_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            LoggingPillarScore(
                pillar_name="Log Centralization & OTel Pipeline Readiness",
                weight_pct=cent_weight,
                achieved_score_pct=round(cent_score, 2),
                weighted_score_pct=round(cent_weighted, 2),
                status="PASSED" if cent_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            LoggingPillarScore(
                pillar_name="Performance Impact & Low Latency Overhead",
                weight_pct=perf_weight,
                achieved_score_pct=round(perf_score, 2),
                weighted_score_pct=round(perf_weighted, 2),
                status="PASSED" if perf_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
        ]

        if total_score >= 95.0:
            tier = LoggingCertificationTier.ENTERPRISE_LOGGING_READY
            granted = True
        elif total_score >= 90.0:
            tier = LoggingCertificationTier.PRODUCTION_READY
            granted = True
        elif total_score >= 80.0:
            tier = LoggingCertificationTier.IMPROVEMENT_REQUIRED
            granted = False
        else:
            tier = LoggingCertificationTier.FAILED
            granted = False

        return CertificationReport(
            report_title="Phase 3I.2 Enterprise Logging Infrastructure Certification",
            evaluated_at=datetime.now(timezone.utc).isoformat(),
            certification_tier=tier,
            overall_score_pct=total_score,
            minimum_passing_threshold_pct=95.0,
            pillar_scores=pillar_scores,
            certification_granted=granted,
            auditor="DocuTask Enterprise Observability & SRE Certification Engine"
        )
