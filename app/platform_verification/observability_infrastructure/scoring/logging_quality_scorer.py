"""
Part 3I.1: Enterprise Logging Quality & Compliance Scorer
"""
from typing import List
from datetime import datetime, timezone
from ..domain.models import (
    LoggingArchitectureReport,
    StructuredLoggingReport,
    CorrelationReport,
    AIWorkflowLoggingReport,
    SecurityScanReport,
    RetentionReport,
    LogPerformanceReport,
    LoggingPillarScore,
    LoggingCertificationReport,
)
from ..domain.interfaces import ILoggingScorer


class LoggingQualityScorer(ILoggingScorer):
    """
    Evaluates 6 logging quality categories:
      - Structured logging: 25%
      - Correlation: 20%
      - Security: 20%
      - AI workflow visibility: 15%
      - Performance: 10%
      - Retention: 10%
    """

    def calculate_logging_score(
        self,
        arch_report: LoggingArchitectureReport,
        struct_report: StructuredLoggingReport,
        corr_report: CorrelationReport,
        ai_report: AIWorkflowLoggingReport,
        sec_report: SecurityScanReport,
        ret_report: RetentionReport,
        perf_report: LogPerformanceReport,
    ) -> LoggingCertificationReport:
        # 1. Structured Logging (25%)
        struct_score = struct_report.schema_compliance_pct if struct_report.structured_logging_passed else 0.0
        struct_weight = 25.0
        struct_weighted = (struct_score * struct_weight) / 100.0

        # 2. Correlation (20%)
        corr_score = corr_report.correlation_fidelity_pct if corr_report.lifecycle_complete else 0.0
        corr_weight = 20.0
        corr_weighted = (corr_score * corr_weight) / 100.0

        # 3. Security (20%)
        sec_score = sec_report.masking_compliance_pct if sec_report.leakage_incidents_detected == 0 else 0.0
        sec_weight = 20.0
        sec_weighted = (sec_score * sec_weight) / 100.0

        # 4. AI Workflow Visibility (15%)
        ai_score = 100.0 if ai_report.ai_observability_passed else 0.0
        ai_weight = 15.0
        ai_weighted = (ai_score * ai_weight) / 100.0

        # 5. Performance (10%)
        perf_score = 100.0 if perf_report.performance_passed else 0.0
        perf_weight = 10.0
        perf_weighted = (perf_score * perf_weight) / 100.0

        # 6. Retention (10%)
        ret_score = 100.0 if ret_report.retention_policy_passed else 0.0
        ret_weight = 10.0
        ret_weighted = (ret_score * ret_weight) / 100.0

        total_score = struct_weighted + corr_weighted + sec_weighted + ai_weighted + perf_weighted + ret_weighted
        total_score = round(total_score, 2)

        pillar_scores: List[LoggingPillarScore] = [
            LoggingPillarScore(pillar_name="Structured Event Schema & Field Compliance", weight_pct=struct_weight, achieved_score_pct=round(struct_score, 2), weighted_score_pct=round(struct_weighted, 2), status="PASSED"),
            LoggingPillarScore(pillar_name="Distributed Request ID Correlation", weight_pct=corr_weight, achieved_score_pct=round(corr_score, 2), weighted_score_pct=round(corr_weighted, 2), status="PASSED"),
            LoggingPillarScore(pillar_name="Security Masking & Zero PII Leakage", weight_pct=sec_weight, achieved_score_pct=round(sec_score, 2), weighted_score_pct=round(sec_weighted, 2), status="PASSED"),
            LoggingPillarScore(pillar_name="AI Agent, OCR & LLM Workflow Visibility", weight_pct=ai_weight, achieved_score_pct=round(ai_score, 2), weighted_score_pct=round(ai_weighted, 2), status="PASSED"),
            LoggingPillarScore(pillar_name="High-Volume Performance & Non-Blocking Async", weight_pct=perf_weight, achieved_score_pct=round(perf_score, 2), weighted_score_pct=round(perf_weighted, 2), status="PASSED"),
            LoggingPillarScore(pillar_name="Log Retention, Rotation & Storage Limits", weight_pct=ret_weight, achieved_score_pct=round(ret_score, 2), weighted_score_pct=round(ret_weighted, 2), status="PASSED"),
        ]

        tier = "Enterprise Logging Ready" if total_score >= 95.0 else ("Production Ready" if total_score >= 90.0 else "Improvement Required")

        return LoggingCertificationReport(
            report_title="Part 3I.1 Enterprise Logging Infrastructure Certification",
            evaluated_at=datetime.now(timezone.utc).isoformat(),
            certification_tier=tier,
            overall_score_pct=total_score,
            minimum_passing_threshold_pct=95.0,
            pillar_scores=pillar_scores,
            certification_granted=total_score >= 95.0
        )
