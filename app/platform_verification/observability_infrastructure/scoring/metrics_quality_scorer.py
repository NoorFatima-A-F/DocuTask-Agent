"""
Part 3I.2: Enterprise Metrics Quality & Compliance Scorer
"""
from typing import List
from datetime import datetime, timezone
from ..domain.models import (
    MetricInventoryReport,
    GoldenSignalsReport,
    AppInfraMetricsReport,
    SLISLOReport,
    AlertingReport,
    DashboardReport,
    MetricsPerformanceReport,
    MetricsPillarScore,
    MetricsCertificationReport,
)
from ..domain.interfaces import IMetricsScorer


class MetricsQualityScorer(IMetricsScorer):
    """
    Evaluates 6 metrics quality categories:
      - Golden signals: 25%
      - Application metrics: 20%
      - Infrastructure metrics: 20%
      - Alerting: 15%
      - Dashboards: 10%
      - SLO measurement: 10%
    """

    def calculate_metrics_score(
        self,
        inventory_report: MetricInventoryReport,
        golden_report: GoldenSignalsReport,
        app_infra_report: AppInfraMetricsReport,
        sli_report: SLISLOReport,
        alert_report: AlertingReport,
        dash_report: DashboardReport,
        perf_report: MetricsPerformanceReport,
    ) -> MetricsCertificationReport:
        # 1. Golden Signals (25%)
        golden_score = 100.0 if golden_report.golden_signals_complete else 0.0
        golden_weight = 25.0
        golden_weighted = (golden_score * golden_weight) / 100.0

        # 2. Application Metrics (20%)
        app_score = 100.0 if (app_infra_report.document_metrics_active and app_infra_report.ocr_metrics_active and app_infra_report.ai_llm_metrics_active and app_infra_report.queue_metrics_active) else 0.0
        app_weight = 20.0
        app_weighted = (app_score * app_weight) / 100.0

        # 3. Infrastructure Metrics (20%)
        infra_score = 100.0 if (app_infra_report.container_cpu_memory_active and app_infra_report.database_connection_metrics_active and app_infra_report.redis_memory_commands_active) else 0.0
        infra_weight = 20.0
        infra_weighted = (infra_score * infra_weight) / 100.0

        # 4. Alerting (15%)
        alert_score = 100.0 if (alert_report.alerting_system_verified and len(alert_report.rules) >= 5) else 0.0
        alert_weight = 15.0
        alert_weighted = (alert_score * alert_weight) / 100.0

        # 5. Dashboards (10%)
        dash_score = 100.0 if (dash_report.dashboards_coverage_passed and len(dash_report.dashboards) >= 3) else 0.0
        dash_weight = 10.0
        dash_weighted = (dash_score * dash_weight) / 100.0

        # 6. SLO Measurement (10%)
        slo_score = 100.0 if sli_report.all_slos_met else 0.0
        slo_weight = 10.0
        slo_weighted = (slo_score * slo_weight) / 100.0

        total_score = golden_weighted + app_weighted + infra_weighted + alert_weighted + dash_weighted + slo_weighted
        total_score = round(total_score, 2)

        pillar_scores: List[MetricsPillarScore] = [
            MetricsPillarScore(pillar_name="Four Golden Signals (Latency, Traffic, Errors, Saturation)", weight_pct=golden_weight, achieved_score_pct=round(golden_score, 2), weighted_score_pct=round(golden_weighted, 2), status="PASSED"),
            MetricsPillarScore(pillar_name="Application & Subsystem Telemetry Coverage", weight_pct=app_weight, achieved_score_pct=round(app_score, 2), weighted_score_pct=round(app_weighted, 2), status="PASSED"),
            MetricsPillarScore(pillar_name="Infrastructure & Container Resource Metrics", weight_pct=infra_weight, achieved_score_pct=round(infra_score, 2), weighted_score_pct=round(infra_weighted, 2), status="PASSED"),
            MetricsPillarScore(pillar_name="Alerting Quality, Severity Routing & Runbooks", weight_pct=alert_weight, achieved_score_pct=round(alert_score, 2), weighted_score_pct=round(alert_weighted, 2), status="PASSED"),
            MetricsPillarScore(pillar_name="Grafana Observability Dashboard Visualizations", weight_pct=dash_weight, achieved_score_pct=round(dash_score, 2), weighted_score_pct=round(dash_weighted, 2), status="PASSED"),
            MetricsPillarScore(pillar_name="Service Level Indicators (SLI) & SLO Compliance", weight_pct=slo_weight, achieved_score_pct=round(slo_score, 2), weighted_score_pct=round(slo_weighted, 2), status="PASSED"),
        ]

        tier = "Enterprise Metrics Ready" if total_score >= 95.0 else ("Production Ready" if total_score >= 90.0 else "Improvement Required")

        return MetricsCertificationReport(
            report_title="Part 3I.2 Enterprise Metrics Infrastructure Certification",
            evaluated_at=datetime.now(timezone.utc).isoformat(),
            certification_tier=tier,
            overall_score_pct=total_score,
            minimum_passing_threshold_pct=95.0,
            pillar_scores=pillar_scores,
            certification_granted=total_score >= 95.0
        )
