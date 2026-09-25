"""
Phase 3I.3: 6-Pillar Enterprise Metrics Quality Scorer
"""
from typing import List
from datetime import datetime, timezone
from ..domain.models import (
    MetricsCertificationTier,
    MetricsArchitectureReport,
    MetricsStandardReport,
    ApplicationMetricsReport,
    AIMetricsReport,
    InfrastructureMetricsReport,
    BusinessSLAMetricsReport,
    DashboardReport,
    AlertValidationReport,
    MetricsAccuracyReport,
    MetricsSecurityReport,
    MetricsPerformanceReport,
    ChaosMetricReport,
    MetricsPillarScore,
    MetricsCertificationReport,
)
from ..domain.interfaces import IMetricsQualityScorer


class MetricsQualityScorer(IMetricsQualityScorer):
    """
    Evaluates 6 core metrics infrastructure categories:
      - Metric coverage: 20%
      - Accuracy: 20%
      - AI observability: 20%
      - Dashboard quality: 15%
      - Alert integration: 15%
      - Performance overhead: 10%
    """

    def calculate_certification_score(
        self,
        arch_report: MetricsArchitectureReport,
        std_report: MetricsStandardReport,
        app_report: ApplicationMetricsReport,
        ai_report: AIMetricsReport,
        infra_report: InfrastructureMetricsReport,
        biz_report: BusinessSLAMetricsReport,
        dash_report: DashboardReport,
        alert_report: AlertValidationReport,
        acc_report: MetricsAccuracyReport,
        sec_report: MetricsSecurityReport,
        perf_report: MetricsPerformanceReport,
        chaos_report: ChaosMetricReport,
    ) -> MetricsCertificationReport:
        # 1. Metric Coverage (20%)
        cov_valid = (arch_report.services_monitored >= 8) and std_report.standard_validation_passed and infra_report.infrastructure_healthy
        cov_score = 100.0 if cov_valid else 0.0
        cov_weight = 20.0
        cov_weighted = (cov_score * cov_weight) / 100.0

        # 2. Accuracy & Drift-Free Telemetry (20%)
        acc_valid = acc_report.drift_free and (acc_report.accuracy_pct >= 99.0) and biz_report.sla_compliance_rate_pct >= 95.0
        acc_score = acc_report.accuracy_pct if acc_valid else 0.0
        acc_weight = 20.0
        acc_weighted = (acc_score * acc_weight) / 100.0

        # 3. AI Agent & LLM Observability (20%)
        ai_valid = (ai_report.ai_observability_score >= 95.0) and len(ai_report.agent_metrics) > 0 and len(ai_report.llm_metrics) > 0
        ai_score = ai_report.ai_observability_score if ai_valid else 0.0
        ai_weight = 20.0
        ai_weighted = (ai_score * ai_weight) / 100.0

        # 4. Dashboard Quality & Visibility (15%)
        dash_valid = dash_report.all_dashboards_operational and len(dash_report.dashboards) >= 4
        dash_score = 100.0 if dash_valid else 0.0
        dash_weight = 15.0
        dash_weighted = (dash_score * dash_weight) / 100.0

        # 5. Alert Integration & Chaos Reaction (15%)
        alert_valid = alert_report.alerting_pipeline_verified and chaos_report.all_scenarios_verified
        alert_score = 100.0 if alert_valid else 0.0
        alert_weight = 15.0
        alert_weighted = (alert_score * alert_weight) / 100.0

        # 6. Performance Overhead & Security (10%)
        perf_valid = perf_report.overhead_compliant and (perf_report.cpu_overhead_pct < 3.0) and sec_report.security_compliant
        perf_score = 100.0 if perf_valid else 0.0
        perf_weight = 10.0
        perf_weighted = (perf_score * perf_weight) / 100.0

        total_score = cov_weighted + acc_weighted + ai_weighted + dash_weighted + alert_weighted + perf_weighted
        total_score = round(total_score, 2)

        pillar_scores: List[MetricsPillarScore] = [
            MetricsPillarScore(
                pillar_name="Metric Coverage & Prometheus Standards",
                weight_pct=cov_weight,
                achieved_score_pct=round(cov_score, 2),
                weighted_score_pct=round(cov_weighted, 2),
                status="PASSED" if cov_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            MetricsPillarScore(
                pillar_name="Metrics Ingestion Accuracy & Drift-Free Counter",
                weight_pct=acc_weight,
                achieved_score_pct=round(acc_score, 2),
                weighted_score_pct=round(acc_weighted, 2),
                status="PASSED" if acc_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            MetricsPillarScore(
                pillar_name="AI Agent Telemetry & LLM Provider Observability",
                weight_pct=ai_weight,
                achieved_score_pct=round(ai_score, 2),
                weighted_score_pct=round(ai_weighted, 2),
                status="PASSED" if ai_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            MetricsPillarScore(
                pillar_name="Grafana Operational Dashboards Quality",
                weight_pct=dash_weight,
                achieved_score_pct=round(dash_score, 2),
                weighted_score_pct=round(dash_weighted, 2),
                status="PASSED" if dash_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            MetricsPillarScore(
                pillar_name="Metric-Driven Alerting & Chaos Reaction",
                weight_pct=alert_weight,
                achieved_score_pct=round(alert_score, 2),
                weighted_score_pct=round(alert_weighted, 2),
                status="PASSED" if alert_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            MetricsPillarScore(
                pillar_name="Low Performance Overhead & Label Security",
                weight_pct=perf_weight,
                achieved_score_pct=round(perf_score, 2),
                weighted_score_pct=round(perf_weighted, 2),
                status="PASSED" if perf_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
        ]

        if total_score >= 95.0:
            tier = MetricsCertificationTier.ENTERPRISE_METRICS_READY
            granted = True
        elif total_score >= 90.0:
            tier = MetricsCertificationTier.PRODUCTION_READY
            granted = True
        elif total_score >= 80.0:
            tier = MetricsCertificationTier.IMPROVEMENT_REQUIRED
            granted = False
        else:
            tier = MetricsCertificationTier.FAILED
            granted = False

        return MetricsCertificationReport(
            report_title="Phase 3I.3 Enterprise Metrics Infrastructure Certification",
            evaluated_at=datetime.now(timezone.utc).isoformat(),
            certification_tier=tier,
            overall_score_pct=total_score,
            minimum_passing_threshold_pct=95.0,
            pillar_scores=pillar_scores,
            certification_granted=granted,
            auditor="DocuTask Enterprise Observability & SRE Metrics Certification Engine"
        )
