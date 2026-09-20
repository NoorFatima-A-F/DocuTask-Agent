"""
Phase 3H.4.10.12: Observability Security Quality Scorer
"""
from typing import Dict, Any
from ..domain.interfaces import IObservabilitySecurityScorer
from ..domain.models import (
    ObservabilitySecurityScorecard,
    SecurityTier,
    DataClassificationReport,
    LogSecurityReport,
    MetricSecurityReport,
    TraceSecurityReport,
    DashboardAccessReport,
    PipelineSecurityReport,
    AISecurityReport,
)


class ObservabilitySecurityScorer(IObservabilitySecurityScorer):
    def calculate_scorecard(
        self,
        classification_report: DataClassificationReport,
        log_report: LogSecurityReport,
        metric_report: MetricSecurityReport,
        trace_report: TraceSecurityReport,
        access_report: DashboardAccessReport,
        pipeline_report: PipelineSecurityReport,
        ai_report: AISecurityReport,
    ) -> ObservabilitySecurityScorecard:
        # 1. Data classification (15%)
        data_class_score = 100.0 if classification_report.classification_policy_passed else 60.0

        # 2. Log protection (20%)
        if log_report.unmasked_leaks_count == 0 and log_report.log_security_passed:
            log_score = 100.0
        else:
            log_score = max(0.0, 100.0 - (log_report.unmasked_leaks_count * 25.0))

        # 3. Metric security (15%)
        if metric_report.metrics_failed == 0 and metric_report.metric_privacy_passed:
            metric_score = 100.0
        else:
            metric_score = max(0.0, 100.0 - (metric_report.metrics_failed * 20.0))

        # 4. Trace security (15%)
        if trace_report.trace_security_passed:
            trace_score = 100.0
        else:
            trace_score = (trace_report.compliant_spans / trace_report.total_spans_inspected) * 100.0 if trace_report.total_spans_inspected > 0 else 0.0

        # 5. Access control (15%)
        if access_report.rbac_enforcement_passed and access_report.unauthorized_attempts_blocked > 0:
            access_score = 100.0
        else:
            access_score = 60.0

        # 6. Pipeline security (10%)
        if pipeline_report.pipeline_security_passed and pipeline_report.transport_encryption_tls13:
            pipeline_score = 100.0
        else:
            pipeline_score = 50.0

        # 7. AI telemetry security (10%)
        if ai_report.ai_observability_safe and ai_report.zero_prompt_leakage_verified and ai_report.zero_response_leakage_verified:
            ai_score = 100.0
        else:
            ai_score = 40.0

        # Weighted composite score
        composite = (
            (data_class_score * 0.15)
            + (log_score * 0.20)
            + (metric_score * 0.15)
            + (trace_score * 0.15)
            + (access_score * 0.15)
            + (pipeline_score * 0.10)
            + (ai_score * 0.10)
        )

        if composite >= 95.0:
            tier = SecurityTier.ENTERPRISE_OBSERVABILITY_SECURITY_CERTIFIED
            certified = True
        elif composite >= 90.0:
            tier = SecurityTier.PRODUCTION_SECURE
            certified = True
        elif composite >= 80.0:
            tier = SecurityTier.IMPROVEMENT_REQUIRED
            certified = False
        else:
            tier = SecurityTier.FAILED
            certified = False

        return ObservabilitySecurityScorecard(
            data_classification_score=round(data_class_score, 2),
            log_protection_score=round(log_score, 2),
            metric_security_score=round(metric_score, 2),
            trace_security_score=round(trace_score, 2),
            access_control_score=round(access_score, 2),
            pipeline_security_score=round(pipeline_score, 2),
            ai_telemetry_security_score=round(ai_score, 2),
            composite_score=round(composite, 2),
            tier=tier,
            certified_enterprise_ready=certified,
        )
